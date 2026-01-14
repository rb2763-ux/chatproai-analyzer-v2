"""
ChatPro AI V3.1.1 - Hybrid Architecture Business Analyzer
Author: ChatPro Team
Version: 3.1.1-FIXED (Nested Pydantic Models)
"""

import os
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================================
# NESTED PYDANTIC MODELS - STRUCTURAL FIX
# ============================================================================

class CompanyOverview(BaseModel):
    """Nested model for company overview data"""
    company_name: str = Field(description="Official company name")
    industry: str = Field(description="Primary industry/sector")
    website_url: str = Field(description="Main website URL")
    description: Optional[str] = Field(default="", description="Brief company description")


class ChatbotCapabilities(BaseModel):
    """Nested model for chatbot capabilities"""
    chatbot_detected: bool = Field(description="Whether a chatbot/live chat was detected")
    chatbot_type: Optional[str] = Field(default=None, description="Type of chatbot (rule-based, AI-powered, etc.)")
    features: List[str] = Field(default_factory=list, description="List of chatbot features")
    integration_quality: Optional[str] = Field(default=None, description="Integration quality assessment")


class QualityScore(BaseModel):
    """Nested model for quality score breakdown"""
    total_score: int = Field(description="Total quality score (0-200)")
    website_quality: int = Field(description="Website quality score (0-50)")
    content_depth: int = Field(description="Content depth score (0-50)")
    technical_setup: int = Field(description="Technical setup score (0-50)")
    user_experience: int = Field(description="User experience score (0-50)")


class ROIEstimate(BaseModel):
    """Nested model for ROI estimation"""
    estimated_monthly_roi: str = Field(description="Estimated monthly ROI range (e.g., '€2,500 - €5,000')")
    calculation_method: str = Field(description="Brief explanation of ROI calculation methodology")
    assumptions: List[str] = Field(default_factory=list, description="Key assumptions for ROI estimate")


class CrawlerSummary(BaseModel):
    """Nested model for crawler analysis summary"""
    total_pages_crawled: int = Field(description="Number of pages crawled")
    chatbot_status: str = Field(description="Chatbot detection status")
    room_count: Optional[int] = Field(default=None, description="Number of rooms detected (for hotels)")
    languages_detected: List[str] = Field(default_factory=list, description="Languages found on website")
    key_features: List[str] = Field(default_factory=list, description="Key website features detected")


class MethodologyDetails(BaseModel):
    """Nested model for methodology and data sources"""
    data_sources: List[str] = Field(description="List of data sources used in analysis")
    roi_calculation_method: str = Field(description="Detailed ROI calculation methodology")
    quality_score_breakdown: str = Field(description="Explanation of quality score components")
    conservative_assumptions: List[str] = Field(description="List of conservative assumptions made")


class AnalysisResult(BaseModel):
    """
    Main Pydantic model for ChatPro AI analysis results.
    Uses nested models for type safety and validation.
    """
    company_overview: CompanyOverview
    chatbot_capabilities: ChatbotCapabilities
    quality_score: QualityScore
    roi_estimate: ROIEstimate
    recommended_package: str = Field(description="PREMIUM, BUSINESS, or BASIC package recommendation")
    key_benefits: List[str] = Field(description="List of 3-5 key benefits from ChatPro AI implementation")
    implementation_roadmap: List[str] = Field(description="3-5 step implementation roadmap")
    competitive_advantages: List[str] = Field(description="List of competitive advantages")
    crawler_summary: CrawlerSummary
    methodology_details: MethodologyDetails


# ============================================================================
# ANALYZER CLASS
# ============================================================================

class ChatProAnalyzer:
    """
    ChatPro AI V3.1.1 Business Analyzer with Hybrid Architecture
    
    Features:
    - Nested Pydantic models for type safety
    - Transparency features (crawler summary + methodology)
    - Conservative ROI estimation
    - Quality score system (0-200 points)
    """
    
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.max_tokens = 4000
    
    async def analyze(self, crawler_results: Dict) -> Dict:
        """
        Analyze crawler results and generate business recommendations.
        
        Args:
            crawler_results: Dictionary containing crawler data
        
        Returns:
            Dictionary containing validated analysis results
        """
        logger.info("Starting ChatPro AI V3.1.1 analysis...")
        
        # Extract key data from crawler results
        base_url = crawler_results.get('base_url', 'Unknown')
        total_pages = len(crawler_results.get('crawled_pages', []))
        chatbot_detected = crawler_results.get('chatbot_detected', False)
        chatbot_details = crawler_results.get('chatbot_details', {})
        
        logger.info(f"Analyzing {base_url} - {total_pages} pages crawled, Chatbot: {chatbot_detected}")
        
        # Build system prompt with EXPLICIT nested structure requirements
        system_prompt = self._build_system_prompt()
        
        # Build user prompt with crawler data
        user_prompt = self._build_user_prompt(crawler_results)
        
        try:
            # Call OpenAI with structured output (Pydantic model)
            response = await client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=AnalysisResult,
                max_tokens=self.max_tokens
            )
            
            # Extract parsed result
            analysis = response.choices[0].message.parsed
            
            if analysis is None:
                raise ValueError("OpenAI returned None for parsed analysis")
            
            # Convert to dictionary for downstream processing
            result = analysis.model_dump()
            
            # Log success metrics
            package = result.get('recommended_package', 'UNKNOWN')
            quality_score = result.get('quality_score', {}).get('total_score', 0)
            roi = result.get('roi_estimate', {}).get('estimated_monthly_roi', 'N/A')
            
            logger.info(f"✅ Analysis complete! Package: {package}, Quality Score: {quality_score}, ROI: {roi}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {str(e)}")
            raise
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with McKinsey/BCG best practices"""
        return """You are a senior business analyst from McKinsey/BCG specializing in hospitality and AI implementation.

