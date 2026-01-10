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
    
    def __init__(self, url: str, timeout: int = 30):
        self.url = url if url.startswith('http') else f'https://{url}'
        self.timeout = timeout
        self.domain = urlparse(self.url).netloc
        
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
    
    def crawl(self) -> Dict:
        """
        Main crawl method
        
        Returns comprehensive website analysis
        """
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ChatProAI-Analyzer/1.0'
        }
        
        try:
            # Make request
            response = requests.get(
                self.url,
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
                "url": self.url,
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
            chatbot_data = self._detect_chatbot(html_content, soup)
            analysis["has_chatbot"] = chatbot_data["detected"]
            analysis["chatbot_details"] = chatbot_data
            
            return analysis
            
        except requests.exceptions.Timeout:
            return {
                "error": "Website timeout - Seite antwortet nicht innerhalb von 30 Sekunden",
                "url": self.url,
                "status": "timeout"
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Verbindungsfehler - Website nicht erreichbar",
                "url": self.url,
                "status": "connection_error"
            }
        except requests.exceptions.HTTPError as e:
            return {
                "error": f"HTTP Fehler: {e.response.status_code}",
                "url": self.url,
                "status": "http_error"
            }
        except Exception as e:
            return {
                "error": f"Unerwarteter Fehler: {str(e)}",
                "url": self.url,
                "status": "failed"
            }
    
    def _detect_chatbot(self, html_content: str, soup: BeautifulSoup) -> Dict:
        """
        Detect existing chatbot on website
        """
        
        detected = False
        chatbot_type = None
        has_lead_form = False
        details = {}
        
        # Check for chatbot signatures in HTML
        html_lower = html_content.lower()
        
        for bot_name, signatures in self.chatbot_signatures.items():
            for signature in signatures:
                if signature.lower() in html_lower:
                    detected = True
                    chatbot_type = bot_name
                    details["signature_found"] = signature
                    break
            if detected:
                break
        
        # Check for lead form in chatbot
        if detected:
            lead_form_indicators = [
                "email", "e-mail", "name", "vorname", "nachname",
                "prechat", "pre-chat", "required", "form"
            ]
            
            for indicator in lead_form_indicators:
                if indicator in html_lower:
                    has_lead_form = True
                    break
        
        # Priority calculation
        if detected and has_lead_form:
            priority = "HIGH"  # Zendesk with lead form - perfect target!
        elif detected:
            priority = "MEDIUM"  # Has chatbot but unclear about lead form
        else:
            priority = "LOW"  # No chatbot detected
        
        return {
            "detected": detected,
            "type": chatbot_type if detected else None,
            "has_lead_form": has_lead_form,
            "priority": priority,
            "details": details
        }
    
    def _find_lead_forms(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Find lead forms on page
        """
        
        forms = []
        
        for form in soup.find_all('form'):
            inputs = form.find_all(['input', 'textarea', 'select'])
            
            has_email = any(
                inp.get('type') == 'email' or
                'email' in str(inp.get('name', '')).lower() or
                'email' in str(inp.get('id', '')).lower()
                for inp in inputs
            )
            
            has_name = any(
                'name' in str(inp.get('name', '')).lower() or
                'name' in str(inp.get('id', '')).lower() or
                'vorname' in str(inp.get('name', '')).lower() or
                'nachname' in str(inp.get('name', '')).lower()
                for inp in inputs
            )
            
            if has_email:
                forms.append({
                    "has_email": has_email,
                    "has_name": has_name,
                    "field_count": len(inputs),
                    "action": form.get('action', '')
                })
        
        return forms
    
    def _detect_languages(self, soup: BeautifulSoup) -> List[str]:
        """
        Detect available languages on website
        """
        
        languages = set()
        
        # Check HTML lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            lang = html_tag['lang'].split('-')[0].lower()
            languages.add(lang)
        
        # Check for language switcher links
        for link in soup.find_all('a', href=True):
            if link.get('hreflang'):
                lang = link['hreflang'].split('-')[0].lower()
                languages.add(lang)
            
            # Check for common language patterns
            text = link.get_text().strip().lower()
            href = link['href'].lower()
            
            lang_map = {
                'de': ['deutsch', 'german', '/de/', '/de-'],
                'en': ['english', 'englisch', '/en/', '/en-'],
                'fr': ['français', 'french', '/fr/', '/fr-'],
                'es': ['español', 'spanish', '/es/', '/es-'],
                'it': ['italiano', 'italian', '/it/', '/it-']
            }
            
            for lang_code, patterns in lang_map.items():
                if any(pattern in text or pattern in href for pattern in patterns):
                    languages.add(lang_code)
        
        return list(languages) if languages else ["de"]  # Default German
    
    def _count_pages(self, soup: BeautifulSoup) -> int:
        """
        Count internal pages
        """
        
        internal_links = set()
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Make absolute URL
            absolute_url = urljoin(self.url, href)
            
            # Check if internal link
            if urlparse(absolute_url).netloc == self.domain:
                # Remove anchors and query params
                clean_url = absolute_url.split('#')[0].split('?')[0]
                internal_links.add(clean_url)
        
        return len(internal_links)
    
    def _check_mobile(self, soup: BeautifulSoup) -> bool:
        """
        Check mobile responsiveness
        """
        
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return bool(viewport)
    
    def _find_contact_info(self, html_content: str) -> Dict:
        """
        Find contact information
        """
        
        # Email regex
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w{2,}', html_content)
        # Filter out common false positives
        emails = [e for e in emails if not any(x in e.lower() for x in ['example', 'domain', 'test', '@sentry'])]
        
        # Phone regex (German + International)
        phones = re.findall(
            r'(?:\+49|0049|0)\s*\d{2,4}[\s/-]?\d{3,}[\s/-]?\d{3,}',
            html_content
        )
        
        return {
            "emails": list(set(emails))[:3],  # Max 3 unique
            "phones": list(set(phones))[:3]   # Max 3 unique
        }
    
    def _get_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Get page title"""
        
        title = soup.find('title')
        return title.get_text().strip() if title else None
    
    def _get_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Get meta description"""
        
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta['content'].strip() if meta and meta.get('content') else None


# Test function
def test_crawler():
    """Test crawler with sample URLs"""
    
    test_urls = [
        "https://www.guesthouseholland.com",
        "https://adoro-aparthotel.com"
    ]
    
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"Testing: {url}")
        print('='*60)
        
        crawler = WebsiteCrawler(url)
        result = crawler.crawl()
        
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            continue
        
        print(f"✅ Status: {result['status_code']}")
        print(f"📄 Title: {result.get('title')}")
        print(f"🌐 Languages: {result.get('languages')}")
        print(f"🤖 Has Chatbot: {result.get('has_chatbot')}")
        if result.get('has_chatbot'):
            details = result.get('chatbot_details', {})
            print(f"   Type: {details.get('type')}")
            print(f"   Has Lead Form: {details.get('has_lead_form')}")
            print(f"   Priority: {details.get('priority')}")
        print(f"📝 Lead Forms: {len(result.get('lead_forms', []))}")
        print(f"📱 Mobile: {result.get('mobile_responsive')}")
        print(f"🔗 Pages: {result.get('pages_count')}")
        print(f"📧 Emails: {result.get('contact_info', {}).get('emails', [])}")
        print(f"⏱️  Response Time: {result.get('response_time_ms')}ms")


if __name__ == "__main__":
    test_crawler()
