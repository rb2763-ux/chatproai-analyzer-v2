"""
CHATPRO AI ANALYZER - PROCESSING PIPELINE V2.0
Complete analysis pipeline: Crawl → AI Analysis (OpenAI) → PDF → Brevo CRM
"""

import asyncio
from typing import Dict
import os
from datetime import datetime
import uuid

from .crawler import WebsiteCrawler
from .analyzer import AIAnalyzer
from .pdf_generator import PDFReportGenerator
from .brevo_crm import BrevoCRM
from .sources_database import SOURCES

class AnalysisPipeline:
    """
    Complete analysis pipeline with OpenAI GPT-4
    
    Steps:
    1. Crawl website (~10-15s)
    2. AI analysis with OpenAI GPT-4 (~20-40s)
    3. Generate PDF report (~5-10s)
    4. Save to Brevo CRM (instant)
    
    Total: 30-65 seconds
    """
    
    def __init__(self, output_dir: str = "/mnt/user-data/outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.analyzer = AIAnalyzer()
        self.pdf_generator = PDFReportGenerator()
        self.brevo_crm = BrevoCRM()
    
    async def process(
        self,
        website_url: str,
        industry: str,
        email: str,
        company_name: str = None
    ) -> Dict:
        """
        Process complete analysis pipeline
        
        Returns:
            dict: {
                "status": "completed",
                "analysis_id": "...",
                "report_url": "...",
                "roi_monat": 13180,
                "chatbot_priority": "HIGH"
            }
        """
        
        analysis_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        try:
            # STEP 1: Crawl website (~10-15s)
            print(f"\n{'='*60}")
            print(f"[{analysis_id[:8]}] ANALYSIS STARTED")
            print(f"{'='*60}")
            print(f"[{analysis_id[:8]}] Step 1/4: Crawling {website_url}...")
            
            crawler = WebsiteCrawler(website_url)
            crawler_data = crawler.crawl()
            
            if "error" in crawler_data:
                return {
                    "status": "failed",
                    "error": crawler_data["error"],
                    "step": "crawling",
                    "analysis_id": analysis_id
                }
            
            # Extract company name from title if not provided
            if not company_name:
                company_name = crawler_data.get('title', 'Ihr Unternehmen')
            
            crawl_time = (datetime.now() - start_time).total_seconds()
            print(f"[{analysis_id[:8]}] ✅ Crawling complete ({crawl_time:.1f}s)")
            print(f"  - Pages: {crawler_data.get('page_count', 0)}")
            print(f"  - Chatbot: {'✓ ' + crawler_data.get('chatbot_type', '') if crawler_data.get('has_chatbot') else '✗ None'}")
            print(f"  - Lead Forms: {len(crawler_data.get('lead_forms', []))}")
            
            # STEP 2: AI Analysis with OpenAI GPT-4 (~20-40s)
            analysis_start = datetime.now()
            print(f"\n[{analysis_id[:8]}] Step 2/4: AI Analysis with OpenAI GPT-4...")
            print(f"  Model: {self.analyzer.model}")
            print(f"  Industry: {industry}")
            
            analysis_result = self.analyzer.analyze(
                crawler_data=crawler_data,
                industry=industry,
                company_name=company_name
            )
            
            analysis_time = (datetime.now() - analysis_start).total_seconds()
            roi_data = analysis_result.get("roi_calculation", {})
            
            print(f"[{analysis_id[:8]}] ✅ Analysis complete ({analysis_time:.1f}s)")
            print(f"  - Monthly ROI: €{roi_data.get('monthly_roi', 0):,.0f}")
            print(f"  - ROI Multiplier: {roi_data.get('roi_multiplier', 0):.1f}x")
            print(f"  - Priority: {analysis_result.get('chatbot_priority', 'MEDIUM')}")
            print(f"  - Pain Points: {len(analysis_result.get('pain_points', []))}")
            print(f"  - Recommendations: {len(analysis_result.get('recommendations', []))}")
            
            # STEP 3: Generate PDF Report (~5-10s)
            pdf_start = datetime.now()
            print(f"\n[{analysis_id[:8]}] Step 3/4: Generating PDF Report...")
            
            report_filename = f"chatpro_analyse_{analysis_id[:8]}.pdf"
            report_path = os.path.join(self.output_dir, report_filename)
            
            generated_path = await self.pdf_generator.generate(
                crawler_data=crawler_data,
                analysis_data=analysis_result,
                company_name=company_name,
                industry=industry,
                output_path=report_path,
                sources=SOURCES  # Include sources
            )
            
            pdf_time = (datetime.now() - pdf_start).total_seconds()
            print(f"[{analysis_id[:8]}] ✅ PDF generated ({pdf_time:.1f}s)")
            print(f"  - Path: {generated_path}")
            
            # STEP 4: Save to Brevo CRM (NO EMAIL!)
            crm_start = datetime.now()
            print(f"\n[{analysis_id[:8]}] Step 4/4: Saving to Brevo CRM...")
            
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
            
            crm_time = (datetime.now() - crm_start).total_seconds()
            
            if crm_result.get("status") == "success":
                print(f"[{analysis_id[:8]}] ✅ Lead saved to Brevo ({crm_time:.1f}s)")
                print(f"  - Contact ID: {crm_result.get('contact_id', 'N/A')}")
                print(f"  - Tags: {', '.join(crm_result.get('tags_added', []))}")
            else:
                print(f"[{analysis_id[:8]}] ⚠️  Brevo save failed: {crm_result.get('error')}")
            
            # FINAL RESULTS
            total_time = (datetime.now() - start_time).total_seconds()
            print(f"\n{'='*60}")
            print(f"[{analysis_id[:8]}] ✅ ANALYSIS COMPLETED")
            print(f"{'='*60}")
            print(f"Total Time: {total_time:.1f}s")
            print(f"  - Crawl: {crawl_time:.1f}s")
            print(f"  - AI Analysis: {analysis_time:.1f}s")
            print(f"  - PDF Gen: {pdf_time:.1f}s")
            print(f"  - CRM: {crm_time:.1f}s")
            print(f"{'='*60}\n")
            
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
            print(f"\n{'='*60}")
            print(f"[{analysis_id[:8]}] ❌ ANALYSIS FAILED")
            print(f"{'='*60}")
            print(f"Error: {str(e)}")
            print(f"Time elapsed: {error_time:.1f}s")
            print(f"{'='*60}\n")
            
            return {
                "status": "failed",
                "error": str(e),
                "analysis_id": analysis_id,
                "processing_time": error_time
            }
