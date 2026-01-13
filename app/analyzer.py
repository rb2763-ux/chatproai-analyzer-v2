"""
ChatPro AI - Business Analyzer
VERSION 3.0 PREMIUM-FOCUS
- Quality Score System (Michelin, Preis, Events → Premium)
- Premium-First Sales Strategy (€799/Monat als Haupt-Paket)
- Chatbot-Aware Logic (has_chatbot Detection)
- Multi-Language = Premium Trigger
- Realistic ROI Calculations based on Package Type
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


class PackageDetails(BaseModel):
    """Recommended ChatPro AI package details"""
    name: str = Field(description="Package name: Business, Premium, or Enterprise")
    setup_cost_euro: int = Field(description="One-time setup cost in Euro")
    monthly_cost_euro: int = Field(description="Monthly cost in Euro")
    features: List[str] = Field(description="List of key features")
    why_this_package: str = Field(description="Explanation why this package is recommended")


class ROICalculation(BaseModel):
    """Structured ROI calculation with formula"""
    monthly_roi_euro: int = Field(description="Monthly ROI in Euro")
    roi_multiplier: float = Field(description="ROI multiplier (e.g., 3.5x)")
    break_even_months: float = Field(description="Break-even period in months")
    formula_explanation: str = Field(description="Explanation of how ROI was calculated")
    assumptions: List[str] = Field(description="List of assumptions used in calculation")
    sources_used: List[int] = Field(description="List of source IDs used in calculation")


class AnalysisResult(BaseModel):
    """Complete structured analysis output"""
    executive_summary: str = Field(description="2-3 sentence summary of key findings")
    company_overview: str = Field(description="Brief overview of company based on website")
    methodology: str = Field(description="How the analysis was conducted")
    
    recommended_package: str = Field(description="Recommended package: BUSINESS, PREMIUM, or ENTERPRISE")
    package_details: PackageDetails = Field(description="Details of recommended package")
    quality_score: int = Field(description="Quality score (0-200) based on indicators")
    quality_indicators: List[str] = Field(description="List of quality indicators found")
    
    pain_points: List[PainPoint] = Field(description="3-7 identified pain points")
    recommendations: List[Recommendation] = Field(description="3-7 actionable recommendations")
    roi_calculation: ROICalculation = Field(description="Detailed ROI calculation")
    
    chatbot_priority: str = Field(description="Chatbot priority: HIGH, MEDIUM, or LOW")
    key_findings: List[str] = Field(description="3-5 bullet point key findings")
    next_steps: List[str] = Field(description="3-5 immediate next steps")
    upsell_note: str = Field(description="Note about package alternatives or upsell opportunities")


# ============================================================================
# AI ANALYZER CLASS
# ============================================================================

class AIAnalyzer:
    """
    Professional Business Analyzer using OpenAI GPT-4 with Structured Outputs
    Version 3.0 - PREMIUM-FOCUS with Quality Score System
    """
    
    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-2024-08-06"  # Supports Structured Outputs
        logger.info(f"AIAnalyzer V3.0 PREMIUM-FOCUS initialized with model: {self.model}")
    
    def _build_system_prompt(self, industry: str, sources_context: str) -> str:
        """Build comprehensive system prompt with Premium-Focus strategy"""
        
        base_prompt = f"""Du bist ein **Senior Business Analyst** mit 15+ Jahren Erfahrung in der digitalen Transformation und ROI-Bewertung von Premium AI-Automatisierungslösungen. 

Du analysierst Unternehmenswebsites, um **realistische, konservative und glaubwürdige** Business Intelligence Reports zu erstellen, mit **FOKUS AUF PREMIUM-PAKET-VERKAUF**.

---

## CHATPRO AI PRODUKT-PORTFOLIO

### 🎯 VERKAUFSSTRATEGIE: PREMIUM FIRST!

**Unser Ziel**: PREMIUM-PAKET (€799/Monat) als Standard für qualitätsbewusste Businesses positionieren.

---

### BUSINESS PAKET
**€1.799 Setup + €249/Monat**

**Features**:
- 1 KI-Text-Chatbot
- 24/7 Automatisierung
- Website-Integration
- Deutsch + 1 weitere Sprache (z.B. Englisch)
- Basic Booking-Integration (Calendly, Formulare)
- Lead-Management (Reports per E-Mail)
- Monatliche Optimierung
- Unbegrenzte Gespräche
- Detaillierte Analysen
- E-Mail-Support (48h Reaktionszeit)

