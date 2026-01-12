"""
ChatPro AI - Business Analyzer
PRODUCTION-READY VERSION with structured outputs and professional analysis
"""
import os
import json
import logging
from typing import Dict, Any, List
from openai import OpenAI
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUT
# ============================================================================

class PainPoint(BaseModel):
    """Structured pain point with business focus"""
    title: str = Field(description="Clear, business-focused title (e.g., 'Low Mobile Conversion Rate')")
    category: str = Field(description="Category: Technology, Customer Experience, Marketing, Operations, or Revenue")
    description: str = Field(description="Detailed description of the problem")
    business_impact: str = Field(description="Estimated business impact (€ or % if possible)")
    evidence: str = Field(description="Concrete evidence from website analysis")
    priority: str = Field(description="Priority: HIGH, MEDIUM, or LOW")


class Recommendation(BaseModel):
    """Structured recommendation with actionable steps"""
    title: str = Field(description="Clear, actionable title (e.g., 'Implement AI-Powered Chatbot')")
    description: str = Field(description="Detailed description with concrete steps")
    business_value: str = Field(description="Expected ROI or KPI improvement")
    implementation_effort: str = Field(description="Estimated time and cost")
    priority: str = Field(description="Priority: HIGH, MEDIUM, or LOW")
    quick_win: bool = Field(description="True if this is a quick win (< 1 month)")


class ROICalculation(BaseModel):
    """Structured ROI calculation with formula"""
    monthly_roi_euro: int = Field(description="Monthly ROI in Euro")
    roi_multiplier: float = Field(description="ROI multiplier (e.g., 3.5x)")
    break_even_months: int = Field(description="Break-even period in months")
    formula_explanation: str = Field(description="Explanation of how ROI was calculated")
    assumptions: List[str] = Field(description="List of assumptions used in calculation")
    

class AnalysisResult(BaseModel):
    """Complete structured analysis output"""
    executive_summary: str = Field(description="2-3 sentence summary of key findings")
    company_overview: str = Field(description="Brief overview of company based on website")
    methodology: str = Field(description="How the analysis was conducted")
    
    pain_points: List[PainPoint] = Field(description="3-7 identified pain points")
    recommendations: List[Recommendation] = Field(description="3-7 actionable recommendations")
    roi_calculation: ROICalculation = Field(description="Detailed ROI calculation")
    
    chatbot_priority: str = Field(description="Chatbot priority: HIGH, MEDIUM, or LOW")
    key_findings: List[str] = Field(description="3-5 bullet point key findings")
    next_steps: List[str] = Field(description="3-5 immediate next steps")


# ============================================================================
# AI ANALYZER CLASS
# ============================================================================

