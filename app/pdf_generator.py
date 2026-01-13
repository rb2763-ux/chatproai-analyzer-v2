#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatPro AI - Professional PDF Report Generator
===============================================
McKinsey-style business analysis reports with ReportLab.

Features:
- Professional cover page
- Table of contents
- Executive summary
- ROI analysis with charts
- Categorized pain points
- Detailed recommendations
- Implementation roadmap
- Source bibliography
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, Frame, PageTemplate
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ChatPro AI Brand Colors (McKinsey-inspired)
PRIMARY_COLOR = colors.HexColor('#2563eb')       # Professional Blue
SECONDARY_COLOR = colors.HexColor('#7c3aed')     # Purple accent
SUCCESS_COLOR = colors.HexColor('#10b981')       # Green for positive
WARNING_COLOR = colors.HexColor('#f59e0b')       # Orange for medium
DANGER_COLOR = colors.HexColor('#ef4444')        # Red for critical
GRAY_DARK = colors.HexColor('#1f2937')           # Dark text
GRAY_MEDIUM = colors.HexColor('#6b7280')         # Medium gray
GRAY_LIGHT = colors.HexColor('#e5e7eb')          # Light gray
BACKGROUND_LIGHT = colors.HexColor('#f9fafb')    # Very light background

# Page layout constants
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 2 * cm
MARGIN_RIGHT = 2 * cm
MARGIN_TOP = 1.5 * cm
MARGIN_BOTTOM = 1.5 * cm
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT


class NumberedCanvas(canvas.Canvas):
    """Custom canvas with professional headers and footers"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        """Add page decorations to all pages"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_decorations(self, page_count):
        """Draw professional header and footer"""
        page_num = self._pageNumber
        
        # Skip decorations on cover page
        if page_num == 1:
            return
            
        self.saveState()
        
        # Header line
        self.setStrokeColor(GRAY_LIGHT)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, PAGE_HEIGHT - MARGIN_TOP + 0.5*cm, 
                 PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - MARGIN_TOP + 0.5*cm)
        
        # Header text
        self.setFont('Helvetica', 9)
        self.setFillColor(GRAY_MEDIUM)
        self.drawString(MARGIN_LEFT, PAGE_HEIGHT - MARGIN_TOP + 0.8*cm, 
                       "ChatPro AI - Business Analysis Report")
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, 
                           PAGE_HEIGHT - MARGIN_TOP + 0.8*cm,
                           datetime.now().strftime('%d. %B %Y'))
        
        # Footer line
        self.setStrokeColor(GRAY_LIGHT)
        self.line(MARGIN_LEFT, MARGIN_BOTTOM - 0.5*cm,
                 PAGE_WIDTH - MARGIN_RIGHT, MARGIN_BOTTOM - 0.5*cm)
        
        # Footer text
        self.setFont('Helvetica', 8)
        self.setFillColor(GRAY_MEDIUM)
        self.drawString(MARGIN_LEFT, MARGIN_BOTTOM - 0.8*cm, "VERTRAULICH")
        self.drawCentredString(PAGE_WIDTH / 2, MARGIN_BOTTOM - 0.8*cm,
                              f"Seite {page_num} von {page_count}")
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, MARGIN_BOTTOM - 0.8*cm,
                           "www.chatproai.io")
        
        self.restoreState()


