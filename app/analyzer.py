#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatPro AI - Business Analyzer
VERSION 3.1 - QUALITY SCORE + PREMIUM + INTELLIGENT ESTIMATION

Features:
- Quality Score System (0-200 points)
- Premium Package Recommendation (€799/month)
- Intelligent room count estimation when crawler returns None
- Realistic ROI calculations based on room count
- Chatbot-aware recommendations
- 100% German output
"""

import os
import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUT
# ============================================================================

class PainPoint(BaseModel):
    """Pain point model"""
    title: str = Field(description="Pain point title in German")
    category: str = Field(description="Category: Technology, Marketing, Customer Experience, Operations")
    description: str = Field(description="Detailed description in German")
    business_impact: str = Field(description="Business impact description in German")
    evidence: str = Field(description="Evidence from website analysis in German")
    priority: str = Field(description="Priority: HIGH, MEDIUM, LOW")


class Recommendation(BaseModel):
    """Recommendation model"""
    title: str = Field(description="Recommendation title in German")
    description: str = Field(description="Detailed description in German")
    business_value: str = Field(description="Business value in German")
    implementation_effort: str = Field(description="Implementation effort in German")
    priority: str = Field(description="Priority: HIGH, MEDIUM, LOW")
    quick_win: bool = Field(description="Whether this is a quick win")


class PackageDetails(BaseModel):
    """Package details model"""
    name: str = Field(description="PREMIUM or BUSINESS")
    setup_cost_euro: int = Field(description="Setup cost in EUR")
    monthly_cost_euro: int = Field(description="Monthly cost in EUR")
    features: List[str] = Field(description="List of key features in German")
    why_this_package: str = Field(description="Explanation why this package was recommended in German")


class ROICalculation(BaseModel):
    """ROI calculation model"""
    monthly_roi_euro: int = Field(description="Monthly ROI in EUR")
    roi_multiplier: float = Field(description="ROI multiplier (e.g., 3.5x)")
    break_even_months: float = Field(description="Break-even period in months")
    formula_explanation: str = Field(description="How ROI was calculated in German")
    assumptions: List[str] = Field(description="List of assumptions in German")
    sources_used: List[int] = Field(description="List of source IDs used (1-14)")


class AnalysisResult(BaseModel):
    """Complete analysis result"""
    executive_summary: str = Field(description="Executive summary in German")
    company_overview: str = Field(description="Company overview in German")
    methodology: str = Field(description="Analysis methodology in German")
    
    # NEW V3.1 FIELDS
    recommended_package: str = Field(description="PREMIUM or BUSINESS")
    package_details: PackageDetails = Field(description="Package details")
    quality_score: int = Field(description="Quality score 0-200")
    quality_indicators: List[str] = Field(description="List of quality indicators found")
    estimated_room_count: Optional[int] = Field(description="Estimated room count if not found by crawler")
    room_count_method: str = Field(description="How room count was determined: crawler, estimated, or unknown")
    
    pain_points: List[PainPoint] = Field(description="3-7 pain points", min_length=3, max_length=7)
    recommendations: List[Recommendation] = Field(description="3-7 recommendations", min_length=3, max_length=7)
    roi_calculation: ROICalculation = Field(description="ROI calculation")
    chatbot_priority: str = Field(description="HIGH, MEDIUM, or LOW")
    key_findings: List[str] = Field(description="3-5 key findings", min_length=3, max_length=5)
    next_steps: List[str] = Field(description="3-5 next steps", min_length=3, max_length=5)
    upsell_note: Optional[str] = Field(description="Optional upsell note if Business package recommended")


# ============================================================================
# AI ANALYZER CLASS
# ============================================================================

class AIAnalyzer:
    """
    AI-powered business analyzer using OpenAI with structured outputs
    
    Version: 3.1
    - Quality Score System
    - Premium Package Recommendation
    - Intelligent Room Count Estimation
    """
    
    def __init__(self):
        """Initialize analyzer with OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-2024-08-06"  # Supports structured outputs
        
        logger.info(f"AIAnalyzer initialized with model: {self.model}")
    
    def _build_system_prompt(self, industry: str, sources: List[Dict]) -> str:
        """Build comprehensive system prompt with V3.1 enhancements"""
        
        sources_text = self._format_sources(sources)
        
        prompt = f"""Du bist ein Senior Business Analyst für ChatPro AI mit Spezialisierung auf die {industry}-Branche.

VERSION 3.1 - PREMIUM-FOCUS + QUALITY SCORE SYSTEM

# QUALITY SCORE SYSTEM (0-200 PUNKTE)

**Auszeichnungen** (0-40):
- Michelin-Stern: +40
- Gault Millau: +35
- Relais & Châteaux: +30
- 5 Sterne: +30

**Preisniveau** (0-30):
- ≥€200/Nacht: +30
- €150-199: +25
- €120-149: +20
- "Luxus"/"Premium": +15

**Gastronomie** (0-25):
- Degustationsmenü: +15
- Weinkarte: +15
- Fine Dining: +20
- Events/Weinproben: +15

**International** (0-30):
- 3+ Sprachen: +30
- 2 Sprachen: +15
- "International guests": +25

**Zusatzleistungen** (0-25):
- Spa/Wellness: +15
- Concierge: +15
- VIP-Service: +20

# PAKET-EMPFEHLUNG

**PREMIUM (€799/Monat)** wenn:
- Quality Score ≥40, ODER
- 3+ Sprachen, ODER
- Michelin/Gault Millau, ODER
- Preis >€120/Nacht

**BUSINESS (€249/Monat)** nur wenn:
- Score <40, UND
- Nur 1-2 Sprachen, UND
- Standard-Hotel

# ZIMMERZAHL-SCHÄTZUNG

Falls room_count == None:

IF Score ≥80: estimated = 10-20 (Luxury)
ELIF Score 40-79: estimated = 15-30 (Premium)
ELSE: estimated = 50-80 (Standard)

# ROI-BERECHNUNG

**Premium-Hotel:**
- Mehrsprachigkeit: rooms × 30 × 0.75 × price × 0.10
- Direktbuchungen: revenue × 0.05 × 0.15
- Upselling: rooms × 30 × 0.70 × 30€
- Staff Saved: 20-30h × 25€ × 4

**KONSERVATIV:**
- Belegung: 70-85%
- Uplift: 5-12%
- ROI: Premium €2.500-5.000, Business €800-1.500

# CHATBOT-AWARE

IF has_chatbot:
  Recommendation: "Upgrade auf Premium"
  Setup: €500-1.000
ELSE:
  Recommendation: "Einführung Chatbot"
  Setup: €1.799 (Business) / €4.999 (Premium)

# PACKAGE DETAILS

**PREMIUM:**
- Setup: €4.999
- Monthly: €799
- Features: 50+ Sprachen, PMS, Account Manager

**BUSINESS:**
- Setup: €1.799
- Monthly: €249
- Features: 2 Sprachen, Basic Integration

# QUELLEN

{sources_text}

# CHATBOT PRIORITY

WICHTIG: Setze chatbot_priority auf HIGH wenn kein Chatbot erkannt wurde!
Ein Chatbot ist eine kritische Grundfunktion für moderne Hotels und sollte höchste Priorität haben.

Falls Chatbot bereits vorhanden: chatbot_priority = MEDIUM (Optimierung bestehender Systeme)

Erstelle jetzt die vollständige Analyse auf DEUTSCH!
"""
        return prompt
    
    def _format_sources(self, sources: List[Dict]) -> str:
        """Format sources for prompt"""
        if not sources:
            return "Keine Quellen verfügbar."
        
        formatted = []
        for i, source in enumerate(sources, 1):
            formatted.append(f"{i}. {source.get('title', 'Unbekannt')} - {source.get('url', 'N/A')}")
        
        return "\n".join(formatted)
    
    async def analyze(
        self,
        crawler_data: Dict,
        industry: str,
        company_name: str,
        sources: List[Dict]
    ) -> Dict:
        """Analyze website and generate structured report"""
        
        try:
            logger.info(f"Starting analysis for {company_name} ({industry})")
            logger.info(f"Crawler: has_chatbot={crawler_data.get('has_chatbot')}, room_count={crawler_data.get('room_count')}")
            
            system_prompt = self._build_system_prompt(industry, sources)
            
            # Build user message using string concatenation
            user_msg = "Analysiere diese Website:\n\n"
            user_msg += f"**UNTERNEHMEN:** {company_name}\n"
            user_msg += f"**BRANCHE:** {industry}\n\n"
            user_msg += "**CRAWLER-DATEN:**\n"
            user_msg += f"- URL: {crawler_data.get('url', 'N/A')}\n"
            user_msg += f"- Title: {crawler_data.get('title', 'N/A')}\n"
            user_msg += f"- Description: {crawler_data.get('meta_description', 'N/A')}\n"
            user_msg += f"- Has Chatbot: {crawler_data.get('has_chatbot', False)}\n"
            user_msg += f"- Chatbot Type: {crawler_data.get('chatbot_type', 'None')}\n"
            user_msg += f"- Room Count: {crawler_data.get('room_count', 'None')}\n"
            user_msg += f"- Mobile: {crawler_data.get('mobile_responsive', False)}\n"
            user_msg += f"- Languages: {crawler_data.get('languages', [])}\n\n"
            user_msg += "**AUFGABE:**\n"
            user_msg += "1. Berechne Quality Score\n"
            user_msg += "2. Schätze room_count falls None\n"
            user_msg += "3. Empfehle PREMIUM wenn Score >=40\n"
            user_msg += "4. Berechne ROI\n"
            user_msg += "5. DEUTSCH!\n\n"
            user_msg += "Erstelle die Analyse!"
            
            # Call OpenAI with structured output
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                response_format=AnalysisResult,
                temperature=0.7
            )
            
            result = completion.choices[0].message.parsed
            
            if not result:
                raise ValueError("No structured output received")
            
            logger.info(f"✅ Analysis complete!")
            logger.info(f"   Package: {result.recommended_package}")
            logger.info(f"   Quality Score: {result.quality_score}")
            logger.info(f"   Room Count: {result.estimated_room_count} ({result.room_count_method})")
            logger.info(f"   ROI: €{result.roi_calculation.monthly_roi_euro:,}")
            
            return result.model_dump()
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def test():
        test_data = {
            "url": "https://engel-sasbachwalden.de/",
            "title": "Der Engel Sasbachwalden – Genießen zwischen Himmel und Erde seit 1764",
            "meta_description": "Michelin-Restaurant, Degustationsmenü, Weinproben, Events",
            "has_chatbot": False,
            "chatbot_type": None,
            "room_count": None,
            "mobile_responsive": True,
            "languages": ["de"]
        }
        
        sources = [
            {"title": "Vynta AI Study", "url": "https://vynta.ai"},
            {"title": "AirDNA Study", "url": "https://airdna.co"}
        ]
        
        analyzer = AIAnalyzer()
        
        print("\n" + "="*80)
        print("ANALYZER V3.1 TEST")
        print("="*80)
        
        result = await analyzer.analyze(
            crawler_data=test_data,
            industry="hotel",
            company_name="Hotel Engel Sasbachwalden",
            sources=sources
        )
        
        print(f"\n✅ Results:")
        print(f"   Package: {result['recommended_package']}")
        print(f"   Setup: €{result['package_details']['setup_cost_euro']:,}")
        print(f"   Monthly: €{result['package_details']['monthly_cost_euro']:,}")
        print(f"   Quality Score: {result['quality_score']}/200")
        print(f"   Room Method: {result['room_count_method']}")
        print(f"   Rooms: {result['estimated_room_count']}")
        print(f"   ROI: €{result['roi_calculation']['monthly_roi_euro']:,}")
        print(f"   Multiplier: {result['roi_calculation']['roi_multiplier']}x")
        print(f"   Break-Even: {result['roi_calculation']['break_even_months']} Mon")
    
    asyncio.run(test())
