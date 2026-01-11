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

# Setup logger
logger = logging.getLogger("app.pipeline")


class AnalysisPipeline:
    """Production-ready analysis pipeline with comprehensive error handling"""
    
    def __init__(self, output_dir: str = "/mnt/user-data/outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.crawler = WebsiteCrawler()
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
        Process complete analysis pipeline
        
        Args:
            website_url: Target website URL
            industry: Business industry
            email: Contact email
            company_name: Company name
            analysis_id: Optional analysis ID (generated if not provided)
            
        Returns:
            Dict with analysis results and metadata
        """
        
        if not analysis_id:
            analysis_id = str(uuid.uuid4())
        
        logger.info(f"[{analysis_id[:8]}] Starting analysis for {website_url}")
        
        start_time = datetime.now()
        
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
            logger.info(f"[{analysis_id[:8]}] Crawling complete: {crawl_time:.1f}s")
            
            # STEP 2: AI Analysis
            analysis_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 2/4: AI Analysis with OpenAI...")
            
            try:
                # Sources are fetched inside analyzer.analyze()
                
                analysis_result = self.analyzer.analyze(
                    crawler_data=crawler_data,
                    industry=industry,
                    company_name=company_name
                )
                
                # Defensive check
                if not analysis_result or not isinstance(analysis_result, dict):
                    logger.error(f"[{analysis_id[:8]}] Invalid analysis_result: {type(analysis_result)}")
                    raise ValueError("Analysis returned invalid data structure")
                
            except Exception as analysis_error:
                logger.error(f"[{analysis_id[:8]}] AI Analysis failed: {str(analysis_error)}")
                logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
                return {
                    "status": "failed",
                    "error": str(analysis_error),
                    "analysis_id": analysis_id,
                    "processing_time": (datetime.now() - start_time).total_seconds()
                }
            
            analysis_time = (datetime.now() - analysis_start).total_seconds()
            logger.info(f"[{analysis_id[:8]}] AI Analysis complete: {analysis_time:.1f}s")
            
            # Log analysis results
            roi_data = analysis_result.get("roi_calculation", {})
            logger.info(f"[{analysis_id[:8]}] ROI: {roi_data.get('monthly_roi', 0)} | Multiplier: {roi_data.get('roi_multiplier', 0)}x")
            logger.info(f"[{analysis_id[:8]}] Chatbot Priority: {analysis_result.get('chatbot_priority', 'UNKNOWN')}")
            logger.info(f"[{analysis_id[:8]}] Pain Points: {len(analysis_result.get('pain_points', []))}")
            logger.info(f"[{analysis_id[:8]}] Recommendations: {len(analysis_result.get('recommendations', []))}") 
            
            # STEP 3: PDF Generation
            pdf_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 3/4: Generating PDF report...")
            
            try:
                report_filename = f"chatpro_analyse_{analysis_id[:8]}.html"
                report_path = os.path.join(self.output_dir, report_filename)
                
                generated_path = self.pdf_generator.generate(
                    crawler_data=crawler_data,
                    analysis_data=analysis_result,
                    company_name=company_name,
                    industry=industry,
                    output_path=report_path
                )
                
                if not generated_path or not os.path.exists(generated_path):
                    logger.error(f"[{analysis_id[:8]}] PDF generation failed - file not created")
                    generated_path = None
                    
            except Exception as pdf_error:
                logger.error(f"[{analysis_id[:8]}] PDF generation failed: {str(pdf_error)}")
                logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
                generated_path = None
            
            pdf_time = (datetime.now() - pdf_start).total_seconds()
            logger.info(f"[{analysis_id[:8]}] PDF generated: {pdf_time:.1f}s")
            
            # STEP 4: Save to Brevo CRM
            crm_start = datetime.now()
            logger.info(f"[{analysis_id[:8]}] Step 4/4: Saving to Brevo CRM...")
            
            try:
                crm_response = await self.brevo_crm.save_lead(
                    email=email,
                    company_name=company_name,
                    website_url=website_url,
                    industry=industry,
                    analysis_id=analysis_id,
                    has_chatbot=crawler_data.get("has_chatbot", False),
                    roi_monthly=roi_data.get("monthly_roi", 0),
                    roi_multiplier=roi_data.get("roi_multiplier", 0),
                    chatbot_type=crawler_data.get("chatbot_type", "")
                )
                
                logger.info(f"[{analysis_id[:8]}] Lead saved to Brevo: {crm_response}")
                
            except Exception as crm_error:
                logger.error(f"[{analysis_id[:8]}] Brevo CRM save failed: {str(crm_error)}")
                logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
            
            crm_time = (datetime.now() - crm_start).total_seconds()
            
            # Calculate total time
            total_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"[{analysis_id[:8]}] ANALYSIS COMPLETED")
            logger.info(f"[{analysis_id[:8]}] Total Time: {total_time:.1f}s | Crawl: {crawl_time:.1f}s | AI Analysis: {analysis_time:.1f}s | PDF Gen: {pdf_time:.1f}s | CRM: {crm_time:.1f}s")
            
            # Return success response
            return {
                "status": "completed",
                "analysis_id": analysis_id,
                "report_path": generated_path,
                "report_filename": report_filename if generated_path else None,
                "roi_monat": roi_data.get("monthly_roi", 0),
                "roi_multiplier": roi_data.get("roi_multiplier", 0),
                "break_even_months": roi_data.get("break_even_months", 0),
                "has_chatbot": crawler_data.get("has_chatbot", False),
                "chatbot_type": crawler_data.get("chatbot_type", ""),
                "processing_time": {
                    "total": total_time,
                    "crawl": crawl_time,
                    "analysis": analysis_time,
                    "pdf": pdf_time,
                    "crm": crm_time
                }
            }
            
        except Exception as e:
            error_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"[{analysis_id[:8]}] ANALYSIS FAILED: {str(e)}")
            logger.error(f"[{analysis_id[:8]}] Traceback:\n{traceback.format_exc()}")
            
            return {
                "status": "failed",
                "error": str(e),
                "analysis_id": analysis_id,
                "processing_time": error_time
            }
