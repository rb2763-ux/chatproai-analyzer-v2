"""
ChatPro AI - Analysis Pipeline
PRODUCTION-READY VERSION with proper error handling and logging
"""
import os
import uuid
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

from .crawler import WebsiteCrawler
from .analyzer import AIAnalyzer
from .pdf_generator import PDFReportGenerator
from .brevo_crm import BrevoCRM
from .sources_database import get_sources_for_industry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisPipeline:
    """
    Complete analysis pipeline orchestrating all components
    """
    
    def __init__(self, output_dir: str = "/mnt/user-data/outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.crawler = WebsiteCrawler()
        self.analyzer = AIAnalyzer()
        self.pdf_generator = PDFReportGenerator()
        self.brevo_crm = BrevoCRM()
        
        logger.info(f"Pipeline initialized with output_dir: {output_dir}")
    
    async def process(
        self,
        website_url: str,
        industry: str,
        email: str,
        company_name: str,
        analysis_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run complete analysis pipeline
        
        Args:
            website_url: URL to analyze
            industry: Industry category
            email: Contact email
            company_name: Company name
            analysis_id: Optional analysis ID (generates if not provided)
            
        Returns:
            Dict with analysis results and paths
        """
        
        if not analysis_id:
            analysis_id = str(uuid.uuid4())
        
        logger.info(f"[{analysis_id[:8]}] Starting analysis for {website_url}")
        
        try:
            # STEP 1: Crawl website
            logger.info(f"[{analysis_id[:8]}] Step 1/5: Crawling {website_url}...")
            crawler_data = await self.crawler.crawl(website_url)
            
            # Defensive check
            if not crawler_data or not isinstance(crawler_data, dict):
                logger.error(f"[{analysis_id[:8]}] Invalid crawler_data: {type(crawler_data)}")
                crawler_data = {}
            
            logger.info(f"[{analysis_id[:8]}] Crawl complete. Has chatbot: {crawler_data.get('has_chatbot', False)}")
            
            # STEP 2: Get industry sources (BEFORE analysis!)
            logger.info(f"[{analysis_id[:8]}] Step 2/5: Loading industry sources...")
            try:
                sources = get_sources_for_industry(industry)
                logger.info(f"[{analysis_id[:8]}] Loaded {len(sources)} sources for industry: {industry}")
            except Exception as e:
                logger.error(f"[{analysis_id[:8]}] Failed to load sources: {e}")
                sources = []
            
            # STEP 3: AI Analysis (WITH sources!)
            logger.info(f"[{analysis_id[:8]}] Step 3/5: Running AI analysis...")
            analysis_result = await self.analyzer.analyze(
                crawler_data=crawler_data,
                industry=industry,
                company_name=company_name,
                sources=sources  # â† PASS SOURCES HERE!
            )
            
            # Defensive check
            if not analysis_result or not isinstance(analysis_result, dict):
                logger.error(f"[{analysis_id[:8]}] Invalid analysis_result: {type(analysis_result)}")
                analysis_result = {}
            
            logger.info(f"[{analysis_id[:8]}] Analysis complete")
            
            # STEP 4: Generate PDF Report
            pdf_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 4/5: Generating PDF report...")
            
            pdf_path = os.path.join(self.output_dir, f"report_{analysis_id}.pdf")
            
            try:
                # analysis_result now contains crawler_summary and methodology_details
                # analysis_result contains crawler_summary and methodology_details
                report_path = self.pdf_generator.generate_report(
                    analysis_data=analysis_result,
                    output_filename=f"report_{analysis_id}.pdf"
                )
                
                pdf_duration = (datetime.now() - pdf_start).total_seconds()
                logger.info(f"[{analysis_id[:8]}] PDF generated in {pdf_duration:.1f}s: {report_path}")
                
            except Exception as pdf_error:
                logger.error(f"[{analysis_id[:8]}] PDF generation failed: {pdf_error}")
                logger.error(traceback.format_exc())
                report_path = None
            
            # STEP 5: Save to Brevo CRM
            crm_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 5/5: Saving to Brevo CRM...")
            
            try:
                # Extract ROI data
                roi_data = analysis_result.get("roi_calculation", {})
                if not isinstance(roi_data, dict):
                    logger.warning(f"[{analysis_id[:8]}] Invalid roi_data type: {type(roi_data)}, using empty dict")
                    roi_data = {}
                
                # Extract chatbot_priority
                chatbot_priority = analysis_result.get("chatbot_priority", "medium")
                if not isinstance(chatbot_priority, str):
                    chatbot_priority = "medium"
                
                crm_response = self.brevo_crm.save_lead(
                    email=email,
                    company_name=company_name,
                    website_url=website_url,
                    industry=industry,
                    roi_monat=int(roi_data.get("monthly_roi_euro", 0)),
                    has_chatbot=crawler_data.get("has_chatbot", False),
                    chatbot_priority=chatbot_priority,
                    analysis_id=analysis_id,
                    chatbot_type=crawler_data.get("chatbot_type", "")
                )
                
                logger.info(f"[{analysis_id[:8]}] Lead saved to Brevo: {crm_response}")
                
            except Exception as crm_error:
                logger.error(f"[{analysis_id[:8]}] Brevo CRM save failed: {crm_error}")
                logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
                crm_response = None
            
            crm_duration = (datetime.now() - crm_start).total_seconds()
            logger.info(f"[{analysis_id[:8]}] CRM step completed in {crm_duration:.1f}s")
            
            # Build result
            result = {
                "analysis_id": analysis_id,
                "status": "completed",
                "crawler_data": crawler_data,
                "analysis_data": analysis_result,
                "report_path": report_path,
                "crm_response": crm_response,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"[{analysis_id[:8]}] Pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"[{analysis_id[:8]}] Pipeline failed: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "analysis_id": analysis_id,
                "status": "failed",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "timestamp": datetime.now().isoformat()
            }

