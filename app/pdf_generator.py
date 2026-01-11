"""
ChatPro AI - PDF Report Generator
PRODUCTION-READY VERSION with safe dictionary access
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger("app.pdf_generator")


class PDFReportGenerator:
    """Generate HTML/PDF reports with defensive programming"""
    
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        logger.info("PDFReportGenerator initialized")
    
    def generate(
        self,
        crawler_data: Dict[str, Any],
        analysis_data: Dict[str, Any],
        company_name: str,
        industry: str,
        output_path: str,
        sources: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generate HTML report with safe dictionary access
        
        Args:
            crawler_data: Crawler results (dict)
            analysis_data: AI analysis results (dict)
            company_name: Company name
            industry: Industry type
            output_path: Output file path
            sources: List of source dictionaries
            
        Returns:
            Path to generated HTML file
        """
        # Defensive checks
        if not crawler_data or not isinstance(crawler_data, dict):
            logger.warning(f"Invalid crawler_data: {type(crawler_data)}, using empty dict")
            crawler_data = {}
        
        if not analysis_data or not isinstance(analysis_data, dict):
            logger.warning(f"Invalid analysis_data: {type(analysis_data)}, using empty dict")
            analysis_data = {}
        
        if not sources or not isinstance(sources, list):
            logger.warning(f"Invalid sources: {type(sources)}, using empty list")
            sources = []
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate HTML content
        try:
            html_content = self._generate_html(
                crawler_data=crawler_data,
                analysis_data=analysis_data,
                company_name=company_name,
                industry=industry,
                sources=sources
            )
        except Exception as e:
            logger.error(f"HTML generation failed: {str(e)}")
            raise
        
        # Write to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Report generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to write report file: {str(e)}")
            raise
    
    def _generate_html(
        self,
        crawler_data: Dict[str, Any],
        analysis_data: Dict[str, Any],
        company_name: str,
        industry: str,
        sources: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Generate HTML content with SAFE dictionary access"""
        
        # Defensive defaults
        if sources is None:
            sources = []
        
        # Get today's date
        today = datetime.now().strftime("%d.%m.%Y")
        
        # Industry labels
        industry_labels = {
            "hotel": "Hotel & Unterkunft",
            "restaurant": "Gastronomie",
            "fitness": "Fitness & Wellness",
            "salon": "Beauty & Salon"
        }
        industry_label = industry_labels.get(industry, industry)
        
        # SAFE: Extract data from new OpenAI format
        pain_points = analysis_data.get('pain_points', [])
        if not isinstance(pain_points, list):
            logger.warning(f"pain_points is not a list: {type(pain_points)}")
            pain_points = []
        
        roi_calc = analysis_data.get('roi_calculation', {})
        if not isinstance(roi_calc, dict):
            logger.warning(f"roi_calculation is not a dict: {type(roi_calc)}")
            roi_calc = {}
        
        recommendations = analysis_data.get('recommendations', [])
        if not isinstance(recommendations, list):
            logger.warning(f"recommendations is not a list: {type(recommendations)}")
            recommendations = []
        
        chatbot_priority = analysis_data.get('chatbot_priority', 'MEDIUM')
        
        # SAFE: Fallback for old format with defensive access
        website_check = analysis_data.get('website_check')
        chatbot_analysis = analysis_data.get('chatbot_analysis')
        
        if not website_check:
            # Build from crawler_data with safe defaults
            website_check = {
                'pages': crawler_data.get('page_count', 0),
                'languages': len(crawler_data.get('languages', ['Deutsch'])),
                'mobile_friendly': crawler_data.get('is_mobile_friendly', True)
            }
        
        if not chatbot_analysis:
            chatbot_analysis = {
                'has_chatbot': crawler_data.get('has_chatbot', False),
                'chatbot_type': crawler_data.get('chatbot_type', 'Kein Chatbot'),
                'priority': chatbot_priority
            }
        
        # SAFE: Extract ROI metrics
        monthly_roi = roi_calc.get('monthly_roi', 0)
        roi_multiplier = roi_calc.get('roi_multiplier', 0)
        break_even = roi_calc.get('break_even_months', 0)
        
        # SAFE: Build sources HTML
        sources_html = ""
        if sources and isinstance(sources, list):
            for source in sources:
                if not isinstance(source, dict):
                    logger.warning(f"Skipping invalid source: {type(source)}")
                    continue
                
                source_id = source.get('id', 'N/A')
                title = source.get('title', 'N/A')
                url = source.get('url', '#')
                
                sources_html += f"""
                <div class='source-item'>
                    <strong>[{source_id}] {title}</strong><br>
                    <a href='{url}' target='_blank'>{url}</a>
                </div>
                """
        else:
            sources_html = "<p>Quellen werden geladen...</p>"
        
        # SAFE: Build pain points HTML
        pain_points_html = ""
        for i, point in enumerate(pain_points[:3], 1):  # Max 3
            if not isinstance(point, dict):
                continue
            
            problem = point.get('problem', 'N/A')
            impact = point.get('impact', 'N/A')
            evidence = point.get('evidence', 'N/A')
            
            pain_points_html += f"""
            <div class='pain-point'>
                <h3>{i}. {problem}</h3>
                <p><strong>Impact:</strong> {impact}</p>
                <p><strong>Evidence:</strong> {evidence}</p>
            </div>
            """
        
        # SAFE: Build ROI details HTML
        roi_details_html = ""
        calculations = roi_calc.get('calculations', [])
        if isinstance(calculations, list):
            for calc in calculations:
                if not isinstance(calc, dict):
                    continue
                
                category = calc.get('category', 'N/A')
                monthly_value = calc.get('monthly_value', 0)
                calculation = calc.get('calculation', 'N/A')
                source_ids = calc.get('source_ids', [])
                
                roi_details_html += f"""
                <div class='roi-item'>
                    <h4>{category}</h4>
                    <p><strong>Monatlicher Wert:</strong> €{monthly_value:,.0f}</p>
                    <p><strong>Berechnung:</strong> {calculation}</p>
                    <p><small>Quellen: [{', '.join(source_ids)}]</small></p>
                </div>
                """
        
        # SAFE: Build recommendations HTML
        recommendations_html = ""
        for rec in recommendations[:5]:  # Max 5
            if not isinstance(rec, dict):
                continue
            
            priority = rec.get('priority', 'MEDIUM')
            title = rec.get('title', 'N/A')
            description = rec.get('description', 'N/A')
            impact = rec.get('impact', 'N/A')
            implementation = rec.get('implementation', 'N/A')
            
            priority_class = priority.lower()
            priority_label = {'HIGH': 'Hoch', 'MEDIUM': 'Mittel', 'LOW': 'Niedrig'}.get(priority, priority)
            
            recommendations_html += f"""
            <div class='recommendation priority-{priority_class}'>
                <span class='priority-badge'>{priority_label}</span>
                <h3>{title}</h3>
                <p><strong>Beschreibung:</strong> {description}</p>
                <p><strong>Impact:</strong> {impact}</p>
                <p><strong>Umsetzung:</strong> {implementation}</p>
            </div>
            """
        
        # Build complete HTML (simplified template)
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ChatPro AI Analyse - {company_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .roi-box {{ background: #3498db; color: white; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .pain-point {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #e74c3c; }}
        .recommendation {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #2ecc71; }}
        .priority-high {{ border-color: #e74c3c; }}
        .priority-medium {{ border-color: #f39c12; }}
        .priority-low {{ border-color: #95a5a6; }}
        .source-item {{ margin: 10px 0; padding: 10px; background: #ecf0f1; }}
        .priority-badge {{ background: #3498db; color: white; padding: 5px 10px; border-radius: 5px; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>ChatPro AI Analyse für {company_name}</h1>
    <p><strong>Branche:</strong> {industry_label}</p>
    <p><strong>Datum:</strong> {today}</p>
    
    <div class='roi-box'>
        <h2>ROI-Potenzial</h2>
        <p><strong>Monatliches ROI:</strong> €{monthly_roi:,.0f}</p>
        <p><strong>ROI Multiplier:</strong> {roi_multiplier:.1f}x</p>
        <p><strong>Break Even:</strong> {break_even} Monate</p>
    </div>
    
    <h2>Pain Points</h2>
    {pain_points_html}
    
    <h2>ROI Details</h2>
    {roi_details_html}
    
    <h2>Empfehlungen</h2>
    {recommendations_html}
    
    <h2>Quellenverzeichnis</h2>
    {sources_html}
    
    <footer style='margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; color: #7f8c8d;'>
        <p>Erstellt von ChatPro AI | {today}</p>
    </footer>
</body>
</html>
"""
        
        return html
