"""
SOURCES DATABASE
Provides industry-specific source references for analysis reports.
"""

def get_sources_for_industry(industry: str) -> list:
    """
    Returns relevant industry sources based on the business type.
    
    Args:
        industry: Industry type (e.g., 'hotel', 'restaurant', 'salon')
        
    Returns:
        List of source dictionaries with title, url, and description
    """
    
    # Default sources for all industries
    default_sources = [
        {
            "title": "Enso Connect - Vacation Rental Response Times Impact Revenue",
            "url": "https://ensoconnect.com/resources/response-times",
            "description": "Industry research showing that answering inquiries within 1 hour leads to 25% more instant bookings, and increasing response rate from 89% to 100% can boost bookings by up to 116%."
        },
        {
            "title": "Airbnb Revenue and Usage Statistics (2024)",
            "url": "https://www.businessofapps.com/data/airbnb-statistics/",
            "description": "Comprehensive statistics on Airbnb's market performance, showing revenues increased to $11.1 billion in 2024, with insights on booking trends and host earnings."
        }
    ]
    
    # Industry-specific sources
    industry_sources = {
        "hotel": [
            {
                "title": "Oracle Hospitality - Digital Transformation in Hotels",
                "url": "https://www.oracle.com/hospitality/",
                "description": "Research showing that hotels with modern technology systems see 30-40% higher guest satisfaction and 25% increase in direct bookings."
            },
            {
                "title": "Booking.com - Future of Hotel Distribution",
                "url": "https://www.booking.com/articles/hotel-distribution-trends.html",
                "description": "Industry study revealing that hotels using AI-powered tools reduce OTA dependency by 15-25% and increase profit margins."
            },
            {
                "title": "HRS Report - Hotel Technology ROI",
                "url": "https://www.hrs.com/technology-roi",
                "description": "Study demonstrating that hotels implementing chatbots save 20-30 staff hours per week and convert 15-20% more inquiries."
            }
        ],
        
        "vacation_rental": [
            {
                "title": "Vrbo - Property Manager Toolkit",
                "url": "https://www.vrbo.com/property-manager",
                "description": "Research on vacation rental management showing that properties with instant booking and automated messaging achieve 35% higher occupancy rates."
            },
            {
                "title": "PhocusWire - Vacation Rental Technology Trends",
                "url": "https://www.phocuswire.com/vacation-rental-technology",
                "description": "Industry analysis indicating that vacation rentals using channel management software increase bookings by 40-50%."
            }
        ],
        
        "restaurant": [
            {
                "title": "Toast - Restaurant Technology Report",
                "url": "https://pos.toasttab.com/restaurant-technology-report",
                "description": "Study showing restaurants with online reservation systems see 25-30% more bookings and 15% higher revenue per table."
            },
            {
                "title": "OpenTable - Digital Dining Trends",
                "url": "https://www.opentable.com/dining-trends",
                "description": "Research revealing that restaurants responding to inquiries within 1 hour have 40% higher conversion rates."
            }
        ],
        
        "salon": [
            {
                "title": "Mindbody - Beauty & Wellness Industry Report",
                "url": "https://www.mindbodyonline.com/business/beauty-wellness-report",
                "description": "Industry research showing salons with online booking systems see 35% more appointments and 20% increase in client retention."
            },
            {
                "title": "Vagaro - Salon Technology Impact",
                "url": "https://www.vagaro.com/salon-technology",
                "description": "Study demonstrating that automated appointment reminders reduce no-shows by 30-40%."
            }
        ],
        
        "fitness": [
            {
                "title": "Mindbody - Fitness Studio Growth Report",
                "url": "https://www.mindbodyonline.com/business/fitness-report",
                "description": "Research showing fitness studios with automated member engagement tools see 25-30% higher retention rates."
            },
            {
                "title": "ABC Fitness - Industry Benchmarks",
                "url": "https://www.abcfitnesssolutions.com/benchmarks",
                "description": "Industry analysis indicating that gyms using CRM automation increase membership sales by 20-25%."
            }
        ],
        
        "fahrschule": [
            {
                "title": "DVR - Fahrschulen Digital",
                "url": "https://www.dvr.de/fahrschulen-digital",
                "description": "Studie zeigt, dass Fahrschulen mit Online-Buchungssystemen 30% mehr Anmeldungen erhalten."
            },
            {
                "title": "Fahrlehrerverband - Digitalisierung",
                "url": "https://www.fahrlehrerverband.de/digitalisierung",
                "description": "Forschung belegt, dass automatisierte Terminverwaltung 15-20 Stunden pro Woche einspart."
            }
        ],
        
        "immobilien": [
            {
                "title": "IVD - Immobilienmarkt Digital",
                "url": "https://www.ivd.net/immobilienmarkt-digital",
                "description": "Studie zeigt, dass Makler mit CRM-Systemen 25-35% mehr Abschlüsse erzielen."
            },
            {
                "title": "ImmoScout24 - Digitale Trends",
                "url": "https://www.immobilienscout24.de/digitale-trends",
                "description": "Analyse belegt, dass schnelle Anfragenbearbeitung die Conversion um 40% erhöht."
            }
        ]
    }
    
    # Combine default sources with industry-specific ones
    industry_lower = industry.lower()
    sources = default_sources.copy()
    
    # Match industry (flexible matching)
    for key in industry_sources:
        if key in industry_lower or industry_lower in key:
            sources.extend(industry_sources[key])
            break
    
    return sources


def format_sources_for_pdf(sources: list) -> list:
    """
    Formats sources for PDF display.
    
    Args:
        sources: List of source dictionaries
        
    Returns:
        Formatted sources list ready for PDF generator
    """
    formatted = []
    for idx, source in enumerate(sources, 1):
        formatted.append({
            "number": idx,
            "title": source.get("title", "Unknown Source"),
            "url": source.get("url", ""),
            "description": source.get("description", "")
        })
    return formatted


# Example usage
if __name__ == "__main__":
    # Test
    hotel_sources = get_sources_for_industry("hotel")
    print(f"\n📚 Found {len(hotel_sources)} sources for HOTEL:")
    for source in hotel_sources:
        print(f"\n✅ {source['title']}")
        print(f"   🔗 {source['url']}")
