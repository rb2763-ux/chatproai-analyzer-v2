"""
CHATPRO AI ANALYZER - EMAIL SENDER (AWS SES)
Send analysis reports via AWS SES with tracking
"""

import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional
import os
from datetime import datetime

class EmailSender:
    """
    AWS SES Email Sender for analysis reports
    """
    
    def __init__(
        self,
        aws_region: str = "eu-central-1",
        from_email: str = "robert@chatproai.io",
        from_name: str = "Robert Bruckner - ChatPro AI"
    ):
        self.aws_region = aws_region
        self.from_email = from_email
        self.from_name = from_name
        
        # Initialize SES client
        self.ses_client = boto3.client(
            'ses',
            region_name=self.aws_region
        )
    
    def send_analysis_report(
        self,
        to_email: str,
        company_name: str,
        website_url: str,
        roi_monat: int,
        roi_multiplikator: float,
        report_url: str,
        analysis_id: str
    ) -> Dict:
        """
        Send analysis report email
        
        Returns:
            Dict with status and message_id
        """
        
        # Build email content
        subject = f"Ihre ChatPro AI Website-Analyse für {company_name}"
        
        html_body = self._build_html_email(
            company_name=company_name,
            website_url=website_url,
            roi_monat=roi_monat,
            roi_multiplikator=roi_multiplikator,
            report_url=report_url,
            analysis_id=analysis_id
        )
        
        text_body = self._build_text_email(
            company_name=company_name,
            website_url=website_url,
            roi_monat=roi_monat,
            report_url=report_url
        )
        
        try:
            # Send email
            response = self.ses_client.send_email(
                Source=f"{self.from_name} <{self.from_email}>",
                Destination={
                    'ToAddresses': [to_email]
                },
                Message={
                    'Subject': {
                        'Data': subject,
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': text_body,
                            'Charset': 'UTF-8'
                        },
                        'Html': {
                            'Data': html_body,
                            'Charset': 'UTF-8'
                        }
                    }
                }
            )
            
            return {
                'status': 'success',
                'message_id': response['MessageId'],
                'sent_at': datetime.utcnow().isoformat()
            }
            
        except ClientError as e:
            error_message = e.response['Error']['Message']
            return {
                'status': 'failed',
                'error': error_message
            }
    
    def _build_html_email(
        self,
        company_name: str,
        website_url: str,
        roi_monat: int,
        roi_multiplikator: float,
        report_url: str,
        analysis_id: str
    ) -> str:
        """
        Build HTML email content
        """
        
        return f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ihre ChatPro AI Analyse</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background-color: #f3f4f6;">
    <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f3f4f6;">
        <tr>
            <td style="padding: 40px 20px;">
                <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                            <div style="font-size: 48px; margin-bottom: 10px;">🤖</div>
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700;">ChatPro AI Analyzer</h1>
                            <p style="margin: 10px 0 0; color: rgba(255,255,255,0.9); font-size: 16px;">Ihre Website-Analyse ist fertig!</p>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="margin: 0 0 20px; color: #374151; font-size: 16px; line-height: 1.6;">
                                Hallo,
                            </p>
                            
                            <p style="margin: 0 0 20px; color: #374151; font-size: 16px; line-height: 1.6;">
                                vielen Dank für Ihr Interesse an ChatPro AI! Ihre persönliche Website-Analyse für <strong>{company_name}</strong> ist fertig.
                            </p>
                            
                            <!-- ROI Box -->
                            <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 30px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; overflow: hidden;">
                                <tr>
                                    <td style="padding: 30px; text-align: center;">
                                        <div style="color: rgba(255,255,255,0.9); font-size: 14px; margin-bottom: 10px;">ROI-POTENZIAL</div>
                                        <div style="color: #ffffff; font-size: 42px; font-weight: 700; margin-bottom: 10px;">€{roi_monat:,}</div>
                                        <div style="color: rgba(255,255,255,0.9); font-size: 16px;">pro Monat</div>
                                        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
                                            <span style="color: rgba(255,255,255,0.9); font-size: 14px;">ROI-Multiplikator: </span>
                                            <span style="color: #ffffff; font-size: 24px; font-weight: 700;">{roi_multiplikator}x</span>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- What's in the Report -->
                            <div style="background-color: #f0f9ff; border: 2px solid #bfdbfe; border-radius: 8px; padding: 20px; margin: 30px 0;">
                                <h3 style="margin: 0 0 15px; color: #1e40af; font-size: 18px; font-weight: 600;">📄 Im Report enthalten:</h3>
                                <ul style="margin: 0; padding: 0 0 0 20px; color: #1e3a8a;">
                                    <li style="margin-bottom: 8px;">Website-Analyse mit technischen Details</li>
                                    <li style="margin-bottom: 8px;">Chatbot-Analyse und Schwachstellen</li>
                                    <li style="margin-bottom: 8px;">ROI-Berechnung mit transparenten Quellen</li>
                                    <li style="margin-bottom: 8px;">Konkrete Handlungsempfehlungen</li>
                                    <li style="margin-bottom: 8px;">Vollständiges Quellenverzeichnis</li>
                                </ul>
                            </div>
                            
                            <!-- CTA Button -->
                            <table role="presentation" style="width: 100%; margin: 30px 0;">
                                <tr>
                                    <td style="text-align: center;">
                                        <a href="{report_url}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; padding: 16px 40px; border-radius: 8px; font-weight: 600; font-size: 16px;">
                                            📥 Report jetzt herunterladen
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 30px 0 20px; color: #374151; font-size: 16px; line-height: 1.6;">
                                <strong>Nächster Schritt:</strong><br>
                                Buchen Sie eine kostenlose 30-Minuten Demo und sehen Sie ChatPro AI live in Aktion!
                            </p>
                            
                            <!-- Demo Button -->
                            <table role="presentation" style="width: 100%; margin: 20px 0;">
                                <tr>
                                    <td style="text-align: center;">
                                        <a href="https://calendly.com/chatproaiio/30min" style="display: inline-block; background-color: #10b981; color: #ffffff; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 600; font-size: 15px;">
                                            📅 Kostenlose Demo buchen
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 30px 0 20px; color: #374151; font-size: 16px; line-height: 1.6;">
                                Bei Fragen stehe ich Ihnen gerne zur Verfügung!
                            </p>
                            
                            <p style="margin: 0; color: #374151; font-size: 16px; line-height: 1.6;">
                                Beste Grüße,<br>
                                <strong>Robert Bruckner</strong><br>
                                ChatPro AI
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f9fafb; padding: 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                            <p style="margin: 0 0 10px; color: #6b7280; font-size: 14px;">
                                <strong>ChatPro AI</strong> - 24/7 AI-Chatbot Lösungen
                            </p>
                            <p style="margin: 0 0 15px; color: #6b7280; font-size: 13px;">
                                📧 robert@chatproai.io | 🌐 www.chatproai.io
                            </p>
                            <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                                <a href="https://www.chatproai.io/impressum.html" style="color: #6b7280; text-decoration: none;">Impressum</a> | 
                                <a href="https://www.chatproai.io/datenschutz.html" style="color: #6b7280; text-decoration: none;">Datenschutz</a>
                            </p>
                            
                            <!-- Tracking Pixel -->
                            <img src="https://track.chatproai.io/open/{analysis_id}" width="1" height="1" style="display: block; margin: 20px auto 0;" alt="">
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
        """
    
    def _build_text_email(
        self,
        company_name: str,
        website_url: str,
        roi_monat: int,
        report_url: str
    ) -> str:
        """
        Build plain text email content
        """
        
        return f"""
