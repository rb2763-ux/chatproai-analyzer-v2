"""
CHATPRO AI ANALYZER - MCKINSEY-STYLE PDF REPORT GENERATOR
Premium Business Consulting Report Layout (German)
"""

from typing import Dict, List, Optional
from datetime import datetime
import os
import uuid

class PDFReportGenerator:
    """
    Generate McKinsey-style professional HTML reports in German
    """
    
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        os.makedirs(self.template_dir, exist_ok=True)
    
    def generate(
        self,
        crawler_data: Dict,
        analysis_data: Dict,
        company_name: str,
        industry: str,
        output_path: str,
        sources: List[Dict] = None
    ) -> str:
        """Generate McKinsey-style PDF report in German"""
        
        html_content = self._generate_html(
            crawler_data,
            analysis_data,
            company_name,
            industry,
            sources or []
        )
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write HTML first (temp)
        html_path = output_path.replace('.pdf', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Convert to PDF using Playwright Chromium
        pdf_path = output_path if output_path.endswith('.pdf') else output_path.replace('.html', '.pdf')
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(f'file://{os.path.abspath(html_path)}', wait_until='networkidle')
                page.pdf(
                    path=pdf_path,
                    format='A4',
                    print_background=True,
                    margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
                )
                browser.close()
            print(f"  ✅ PDF created: {pdf_path}")
            # Clean up HTML temp file
            try:
                os.remove(html_path)
            except:
                pass
            return pdf_path
        except Exception as e:
            print(f"  ⚠️ PDF conversion failed ({e}), falling back to HTML")
            return html_path
    
    def _generate_html(
        self,
        crawler_data: Dict,
        analysis_data: Dict,
        company_name: str,
        industry: str,
        sources: List[Dict] = None
    ) -> str:
        
        # Extract analysis data
        pain_points = analysis_data.get('pain_points', [])
        roi_calc = analysis_data.get('roi_calculation', {})
        recommendations = analysis_data.get('recommendations', [])
        chatbot_priority = analysis_data.get('chatbot_priority', 'MITTEL')
        
        # Website metrics
        website_check = {
            'pages': crawler_data.get('page_count', 0),
            'languages': len(crawler_data.get('languages', ['Deutsch'])),
            'mobile_friendly': crawler_data.get('is_mobile_friendly', True),
            'has_chatbot': crawler_data.get('has_chatbot', False),
            'chatbot_type': crawler_data.get('chatbot_type', 'Nicht vorhanden')
        }
        
        # Meta information
        today = datetime.now().strftime("%d.%m.%Y")
        report_id = str(uuid.uuid4())[:8].upper()
        
        # Industry mapping to German
        industry_map = {
            "hotel": "Hospitality & Hotellerie",
            "restaurant": "Gastronomie & Food Service",
            "fitness": "Health & Fitness",
            "salon": "Beauty & Wellness",
            "immobilien": "Immobilien & Real Estate",
            "ecommerce": "E-Commerce & Retail",
            "anwalt": "Rechtsberatung & Legal Services",
            "steuerberater": "Steuerberatung & Audit",
            "versicherung": "Versicherungswesen",
            "arzt": "Gesundheitswesen & Healthcare"
        }
        industry_label = industry_map.get(industry.lower(), industry.capitalize())
        
        # ROI metrics
        monthly_roi = roi_calc.get('monthly_roi', 0)
        roi_multiplier = roi_calc.get('roi_multiplier', 0)
        break_even = roi_calc.get('break_even_months', 0)
        
        # Priority translation — action-oriented, kein "MITTEL" (Eigentor-Vermeidung)
        priority_map = {'HIGH': 'SOFORT UMSETZEN', 'MEDIUM': 'KURZFRISTIG UMSETZEN', 'LOW': 'STRATEGISCH PLANEN',
                        'HOCH': 'SOFORT UMSETZEN', 'MITTEL': 'KURZFRISTIG UMSETZEN', 'NIEDRIG': 'STRATEGISCH PLANEN'}
        chatbot_priority_de = priority_map.get(chatbot_priority, 'KURZFRISTIG UMSETZEN')
        
        # Generate HTML sections
        pain_points_html = self._generate_pain_points_html(pain_points)
        roi_details_html = self._generate_roi_details_html(roi_calc)
        recommendations_html = self._generate_recommendations_html(recommendations, priority_map)
        sources_html = self._generate_sources_html(sources)
        website_analysis_html = self._generate_website_analysis_html(website_check, crawler_data)
        waterfall_chart_html = self._generate_waterfall_chart_html(roi_calc)
        
        # Traffic light scoring system
        scoring_html = self._generate_scoring_system(chatbot_priority, website_check)
        
        # Full McKinsey-style HTML template
        html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Digitale Effizienz-Analyse — {company_name}</title>
    <style>
        /* === MCKINSEY-STYLE CSS === */
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {{
            --primary-navy: #0f172a;
            --accent-blue: #2563eb;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --success-green: #059669;
            --warning-orange: #d97706;
            --danger-red: #dc2626;
            --background: #ffffff;
            --surface-light: #f8fafc;
            --border-light: #e2e8f0;
        }}
        
        /* Page Setup für PDF-Export */
        @page {{
            size: A4;
            margin: 0;
            color-adjust: exact;
            -webkit-print-color-adjust: exact;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            color: var(--text-primary);
            background: var(--background);
            font-size: 12px;
            line-height: 1.6;
        }}
        
        .page {{
            position: relative;
        }}
        
        /* Nur Deckblatt und CTA bekommen eigene Seite */
        .cover-page {{
            min-height: 100vh;
            page-break-after: always;
        }}
        
        .cta-page {{
            page-break-before: always;
        }}
        
        /* Quellenverzeichnis auf eigene Seite */
        .sources-page {{
            page-break-before: always;
        }}
        
        /* === DECKBLATT (PAGE 1) === */
        .cover-page {{
            background: linear-gradient(135deg, var(--primary-navy) 0%, #1e40af 100%);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 50px;
        }}
        
        .cover-header {{
            text-align: center;
            margin-top: 60px;
        }}
        
        .logo {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }}
        
        .cover-title {{
            font-size: 42px;
            font-weight: 300;
            margin: 30px 0;
            line-height: 1.2;
        }}
        
        .company-name {{
            font-size: 26px;
            font-weight: 600;
            color: #93c5fd;
            margin: 20px 0;
        }}
        
        .cover-meta {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 20px;
            margin: 40px 0;
            font-size: 13px;
        }}
        
        .cover-footer {{
            text-align: center;
            font-size: 11px;
            opacity: 0.8;
            border-top: 1px solid rgba(255,255,255,0.2);
            padding-top: 20px;
        }}
        
        /* === EXECUTIVE SUMMARY === */
        .exec-page {{
            padding: 30px 50px 20px 50px;
        }}
        
        .page-title {{
            font-size: 24px;
            font-weight: 600;
            color: var(--primary-navy);
            margin-bottom: 20px;
            position: relative;
        }}
        
        .page-title::after {{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 60px;
            height: 3px;
            background: var(--accent-blue);
        }}
        
        .traffic-lights {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 12px;
            margin: 15px 0;
        }}
        
        .traffic-light {{
            background: var(--surface-light);
            border-radius: 8px;
            padding: 14px;
            text-align: center;
            border: 1px solid var(--border-light);
        }}
        
        .traffic-icon {{
            font-size: 24px;
            margin-bottom: 10px;
        }}
        
        .traffic-label {{
            font-size: 11px;
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: 5px;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 12px;
            margin: 15px 0;
        }}
        
        .kpi-card {{
            background: var(--background);
            border: 2px solid var(--border-light);
            border-radius: 10px;
            padding: 16px;
            text-align: center;
        }}
        
        .kpi-label {{
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-secondary);
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .kpi-value {{
            font-size: 24px;
            font-weight: 700;
            color: var(--primary-navy);
            margin: 4px 0;
        }}
        
        .kpi-unit {{
            font-size: 14px;
            color: var(--text-secondary);
        }}
        
        .management-summary {{
            background: var(--surface-light);
            border-left: 4px solid var(--accent-blue);
            padding: 14px 18px;
            margin: 15px 0;
            font-size: 12px;
            line-height: 1.5;
        }}
        
        /* === STANDARD CONTENT PAGES === */
        .content-page {{
            padding: 25px 50px 15px 50px;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            page-break-after: avoid;
        }}
        
        .section-number {{
            background: var(--accent-blue);
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            margin-right: 15px;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            color: var(--primary-navy);
        }}
        
        /* Website Analysis Table */
        .analysis-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        .analysis-table th {{
            background: var(--surface-light);
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            font-size: 11px;
            border-bottom: 2px solid var(--border-light);
            color: var(--text-secondary);
        }}
        
        .analysis-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-light);
            font-size: 12px;
        }}
        
        .status-icon {{
            margin-right: 8px;
        }}
        
        .status-good {{ color: var(--success-green); }}
        .status-warning {{ color: var(--warning-orange); }}
        .status-critical {{ color: var(--danger-red); }}
        
        /* Risk Cards */
        .risk-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 10px 0;
        }}
        
        .risk-card {{
            border: 1px solid var(--border-light);
            border-radius: 8px;
            overflow: hidden;
            background: var(--background);
            page-break-inside: avoid;
        }}
        
        .risk-header {{
            background: linear-gradient(90deg, #fef2f2 0%, #fee2e2 100%);
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-light);
        }}
        
        .risk-id {{
            background: var(--danger-red);
            color: white;
            font-size: 9px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 8px;
        }}
        
        .risk-title {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }}
        
        .risk-body {{
            padding: 10px 14px;
        }}
        
        .risk-impact {{
            margin-bottom: 15px;
            line-height: 1.6;
        }}
        
        .risk-evidence {{
            font-size: 11px;
            color: var(--text-secondary);
            border-top: 1px dashed var(--border-light);
            padding-top: 12px;
            font-style: italic;
        }}
        
        /* ROI Tables */
        .roi-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 12px;
        }}
        
        .roi-table th {{
            background: var(--primary-navy);
            color: white;
            padding: 14px 16px;
            text-align: left;
            font-weight: 600;
        }}
        
        .roi-table td {{
            padding: 16px;
            border-bottom: 1px solid var(--border-light);
        }}
        
        .roi-category {{
            font-weight: 500;
        }}
        
        .roi-calculation {{
            color: var(--text-secondary);
            font-style: italic;
            font-size: 11px;
        }}
        
        .roi-value {{
            text-align: right;
            font-weight: 700;
            font-family: 'Monaco', monospace;
        }}
        
        .total-row {{
            background: var(--surface-light);
            border-top: 2px solid var(--accent-blue);
            font-weight: 700;
        }}
        
        .total-row .roi-value {{
            color: var(--accent-blue);
            font-size: 14px;
        }}
        
        /* Waterfall Chart */
        .waterfall-container {{
            margin: 15px 0;
            background: var(--surface-light);
            border-radius: 8px;
            padding: 15px;
            page-break-inside: avoid;
        }}
        
        .waterfall-title {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--primary-navy);
        }}
        
        .waterfall-bar {{
            display: flex;
            align-items: center;
            margin: 10px 0;
        }}
        
        .bar-label {{
            width: 120px;
            font-size: 11px;
            font-weight: 500;
        }}
        
        .bar-visual {{
            height: 20px;
            background: linear-gradient(90deg, var(--accent-blue), #3b82f6);
            border-radius: 4px;
            margin: 0 10px;
            position: relative;
        }}
        
        .bar-value {{
            font-size: 11px;
            font-weight: 600;
            color: var(--text-primary);
        }}
        
        /* Recommendations */
        .recommendation-card {{
            border-left: 4px solid var(--border-light);
            padding: 10px 16px;
            margin: 8px 0;
            background: var(--background);
            border-radius: 0 8px 8px 0;
            page-break-inside: avoid;
        }}
        
        .priority-hoch, .priority-sofort {{ border-left-color: var(--danger-red); }}
        .priority-mittel, .priority-kurzfristig {{ border-left-color: var(--warning-orange); }}
        .priority-niedrig, .priority-strategisch {{ border-left-color: var(--success-green); }}
        
        .rec-header {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .priority-badge {{
            font-size: 9px;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: 4px;
            color: white;
            margin-right: 12px;
        }}
        
        .badge-hoch, .badge-sofort {{ background: var(--danger-red); }}
        .badge-mittel, .badge-kurzfristig {{ background: var(--warning-orange); }}
        .badge-niedrig, .badge-strategisch {{ background: var(--success-green); }}
        
        .rec-title {{
            font-size: 15px;
            font-weight: 600;
            margin: 0;
        }}
        
        .rec-description {{
            margin: 8px 0;
            line-height: 1.6;
        }}
        
        .rec-impact {{
            font-size: 11px;
            color: var(--text-secondary);
            font-weight: 500;
        }}
        
        /* CTA Page */
        .cta-page {{
            padding: 30px 50px;
            text-align: center;
            background: linear-gradient(135deg, var(--surface-light) 0%, white 100%);
        }}
        
        .cta-title {{
            font-size: 28px;
            font-weight: 600;
            color: var(--primary-navy);
            margin: 30px 0 20px 0;
        }}
        
        .steps-container {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 18px;
            margin: 20px 0;
        }}
        
        .step-card {{
            background: white;
            border-radius: 10px;
            padding: 22px 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border-light);
        }}
        
        .step-number {{
            background: var(--accent-blue);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 18px;
            margin: 0 auto 20px auto;
        }}
        
        .step-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--primary-navy);
        }}
        
        .contact-info {{
            background: var(--primary-navy);
            color: white;
            padding: 24px;
            border-radius: 10px;
            margin: 25px 0;
        }}
        
        .contact-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
        }}
        
        .contact-details {{
            font-size: 14px;
            line-height: 1.8;
        }}
        
        .calendly-link {{
            color: #93c5fd;
            text-decoration: none;
            font-weight: 500;
        }}
        
        /* Sources */
        .sources-section {{
            margin-top: 40px;
            font-size: 11px;
        }}
        
        .source-item {{
            margin: 8px 0;
            line-height: 1.5;
        }}
        
        .source-id {{
            font-weight: 600;
            color: var(--accent-blue);
        }}
        
        /* Separator between flowing sections */
        .content-page + .content-page {{
            border-top: 1px solid var(--border-light);
        }}
    </style>
