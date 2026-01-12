"""
CHATPRO AI ANALYZER - MAIN BACKEND APPLICATION (UPDATED)
FastAPI backend with complete pipeline integration
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

# Import pipeline
from .pipeline import AnalysisPipeline

# Initialize FastAPI
app = FastAPI(
    title="ChatPro AI Analyzer",
    description="Kostenlose Website-Analyse für Hotels, Fitness, Salons und mehr",
    version="1.0.0"
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
    website_url: str  # Changed from HttpUrl for flexibility
    industry: Literal["hotel", "fitness", "salon", "immobilien", "restaurant", "other"]
    email: EmailStr
    company_name: Optional[str] = None

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: Literal["processing", "completed", "failed"]
    message: str
    report_url: Optional[str] = None
    estimated_time: Optional[int] = None  # seconds
    data: Optional[dict] = None

# Status Storage (in-memory for now)
analysis_status = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "ChatPro AI Analyzer",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "analyze": "/api/analyze",
            "status": "/api/status/{analysis_id}",
            "report": "/api/report/{analysis_id}"
        }
    }

async def process_analysis_task(analysis_id: str, request: AnalysisRequest):
    """
    Background task to process analysis
    """
    
    try:
        # Update status
        analysis_status[analysis_id]["status"] = "processing"
        analysis_status[analysis_id]["progress"] = 10
        
        # Run pipeline
        result = await pipeline.process(
            website_url=request.website_url,
            industry=request.industry,
            email=request.email,
            company_name=request.company_name
        )
        
        if result["status"] == "completed":
            analysis_status[analysis_id].update({
                "status": "completed",
                "progress": 100,
                "report_path": result["report_path"],
                "report_url": f"/api/report/{analysis_id}",
                "data": result.get("analysis_data", {}),
                "completed_at": datetime.utcnow().isoformat()
            })
        else:
            analysis_status[analysis_id].update({
                "status": "failed",
                "error": result.get("error", "Unknown error"),
                "failed_at": datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        analysis_status[analysis_id].update({
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.utcnow().isoformat()
        })

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_website(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Start website analysis
    
    Process:
    1. Validate URL
    2. Crawl website
    3. Analyze with AI
    4. Generate PDF
    5. Send email (TODO)
    6. Save to Brevo CRM (TODO)
    """
    
    # Generate unique analysis ID
    analysis_id = str(uuid.uuid4())
    
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
    
    # Add background task
    background_tasks.add_task(
        process_analysis_task,
        analysis_id,
        request
    )
    
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
    Download PDF/HTML report
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
        "industries": industries
    }

# Error Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global error handler"""
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