ChatPro AI Website-Analyse - {company_name}

Hallo,

vielen Dank für Ihr Interesse an ChatPro AI! Ihre persönliche Website-Analyse für {company_name} ist fertig.

ROI-POTENZIAL: €{roi_monat:,} pro Monat

Im Report enthalten:
- Website-Analyse mit technischen Details
- Chatbot-Analyse und Schwachstellen
- ROI-Berechnung mit transparenten Quellen
- Konkrete Handlungsempfehlungen
- Vollständiges Quellenverzeichnis

Report herunterladen:
{report_url}

Nächster Schritt:
Buchen Sie eine kostenlose 30-Minuten Demo und sehen Sie ChatPro AI live in Aktion!

Demo buchen:
https://calendly.com/chatproaiio/30min

Bei Fragen stehe ich Ihnen gerne zur Verfügung!

Beste Grüße,
Robert Bruckner
ChatPro AI

---
ChatPro AI - 24/7 AI-Chatbot Lösungen
📧 robert@chatproai.io
🌐 www.chatproai.io

Impressum: https://www.chatproai.io/impressum.html
Datenschutz: https://www.chatproai.io/datenschutz.html
        """


# Test function
def test_email_sender():
    """Test email sender"""
    
    sender = EmailSender()
    
    result = sender.send_analysis_report(
        to_email="robert@chatproai.io",
        company_name="ADORO Aparthotel",
        website_url="https://adoro-aparthotel.com",
        roi_monat=13180,
        roi_multiplikator=16.5,
        report_url="https://analyzer.chatproai.io/api/report/abc123",
        analysis_id="abc123"
    )
    
    print("=== EMAIL SEND RESULT ===")
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Message ID: {result['message_id']}")
        print(f"Sent at: {result['sent_at']}")
    else:
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    test_email_sender()