</head>
<body>

    <!-- DECKBLATT (PAGE 1) -->
    <div class="page cover-page">
        <div class="cover-header">
            <div class="logo">CHATPRO AI 🤖</div>
            <div class="cover-title">Digitale Effizienz-Analyse</div>
            <div class="company-name">{company_name}</div>
            
            <div class="cover-meta">
                <div>
                    <strong>Branche:</strong><br>{industry_label}
                </div>
                <div>
                    <strong>Analysedatum:</strong><br>{today}
                </div>
                <div>
                    <strong>Referenz-ID:</strong><br>CPA-{report_id}
                </div>
                <div>
                    <strong>Handlungspriorität:</strong><br>{chatbot_priority_de}
                </div>
            </div>
        </div>
        
        <div class="cover-footer">
            Vertraulich — Erstellt von ChatPro AI Analytics<br>
            © 2026 FITCOACHAI LTD. — Alle Rechte vorbehalten
        </div>
    </div>

    <!-- EXECUTIVE SUMMARY -->
    <div class="exec-page">
        <h1 class="page-title">Executive Summary</h1>
        
        <!-- Ampel-Scoring-System -->
        <div class="traffic-lights">
            {scoring_html}
        </div>
        
        <!-- KPI-Boxen -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Einsparpotenzial</div>
                <div class="kpi-value">€ {monthly_roi:,.0f}</div>
                <div class="kpi-unit">pro Monat</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">ROI-Faktor</div>
                <div class="kpi-value">{roi_multiplier:.1f}x</div>
                <div class="kpi-unit">Rendite-Multiplikator</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Amortisation</div>
                <div class="kpi-value">{break_even:.1f}</div>
                <div class="kpi-unit">Monate</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Handlungsbedarf</div>
                <div class="kpi-value" style="color: {
                    'var(--danger-red)' if chatbot_priority_de == 'HOCH' else 
                    'var(--warning-orange)' if chatbot_priority_de == 'MITTEL' else 
                    'var(--success-green)'
                }">{chatbot_priority_de}</div>
                <div class="kpi-unit">Prioritätsstufe</div>
            </div>
        </div>
        
        <!-- Management Summary -->
        <div class="management-summary">
            <strong>Management Summary:</strong> Die Analyse zeigt erhebliches Optimierungspotenzial in der digitalen Kundeninteraktion. 
            Durch strategische Automatisierung können monatlich €{monthly_roi:,.0f} an Effizienzgewinnen realisiert werden. 
            Die Amortisation erfolgt innerhalb von {break_even:.1f} Monaten bei einem ROI-Faktor von {roi_multiplier:.1f}x.
        </div>
    </div>

    <!-- WEBSITE-ANALYSE -->
    <div class="content-page">
        <div class="section-header">
            <div class="section-number">1</div>
            <div class="section-title">Technische Status-Quo Analyse</div>
        </div>
        
        <p>Die detaillierte Analyse der bestehenden Webpräsenz <strong>{crawler_data.get('url', 'N/A')}</strong> 
        ergab folgende technische und strukturelle Charakteristika:</p>
        
        {website_analysis_html}
    </div>

    <!-- IDENTIFIZIERTE INEFFIZIENZEN -->
    <div class="content-page">
        <div class="section-header">
            <div class="section-number">2</div>
            <div class="section-title">Identifizierte Ineffizienzen & Geschäftsrisiken</div>
        </div>
        
        <p>Die Analyse der operativen Prozesse zeigt kritische Schwachstellen in der Kundeninteraktion auf:</p>
        
        {pain_points_html}
    </div>

    <!-- ROI-BERECHNUNG -->
    <div class="content-page">
        <div class="section-header">
            <div class="section-number">3</div>
            <div class="section-title">Wirtschaftlichkeitsbetrachtung (ROI-Analyse)</div>
        </div>
        
        <p style="margin-bottom: 12px; color: var(--text-secondary);">
            <em>Hinweis: Alle Berechnungen basieren auf konservativen Branchenbenchmarks und dokumentierten Effizienzgewinnen. 
            Quellenreferenzen siehe Anhang.</em>
        </p>
        
        <!-- ROI-Details Tabelle -->
        <table class="roi-table">
            <thead>
                <tr>
                    <th style="width: 35%">Kostenstelle / Optimierungsbereich</th>
                    <th style="width: 45%">Berechnungsgrundlage</th>
                    <th style="width: 20%">Monatlicher Wert</th>
                </tr>
            </thead>
            <tbody>
                {roi_details_html}
                <tr class="total-row">
                    <td><strong>GESAMT-EINSPARPOTENZIAL</strong></td>
                    <td><em>Summe aller identifizierten Optimierungen</em></td>
                    <td class="roi-value"><strong>€ {monthly_roi:,.0f}</strong></td>
                </tr>
            </tbody>
        </table>
        
        <!-- Wasserfall-Chart -->
        {waterfall_chart_html}
    </div>

    <!-- STRATEGISCHE EMPFEHLUNGEN -->
    <div class="content-page">
        <div class="section-header">
            <div class="section-number">4</div>
            <div class="section-title">Strategische Handlungsempfehlungen</div>
        </div>
        
        <p>Basierend auf der Analyseergebnisse empfehlen wir folgende priorisierte Maßnahmen:</p>
        
        {recommendations_html}
    </div>

    <!-- CTA-SEITE -->
    <div class="cta-page">
        <h1 class="cta-title">Nächste Schritte</h1>
        
        <p style="font-size: 16px; color: var(--text-secondary); max-width: 600px; margin: 0 auto;">
            Realisieren Sie das identifizierte Potenzial von <strong>€{monthly_roi:,.0f}/Monat</strong> 
            durch strategische Digitalisierung Ihrer Kundeninteraktion.
        </p>
        
        <div class="steps-container">
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-title">Kostenlose Beratung buchen</div>
                <p>Individuelle Strategiesession zur Detailplanung und Implementierungsroadmap</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-title">Individuelles Konzept</div>
                <p>Entwicklung einer maßgeschneiderten Lösung für Ihre spezifischen Anforderungen</p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-title">Implementierung</div>
                <p>Professionelle Umsetzung mit Erfolgsgarantie und kontinuierlicher Optimierung</p>
            </div>
        </div>
        
        <div class="contact-info">
            <div class="contact-title">Direktkontakt für Rückfragen</div>
            <div class="contact-details">
                <strong>Beratungstermin buchen:</strong><br>
                <a href="https://calendly.com/chatproaiio/30min" class="calendly-link" target="_blank">
                    calendly.com/chatproaiio/30min
                </a><br><br>
                
                <strong>E-Mail:</strong> info@chatproai.io<br>
                <strong>Telefon:</strong> +49 322 126 190 99<br>
                <strong>Geschäftszeiten:</strong> Mo-Fr 9:00-18:00 Uhr
            </div>
        </div>
        
        <div style="margin-top: 25px; font-size: 12px; color: var(--text-secondary);">
            <strong>CHATPRO AI</strong> — Premium KI-Lösungen für Unternehmenseffizienz<br>
            FITCOACHAI LTD | Spezialisiert auf B2B-Automatisierung & ROI-optimierte Digitalisierung
        </div>
    </div>

    <!-- QUELLENVERZEICHNIS -->
    <div class="content-page sources-page">
        <div class="section-header">
            <div class="section-number">A</div>
            <div class="section-title">Quellenverzeichnis & Methodik</div>
        </div>
        
        <h3 style="color: var(--primary-navy); margin-bottom: 15px;">Datengrundlagen:</h3>
        <div class="sources-section">
            {sources_html}
        </div>
        
        <h3 style="color: var(--primary-navy); margin: 30px 0 15px 0;">Analysemethodik:</h3>
        <p style="font-size: 12px; line-height: 1.6;">
            Die vorliegende Analyse basiert auf einer systematischen Auswertung der technischen Webpräsenz, 
            kombiniert mit branchenspezifischen Benchmarks und dokumentierten Best Practices. 
            Alle ROI-Berechnungen wurden nach konservativen Annahmen durchgeführt, um realistische 
            Erwartungswerte zu gewährleisten.
        </p>
        
        <h3 style="color: var(--primary-navy); margin: 30px 0 15px 0;">Haftungsausschluss:</h3>
        <p style="font-size: 11px; color: var(--text-secondary); line-height: 1.6;">
            Dieser Bericht wurde durch KI-gestützte Analyse erstellt. Die ROI-Projektionen stellen 
            Schätzungen basierend auf Branchendurchschnittswerten dar und können nicht als Garantie 
            für tatsächliche Ergebnisse interpretiert werden. Einzelergebnisse können variieren.
        </p>
        
        <div style="margin-top: 30px; text-align: center; font-size: 10px; color: var(--text-secondary); border-top: 1px solid var(--border-light); padding-top: 15px;">
            ChatPro AI Analytics — Bericht generiert am {today}
        </div>
    </div>