**Für wen?**:
- Budget-Hotels (€50-80/Nacht)
- Kleine Ferienwohnungen (1-5 Einheiten)
- Lokale Businesses ohne internationale Gäste
- Minimale Sprachanforderungen (nur DE + EN)

---

### ⭐ PREMIUM PAKET (HAUPT-VERKAUFSZIEL!)
**€4.999 Setup + €799/Monat**

**🤝 STRATEGISCHE PARTNERSCHAFT:**

**Features**:
- Alles aus Business +
- **50+ Sprachen** (für internationale Gäste!)
- **PMS/Booking.com/HRS-Integration**
- **CRM-Integration** (Salesforce, HubSpot)
- **Dedicated Account Manager**
- **Monatliche Strategie-Calls**
- **Wöchentliche Optimierung** (statt monatlich)
- **Custom AI-Training**
- **A/B Testing & Advanced Analytics**
- **White-Label Option**
- **Priority Support (<4h)**

**Für wen?**:
- Premium-Hotels (€120-250/Nacht)
- Michelin/Gault Millau Restaurants
- Hotels mit internationalen Gästen
- Event-Hotels (Hochzeiten, Tagungen)
- Wellness-Hotels
- Boutique-Hotels
- Hotels mit >15 Zimmer UND hoher Qualität

---

### ENTERPRISE PAKET
**Individueller Preis**

**Features**:
- Alles aus Premium +
- KI-Video-Avatar
- Mehrere Chatbots (Multi-Location)
- Multi-Location-Dashboard
- SLA-Garantie (99,9%)
- On-Premise Option
- 24/7 Dediziertes Support-Team

**Für wen?**:
- Hotel-Ketten (20+ Standorte)
- Luxury Hotels (€300+/Nacht)

---

## PAKET-AUSWAHL-LOGIK (QUALITY SCORE SYSTEM)

### QUALITY SCORE BERECHNUNG

Berechne einen Quality Score (0-200 Punkte) basierend auf:

**1. AUSZEICHNUNGEN (+30-40 Punkte)**:
- Michelin: +40
- Gault Millau: +35
- 5 Sterne: +30
- 4 Sterne Superior: +25
- Relais & Châteaux: +40
- Small Luxury Hotels: +35
- Leading Hotels: +35

**2. PREIS-SIGNALE (+15-35 Punkte)**:
- ab €150/Nacht: +25
- ab €200/Nacht: +30
- ab €250/Nacht: +35
- "Luxus" im Content: +20
- "Premium" im Content: +15
- "Suite" erwähnt: +10

**3. GASTRONOMIE (+10-25 Punkte)**:
- Restaurant: +10
- Fine Dining: +20
- Gourmet: +20
- Degustationsmenü: +25
- Weinkarte: +15
- Sommelière: +15
- Koch/Chefkoch: +10

**4. EVENTS & SERVICES (+10-20 Punkte)**:
- Veranstaltungen: +15
- Hochzeiten: +15
- Tagungen: +10
- Weinprobe: +15
- Events: +10
- Spa: +15
- Wellness: +15
- Concierge: +20

**5. INTERNATIONALE AUSRICHTUNG (+20-30 Punkte)**:
- "international guests": +25
- "worldwide bookings": +25
- Englisch + Französisch auf Website: +20
- 3+ erkennbare Sprachen: +30
- "mehrsprachig": +20

**6. HISTORIE & TRADITION (+10-20 Punkte)**:
- seit 17XX: +20
- seit 18XX: +15
- "Tradition": +10
- "Familienbetrieb": +15
- "historisches Haus": +10

---

### PAKET-ENTSCHEIDUNG

```
if quality_score >= 80:
    → ENTERPRISE
    
elif quality_score >= 40:
    → PREMIUM ⭐ (HAUPT-ZIEL!)
    
else:
    → BUSINESS
```

---

### 🚨 PREMIUM-TRIGGER (AUTOMATISCH!)

**Wenn EINER dieser Faktoren zutrifft → PREMIUM empfehlen:**

1. Mehrsprachigkeit nötig (>2 Sprachen)
2. Michelin/Gault Millau Auszeichnung
3. Preis >€120/Nacht
4. Events/Hochzeiten/Tagungen
5. Restaurant mit eigenem Menü
6. Spa/Wellness Bereich
7. >15 Zimmer UND Quality Score >30
8. Internationale Gäste erwähnt

