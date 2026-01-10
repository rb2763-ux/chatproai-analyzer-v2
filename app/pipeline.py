"""
CHATPRO AI ANALYZER - PROCESSING PIPELINE
Complete analysis pipeline: Crawl → Analyze → PDF → Email → CRM
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

class AnalysisPipeline:
    """
    Complete analysis pipeline
    
    Steps:
    1. Crawl website
    2. AI analysis
    3. Generate PDF
    4. Send email (TODO)
    5. Save to Brevo CRM (TODO)
    """
    
    def __init__(self, output_dir: str = "/mnt/user-data/outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.crawler = None
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
        Process complete analysis
        
        Returns status and results
        """
        
        analysis_id = str(uuid.uuid4())
        
        try:
            # Step 1: Crawl website
            print(f"[{analysis_id}] Step 1: Crawling {website_url}...")
            crawler = WebsiteCrawler(website_url)
            crawler_data = crawler.crawl()
            
            if "error" in crawler_data:
                return {
                    "status": "failed",
                    "error": crawler_data["error"],
                    "step": "crawling"
                }
            
            # Extract company name from title if not provided
            if not company_name:
                company_name = crawler_data.get('title', 'Ihr Unternehmen')
            
            print(f"[{analysis_id}] ✅ Crawling complete")
            print(f"  - Title: {crawler_data.get('title')}")
            print(f"  - Chatbot: {crawler_data.get('has_chatbot')}")
            
            # Step 2: AI Analysis
            print(f"[{analysis_id}] Step 2: Analyzing...")
            analysis_data = self.analyzer.analyze(crawler_data, industry)
            
            roi = analysis_data['roi_calculation']['summary']['total_roi_monat']
            print(f"[{analysis_id}] ✅ Analysis complete")
            print(f"  - ROI/Monat: €{roi:,}")
            
            # Step 3: Generate PDF
            print(f"[{analysis_id}] Step 3: Generating PDF...")
            
            report_filename = f"chatpro_analyse_{analysis_id[:8]}.html"
            report_path = os.path.join(self.output_dir, report_filename)
            
            generated_path = self.pdf_generator.generate(
                crawler_data=crawler_data,
                analysis_data=analysis_data,
                company_name=company_name,
                industry=industry,
                output_path=report_path
            )
            
            print(f"[{analysis_id}] ✅ PDF generated: {generated_path}")
            
            # Step 4: Save to Brevo CRM (Email wird später über Brevo gesendet)

           
            
            # Step 5: Save to Brevo CRM
            print(f"[{analysis_id}] Step 5: Saving to Brevo CRM...")
            
            crm_result = self.brevo_crm.save_lead(
                email=email,
                company_name=company_name,
                website_url=website_url,
                industry=industry,
                roi_monat=roi_data['total_roi_monat'],
                has_chatbot=crawler_data.get('has_chatbot', False),
                chatbot_priority=crawler_data.get('chatbot_details', {}).get('priority', 'LOW'),
                analysis_id=analysis_id
            )
            
            if crm_result['status'] == 'success':
                print(f"[{analysis_id}] ✅ Brevo CRM: {crm_result['action']}")
                
                # Add tags
                tags = [f"analyzer-{industry}"]
                if crawler_data.get('has_chatbot'):
                    tags.append('has-chatbot')
                    chatbot_type = crawler_data.get('chatbot_details', {}).get('type')
                    if chatbot_type:
                        tags.append(f'has-{chatbot_type}')
                if crawler_data.get('chatbot_details', {}).get('priority') == 'HIGH':
                    tags.append('high-priority')
                
                self.brevo_crm.add_tags(email, tags)
            else:
                print(f"[{analysis_id}] ⚠️  Brevo CRM failed: {crm_result.get('error', 'Unknown')}")
            
            return {
                "status": "completed",
                "analysis_id": analysis_id,
                "report_path": generated_path,
                "report_url": f"/api/report/{analysis_id}",
                "data": {
                    "company_name": company_name,
                    "website_url": website_url,
                    "industry": industry,
                    "email": email,
                    "roi_monat": roi,
                    "has_chatbot": crawler_data.get('has_chatbot'),
                    "chatbot_priority": crawler_data.get('chatbot_details', {}).get('priority', 'LOW')
                }
            }
            
        except Exception as e:
            print(f"[{analysis_id}] ❌ Error: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "analysis_id": analysis_id
            }


# Test function
async def test_pipeline():
    """Test complete pipeline"""
    
    pipeline = AnalysisPipeline()
    
    # Test with ADORO
    print("="*60)
    print("TESTING COMPLETE PIPELINE - ADORO APARTHOTEL")
    print("="*60)
    
    result = await pipeline.process(
        website_url="https://adoro-aparthotel.com",
        industry="hotel",
        email="robert@chatproai.io",
        company_name="ADORO Aparthotel"
    )
    
    print("\n" + "="*60)
    print("PIPELINE RESULT:")
    print("="*60)
    print(f"Status: {result['status']}")
    if result['status'] == 'completed':
        print(f"Analysis ID: {result['analysis_id']}")
        print(f"Report: {result['report_path']}")
        print(f"\nData:")
        for key, value in result['data'].items():
            print(f"  {key}: {value}")
    else:
        print(f"Error: {result.get('error')}")
    
    return result


if __name__ == "__main__":
    result = asyncio.run(test_pipeline())
