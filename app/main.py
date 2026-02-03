"""
CHATPRO AI ANALYZER - MAIN BACKEND APPLICATION (FIXED ASYNC)
FastAPI backend with proper async/sync handling for BackgroundTasks
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional, Literal
import os
from datetime import datetime
import uuid
import asyncio
import logging

# Import pipeline
from .pipeline import AnalysisPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="ChatPro AI Analyzer",
    description="Kostenlose Website-Analyse für Hotels, Fitness, Salons und mehr",
    version="1.0.1"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pipeline
pipeline = AnalysisPipeline(output_dir="/mnt/user-data/outputs")

# Request Models
class AnalysisRequest(BaseModel):
    website_url: str
    industry: Literal["hotel", "fitness", "salon", "immobilien", "restaurant", "vacation_rental", "fahrschule", "other"]
    email: EmailStr
    company_name: Optional[str] = None

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: Literal["processing", "completed", "failed"]
    message: str
    report_url: Optional[str] = None
    estimated_time: Optional[int] = None
    data: Optional[dict] = None

# Status Storage (in-memory for now)
analysis_status = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "ChatPro AI Analyzer",
        "version": "1.0.1",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "analyze": "/api/analyze",
            "status": "/api/status/{analysis_id}",
            "report": "/api/report/{analysis_id}"
        }
    }

@app.get("/health")
async def health():
    """Health check for Railway"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


