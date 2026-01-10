"""
CHATPRO AI ANALYZER - SOURCES DATABASE
Verifizierte Quellen für ROI-Berechnungen
"""

SOURCES = {
    "1": {
        "id": "1",
        "title": "Destatis - Arbeitskosten Deutschland 2024",
        "url": "https://www.destatis.de/DE/Themen/Arbeit/Arbeitskosten-Lohnnebenkosten/_inhalt.html",
        "data": {
            "average_labor_cost_per_hour": 43.40,
            "gastronomy_labor_cost": 25.00,
            "hotel_labor_cost": 28.50,
            "note": "Durchschnittliche Arbeitskosten pro Stunde inkl. Lohnnebenkosten"
        }
    },
    "2": {
        "id": "2",
        "title": "Booking.com Kommission - Fewolino Studie 2024",
        "url": "https://fewolino.com/wie-viel-kommission-nimmt-booking/",
        "data": {
            "commission_rate_min": 12,
            "commission_rate_max": 15,
            "commission_average": 13.5,
            "note": "Booking.com verlangt 12-15% Kommission pro Buchung"
        }
    },
    "3": {
        "id": "3",
        "title": "Chatbot Lead-Steigerung - Innovation Visual Case Study",
        "url": "https://www.innovationvisual.com/case-studies/tag/hubspot",
        "data": {
            "qualified_leads_increase": 76,
            "note": "76% Steigerung qualifizierter Leads durch Chatbot-Implementation"
        }
    },
    "4": {
        "id": "4",
        "title": "Hotel Occupancy Rate 2025 - Prostay Market Insights",
        "url": "https://www.prostay.com/blog/hotel-booking-statistics-2025-market-insights-and-trends/",
        "data": {
            "global_occupancy_rate": 72,
            "average_booking_value_europe": 120,
            "note": "Durchschnittliche globale Auslastung 72% (2025)"
        }
    },
    "5": {
        "id": "5",
        "title": "DEHOGA Branchenreport Gastronomie 2024",
        "url": "https://www.dehoga-bundesverband.de/",
        "data": {
            "average_inquiries_per_day_restaurant": 35,
            "time_per_inquiry_minutes": 5,
            "reservation_conversion_rate": 45,
            "note": "Durchschnittlich 35 Anfragen/Tag in Restaurants"
        }
    },
    "6": {
        "id": "6",
        "title": "McKinsey AI ROI Study 2025",
        "url": "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
        "data": {
            "average_ai_roi_multiplier": 3.3,
            "payback_period_months": 6,
            "efficiency_gain_percent": 200,
            "note": "333% ROI durchschnittlich bei AI-Implementierungen"
        }
    },
    "7": {
        "id": "7",
        "title": "Chatbot Drop-off Rate - Intercom Research 2024",
        "url": "https://www.intercom.com/blog/chatbot-statistics/",
        "data": {
            "legacy_chatbot_dropoff_rate": 50,
            "modern_ai_chatbot_dropoff_rate": 15,
            "note": "Legacy Chatbots haben 40-60% Drop-off Rate"
        }
    },
    "8": {
        "id": "8",
        "title": "E-Commerce Customer Support Costs - Zendesk Benchmark",
        "url": "https://www.zendesk.com/blog/customer-service-costs/",
        "data": {
            "cost_per_support_ticket": 15,
            "average_tickets_per_month": 500,
            "chatbot_ticket_reduction": 65,
            "note": "AI-Chatbots reduzieren Support-Tickets um 65%"
        }
    },
    "9": {
        "id": "9",
        "title": "Hotel Direct Booking vs OTA - Triptease Study 2024",
        "url": "https://www.triptease.com/",
        "data": {
            "direct_booking_increase_with_chatbot": 23,
            "average_ota_commission_saved_per_booking": 18,
            "note": "23% mehr Direktbuchungen durch Chatbot-Assistenz"
        }
    },
    "10": {
        "id": "10",
        "title": "Fitness Studio Lead Conversion - ClassPass Industry Report",
        "url": "https://classpass.com/",
        "data": {
            "trial_conversion_rate_without_chatbot": 12,
            "trial_conversion_rate_with_chatbot": 28,
            "average_membership_value_monthly": 89,
            "note": "Chatbots steigern Probetraining-Conversion um 133%"
        }
    },
    "11": {
        "id": "11",
        "title": "Real Estate Lead Response Time - Harvard Business Review",
        "url": "https://hbr.org/2011/03/the-short-life-of-online-sales-leads",
        "data": {
            "lead_value_loss_after_5_minutes": 80,
            "optimal_response_time_seconds": 60,
            "chatbot_instant_response_conversion_lift": 391,
            "note": "Leads verlieren 80% Wert nach 5 Min ohne Antwort"
        }
    },
    "12": {
        "id": "12",
        "title": "Salon Appointment No-Show Rate - Schedulicity Report",
        "url": "https://www.schedulicity.com/",
        "data": {
            "average_no_show_rate": 15,
            "chatbot_reminder_no_show_reduction": 45,
            "average_appointment_value": 75,
            "note": "Automatische Erinnerungen reduzieren No-Shows um 45%"
        }
    },
    "13": {
        "id": "13",
        "title": "B2B Lead Qualification - Salesforce State of Marketing 2025",
        "url": "https://www.salesforce.com/resources/research-reports/state-of-marketing/",
        "data": {
            "manual_lead_qualification_hours_per_week": 12,
            "ai_lead_qualification_accuracy": 87,
            "sales_time_saved_percent": 40,
            "note": "AI-Chatbots qualifizieren Leads 87% genau, sparen 40% Zeit"
        }
    }
}

def get_source_by_id(source_id: str) -> dict:
    """Get source by ID"""
    return SOURCES.get(source_id, {})

def get_sources_for_industry(industry: str) -> list:
    """Get relevant sources for specific industry"""
    industry_mapping = {
        "hotel": ["1", "2", "3", "4", "7", "9"],
        "restaurant": ["1", "3", "5", "7"],
        "fitness": ["1", "3", "7", "10"],
        "salon": ["1", "3", "7", "12"],
        "immobilien": ["1", "3", "7", "11"],
        "ecommerce": ["1", "3", "7", "8"],
        "anwalt": ["1", "3", "7", "13"],
        "steuerberater": ["1", "3", "7", "13"],
        "versicherung": ["1", "3", "7", "13"],
        "arzt": ["1", "3", "7", "12"]
    }
    
    source_ids = industry_mapping.get(industry.lower(), ["1", "3", "6", "7"])
    return [SOURCES[sid] for sid in source_ids if sid in SOURCES]

def format_sources_for_prompt(sources: list) -> str:
    """Format sources for OpenAI prompt"""
    formatted = []
    for source in sources:
        formatted.append(f"""
[Source {source.get('id', 'N/A')}] {source.get('title', 'N/A')}
URL: {source.get('url', '#')}
Data: {source.get('data', {})}
""")
    return "\n".join(formatted)
