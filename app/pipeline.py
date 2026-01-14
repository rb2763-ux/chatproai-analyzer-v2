"""
ChatPro AI V3.1.1 - Unified Pipeline
Author: ChatPro Team
Version: 3.1.1-FIXED
"""

import logging
from typing import Dict
from app.crawler import WebsiteCrawler as ChatProCrawler
from app.analyzer import ChatProAnalyzer
from app.pdf_generator import generate_pdf_report

logger = logging.getLogger(__name__)


class ChatProPipeline:
    """
    Unified pipeline for ChatPro AI analysis workflow.
    
    Workflow:
    1. Crawler V3.1: Multi-page crawling with chatbot detection
    2. Analyzer V3.1.1: AI-powered analysis with nested Pydantic models
    3. PDF Generator V3.1: Modern report with transparency features
    """
    
    def __init__(self):
        self.crawler = ChatProCrawler()
        self.analyzer = ChatProAnalyzer()
    
    async def analyze_website(self, url: str, max_pages: int = 10) -> Dict:
        """
        Analyze a website and return structured data.
        
        Args:
            url: Target website URL
            max_pages: Maximum pages to crawl (default: 10)
        
        Returns:
            Dictionary with analysis results (nested structure)
        """
        logger.info(f"Starting ChatPro AI analysis for: {url}")
        
        # Step 1: Crawl website
        logger.info(f"Step 1/3: Crawling website (max {max_pages} pages)...")
        crawler_results = await self.crawler.crawl(url)
        
        # Step 2: Analyze with AI
        logger.info("Step 2/3: Analyzing with ChatPro AI V3.1.1...")
        analysis_results = await self.analyzer.analyze(crawler_results)
        
        logger.info("✅ Analysis complete!")
        return analysis_results
    
    async def generate_report(self, url: str, output_filename: str, max_pages: int = 10):
        """
        Generate complete PDF report for a website.
        
        Args:
            url: Target website URL
            output_filename: Output PDF file path
            max_pages: Maximum pages to crawl (default: 10)
        """
        logger.info(f"Generating report for: {url} → {output_filename}")
        
        # Step 1 & 2: Analyze website
        analysis_data = await self.analyze_website(url, max_pages=max_pages)
        
        # Step 3: Generate PDF
        logger.info("Step 3/3: Generating PDF report...")
        generate_pdf_report(analysis_data, output_filename)
        
        logger.info(f"✅ Report generated successfully: {output_filename}")
        
        return analysis_data