class PDFReportGenerator:
    """
    Professional PDF Report Generator
    Creates McKinsey-style business analysis reports
    """
    
    def __init__(self):
        """Initialize the PDF generator with professional styles"""
        self.styles = self._create_custom_styles()
        
    def _create_custom_styles(self) -> Dict:
        """Create custom paragraph styles for professional layout"""
        base_styles = getSampleStyleSheet()
        
        custom_styles = {
            # Cover page styles
            'CoverTitle': ParagraphStyle(
                'CoverTitle',
                parent=base_styles['Heading1'],
                fontName='Helvetica-Bold',
                fontSize=32,
                textColor=GRAY_DARK,
                spaceAfter=12,
                alignment=TA_CENTER,
                leading=38
            ),
            'CoverSubtitle': ParagraphStyle(
                'CoverSubtitle',
                parent=base_styles['Normal'],
                fontName='Helvetica',
                fontSize=18,
                textColor=PRIMARY_COLOR,
                spaceAfter=24,
                alignment=TA_CENTER,
                leading=22
            ),
            'CoverCompany': ParagraphStyle(
                'CoverCompany',
                parent=base_styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=24,
                textColor=GRAY_DARK,
                spaceAfter=8,
                alignment=TA_CENTER,
                leading=28
            ),
            'CoverMeta': ParagraphStyle(
                'CoverMeta',
                parent=base_styles['Normal'],
                fontName='Helvetica',
                fontSize=12,
                textColor=GRAY_MEDIUM,
                spaceAfter=6,
                alignment=TA_CENTER,
                leading=16
            ),
            
            # Heading styles
            'Heading1': ParagraphStyle(
                'CustomHeading1',
                parent=base_styles['Heading1'],
                fontName='Helvetica-Bold',
                fontSize=16,
                textColor=GRAY_DARK,
                spaceAfter=12,
                spaceBefore=16,
                leading=20
            ),
            'Heading2': ParagraphStyle(
                'CustomHeading2',
                parent=base_styles['Heading2'],
                fontName='Helvetica-Bold',
                fontSize=12,
                textColor=GRAY_DARK,
                spaceAfter=8,
                spaceBefore=12,
                leading=16
            ),
            'Heading3': ParagraphStyle(
                'CustomHeading3',
                parent=base_styles['Heading3'],
                fontName='Helvetica-Bold',
                fontSize=12,
                textColor=PRIMARY_COLOR,
                spaceAfter=6,
                spaceBefore=10,
                leading=15
            ),
            
            # Body text styles
            'BodyText': ParagraphStyle(
                'CustomBodyText',
                parent=base_styles['Normal'],
                fontName='Helvetica',
                fontSize=10,
                textColor=GRAY_DARK,
                spaceAfter=8,
                alignment=TA_JUSTIFY,
                leading=14
            ),
            'BodyTextIndent': ParagraphStyle(
                'BodyTextIndent',
                parent=base_styles['Normal'],
                fontName='Helvetica',
                fontSize=10,
                textColor=GRAY_DARK,
                spaceAfter=6,
                leftIndent=20,
                alignment=TA_JUSTIFY,
                leading=14
            ),
            
            # Special styles
            'Highlight': ParagraphStyle(
                'Highlight',
                parent=base_styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=12,
                textColor=PRIMARY_COLOR,
                spaceAfter=10,
                leading=16
            ),
            'MetricValue': ParagraphStyle(
                'MetricValue',
                parent=base_styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=24,
                textColor=SUCCESS_COLOR,
                spaceAfter=4,
                alignment=TA_CENTER,
                leading=28
            ),
            'MetricLabel': ParagraphStyle(
                'MetricLabel',
                parent=base_styles['Normal'],
                fontName='Helvetica',
                fontSize=10,
                textColor=GRAY_MEDIUM,
                spaceAfter=12,
                alignment=TA_CENTER,
                leading=12
            ),
            'BulletPoint': ParagraphStyle(
                'BulletPoint',
                parent=base_styles['Normal'],
                fontName='Helvetica',
                fontSize=11,
                textColor=GRAY_DARK,
                spaceAfter=6,
                leftIndent=20,
                bulletIndent=10,
                leading=15
            ),
            'Caption': ParagraphStyle(
                'Caption',
                parent=base_styles['Normal'],
                fontName='Helvetica-Oblique',
                fontSize=9,
                textColor=GRAY_MEDIUM,
                spaceAfter=8,
                alignment=TA_CENTER,
                leading=11
            ),
        }
        
        return custom_styles
    
    def generate(self, company_name: str, industry: str, 
                crawler_data: Dict, analysis_data: Dict,
                sources: List[Dict] = None,
                output_path: str = None) -> str:
        """
        Generate professional PDF report
        
        Args:
            company_name: Name of the company
            industry: Industry sector
            crawler_data: Website crawling results
            analysis_data: AI analysis results
            sources: List of industry sources
            output_path: Optional output path for PDF
            
        Returns:
            str: Path to generated PDF file
        """
        try:
            # Set default output path
            if not output_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = f"/tmp/report_{company_name}_{timestamp}.pdf"
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                leftMargin=MARGIN_LEFT,
                rightMargin=MARGIN_RIGHT,
                topMargin=MARGIN_TOP,
                bottomMargin=MARGIN_BOTTOM,
                title=f"{company_name} - Business Analysis Report"
            )
            
            # Build document content
            story = []
            
            # 1. Cover Page
            story.extend(self._create_cover_page(company_name, industry, crawler_data))
            story.append(PageBreak())
            
            # 2. Table of Contents (placeholder - would need bookmarks in full version)
            story.extend(self._create_table_of_contents())
            story.append(PageBreak())
            
            # 3. Executive Summary
            story.extend(self._create_executive_summary(analysis_data, crawler_data))
            story.append(PageBreak())
            
            # 4. Company Overview
            story.extend(self._create_company_overview(company_name, industry, crawler_data))
            story.append(Spacer(1, 0.3*cm))
            
            # 5. ROI Analysis
            story.extend(self._create_roi_analysis(analysis_data))
            story.append(PageBreak())
            
            # 6. Pain Points Analysis
            story.extend(self._create_pain_points(analysis_data.get('pain_points', [])))
            story.append(PageBreak())
            
            # 7. Recommendations
            story.extend(self._create_recommendations(analysis_data.get('recommendations', [])))
            story.append(PageBreak())
            
            # 8. Sources & References
            if sources:
                story.extend(self._create_sources_section(sources))
                story.append(PageBreak())
            
            # 9. Legal Disclaimer Page
            story.extend(self._create_legal_disclaimer_page())
            
            # Build PDF with custom canvas
            doc.build(story, canvasmaker=NumberedCanvas)
            
            logger.info(f"✅ Professional PDF generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error generating PDF: {str(e)}")
            raise
    
    def _create_cover_page(self, company_name: str, industry: str, 
                          crawler_data: Dict) -> List:
        """Create professional cover page"""
        elements = []
        
        # Add vertical space
        elements.append(Spacer(1, 4*cm))
        
        # Main title
        elements.append(Paragraph(
            "Website-Analyse & ROI-Bewertung",
            self.styles['CoverTitle']
        ))
        
        # Subtitle
        elements.append(Paragraph(
            "Geschäftsanalyse-Bericht",
            self.styles['CoverSubtitle']
        ))
        
        elements.append(Spacer(1, 1*cm))
        
        # Company name
        elements.append(Paragraph(
            company_name,
            self.styles['CoverCompany']
        ))
        
        # Industry
        industry_display = {
            'hotel': 'Hotel & Gastgewerbe',
            'vacation_rental': 'Ferienvermietung',
            'restaurant': 'Gastronomie',
            'fitness': 'Fitness & Wellness',
            'salon': 'Beauty & Salon',
            'fahrschule': 'Fahrschule',
            'immobilien': 'Immobilien',
            'other': 'Allgemein'
        }.get(industry, industry.title())
        
        elements.append(Paragraph(
            industry_display,
            self.styles['CoverMeta']
        ))
        
        # Website URL
        if 'url' in crawler_data:
            elements.append(Paragraph(
                crawler_data['url'],
                self.styles['CoverMeta']
            ))
        
        elements.append(Spacer(1, 3*cm))
        
        # Date and branding
        elements.append(Paragraph(
            f"Erstellt am {datetime.now().strftime('%d. %B %Y')}",
            self.styles['CoverMeta']
        ))
        
        elements.append(Spacer(1, 0.6*cm))
        
        elements.append(Paragraph(
            "<b>ChatPro AI</b> | KI-gestützte Geschäftsanalyse",
            self.styles['CoverMeta']
        ))
        
        # Legal disclaimer at bottom
        elements.append(Spacer(1, 1*cm))
        
        disclaimer_style = ParagraphStyle(
            'CoverDisclaimer',
            parent=self.styles['CoverMeta'],
            fontSize=8,
            textColor=GRAY_MEDIUM,
            alignment=TA_CENTER,
            leading=10
        )
        
        elements.append(Paragraph(
            "<i>Hinweis: Diese Analyse basiert auf Schätzungen und automatisierten Berechnungen. "
            "Die dargestellten ROI-Werte und Empfehlungen dienen ausschließlich zu Informationszwecken "
            "und stellen keine Garantie für tatsächliche Ergebnisse dar. Keine Rechts- oder Anlageberatung.</i>",
            disclaimer_style
        ))
        
        return elements
    
    def _create_table_of_contents(self) -> List:
        """Create table of contents"""
        elements = []
        
        elements.append(Paragraph("Inhaltsverzeichnis", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        toc_data = [
            ['1.', 'Zusammenfassung', '3'],
            ['2.', 'Unternehmensübersicht', '4'],
            ['3.', 'ROI-Analyse', '5'],
            ['4.', 'Identifizierte Herausforderungen', '6'],
            ['5.', 'Empfehlungen', '7'],
            ['6.', 'Quellen & Referenzen', '8'],
            ['7.', 'Rechtliche Hinweise', '9'],
        ]
        
        toc_table = Table(toc_data, colWidths=[1.5*cm, 13*cm, 2*cm])
        toc_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), GRAY_DARK),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_LIGHT),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(toc_table)
        
        return elements
    
    def _create_executive_summary(self, analysis_data: Dict, 
                                 crawler_data: Dict) -> List:
        """Create executive summary page"""
        elements = []
        
        elements.append(Paragraph("Zusammenfassung", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Key findings box
        roi_calc = analysis_data.get('roi_calculation', {})
        pain_points = analysis_data.get('pain_points', [])
        recommendations = analysis_data.get('recommendations', [])
        
        # Summary text
        summary_text = f"""
        Diese Analyse untersucht die digitale Präsenz und identifiziert konkrete 
        Optimierungspotenziale. Basierend auf unserer Bewertung der Website und 
        Branchenbenchmarks haben wir {len(pain_points)} prioritäre Handlungsfelder 
        identifiziert und {len(recommendations)} umsetzbare Empfehlungen entwickelt.
        """
        
        elements.append(Paragraph(summary_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Key metrics table
        monthly_roi = roi_calc.get('monthly_roi_euro', 0)
        roi_multiplier = roi_calc.get('roi_multiplier', 0)
        break_even = roi_calc.get('break_even_months', 0)
        
        metrics_data = [
            ['Monatliches ROI-Potenzial', f"€{monthly_roi:,}"],
            ['ROI-Multiplikator', f"{roi_multiplier}x"],
            ['Break-Even Zeitraum', f"{break_even} Monate"],
            ['Prioritäre Maßnahmen', str(len([r for r in recommendations if r.get('priority') == 'HIGH']))],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[10*cm, 6*cm])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), BACKGROUND_LIGHT),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), GRAY_DARK),
            ('TEXTCOLOR', (1, 0), (1, 0), SUCCESS_COLOR),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRAY_LIGHT),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.4*cm))
        
        # Quick wins highlight
        quick_wins = [r for r in recommendations if r.get('quick_win', False)]
        if quick_wins:
            elements.append(Paragraph("⚡ Schnelle Erfolge", self.styles['Heading3']))
            
            for rec in quick_wins[:3]:  # Top 3 quick wins
                elements.append(Paragraph(
                    f"• <b>{rec.get('title', 'N/A')}</b>",
                    self.styles['BulletPoint']
                ))
            
            elements.append(Spacer(1, 0.3*cm))
        
        # Chatbot detection
        if crawler_data.get('has_chatbot'):
            elements.append(Paragraph(
                "✅ <b>Chatbot erkannt:</b> Ihre Website verfügt bereits über einen Chatbot. "
                "Unsere Analyse zeigt Optimierungspotenziale auf.",
                self.styles['BodyText']
            ))
        else:
            elements.append(Paragraph(
                "⚠️ <b>Kein Chatbot erkannt:</b> Die Integration eines KI-Chatbots könnte "
                "Kundenanfragen automatisieren und die Conversion-Rate steigern.",
                self.styles['BodyText']
            ))
        
        elements.append(Spacer(1, 0.3*cm))
        
        # Disclaimer box
        disclaimer_text = (
            "<i>⚠️ <b>Wichtiger Hinweis:</b> Diese Analyse stellt eine unverbindliche Einschätzung dar "
            "und basiert auf automatisierten Berechnungen sowie allgemeinen Branchendaten. "
            "Die genannten Werte sind Schätzungen und können im Einzelfall erheblich abweichen. "
            "Diese Analyse ersetzt keine professionelle Beratung.</i>"
        )
        
        disclaimer_data = [[Paragraph(disclaimer_text, self.styles['BodyText'])]]
        disclaimer_table = Table(disclaimer_data, colWidths=[CONTENT_WIDTH])
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#856404')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#ffc107')),
        ]))
        
        elements.append(disclaimer_table)
        
        return elements
    
    def _create_company_overview(self, company_name: str, industry: str,
                                crawler_data: Dict) -> List:
        """Create company overview section"""
        elements = []
        
        elements.append(Paragraph("Unternehmensübersicht", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Company info table
        industry_display = {
            'hotel': 'Hotel & Gastgewerbe',
            'vacation_rental': 'Ferienvermietung',
            'restaurant': 'Gastronomie',
            'fitness': 'Fitness & Wellness',
            'salon': 'Beauty & Salon',
            'fahrschule': 'Fahrschule',
            'immobilien': 'Immobilien',
            'other': 'Allgemein'
        }.get(industry, industry.title())
        
        overview_data = [
            ['Unternehmen', company_name],
            ['Branche', industry_display],
            ['Website', crawler_data.get('url', 'N/A')],
            ['Analysedatum', datetime.now().strftime('%d.%m.%Y')],
        ]
        
        overview_table = Table(overview_data, colWidths=[5*cm, 11*cm])
        overview_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), GRAY_DARK),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_LIGHT),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(overview_table)
        
        return elements
    
    def _create_roi_chart(self, monthly_roi: int) -> Drawing:
        """Create ROI bar chart"""
        drawing = Drawing(CONTENT_WIDTH, 200)
        
        # Create bar chart
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = CONTENT_WIDTH - 100
        bc.data = [[monthly_roi * i for i in [0.7, 0.85, 1.0, 1.15, 1.3, 1.45]]]
        bc.strokeColor = None
        
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = monthly_roi * 1.6
        bc.valueAxis.valueStep = monthly_roi * 0.2
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 0
        bc.categoryAxis.categoryNames = ['Monat 1', 'Monat 2', 'Monat 3', 
                                         'Monat 4', 'Monat 5', 'Monat 6']
        
        bc.bars[0].fillColor = PRIMARY_COLOR
        
        drawing.add(bc)
        
        return drawing
    
    def _create_roi_analysis(self, analysis_data: Dict) -> List:
        """Create detailed ROI analysis section"""
        elements = []
        
        elements.append(Paragraph("ROI-Analyse", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        roi_calc = analysis_data.get('roi_calculation', {})
        
        if not roi_calc:
            elements.append(Paragraph(
                "Keine ROI-Daten verfügbar.",
                self.styles['BodyText']
            ))
            return elements
        
        # ROI metrics
        monthly_roi = roi_calc.get('monthly_roi_euro', 0)
        roi_multiplier = roi_calc.get('roi_multiplier', 0)
        break_even = roi_calc.get('break_even_months', 0)
        
        # Key figures in boxes
        figures_data = [
            [
                Paragraph(f"<b>€{monthly_roi:,}</b>", self.styles['MetricValue']),
                Paragraph(f"<b>{roi_multiplier}x</b>", self.styles['MetricValue']),
                Paragraph(f"<b>{break_even}</b>", self.styles['MetricValue'])
            ],
            [
                Paragraph("Monatliches ROI", self.styles['MetricLabel']),
                Paragraph("ROI-Multiplikator", self.styles['MetricLabel']),
                Paragraph("Break-Even (Monate)", self.styles['MetricLabel'])
            ]
        ]
        
        figures_table = Table(figures_data, colWidths=[5.3*cm, 5.3*cm, 5.3*cm])
        figures_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), BACKGROUND_LIGHT),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRAY_LIGHT),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(figures_table)
        elements.append(Spacer(1, 0.4*cm))
        
        # Formula explanation
        formula_text = roi_calc.get('formula_explanation', 'Keine Formel verfügbar')
        elements.append(Paragraph("Berechnungsgrundlage", self.styles['Heading3']))
        elements.append(Paragraph(formula_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Assumptions
        assumptions = roi_calc.get('assumptions', [])
        if assumptions:
            elements.append(Paragraph("Annahmen", self.styles['Heading3']))
            for assumption in assumptions:
                elements.append(Paragraph(
                    f"• {assumption}",
                    self.styles['BulletPoint']
                ))
            elements.append(Spacer(1, 0.3*cm))
        
        # ROI Disclaimer
        roi_disclaimer_text = (
            "<i>⚠️ <b>ROI-Disclaimer:</b> Die dargestellten ROI-Berechnungen sind Schätzungen basierend auf "
            "Branchendurchschnitten, allgemeinen Marktdaten und KI-gestützten Analysen. Tatsächliche Ergebnisse "
            "können erheblich abweichen und hängen von zahlreichen Faktoren ab, einschließlich aber nicht beschränkt auf: "
            "Marktbedingungen, Wettbewerb, Umsetzungsqualität und externe Einflüsse. "
            "<b>Wir übernehmen keine Gewähr oder Garantie für die Richtigkeit der Berechnungen oder "
            "den Eintritt der prognostizierten Ergebnisse.</b> Diese Informationen stellen keine Anlage-, "
            "Rechts- oder Steuerberatung dar.</i>"
        )
        
        roi_disclaimer_data = [[Paragraph(roi_disclaimer_text, self.styles['BodyText'])]]
        roi_disclaimer_table = Table(roi_disclaimer_data, colWidths=[CONTENT_WIDTH])
        roi_disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8d7da')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#721c24')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#f5c6cb')),
        ]))
        
        elements.append(roi_disclaimer_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # ROI chart
        if monthly_roi > 0:
            elements.append(Paragraph("Prognostizierte Entwicklung (6 Monate)", 
                                    self.styles['Heading3']))
            elements.append(self._create_roi_chart(monthly_roi))
            elements.append(Paragraph(
                "Abbildung: Prognostizierter monatlicher ROI über 6 Monate",
                self.styles['Caption']
            ))
        
        return elements
    
    def _create_pain_points(self, pain_points: List[Dict]) -> List:
        """Create pain points analysis section"""
        elements = []
        
        elements.append(Paragraph("Identifizierte Herausforderungen", 
                                self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        if not pain_points:
            elements.append(Paragraph(
                "Keine spezifischen Herausforderungen identifiziert.",
                self.styles['BodyText']
            ))
            return elements
        
        # Group by priority
        high_priority = [p for p in pain_points if p.get('priority') == 'HIGH']
        medium_priority = [p for p in pain_points if p.get('priority') == 'MEDIUM']
        low_priority = [p for p in pain_points if p.get('priority') == 'LOW']
        
        # Priority summary
        summary_data = [
            ['🔴 Hohe Priorität', str(len(high_priority))],
            ['🟠 Mittlere Priorität', str(len(medium_priority))],
            ['🟡 Niedrige Priorität', str(len(low_priority))],
        ]
        
        summary_table = Table(summary_data, colWidths=[13*cm, 3*cm])
        summary_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica', 11),
            ('FONT', (1, 0), (1, -1), 'Helvetica-Bold', 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), GRAY_DARK),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_LIGHT),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.4*cm))
        
        # Detailed pain points
        for idx, pain_point in enumerate(pain_points, 1):
            # Priority indicator
            priority = pain_point.get('priority', 'MEDIUM')
            priority_color = {
                'HIGH': DANGER_COLOR,
                'MEDIUM': WARNING_COLOR,
                'LOW': GRAY_MEDIUM
            }.get(priority, GRAY_MEDIUM)
            
            priority_emoji = {
                'HIGH': '🔴',
                'MEDIUM': '🟠',
                'LOW': '🟡'
            }.get(priority, '⚪')
            
            # Pain point box
            title = pain_point.get('title', 'N/A')
            category = pain_point.get('category', 'Allgemein')
            description = pain_point.get('description', '')
            business_impact = pain_point.get('business_impact', 'Nicht quantifiziert')
            
            # Header
            elements.append(Paragraph(
                f"{priority_emoji} <b>Herausforderung #{idx}: {title}</b>",
                self.styles['Heading3']
            ))
            
            # Info table
            info_data = [
                ['Kategorie', category],
                ['Priorität', priority],
                ['Geschäftliche Auswirkung', business_impact],
            ]
            
            info_table = Table(info_data, colWidths=[4*cm, 12*cm])
            info_table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
                ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), GRAY_DARK),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_LIGHT),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            elements.append(info_table)
            elements.append(Spacer(1, 0.3*cm))
            
            # Description
            elements.append(Paragraph(description, self.styles['BodyText']))
            elements.append(Spacer(1, 0.3*cm))
        
        return elements
    
    def _create_recommendations(self, recommendations: List[Dict]) -> List:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Empfehlungen", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        if not recommendations:
            elements.append(Paragraph(
                "Keine Empfehlungen verfügbar.",
                self.styles['BodyText']
            ))
            return elements
        
        # Quick wins first
        quick_wins = [r for r in recommendations if r.get('quick_win', False)]
        regular_recs = [r for r in recommendations if not r.get('quick_win', False)]
        
        if quick_wins:
            elements.append(Paragraph("⚡ Schnelle Erfolge", self.styles['Heading2']))
            elements.append(Spacer(1, 0.3*cm))
            
            for idx, rec in enumerate(quick_wins, 1):
                elements.extend(self._format_recommendation(idx, rec, is_quick_win=True))
        
        if regular_recs:
            if quick_wins:
                elements.append(Spacer(1, 0.4*cm))
            elements.append(Paragraph("📋 Weitere Empfehlungen", self.styles['Heading2']))
            elements.append(Spacer(1, 0.3*cm))
            
            start_idx = len(quick_wins) + 1
            for idx, rec in enumerate(regular_recs, start_idx):
                elements.extend(self._format_recommendation(idx, rec, is_quick_win=False))
        
        return elements
    
    def _format_recommendation(self, idx: int, rec: Dict, is_quick_win: bool) -> List:
        """Format a single recommendation"""
        elements = []
        
        title = rec.get('title', 'N/A')
        description = rec.get('description', '')
        business_value = rec.get('business_value', 'Nicht quantifiziert')
        implementation_effort = rec.get('implementation_effort', 'Nicht spezifiziert')
        priority = rec.get('priority', 'MEDIUM')
        
        # Priority indicator
        priority_emoji = {
            'HIGH': '🔴',
            'MEDIUM': '🟠',
            'LOW': '🟡'
        }.get(priority, '⚪')
        
        # Title
        quick_win_badge = " ⚡" if is_quick_win else ""
        elements.append(Paragraph(
            f"{priority_emoji} <b>Empfehlung #{idx}: {title}{quick_win_badge}</b>",
            self.styles['Heading3']
        ))
        
        # Info table
        info_data = [
            ['Priorität', priority],
            ['Business Value', business_value],
            ['Umsetzungsaufwand', implementation_effort],
        ]
        
        info_table = Table(info_data, colWidths=[5*cm, 11*cm])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), GRAY_DARK),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, GRAY_LIGHT),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # Description
        elements.append(Paragraph(description, self.styles['BodyText']))
        elements.append(Spacer(1, 0.6*cm))
        
        return elements
    
    def _create_sources_section(self, sources: List[Dict]) -> List:
        """Create sources and references section"""
        elements = []
        
        elements.append(Paragraph("Quellen & Referenzen", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        elements.append(Paragraph(
            f"Diese Analyse basiert auf {len(sources)} branchenspezifischen "
            "Quellen und aktuellen Marktdaten:",
            self.styles['BodyText']
        ))
        elements.append(Spacer(1, 0.3*cm))
        
        for idx, source in enumerate(sources, 1):
            title = source.get('title', 'N/A')
            url = source.get('url', '')
            key_insight = source.get('key_insight', '')
            
            # Source entry
            elements.append(Paragraph(
                f"<b>[{idx}] {title}</b>",
                self.styles['BodyText']
            ))
            
            if url:
                elements.append(Paragraph(
                    f'<link href="{url}" color="blue">{url}</link>',
                    self.styles['BodyTextIndent']
                ))
            
            if key_insight:
                elements.append(Paragraph(
                    f"→ {key_insight}",
                    self.styles['BodyTextIndent']
                ))
            
            elements.append(Spacer(1, 0.4*cm))
        
        return elements
    
    def _create_legal_disclaimer_page(self) -> List:
        """Create comprehensive legal disclaimer page"""
        elements = []
        
        elements.append(Paragraph("Rechtliche Hinweise", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Main disclaimer sections
        sections = [
            {
                'title': '1. ALLGEMEINE HINWEISE',
                'content': (
                    "Die in diesem Report dargestellten Analysen, Berechnungen und Empfehlungen basieren auf:"
                    "<br/>• Automatisierter Website-Analyse mittels KI-Technologie"
                    "<br/>• Allgemeinen Branchendaten und statistischen Durchschnittswerten"
                    "<br/>• Öffentlich zugänglichen Marktinformationen"
                    "<br/>• KI-gestützten Schätzungen und Hochrechnungen"
                    "<br/><br/>"
                    "Diese Analyse dient ausschließlich zu Informationszwecken und stellt eine "
                    "unverbindliche Einschätzung dar."
                )
            },
            {
                'title': '2. KEINE GEWÄHR FÜR RICHTIGKEIT',
                'content': (
                    "<b>Wir übernehmen keine Gewähr oder Garantie für:</b>"
                    "<br/>• Die Richtigkeit, Vollständigkeit oder Aktualität der Informationen"
                    "<br/>• Die Genauigkeit der ROI-Berechnungen und Prognosen"
                    "<br/>• Den Eintritt der prognostizierten Geschäftsergebnisse"
                    "<br/>• Den Erfolg der implementierten Empfehlungen"
                    "<br/>• Die Eignung der Empfehlungen für Ihren spezifischen Einzelfall"
                    "<br/><br/>"
                    "<b>Tatsächliche Ergebnisse können erheblich von den Schätzungen abweichen</b> und hängen von "
                    "zahlreichen Faktoren ab, einschließlich aber nicht beschränkt auf: Marktbedingungen, "
                    "Wettbewerbssituation, Umsetzungsqualität, Timing, Budget, Team-Kompetenz und externe Einflüsse."
                )
            },
            {
                'title': '3. HAFTUNGSAUSSCHLUSS',
                'content': (
                    "<b>ChatPro AI haftet nicht für:</b>"
                    "<br/>• Finanzielle Verluste oder entgangene Gewinne"
                    "<br/>• Geschäftsschäden jeglicher Art"
                    "<br/>• Folgeschäden aus der Nutzung dieser Analyse"
                    "<br/>• Entscheidungen, die auf Basis dieses Reports getroffen werden"
                    "<br/><br/>"
                    "Die Nutzung der Informationen in diesem Report erfolgt auf eigenes Risiko. "
                    "Der Nutzer trägt die volle Verantwortung für alle geschäftlichen Entscheidungen "
                    "und deren Umsetzung."
                )
            },
            {
                'title': '4. KEINE BERATUNG',
                'content': (
                    "<b>Dieser Report stellt ausdrücklich KEINE dar:</b>"
                    "<br/>• Rechtsberatung oder juristische Empfehlung"
                    "<br/>• Steuerberatung oder steuerliche Empfehlung"
                    "<br/>• Anlageberatung oder Finanzberatung"
                    "<br/>• Unternehmensberatung im Sinne professioneller Consultingleistungen"
                    "<br/>• Individualisierte Beratung für Ihren spezifischen Einzelfall"
                    "<br/><br/>"
                    "Für rechtsverbindliche Auskünfte und individuelle Beratung konsultieren Sie bitte "
                    "entsprechende Fachexperten (Rechtsanwälte, Steuerberater, Unternehmensberater)."
                )
            },
            {
                'title': '5. DATENSCHUTZ (DSGVO)',
                'content': (
                    "Diese Analyse wurde unter Beachtung der Datenschutz-Grundverordnung (DSGVO) erstellt. "
                    "Es wurden ausschließlich öffentlich zugängliche Informationen Ihrer Website analysiert. "
                    "<br/><br/>"
                    "<b>Datenverarbeitung:</b>"
                    "<br/>• Website-URL und öffentliche Inhalte"
                    "<br/>• Unternehmensname (soweit öffentlich)"
                    "<br/>• Branchenzuordnung"
                    "<br/>• Kontakt-E-Mail (nur für Report-Zustellung)"
                    "<br/><br/>"
                    "Weitere Informationen zum Datenschutz finden Sie unter: "
                    "<link href='https://www.chatproai.io/datenschutz' color='blue'>www.chatproai.io/datenschutz</link>"
                )
            },
            {
                'title': '6. URHEBERRECHT',
                'content': (
                    "Dieser Report und alle darin enthaltenen Inhalte sind urheberrechtlich geschützt. "
                    "<br/><br/>"
                    "<b>© 2026 ChatPro AI - Alle Rechte vorbehalten.</b>"
                    "<br/><br/>"
                    "Die Weitergabe, Vervielfältigung oder Veröffentlichung dieses Reports oder Teilen davon "
                    "ist nur mit ausdrücklicher schriftlicher Genehmigung von ChatPro AI gestattet."
                )
            },
            {
                'title': '7. KONTAKT & SUPPORT',
                'content': (
                    "<b>ChatPro AI</b>"
                    "<br/>KI-gestützte Geschäftsanalyse"
                    "<br/><br/>"
                    "Website: <link href='https://www.chatproai.io' color='blue'>www.chatproai.io</link>"
                    "<br/>E-Mail: info@chatproai.io"

                    "<br/><br/>"
                    "Für Fragen zu diesem Report oder unseren Dienstleistungen kontaktieren Sie uns gerne."
                )
            }
        ]
        
        # Add each section
        for section in sections:
            elements.append(Paragraph(section['title'], self.styles['Heading3']))
            elements.append(Paragraph(section['content'], self.styles['BodyText']))
            elements.append(Spacer(1, 0.3*cm))
        
        # Final notice box
        elements.append(Spacer(1, 0.3*cm))
        
        final_notice = (
            "<b>⚠️ WICHTIG:</b> Mit der Nutzung dieses Reports bestätigen Sie, dass Sie diese rechtlichen "
            "Hinweise zur Kenntnis genommen haben und akzeptieren. Sollten Sie mit diesen Bedingungen "
            "nicht einverstanden sein, dürfen Sie die Informationen in diesem Report nicht verwenden."
        )
        
        final_notice_data = [[Paragraph(final_notice, self.styles['BodyText'])]]
        final_notice_table = Table(final_notice_data, colWidths=[CONTENT_WIDTH])
        final_notice_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8d7da')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#721c24')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#f5c6cb')),
        ]))
        
        elements.append(final_notice_table)
        
        return elements


