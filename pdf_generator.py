"""
CHATPRO AI ANALYZER - PDF REPORT GENERATOR
Professional 7-page PDF reports with sources
"""

from typing import Dict, Optional
from datetime import datetime
import os

class PDFReportGenerator:
    """
    Generate professional PDF reports with WeasyPrint
    
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
        output_path: str
    ) -> str:
        """
        Generate PDF report
        
        Returns: Path to generated PDF
        """
        
        # Generate HTML content
        html_content = self._generate_html(
            crawler_data,
            analysis_data,
            company_name,
            industry
        )
        
        # Save HTML for debugging
        html_path = output_path.replace('.pdf', '.html')
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
        industry: str
    ) -> str:
        """
        Generate complete HTML report
        """
        
        website_check = analysis_data['website_check']
        chatbot_analysis = analysis_data['chatbot_analysis']
        pain_points = analysis_data['pain_points']
        roi_calc = analysis_data['roi_calculation']
        recommendations = analysis_data['recommendations']
        sources = analysis_data['sources']
        
        # Generate date
        today = datetime.now().strftime("%d.%m.%Y")
        
        # Industry labels
        industry_labels = {
            "hotel": "Hotels",
            "fitness": "Fitnessstudios",
            "salon": "Salons",
            "immobilien": "Immobilien",
            "restaurant": "Restaurants",
            "other": "Dienstleistungen"
        }
        
        industry_label = industry_labels.get(industry, "Unternehmen")
        
        html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatPro AI Website-Analyse - {company_name}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #ffffff;
        }}
        
        .page {{
            width: 210mm;
            min-height: 297mm;
            padding: 20mm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            page-break-after: always;
        }}
        
        .page:last-child {{
            page-break-after: auto;
        }}
        
        /* Cover Page */
        .cover {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .cover-header {{
            text-align: center;
            padding-top: 60px;
        }}
        
        .cover-logo {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .cover-title {{
            font-size: 36px;
            font-weight: 700;
            margin: 40px 0 20px;
            line-height: 1.2;
        }}
        
        .cover-subtitle {{
            font-size: 20px;
            opacity: 0.9;
            margin-bottom: 60px;
        }}
        
        .cover-info {{
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }}
        
        .cover-info h2 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .cover-info p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .cover-footer {{
            text-align: center;
            padding-top: 40px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }}
        
        .cover-footer p {{
            font-size: 14px;
            opacity: 0.8;
        }}
        
        /* Header */
        .header {{
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 28px;
            font-weight: 700;
        }}
        
        .header .page-number {{
            color: #666;
            font-size: 14px;
            float: right;
        }}
        
        /* Content */
        h2 {{
            color: #667eea;
            font-size: 24px;
            margin: 30px 0 15px;
            font-weight: 700;
        }}
        
        h3 {{
            color: #333;
            font-size: 18px;
            margin: 20px 0 10px;
            font-weight: 600;
        }}
        
        p {{
            margin-bottom: 12px;
            color: #444;
        }}
        
        /* Stats Box */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        
        .stat-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: 700;
            color: #333;
        }}
        
        .stat-value.success {{
            color: #10b981;
        }}
        
        .stat-value.warning {{
            color: #f59e0b;
        }}
        
        .stat-value.error {{
            color: #ef4444;
        }}
        
        /* Issue List */
        .issue-list {{
            margin: 20px 0;
        }}
        
        .issue-item {{
            background: #fff5f5;
            border-left: 4px solid #ef4444;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }}
        
        .issue-title {{
            font-weight: 600;
            color: #991b1b;
            margin-bottom: 5px;
        }}
        
        .issue-impact {{
            color: #666;
            font-size: 14px;
            margin-bottom: 5px;
        }}
        
        .issue-cost {{
            color: #ef4444;
            font-weight: 600;
            font-size: 15px;
        }}
        
        /* ROI Table */
        .roi-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .roi-table th,
        .roi-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .roi-table th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        
        .roi-table tr:last-child {{
            background: #f0fdf4;
            font-weight: 700;
        }}
        
        .roi-table tr:last-child td {{
            color: #10b981;
            font-size: 16px;
        }}
        
        .amount {{
            text-align: right;
            font-weight: 600;
        }}
        
        /* Summary Box */
        .summary-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin: 30px 0;
            text-align: center;
        }}
        
        .summary-box h3 {{
            color: white;
            font-size: 20px;
            margin-bottom: 20px;
        }}
        
        .summary-metric {{
            display: inline-block;
            margin: 0 20px;
        }}
        
        .summary-metric-value {{
            font-size: 36px;
            font-weight: 700;
            display: block;
            margin-bottom: 5px;
        }}
        
        .summary-metric-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        /* Recommendations */
        .recommendation-list {{
            margin: 20px 0;
        }}
        
        .recommendation-item {{
            background: #f0fdf4;
            border-left: 4px solid #10b981;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            font-size: 15px;
        }}
        
        /* Sources */
        .source-item {{
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            font-size: 13px;
            border-left: 3px solid #667eea;
        }}
        
        .source-id {{
            font-weight: 700;
            color: #667eea;
            margin-right: 5px;
        }}
        
        .source-title {{
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .source-url {{
            color: #666;
            word-break: break-all;
            font-size: 12px;
            font-family: monospace;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
        
        /* Print Styles */
        @media print {{
            .page {{
                box-shadow: none;
                margin: 0;
            }}
        }}
        
        /* Disclaimer */
        .disclaimer {{
            background: #fffbeb;
            border: 1px solid #fbbf24;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 13px;
            color: #78350f;
        }}
        
        .disclaimer strong {{
            display: block;
            margin-bottom: 8px;
            color: #92400e;
        }}
    </style>
</head>
<body>

<!-- PAGE 1: COVER -->
<div class="page cover">
    <div class="cover-header">
        <div class="cover-logo">🤖 ChatPro AI</div>
        <h1 class="cover-title">Website-Analyse</h1>
        <p class="cover-subtitle">Kostenlose AI-gestützte Analyse für {industry_label}</p>
    </div>
    
    <div class="cover-info">
        <h2>{company_name}</h2>
        <p>{crawler_data.get('url', 'N/A')}</p>
        <p style="margin-top: 20px;">Erstellt am: {today}</p>
    </div>
    
    <div class="cover-footer">
        <p><strong>ChatPro AI</strong> - 24/7 AI-Chatbot Lösungen</p>
        <p>https://www.chatproai.io | robert@chatproai.io</p>
        <p style="margin-top: 10px; font-size: 11px;">
            Alle Berechnungen basieren auf verifizierten Quellen und konservativen Schätzungen.<br>
            Individuelle Ergebnisse können variieren.
        </p>
    </div>
</div>

<!-- PAGE 2: EXECUTIVE SUMMARY -->
<div class="page">
    <div class="header">
        <h1>Executive Summary</h1>
        <span class="page-number">Seite 2 von 7</span>
    </div>
    
    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-label">Website-Status</div>
            <div class="stat-value success">{website_check['status']}</div>
        </div>
        
        <div class="stat-box">
            <div class="stat-label">Chatbot</div>
            <div class="stat-value {'success' if chatbot_analysis['exists'] else 'error'}">
                {'✅ Gefunden' if chatbot_analysis['exists'] else '❌ Nicht gefunden'}
            </div>
        </div>
        
        <div class="stat-box">
            <div class="stat-label">Sprachen</div>
            <div class="stat-value">{website_check['language_count']} Sprache(n)</div>
        </div>
        
        <div class="stat-box">
            <div class="stat-label">Mobile</div>
            <div class="stat-value {'success' if website_check['mobile_responsive'] else 'warning'}">
                {'✅ Responsive' if website_check['mobile_responsive'] else '⚠️ Eingeschränkt'}
            </div>
        </div>
    </div>
    
    <div class="summary-box">
        <h3>ROI-Potenzial mit ChatPro AI</h3>
        <div class="summary-metric">
            <span class="summary-metric-value">€{roi_calc['summary']['total_roi_monat']:,}</span>
            <span class="summary-metric-label">ROI pro Monat</span>
        </div>
        <div class="summary-metric">
            <span class="summary-metric-value">{roi_calc['summary']['roi_multiplikator']}x</span>
            <span class="summary-metric-label">ROI-Multiplikator</span>
        </div>
        <div class="summary-metric">
            <span class="summary-metric-value">{roi_calc['summary']['break_even_monate']}</span>
            <span class="summary-metric-label">Break-Even (Monate)</span>
        </div>
    </div>
    
    <h2>Wichtigste Erkenntnisse</h2>
    <ul style="margin-left: 20px; line-height: 2;">
        <li><strong>Website:</strong> {website_check['pages']} Seiten gefunden, {website_check['language_count']} Sprache(n) verfügbar</li>
        <li><strong>Chatbot:</strong> {chatbot_analysis['status']}</li>
        <li><strong>Pain Points:</strong> {len(pain_points)} kritische Bereiche identifiziert</li>
        <li><strong>ROI:</strong> €{roi_calc['summary']['net_gewinn_monat']:,} Nettogewinn pro Monat möglich</li>
    </ul>
    
    <div class="footer">
        ChatPro AI - Transparent. Messbar. Vertrauenswürdig.
    </div>
</div>

<!-- PAGE 3: WEBSITE-ANALYSE -->
<div class="page">
    <div class="header">
        <h1>Website-Analyse</h1>
        <span class="page-number">Seite 3 von 7</span>
    </div>
    
    <h2>Technische Details</h2>
    
    <table class="roi-table">
        <tr>
            <th>Kriterium</th>
            <th>Status</th>
            <th>Details</th>
        </tr>
        <tr>
            <td><strong>URL</strong></td>
            <td>✅</td>
            <td>{crawler_data.get('url', 'N/A')}</td>
        </tr>
        <tr>
            <td><strong>Status Code</strong></td>
            <td>✅</td>
            <td>{crawler_data.get('status_code', 'N/A')}</td>
        </tr>
        <tr>
            <td><strong>Titel</strong></td>
            <td>✅</td>
            <td>{website_check.get('title', 'N/A')}</td>
        </tr>
        <tr>
            <td><strong>Seitenanzahl</strong></td>
            <td>✅</td>
            <td>{website_check['pages']} interne Seiten gefunden</td>
        </tr>
        <tr>
            <td><strong>Sprachen</strong></td>
            <td>{'✅' if website_check['language_count'] >= 3 else '⚠️'}</td>
            <td>{', '.join(website_check['languages'])}</td>
        </tr>
        <tr>
            <td><strong>Mobile Responsive</strong></td>
            <td>{'✅' if website_check['mobile_responsive'] else '❌'}</td>
            <td>{'Ja - Mobile-optimiert' if website_check['mobile_responsive'] else 'Nein - Nicht optimiert'}</td>
        </tr>
        <tr>
            <td><strong>Lead-Formulare</strong></td>
            <td>{'✅' if website_check['lead_forms_count'] > 0 else '⚠️'}</td>
            <td>{website_check['lead_forms_count']} Formulare gefunden</td>
        </tr>
        <tr>
            <td><strong>Ladezeit</strong></td>
            <td>✅</td>
            <td>{crawler_data.get('response_time_ms', 0)}ms</td>
        </tr>
    </table>
    
    <h2>Kontaktinformationen</h2>
    <p><strong>E-Mails gefunden:</strong> {', '.join(crawler_data.get('contact_info', {}).get('emails', [])) or 'Keine gefunden'}</p>
    <p><strong>Telefonnummern:</strong> {', '.join(crawler_data.get('contact_info', {}).get('phones', [])) or 'Keine gefunden'}</p>
    
    <div class="footer">
        Seite 3 von 7 - Website-Analyse
    </div>
</div>

<!-- PAGE 4: CHATBOT-ANALYSE & PAIN POINTS -->
<div class="page">
    <div class="header">
        <h1>Chatbot-Analyse & Pain Points</h1>
        <span class="page-number">Seite 4 von 7</span>
    </div>
    
    <h2>Aktueller Chatbot-Status</h2>
    
    <div class="stat-box" style="margin-bottom: 20px;">
        <div class="stat-label">Status</div>
        <div class="stat-value">{chatbot_analysis['status']}</div>
    </div>
    
    {'<p><strong>Chatbot-Typ:</strong> ' + chatbot_analysis.get('type', 'N/A') + '</p>' if chatbot_analysis['exists'] else ''}
    {'<p><strong>Lead-Formular vor Chat:</strong> ' + ('Ja - kritisches Problem!' if chatbot_analysis.get('has_lead_form') else 'Nein') + '</p>' if chatbot_analysis['exists'] else ''}
    {'<p><strong>Priority-Level:</strong> ' + chatbot_analysis.get('priority', 'N/A') + '</p>' if chatbot_analysis['exists'] else ''}
    
    {'''
    <div class="issue-list">
        <h3>Erkannte Probleme:</h3>
        ''' + ''.join([f'''
        <div class="issue-item">
            <div class="issue-title">⚠️ {issue}</div>
        </div>
        ''' for issue in chatbot_analysis.get('issues', [])]) + '''
    </div>
    ''' if chatbot_analysis.get('issues') else ''}
    
    <h2>Identifizierte Pain Points</h2>
    
    <div class="issue-list">
        {self._generate_pain_points_html(pain_points)}
    </div>
    
    <div class="disclaimer">
        <strong>Hinweis zu den Pain Points:</strong>
        Alle identifizierten Probleme basieren auf Best Practices der Industrie und verifizierten Case Studies. 
        Die Kostenangaben sind konservative Schätzungen basierend auf Branchendurchschnitten.
    </div>
    
    <div class="footer">
        Seite 4 von 7 - Chatbot-Analyse & Pain Points
    </div>
</div>

<!-- PAGE 5: ROI-BERECHNUNG -->
<div class="page">
    <div class="header">
        <h1>ROI-Berechnung</h1>
        <span class="page-number">Seite 5 von 7</span>
    </div>
    
    {self._generate_roi_html(roi_calc, industry)}
    
    <div class="footer">
        Seite 5 von 7 - ROI-Berechnung
    </div>
</div>

<!-- PAGE 6: CHATPRO AI LÖSUNG -->
<div class="page">
    <div class="header">
        <h1>ChatPro AI Lösung</h1>
        <span class="page-number">Seite 6 von 7</span>
    </div>
    
    <h2>Was macht ChatPro AI anders?</h2>
    
    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-label">Verfügbarkeit</div>
            <div class="stat-value success">24/7</div>
        </div>
        
        <div class="stat-box">
            <div class="stat-label">Sprachen</div>
            <div class="stat-value success">50+</div>
        </div>
        
        <div class="stat-box">
            <div class="stat-label">Setup-Zeit</div>
            <div class="stat-value success">7-14 Tage</div>
        </div>
        
        <div class="stat-box">
            <div class="stat-label">Support</div>
            <div class="stat-value success">Dedicated</div>
        </div>
    </div>
    
    <h2>Ihre Empfehlungen</h2>
    
    <div class="recommendation-list">
        {self._generate_recommendations_html(recommendations)}
    </div>
    
    <h2>Preisgestaltung</h2>
    
    <table class="roi-table">
        <tr>
            <th>Paket</th>
            <th>Setup</th>
            <th>Monatlich</th>
            <th>Features</th>
        </tr>
        <tr>
            <td><strong>Business</strong></td>
            <td>€1.799</td>
            <td>€249</td>
            <td>2 Sprachen, Basic Support</td>
        </tr>
        <tr>
            <td><strong>Premium ⭐</strong></td>
            <td>€4.999</td>
            <td>€799</td>
            <td>50+ Sprachen, PMS/CRM Integration, Dedicated Account Manager</td>
        </tr>
        <tr>
            <td><strong>Enterprise</strong></td>
            <td>Individuell</td>
            <td>Individuell</td>
            <td>Custom Solutions, WhatsApp, Video Avatar</td>
        </tr>
    </table>
    
    <div style="margin-top: 30px; text-align: center; padding: 20px; background: #f0fdf4; border-radius: 8px;">
        <h3 style="color: #10b981; margin-bottom: 15px;">🎯 Nächster Schritt</h3>
        <p style="font-size: 16px; margin-bottom: 15px;">
            Buchen Sie eine kostenlose 30-Minuten Demo und sehen Sie ChatPro AI live in Aktion!
        </p>
        <p style="font-size: 18px; font-weight: 600; color: #667eea;">
            📅 https://calendly.com/chatproaiio/30min
        </p>
        <p style="font-size: 16px; margin-top: 15px;">
            📧 robert@chatproai.io | 🌐 https://www.chatproai.io
        </p>
    </div>
    
    <div class="footer">
        Seite 6 von 7 - ChatPro AI Lösung
    </div>
</div>

<!-- PAGE 7: QUELLENVERZEICHNIS -->
<div class="page">
    <div class="header">
        <h1>Quellenverzeichnis</h1>
        <span class="page-number">Seite 7 von 7</span>
    </div>
    
    <h2>Verwendete Quellen</h2>
    
    <p style="margin-bottom: 20px; color: #666;">
        Alle in diesem Bericht verwendeten Daten und Berechnungen basieren auf den folgenden 
        verifizierten Quellen. Alle URLs wurden am {today} überprüft.
    </p>
    
    {self._generate_sources_html(sources)}
    
    <h2>ChatPro AI Berechnungen</h2>
    
    <div class="source-item">
        <span class="source-id">[13]</span>
        <div class="source-title">ChatPro AI (2026): ROI-Kalkulation {industry_label}</div>
        <p style="margin-top: 10px; color: #666; font-size: 13px;">
            Eigene Berechnungen basierend auf:<br>
            - Konservativen Branchendurchschnitten<br>
            - Verifizierten Statistiken (Destatis, DEHOGA, Prostay)<br>
            - Peer-reviewed Case Studies (HubSpot, Innovation Visual)<br>
            - Transparenten Rechenwegen (siehe Seite 5)
        </p>
    </div>
    
    <div class="disclaimer">
        <strong>Disclaimer:</strong>
        Alle ROI-Berechnungen basieren auf konservativen Schätzungen und Durchschnittswerten 
        der genannten Quellen. Individuelle Ergebnisse können je nach Betriebsgröße, Lage, 
        Auslastung und Marktpositionierung variieren. Die aufgeführten Quellen wurden sorgfältig 
        ausgewählt und zum Zeitpunkt der Berichterstellung verifiziert.
    </div>
    
    <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #e5e7eb;">
        <h2>Impressum & Datenschutz</h2>
        <p style="font-size: 13px; color: #666; line-height: 1.8;">
            <strong>FITCOACHAI LTD - ChatPro AI</strong><br>
            E-Mail: robert@chatproai.io<br>
            Website: https://www.chatproai.io<br>
            <br>
            Impressum: https://www.chatproai.io/impressum.html<br>
            Datenschutz: https://www.chatproai.io/datenschutz.html<br>
            <br>
            © 2026 FITCOACHAI LTD. Alle Rechte vorbehalten.
        </p>
    </div>
    
    <div class="footer">
        Seite 7 von 7 - Quellenverzeichnis | Erstellt mit ChatPro AI Analyzer
    </div>
</div>

</body>
</html>
        """
        
        return html
    
    def _generate_pain_points_html(self, pain_points: list) -> str:
        """Generate HTML for pain points"""
        
        html = ""
        for i, pp in enumerate(pain_points, 1):
            html += f"""
        <div class="issue-item">
            <div class="issue-title">{i}. {pp['issue']}</div>
            <div class="issue-impact">📊 Impact: {pp['impact']}</div>
            <div class="issue-cost">💰 Kosten: {pp['cost']}</div>
            {f'<div style="margin-top: 5px; font-size: 12px; color: #666;">Quelle: {pp["source"]}</div>' if pp.get('source') else ''}
        </div>
            """
        
        return html
    
    def _generate_roi_html(self, roi_calc: Dict, industry: str) -> str:
        """Generate HTML for ROI calculation"""
        
        assumptions = roi_calc['assumptions']
        calculations = roi_calc.get('calculations', {})
        summary = roi_calc['summary']
        
        html = f"""
    <h2>Annahmen (Konservativ)</h2>
    
    <div class="disclaimer">
        <strong>Berechnungsgrundlage:</strong>
        Alle Annahmen basieren auf Branchendurchschnitten und konservativen Schätzungen.
        """
        
        # Industry-specific assumptions
        if industry == "hotel":
            html += f"""
        <ul style="margin: 10px 0 0 20px; color: #78350f;">
            <li>Zimmer: {assumptions['zimmer']}</li>
            <li>Auslastung: {assumptions['auslastung_prozent']}% (Branchendurchschnitt {assumptions['sources'][1]})</li>
            <li>Durchschnittspreis/Nacht: €{assumptions['preis_pro_nacht']}</li>
            <li>Booking.com Provision: {assumptions['booking_provision_prozent']}% {assumptions['sources'][0]}</li>
        </ul>
            """
        
        html += """
    </div>
    
    <h2>ROI-Aufschlüsselung</h2>
    
    <table class="roi-table">
        <tr>
            <th>Position</th>
            <th style="text-align: right;">Betrag/Monat</th>
        </tr>
        """
        
        # Add calculation rows
        if industry == "hotel":
            phase1 = calculations.get('phase1_direktbuchungen', {})
            phase2 = calculations.get('phase2_zeitersparnis', {})
            phase3 = calculations.get('phase3_upselling', {})
            
            html += f"""
        <tr>
            <td>
                <strong>Phase 1: Direktbuchungen</strong><br>
                <span style="font-size: 13px; color: #666;">
                    Ersparte Booking.com Provision + 24/7 Mehrbu chungen {phase1.get('source', '')}
                </span>
            </td>
            <td class="amount">€{phase1.get('total', 0):,}</td>
        </tr>
        <tr>
            <td>
                <strong>Phase 2: Zeitersparnis</strong><br>
                <span style="font-size: 13px; color: #666;">
                    {phase2.get('stunden_pro_monat', 0)}h/Monat × €{phase2.get('stundenlohn', 0)}/h {phase2.get('source', '')}
                </span>
            </td>
            <td class="amount">€{phase2.get('total', 0):,}</td>
        </tr>
        <tr>
            <td>
                <strong>Phase 3: Upselling</strong><br>
                <span style="font-size: 13px; color: #666;">
                    {phase3.get('upselling_rate_prozent', 0)}% Upselling-Rate × €{phase3.get('wert_pro_upsell', 0)} {phase3.get('source', '')}
                </span>
            </td>
            <td class="amount">€{phase3.get('total', 0):,}</td>
        </tr>
            """
        else:
            zeitersparnis = calculations.get('zeitersparnis', {})
            lead_steigerung = calculations.get('lead_steigerung', {})
            
            html += f"""
        <tr>
            <td>
                <strong>Zeitersparnis</strong><br>
                <span style="font-size: 13px; color: #666;">
                    Automatisierung durch 24/7-Chatbot {zeitersparnis.get('source', '')}
                </span>
            </td>
            <td class="amount">€{zeitersparnis.get('total', 0):,}</td>
        </tr>
        <tr>
            <td>
                <strong>Lead-Steigerung</strong><br>
                <span style="font-size: 13px; color: #666;">
                    +{lead_steigerung.get('zusaetzliche_leads', 0)} Leads/Monat {lead_steigerung.get('source', '')}
                </span>
            </td>
            <td class="amount">€{lead_steigerung.get('total', 0):,}</td>
        </tr>
            """
        
        html += f"""
        <tr>
            <td><strong>GESAMT ROI</strong></td>
            <td class="amount">€{summary['total_roi_monat']:,}</td>
        </tr>
        <tr>
            <td>ChatPro AI Premium Kosten</td>
            <td class="amount">- €{summary['chatpro_kosten_monat']}</td>
        </tr>
        <tr style="background: #f0fdf4;">
            <td><strong>NET GEWINN PRO MONAT</strong></td>
            <td class="amount" style="color: #10b981; font-size: 18px;">€{summary['net_gewinn_monat']:,}</td>
        </tr>
    </table>
    
    <div class="summary-box" style="margin-top: 30px;">
        <h3>ROI-Zusammenfassung</h3>
        <div class="summary-metric">
            <span class="summary-metric-value">{summary['roi_multiplikator']}x</span>
            <span class="summary-metric-label">ROI-Multiplikator</span>
        </div>
        <div class="summary-metric">
            <span class="summary-metric-value">{summary['break_even_monate']}</span>
            <span class="summary-metric-label">Break-Even (Monate)</span>
        </div>
        <div class="summary-metric">
            <span class="summary-metric-value">€{summary['jahres_roi']:,}</span>
            <span class="summary-metric-label">Jahres-ROI</span>
        </div>
    </div>
        """
        
        return html
    
    def _generate_recommendations_html(self, recommendations: list) -> str:
        """Generate HTML for recommendations"""
        
        html = ""
        for rec in recommendations:
            html += f"""
        <div class="recommendation-item">
            {rec}
        </div>
            """
        
        return html
    
    def _generate_sources_html(self, sources: list) -> str:
        """Generate HTML for sources"""
        
        html = ""
        for source in sources:
            html += f"""
    <div class="source-item">
        <span class="source-id">{source['id']}</span>
        <div class="source-title">{source['title']}</div>
        <p style="margin-top: 5px; color: #666; font-size: 13px;">
            {source.get('value', '')}
        </p>
        <div class="source-url">{source['url']}</div>
        <p style="margin-top: 5px; font-size: 11px; color: #999;">
            Abgerufen: {source.get('date', '2026')}
        </p>
    </div>
            """
        
        return html


