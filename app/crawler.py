"""
CHATPRO AI ANALYZER - SIMPLIFIED CRAWLER (BeautifulSoup + Requests)
Production-ready crawler without Playwright dependencies
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin
import re
import time

class WebsiteCrawler:
    """
    Lightweight website crawler using requests + BeautifulSoup
    
    Features:
    - Chatbot detection (Zendesk, Tidio, Intercom, etc.)
    - Lead form detection
    - Language detection
    - Contact information extraction
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize crawler without URL (URL provided per crawl)
        
        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        
        # Chatbot signatures
        self.chatbot_signatures = {
            "zendesk": ["zdassets.com", "zendesk.com", "$zopim", "zEmbed", "zE("],
            "tidio": ["tidio.co", "tidiochat", "tidioChatApi"],
            "intercom": ["intercom.io", "window.Intercom", "Intercom("],
            "drift": ["drift.com", "window.drift", "drift.load"],
            "livechat": ["livechatinc.com", "LC_API"],
            "freshchat": ["freshchat.com", "fcWidget"],
            "chatbot.com": ["chatbot.com", "chatbot-widget"],
            "hubspot": ["hubspot", "hs-analytics"],
            "custom": []
        }
    
    async def crawl(self, url: str) -> Dict:
        """
        Main crawl method
        
        Args:
            url: Website URL to crawl
            
        Returns:
            Dict with comprehensive website analysis
        """
        # Normalize URL
        url = url if url.startswith('http') else f'https://{url}'
        domain = urlparse(url).netloc
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ChatProAI-Analyzer/1.0'
        }
        
        try:
            # Make request
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            html_content = response.text
            
            # Collect data
            analysis = {
                "url": url,
                "final_url": response.url,
                "status_code": response.status_code,
                "title": self._get_title(soup),
                "meta_description": self._get_meta_description(soup),
                "languages": self._detect_languages(soup),
                "has_chatbot": False,
                "chatbot_details": {},
                "lead_forms": self._find_lead_forms(soup),
                "pages_count": self._count_pages(soup),
                "mobile_responsive": self._check_mobile(soup),
                "contact_info": self._find_contact_info(html_content),
                "response_time_ms": int(response.elapsed.total_seconds() * 1000)
            }
            
            # Detect chatbot
            chatbot_info = self._detect_chatbot(html_content, soup)
            analysis["has_chatbot"] = chatbot_info["has_chatbot"]
            analysis["chatbot_details"] = chatbot_info
            
            return analysis
            
        except requests.exceptions.Timeout:
            return {
                "url": url,
                "error": "Timeout",
                "error_message": f"Request timed out after {self.timeout} seconds"
            }
        except requests.exceptions.RequestException as e:
            return {
                "url": url,
                "error": "RequestException",
                "error_message": str(e)
            }
        except Exception as e:
            return {
                "url": url,
                "error": "UnknownError",
                "error_message": str(e)
            }
    
    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else "No title found"
    
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '').strip() if meta else ""
    
    def _detect_languages(self, soup: BeautifulSoup) -> List[str]:
        """Detect website languages"""
        languages = []
        
        # Check HTML lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            languages.append(html_tag['lang'][:2])
        
        # Check meta tags
        for meta in soup.find_all('meta'):
            if 'lang' in meta.attrs:
                languages.append(meta['lang'][:2])
        
        return list(set(languages)) if languages else ["en"]
    
    def _detect_chatbot(self, html_content: str, soup: BeautifulSoup) -> Dict:
        """Detect chatbot presence and type"""
        html_lower = html_content.lower()
        
        for chatbot_type, signatures in self.chatbot_signatures.items():
            for signature in signatures:
                if signature.lower() in html_lower:
                    return {
                        "has_chatbot": True,
                        "chatbot_type": chatbot_type,
                        "signature_found": signature
                    }
        
        # Check for generic chat widgets
        chat_indicators = ['livechat', 'live-chat', 'chat-widget', 'chat-button']
        for indicator in chat_indicators:
            if indicator in html_lower:
                return {
                    "has_chatbot": True,
                    "chatbot_type": "generic",
                    "signature_found": indicator
                }
        
        return {"has_chatbot": False}
    
    def _find_lead_forms(self, soup: BeautifulSoup) -> List[Dict]:
        """Find lead generation forms"""
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                "action": form.get('action', ''),
                "method": form.get('method', '').upper(),
                "inputs": []
            }
            
            # Collect input fields
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                input_type = input_tag.get('type', 'text')
                input_name = input_tag.get('name', '')
                
                if input_name:
                    form_data["inputs"].append({
                        "type": input_type,
                        "name": input_name
                    })
            
            if form_data["inputs"]:
                forms.append(form_data)
        
        return forms
    
    def _count_pages(self, soup: BeautifulSoup) -> int:
        """Estimate page count from internal links"""
        links = soup.find_all('a', href=True)
        unique_pages = set()
        
        for link in links:
            href = link['href']
            if href.startswith('/') or href.startswith('http'):
                unique_pages.add(href)
        
        return min(len(unique_pages), 100)  # Cap at 100
    
    def _check_mobile(self, soup: BeautifulSoup) -> bool:
        """Check if website is mobile responsive"""
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        return viewport_meta is not None
    
    def _find_contact_info(self, html_content: str) -> Dict:
        """Extract contact information"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        
        emails = list(set(re.findall(email_pattern, html_content)))[:5]
        phones = list(set(re.findall(phone_pattern, html_content)))[:5]
        
        return {
            "emails": emails,
            "phones": [p[0] if isinstance(p, tuple) else p for p in phones]
        }