def process_analysis_task_sync(analysis_id: str, request: AnalysisRequest):
    """
    SYNCHRONOUS wrapper for async pipeline
    
    This is required because FastAPI BackgroundTasks expects a sync function.
    We create a new event loop to run the async pipeline.
    """
    
    logger.info(f"[{analysis_id[:8]}] Background task started")
    
    # Create new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Update status to processing
        analysis_status[analysis_id]["status"] = "processing"
        analysis_status[analysis_id]["progress"] = 10
        
        logger.info(f"[{analysis_id[:8]}] Running async pipeline...")
        
        # Run async pipeline in sync context
        result = loop.run_until_complete(
            pipeline.process(
                website_url=request.website_url,
                industry=request.industry,
                email=request.email,
                company_name=request.company_name,
                analysis_id=analysis_id
            )
        )
        
        logger.info(f"[{analysis_id[:8]}] Pipeline completed with status: {result.get('status')}")
        
        # Update status based on result
        if result["status"] == "completed":
            analysis_status[analysis_id].update({
                "status": "completed",
                "progress": 100,
                "report_path": result["report_path"],
                "report_url": f"/api/report/{analysis_id}",
                "data": result.get("analysis_data", {}),
                "completed_at": datetime.utcnow().isoformat()
            })
            logger.info(f"[{analysis_id[:8]}] ✅ Analysis completed successfully")
        else:
            analysis_status[analysis_id].update({
                "status": "failed",
                "error": result.get("error", "Unknown error"),
                "failed_at": datetime.utcnow().isoformat()
            })
            logger.error(f"[{analysis_id[:8]}] ❌ Analysis failed: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"[{analysis_id[:8]}] ❌ Background task exception: {str(e)}")
        analysis_status[analysis_id].update({
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.utcnow().isoformat()
        })
    finally:
        # Always close the loop
        loop.close()
        logger.info(f"[{analysis_id[:8]}] Background task finished")


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_website(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Start website analysis
    
    Returns immediately with 202 status and analysis_id.
    Actual processing happens in background.
    
    Process:
    1. Generate analysis_id
    2. Initialize status
    3. Start background task
    4. Return 202 with analysis_id
    5. Client polls /api/status/{analysis_id}
    6. When complete, client downloads /api/report/{analysis_id}
    """
    
    # Generate unique analysis ID
    analysis_id = str(uuid.uuid4())
    
    logger.info(f"[{analysis_id[:8]}] New analysis request received")
    logger.info(f"[{analysis_id[:8]}]   URL: {request.website_url}")
    logger.info(f"[{analysis_id[:8]}]   Industry: {request.industry}")
    logger.info(f"[{analysis_id[:8]}]   Email: {request.email}")
    
    # Initialize status
    analysis_status[analysis_id] = {
        "status": "processing",
        "created_at": datetime.utcnow().isoformat(),
        "website_url": request.website_url,
        "industry": request.industry,
        "email": request.email,
        "company_name": request.company_name,
        "progress": 0
    }
    
    # Add SYNC background task
    background_tasks.add_task(
        process_analysis_task_sync,  # ← SYNC function!
        analysis_id,
        request
    )
    
    logger.info(f"[{analysis_id[:8]}] Background task scheduled")
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status="processing",
        message="Analyse gestartet. Dies dauert ca. 30-60 Sekunden.",
        estimated_time=60
    )


@app.get("/api/status/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_status(analysis_id: str):
    """
    Check analysis status
    
    Client should poll this endpoint every 2-5 seconds
    until status is 'completed' or 'failed'.
    """
    
    if analysis_id not in analysis_status:
        raise HTTPException(
            status_code=404,
            detail="Analysis ID not found"
        )
    
    status = analysis_status[analysis_id]
    
    # Build message
    if status["status"] == "processing":
        message = f"Analyse läuft... ({status.get('progress', 0)}%)"
    elif status["status"] == "completed":
        message = "Analyse abgeschlossen! PDF-Report ist verfügbar."
    else:
        message = f"Fehler: {status.get('error', 'Unknown')}"
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status=status["status"],
        message=message,
        report_url=status.get("report_url"),
        data=status.get("data")
    )


@app.get("/api/report/{analysis_id}")
async def get_report(analysis_id: str):
    """
    Download PDF report
    
    Returns FileResponse with PDF attachment.
    """
    
    if analysis_id not in analysis_status:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    
    status = analysis_status[analysis_id]
    
    if status["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Report not ready yet. Current status: " + status["status"]
        )
    
    report_path = status.get("report_path")
    
    if not report_path or not os.path.exists(report_path):
        raise HTTPException(
            status_code=404,
            detail="Report file not found"
        )
    
    # Determine media type
    if report_path.endswith('.pdf'):
        media_type = "application/pdf"
        filename = f"chatpro-ai-analyse-{analysis_id[:8]}.pdf"
    else:
        media_type = "text/html"
        filename = f"chatpro-ai-analyse-{analysis_id[:8]}.html"
    
    logger.info(f"[{analysis_id[:8]}] Serving report: {filename}")
    
    return FileResponse(
        report_path,
        media_type=media_type,
        filename=filename
    )


@app.get("/api/stats")
async def get_stats():
    """
    Get analyzer statistics
    """
    
    total = len(analysis_status)
    completed = sum(1 for s in analysis_status.values() if s["status"] == "completed")
    processing = sum(1 for s in analysis_status.values() if s["status"] == "processing")
    failed = sum(1 for s in analysis_status.values() if s["status"] == "failed")
    
    # Industry breakdown
    industries = {}
    for status in analysis_status.values():
        industry = status.get("industry", "unknown")
        industries[industry] = industries.get(industry, 0) + 1
    
    return {
        "total_analyses": total,
        "completed": completed,
        "processing": processing,
        "failed": failed,
        "success_rate": round(completed / total * 100, 1) if total > 0 else 0,
        "industries": industries,
        "timestamp": datetime.utcnow().isoformat()
    }


# Error Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global error handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


# ==================== PARTNER WEBHOOK ====================
import httpx

class PartnerRequest(BaseModel):
    name: str
    company: str
    email: EmailStr
    phone: str
    website: str

@app.post("/api/partner")
async def create_partner(request: PartnerRequest):
    """Receive partner application and save to Notion"""
    
    NOTION_KEY = os.getenv("NOTION_API_KEY")
    DATABASE_ID = "2fc040f31f9d81c29f31dc85b4f9b106"
    
    if not NOTION_KEY:
        raise HTTPException(status_code=500, detail="Notion API key not configured")
    
    notion_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": request.name}}]},
            "Firma": {"rich_text": [{"text": {"content": request.company}}]},
            "Email": {"email": request.email},
            "Telefon": {"phone_number": request.phone},
            "Website": {"url": request.website},
            "Status": {"select": {"name": "Neu"}},
            "Eingegangen": {"date": {"start": datetime.utcnow().strftime("%Y-%m-%d")}}
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.notion.com/v1/pages",
            headers={
                "Authorization": f"Bearer {NOTION_KEY}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            },
            json=notion_data
        )
    
    if response.status_code != 200:
        print(f"Notion error: {response.text}")
        raise HTTPException(status_code=500, detail="Failed to save to Notion")
    
    return {"success": True, "message": "Partner application received"}
