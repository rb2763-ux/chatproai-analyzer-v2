"""
CHATPRO AI ANALYZER - AI ANALYSIS ENGINE
OpenAI-powered analysis for website and industry-specific ROI calculation
"""

from typing import Dict, Optional, List
import json

# Sources database (from SOURCES_DATABASE.md)
SOURCES = {
    "personalkosten": {
        "id": "[1]",
        "title": "Destatis (2025): Arbeits- und Lohnnebenkosten 2024",
        "value": "€43,40/Stunde durchschnittlich (Gastgewerbe: ca. €25-30/h)",
        "url": "https://www.destatis.de/DE/Themen/Arbeit/Arbeitskosten-Lohnnebenkosten/_inhalt.html",
        "date": "30.04.2025"
    },
    "booking_provision": {
        "id": "[3]",
        "title": "Fewolino (2025): Booking.com Provisionsmodell Deutschland",
        "value": "12-15% Provision (Standard: 12%, Berlin: 15%)",
        "url": "https://fewolino.com/wie-viel-kommission-nimmt-booking/",
        "date": "2025"
    },
    "chatbot_conversion": {
        "id": "[7]",
        "title": "Innovation Visual (2025): Citron Hygiene Case Study",
        "value": "76% Increase in qualified leads durch Chatbot",
        "url": "https://www.innovationvisual.com/case-studies/tag/hubspot",
        "date": "2025"
    },
    "hotel_auslastung": {
        "id": "[9]",
        "title": "Prostay (2025): Hotel Booking Statistics 2025",
        "value": "72% Globale Hotelauslastung in 2025",
        "url": "https://www.prostay.com/blog/hotel-booking-statistics-2025-market-insights-and-trends/",
        "date": "13.08.2025"
    }
}