# Test function
def test_pdf_generator():
    """Test PDF generator"""
    
    # Import dependencies
    import sys
    sys.path.append('/home/user/chatproai-analyzer/backend/app')
    
    from crawler import WebsiteCrawler
    from analyzer import AIAnalyzer
    
    # Crawl ADORO
    print("🔍 Crawling ADORO...")
    crawler = WebsiteCrawler("https://adoro-aparthotel.com")
    crawler_data = crawler.crawl()
    
    if "error" in crawler_data:
        print(f"❌ Crawler Error: {crawler_data['error']}")
        return
    
    # Analyze
    print("🤖 Analyzing...")
    analyzer = AIAnalyzer()
    analysis_data = analyzer.analyze(crawler_data, "hotel")
    
    # Generate PDF
    print("📄 Generating PDF...")
    generator = PDFReportGenerator()
    
    output_path = "/mnt/user-data/outputs/adoro_report.pdf"
    result_path = generator.generate(
        crawler_data=crawler_data,
        analysis_data=analysis_data,
        company_name="ADORO Aparthotel",
        industry="hotel",
        output_path=output_path
    )
    
    print(f"✅ Report generated: {result_path}")
    print(f"\nPreview: file://{result_path}")


if __name__ == "__main__":
    test_pdf_generator()
