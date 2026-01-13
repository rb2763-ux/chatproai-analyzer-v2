"""
ChatPro AI - Website Crawler
VERSION 3.0 - FIXED CHATBOT DETECTION
- Stricter chatbot detection (nur echte Widget-Scripts)
- Keine False Positives mehr bei Text-Erwähnungen
- Zimmerzahl-Extraktion aus Content
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin
import re
import time
import logging

logger = logging.getLogger(__name__)


class WebsiteCrawler:
    """
    Lightweight website crawler using requests + BeautifulSoup

    Features:
    - STRICT Chatbot detection (nur Widget-Scripts, keine Text-Erwähnungen)
    - Zimmerzahl-Extraktion
    - Lead form detection
    - Language detection
    - Contact information extraction
    
    Version: 3.0 - Fixed false positive chatbot detection
    """

    def __init__(self, timeout: int = 30):
        """
        Initialize crawler without URL (URL provided per crawl)

        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout

        # Chatbot signatures - NUR SCRIPT/EMBED URLS, NICHT TEXT!
        self.chatbot_signatures = {
            "zendesk": ["zdassets.com", "zendesk.com/embeddable"],
            "tidio": ["tidio.co/script", "tidiochat"],
            "intercom": ["widget.intercom.io", "intercom.io/widget"],
            "drift": ["js.driftt.com", "drift.com/include"],
            "livechat": ["cdn.livechatinc.com", "livechatinc.com/tracking"],
            "freshchat": ["wchat.freshchat.com", "freshchat.com/js"],
            "tawk.to": ["embed.tawk.to"],
            "chatbot.com": ["chatbot.com/widget"],
            "hubspot": ["js.hs-scripts.com/conversations"],
            "crisp": ["client.crisp.chat"],
            "smartsupp": ["smartsupp.com/widget"]
        }

    async def crawl(self, url: str) -> Dict:
        """
        Main crawl method

        Args:
            url: Website URL to crawl

        Returns:
            Dict with crawl results
        """
        try:
            # Make request
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={"User-Agent": "ChatProAI-Analyzer/3.0"}
            )
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
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
                "chatbot_type": None,
                "chatbot_details": {},
                "room_count": self._extract_room_count(html_content, soup),  # NEU!
                "lead_forms": self._find_lead_forms(soup),
                "pages_count": self._count_pages(soup),
                "mobile_responsive": self._check_mobile(soup),
                "contact_info": self._find_contact_info(html_content),
                "response_time_ms": int(response.elapsed.total_seconds() * 1000)
            }

            # Detect chatbot - V3.0 STRICT MODE
            chatbot_info = self._detect_chatbot_strict(html_content, soup)
            analysis["has_chatbot"] = chatbot_info["has_chatbot"]
            analysis["chatbot_type"] = chatbot_info.get("chatbot_type")
            analysis["chatbot_details"] = chatbot_info

            logger.info(f"Crawl complete: {url}")
            logger.info(f"  - Has chatbot: {analysis['has_chatbot']}")
            logger.info(f"  - Chatbot type: {analysis['chatbot_type']}")
            logger.info(f"  - Room count: {analysis['room_count']}")

            return analysis

        except requests.exceptions.Timeout:
            logger.error(f"Timeout crawling {url}")
            return {
                "url": url,
                "error": "Timeout",
                "error_message": f"Request timed out after {self.timeout} seconds"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error crawling {url}: {str(e)}")
            return {
                "url": url,
                "error": "RequestException",
                "error_message": str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error crawling {url}: {str(e)}")
            return {
                "url": url,
                "error": "UnexpectedException",
                "error_message": str(e)
            }

    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else ""

    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        return meta_desc.get('content', '') if meta_desc else ""

    def _detect_languages(self, soup: BeautifulSoup) -> List[str]:
        """Detect website languages"""
        languages = []

        # Check html lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            languages.append(html_tag['lang'][:2])

        # Check meta tags
        for meta in soup.find_all('meta'):
            if 'lang' in meta.attrs:
                languages.append(meta['lang'][:2])

        return list(set(languages)) if languages else ["en"]

    def _detect_chatbot_strict(self, html_content: str, soup: BeautifulSoup) -> Dict:
        """
        STRICT Chatbot Detection - V3.0
        
        Only detects REAL chatbot widgets by checking:
        1. Script tags with chatbot CDN URLs
        2. Iframe embeds with chatbot domains
        3. NOT plain text mentions of "chatbot"
        
        Returns:
            Dict with has_chatbot, chatbot_type, signature_found
        """
        
        # STEP 1: Check <script> tags for chatbot CDN URLs
        for script in soup.find_all('script'):
            src = script.get('src', '')
            if src:
                for chatbot_type, signatures in self.chatbot_signatures.items():
                    for signature in signatures:
                        if signature in src:
                            logger.info(f"✅ CHATBOT FOUND: {chatbot_type} via <script src='{src}'>")
                            return {
                                "has_chatbot": True,
                                "chatbot_type": chatbot_type,
                                "signature_found": signature,
                                "detection_method": "script_src"
                            }
        
        # STEP 2: Check inline <script> content for widget initialization
        for script in soup.find_all('script'):
            script_content = script.string
            if script_content:
                script_lower = script_content.lower()
                
                # Check for specific widget initialization patterns
                widget_patterns = {
                    "zendesk": ["window.$zopim", "ze('webwidget'", "zopim.livechat"],
                    "tidio": ["tidiochatapi", "document.tidiochat"],
                    "intercom": ["window.intercom(", "intercom('boot'"],
                    "drift": ["drift.load(", "drift.on("],
                    "tawk.to": ["tawk_", "tawk.to"],
                    "crisp": ["window.$crisp", "crisp.push"],
                    "smartsupp": ["smartsupp(", "_smartsupp"]
                }
                
                for chatbot_type, patterns in widget_patterns.items():
                    for pattern in patterns:
                        if pattern in script_lower:
                            logger.info(f"✅ CHATBOT FOUND: {chatbot_type} via inline script pattern '{pattern}'")
                            return {
                                "has_chatbot": True,
                                "chatbot_type": chatbot_type,
                                "signature_found": pattern,
                                "detection_method": "inline_script"
                            }
        
        # STEP 3: Check <iframe> embeds
        for iframe in soup.find_all('iframe'):
            src = iframe.get('src', '')
            if src:
                for chatbot_type, signatures in self.chatbot_signatures.items():
                    for signature in signatures:
                        if signature in src:
                            logger.info(f"✅ CHATBOT FOUND: {chatbot_type} via <iframe src='{src}'>")
                            return {
                                "has_chatbot": True,
                                "chatbot_type": chatbot_type,
                                "signature_found": signature,
                                "detection_method": "iframe_embed"
                            }
        
        # NO CHATBOT FOUND
        logger.info("❌ NO CHATBOT DETECTED (strict mode)")
        return {
            "has_chatbot": False,
            "chatbot_type": None,
            "detection_method": None
        }

    def _extract_room_count(self, html_content: str, soup: BeautifulSoup) -> Optional[int]:
        """
        Extract room/unit count from website content
        
        Looks for patterns like:
        - "17 Zimmer"
        - "20 rooms"
        - "5 Ferienwohnungen"
        - "30 units"
        
        Returns:
            int: Number of rooms/units, or None if not found
        """
        
        # Patterns to search for
        patterns = [
            r'(\d+)\s+zimmer',
            r'(\d+)\s+rooms?',
            r'(\d+)\s+einheiten',
            r'(\d+)\s+units?',
            r'(\d+)\s+ferienwohnungen?',
            r'(\d+)\s+apartments?',
            r'(\d+)\s+suites?',
            r'(\d+)\s+accommodations?'
        ]
        
        html_lower = html_content.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, html_lower)
            if matches:
                # Take first match and convert to int
                try:
                    room_count = int(matches[0])
                    # Sanity check: between 1 and 500 rooms
                    if 1 <= room_count <= 500:
                        logger.info(f"✅ ROOM COUNT FOUND: {room_count} (pattern: {pattern})")
                        return room_count
                except ValueError:
                    continue
        
        logger.info("❌ NO ROOM COUNT DETECTED")
        return None

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
                input_data = {
                    "type": input_tag.get('type', input_tag.name),
                    "name": input_tag.get('name', ''),
                    "placeholder": input_tag.get('placeholder', '')
                }
                form_data["inputs"].append(input_data)

            if form_data["inputs"]:
                forms.append(form_data)

        return forms

    def _count_pages(self, soup: BeautifulSoup) -> int:
        """Estimate number of pages by counting internal links"""
        internal_links = set()

        for link in soup.find_all('a', href=True):
            href = link['href']
            # Filter internal links
            if href.startswith('/') or href.startswith('#'):
                internal_links.add(href)

        return len(internal_links)

    def _check_mobile(self, soup: BeautifulSoup) -> bool:
        """Check if website is mobile responsive"""
        # Check viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            content = viewport.get('content', '').lower()
            if 'width=device-width' in content:
                return True

        # Check for responsive CSS
        for link in soup.find_all('link', rel='stylesheet'):
            if 'responsive' in link.get('href', '').lower():
                return True

        return False

    def _find_contact_info(self, html_content: str) -> Dict:
        """Extract contact information"""
        contact = {
            "emails": [],
            "phones": [],
            "social_media": []
        }

        # Email pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        contact["emails"] = list(set(re.findall(email_pattern, html_content)))

        # Phone pattern (international)
        phone_pattern = r'[\+\(]?[0-9][0-9\s\-\(\)]{7,}[0-9]'
        contact["phones"] = list(set(re.findall(phone_pattern, html_content)))

        # Social media
        social_patterns = {
            "facebook": r'facebook\.com/[\w\-\.]+',
            "instagram": r'instagram\.com/[\w\-\.]+',
            "twitter": r'twitter\.com/[\w\-\.]+',
            "linkedin": r'linkedin\.com/[\w\-\./]+'
        }

        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, html_content)
            if matches:
                contact["social_media"].extend([f"https://{m}" for m in matches])

        return contact


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def test():
        crawler = WebsiteCrawler()
        
        # Test with Engel Sasbachwalden
        print("\n" + "="*80)
        print("Testing: Hotel Engel Sasbachwalden")
        print("="*80)
        
        result = await crawler.crawl("https://engel-sasbachwalden.de/")
        
        print(f"\n✅ Crawl Results:")
        print(f"   Title: {result.get('title')}")
        print(f"   Has Chatbot: {result.get('has_chatbot')}")
        print(f"   Chatbot Type: {result.get('chatbot_type')}")
        print(f"   Room Count: {result.get('room_count')}")
        print(f"   Mobile Responsive: {result.get('mobile_responsive')}")
        print(f"   Languages: {result.get('languages')}")
        
        if result.get('has_chatbot'):
            print(f"\n   Chatbot Details:")
            print(f"      - Type: {result['chatbot_details'].get('chatbot_type')}")
            print(f"      - Detection: {result['chatbot_details'].get('detection_method')}")
            print(f"      - Signature: {result['chatbot_details'].get('signature_found')}")
    
    asyncio.run(test())
