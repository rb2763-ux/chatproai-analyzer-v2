#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatPro AI - PDF Report Generator (ReportLab)
==============================================
Professional PDF generation with ReportLab for business analysis reports.

Features:
- Cover page with branding
- Header/Footer with page numbers
- ROI calculations with sources
- Pain points analysis
- Recommendations
- Complete source bibliography
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Frame, PageTemplate
)
from reportlab.pdfgen import canvas

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ChatPro AI Brand Colors
BRAND_PRIMARY = colors.HexColor('#00ff87')  # Neon Green
BRAND_SECONDARY = colors.HexColor('#60efff')  # Cyan
BRAND_DARK = colors.HexColor('#1a1a1a')  # Dark Background
BRAND_GRAY = colors.HexColor('#808080')  # Gray text

class NumberedCanvas(canvas.Canvas):
    """Custom canvas for adding headers, footers, and page numbers"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        """Add header/footer to all pages"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_decorations(self, page_count):
        """Draw header and footer on each page"""
        page_num = self._pageNumber
        
        # Skip header/footer on cover page (page 1)
        if page_num == 1:
            return
            
        # Header
        self.saveState()
        self.setStrokeColor(BRAND_GRAY)
        self.setLineWidth(0.5)
        self.line(2*cm, A4[1] - 2*cm, A4[0] - 2*cm, A4[1] - 2*cm)
        
        self.setFont('Helvetica', 8)
        self.setFillColor(BRAND_GRAY)
        self.drawString(2*cm, A4[1] - 1.7*cm, "ChatPro AI - Business Analysis Report")
        self.drawRightString(A4[0] - 2*cm, A4[1] - 1.7*cm, 
                           datetime.now().strftime('%d.%m.%Y'))
        
        # Footer
        self.setStrokeColor(BRAND_GRAY)
        self.line(2*cm, 2*cm, A4[0] - 2*cm, 2*cm)
        
        self.setFont('Helvetica', 8)
        self.drawCentredString(A4[0] / 2, 1.5*cm, 
                              f"Seite {page_num} von {page_count}")
        
        self.drawString(2*cm, 1.5*cm, "VERTRAULICH")
        self.drawRightString(A4[0] - 2*cm, 1.5*cm, "www.chatproai.io")
        
        self.restoreState()


