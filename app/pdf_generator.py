"""
ChatPro AI V3.1 - Modern PDF Report Generator with Transparency Features
Author: ChatPro Team
Version: 3.1-FIXED (Robust Nested Data Access)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ChatProPDFGenerator:
    """
    Modern PDF Report Generator with Transparency Features
    
    V3.1 Features:
    - Section 2.1: Analysierte Website-Daten (Crawler Summary)
    - Section 3.1: Methodik & Datenquellen
    - Robust nested data access with .get() fallbacks
    - Package badge design
    - Quality score visualization
    """
    
    def __init__(self):
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection header style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=16
        ))
        
        # Highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2980b9'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, analysis_data: dict, output_filename: str):
        """
        Generate PDF report from analysis data.
        
        Args:
            analysis_data: Dictionary with nested structure from analyzer.py
            output_filename: Output PDF file path
        """
        logger.info(f"Generating PDF report: {output_filename}")
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Build content
        story = []
        
        # Cover page
        story.extend(self._create_cover_page(analysis_data))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._create_executive_summary(analysis_data))
        story.append(PageBreak())
        
        # Section 1: Aktuelle Situation (with 2.1 Crawler Summary)
        story.extend(self._create_current_situation(analysis_data))
        
        # Section 2: ChatPro AI Lösung
        story.extend(self._create_solution_section(analysis_data))
        story.append(PageBreak())
        
        # Section 3: ROI & Implementation (with 3.1 Methodology)
        story.extend(self._create_roi_implementation(analysis_data))
        
        # Build PDF
        doc.build(story)
        logger.info(f"✅ PDF report generated successfully: {output_filename}")
    
    def _safe_get(self, data: dict, *keys, default='N/A'):
        """
        Safely navigate nested dictionary structures.
        
        Args:
            data: Dictionary to navigate
            *keys: Sequence of keys to traverse
            default: Default value if key not found
        
        Returns:
            Value at nested key path or default
        """
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
                if current is None:
                    return default
            else:
                return default
        return current if current is not None else default
    
    def _create_cover_page(self, data: dict):
        """Create modern cover page with package badge"""
        elements = []
        
        # Add spacing from top
        elements.append(Spacer(1, 3*cm))
        
        # Main title
        title = Paragraph("ChatPro AI Business Analyse", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # Company name - ROBUST ACCESS
        company_name = self._safe_get(data, 'company_overview', 'company_name', default='Ihr Unternehmen')
        subtitle = Paragraph(f"Erstellt für: <b>{company_name}</b>", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        elements.append(Spacer(1, 1*cm))
        
        # Package badge - ROBUST ACCESS
        package = self._safe_get(data, 'recommended_package', default='BUSINESS')
        package_colors = {
            'PREMIUM': colors.HexColor('#d4af37'),  # Gold
            'BUSINESS': colors.HexColor('#2980b9'),  # Blue
            'BASIC': colors.HexColor('#27ae60')     # Green
        }
        package_color = package_colors.get(package, colors.HexColor('#2980b9'))
        
        package_table = Table(
            [[f"Empfohlenes Paket: {package}"]],
            colWidths=[10*cm]
        )
        package_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('BACKGROUND', (0, 0), (-1, -1), package_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ]))
        elements.append(package_table)
        elements.append(Spacer(1, 1*cm))
        
        # Quality Score - ROBUST ACCESS
        quality_score = self._safe_get(data, 'quality_score', 'total_score', default=0)
        score_text = Paragraph(
            f"<b>Quality Score:</b> {quality_score}/200 Punkte",
            self.styles['Highlight']
        )
        elements.append(score_text)
        elements.append(Spacer(1, 0.5*cm))
        
        # ROI Estimate - ROBUST ACCESS
        roi = self._safe_get(data, 'roi_estimate', 'estimated_monthly_roi', default='Auf Anfrage')
        roi_text = Paragraph(
            f"<b>Geschätzter monatlicher ROI:</b> {roi}",
            self.styles['Highlight']
        )
        elements.append(roi_text)
        elements.append(Spacer(1, 2*cm))
        
        # Date
        date_str = datetime.now().strftime("%d.%m.%Y")
        date_text = Paragraph(f"Erstellt am: {date_str}", self.styles['CustomBody'])
        elements.append(date_text)
        
        return elements
    
    def _create_executive_summary(self, data: dict):
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Company overview - ROBUST ACCESS
        company_name = self._safe_get(data, 'company_overview', 'company_name', default='Ihr Unternehmen')
        industry = self._safe_get(data, 'company_overview', 'industry', default='Hospitality')
        website = self._safe_get(data, 'company_overview', 'website_url', default='N/A')
        
        summary_text = f"""
        Diese Analyse wurde für <b>{company_name}</b> ({industry}) erstellt und zeigt das 
        Potenzial der ChatPro AI Integration für Ihre Website ({website}).
        <br/><br/>
        Unsere Analyse basiert auf einer detaillierten Untersuchung Ihrer Website und 
        aktuellen Chatbot-Infrastruktur. Wir haben konservative ROI-Schätzungen verwendet, 
        um realistische Erwartungen zu setzen.
        """
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Key benefits - ROBUST ACCESS
        benefits = data.get('key_benefits', [])
        if benefits:
            elements.append(Paragraph("<b>Hauptvorteile der ChatPro AI Integration:</b>", self.styles['SubsectionHeader']))
            for benefit in benefits:
                elements.append(Paragraph(f"• {benefit}", self.styles['CustomBody']))
        
        return elements
    
    def _create_current_situation(self, data: dict):
        """Create current situation section with crawler summary"""
        elements = []
        
        elements.append(Paragraph("1. Aktuelle Situation", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Chatbot capabilities - ROBUST ACCESS
        chatbot_detected = self._safe_get(data, 'chatbot_capabilities', 'chatbot_detected', default=False)
        chatbot_type = self._safe_get(data, 'chatbot_capabilities', 'chatbot_type', default='Nicht erkannt')
        
        status_text = "✅ Chatbot erkannt" if chatbot_detected else "❌ Kein Chatbot erkannt"
        elements.append(Paragraph(f"<b>Chatbot Status:</b> {status_text}", self.styles['CustomBody']))
        
        if chatbot_detected:
            elements.append(Paragraph(f"<b>Typ:</b> {chatbot_type}", self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.5*cm))
        
        # NEW: Section 2.1 - Analysierte Website-Daten (Crawler Summary)
        elements.append(Paragraph("1.1 Analysierte Website-Daten", self.styles['SubsectionHeader']))
        elements.append(Spacer(1, 0.2*cm))
        
        crawler_summary = data.get('crawler_summary', {})
        
        crawler_data = [
            ['Metrik', 'Wert'],
            ['Analysierte Seiten', str(self._safe_get(crawler_summary, 'total_pages_crawled', default=0))],
            ['Chatbot Status', self._safe_get(crawler_summary, 'chatbot_status', default='Nicht erkannt')],
            ['Zimmerzahl', str(self._safe_get(crawler_summary, 'room_count', default='Nicht erkannt'))],
            ['Sprachen', ', '.join(self._safe_get(crawler_summary, 'languages_detected', default=['de']))],
        ]
        
        crawler_table = Table(crawler_data, colWidths=[8*cm, 8*cm])
        crawler_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        elements.append(crawler_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Key features detected
        key_features = self._safe_get(crawler_summary, 'key_features', default=[])
        if key_features:
            elements.append(Paragraph("<b>Erkannte Website-Features:</b>", self.styles['CustomBody']))
            for feature in key_features:
                elements.append(Paragraph(f"• {feature}", self.styles['CustomBody']))
        
        return elements
    
    def _create_solution_section(self, data: dict):
        """Create ChatPro AI solution section"""
        elements = []
        
        elements.append(Paragraph("2. ChatPro AI Lösung", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Package recommendation - ROBUST ACCESS
        package = self._safe_get(data, 'recommended_package', default='BUSINESS')
        elements.append(Paragraph(f"<b>Empfohlenes Paket:</b> {package}", self.styles['Highlight']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Competitive advantages - ROBUST ACCESS
        advantages = data.get('competitive_advantages', [])
        if advantages:
            elements.append(Paragraph("<b>Wettbewerbsvorteile:</b>", self.styles['SubsectionHeader']))
            for advantage in advantages:
                elements.append(Paragraph(f"• {advantage}", self.styles['CustomBody']))
        
        return elements
    
    def _create_roi_implementation(self, data: dict):
        """Create ROI and implementation section with methodology"""
        elements = []
        
        elements.append(Paragraph("3. ROI & Implementierung", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*cm))
        
        # ROI estimate - ROBUST ACCESS
        roi = self._safe_get(data, 'roi_estimate', 'estimated_monthly_roi', default='Auf Anfrage')
        elements.append(Paragraph(f"<b>Geschätzter monatlicher ROI:</b> {roi}", self.styles['Highlight']))
        elements.append(Spacer(1, 0.5*cm))
        
        # NEW: Section 3.1 - Methodik & Datenquellen
        elements.append(Paragraph("3.1 Methodik & Datenquellen", self.styles['SubsectionHeader']))
        elements.append(Spacer(1, 0.2*cm))
        
        methodology = data.get('methodology_details', {})
        
        # Data sources
        data_sources = self._safe_get(methodology, 'data_sources', default=[])
        if data_sources:
            elements.append(Paragraph("<b>Datenquellen:</b>", self.styles['CustomBody']))
            for source in data_sources:
                elements.append(Paragraph(f"• {source}", self.styles['CustomBody']))
            elements.append(Spacer(1, 0.3*cm))
        
        # ROI calculation method
        roi_method = self._safe_get(methodology, 'roi_calculation_method', default='Standardmethode')
        elements.append(Paragraph("<b>ROI-Berechnungsmethode:</b>", self.styles['CustomBody']))
        elements.append(Paragraph(roi_method, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Quality score breakdown
        quality_breakdown = self._safe_get(methodology, 'quality_score_breakdown', default='Siehe Quality Score')
        elements.append(Paragraph("<b>Quality Score Berechnung:</b>", self.styles['CustomBody']))
        elements.append(Paragraph(quality_breakdown, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Conservative assumptions
        assumptions = self._safe_get(methodology, 'conservative_assumptions', default=[])
        if assumptions:
            elements.append(Paragraph("<b>Konservative Annahmen:</b>", self.styles['CustomBody']))
            for assumption in assumptions:
                elements.append(Paragraph(f"• {assumption}", self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Implementation roadmap - ROBUST ACCESS
        roadmap = data.get('implementation_roadmap', [])
        if roadmap:
            elements.append(Paragraph("3.2 Implementierungs-Roadmap", self.styles['SubsectionHeader']))
            for i, step in enumerate(roadmap, 1):
                elements.append(Paragraph(f"<b>Schritt {i}:</b> {step}", self.styles['CustomBody']))
        
        return elements


def generate_pdf_report(analysis_data: dict, output_filename: str):
    """
    Convenience function to generate PDF report.
    
    Args:
        analysis_data: Dictionary with nested structure from analyzer.py
        output_filename: Output PDF file path
    """
    generator = ChatProPDFGenerator()
    generator.generate_report(analysis_data, output_filename)
