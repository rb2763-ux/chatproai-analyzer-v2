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

# Setup logger
logger = logging.getLogger("app.pipeline")


class AnalysisPipeline:
    """Production-ready analysis pipeline with comprehensive error handling"""
    
    def __init__(self, output_dir: str = "/mnt/user-data/outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.crawler = WebCrawler()
        self.analyzer = AIAnalyzer()
        self.pdf_generator = PDFReportGenerator()
        self.brevo_crm = BrevoCRM()
        
        logger.info(f"Pipeline initialized. Output dir: {output_dir}")
    
    async def process(
        self,
        website_url: str,
        industry: str,
        email: str,
        company_name: str,
        analysis_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process complete analysis pipeline with comprehensive error handling
        
        Returns:
            Dict with status, analysis_id, and results or error information
        """
        if not analysis_id:
            analysis_id = str(uuid.uuid4())
        
        start_time = datetime.now()
        
        logger.info(f"[{analysis_id[:8]}] Starting analysis for {website_url}")
        logger.info(f"[{analysis_id[:8]}] Industry: {industry}, Company: {company_name}")
        
        try:
            # STEP 1: Web Crawling
            crawl_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 1/4: Crawling {website_url}...")
            
            try:
                crawler_data = await self.crawler.crawl(website_url)
                
                # Defensive check
                if not crawler_data or not isinstance(crawler_data, dict):
                    logger.error(f"[{analysis_id[:8]}] Invalid crawler_data: {type(crawler_data)}")
                    crawler_data = {}
                    
            except Exception as crawl_error:
                logger.error(f"[{analysis_id[:8]}] Crawling failed: {str(crawl_error)}")
                logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
                crawler_data = {}
            
            crawl_time = (datetime.now() - crawl_start).total_seconds()
            logger.info(f"[{analysis_id[:8]}] ✅ Crawling complete ({crawl_time:.1f}s)")
            
            # STEP 2: AI Analysis
            analysis_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 2/4: AI Analysis with OpenAI...")
            
            try:
                # Get relevant sources
                sources = get_sources_for_industry(industry)
                logger.debug(f"[{analysis_id[:8]}] Using {len(sources)} sources for {industry}")
                
                analysis_result = self.analyzer.analyze(
                    crawler_data=crawler_data,
                    industry=industry,
                    sources=sources
                )
                
                # Defensive check
                if not analysis_result or not isinstance(analysis_result, dict):
                    logger.error(f"[{analysis_id[:8]}] Invalid analysis_result: {type(analysis_result)}")
                    raise ValueError("Analysis returned invalid data structure")
                
            except Exception as analysis_error:
                logger.error(f"[{analysis_id[:8]}] AI Analysis failed: {str(analysis_error)}")
                logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
                raise
            
            analysis_time = (datetime.now() - analysis_start).total_seconds()
            
            # Safe access to analysis results
            roi_data = analysis_result.get("roi_calculation", {})
            if not isinstance(roi_data, dict):
                logger.warning(f"[{analysis_id[:8]}] roi_calculation is not a dict: {type(roi_data)}")
                roi_data = {}
            
            logger.info(f"[{analysis_id[:8]}] ✅ Analysis complete ({analysis_time:.1f}s)")
            logger.info(f"[{analysis_id[:8]}]   - Monthly ROI: €{roi_data.get('monthly_roi', 0):,.0f}")
            logger.info(f"[{analysis_id[:8]}]   - ROI Multiplier: {roi_data.get('roi_multiplier', 0):.1f}x")
            logger.info(f"[{analysis_id[:8]}]   - Priority: {analysis_result.get('chatbot_priority', 'MEDIUM')}")
            
            # STEP 3: Generate PDF Report
            pdf_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 3/4: Generating PDF Report...")
            
            try:
                report_filename = f"chatpro_analyse_{analysis_id[:8]}.html"
                report_path = os.path.join(self.output_dir, report_filename)
                
                generated_path = self.pdf_generator.generate(
                    crawler_data=crawler_data,
                    analysis_data=analysis_result,
                    company_name=company_name,
                    industry=industry,
                    output_path=report_path,
                    sources=sources
                )
                
                if not generated_path or not os.path.exists(generated_path):
                    logger.error(f"[{analysis_id[:8]}] PDF generation failed - file not created")
                    raise ValueError("PDF file was not created")
                    
            except Exception as pdf_error:
                logger.error(f"[{analysis_id[:8]}] PDF generation failed: {str(pdf_error)}")
                logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
                raise
            
            pdf_time = (datetime.now() - pdf_start).total_seconds()
            logger.info(f"[{analysis_id[:8]}] ✅ PDF generated ({pdf_time:.1f}s)")
            
            # STEP 4: Save to Brevo CRM
            crm_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 4/4: Saving to Brevo CRM...")
            
            try:
                crm_result = self.brevo_crm.save_lead(
                    email=email,
                    company_name=company_name,
                    website_url=website_url,
                    industry=industry,
                    roi_monat=roi_data.get("monthly_roi", 0),
                    has_chatbot=crawler_data.get("has_chatbot", False),
                    chatbot_priority=analysis_result.get("chatbot_priority", "MEDIUM"),
                    analysis_id=analysis_id,
                    chatbot_type=crawler_data.get("chatbot_type", "")
                )
                
                # Defensive check
                if not isinstance(crm_result, dict):
                    logger.warning(f"[{analysis_id[:8]}] CRM result is not a dict: {type(crm_result)}")
                    crm_result = {"status": "unknown"}
                    
            except Exception as crm_error:
                logger.error(f"[{analysis_id[:8]}] Brevo CRM save failed: {str(crm_error)}")
                logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
                crm_result = {"status": "error", "error": str(crm_error)}
            
            crm_time = (datetime.now() - crm_start).total_seconds()
            
            if crm_result.get("status") == "success":
                logger.info(f"[{analysis_id[:8]}] ✅ Lead saved to Brevo ({crm_time:.1f}s)")
            else:
                logger.warning(f"[{analysis_id[:8]}] ⚠️  Brevo save failed: {crm_result.get('error', 'Unknown')}")
            
            # FINAL RESULTS
            total_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"[{analysis_id[:8]}] ✅ ANALYSIS COMPLETED")
            logger.info(f"[{analysis_id[:8]}] Total Time: {total_time:.1f}s")
            
            return {
                "status": "completed",
                "analysis_id": analysis_id,
                "report_path": generated_path,
                "report_filename": report_filename,
                "roi_monat": roi_data.get("monthly_roi", 0),
                "roi_multiplier": roi_data.get("roi_multiplier", 0),
                "break_even_months": roi_data.get("break_even_months", 0),
                "chatbot_priority": analysis_result.get("chatbot_priority", "MEDIUM"),
                "has_chatbot": crawler_data.get("has_chatbot", False),
                "chatbot_type": crawler_data.get("chatbot_type", ""),
                "processing_time": {
                    "total": total_time,
                    "crawl": crawl_time,
                    "analysis": analysis_time,
                    "pdf": pdf_time,
                    "crm": crm_time
                },
                "brevo_status": crm_result.get("status", "unknown")
            }
            
        except Exception as e:
            error_time = (datetime.now() - start_time).total_seconds()
            error_type = type(e).__name__
            error_message = str(e)
            full_traceback = traceback.format_exc()
            
            logger.error(f"[{analysis_id[:8]}] ❌ ANALYSIS FAILED")
            logger.error(f"[{analysis_id[:8]}] Error Type: {error_type}")
            logger.error(f"[{analysis_id[:8]}] Error: {error_message}")
            logger.error(f"[{analysis_id[:8]}] Full Traceback:\n{full_traceback}")
            logger.error(f"[{analysis_id[:8]}] Time elapsed: {error_time:.1f}s")
            
            return {
                "status": "failed",
                "error": error_message,
                "error_type": error_type,
                "traceback": full_traceback,  # FULL STACK TRACE
                "analysis_id": analysis_id,
                "processing_time": error_time
            }