def main():
    """Test the PDF generator"""
    # Test data
    test_data = {
        'company_name': 'Guest House Holland',
        'industry': 'hotel',
        'crawler_data': {
            'url': 'https://guesthouseholland.com',
            'has_chatbot': True
        },
        'analysis_data': {
            'roi_calculation': {
                'monthly_roi_euro': 3000,
                'roi_multiplier': 3.5,
                'break_even_months': 5,
                'formula_explanation': 'Basierend auf durchschnittlicher Buchungssteigerung',
                'assumptions': ['Durchschnittliche Zimmerbelegung: 75%', 'Conversion-Rate-Verbesserung: 12%']
            },
            'pain_points': [
                {
                    'title': 'Niedrige Mobile Conversion',
                    'category': 'Customer Experience',
                    'priority': 'HIGH',
                    'description': 'Mobile Nutzer konvertieren nur mit 2.3%',
                    'business_impact': '€12,000/Monat verloren'
                }
            ],
            'recommendations': [
                {
                    'title': 'Mobile-First Optimierung',
                    'priority': 'HIGH',
                    'quick_win': True,
                    'description': 'Implementierung eines responsiven Designs',
                    'business_value': '+€12,000/Monat',
                    'implementation_effort': '2-3 Wochen'
                }
            ]
        },
        'sources': []
    }
    
    generator = PDFReportGenerator()
    output = generator.generate(**test_data)
    print(f"✅ Test PDF generated: {output}")


if __name__ == '__main__':
    main()