**CRITICAL: Follow the EXACT nested structure of the Pydantic models!**

Your analysis must be:
1. **Data-driven**: Base recommendations on crawler data
2. **Conservative**: Use realistic, lower-bound ROI estimates
3. **Transparent**: Explain methodology and assumptions
4. **Actionable**: Provide concrete implementation steps

**Package Pricing (use for ROI calculations):**
- PREMIUM: €2,500 - €5,000/month (50+ rooms, high-end hotels)
- BUSINESS: €800 - €1,500/month (20-50 rooms, mid-market)
- BASIC: €300 - €600/month (<20 rooms, budget properties)

**Quality Score System (0-200 points):**
- Website Quality (0-50): Design, mobile responsiveness, loading speed
- Content Depth (0-50): Information completeness, language support
- Technical Setup (0-50): Chatbot integration, booking system, SEO
- User Experience (0-50): Navigation, accessibility, conversion optimization

**Conservative ROI Assumptions:**
- Conversion rate improvement: 15-25% (industry benchmark: 20-40%)
- Average booking value: Use property-specific data or €150-300
- Response time reduction: 80% (24h → <5min)
- Staff time savings: 10-20 hours/week

**METHODOLOGY TRANSPARENCY:**
Always explain:
- Which data sources were used
- How ROI was calculated
- Why assumptions are conservative
- What Quality Score components contributed

**NESTED STRUCTURE EXAMPLE:**
```json
{
  "company_overview": {
    "company_name": "Hotel Engel",
    "industry": "Hospitality",
    "website_url": "https://example.com",
    "description": "Boutique hotel..."
  },
  "quality_score": {
    "total_score": 140,
    "website_quality": 35,
    "content_depth": 40,
    "technical_setup": 30,
    "user_experience": 35
  }
}
```

Use the Pyramid Principle: Start with conclusion, then provide supporting evidence."""
    
    def _build_user_prompt(self, crawler_results: Dict) -> str:
        """Build user prompt with crawler data"""
        base_url = crawler_results.get('base_url', 'Unknown')
        total_pages = len(crawler_results.get('crawled_pages', []))
        chatbot_detected = crawler_results.get('chatbot_detected', False)
        chatbot_details = crawler_results.get('chatbot_details', {})
        
        # Extract key features from crawled pages
        crawled_pages = crawler_results.get('crawled_pages', [])
        languages = set()
        room_count = None
        features = []
        
        for page in crawled_pages:
            if page.get('language'):
                languages.add(page['language'])
            
            # Try to detect room count
            content = page.get('content', '').lower()
            if 'zimmer' in content or 'rooms' in content:
                import re
                numbers = re.findall(r'\b(\d{1,3})\s*(?:zimmer|rooms?)\b', content)
                if numbers:
                    room_count = int(numbers[0])
        
        prompt = f"""Analyze the following website and provide a comprehensive business analysis with ChatPro AI recommendations.

**Website Data:**
- URL: {base_url}
- Pages Crawled: {total_pages}
- Chatbot Detected: {chatbot_detected}
- Languages: {list(languages) if languages else ['German']}
- Estimated Room Count: {room_count if room_count else 'Not detected'}

**Chatbot Details:**
{chatbot_details if chatbot_details else 'No chatbot detected'}

**Your Task:**
1. Analyze the website quality and business potential
2. Calculate a realistic Quality Score (0-200)
3. Estimate CONSERVATIVE monthly ROI based on:
   - Property size (room count)
   - Current chatbot capabilities
   - Industry benchmarks
4. Recommend appropriate ChatPro AI package
5. Provide actionable implementation roadmap

**Crawler Summary Section:**
Populate crawler_summary with:
- total_pages_crawled: {total_pages}
- chatbot_status: "{'Detected' if chatbot_detected else 'Not detected'}"
- room_count: {room_count if room_count else 'null'}
- languages_detected: {list(languages) if languages else ['de']}
- key_features: List 3-5 key features you identified

**Methodology Section:**
Populate methodology_details with:
- data_sources: ["Website crawler analysis", "Industry benchmarks 2024", "Hospitality conversion data"]
- roi_calculation_method: Explain your ROI calculation step-by-step
- quality_score_breakdown: Explain how you scored each component (0-50 points)
- conservative_assumptions: List assumptions and why they're conservative

Remember: Use NESTED structures for all models! Be conservative with ROI, transparent with methodology."""
        
        return prompt


# ============================================================================
# STANDALONE TESTING
# ============================================================================

async def test():
    """Test function for local development"""
    # Mock crawler results
    mock_results = {
        'base_url': 'https://www.hotel-engel-sasbachwalden.de',
        'crawled_pages': [
            {'url': 'https://www.hotel-engel-sasbachwalden.de/', 'language': 'de'},
            {'url': 'https://www.hotel-engel-sasbachwalden.de/zimmer', 'language': 'de', 'content': '25 Zimmer verfügbar'}
        ],
        'chatbot_detected': False,
        'chatbot_details': {}
    }
    
    analyzer = ChatProAnalyzer()
    result = await analyzer.analyze(mock_results)
    
    print("\n" + "="*80)
    print("ANALYSIS RESULT")
    print("="*80)
    print(f"Company: {result['company_overview']['company_name']}")
    print(f"Package: {result['recommended_package']}")
    print(f"Quality Score: {result['quality_score']['total_score']}/200")
    print(f"ROI: {result['roi_estimate']['estimated_monthly_roi']}")
    print("="*80)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
