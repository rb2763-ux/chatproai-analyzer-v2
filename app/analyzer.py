"""
CHATPRO AI ANALYZER - AI-POWERED WEBSITE ANALYSIS
OpenAI GPT-4 Integration with Structured Outputs
"""

import os
import json
from typing import Dict, List, Optional
from openai import OpenAI
from .sources_database import get_sources_for_industry, format_sources_for_prompt

class AIAnalyzer:
    """AI-powered website analysis using OpenAI GPT-4"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-2024-08-06"  # Structured Outputs support
        
    def analyze(self, crawler_data: dict, industry: str, company_name: str = "") -> dict:
        """
        Analyze website data and calculate ROI using OpenAI GPT-4
        
        Args:
            crawler_data: Data from WebsiteCrawler
            industry: Business industry (hotel, restaurant, fitness, etc.)
            company_name: Name of the company
            
        Returns:
            dict: Analysis results with pain_points, roi_calculation, recommendations
        """
        
        # Get relevant sources for this industry
        sources = get_sources_for_industry(industry)
        sources_text = format_sources_for_prompt(sources)
        
        # Build system prompt
        system_prompt = self._build_system_prompt(industry, sources_text)
        
        # Build user prompt with crawler data
        user_prompt = self._build_user_prompt(crawler_data, company_name, industry)
        
        # Define JSON Schema for Structured Outputs
        response_schema = self._get_response_schema()
        
        try:
            # Call OpenAI API with Structured Outputs
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "website_analysis",
                        "strict": True,
                        "schema": response_schema
                    }
                },
                temperature=0.7,
                max_tokens=3000
            )
            
            # Parse response
            analysis = json.loads(response.choices[0].message.content)
            
            # Add metadata
            analysis["model"] = self.model
            analysis["industry"] = industry
            analysis["company_name"] = company_name
            
            return analysis
            
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            # Fallback to basic analysis if OpenAI fails
            return self._fallback_analysis(crawler_data, industry)
    
    def _build_system_prompt(self, industry: str, sources_text: str) -> str:
        """Build system prompt with industry context"""
        
        industry_contexts = {
            "hotel": "Hotels & Pensionen mit 50-200+ Anfragen/Tag",
            "restaurant": "Restaurants & Cafés mit hohem Reservierungsaufkommen",
            "fitness": "Fitnessstudios & Wellness mit Mitgliederbetreuung",
            "salon": "Friseursalons & Beauty mit Terminmanagement",
            "immobilien": "Immobilienmakler mit Lead-Qualifizierung",
            "ecommerce": "E-Commerce mit Customer Support",
            "anwalt": "Rechtsanwälte mit Mandantenanfragen",
            "steuerberater": "Steuerberater mit Beratungsanfragen",
            "versicherung": "Versicherungsagenturen mit Kundenservice",
            "arzt": "Arztpraxen mit Terminverwaltung"
        }
        
        context = industry_contexts.get(industry.lower(), "Dienstleistungsunternehmen")
        
        return f"""Du bist ein Senior Business Analyst für {context}.

AUFGABE:
Analysiere die Website-Daten und erstelle eine professionelle, quellenbasierte ROI-Analyse für einen KI-Chatbot (ChatPro AI).

KONTEXT - CHATPRO AI:
- Premium B2B SaaS AI-Chatbot
- 95%+ Automatisierung
- 24/7 Verfügbarkeit
- 50+ Sprachen
- PMS/CRM Integration
- DSGVO-konform

PRICING:
- Business: €1.799 Setup + €249/Monat
- Premium: €4.999 Setup + €799/Monat (empfohlen für Hotels!)
- Enterprise: €10.000+ (große Ketten)

SOURCES (verwende diese für ROI-Berechnungen):
{sources_text}

WICHTIG:
1. Alle Zahlen MÜSSEN mit source_ids referenziert werden
2. Sei KONSERVATIV in Schätzungen (Glaubwürdigkeit > Begeisterung)
3. Pain Points müssen KONKRET zur Website passen (nutze crawler_data!)
4. Empfehlungen müssen UMSETZBAR sein
5. ROI-Berechnung muss TRANSPARENT sein (Formel + Quellen)

CHATBOT PRIORITY LOGIC:
- HIGH: Kein Chatbot + ROI > €5.000/Monat + Hotel/Restaurant/Fitness
- MEDIUM: Legacy Chatbot (Zendesk/Tidio) ODER ROI €2.000-€5.000/Monat
- LOW: Moderner Chatbot ODER ROI < €2.000/Monat

OUTPUT: JSON gemäß Schema (siehe response_format)
"""
    
    def _build_user_prompt(self, crawler_data: dict, company_name: str, industry: str) -> str:
        """Build user prompt with website data"""
        
        chatbot_status = "Kein Chatbot erkannt"
        if crawler_data.get("has_chatbot"):
            chatbot_type = crawler_data.get("chatbot_type", "Unknown")
            chatbot_status = f"Chatbot erkannt: {chatbot_type}"
        
        return f"""WEBSITE-ANALYSE FÜR: {company_name or 'Unbekannt'}
Branche: {industry}

CRAWLER-DATEN:
- Website: {crawler_data.get('url', 'N/A')}
- Seiten: {crawler_data.get('page_count', 0)}
- Sprachen: {', '.join(crawler_data.get('languages', ['Deutsch']))}
- Mobile: {'✓ Optimiert' if crawler_data.get('is_mobile_friendly') else '✗ Nicht optimiert'}
- Chatbot: {chatbot_status}
- Lead-Formulare: {len(crawler_data.get('lead_forms', []))}
- Kontakt gefunden: {'Ja' if crawler_data.get('has_contact_info') else 'Nein'}