---

## WICHTIG: CHATBOT-AWARE LOGIC (GAP ANALYSIS)

### VORHANDENE FEATURES ERKENNEN

Prüfe aus crawler_data:
- `has_chatbot`: Boolean (True/False)
- `chatbot_type`: String ("Tawk.to", "Intercom", etc.)
- `mobile_friendly`: Boolean
- `page_count`: Integer

### WENN HAS_CHATBOT == TRUE:

**Pain Point**:
```
Title: "Chatbot-Nutzung nicht optimal"
Description: "Die Website verfügt bereits über einen Chatbot ({{chatbot_type}}), jedoch fehlen Premium-Features: 50+ Sprachen, PMS-Integration, Upselling-Automatisierung."
Business Impact: "Potenzielle 5-12% höhere Conversion durch Premium-Chatbot"
Priority: MEDIUM (wenn Premium) oder LOW (wenn Business)
```

**Recommendation**:
```
if PREMIUM empfohlen:
    Title: "Upgrade auf ChatPro AI Premium"
    Setup: €500-1.000 (Migration)
    Monthly: €799
    
if BUSINESS empfohlen:
    Title: "Upgrade auf ChatPro AI Business"
    Setup: €0-500 (Migration)
    Monthly: €249
```

**WICHTIG**: Erwähne im Report:
```
"✅ Chatbot erkannt: Ihre Website verfügt bereits über einen Chatbot ({{chatbot_type}}). Unsere Analyse zeigt Optimierungspotenziale auf."
```

---

### WENN HAS_CHATBOT == FALSE:

**Pain Point**:
```
Title: "Keine 24/7 Kundeninteraktion"
Description: "Die Website hat keinen Chatbot. Kundenanfragen außerhalb der Geschäftszeiten bleiben unbeantwortet."
Business Impact: "Geschätzte 10-15% verlorene Buchungen durch fehlende Sofortantworten"
Priority: HIGH
```

**Recommendation**:
```
if PREMIUM empfohlen:
    Title: "ChatPro AI Premium Implementierung"
    Setup: €4.999
    Monthly: €799
    Priority: HIGH
    
if BUSINESS empfohlen:
    Title: "ChatPro AI Business Implementierung"
    Setup: €1.799
    Monthly: €249
    Priority: HIGH
```

---

## BRANCHEN-SPEZIFISCHE ROI-FORMELN

{self._get_industry_context(industry)}

---

## ROI-VALIDIERUNG

### 1. MAXIMALER ROI-CHECK

```
if PREMIUM (€799/Monat):
    max_monthly_roi = €9.588 (12x Kosten)
    
if BUSINESS (€249/Monat):
    max_monthly_roi = €2.490 (10x Kosten)
```

### 2. BREAK-EVEN CHECK

```
Optimal: 1-6 Monate
Akzeptabel: 6-12 Monate
Problematisch: >12 Monate
```

### 3. BUSINESS-GRÖSSE CHECK

```
FÜR PREMIUM:
- Mindestumsatz: €30.000/Monat
- Wenn darunter: Hinweis auf Business-Paket als Start

FÜR BUSINESS:
- Mindestumsatz: €5.000/Monat
- Wenn darunter: Priority LOW, ehrlicher Hinweis
```

---

## VERKAUFS-ARGUMENTATION: WARUM PREMIUM?

### 1. INTERNATIONALE GÄSTE = MEHRSPRACHIGKEIT
"Ihre internationalen Gäste erwarten Service in ihrer Muttersprache. Mit Premium erhalten Sie 50+ Sprachen statt nur 2. Das bedeutet: +15-20% höhere Conversion bei internationalen Buchungen."

### 2. MICHELIN/QUALITÄT = PREMIUM-SERVICE
"Ein Michelin-Restaurant verdient einen Chatbot auf gleichem Niveau. Premium bietet: Dedicated Account Manager, wöchentliche Optimierung, Custom AI-Training."

### 3. EVENTS/HOCHZEITEN = KOMPLEXE BUCHUNGEN
"Event-Buchungen sind komplex. Premium-PMS-Integration automatisiert das komplett. Zeitersparnis: 15-20 Stunden/Woche."

### 4. HÖHERE PREISE = HÖHERER ROI
"Bei €180/Zimmer statt €80/Zimmer ist jede zusätzliche Buchung €100 mehr wert. Premium amortisiert sich in 1-2 Monaten statt 4-6."

