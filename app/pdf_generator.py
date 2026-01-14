"""
ChatPro AI - PDF Report Generator
VERSION 3.1 - MODERN LAYOUT
"""

import os
from datetime import datetime
from typing import Dict, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

# PAGE SETTINGS - V3.1 MORE WHITESPACE
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 2.5 * cm
MARGIN_RIGHT = 2.5 * cm
MARGIN_TOP = 2.5 * cm
MARGIN_BOTTOM = 2.5 * cm

# COLORS
COLOR_PRIMARY = colors.HexColor('#2C3E50')
COLOR_SECONDARY = colors.HexColor('#3498DB')
COLOR_ACCENT = colors.HexColor('#E74C3C')
COLOR_SUCCESS = colors.HexColor('#27AE60')
COLOR_WARNING = colors.HexColor('#F39C12')
COLOR_TEXT = colors.HexColor('#2C3E50')

# SPACING
SECTION_SPACING = 0.4 * cm
PARAGRAPH_SPACING = 0.3 * cm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        page_num = f"Seite {self._pageNumber} von {page_count}"
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, MARGIN_BOTTOM/2, page_num)
        self.drawString(MARGIN_LEFT, MARGIN_BOTTOM/2, "www.chatproai.io")

class PDFReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = self._create_styles()

    def _create_styles(self) -> Dict:
        styles = getSampleStyleSheet()
        
        custom_styles = {
            'CustomTitle': ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=COLOR_PRIMARY,
                spaceAfter=0.5*cm,
                alignment=TA_CENTER,
                leading=30
            ),
            'CustomHeading1': ParagraphStyle(
                'CustomHeading1',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=COLOR_PRIMARY,
                spaceAfter=0.4*cm,
                spaceBefore=0.5*cm,
                leading=20
            ),
            'CustomHeading2': ParagraphStyle(
                'CustomHeading2',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=COLOR_SECONDARY,
                spaceAfter=0.3*cm,
                spaceBefore=0.4*cm,
                leading=18
            ),
            'CustomBody': ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=10,
                textColor=COLOR_TEXT,
                alignment=TA_JUSTIFY,
                spaceAfter=PARAGRAPH_SPACING,
                leading=14
            ),
            'CustomBullet': ParagraphStyle(
                'CustomBullet',
                parent=styles['BodyText'],
                fontSize=10,
                textColor=COLOR_TEXT,
                leftIndent=0.5*cm,
                spaceAfter=0.2*cm,
                leading=14
            )
        }
        
        return custom_styles

    def generate_report(self, analysis_data: Dict, output_filename: str) -> str:
        output_path = os.path.join(self.output_dir, output_filename)
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=MARGIN_LEFT,
            rightMargin=MARGIN_RIGHT,
            topMargin=MARGIN_TOP,
            bottomMargin=MARGIN_BOTTOM,
            title="ChatPro AI - Business Analysis Report"
        )
        
        story = []
        story.extend(self._create_cover_page(analysis_data))
        story.append(PageBreak())
        story.extend(self._create_toc())
        story.append(PageBreak())
        story.extend(self._create_executive_summary(analysis_data))
        story.append(Spacer(1, SECTION_SPACING))
        story.extend(self._create_company_overview(analysis_data))
        story.append(Spacer(1, SECTION_SPACING))
        story.extend(self._create_roi_section(analysis_data))
        story.append(PageBreak())
        story.extend(self._create_pain_points_section(analysis_data))
        story.append(Spacer(1, SECTION_SPACING))
        story.extend(self._create_recommendations_section(analysis_data))
        story.append(PageBreak())
        story.extend(self._create_sources_section(analysis_data))
        
        doc.build(story, canvasmaker=NumberedCanvas)
        return output_path

    def _create_cover_page(self, data: Dict) -> List:
        elements = []
        elements.append(Spacer(1, 3*cm))
        
        title = Paragraph("ChatPro AI<br/>Business Analysis Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 1*cm))
        
        company = data.get('company_overview', {}).get('company_name', 'N/A')
        company_para = Paragraph(
            f"<b>{company}</b>",
            ParagraphStyle('CompanyName', fontSize=18, textColor=COLOR_SECONDARY, alignment=TA_CENTER)
        )
        elements.append(company_para)
        elements.append(Spacer(1, 2*cm))
        
        date_str = datetime.now().strftime("%d. %B %Y")
        date_para = Paragraph(date_str, ParagraphStyle('Date', fontSize=12, textColor=colors.grey, alignment=TA_CENTER))
        elements.append(date_para)
        elements.append(Spacer(1, 3*cm))
        
        confidential = Paragraph(
            "<b>VERTRAULICH</b><br/>Dieser Bericht enthält vertrauliche Geschäftsinformationen.",
            ParagraphStyle('Confidential', fontSize=10, textColor=COLOR_ACCENT, alignment=TA_CENTER)
        )
        elements.append(confidential)
        
        return elements

    def _create_toc(self) -> List:
        elements = []
        elements.append(Paragraph("Inhaltsverzeichnis", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.5*cm))
        
        toc_items = [
            "1. Zusammenfassung",
            "2. Unternehmensübersicht",
            "3. ROI-Analyse",
            "4. Identifizierte Herausforderungen",
            "5. Empfehlungen",
            "6. Quellen & Referenzen",
            "7. Rechtliche Hinweise"
        ]
        
        for item in toc_items:
            elements.append(Paragraph(item, self.styles['CustomBody']))
            elements.append(Spacer(1, 0.2*cm))
        
        return elements

    def _create_executive_summary(self, data: Dict) -> List:
        elements = []
        elements.append(Paragraph("1. Zusammenfassung", self.styles['CustomHeading1']))
        
        recommended_package = data.get('recommended_package', '').upper()
        if recommended_package:
            badge_color = COLOR_SUCCESS if recommended_package == 'PREMIUM' else COLOR_SECONDARY
            badge_table = Table(
                [[Paragraph(f"<b>EMPFOHLENES PAKET: {recommended_package}</b>", 
                           ParagraphStyle('Badge', fontSize=12, textColor=colors.white, alignment=TA_CENTER))]],
                colWidths=[10*cm]
            )
            badge_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), badge_color),
                ('PADDING', (0,0), (-1,-1), 0.3*cm),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')
            ]))
            elements.append(badge_table)
            elements.append(Spacer(1, 0.4*cm))
        
        quality_score = data.get('quality_score')
        if quality_score is not None:
            score_para = Paragraph(f"<b>Quality Score:</b> {quality_score}/200 Punkte", self.styles['CustomBody'])
            elements.append(score_para)
            elements.append(Spacer(1, 0.3*cm))
        
        summary = data.get('executive_summary', 'Keine Zusammenfassung verfügbar.')
        elements.append(Paragraph(summary, self.styles['CustomBody']))
        
        return elements

    def _create_company_overview(self, data: Dict) -> List:
        elements = []
        elements.append(Paragraph("2. Unternehmensübersicht", self.styles['CustomHeading1']))
        
        overview = data.get('company_overview', {})
        overview_data = [
            ['Unternehmen:', overview.get('company_name', 'N/A')],
            ['Branche:', overview.get('industry', 'N/A')],
            ['Website:', overview.get('website_url', 'N/A')],
            ['Analysedatum:', datetime.now().strftime("%d.%m.%Y")]
        ]
        
        table = Table(overview_data, colWidths=[5*cm, 11*cm])
        table.setStyle(TableStyle([
            ('FONT', (0,0), (0,-1), 'Helvetica-Bold', 10),
            ('FONT', (1,0), (1,-1), 'Helvetica', 10),
            ('TEXTCOLOR', (0,0), (-1,-1), COLOR_TEXT),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 0.2*cm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.3*cm)
        ]))
        
        elements.append(table)
        return elements

    def _create_roi_section(self, data: Dict) -> List:
        elements = []
        elements.append(Paragraph("3. ROI-Analyse", self.styles['CustomHeading1']))
        
        roi_data = data.get('roi_calculation', {})
        
        if not roi_data or roi_data.get('monthly_roi_euro', 0) == 0:
            elements.append(Paragraph("Keine ROI-Daten verfügbar.", self.styles['CustomBody']))
            return elements
        
        roi_metrics = [
            ['ROI-Potenzial (monatlich):', f"€{roi_data.get('monthly_roi_euro', 0):,.0f}".replace(',', '.')],
            ['ROI-Multiplikator:', f"{roi_data.get('roi_multiplier', 0):.1f}x"],
            ['Break-Even Zeitraum:', f"{roi_data.get('break_even_months', 0):.1f} Monate"]
        ]
        
        table = Table(roi_metrics, colWidths=[8*cm, 8*cm])
        table.setStyle(TableStyle([
            ('FONT', (0,0), (0,-1), 'Helvetica-Bold', 11),
            ('FONT', (1,0), (1,-1), 'Helvetica', 11),
            ('TEXTCOLOR', (0,0), (-1,-1), COLOR_TEXT),
            ('PADDING', (0,0), (-1,-1), 0.3*cm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.4*cm)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*cm))
        
        package_details = data.get('package_details', {})
        if package_details:
            elements.append(Paragraph("Paket-Details:", self.styles['CustomHeading2']))
            
            pkg_data = [
                ['Setup-Kosten:', f"€{package_details.get('setup_cost_euro', 0):,.0f}".replace(',', '.')],
                ['Monatliche Kosten:', f"€{package_details.get('monthly_cost_euro', 0):,.0f}".replace(',', '.')]
            ]
            
            pkg_table = Table(pkg_data, colWidths=[8*cm, 8*cm])
            pkg_table.setStyle(TableStyle([
                ('FONT', (0,0), (0,-1), 'Helvetica-Bold', 10),
                ('FONT', (1,0), (1,-1), 'Helvetica', 10),
                ('TEXTCOLOR', (0,0), (-1,-1), COLOR_TEXT),
                ('PADDING', (0,0), (-1,-1), 0.2*cm)
            ]))
            
            elements.append(pkg_table)
            elements.append(Spacer(1, 0.4*cm))
        
        assumptions = roi_data.get('assumptions', [])
        if assumptions:
            elements.append(Paragraph("Annahmen:", self.styles['CustomHeading2']))
            for assumption in assumptions:
                elements.append(Paragraph(f"• {assumption}", self.styles['CustomBullet']))
        
        return elements

    def _create_pain_points_section(self, data: Dict) -> List:
        elements = []
        elements.append(Paragraph("4. Identifizierte Herausforderungen", self.styles['CustomHeading1']))
        
        pain_points = data.get('pain_points', [])
        
        if not pain_points:
            elements.append(Paragraph("Keine spezifischen Herausforderungen identifiziert.", self.styles['CustomBody']))
            return elements
        
        priority_colors = {
            'HIGH': COLOR_ACCENT,
            'MEDIUM': COLOR_WARNING,
            'LOW': COLOR_SUCCESS
        }
        
        for i, pain in enumerate(pain_points, 1):
            priority = pain.get('priority', 'MEDIUM').upper()
            priority_color = priority_colors.get(priority, COLOR_WARNING)
            
            header = Paragraph(
                f"<b>{i}. {pain.get('title', 'N/A')}</b> <font color='{priority_color.hexval()}'>({priority})</font>",
                self.styles['CustomHeading2']
            )
            elements.append(header)
            
            desc = pain.get('description', 'Keine Beschreibung verfügbar.')
            elements.append(Paragraph(desc, self.styles['CustomBody']))
            elements.append(Spacer(1, 0.3*cm))
        
        return elements

    def _create_recommendations_section(self, data: Dict) -> List:
        elements = []
        elements.append(Paragraph("5. Empfehlungen", self.styles['CustomHeading1']))
        
        recommendations = data.get('recommendations', [])
        
        if not recommendations:
            elements.append(Paragraph("Keine Empfehlungen verfügbar.", self.styles['CustomBody']))
            return elements
        
        for i, rec in enumerate(recommendations, 1):
            priority = rec.get('priority', 'MEDIUM').upper()
            
            title = Paragraph(f"<b>{i}. {rec.get('title', 'N/A')}</b> ({priority})", self.styles['CustomHeading2'])
            elements.append(title)
            
            desc = rec.get('description', 'Keine Beschreibung verfügbar.')
            elements.append(Paragraph(desc, self.styles['CustomBody']))
            
            value = rec.get('business_value', '')
            if value:
                elements.append(Paragraph(f"<b>Geschäftswert:</b> {value}", self.styles['CustomBody']))
            
            elements.append(Spacer(1, 0.4*cm))
        
        return elements

    def _create_sources_section(self, data: Dict) -> List:
        elements = []
        elements.append(Paragraph("6. Quellen & Referenzen", self.styles['CustomHeading1']))
        
        methodology = data.get('methodology', '')
        if methodology:
            elements.append(Paragraph(methodology, self.styles['CustomBody']))
            elements.append(Spacer(1, 0.4*cm))
        
        disclaimer = """
        <b>Rechtliche Hinweise:</b><br/>
        Dieser Bericht wurde auf Basis öffentlich zugänglicher Informationen und Branchendaten erstellt. 
        Die ROI-Berechnungen sind Schätzungen und können je nach tatsächlicher Implementierung variieren. 
        ChatPro AI übernimmt keine Haftung für geschäftliche Entscheidungen, die auf Basis dieses Berichts getroffen werden.
        Alle Daten werden gemäß DSGVO verarbeitet.
        """
        
        elements.append(Paragraph(disclaimer, self.styles['CustomBody']))
        return elements

def main():
    generator = PDFReportGenerator()
    
    test_data = {
        'executive_summary': 'Test Summary',
        'company_overview': {
            'company_name': 'Test Company',
            'industry': 'Hotel',
            'website_url': 'https://example.com'
        },
        'recommended_package': 'PREMIUM',
        'quality_score': 125,
        'package_details': {
            'setup_cost_euro': 4999,
            'monthly_cost_euro': 799
        },
        'roi_calculation': {
            'monthly_roi_euro': 3500,
            'roi_multiplier': 4.4,
            'break_even_months': 1.4,
            'assumptions': ['Test assumption']
        },
        'pain_points': [
            {'title': 'Test Pain Point', 'description': 'Test description', 'priority': 'HIGH'}
        ],
        'recommendations': [
            {'title': 'Test Recommendation', 'description': 'Test description', 'priority': 'HIGH'}
        ],
        'methodology': 'Test methodology'
    }
    
    output = generator.generate_report(test_data, 'test_report_v31.pdf')
    print(f"✅ PDF generated: {output}")

if __name__ == '__main__':
    main()