AUFGABE:
Erstelle eine detaillierte, quellenbasierte ROI-Analyse für ChatPro AI Chatbot.

Analysiere:
1. Pain Points (basierend auf den konkreten Website-Daten)
2. ROI-Berechnung (mit Quellen-IDs!)
3. Individuelle Empfehlungen (3-5 Stück, priorisiert)
4. Chatbot Priority (HIGH/MEDIUM/LOW)

Sei präzise, konservativ und transparent!
"""
    
    def _get_response_schema(self) -> dict:
        """Get JSON Schema for Structured Outputs"""
        return {
            "type": "object",
            "properties": {
                "pain_points": {
                    "type": "array",
                    "description": "Konkrete Pain Points basierend auf Website-Analyse",
                    "items": {
                        "type": "object",
                        "properties": {
                            "problem": {
                                "type": "string",
                                "description": "Beschreibung des Problems"
                            },
                            "impact": {
                                "type": "string",
                                "description": "Auswirkung auf das Business"
                            },
                            "evidence": {
                                "type": "string",
                                "description": "Beweis aus Crawler-Daten"
                            },
                            "source_ids": {
                                "type": "array",
                                "description": "IDs der verwendeten Quellen",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["problem", "impact", "evidence", "source_ids"],
                        "additionalProperties": False
                    }
                },
                "roi_calculation": {
                    "type": "object",
                    "description": "ROI-Berechnung mit Quellen",
                    "properties": {
                        "monthly_roi": {
                            "type": "number",
                            "description": "Monatliches ROI-Potenzial in Euro"
                        },
                        "roi_multiplier": {
                            "type": "number",
                            "description": "ROI-Multiplikator (z.B. 16.5 = 16,5x Return)"
                        },
                        "break_even_months": {
                            "type": "number",
                            "description": "Break-Even in Monaten"
                        },
                        "calculations": {
                            "type": "array",
                            "description": "Einzelne Berechnungen",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "category": {
                                        "type": "string",
                                        "description": "Kategorie (z.B. 'Zeitersparnis', 'Direktbuchungen')"
                                    },
                                    "monthly_value": {
                                        "type": "number",
                                        "description": "Monatlicher Wert in Euro"
                                    },
                                    "calculation": {
                                        "type": "string",
                                        "description": "Formel/Erklärung der Berechnung"
                                    },
                                    "source_ids": {
                                        "type": "array",
                                        "description": "IDs der verwendeten Quellen",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["category", "monthly_value", "calculation", "source_ids"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["monthly_roi", "roi_multiplier", "break_even_months", "calculations"],
                    "additionalProperties": False
                },
                "recommendations": {
                    "type": "array",
                    "description": "Individuelle Empfehlungen (3-5 Stück)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "priority": {
                                "type": "string",
                                "enum": ["HIGH", "MEDIUM", "LOW"],
                                "description": "Priorität der Empfehlung"
                            },
                            "title": {
                                "type": "string",
                                "description": "Titel der Empfehlung"
                            },
                            "description": {
                                "type": "string",
                                "description": "Detaillierte Beschreibung"
                            },
                            "impact": {
                                "type": "string",
                                "description": "Erwarteter Impact"
                            },
                            "implementation": {
                                "type": "string",
                                "description": "Wie umsetzen"
                            }
                        },
                        "required": ["priority", "title", "description", "impact", "implementation"],
                        "additionalProperties": False
                    }
                },
                "chatbot_priority": {
                    "type": "string",
                    "enum": ["HIGH", "MEDIUM", "LOW"],
                    "description": "Lead-Priorität für Sales-Team"
                }
            },
            "required": ["pain_points", "roi_calculation", "recommendations", "chatbot_priority"],
            "additionalProperties": False
        }
    
    def _fallback_analysis(self, crawler_data: dict, industry: str) -> dict:
        """Fallback analysis if OpenAI fails"""
        return {
            "pain_points": [
                {
                    "problem": "Manuelle Anfragenbearbeitung zeitintensiv",
                    "impact": "Hoher Zeitaufwand für repetitive Aufgaben",
                    "evidence": f"Website hat {crawler_data.get('page_count', 0)} Seiten",
                    "source_ids": ["1", "3"]
                }
            ],
            "roi_calculation": {
                "monthly_roi": 3000,
                "roi_multiplier": 3.8,
                "break_even_months": 1.6,
                "calculations": [
                    {
                        "category": "Zeitersparnis",
                        "monthly_value": 1200,
                        "calculation": "20h/Woche × €15/h × 4 Wochen",
                        "source_ids": ["1"]
                    },
                    {
                        "category": "Lead-Steigerung",
                        "monthly_value": 1800,
                        "calculation": "Geschätzt basierend auf Branchendurchschnitt",
                        "source_ids": ["3"]
                    }
                ]
            },
            "recommendations": [
                {
                    "priority": "HIGH",
                    "title": "KI-Chatbot implementieren",
                    "description": "24/7 Automatisierung der Standardanfragen",
                    "impact": "Zeitersparnis + mehr qualifizierte Leads",
                    "implementation": "ChatPro AI Premium-Paket empfohlen"
                }
            ],
            "chatbot_priority": "MEDIUM",
            "model": "fallback",
            "industry": industry
        }