</body>
</html>
"""
        return html
    
    def _generate_scoring_system(self, chatbot_priority: str, website_check: Dict) -> str:
        """Generate traffic light scoring system for different areas"""
        
        # Automatisierung Status
        automation_color = "🔴" if not website_check.get('has_chatbot') else "🟢"
        automation_status = "KRITISCH" if not website_check.get('has_chatbot') else "GUT"
        
        # Skalierbarkeit
        scalability_color = "🟡" if website_check.get('pages', 0) > 15 else "🟢"
        scalability_status = "OPTIMIERBAR" if website_check.get('pages', 0) > 15 else "GUT"
        
        # Effizienz
        efficiency_color = "🔴" if chatbot_priority == "HIGH" else ("🟡" if chatbot_priority == "MEDIUM" else "🟢")
        efficiency_status = "NIEDRIG" if chatbot_priority == "HIGH" else ("MITTEL" if chatbot_priority == "MEDIUM" else "HOCH")
        
        # Wettbewerbsfähigkeit
        competitive_color = "🟡" if website_check.get('languages', 1) < 2 else "🟢"
        competitive_status = "AUSBAUFÄHIG" if website_check.get('languages', 1) < 2 else "STARK"
        
        return f"""
            <div class="traffic-light">
                <div class="traffic-icon">{automation_color}</div>
                <div class="traffic-label">Automatisierung</div>
                <div style="font-weight: 600; font-size: 12px;">{automation_status}</div>
            </div>
            <div class="traffic-light">
                <div class="traffic-icon">{scalability_color}</div>
                <div class="traffic-label">Skalierbarkeit</div>
                <div style="font-weight: 600; font-size: 12px;">{scalability_status}</div>
            </div>
            <div class="traffic-light">
                <div class="traffic-icon">{efficiency_color}</div>
                <div class="traffic-label">Prozesseffizienz</div>
                <div style="font-weight: 600; font-size: 12px;">{efficiency_status}</div>
            </div>
            <div class="traffic-light">
                <div class="traffic-icon">{competitive_color}</div>
                <div class="traffic-label">Wettbewerbsposition</div>
                <div style="font-weight: 600; font-size: 12px;">{competitive_status}</div>
            </div>
        """
    
    def _generate_website_analysis_html(self, website_check: Dict, crawler_data: Dict) -> str:
        """Generate website analysis table"""
        
        mobile_status = "✅ Optimiert" if website_check.get('mobile_friendly') else "❌ Nicht optimiert"
        mobile_class = "status-good" if website_check.get('mobile_friendly') else "status-critical"
        
        chatbot_status = "❌ Nicht vorhanden" if not website_check.get('has_chatbot') else f"✅ {website_check.get('chatbot_type')}"
        chatbot_class = "status-critical" if not website_check.get('has_chatbot') else "status-good"
        
        complexity = "⚠️ Hoch" if website_check.get('pages', 0) > 20 else "✅ Standard"
        complexity_class = "status-warning" if website_check.get('pages', 0) > 20 else "status-good"
        
        return f"""
        <table class="analysis-table">
            <thead>
                <tr>
                    <th>Analyseparameter</th>
                    <th>Ist-Zustand</th>
                    <th>Bewertung</th>
                    <th>Geschäftsimpact</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Informationsarchitektur</strong></td>
                    <td>{website_check.get('pages', 0)} indexierte Seiten</td>
                    <td><span class="status-icon {complexity_class}">{complexity}</span></td>
                    <td>{'Hoher Support-Bedarf durch Komplexität' if website_check.get('pages', 0) > 20 else 'Überschaubare Struktur'}</td>
                </tr>
                <tr>
                    <td><strong>Mobile Optimierung</strong></td>
                    <td>Responsive Design</td>
                    <td><span class="status-icon {mobile_class}">{mobile_status}</span></td>
                    <td>{'Nutzerfreundliche mobile Experience' if website_check.get('mobile_friendly') else 'Potenzielle Abbrüche bei mobilen Nutzern'}</td>
                </tr>
                <tr>
                    <td><strong>Kundenservice-Automatisierung</strong></td>
                    <td>{website_check.get('chatbot_type', 'Keine Automatisierung')}</td>
                    <td><span class="status-icon {chatbot_class}">{chatbot_status}</span></td>
                    <td>{'Manuelle Bearbeitung aller Anfragen erforderlich' if not website_check.get('has_chatbot') else 'Teilautomatisierte Kundenbetreuung'}</td>
                </tr>
                <tr>
                    <td><strong>Internationalisierung</strong></td>
                    <td>{website_check.get('languages', 1)} Sprache(n) erkannt</td>
                    <td><span class="status-icon {'status-warning' if website_check.get('languages', 1) < 2 else 'status-good'}">
                        {'⚠️ Monolingual' if website_check.get('languages', 1) < 2 else '✅ Multilingual'}</span></td>
                    <td>{'Begrenzte Zielgruppenreichweite' if website_check.get('languages', 1) < 2 else 'Internationale Markterschließung möglich'}</td>
                </tr>
            </tbody>
        </table>
        """
    
    def _generate_pain_points_html(self, pain_points: List[Dict]) -> str:
        """Generate risk cards for identified pain points"""
        
        if not pain_points:
            return """
            <div style="text-align: center; color: var(--text-secondary); padding: 40px;">
                <em>Keine kritischen Ineffizienzen identifiziert.</em>
            </div>
            """
        
        html = '<div class="risk-grid">'
        
        for i, pp in enumerate(pain_points[:4], 1):
            html += f"""
            <div class="risk-card">
                <div class="risk-header">
                    <div class="risk-id">RISIKO #{i}</div>
                    <h4 class="risk-title">{pp.get('problem', 'N/A')}</h4>
                </div>
                <div class="risk-body">
                    <div class="risk-impact">
                        <strong>Wirtschaftliche Auswirkung:</strong><br>
                        {pp.get('impact', 'N/A')}
                    </div>
                    <div class="risk-evidence">
                        <strong>Daten-Evidenz:</strong> {pp.get('evidence', 'N/A')}
                        {' [' + ', '.join(pp.get('source_ids', [])) + ']' if pp.get('source_ids') else ''}
                    </div>
                </div>
            </div>
            """
        
        html += '</div>'
        return html
    
    def _generate_roi_details_html(self, roi_calc: Dict) -> str:
        """Generate ROI calculation table rows"""
        
        calculations = roi_calc.get('calculations', [])
        if not calculations:
            return """
            <tr>
                <td colspan="3" style="text-align: center; color: var(--text-secondary); padding: 20px;">
                    <em>Keine detaillierten ROI-Berechnungen verfügbar.</em>
                </td>
            </tr>
            """
        
        html = ""
        for calc in calculations:
            source_refs = ""
            if calc.get('source_ids'):
                source_refs = " [" + ", ".join(calc.get('source_ids', [])) + "]"
            
            html += f"""
            <tr>
                <td class="roi-category">{calc.get('category', 'N/A')}</td>
                <td class="roi-calculation">{calc.get('calculation', 'N/A')}{source_refs}</td>
                <td class="roi-value">€ {calc.get('monthly_value', 0):,.0f}</td>
            </tr>
            """
        
        return html
    
    def _generate_waterfall_chart_html(self, roi_calc: Dict) -> str:
        """Generate CSS-based waterfall chart"""
        
        calculations = roi_calc.get('calculations', [])
        if not calculations:
            return ""
        
        max_value = max([calc.get('monthly_value', 0) for calc in calculations] + [1])
        
        html = """
        <div class="waterfall-container">
            <div class="waterfall-title">Aufschlüsselung der monatlichen Einsparungen</div>
        """
        
        for calc in calculations:
            value = calc.get('monthly_value', 0)
            width_pct = (value / max_value) * 100
            
            html += f"""
            <div class="waterfall-bar">
                <div class="bar-label">{calc.get('category', 'N/A')[:15]}...</div>
                <div class="bar-visual" style="width: {width_pct}%"></div>
                <div class="bar-value">€ {value:,.0f}</div>
            </div>
            """
        
        html += "</div>"
        return html
    
    def _generate_recommendations_html(self, recommendations: List[Dict], priority_map: Dict) -> str:
        """Generate recommendation cards with German priority levels"""
        
        if not recommendations:
            return """
            <div style="text-align: center; color: var(--text-secondary); padding: 40px;">
                <em>Keine spezifischen Empfehlungen verfügbar.</em>
            </div>
            """
        
        html = ""
        
        for rec in recommendations:
            priority = rec.get('priority', 'MEDIUM')
            priority_label = priority_map.get(priority, 'KURZFRISTIG UMSETZEN')
            # CSS class mapping
            css_map = {'SOFORT UMSETZEN': 'sofort', 'KURZFRISTIG UMSETZEN': 'kurzfristig', 'STRATEGISCH PLANEN': 'strategisch',
                       'HOCH': 'sofort', 'MITTEL': 'kurzfristig', 'NIEDRIG': 'strategisch'}
            priority_css = css_map.get(priority_label, css_map.get(priority, 'kurzfristig'))
            
            html += f"""
            <div class="recommendation-card priority-{priority_css}">
                <div class="rec-header">
                    <div class="priority-badge badge-{priority_css}">{priority_label}</div>
                    <h4 class="rec-title">{rec.get('title', 'N/A')}</h4>
                </div>
                <div class="rec-description">{rec.get('description', 'N/A')}</div>
                <div class="rec-impact">
                    <strong>Erwarteter Impact:</strong> {rec.get('impact', 'N/A')}<br>
                    <strong>Umsetzung:</strong> {rec.get('implementation', 'N/A')}
                </div>
            </div>
            """
        
        return html
    
    def _generate_sources_html(self, sources: List[Dict]) -> str:
        """Generate sources list"""
        
        if not sources:
            return """
            <div class="source-item">
                <em>Keine externen Quellen referenziert. Analyse basiert auf internen Benchmarks und Best Practices.</em>
            </div>
            """
        
        html = ""
        
        for source in sources:
            source_id = source.get('id', '?')
            title = source.get('title', 'Unbekannte Quelle')
            url = source.get('url', '#')
            year = source.get('year', datetime.now().year)
            
            html += f"""
            <div class="source-item">
                <span class="source-id">[{source_id}]</span> 
                {title}, {year} — <a href="{url}" target="_blank" style="color: var(--accent-blue);">{url}</a>
            </div>
            """
        
        return html