class AIAnalyzer:
    """
    Professional Business Analyzer using OpenAI GPT-4 with Structured Outputs
    """
    
    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-2024-08-06"  # Supports Structured Outputs
        logger.info(f"AIAnalyzer initialized with model: {self.model}")
    
    def _build_system_prompt(self, industry: str, sources_context: str) -> str:
        """Build comprehensive system prompt"""
        return f"""You are a Senior Business Analyst specializing in the {industry} industry.

YOUR ROLE:
You conduct professional business analyses for companies, providing data-driven insights and actionable recommendations.

YOUR TASK:
Analyze the provided website data and create a comprehensive business analysis report.

CRITICAL REQUIREMENTS:

1. ROI CALCULATION MUST BE REALISTIC:
   - Base calculations on actual website traffic data
   - Use industry benchmarks from the provided sources
   - Show your calculation formula
   - List all assumptions clearly
   - Example formula: (Expected Annual Revenue Increase - Annual Costs) / Annual Costs × 100

2. PAIN POINTS MUST BE BUSINESS-FOCUSED:
   - NOT technical jargon like "Mobile: 7 Nicht optimiert"
   - YES business language like "Mobile visitors have 40% higher bounce rate, losing ~€X monthly"
   - Categorize: Technology, Customer Experience, Marketing, Operations, Revenue
   - Prioritize by business impact
   - Provide concrete evidence from website data

3. RECOMMENDATIONS MUST BE ACTIONABLE:
   - NOT vague like "Improve website"
   - YES specific like "Implement AI chatbot to handle 80% of FAQ inquiries, saving 25h/week staff time"
   - Include implementation effort estimate
   - Show expected business value
   - Mark quick wins (< 1 month)

4. USE INDUSTRY DATA:
{sources_context}

5. LANGUAGE:
   - Write in clear, professional German
   - Avoid technical jargon
   - Focus on business value
   - Be specific with numbers

ANALYSIS METHODOLOGY:
1. Analyze website performance (mobile, speed, chatbot presence)
2. Estimate current inquiry volume and conversion rates
3. Calculate potential improvements based on industry benchmarks
4. Prioritize recommendations by ROI
5. Provide realistic implementation roadmap

OUTPUT:
Return a complete AnalysisResult object with all fields filled professionally."""

    def _build_user_prompt(self, crawler_data: Dict, company_name: str) -> str:
        """Build user prompt with website data"""
        
        # Extract key data points
        has_chatbot = crawler_data.get("has_chatbot", False)
        chatbot_type = crawler_data.get("chatbot_type", "None")
        is_mobile_friendly = crawler_data.get("is_mobile_friendly", False)
        meta_description = crawler_data.get("meta_description", "")
        page_title = crawler_data.get("page_title", "")
        
        # Build prompt
        prompt = f"""COMPANY TO ANALYZE: {company_name}

WEBSITE DATA:
- Page Title: {page_title}
- Meta Description: {meta_description}
- Has Chatbot: {has_chatbot}
- Chatbot Type: {chatbot_type}
- Mobile Friendly: {is_mobile_friendly}

TASK:
Create a comprehensive business analysis for {company_name}.

FOCUS AREAS:
1. Current digital presence assessment
2. Customer experience analysis
3. Automation potential (especially chatbot)
4. Revenue optimization opportunities
5. Competitive positioning

Remember:
- Be realistic with numbers
- Base ROI on industry data
- Provide actionable insights
- Show clear business value"""

        return prompt

    def analyze(
        self,
        crawler_data: Dict[str, Any],
        industry: str,
        company_name: str,
        sources: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Perform professional business analysis
        
        Args:
            crawler_data: Website crawl data
            industry: Industry category
            company_name: Company name
            sources: Industry sources for context
            
        Returns:
            Structured analysis result as dict
        """
        logger.info(f"Starting analysis for {company_name} in {industry} industry")
        
        try:
            # Build sources context
            sources_context = self._format_sources(sources or [])
            
            # Build prompts
            system_prompt = self._build_system_prompt(industry, sources_context)
            user_prompt = self._build_user_prompt(crawler_data, company_name)
            
            # Call OpenAI with Structured Outputs
            logger.info(f"Calling OpenAI {self.model} with structured output...")
            
            completion = self.client.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=AnalysisResult,
                temperature=0.7
            )
            
            # Extract parsed result
            analysis = completion.choices[0].message.parsed
            
            if not analysis:
                raise ValueError("OpenAI returned no parsed result")
            
            # Convert to dict
            result = analysis.model_dump()
            
            # Add metadata
            result["model"] = self.model
            result["industry"] = industry
            result["company_name"] = company_name
            
            logger.info(f"Analysis completed successfully for {company_name}")
            logger.info(f"Generated {len(result['pain_points'])} pain points and {len(result['recommendations'])} recommendations")
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            logger.error(f"Crawler data: {crawler_data}")
            raise
    
    def _format_sources(self, sources: List[Dict]) -> str:
        """Format sources for prompt context"""
        if not sources:
            return "No specific industry sources available."
        
        formatted = "INDUSTRY RESEARCH SOURCES:\n\n"
        for idx, source in enumerate(sources, 1):
            formatted += f"{idx}. {source.get('title', 'Unknown')}\n"
            formatted += f"   URL: {source.get('url', 'N/A')}\n"
            formatted += f"   Key Insight: {source.get('description', 'N/A')}\n\n"
        
        formatted += "\nUse these sources to support your analysis with industry data.\n"
        return formatted


# Example usage for testing
if __name__ == "__main__":
    # Test the analyzer
    analyzer = AIAnalyzer()
    
    test_crawler_data = {
        "page_title": "Guest House Holland - Vacation Rentals in Juan Dolio",
        "meta_description": "Luxury beachfront apartments in Dominican Republic",
        "has_chatbot": True,
        "chatbot_type": "Unknown",
        "is_mobile_friendly": True
    }
    
    test_sources = [
        {
            "title": "Vacation Rental Response Time Study",
            "url": "https://example.com",
            "description": "Response within 1 hour increases bookings by 25%"
        }
    ]
    
    result = analyzer.analyze(
        crawler_data=test_crawler_data,
        industry="hotel",
        company_name="Guest House Holland",
        sources=test_sources
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