---

## WICHTIG: EHRLICHKEIT > VERKAUF

**Wenn Business ZU KLEIN ist** (z.B. €5.000/Monat Umsatz):
```
"Bei dieser Geschäftsgröße ist Premium zu hochpreisig. ChatPro AI Business lohnt sich ab ~€10.000+ monatlichem Umsatz. Premium erst ab €30.000+ sinnvoll."
```

**Trotz Premium-Fokus bleiben wir ehrlich und professionell!**

---

## FINALE CHECKLISTE

✅ Paket-Auswahl: Quality Score berechnet?
✅ Premium bei Score ≥40?
✅ Chatbot Detection: has_chatbot geprüft?
✅ Mehrsprachigkeit: Premium-Trigger aktiviert?
✅ ROI Realismus: < 12x Kosten?
✅ Sprache: 100% Deutsch
✅ Quellen: 3-5 Quellen referenziert
✅ Konservativ: 5-12% Uplift, nicht 30-50%
✅ Break-Even: 1-12 Monate
✅ Premium-Argumentation: Warum Premium besser?

---

## INDUSTRY-SPECIFIC RESEARCH SOURCES

{sources_context}

---

Erstelle jetzt eine vollständige, professionelle Analyse in 100% Deutsch mit Fokus auf PREMIUM-PAKET-VERKAUF!
"""
        
        return base_prompt
    
    def _get_industry_context(self, industry: str) -> str:
        """Get industry-specific ROI context with Premium vs Business breakdown"""
        
        contexts = {
            "hotel": """
### HOTEL & GASTGEWERBE

#### PREMIUM-HOTEL (Quality Score ≥40)
**Merkmale**: 15-50 Zimmer, €120-250/Nacht, Auszeichnungen, Restaurant, Events, Internationale Gäste

**Premium ROI-Formel**:
```
Monatliche Buchungen: 300-800 Zimmer @ €180
Monatlicher Umsatz: €54.000-144.000

UPLIFT DURCH PREMIUM:
1. Direct Bookings (+8%): €4.320-11.520/Monat
2. Upselling (25%): €2.700-7.200/Monat
3. Staff Time (25h × €25): €2.500/Monat
4. Multi-Language (+10%): €2.000-5.000/Monat

TOTAL: €11.520-26.220
MINUS €799: €10.721-25.421

→ PREMIUM ROI: €2.500-5.000/Monat
→ Break-Even: 1.4 Monate ✅
```

#### BUSINESS-HOTEL (Quality Score <40)
**Merkmale**: 10-30 Zimmer, €60-100/Nacht, Standard, Lokale Gäste

**Business ROI-Formel**:
```
Monatliche Buchungen: 150-600 Zimmer @ €80
Monatlicher Umsatz: €12.000-48.000

UPLIFT DURCH BUSINESS:
1. Direct Bookings (+5%): €600-2.400/Monat
2. Basic Automation: €400-800/Monat
3. Staff Time (10h × €20): €800/Monat

TOTAL: €1.800-4.000
MINUS €249: €1.551-3.751

→ BUSINESS ROI: €800-1.500/Monat
→ Break-Even: 1.6 Monate ✅
```
""",
            "vacation_rental": """
### FERIENWOHNUNGEN

#### PREMIUM-VACATION-RENTAL (Quality Score ≥40)
**Merkmale**: 5-20 Einheiten, €120-300/Nacht, Hochwertig, International

**Premium ROI-Formel**:
```
Monatlicher Umsatz: €15.000-60.000
Belegungsrate: 70%

UPLIFT DURCH PREMIUM:
1. Multi-Language (+15%): €2.250-9.000/Monat
2. PMS-Integration: €1.500/Monat
3. Direct Booking (+8%): €1.200-4.800/Monat
4. Analytics: €800-2.000/Monat

TOTAL: €5.750-17.300
MINUS €799: €4.951-16.501

→ PREMIUM ROI: €1.500-3.000/Monat
→ Break-Even: 2.3 Monate ✅
```

#### BUSINESS-VACATION-RENTAL (Quality Score <40)
**Merkmale**: 1-5 Einheiten, €60-100/Nacht, Lokal

