"""
CHATPRO AI ANALYZER - PDF REPORT GENERATOR
Professional 7-page HTML reports with sources
"""

from typing import Dict, List, Optional
from datetime import datetime
import os

class PDFReportGenerator:

    """
    Generate professional HTML reports
    
    7-Page Structure:
    1. Executive Summary
    2. Website-Analyse
    3. Chatbot-Analyse
    4. Pain Points
    5. ROI-Berechnung
    6. ChatPro AI Lösung
    7. Quellenverzeichnis
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
        """
        Generate HTML report
        
        Returns: Path to generated HTML report
        """
        
        # Generate HTML content
        html_content = self._generate_html(
            crawler_data,
            analysis_data,
            company_name,
            industry,
            sources or []
        )
        
        # Save HTML for debugging
        html_path = output_path
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # For now, return HTML path (will implement PDF conversion later)
        # WeasyPrint requires specific system dependencies
        return html_path
    
    def _generate_html(
        self,
        crawler_data: Dict,
        analysis_data: Dict,
        company_name: str,
        industry: str,
        sources: List[Dict] = None
    ) -> str:
        """
        Generate complete HTML report
        """
        
        # Extract data from new OpenAI format
        pain_points = analysis_data.get('pain_points', [])
        roi_calc = analysis_data.get('roi_calculation', {})
        recommendations = analysis_data.get('recommendations', [])
        chatbot_priority = analysis_data.get('chatbot_priority', 'MEDIUM')
        
        # Fallback for old format
        if 'website_check' in analysis_data:
            website_check = analysis_data['website_check']
            chatbot_analysis = analysis_data['chatbot_analysis']
        else:
            # New OpenAI format
            website_check = {
                'pages': crawler_data.get('page_count', 0),
                'languages': len(crawler_data.get('languages', ['Deutsch'])),
                'mobile_friendly': crawler_data.get('is_mobile_friendly', True)
            }
            chatbot_analysis = {
                'has_chatbot': crawler_data.get('has_chatbot', False),
                'chatbot_type': crawler_data.get('chatbot_type', 'Kein Chatbot'),
                'priority': chatbot_priority
            }
        
        # Generate date
        today = datetime.now().strftime("%d.%m.%Y")
        
        # Industry labels
        industry_labels = {
            "hotel": "Hotels",
            "restaurant": "Restaurants & Cafés",
            "fitness": "Fitnessstudios",
            "salon": "Friseursalons & Beauty",
            "immobilien": "Immobilienmakler",
            "ecommerce": "E-Commerce",
            "anwalt": "Rechtsanwälte",
            "steuerberater": "Steuerberater",
            "versicherung": "Versicherungsagenturen",
            "arzt": "Arztpraxen"
        }
        industry_label = industry_labels.get(industry.lower(), industry)
        
        # Calculate summary metrics from new format
        monthly_roi = roi_calc.get('monthly_roi', 0)
        roi_multiplier = roi_calc.get('roi_multiplier', 0)
        break_even = roi_calc.get('break_even_months', 0)
        
        # Build sources HTML
        sources_html = ""
                if sources:
            for source in sources:
                source_id = source.get('id', 'N/A')
                title = source.get('title', 'N/A')
                url = source.get('url', '#')
                sources_html += f"""
                <div class="source-item">
                    <strong>[{source_id}] {title}</strong><br>
                    <a href="{url}" target="_blank">{url}</a>
                </div>
                """

        else:
            sources_html = "<p>Quellen werden geladen...</p>"
        
        # Build pain points HTML
        pain_points_html = ""
        for i, pp in enumerate(pain_points[:3], 1):
            pain_points_html += f"""
            <div class="pain-point">
                <h3>{i}. {pp.get('problem', 'N/A')}</h3>
                <p><strong>Impact:</strong> {pp.get('impact', 'N/A')}</p>
                <p><strong>Evidence:</strong> {pp.get('evidence', 'N/A')}</p>
            </div>
            """
        
        # Build ROI calculations HTML
        roi_details_html = ""
        for calc in roi_calc.get('calculations', []):
            roi_details_html += f"""
            <div class="roi-detail">
                <h3>{calc.get('category', 'N/A')}</h3>
                <p class="roi-value">€{calc.get('monthly_value', 0):,.0f}/Monat</p>
                <p>{calc.get('calculation', 'N/A')}</p>
                <p class="source-ref">Quellen: {', '.join(['[' + s + ']' for s in calc.get('source_ids', [])])}</p>
            </div>
            """
        
        # Build recommendations HTML
        recommendations_html = ""
        for rec in recommendations[:5]:
            priority_class = rec.get('priority', 'MEDIUM').lower()
            recommendations_html += f"""
            <div class="recommendation priority-{priority_class}">
                <h3><span class="priority-badge">{rec.get('priority', 'MEDIUM')}</span> {rec.get('title', 'N/A')}</h3>
                <p>{rec.get('description', 'N/A')}</p>
                <p><strong>Impact:</strong> {rec.get('impact', 'N/A')}</p>
                <p><strong>Implementation:</strong> {rec.get('implementation', 'N/A')}</p>
            </div>
            """
        
        # Complete HTML template
        html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatPro AI - Website-Analyse für {company_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            border-radius: 20px;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        }}
        
        .header h1 {{
            font-size: 42px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 20px;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .header .meta {{
            font-size: 14px;
            opacity: 0.8;
        }}
        
        .roi-box {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(245, 87, 108, 0.3);
        }}
        
        .roi-box h2 {{
            font-size: 18px;
            margin-bottom: 10px;
            opacity: 0.9;
            font-weight: 500;
        }}
        
        .roi-box .roi-amount {{
            font-size: 56px;
            font-weight: 700;
            margin: 20px 0;
        }}
        
        .roi-box .roi-stats {{
            display: flex;
            justify-content: space-around;
            margin-top: 30px;
        }}
        
        .roi-box .stat {{
            flex: 1;
        }}
        
        .roi-box .stat-value {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .roi-box .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .section {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
        }}
        
        .section h2 {{
            font-size: 28px;
            margin-bottom: 25px;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .website-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        
        .stat-card .value {{
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            font-size: 14px;
            color: #666;
        }}
        
        .chatbot-alert {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .chatbot-alert.success {{
            background: #d4edda;
            border-left-color: #28a745;
        }}
        
        .pain-point {{
            background: #fff5f5;
            border-left: 4px solid #f5576c;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }}
        
        .pain-point h3 {{
            color: #f5576c;
            margin-bottom: 10px;
        }}
        
        .roi-detail {{
            background: #f0f7ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }}
        
        .roi-detail h3 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .roi-detail .roi-value {{
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
            margin: 10px 0;
        }}
        
        .source-ref {{
            font-size: 12px;
            color: #666;
            margin-top: 10px;
            font-style: italic;
        }}
        
        .recommendation {{
            background: white;
            border: 2px solid #e0e0e0;
            padding: 20px;
            margin: 20px 0;
            border-radius: 12px;
        }}
        
        .recommendation.priority-high {{
            border-color: #f5576c;
            background: #fff5f5;
        }}
        
        .recommendation.priority-medium {{
            border-color: #ffc107;
            background: #fff8e1;
        }}
        
        .recommendation.priority-low {{
            border-color: #28a745;
            background: #f0fff4;
        }}
        
        .priority-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            margin-right: 10px;
        }}
        
        .recommendation.priority-high .priority-badge {{
            background: #f5576c;
            color: white;
        }}
        
        .recommendation.priority-medium .priority-badge {{
            background: #ffc107;
            color: white;
        }}
        
        .recommendation.priority-low .priority-badge {{
            background: #28a745;
            color: white;
        }}
        
        .cta-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px;
            border-radius: 20px;
            text-align: center;
            margin-top: 40px;
        }}
        
        .cta-box h2 {{
            font-size: 32px;
            margin-bottom: 20px;
        }}
        
        .cta-box p {{
            font-size: 18px;
            margin-bottom: 30px;
            opacity: 0.9;
        }}
        
        .cta-box .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
            text-align: left;
        }}
        
        .cta-box .feature {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
        }}
        
        .cta-box .contact {{
            margin-top: 30px;
            font-size: 16px;
        }}
        
        .source-item {{
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 14px;
        }}
        
        .source-item a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .source-item a:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>Website-Analyse Report</h1>
            <div class="subtitle">{company_name}</div>
            <div class="meta">
                Branche: {industry_label} | Erstellt am: {today} | Powered by ChatPro AI
            </div>
        </div>
        
        <!-- ROI BOX -->
        <div class="roi-box">
            <h2>Ihr monatliches ROI-Potenzial</h2>
            <div class="roi-amount">€{monthly_roi:,.0f}</div>
            <p>Durch ChatPro AI Chatbot-Implementation</p>
            <div class="roi-stats">
                <div class="stat">
                    <div class="stat-value">{roi_multiplier:.1f}x</div>
                    <div class="stat-label">ROI-Multiplikator</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{break_even:.1f}</div>
                    <div class="stat-label">Monate Break-Even</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{chatbot_priority}</div>
                    <div class="stat-label">Priorität</div>
                </div>
            </div>
        </div>
        
        <!-- WEBSITE CHECK -->
        <div class="section">
            <h2>1. Website-Check</h2>
            <div class="website-stats">
                <div class="stat-card">
                    <div class="value">{website_check.get('pages', 0)}</div>
                    <div class="label">Seiten</div>
                </div>
                <div class="stat-card">
                    <div class="value">{website_check.get('languages', 1)}</div>
                    <div class="label">Sprachen</div>
                </div>
                <div class="stat-card">
                    <div class="value">{'✓' if website_check.get('mobile_friendly', True) else '✗'}</div>
                    <div class="label">Mobile-Optimiert</div>
                </div>
            </div>
        </div>
        
        <!-- CHATBOT ANALYSIS -->
        <div class="section">
            <h2>2. Chatbot-Analyse</h2>
            <div class="chatbot-alert {'success' if not chatbot_analysis.get('has_chatbot') else ''}">
                <h3>Status: {chatbot_analysis.get('chatbot_type', 'Kein Chatbot erkannt')}</h3>
                <p>
                    {
                        'Ihre Website hat aktuell keinen Chatbot. Das bedeutet, dass alle Anfragen manuell bearbeitet werden müssen.' 
                        if not chatbot_analysis.get('has_chatbot') 
                        else f"Ihr aktueller Chatbot ({chatbot_analysis.get('chatbot_type')}) könnte durch eine moderne KI-Lösung ersetzt werden."
                    }
                </p>
            </div>
        </div>
        
        <!-- PAIN POINTS -->
        <div class="section">
            <h2>3. Identifizierte Pain Points</h2>
            {pain_points_html}
        </div>
        
        <!-- ROI CALCULATION -->
        <div class="section">
            <h2>4. ROI-Berechnung</h2>
            <p>Basierend auf verifizierten Quellen und Branchenbenchmarks:</p>
            {roi_details_html}
        </div>
        
        <!-- RECOMMENDATIONS -->
        <div class="section">
            <h2>5. Empfehlungen</h2>
            {recommendations_html}
        </div>
        
        <!-- CTA -->
        <div class="cta-box">
            <h2>Bereit für ChatPro AI?</h2>
            <p>Starten Sie noch heute mit Ihrer KI-Chatbot-Lösung</p>
            <div class="features">
                <div class="feature">
                    <strong>✓ 95%+ Automatisierung</strong><br>
                    Entlasten Sie Ihr Team
                </div>
                <div class="feature">
                    <strong>✓ 24/7 Verfügbarkeit</strong><br>
                    Keine Anfrage bleibt unbeantwortet
                </div>
                <div class="feature">
                    <strong>✓ 50+ Sprachen</strong><br>
                    Internationale Gäste betreuen
                </div>
                <div class="feature">
                    <strong>✓ DSGVO-konform</strong><br>
                    EU-Server & ISO 27001
                </div>
            </div>
            <div class="contact">
                <strong>Kostenlose Demo buchen:</strong><br>
                📧 robert@chatproai.io<br>
                📞 +49 322 126 190 99<br>
                🌐 <a href="https://www.chatproai.io" style="color: white;">www.chatproai.io</a>
            </div>
        </div>
        
        <!-- SOURCES -->
        <div class="section">
            <h2>6. Quellenverzeichnis</h2>
            <p>Alle ROI-Berechnungen basieren auf folgenden verifizierten Quellen:</p>
            {sources_html}
        </div>
        
        <!-- FOOTER -->
        <div class="footer">
            <p>© 2026 ChatPro AI - FITCOACHAI LTD | Alle Rechte vorbehalten</p>
            <p style="margin-top: 10px;">
                <a href="https://www.chatproai.io/impressum" style="color: #667eea;">Impressum</a> | 
                <a href="https://www.chatproai.io/datenschutz" style="color: #667eea;">Datenschutz</a> | 
                <a href="https://www.chatproai.io/agb" style="color: #667eea;">AGB</a>
            </p>
        </div>
    </div>
</body>
</html>
"""
        return html
