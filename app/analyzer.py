"""
CHATPRO AI ANALYZER - AI-POWERED WEBSITE ANALYSIS
OpenAI GPT-4 Integration with Structured Outputs
OPTIMIZED FOR SERIOUS B2B CONSULTING TONE
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
                # WICHTIG: Temperature gesenkt für seriösere, deterministische Antworten
                temperature=0.4, 
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
            return self._fallback_analysis(crawler_data, industry)
    
    def _build_system_prompt(self, industry: str, sources_text: str) -> str:
        """Build system prompt with strict consulting persona"""
        
        industry_contexts = {
            "hotel": "Hotellerie (Fokus: Direktbuchungsquote, Rezeptionsentlastung)",
            "restaurant": "Gastronomie (Fokus: No-Show-Rate, Reservierungsmanagement)",
            "fitness": "Fitness & Health (Fokus: Lead-Qualifizierung, Mitgliederbindung)",
            "salon": "Beauty & Wellness (Fokus: Terminauslastung, Ausfallreduktion)",
            "immobilien": "Real Estate (Fokus: Vorqualifizierung, Reaktionszeit)",
            "ecommerce": "E-Commerce (Fokus: Warenkorbabbruch, Support-Automatisierung)",
            "anwalt": "Rechtsberatung (Fokus: Mandantenaufnahme, Ersteinschätzung)",
            "steuerberater": "Steuerberatung (Fokus: Fristenmanagement, Dokumentenerfassung)",
            "versicherung": "Versicherungswesen (Fokus: Schadensmeldung, Tarifberatung)",
            "arzt": "Gesundheitswesen (Fokus: Anamnese, Terminmanagement)"
        }
        
        context = industry_contexts.get(industry.lower(), "Dienstleistungssektor")
        
        return f"""Du bist ein Senior Strategy Consultant für Digitale Transformation im Bereich {context}.

DEINE ROLLE:
Du analysierst Unternehmen nüchtern, faktenbasiert und kritisch. Dein Ziel ist es, ineffiziente Prozesse aufzudecken und finanzielle Verluste durch fehlende Automatisierung zu quantifizieren.

TONE OF VOICE (STRENG EINHALTEN):
- Professionell, distanziert, "C-Level ready".
- KEINE Marketing-Floskeln (vermeide: "toll", "super", "revolutionär", "Gamechanger").
- Nutze präzise Business-Terminologie (z.B. "Opportunitätskosten", "Konversionsrate", "Ressourcenbindung").
- Formuliere Probleme als finanzielle Risiken.
- Sei direkt: "Die fehlende Automatisierung führt zu X", nicht "Es wäre schön, wenn...".

PRODUKT-KONTEXT (CHATPRO AI):
Wir bieten eine Enterprise-Grade KI-Lösung zur Prozessautomatisierung.
- Funktionalität: 24/7 Lead-Erfassung, PMS/CRM-Integration, Mehrsprachigkeit.
- Pricing (nur für ROI-Referenz): Setup ab €1.799, Monthly ab €249.

QUELLEN FÜR BENCHMARKS:
{sources_text}

ANALYSE-RICHTLINIEN:
1. **Pain Points:** Identifiziere operative Engpässe basierend auf den Crawler-Daten (z.B. viele Unterseiten = hoher Info-Bedarf = hohe Support-Last).
2. **ROI-Berechnung:** Sei KONSERVATIV. Berechne lieber das "Worst-Case"-Szenario, das ist glaubwürdiger. Referenziere IMMER die Source-IDs.
3. **Empfehlungen:** Keine generischen Tipps. Empfiehl konkrete Prozess-Änderungen.

OUTPUT FORMAT:
JSON gemäß Schema.
"""
    
    def _build_user_prompt(self, crawler_data: dict, company_name: str, industry: str) -> str:
        """Build user prompt with structured data presentation"""
        
        chatbot_status = "Nicht vorhanden"
        if crawler_data.get("has_chatbot"):
            chatbot_type = crawler_data.get("chatbot_type", "Unbekannt")
            chatbot_status = f"Vorhanden (System: {chatbot_type})"
        
        # Berechne implizite Metriken für die KI
        complexity_score = "Hoch" if crawler_data.get('page_count', 0) > 20 else "Mittel"
        intl_score = "Ja" if len(crawler_data.get('languages', [])) > 1 else "Nein"
        
        return f"""ANALYSE-OBJEKT:
Unternehmen: {company_name or 'Unbekannt'}
Branche: {industry}

TECHNISCHE IST-AUFNAHME (CRAWLER DATEN):
1. Web-Präsenz:
   - URL: {crawler_data.get('url', 'N/A')}
   - Struktur-Komplexität: {crawler_data.get('page_count', 0)} indexierte Seiten ({complexity_score})
   - Internationalisierung: {intl_score} ({', '.join(crawler_data.get('languages', ['Deutsch']))})
   - Mobile Optimierung: {'Ja' if crawler_data.get('is_mobile_friendly') else 'Nein (Kritisch)'}

2. Interaktions-Kanäle:
   - Bestehende Automatisierung: {chatbot_status}
   - Statische Lead-Formulare: {len(crawler_data.get('lead_forms', []))} Stück
   - Kontakt-Optionen: {'Vorhanden' if crawler_data.get('has_contact_info') else 'Eingeschränkt'}