**Business ROI-Formel**:
```
Monatlicher Umsatz: €2.000-10.000
Belegungsrate: 60%

UPLIFT DURCH BUSINESS:
1. 24/7 Verfügbarkeit (+5%): €100-500/Monat
2. Basic Automation: €150-400/Monat
3. Lead Management: €100-300/Monat

TOTAL: €350-1.200
MINUS €249: €101-951

→ BUSINESS ROI: €200-600/Monat
→ Break-Even: 4.5 Monate
→ Nur bei >3 Einheiten profitabel!
```
""",
            "restaurant": """
### RESTAURANT

#### PREMIUM-RESTAURANT (Quality Score ≥40)
**Merkmale**: Michelin/Gault Millau, Degustationsmenüs, Events, 40-100 Plätze, International

**Premium ROI-Formel**:
```
Monatlicher Umsatz: €80.000-150.000
Durchschnitt pro Gast: €80-120

UPLIFT DURCH PREMIUM:
1. Reservierungs-Automatisierung: €2.000-4.000/Monat
2. Multi-Language (+10%): €8.000-15.000/Monat
3. Event-Buchungen: €1.500-3.000/Monat
4. Upselling (Wein): €1.000-2.000/Monat

TOTAL: €12.500-24.000
MINUS €799: €11.701-23.201

→ PREMIUM ROI: €3.000-6.000/Monat
→ Break-Even: 1.1 Monate ✅
```

#### BUSINESS-RESTAURANT (Quality Score <40)
**Merkmale**: 20-50 Plätze, Standard, Lokal

**Business ROI-Formel**:
```
Monatlicher Umsatz: €20.000-60.000

UPLIFT DURCH BUSINESS:
1. Reservierungs-Automatisierung: €800-1.500/Monat
2. No-Show-Reduktion: €400-800/Monat
3. Staff Time (10h × €20): €800/Monat

TOTAL: €2.000-3.100
MINUS €249: €1.751-2.851

→ BUSINESS ROI: €800-1.500/Monat
→ Break-Even: 2.2 Monate ✅
```
"""
        }
        
        return contexts.get(industry, contexts["hotel"])
    
    def _build_user_prompt(self, crawler_data: Dict[str, Any], industry: str, company_name: str) -> str:
        """Build user prompt with website analysis data"""
        
        # Extract key website information
        page_title = crawler_data.get("page_title", "Unbekannt")
        meta_description = crawler_data.get("meta_description", "Keine Beschreibung")
        has_chatbot = crawler_data.get("has_chatbot", False)
        chatbot_type = crawler_data.get("chatbot_type", "Unknown")
        mobile_friendly = crawler_data.get("mobile_friendly", True)
        page_count = crawler_data.get("page_count", 5)
        
        user_prompt = f"""
Analysiere die folgende Website und erstelle einen umfassenden Business-Analyse-Report:

## UNTERNEHMENSDATEN

**Name**: {company_name}
**Branche**: {industry}

## WEBSITE-ANALYSE DATEN

**Page Title**: {page_title}
**Meta Description**: {meta_description}

**Technische Features**:
- Has Chatbot: {"JA" if has_chatbot else "NEIN"}
- Chatbot Type: {chatbot_type if has_chatbot else "N/A"}
- Mobile Friendly: {"JA" if mobile_friendly else "NEIN"}
- Page Count: {page_count}

## VOLLSTÄNDIGE WEBSITE-DATEN

{json.dumps(crawler_data, indent=2, ensure_ascii=False)}

---

## AUFGABE

Erstelle eine professionelle Business-Analyse mit:

1. **QUALITY SCORE BERECHNUNG**: 
   - Durchsuche Website-Content nach Premium-Indikatoren
   - Berechne Score (0-200 Punkte)
   - Entscheide: PREMIUM (≥40), BUSINESS (<40), oder ENTERPRISE (≥80)

2. **CHATBOT-AWARE ANALYSE**:
   - Prüfe has_chatbot Status
   - Wenn TRUE: "Chatbot-Optimierung" empfehlen (Migration)
   - Wenn FALSE: "Chatbot-Implementierung" empfehlen (Neu)
   - Erwähne im Report: "✅ Chatbot erkannt" (wenn TRUE)

3. **PAKET-EMPFEHLUNG**:
   - Empfehle PREMIUM wenn:
     * Quality Score ≥40
     * Mehrsprachigkeit nötig
     * Michelin/Auszeichnungen
     * Preis >€120/Nacht
     * Events/Wellness
   - Sonst: BUSINESS