class PDFReportGenerator:
    """Professional PDF Report Generator using ReportLab"""
    
    def __init__(self):
        """Initialize PDF generator with styles"""
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        
        # Title style (Cover page)
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=32,
            textColor=BRAND_PRIMARY,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.white,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section Heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=BRAND_PRIMARY,
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection Heading
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=BRAND_SECONDARY,
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.black,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=16
        ))
        
        # Bullet point
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.black,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=8,
            leading=14
        ))
        
        # Source style
        self.styles.add(ParagraphStyle(
            name='Source',
            parent=self.styles['BodyText'],
            fontSize=9,
            textColor=BRAND_GRAY,
            spaceAfter=6,
            leftIndent=15,
            leading=12
        ))
        
    def generate(self, crawler_data: Dict, analysis_data: Dict,
                 company_name: str, industry: str, output_path: str,
                 sources: Optional[List] = None) -> str:
        """
        Generate professional PDF report
        
        Args:
            crawler_data: Website crawling data (chatbot, mobile, etc.)
            analysis_data: AI analysis results (ROI, pain points, recommendations)
            company_name: Name of the analyzed company
            industry: Industry type (hotel, restaurant, etc.)
            output_path: Path where PDF should be saved
            sources: List of sources used in analysis
            
        Returns:
            str: Path to generated PDF file
        """
        try:
            logger.info(f"Starting PDF generation for {company_name}")
            
            # Validate data
            if not crawler_data:
                crawler_data = {}
            if not analysis_data:
                analysis_data = {}
            if not sources:
                sources = []
                
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2.5*cm,
                bottomMargin=2.5*cm
            )
            
            # Build story (content)
            story = []
            
            # 1. Cover Page
            story.extend(self._create_cover_page(company_name, industry))
            story.append(PageBreak())
            
            # 2. Executive Summary
            story.extend(self._create_executive_summary(analysis_data))
            story.append(Spacer(1, 0.5*cm))
            
            # 3. ROI Analysis
            story.extend(self._create_roi_section(analysis_data))
            story.append(Spacer(1, 0.5*cm))
            
            # 4. Pain Points
            story.extend(self._create_pain_points_section(analysis_data, crawler_data))
            story.append(Spacer(1, 0.5*cm))
            
            # 5. Recommendations
            story.extend(self._create_recommendations_section(analysis_data))
            story.append(PageBreak())
            
            # 6. Sources
            if sources:
                story.extend(self._create_sources_section(sources))
            
            # Build PDF with custom canvas (for headers/footers)
            doc.build(story, canvasmaker=NumberedCanvas)
            
            logger.info(f"PDF generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"PDF generation error: {str(e)}")
            raise
            
    def _create_cover_page(self, company_name: str, industry: str) -> List:
        """Create professional cover page"""
        elements = []
        
        # Add vertical spacing
        elements.append(Spacer(1, 4*cm))
        
        # Title
        title = Paragraph(
            "Business Analysis Report",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 1*cm))
        
        # Company name
        company = Paragraph(
            f"<b>{company_name}</b>",
            self.styles['CustomSubtitle']
        )
        elements.append(company)
        elements.append(Spacer(1, 0.5*cm))
        
        # Industry badge
        industry_labels = {
            'hotel': 'Hotel & Hospitality',
            'restaurant': 'Restaurant & Gastronomie',
            'salon': 'Beauty & Wellness',
            'fahrschule': 'Fahrschule',
            'fitness': 'Fitness & Sport',
            'immobilien': 'Immobilien'
        }
        industry_label = industry_labels.get(industry, industry.title())
        
        industry_p = Paragraph(
            f"<i>{industry_label}</i>",
            self.styles['CustomBody']
        )
        elements.append(industry_p)
        elements.append(Spacer(1, 3*cm))
        
        # Date
        date_text = Paragraph(
            f"<b>Erstellt am:</b> {datetime.now().strftime('%d. %B %Y')}",
            self.styles['CustomBody']
        )
        elements.append(date_text)
        elements.append(Spacer(1, 0.5*cm))
        
        # ChatPro AI branding
        branding = Paragraph(
            "<b>ChatPro AI</b><br/>KI-gestützte Business-Analyse",
            self.styles['CustomBody']
        )
        elements.append(branding)
        elements.append(Spacer(1, 1*cm))
        
        # Confidential notice
        confidential = Paragraph(
            "<i>VERTRAULICH - Nur für internen Gebrauch</i>",
            ParagraphStyle(
                'Confidential',
                parent=self.styles['CustomBody'],
                fontSize=9,
                textColor=BRAND_GRAY,
                alignment=TA_CENTER
            )
        )
        elements.append(confidential)
        
        return elements
        
    def _create_executive_summary(self, analysis_data: Dict) -> List:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        
        # Get summary from analysis
        summary = analysis_data.get('executive_summary', 
                                   'Basierend auf der durchgeführten Analyse wurden verschiedene '
                                   'Optimierungspotenziale identifiziert.')
        
        elements.append(Paragraph(summary, self.styles['CustomBody']))
        
        return elements
        
    def _create_roi_section(self, analysis_data: Dict) -> List:
        """Create ROI analysis section"""
        elements = []
        
        elements.append(Paragraph("ROI-Potenzial", self.styles['SectionHeading']))
        
        # Get ROI data
        roi_data = analysis_data.get('roi_calculation', {})
        monthly_roi = roi_data.get('monthly_roi', 0)
        roi_multiplier = roi_data.get('roi_multiplier', 0)
        break_even = roi_data.get('break_even_months', 0)
        
        # ROI Overview Table
        roi_table_data = [
            ['Kennzahl', 'Wert'],
            ['Monatliches ROI-Potenzial', f"€{monthly_roi:,.0f}"],
            ['ROI-Multiplikator', f"{roi_multiplier:.1f}x"],
            ['Break-even', f"{break_even} Monate"]
        ]
        
        roi_table = Table(roi_table_data, colWidths=[8*cm, 6*cm])
        roi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BRAND_PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(roi_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # ROI Details
        roi_details = roi_data.get('calculation_details', {})
        if roi_details:
            elements.append(Paragraph("Berechnungsdetails", self.styles['SubsectionHeading']))
            
            time_savings = roi_details.get('time_savings', 0)
            direct_bookings = roi_details.get('direct_bookings', 0)
            commission_savings = roi_details.get('commission_savings', 0)
            
            details_text = f"""
            <b>Zeitersparnis:</b> €{time_savings:,.0f}/Monat<br/>
            <b>Direktbuchungen:</b> €{direct_bookings:,.0f}/Monat<br/>
            <b>Provisionsersparnis:</b> €{commission_savings:,.0f}/Monat
            """
            elements.append(Paragraph(details_text, self.styles['CustomBody']))
        
        return elements
        
    def _create_pain_points_section(self, analysis_data: Dict, 
                                   crawler_data: Dict) -> List:
        """Create pain points analysis section"""
        elements = []
        
        elements.append(Paragraph("Identifizierte Pain Points", 
                                self.styles['SectionHeading']))
        
        pain_points = analysis_data.get('pain_points', [])
        
        if not pain_points:
            # Generate pain points from crawler data
            pain_points = self._generate_pain_points_from_crawler(crawler_data)
        
        for i, pain_point in enumerate(pain_points[:5], 1):
            if isinstance(pain_point, dict):
                title = pain_point.get('title', f'Pain Point {i}')
                description = pain_point.get('description', '')
                evidence = pain_point.get('evidence', '')
            else:
                title = f"Pain Point {i}"
                description = str(pain_point)
                evidence = ""
            
            # Pain point title
            elements.append(Paragraph(
                f"<b>{i}. {title}</b>",
                self.styles['SubsectionHeading']
            ))
            
            # Description
            elements.append(Paragraph(description, self.styles['CustomBody']))
            
            # Evidence if available
            if evidence:
                elements.append(Paragraph(
                    f"<i>Evidenz: {evidence}</i>",
                    self.styles['Source']
                ))
            
            elements.append(Spacer(1, 0.3*cm))
        
        return elements
        
    def _generate_pain_points_from_crawler(self, crawler_data: Dict) -> List[Dict]:
        """Generate pain points from crawler data"""
        pain_points = []
        
        # Check for chatbot
        if not crawler_data.get('has_chatbot', False):
            pain_points.append({
                'title': 'Kein 24/7 Kundenservice',
                'description': 'Keine automatisierte Beantwortung von Kundenanfragen außerhalb der Geschäftszeiten.',
                'evidence': f"Chatbot: {crawler_data.get('chatbot_type', 'Nicht erkannt')}"
            })
        
        # Check mobile optimization
        if not crawler_data.get('is_mobile_optimized', False):
            pain_points.append({
                'title': 'Nicht mobile-optimiert',
                'description': 'Die Website ist nicht für mobile Endgeräte optimiert, was zu Conversion-Verlusten führt.',
                'evidence': 'Mobile: ✗ Nicht optimiert'
            })
        
        # Check online presence
        pages_count = crawler_data.get('pages_count', 0)
        if pages_count == 0:
            pain_points.append({
                'title': 'Geringe Online-Präsenz',
                'description': 'Fehlende oder unvollständige Online-Präsenz reduziert die Sichtbarkeit.',
                'evidence': f'Seiten: {pages_count}'
            })
        
        return pain_points if pain_points else [{
            'title': 'Optimierungspotenzial vorhanden',
            'description': 'Verschiedene Bereiche können durch KI-Automatisierung verbessert werden.',
            'evidence': 'Basierend auf Branchenanalyse'
        }]
        
    def _create_recommendations_section(self, analysis_data: Dict) -> List:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Empfehlungen", self.styles['SectionHeading']))
        
        recommendations = analysis_data.get('recommendations', [])
        
        if not recommendations:
            recommendations = [
                {
                    'title': 'KI-Chatbot implementieren',
                    'priority': 'Hoch',
                    'description': 'Automatisierung von Kundenanfragen und Steigerung der Direktbuchungen.',
                    'impact': 'Zeitersparnis und höhere Conversion-Rate'
                }
            ]
        
        for i, rec in enumerate(recommendations[:5], 1):
            if isinstance(rec, dict):
                title = rec.get('title', f'Empfehlung {i}')
                priority = rec.get('priority', 'Mittel')
                description = rec.get('description', '')
                impact = rec.get('impact', '')
            else:
                title = f"Empfehlung {i}"
                priority = "Mittel"
                description = str(rec)
                impact = ""
            
            # Recommendation header
            priority_color = {
                'Hoch': colors.red,
                'Mittel': colors.orange,
                'Niedrig': colors.green
            }.get(priority, colors.grey)
            
            elements.append(Paragraph(
                f"<b>{i}. {title}</b> "
                f"<font color='{priority_color.hexval()}'>● {priority}</font>",
                self.styles['SubsectionHeading']
            ))
            
            # Description
            elements.append(Paragraph(description, self.styles['CustomBody']))
            
            # Impact
            if impact:
                elements.append(Paragraph(
                    f"<b>Erwarteter Impact:</b> {impact}",
                    self.styles['BulletPoint']
                ))
            
            elements.append(Spacer(1, 0.3*cm))
        
        return elements
        
    def _create_sources_section(self, sources: List) -> List:
        """Create sources bibliography section"""
        elements = []
        
        elements.append(Paragraph("Quellenverzeichnis", 
                                self.styles['SectionHeading']))
        
        elements.append(Paragraph(
            "Diese Analyse basiert auf folgenden Quellen:",
            self.styles['CustomBody']
        ))
        elements.append(Spacer(1, 0.3*cm))
        
        for i, source in enumerate(sources, 1):
            if isinstance(source, dict):
                title = source.get('title', 'Unbekannte Quelle')
                url = source.get('url', '')
                description = source.get('description', '')
            else:
                # Parse string format like "1. [Title] - URL"
                source_str = str(source)
                parts = source_str.split(' - ', 1)
                title = parts[0].strip('0123456789. []')
                url = parts[1] if len(parts) > 1 else ''
                description = ''
            
            # Source entry
            source_text = f"<b>[{i}]</b> {title}"
            if url:
                source_text += f"<br/><link href='{url}'>{url}</link>"
            if description:
                source_text += f"<br/><i>{description}</i>"
            
            elements.append(Paragraph(source_text, self.styles['Source']))
            elements.append(Spacer(1, 0.2*cm))
        
        return elements


# Singleton instance
_generator = None

def get_generator() -> PDFReportGenerator:
    """Get or create PDF generator instance"""
    global _generator
    if _generator is None:
        _generator = PDFReportGenerator()
    return _generator
