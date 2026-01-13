"""
ChatPro AI - Business Analyzer
PRODUCTION-READY VERSION 2.0 with realistic ROI calculations
Based on 4 real ROI studies (Vynta AI, AirDNA, Go-Globe, Chatarmin, Technova)
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
    sources_used: List[int] = Field(description="List of source IDs used in calculation")


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
    Version 2.0 - Production-Ready with Realistic ROI
    """
    
    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-2024-08-06"  # Supports Structured Outputs
        logger.info(f"AIAnalyzer V2.0 initialized with model: {self.model}")
    
    def _build_system_prompt(self, industry: str, sources_context: str) -> str:
        """Build comprehensive system prompt with realistic ROI guidelines"""
        
        # Industry-specific contexts with realistic ROI benchmarks
        industry_contexts = {
            "hotel": """
## HOTEL & GASTGEWERBE - ROI BENCHMARKS

**Typische Geschäftsgröße**:
- Klein: 10-30 Zimmer, 2-5 Mitarbeiter
- Mittel: 30-80 Zimmer, 10-25 Mitarbeiter
- Groß: 80+ Zimmer, 30+ Mitarbeiter

**Realistische ROI-Benchmarks** (Vynta AI Study 2026):
- Direct Bookings: +20-30% (nicht +50%!)
- Upselling Conversion: 15-25%
- Staff Time Saved: 15-25h/Woche (bei 50+ Zimmer)
- Response Time: 4-8h → <2min
- CSAT Improvement: +10-15%

**Konservative ROI-Formel**:
Klein (10-30 Zimmer): €500-900/Monat
Mittel (30-80 Zimmer): €1.200-2.500/Monat
Groß (80+ Zimmer): €2.500-5.000/Monat
""",
            "vacation_rental": """
## FERIENWOHNUNGEN - ROI BENCHMARKS

**Typische Geschäftsgröße**:
- Klein: 1-5 Einheiten, Einzelunternehmer
- Mittel: 5-20 Einheiten, 2-8 Mitarbeiter
- Groß: 20+ Einheiten, Verwaltungsgesellschaft

**Realistische ROI-Benchmarks** (AirDNA Study):
- Dynamic Pricing Impact: +10-15% (nicht +40%!)
- Direct Booking vs OTA: Spart 15% Provision
- Staff Time Saved: 10-20h/Woche (bei 10+ Einheiten)
- Professional Hosts vs Casual: 2-3x mehr Umsatz

**Konservative ROI-Formel**:
Klein (1-5 Einheiten): €200-600/Monat (nur bei >3 Einheiten profitabel)
Mittel (5-20 Einheiten): €800-1.500/Monat
Groß (20+ Einheiten): €2.000-4.000/Monat
""",
            "restaurant": """
## RESTAURANTS & CAFÉS - ROI BENCHMARKS

**Typische Geschäftsgröße**:
- Klein: 20-50 Plätze, 3-8 Mitarbeiter
- Mittel: 50-120 Plätze, 10-25 Mitarbeiter
- Groß: 120+ Plätze, Kette, 30+ Mitarbeiter

**Realistische ROI-Benchmarks**:
- Reservierungs-Automatisierung: 60-80% ohne Personal
- No-Show-Reduktion: -30% durch Reminder
- Telefon-Volumen: -50%
- Staff Time Saved: 10-20h/Woche

**Konservative ROI-Formel**:
Klein (20-50 Plätze): €400-800/Monat
Mittel (50-120 Plätze): €1.200-2.200/Monat
Groß (120+ Plätze): €2.500-5.000/Monat
""",
            "fitness": """
## FITNESS & WELLNESS - ROI BENCHMARKS

**Typische Geschäftsgröße**:
- Klein: 1 Studio, 100-300 Mitglieder, 2-5 Trainer
- Mittel: 2-5 Standorte, 500-1.500 Mitglieder
- Groß: 5+ Standorte, 2.000+ Mitglieder

**Realistische ROI-Benchmarks**:
- Lead Conversion: +10-20% (nicht +50%!)
- Churn Reduction: -5-10%
- Terminbuchungen: 70% automatisiert
- Staff Time Saved: 15-30h/Woche

**Konservative ROI-Formel**:
Klein (100-300 Mitglieder): €600-1.200/Monat
Mittel (500-1.500 Mitglieder): €1.500-3.000/Monat
Groß (2.000+ Mitglieder): €3.000-6.000/Monat
""",
            "salon": """
## SALONS & BEAUTY - ROI BENCHMARKS

**Typische Geschäftsgröße**:
- Klein: 1-2 Stühle, Einzelunternehmer
- Mittel: 3-8 Stühle, 3-10 Mitarbeiter
- Groß: 10+ Stühle, Kette, 15+ Mitarbeiter

**Realistische ROI-Benchmarks**:
- Terminbuchungen: 80% automatisiert
- No-Show-Reduktion: -40% durch Reminder
- Upselling: +15-25% (Produkte, Add-ons)
- Staff Time Saved: 8-15h/Woche

**Konservative ROI-Formel**:
Klein (1-2 Stühle): €200-400/Monat (grenzwertig profitabel)
Mittel (3-8 Stühle): €700-1.300/Monat
Groß (10+ Stühle): €1.500-3.000/Monat
""",
            "fahrschule": """
## FAHRSCHULEN - ROI BENCHMARKS

**Typische Geschäftsgröße**:
- Klein: 1-2 Fahrlehrer, 20-50 Schüler
- Mittel: 3-8 Fahrlehrer, 80-200 Schüler
- Groß: 10+ Fahrlehrer, 300+ Schüler

**Realistische ROI-Benchmarks**:
- Lead Conversion: +15-25%
- Terminbuchungen: 90% automatisiert
- Theorie-Fragen: 24/7 Support
- Staff Time Saved: 10-20h/Woche

**Konservative ROI-Formel**:
Klein (20-50 Schüler): €800-1.500/Monat
Mittel (80-200 Schüler): €1.800-3.500/Monat
Groß (300+ Schüler): €4.000-8.000/Monat
""",
            "immobilien": """
## IMMOBILIENMAKLER - ROI BENCHMARKS

**Typische Geschäftsgröße**:
- Klein: 1-2 Makler, 10-30 Objekte
- Mittel: 3-10 Makler, 50-150 Objekte
- Groß: 15+ Makler, 200+ Objekte

**Realistische ROI-Benchmarks**:
- Lead Qualification: 70% automatisiert
- Besichtigungsbuchungen: +30%
- Response Time: 24h → <5min
- Staff Time Saved: 15-30h/Woche

**Konservative ROI-Formel**:
Klein (10-30 Objekte): €800-1.500/Monat
Mittel (50-150 Objekte): €2.000-4.000/Monat
Groß (200+ Objekte): €5.000-10.000/Monat
"""
        }
        
        # Get industry-specific context
        industry_context = industry_contexts.get(industry, industry_contexts.get("hotel", ""))
        
        # Build complete prompt
        prompt = f"""Du bist ein **Senior Business Analyst** mit 15+ Jahren Erfahrung in der digitalen Transformation und ROI-Bewertung von AI-Automatisierungslösungen. Du analysierst Unternehmenswebsites, um **realistische, konservative und glaubwürdige** Business Intelligence Reports zu erstellen.

## KONTEXT: CHATPRO AI

**Produkt**: Premium B2B SaaS AI-Chatbot für Kundenservice-Automatisierung
**Kernversprechen**: 
- 95%+ Automatisierung von Routine-Anfragen
- 24/7 Verfügbarkeit in 50+ Sprachen
- Nahtlose Integration in PMS/CRM/ERP-Systeme
- DSGVO-konform & sicher

**Pricing** (2026):
- **Business**: €1.799 Setup + €249/Monat
- **Premium**: €4.999 Setup + €799/Monat  
- **Enterprise**: €10.000+ Setup + Custom Pricing

{industry_context}

## KRITISCHE ROI-VALIDIERUNGSREGELN

### 1. MAXIMALER ROI-CHECK
Monatlicher ROI DARF NICHT > 10x ChatPro AI Kosten sein

**Beispiel**:
- AI-Kosten: €249/Monat → Max €2.490/Monat
- Wenn berechnet: €6.000/Monat → **REDUZIERE AUF €2.000-2.500!**

### 2. BREAK-EVEN ZEITRAUM
Break-Even MUSS zwischen 3-12 Monaten liegen

### 3. BUSINESS-GRÖSSEN-CHECK
- Website < 5 Seiten: Max €500/Monat ROI (SEHR KLEIN)
- Website < 15 Seiten: Max €1.200/Monat ROI (KLEIN)
- Website < 40 Seiten: Max €3.000/Monat ROI (MITTEL)
- Website 40+ Seiten: Max €8.000/Monat ROI (GROSS)

### 4. KONSERVATIVE ANNAHMEN
**IMMER verwenden**:
- Conversion Uplift: +5-10% (NICHT +20-50%!)
- Direct Booking Increase: +5-8% (NICHT +30%!)
- Lead Qualification: +10-15% (NICHT +50%!)
- Staff Time Saved: 10-25h/Woche (NICHT 40h!)

### 5. ROI TRANSPARENZ
**Wenn ROI > €2.000/Monat**: Erkläre detailliert wie berechnet, welche Annahmen, welche Risiken.

## BRANCHEN-SPEZIFISCHE QUELLEN

{sources_context}

Verwende diese Quellen, um deine Analysen zu untermauern. Referenziere mindestens 3-5 Quellen in der ROI-Berechnung.

## FINALE CHECKLISTE

Bevor du die Analyse ausgibst, prüfe:

✅ **Sprache**: 100% Deutsch (keine englischen Phrasen!)
✅ **ROI Realismus**: Monatlicher ROI < 10x AI-Kosten
✅ **Business-Größe**: ROI passt zur Unternehmensgröße
✅ **Quellen**: Mindestens 3-5 Quellen-IDs referenziert
✅ **Transparenz**: ROI-Formel klar erklärt
✅ **Konservativ**: Annahmen sind vorsichtig (5-10%, nicht 30-50%!)
✅ **Break-Even**: 3-12 Monate (nicht <2 oder >18!)
✅ **Evidence**: Pain Points basieren auf crawler_data
✅ **Actionable**: Recommendations sind umsetzbar

## WICHTIG: EHRLICHKEIT > VERKAUF

**Unser Ziel**: Glaubwürdige Analysen, die echten Mehrwert bieten.
**NICHT unser Ziel**: Unrealistische Zahlen, um Verkäufe zu forcieren.

**Wenn ein Business ZU KLEIN ist** (z.B. 1-2 Zimmer Pension):
"Bei dieser Geschäftsgröße ist der ROI marginal. ChatPro AI lohnt sich ab ~10 Zimmer bzw. €5.000+ monatlichem Umsatz."

**Das ist PROFESSIONELL und baut VERTRAUEN auf!** 💪

Antworte immer auf Deutsch und im JSON-Format gemäß dem AnalysisResult Schema.
"""
        
        return prompt

    def _build_user_prompt(self, crawler_data: Dict, company_name: str) -> str:
        """Build user prompt with website data"""
        
        # Extract key data points
        url = crawler_data.get("url", "N/A")
        page_count = crawler_data.get("page_count", 0)
        languages = crawler_data.get("languages", [])
        has_chatbot = crawler_data.get("has_chatbot", False)
        chatbot_type = crawler_data.get("chatbot_type", "None")
        is_mobile_friendly = crawler_data.get("is_mobile_friendly", False)
        has_contact_info = crawler_data.get("has_contact_info", False)
        lead_forms = crawler_data.get("lead_forms", [])
        
        # Build prompt
        prompt = f"""UNTERNEHMEN ZU ANALYSIEREN: {company_name}

WEBSITE-DATEN:
- URL: {url}
- Seitenanzahl: {page_count}
- Sprachen: {', '.join(languages) if languages else 'Deutsch (angenommen)'}
- Mobile-freundlich: {'Ja' if is_mobile_friendly else 'Nein'}
- Hat Chatbot: {'Ja' if has_chatbot else 'Nein'}
- Chatbot-Typ: {chatbot_type}
- Lead-Formulare: {len(lead_forms)} gefunden
- Kontakt-Info: {'Vorhanden' if has_contact_info else 'Nicht gefunden'}

GESCHÄFTSGRÖSSEN-INDIKATOR:
- {page_count} Seiten → {'SEHR KLEIN' if page_count < 5 else 'KLEIN' if page_count < 15 else 'MITTEL' if page_count < 40 else 'GROSS'}
- Max realistischer ROI: {'€500/Monat' if page_count < 5 else '€1.200/Monat' if page_count < 15 else '€3.000/Monat' if page_count < 40 else '€8.000/Monat'}

AUFGABE:
Erstelle eine umfassende Geschäftsanalyse für {company_name} mit:

1. PAIN POINTS (3-7 Stück):
   - Fokus auf geschäftliche Auswirkungen (nicht technische Details)
   - Beispiel: "Keine 24/7 Verfügbarkeit führt zu geschätzten 15-25% verlorenen Buchungen"
   - NICHT: "Kein Chatbot vorhanden"

2. RECOMMENDATIONS (3-7 Stück):
   - Konkret und umsetzbar
   - Mit Implementierungsaufwand
   - Geschäftlicher Wert klar kommuniziert

3. ROI-BERECHNUNG:
   - Basierend auf Geschäftsgröße ({page_count} Seiten)
   - Konservative Annahmen (5-10% Uplift)
   - Break-Even 3-12 Monate
   - Formel transparent erklären
   - Mindestens 3-5 Quellen referenzieren

FOKUS-BEREICHE:
1. Aktuelle digitale Präsenz
2. Kundenerfahrung
3. Automatisierungspotenzial (besonders Chatbot)
4. Umsatzoptimierung
5. Wettbewerbspositionierung

KRITISCH:
- Sei realistisch mit Zahlen
- Basiere ROI auf Branchendaten
- Liefere umsetzbare Einblicke
- Zeige klaren Geschäftswert
- 100% Deutsch"""

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
        logger.info(f"Starting V2.0 analysis for {company_name} in {industry} industry")
        
        try:
            # Build sources context
            sources_context = self._format_sources(sources or [])
            
            # Build prompts
            system_prompt = self._build_system_prompt(industry, sources_context)
            user_prompt = self._build_user_prompt(crawler_data, company_name)
            
            # Log prompt length for debugging
            logger.info(f"System prompt length: {len(system_prompt)} chars")
            logger.info(f"User prompt length: {len(user_prompt)} chars")
            
            # Call OpenAI with Structured Outputs
            logger.info(f"Calling OpenAI {self.model} with structured output (V2.0 prompt)...")
            
            completion = self.client.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=AnalysisResult,
                temperature=0.5  # Lower for more conservative/consistent results
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
            result["analyzer_version"] = "2.0"
            
            logger.info(f"✅ Analysis V2.0 completed for {company_name}")
            logger.info(f"Generated {len(result['pain_points'])} pain points and {len(result['recommendations'])} recommendations")
            logger.info(f"ROI: €{result['roi_calculation']['monthly_roi_euro']}/month, Break-even: {result['roi_calculation']['break_even_months']} months")
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            logger.error(f"Crawler data: {crawler_data}")
            raise
    
    def _format_sources(self, sources: List[Dict]) -> str:
        """Format sources for prompt context"""
        if not sources:
            return "Keine spezifischen Branchenquellen verfügbar."
        
        formatted = "BRANCHEN-SPEZIFISCHE QUELLEN:\n\n"
        for idx, source in enumerate(sources, 1):
            formatted += f"[{idx}] {source.get('title', 'Unbekannt')}\n"
            formatted += f"    URL: {source.get('url', 'N/A')}\n"
            formatted += f"    Key Insight: {source.get('description', 'N/A')}\n\n"
        
        formatted += "\nVerwende diese Quellen zur Untermauerung deiner Analyse mit Branchendaten.\n"
        formatted += "Referenziere Quellen mit [1], [2], etc. in deiner ROI-Berechnung.\n"
        return formatted


# Example usage for testing
if __name__ == "__main__":
    # Test the analyzer
    analyzer = AIAnalyzer()
    
    test_crawler_data = {
        "url": "https://guesthouseholland.com",
        "page_count": 12,
        "languages": ["en", "nl"],
        "has_chatbot": True,
        "chatbot_type": "Unknown",
        "is_mobile_friendly": True,
        "has_contact_info": True,
        "lead_forms": ["contact", "booking"]
    }
    
    test_sources = [
        {
            "title": "Vynta AI Hotel Study 2026",
            "url": "https://vynta.ai/blog/hotel-chatbot/",
            "description": "Direct bookings +20-30%, Upselling 15-25%, Staff time saved 15-25h/week"
        },
        {
            "title": "AirDNA Vacation Rental Study",
            "url": "https://www.airdna.co/",
            "description": "Dynamic pricing +10-15%, Professional hosts 2-3x more revenue"
        }
    ]
    
    result = analyzer.analyze(
        crawler_data=test_crawler_data,
        industry="vacation_rental",
        company_name="Guest House Holland",
        sources=test_sources
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