4. **ROI-BERECHNUNG**:
   - Verwende Premium- oder Business-Formeln
   - Konservative Annahmen (5-12% Uplift)
   - Break-Even: 1-12 Monate
   - Realistische Zahlen!

5. **3-7 PAIN POINTS** (basierend auf crawler_data)

6. **3-7 RECOMMENDATIONS** (passend zu Paket)

7. **KEY FINDINGS & NEXT STEPS**

8. **UPSELL NOTE** (z.B. "Business-Start möglich, Premium empfohlen")

**WICHTIG**:
- 100% DEUTSCH
- PREMIUM-FOKUS (wenn Quality Score passt)
- CHATBOT DETECTION beachten!
- EHRLICH bei zu kleinen Businesses
- KONSERVATIVE ROI-Zahlen

Erstelle jetzt die vollständige Analyse!
"""
        
        return user_prompt
    
    def _format_sources(self, sources: List[Dict[str, str]]) -> str:
        """Format sources for inclusion in prompt"""
        if not sources:
            return "Keine zusätzlichen Quellen verfügbar."
        
        sources_text = "## BRANCHENSPEZIFISCHE QUELLEN\n\n"
        for i, source in enumerate(sources, 1):
            sources_text += f"### [{i}] {source.get('title', 'Quelle')}\n"
            sources_text += f"**URL**: {source.get('url', 'N/A')}\n"
            sources_text += f"**Key Insight**: {source.get('key_insight', 'Keine Details verfügbar')}\n\n"
        
        return sources_text
    
    def analyze(
        self,
        crawler_data: Dict[str, Any],
        industry: str,
        company_name: str,
        sources: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Perform AI analysis on business website
        
        Args:
            crawler_data: Website crawl results
            industry: Business industry (hotel, restaurant, etc.)
            company_name: Name of the company
            sources: Optional list of industry research sources
            
        Returns:
            Dict containing structured analysis results
        """
        logger.info(f"Starting analysis for {company_name} ({industry})")
        
        # Format sources context
        sources_context = self._format_sources(sources or [])
        
        # Build prompts
        system_prompt = self._build_system_prompt(industry, sources_context)
        user_prompt = self._build_user_prompt(crawler_data, industry, company_name)
        
        logger.info("Calling OpenAI API with structured output...")
        
        try:
            # Call OpenAI with Structured Outputs
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=AnalysisResult,
                temperature=0.5  # Slightly creative but consistent
            )
            
            # Extract structured result
            analysis = completion.choices[0].message.parsed
            
            logger.info("Analysis completed successfully")
            
            # Convert to dict and add metadata
            result = analysis.model_dump()
            result["model"] = self.model
            result["industry"] = industry
            result["company_name"] = company_name
            result["analyzer_version"] = "3.0"
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example crawler data for testing
    test_crawler_data = {
        "page_title": "Hotel Engel Sasbachwalden - Michelin Restaurant & Boutique Hotel",
        "meta_description": "Genießen zwischen Himmel und Erde seit 1764. Michelin-Restaurant, 17 klimatisierte Zimmer, Weinkarte.",
        "has_chatbot": True,
        "chatbot_type": "Tawk.to",
        "mobile_friendly": True,
        "page_count": 12,
        "content": "Michelin Guide 2025, Gault Millau, 5 Pfannen, Degustationsmenü, Weinprobe, internationale Gäste, ab €150 pro Nacht"
    }
    
    test_sources = [
        {
            "title": "Vynta AI Hotel Study 2026",
            "url": "https://example.com/vynta",
            "key_insight": "Direct Bookings +20-30% durch AI-Chatbot"
        }
    ]
    
    # Initialize analyzer
    analyzer = AIAnalyzer()
    
    # Run analysis
    result = analyzer.analyze(
        crawler_data=test_crawler_data,
        industry="hotel",
        company_name="Hotel Engel Sasbachwalden",
        sources=test_sources
    )
    
    # Print results
    print("\n" + "="*80)
    print("ANALYSIS RESULTS")
    print("="*80)
    print(f"\nRecommended Package: {result['recommended_package']}")
    print(f"Quality Score: {result['quality_score']}")
    print(f"Monthly ROI: €{result['roi_calculation']['monthly_roi_euro']}")
    print(f"Break-Even: {result['roi_calculation']['break_even_months']} months")
    print("\nQuality Indicators:")
    for indicator in result['quality_indicators']:
        print(f"  - {indicator}")
