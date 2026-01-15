"""
ChatPro AI Analyzer - Main API
Version: 3.1.1-FIXED
Fixed: API signature + return format + error handling
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl, Field
from typing import Literal, Optional, Dict
import asyncio
import uuid
import logging
from pathlib import Path
from datetime import datetime

from app.pipeline import ChatProPipeline

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="ChatPro AI Analyzer",
    version="3.1.1-FIXED",
    description="AI-powered website analysis for chatbot recommendations"
)

# CORS (optional - enable if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class AnalysisRequest(BaseModel):
    website_url: HttpUrl
    industry: Literal["hotel", "fitness", "salon", "immobilien", "restaurant", "vacation_rental", "fahrschule", "other"]
    email: str
    company_name: Optional[str] = None
    max_pages: int = Field(default=10, ge=1, le=50)

# Initialize pipeline (NO parameters!)
try:
    pipeline = ChatProPipeline()
    logger.info("✅ Pipeline initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize pipeline: {e}")
    raise

# In-memory storage (replace with DB in production)
analyses: Dict[str, dict] = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "ChatPro AI Analyzer",
        "version": "3.1.1-FIXED",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "analyze": "/api/analyze",
            "status": "/api/status/{analysis_id}",
            "report": "/api/report/{analysis_id}"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "pipeline": "initialized",
            "filesystem": "writable" if Path("/tmp").is_dir() else "error"
        }
    }

@app.post("/api/analyze")
async def analyze_website(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Start website analysis
    
    Returns analysis_id immediately, analysis runs in background
    """
    analysis_id = str(uuid.uuid4())
    
    logger.info(f"[{analysis_id[:8]}] 📨 New analysis request for {request.website_url}")
    
    # Initialize status
    analyses[analysis_id] = {
        "analysis_id": analysis_id,
        "status": "processing",
        "progress": 0,
        "website_url": str(request.website_url),
        "industry": request.industry,
        "email": request.email,
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Run analysis in background
    background_tasks.add_task(
        run_analysis_pipeline,
        analysis_id,
        request
    )
    
    return {
        "analysis_id": analysis_id,
        "status": "processing",
        "message": "Analysis started. Use /api/status/{analysis_id} to check progress.",
        "estimated_time_seconds": 120
    }

async def run_analysis_pipeline(analysis_id: str, request: AnalysisRequest):
    """
    Background task to run the full pipeline
    
    FIXED: Correct API signature + proper error handling + return format wrapper
    """
    try:
        logger.info(f"[{analysis_id[:8]}] 🚀 Starting pipeline...")
        
        # Update progress
        analyses[analysis_id]["progress"] = 10
        analyses[analysis_id]["current_step"] = "Initializing"
        
        # Define output path
        output_filename = f"/tmp/{analysis_id}.pdf"
        
        # Update progress
        analyses[analysis_id]["progress"] = 20
        analyses[analysis_id]["current_step"] = "Crawling website"
        
        # ✅ FIXED: Call pipeline with CORRECT signature
        logger.info(f"[{analysis_id[:8]}] Calling pipeline.generate_report()")
        
        analysis_data = await pipeline.generate_report(
            url=str(request.website_url),  # ✅ CORRECT: url (not website_url)
            output_filename=output_filename,  # ✅ CORRECT: output_filename
            max_pages=request.max_pages  # ✅ CORRECT: max_pages
        )
        
        logger.info(f"[{analysis_id[:8]}] ✅ Pipeline completed successfully")
        
        # ✅ FIXED: Wrap result to match expected format
        result = {
            "status": "completed",
            "report_path": output_filename,
            "analysis_data": analysis_data  # Full AnalysisResult object
        }
        
        # Verify PDF exists
        pdf_exists = Path(output_filename).exists()
        if not pdf_exists:
            logger.warning(f"[{analysis_id[:8]}] ⚠️ PDF file not found at {output_filename}")
        
        # Update status with complete result
        analyses[analysis_id].update({
            "status": "completed",
            "progress": 100,
            "current_step": "Completed",
            "result": result,
            "report_path": output_filename,
            "pdf_exists": pdf_exists,
            "completed_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"[{analysis_id[:8]}] ✅ Analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"[{analysis_id[:8]}] ❌ Analysis failed: {str(e)}", exc_info=True)
        
        analyses[analysis_id].update({
            "status": "failed",
            "progress": 0,
            "current_step": "Failed",
            "error": str(e),
            "error_type": type(e).__name__,
            "failed_at": datetime.utcnow().isoformat()
        })

@app.get("/api/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Check analysis status"""
    
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analyses[analysis_id]

@app.get("/api/report/{analysis_id}")
async def get_report(analysis_id: str):
    """Download PDF report"""
    
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis = analyses[analysis_id]
    
    if analysis["status"] == "processing":
        raise HTTPException(
            status_code=400, 
            detail=f"Analysis is still processing (progress: {analysis['progress']}%)"
        )
    
    if analysis["status"] == "failed":
        raise HTTPException(
            status_code=400,
            detail=f"Analysis failed: {analysis.get('error', 'Unknown error')}"
        )
    
    report_path = analysis.get("report_path")
    
    if not report_path:
        raise HTTPException(status_code=404, detail="Report path not found")
    
    if not Path(report_path).exists():
        raise HTTPException(
            status_code=404,
            detail=f"Report file not found at {report_path}"
        )
    
    # Return PDF file
    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=f"chatpro_analysis_{analysis_id[:8]}.pdf"
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 ChatPro AI Analyzer V3.1.1-FIXED starting up...")
    logger.info("✅ All systems ready")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 ChatPro AI Analyzer shutting down...")
