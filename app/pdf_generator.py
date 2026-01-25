"""
CHATPRO AI ANALYZER - PDF REPORT GENERATOR
Professional Audit-Style HTML Reports (McKinsey Style)
"""

from typing import Dict, List, Optional
from datetime import datetime
import os

class PDFReportGenerator:
    """
    Generate professional Audit-Style HTML reports
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
        """Generate HTML report"""
        
        html_content = self._generate_html(
            crawler_data,
            analysis_data,
            company_name,
            industry,
            sources or []
        )
        
        html_path = output_path
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_path
    
    def _generate_html(
        self,
        crawler_data: Dict,
        analysis_data: Dict,
        company_name: str,
        industry: str,
        sources: List[Dict] = None
    ) -> str:
        
        # Extract Data
        pain_points = analysis_data.get('pain_points', [])
        roi_calc = analysis_data.get('roi_calculation', {})
        recommendations = analysis_data.get('recommendations', [])
        chatbot_priority = analysis_data.get('chatbot_priority', 'MEDIUM')
        
        # Website Metrics
        website_check = {
            'pages': crawler_data.get('page_count', 0),
            'languages': len(crawler_data.get('languages', ['Deutsch'])),
            'mobile_friendly': crawler_data.get('is_mobile_friendly', True)
        }
        
        chatbot_analysis = {
            'has_chatbot': crawler_data.get('has_chatbot', False),
            'chatbot_type': crawler_data.get('chatbot_type', 'Nicht vorhanden'),
            'priority': chatbot_priority
        }
        
        # Meta Data
        today = datetime.now().strftime("%d.%m.%Y")
        
        # Industry Mapping
        industry_map = {
            "hotel": "Hospitality / Hotellerie",
            "restaurant": "Gastronomie / Food Service",
            "fitness": "Health & Fitness",
            "salon": "Beauty & Care",
            "immobilien": "Real Estate",
            "ecommerce": "E-Commerce / Retail",
            "anwalt": "Legal Services",
            "steuerberater": "Tax & Audit",
            "versicherung": "Insurance",
            "arzt": "Healthcare"
        }
        industry_label = industry_map.get(industry.lower(), industry.capitalize())
        
        # ROI Metrics
        monthly_roi = roi_calc.get('monthly_roi', 0)
        roi_multiplier = roi_calc.get('roi_multiplier', 0)
        break_even = roi_calc.get('break_even_months', 0)
        
        # --- HTML GENERATION HELPERS ---
        
        # 1. Sources List
        sources_html = ""
        if sources:
            for source in sources:
                sources_html += f"""
                <div class="source-item">
                    <span class="source-id">[{source.get('id', '?')}]</span>
                    <span class="source-title">{source.get('title', 'N/A')}</span>
                    <a href="{source.get('url', '#')}" target="_blank" class="source-link">Quelle öffnen ↗</a>
                </div>
                """
        
        # 2. Pain Points (Ineffizienzen)
        pain_points_html = ""
        for i, pp in enumerate(pain_points[:3], 1):
            pain_points_html += f"""
            <div class="audit-finding">
                <div class="finding-header">
                    <span class="finding-id">RISIKO #{i}</span>
                    <h4>{pp.get('problem', 'N/A')}</h4>
                </div>
                <div class="finding-body">
                    <p><strong>Wirtschaftliche Auswirkung:</strong><br>{pp.get('impact', 'N/A')}</p>
                    <p class="evidence"><em>Daten-Evidenz: {pp.get('evidence', 'N/A')}</em></p>
                </div>
            </div>
            """
            
        # 3. ROI Details
        roi_details_html = ""
        for calc in roi_calc.get('calculations', []):
            roi_details_html += f"""
            <tr class="roi-row">
                <td class="roi-cat">{calc.get('category', 'N/A')}</td>
                <td class="roi-calc">{calc.get('calculation', 'N/A')}</td>
                <td class="roi-val">€ {calc.get('monthly_value', 0):,.0f}</td>
            </tr>
            """

        # 4. Recommendations
        recommendations_html = ""
        for rec in recommendations[:4]:
            prio = rec.get('priority', 'MEDIUM')
            recommendations_html += f"""
            <div class="rec-item border-{prio.lower()}">
                <div class="rec-header">
                    <span class="badge badge-{prio.lower()}">{prio} PRIORITY</span>
                    <h4>{rec.get('title', 'N/A')}</h4>
                </div>
                <p>{rec.get('description', 'N/A')}</p>
                <div class="rec-meta">
                    <span><strong>Impact:</strong> {rec.get('impact', 'N/A')}</span>
                </div>
            </div>
            """

        # --- FULL TEMPLATE ---
        html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Digital Efficiency Audit - {company_name}</title>
    <style>
        :root {{
            --primary: #0f172a; /* Navy Blue */
            --secondary: #334155; /* Slate */
            --accent: #2563eb; /* Royal Blue */
            --bg: #f8fafc;
            --surface: #ffffff;
            --border: #e2e8f0;
            --text: #1e293b;
            --text-light: #64748b;
            --danger: #ef4444;
            --success: #10b981;
        }}
        
        body {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.5;
            margin: 0;
            padding: 40px;
            font-size: 14px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: var(--surface);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--border);
        }}
        
        /* HEADER */
        .report-header {{
            background: var(--primary);
            color: white;
            padding: 40px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        
        .header-left h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 300;
            letter-spacing: 1px;
            text-transform: uppercase;
            opacity: 0.9;
        }}
        
        .header-left h2 {{
            margin: 10px 0 0 0;
            font-size: 32px;
            font-weight: 700;
        }}
        
        .header-right {{
            text-align: right;
            font-size: 12px;
            opacity: 0.8;
        }}
        
        /* EXECUTIVE SUMMARY */
        .exec-summary {{
            padding: 40px;
            background: #f1f5f9;
            border-bottom: 1px solid var(--border);
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: 1.5fr 1fr 1fr 1fr;
            gap: 30px;
        }}
        
        .kpi-box h3 {{
            margin: 0 0 10px 0;
            font-size: 12px;
            text-transform: uppercase;
            color: var(--text-light);
            letter-spacing: 0.5px;
        }}
        
        .kpi-main {{
            font-size: 42px;
            font-weight: 700;
            color: var(--primary);
        }}
        
        .kpi-sub {{
            font-size: 24px;
            font-weight: 600;
            color: var(--secondary);
        }}
        
        .kpi-desc {{
            font-size: 12px;
            color: var(--text-light);
            margin-top: 5px;
        }}
        
        /* SECTIONS */
        .section {{
            padding: 40px;
            border-bottom: 1px solid var(--border);
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 25px;
            display: flex;
            align-items: center;
        }}
        
        .section-title::before {{
            content: '';
            display: block;
            width: 4px;
            height: 18px;
            background: var(--accent);
            margin-right: 10px;
        }}
        
        /* AUDIT FINDINGS */
        .audit-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}
        
        .audit-finding {{
            border: 1px solid var(--border);
            background: #fff;
        }}
        
        .finding-header {{
            background: #f8fafc;
            padding: 15px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .finding-id {{
            font-size: 10px;
            font-weight: 700;
            color: var(--danger);
            background: #fef2f2;
            padding: 2px 8px;
            border-radius: 4px;
        }}
        
        .finding-header h4 {{
            margin: 0;
            font-size: 14px;
            font-weight: 600;
        }}
        
        .finding-body {{
            padding: 20px;
        }}
        
        .evidence {{
            margin-top: 15px;
            font-size: 12px;
            color: var(--text-light);
            border-top: 1px dashed var(--border);
            padding-top: 10px;
        }}
        
        /* ROI TABLE */
        .roi-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        
        .roi-table th {{
            text-align: left;
            padding: 12px;
            background: #f8fafc;
            border-bottom: 2px solid var(--border);
            color: var(--text-light);
            font-weight: 600;
        }}
        
        .roi-table td {{
            padding: 15px 12px;
            border-bottom: 1px solid var(--border);
        }}
        
        .roi-val {{
            text-align: right;
            font-weight: 700;
            font-family: monospace;
            font-size: 14px;
        }}
        
        .roi-calc {{
            color: var(--text-light);
            font-style: italic;
        }}
        
        /* RECOMMENDATIONS */
        .rec-item {{
            margin-bottom: 20px;
            padding: 20px;
            background: #fff;
            border-left: 4px solid #ccc;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        
        .border-high {{ border-left-color: var(--danger); }}
        .border-medium {{ border-left-color: #f59e0b; }}
        .border-low {{ border-left-color: var(--success); }}
        
        .rec-header {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .badge {{
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 3px;
            margin-right: 10px;
            color: white;
        }}
        
        .badge-high {{ background: var(--danger); }}
        .badge-medium {{ background: #f59e0b; }}
        .badge-low {{ background: var(--success); }}
        
        .rec-header h4 {{ margin: 0; font-size: 15px; }}
        
        /* FOOTER */
        .report-footer {{
            background: #f1f5f9;
            padding: 30px 40px;
            font-size: 12px;
            color: var(--text-light);
            border-top: 1px solid var(--border);
        }}
        
        .disclaimer {{
            margin-top: 20px;
            font-style: italic;
            font-size: 11px;
        }}
        
        .source-item {{
            margin-bottom: 5px;
        }}
        
        .source-id {{ font-weight: bold; margin-right: 5px; }}
        .source-link {{ color: var(--accent); text-decoration: none; margin-left: 10px; }}
        
    </style>
</head>
<body>

    <div class="container">
        <!-- HEADER -->
        <div class="report-header">
            <div class="header-left">
                <h1>Digital Efficiency Audit</h1>
                <h2>{company_name}</h2>
            </div>
            <div class="header-right">
                <p>Datum: {today}</p>
                <p>Sektor: {industry_label}</p>
                <p>Ref-ID: {chatbot_priority}-AUDIT</p>
            </div>
        </div>

        <!-- EXECUTIVE SUMMARY -->
        <div class="exec-summary">
            <div class="summary-grid">
                <div class="kpi-box">
                    <h3>Identifiziertes Einsparpotenzial</h3>
                    <div class="kpi-main">€ {monthly_roi:,.0f}</div>
                    <div class="kpi-desc">Pro Monat (Konservativ geschätzt)</div>
                </div>
                <div class="kpi-box">
                    <h3>ROI Faktor</h3>
                    <div class="kpi-sub">{roi_multiplier:.1f}x</div>
                    <div class="kpi-desc">Return on Investment</div>
                </div>
                <div class="kpi-box">
                    <h3>Amortisation</h3>
                    <div class="kpi-sub">{break_even:.1f} M</div>
                    <div class="kpi-desc">Monate bis Break-Even</div>
                </div>
                <div class="kpi-box">
                    <h3>Handlungsbedarf</h3>
                    <div class="kpi-sub" style="color: {
                        '#ef4444' if chatbot_priority == 'HIGH' else '#f59e0b'
                    }">{chatbot_priority}</div>
                    <div class="kpi-desc">Priorität der Umsetzung</div>
                </div>
            </div>
        </div>

        <!-- 1. STATUS QUO -->
        <div class="section">
            <div class="section-title">1. Technische Status-Quo Analyse</div>
            <p style="margin-bottom: 20px;">
                Die technische Analyse der Webpräsenz ({crawler_data.get('url', 'N/A')}) zeigt folgende Infrastruktur-Merkmale:
            </p>
            <table class="roi-table">
                <tr>
                    <th>Parameter</th>
                    <th>Status</th>
                    <th>Bewertung</th>
                </tr>
                <tr>
                    <td>Informationsarchitektur</td>
                    <td>{website_check.get('pages', 0)} indexierte Seiten</td>
                    <td>{'Hohe Komplexität' if website_check.get('pages', 0) > 20 else 'Standard'}</td>
                </tr>
                <tr>
                    <td>Internationalisierung</td>
                    <td>{website_check.get('languages', 1)} Sprachen erkannt</td>
                    <td>{'Erweiterungsbedarf' if website_check.get('languages', 1) < 2 else 'International ausgerichtet'}</td>
                </tr>
                <tr>
                    <td>Automatisierungsgrad</td>
                    <td>{chatbot_analysis.get('chatbot_type')}</td>
                    <td>{'Kritisch (Manuelle Prozesse)' if not chatbot_analysis.get('has_chatbot') else 'Vorhanden'}</td>
                </tr>
            </table>
        </div>

        <!-- 2. INEFFIZIENZEN -->
        <div class="section">
            <div class="section-title">2. Identifizierte Ineffizienzen & Risiken</div>
            <div class="audit-grid">
                {pain_points_html}
            </div>
        </div>

        <!-- 3. WIRTSCHAFTLICHKEIT -->
        <div class="section">
            <div class="section-title">3. Wirtschaftlichkeitsbetrachtung (ROI)</div>
            <p style="margin-bottom: 20px; font-size: 13px; color: #666;">
                Die folgende Berechnung basiert auf branchenspezifischen Benchmarks und den erhobenen Website-Daten. 
                Alle Annahmen sind konservativ gewählt.
            </p>
            <table class="roi-table">
                <thead>
                    <tr>
                        <th width="40%">Kostenstelle / Potenzial</th>
                        <th width="40%">Berechnungsgrundlage</th>
                        <th width="20%" style="text-align:right">Monatlicher Wert</th>
                    </tr>
                </thead>
                <tbody>
                    {roi_details_html}
                    <tr style="background: #f1f5f9; font-weight: bold;">
                        <td>GESAMT POTENZIAL</td>
                        <td>Summe der operativen Einsparungen & Opportunitätskosten</td>
                        <td style="text-align:right; color: var(--primary);">€ {monthly_roi:,.0f}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 4. EMPFEHLUNGEN -->
        <div class="section">
            <div class="section-title">4. Strategische Handlungsempfehlungen</div>
            {recommendations_html}
        </div>

        <!-- FOOTER -->
        <div class="report-footer">
            <p><strong>Quellenverzeichnis & Methodik:</strong></p>
            {sources_html}
            
            <div class="disclaimer">
                <p><strong>Disclaimer:</strong> Dieser Bericht wurde automatisiert durch ChatPro AI Analytics erstellt. Die ROI-Berechnungen sind Schätzungen basierend auf öffentlichen Daten und Branchen-Durchschnittswerten. Sie stellen keine garantierte Finanzzusage dar.</p>
                <p>© 2026 ChatPro AI - FITCOACHAI LTD. Vertrauliches Dokument.</p>
            </div>
        </div>
    </div>

</body>
</html>
"""
        return html