AUFGABE:
Erstelle eine Due-Diligence-Analyse der digitalen Kundeninteraktion.
Fokussiere dich auf entgangene Umsätze durch fehlende 24/7-Verfügbarkeit und manuelle Prozesskosten.
"""
    
    def _get_response_schema(self) -> dict:
        """Get JSON Schema with professional descriptions"""
        return {
            "type": "object",
            "properties": {
                "pain_points": {
                    "type": "array",
                    "description": "Identifizierte operative Ineffizienzen",
                    "items": {
                        "type": "object",
                        "properties": {
                            "problem": {
                                "type": "string",
                                "description": "Präzise Problembeschreibung (z.B. 'Hohe Ressourcenbindung durch manuelle Qualifizierung')"
                            },
                            "impact": {
                                "type": "string",
                                "description": "Wirtschaftliche Auswirkung (z.B. 'Verlust von 15% der Leads außerhalb der Geschäftszeiten')"
                            },
                            "evidence": {
                                "type": "string",
                                "description": "Ableitung aus den technischen Daten"
                            },
                            "source_ids": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["problem", "impact", "evidence", "source_ids"],
                        "additionalProperties": False
                    }
                },
                "roi_calculation": {
                    "type": "object",
                    "description": "Wirtschaftlichkeitsberechnung",
                    "properties": {
                        "monthly_roi": {
                            "type": "number",
                            "description": "Konservatives monatliches Einsparpotenzial in EUR"
                        },
                        "roi_multiplier": {
                            "type": "number",
                            "description": "ROI-Faktor (z.B. 4.5)"
                        },
                        "break_even_months": {
                            "type": "number",
                            "description": "Amortisationsdauer in Monaten"
                        },
                        "calculations": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "category": {
                                        "type": "string",
                                        "description": "Kostenstelle (z.B. 'Personalkosten Rezeption', 'Lead-Akquise')"
                                    },
                                    "monthly_value": {
                                        "type": "number",
                                        "description": "Wert in EUR"
                                    },
                                    "calculation": {
                                        "type": "string",
                                        "description": "Transparente Herleitung der Zahl"
                                    },
                                    "source_ids": {
                                        "type": "array",
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
                    "description": "Strategische Handlungsempfehlungen",
                    "items": {
                        "type": "object",
                        "properties": {
                            "priority": {
                                "type": "string",
                                "enum": ["HIGH", "MEDIUM", "LOW"]
                            },
                            "title": {
                                "type": "string",
                                "description": "Handlungsfeld"
                            },
                            "description": {
                                "type": "string",
                                "description": "Maßnahme und Begründung"
                            },
                            "impact": {
                                "type": "string",
                                "description": "Erwarteter betriebswirtschaftlicher Effekt"
                            },
                            "implementation": {
                                "type": "string",
                                "description": "Implementierungsschritt"
                            }
                        },
                        "required": ["priority", "title", "description", "impact", "implementation"],
                        "additionalProperties": False
                    }
                },
                "chatbot_priority": {
                    "type": "string",
                    "enum": ["HIGH", "MEDIUM", "LOW"],
                    "description": "Vertriebspriorität basierend auf Potenzial"
                }
            },
            "required": ["pain_points", "roi_calculation", "recommendations", "chatbot_priority"],
            "additionalProperties": False
        }
    
    def _fallback_analysis(self, crawler_data: dict, industry: str) -> dict:
        """Fallback analysis with professional tone"""
        return {
            "pain_points": [
                {
                    "problem": "Ressourcenbindung durch manuelle Anfragenbearbeitung",
                    "impact": "Erhöhte Personalkosten und verlängerte Reaktionszeiten",
                    "evidence": f"Hohes Informationsvolumen ({crawler_data.get('page_count', 0)} Seiten) ohne Automatisierung",
                    "source_ids": ["1", "3"]
                }
            ],
            "roi_calculation": {
                "monthly_roi": 2800,
                "roi_multiplier": 3.5,
                "break_even_months": 1.8,
                "calculations": [
                    {
                        "category": "Reduktion Personalkosten (First-Level-Support)",
                        "monthly_value": 1200,
                        "calculation": "Substitution von 20h/Monat manueller Bearbeitung à €60 (Vollkosten)",
                        "source_ids": ["1"]
                    },
                    {
                        "category": "Umsatzsteigerung durch 24/7 Verfügbarkeit",
                        "monthly_value": 1600,
                        "calculation": "Konversion von 2 zusätzlichen Buchungen/Woche à €200",
                        "source_ids": ["3"]
                    }
                ]
            },
            "recommendations": [
                {
                    "priority": "HIGH",
                    "title": "Automatisierung der Standardkommunikation",
                    "description": "Implementierung einer KI-Lösung zur Entlastung des Personals von repetitiven Anfragen.",
                    "impact": "Sofortige Reduktion der Ticket-Last um ca. 60-80%",
                    "implementation": "Integration ChatPro AI (Premium)"
                }
            ],
            "chatbot_priority": "MEDIUM",
            "model": "fallback",
            "industry": industry
        }