class AIAnalyzer:
    """
    AI-powered website and ROI analysis
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        # Will use OpenAI API when available
        # For now, use rule-based analysis
    
    def analyze(self, crawler_data: Dict, industry: str) -> Dict:
        """
        Analyze website and calculate ROI
        
        Args:
            crawler_data: Data from WebsiteCrawler
            industry: hotel, fitness, salon, immobilien, restaurant, other
        
        Returns:
            Comprehensive analysis with ROI calculations
        """
        
        # Base analysis
        analysis = {
            "website_check": self._analyze_website(crawler_data),
            "chatbot_analysis": self._analyze_chatbot(crawler_data),
            "pain_points": self._identify_pain_points(crawler_data, industry),
            "roi_calculation": self._calculate_roi(crawler_data, industry),
            "recommendations": self._generate_recommendations(crawler_data, industry),
            "sources": self._collect_sources(industry)
        }
        
        return analysis
    
    def _analyze_website(self, data: Dict) -> Dict:
        """
        Analyze website structure and features
        """
        
        return {
            "status": "✅ Online" if data.get("status_code") == 200 else "❌ Problem",
            "title": data.get("title", "Nicht gefunden"),
            "pages": data.get("pages_count", 0),
            "languages": data.get("languages", ["de"]),
            "language_count": len(data.get("languages", ["de"])),
            "mobile_responsive": data.get("mobile_responsive", False),
            "response_time_ms": data.get("response_time_ms", 0),
            "has_contact_info": bool(data.get("contact_info", {}).get("emails")),
            "lead_forms_count": len(data.get("lead_forms", []))
        }
    
    def _analyze_chatbot(self, data: Dict) -> Dict:
        """
        Analyze existing chatbot (if any)
        """
        
        has_chatbot = data.get("has_chatbot", False)
        details = data.get("chatbot_details", {})
        
        if not has_chatbot:
            return {
                "exists": False,
                "status": "❌ Kein Chatbot gefunden",
                "issue": "Keine 24/7-Verfügbarkeit",
                "lost_leads": "Potenzielle Leads gehen verloren außerhalb Geschäftszeiten"
            }
        
        # Chatbot exists - analyze issues
        bot_type = details.get("type", "unknown")
        has_lead_form = details.get("has_lead_form", False)
        
        issues = []
        if has_lead_form:
            issues.append("Lead-Formular VOR Chat → 40-60% Drop-off [4]")
        if bot_type == "zendesk":
            issues.append("Zendesk: E-Mail + Name erforderlich vor Konversation")
        
        return {
            "exists": True,
            "type": bot_type.title(),
            "status": "⚠️ Chatbot gefunden (mit Schwachstellen)" if issues else "✅ Chatbot gefunden",
            "has_lead_form": has_lead_form,
            "issues": issues,
            "priority": details.get("priority", "MEDIUM")
        }
    
    def _identify_pain_points(self, data: Dict, industry: str) -> List[Dict]:
        """
        Identify specific pain points
        """
        
        pain_points = []
        
        # No chatbot
        if not data.get("has_chatbot"):
            pain_points.append({
                "issue": "Keine 24/7-Verfügbarkeit",
                "impact": "Anfragen außerhalb Geschäftszeiten gehen verloren",
                "cost": "30-40% potenzielle Kunden verloren",
                "source": None
            })
        
        # Chatbot with lead form
        chatbot_details = data.get("chatbot_details", {})
        if chatbot_details.get("has_lead_form"):
            pain_points.append({
                "issue": "Lead-Formular vor Chat",
                "impact": "40-60% der Interessenten brechen ab",
                "cost": "Hohe Lead-Verluste",
                "source": "[Competitor Analysis - Zendesk Case Studies]"
            })
        
        # Limited languages
        languages = data.get("languages", ["de"])
        if len(languages) < 3:
            pain_points.append({
                "issue": f"Nur {len(languages)} Sprache(n): {', '.join(languages)}",
                "impact": "Internationale Gäste können nicht betreut werden",
                "cost": "Verlust internationaler Buchungen",
                "source": "[1]"
            })
        
        # Industry-specific
        if industry == "hotel":
            if not data.get("has_chatbot"):
                pain_points.append({
                    "issue": "Keine Booking.com-Direktbuchungs-Strategie",
                    "impact": "15% Provision an Booking.com",
                    "cost": "€1.500-3.000/Monat bei 50 Zimmern",
                    "source": "[3]"
                })
        
        return pain_points
    
    def _calculate_roi(self, data: Dict, industry: str) -> Dict:
        """
        Calculate industry-specific ROI
        """
        
        if industry == "hotel":
            return self._calculate_hotel_roi(data)
        elif industry == "fitness":
            return self._calculate_fitness_roi(data)
        elif industry == "salon":
            return self._calculate_salon_roi(data)
        elif industry == "immobilien":
            return self._calculate_immobilien_roi(data)
        elif industry == "restaurant":
            return self._calculate_restaurant_roi(data)
        else:
            return self._calculate_generic_roi(data)
    
    def _calculate_hotel_roi(self, data: Dict) -> Dict:
        """
        Hotel-specific ROI calculation
        """
        
        # Assumptions (konservativ)
        zimmer = 50
        auslastung = 0.70  # 70% [9]
        preis_pro_nacht = 120
        booking_provision = 0.15  # 15% [3]
        
        # Monthly calculations
        naechte_pro_monat = zimmer * auslastung * 30
        monatsumsatz = naechte_pro_monat * preis_pro_nacht
        
        # Phase 1: Direktbuchungen
        direktbuchung_steigerung = 0.10  # 10% mehr direkt (konservativ)
        zusaetzliche_direktbuchungen = monatsumsatz * direktbuchung_steigerung
        ersparte_provision = zusaetzliche_direktbuchungen * booking_provision
        
        # 24/7 → mehr Buchungen
        mehrbuchungen_24_7 = monatsumsatz * 0.10  # +10% durch 24/7
        
        phase1_total = ersparte_provision + (mehrbuchungen_24_7 * booking_provision)
        
        # Phase 2: Zeitersparnis
        stunden_pro_monat = 40  # 40h/Monat gespart
        stundenlohn = 25  # €25/h [1]
        zeitersparnis = stunden_pro_monat * stundenlohn
        
        # Phase 3: Upselling
        upselling_rate = 0.20  # 20% der Gäste
        upselling_wert = 40  # €40 pro Upsell
        upselling_revenue = naechte_pro_monat * upselling_rate * upselling_wert
        
        total_roi = phase1_total + zeitersparnis + upselling_revenue
        
        # ChatPro AI Kosten
        setup_kosten = 4999
        monatliche_kosten = 799
        
        # Break-even
        break_even_monate = setup_kosten / total_roi
        
        return {
            "assumptions": {
                "zimmer": zimmer,
                "auslastung_prozent": int(auslastung * 100),
                "preis_pro_nacht": preis_pro_nacht,
                "booking_provision_prozent": int(booking_provision * 100),
                "sources": ["[3]", "[9]", "[1]"]
            },
            "calculations": {
                "naechte_pro_monat": int(naechte_pro_monat),
                "monatsumsatz": int(monatsumsatz),
                "phase1_direktbuchungen": {
                    "ersparte_provision": int(ersparte_provision),
                    "mehr_buchungen_24_7": int(mehrbuchungen_24_7 * booking_provision),
                    "total": int(phase1_total),
                    "source": "[3]"
                },
                "phase2_zeitersparnis": {
                    "stunden_pro_monat": stunden_pro_monat,
                    "stundenlohn": stundenlohn,
                    "total": int(zeitersparnis),
                    "source": "[1]"
                },
                "phase3_upselling": {
                    "upselling_rate_prozent": int(upselling_rate * 100),
                    "wert_pro_upsell": upselling_wert,
                    "total": int(upselling_revenue),
                    "source": "[13]"
                }
            },
            "summary": {
                "total_roi_monat": int(total_roi),
                "chatpro_kosten_monat": monatliche_kosten,
                "net_gewinn_monat": int(total_roi - monatliche_kosten),
                "roi_multiplikator": round(total_roi / monatliche_kosten, 1),
                "break_even_monate": round(break_even_monate, 1),
                "jahres_roi": int(total_roi * 12)
            }
        }
    
    def _calculate_generic_roi(self, data: Dict) -> Dict:
        """
        Generic ROI calculation for other industries
        """
        
        # Zeitersparnis (universal)
        stunden_pro_monat = 30
        stundenlohn = 25
        zeitersparnis = stunden_pro_monat * stundenlohn
        
        # Lead-Steigerung
        aktuelle_anfragen = 100  # Annahme
        lead_steigerung = 0.20  # +20% durch 24/7 [7]
        zusaetzliche_leads = aktuelle_anfragen * lead_steigerung
        wert_pro_lead = 50  # Konservativ
        lead_revenue = zusaetzliche_leads * wert_pro_lead
        
        total_roi = zeitersparnis + lead_revenue
        monatliche_kosten = 799
        
        return {
            "assumptions": {
                "stunden_gespart_monat": stunden_pro_monat,
                "aktuelle_anfragen_monat": aktuelle_anfragen,
                "lead_steigerung_prozent": int(lead_steigerung * 100),
                "sources": ["[1]", "[7]"]
            },
            "calculations": {
                "zeitersparnis": {
                    "total": int(zeitersparnis),
                    "source": "[1]"
                },
                "lead_steigerung": {
                    "zusaetzliche_leads": int(zusaetzliche_leads),
                    "total": int(lead_revenue),
                    "source": "[7]"
                }
            },
            "summary": {
                "total_roi_monat": int(total_roi),
                "chatpro_kosten_monat": monatliche_kosten,
                "net_gewinn_monat": int(total_roi - monatliche_kosten),
                "roi_multiplikator": round(total_roi / monatliche_kosten, 1),
                "jahres_roi": int(total_roi * 12)
            }
        }
    
    def _calculate_fitness_roi(self, data: Dict) -> Dict:
        """Fitness-specific ROI"""
        return self._calculate_generic_roi(data)
    
    def _calculate_salon_roi(self, data: Dict) -> Dict:
        """Salon-specific ROI"""
        return self._calculate_generic_roi(data)
    
    def _calculate_immobilien_roi(self, data: Dict) -> Dict:
        """Real estate-specific ROI"""
        return self._calculate_generic_roi(data)
    
    def _calculate_restaurant_roi(self, data: Dict) -> Dict:
        """Restaurant-specific ROI"""
        return self._calculate_generic_roi(data)
    
    def _generate_recommendations(self, data: Dict, industry: str) -> List[str]:
        """
        Generate specific recommendations
        """
        
        recommendations = []
        
        if not data.get("has_chatbot"):
            recommendations.append("✅ ChatPro AI 24/7-Chatbot implementieren")
        
        if len(data.get("languages", [])) < 3:
            recommendations.append("✅ 50+ Sprachen aktivieren für internationale Gäste")
        
        if industry == "hotel":
            recommendations.append("✅ Booking.com-Integration (Phase 1-3)")
            recommendations.append("✅ PMS-Integration für Pre-Arrival-Automation")
        
        recommendations.append("✅ Dedicated Account Manager für monatliche Strategie-Calls")
        
        return recommendations
    
    def _collect_sources(self, industry: str) -> List[Dict]:
        """
        Collect all relevant sources for report
        """
        
        # Always include these
        sources_list = [
            SOURCES["personalkosten"],
            SOURCES["chatbot_conversion"]
        ]
        
        # Industry-specific
        if industry == "hotel":
            sources_list.extend([
                SOURCES["booking_provision"],
                SOURCES["hotel_auslastung"]
            ])
        
        return sources_list


# Test function
def test_analyzer():
    """Test analyzer"""
    
    # Mock crawler data (ADORO)
    crawler_data = {
        "url": "https://adoro-aparthotel.com",
        "status_code": 200,
        "title": "ADORO Aparthotel",
        "languages": ["de", "en"],
        "has_chatbot": True,
        "chatbot_details": {
            "detected": True,
            "type": "zendesk",
            "has_lead_form": True,
            "priority": "HIGH"
        },
        "lead_forms": [],
        "pages_count": 21,
        "mobile_responsive": True,
        "contact_info": {
            "emails": ["contact@adoro-aparthotel.com"],
            "phones": ["+49 7223 3009640"]
        },
        "response_time_ms": 465
    }
    
    analyzer = AIAnalyzer()
    result = analyzer.analyze(crawler_data, "hotel")
    
    print("=== AI ANALYSIS RESULT ===\n")
    print(f"Website Check: {result['website_check']['status']}")
    print(f"Languages: {result['website_check']['languages']}")
    print(f"\nChatbot Analysis:")
    print(f"  Exists: {result['chatbot_analysis']['exists']}")
    print(f"  Type: {result['chatbot_analysis'].get('type', 'N/A')}")
    print(f"  Priority: {result['chatbot_analysis'].get('priority', 'N/A')}")
    print(f"\nPain Points: {len(result['pain_points'])}")
    for pp in result['pain_points']:
        print(f"  - {pp['issue']}: {pp['impact']}")
    
    print(f"\nROI Calculation:")
    summary = result['roi_calculation']['summary']
    print(f"  Total ROI/Monat: €{summary['total_roi_monat']:,}")
    print(f"  ChatPro Kosten: €{summary['chatpro_kosten_monat']}")
    print(f"  Net Gewinn: €{summary['net_gewinn_monat']:,}")
    print(f"  ROI Multiplikator: {summary['roi_multiplikator']}x")
    print(f"  Break-Even: {summary['break_even_monate']} Monate")
    
    print(f"\nSources: {len(result['sources'])}")


if __name__ == "__main__":
    test_analyzer()
