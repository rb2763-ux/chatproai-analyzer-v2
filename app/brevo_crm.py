"""
CHATPRO AI ANALYZER - BREVO CRM INTEGRATION
Automatically save leads to Brevo CRM
"""

import requests
import os
from typing import Dict, Optional
from datetime import datetime

class BrevoCRM:
    """
    Brevo (formerly Sendinblue) CRM Integration
    """
    
    def __init__(self, api_key: Optional[str] = None, list_id: Optional[int] = None):
        self.api_key = api_key or os.getenv("BREVO_API_KEY")
        self.list_id = list_id or int(os.getenv("BREVO_LIST_ID", "4"))
        self.base_url = "https://api.brevo.com/v3"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": self.api_key
        }
    
    def save_lead(
        self,
        email: str,
        company_name: str,
        website_url: str,
        industry: str,
        roi_monat: int,
        has_chatbot: bool,
        chatbot_priority: str,
        analysis_id: str,
        chatbot_type: str = ""
    ) -> Dict:
        """
        Save lead to Brevo CRM
        
        Args:
            email: Contact email
            company_name: Company name
            website_url: Website URL
            industry: Industry (hotel, restaurant, etc.)
            roi_monat: Monthly ROI in EUR
            has_chatbot: Has existing chatbot
            chatbot_priority: Priority (HIGH/MEDIUM/LOW)
            analysis_id: Analysis ID
            chatbot_type: Type of chatbot (Zendesk, Tidio, etc.)
            
        Returns:
            Dict with status and contact_id
        """
        
        # Extract first/last name from company_name
        name_parts = company_name.split()
        first_name = name_parts[0] if name_parts else company_name
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        
        # Prepare contact data
        contact_data = {
            "email": email,
            "attributes": {
                "FIRSTNAME": first_name,
                "LASTNAME": last_name,
                "WEBSITE": website_url,
                "BRANCHE": industry.capitalize(),
                "ROI_MONAT": int(roi_monat),
                "HAS_CHATBOT": has_chatbot,
                "CHATBOT_TYPE": chatbot_type if chatbot_type else "None",
                "CHATBOT_PRIORITY": chatbot_priority,
                "ANALYZER_USED": True,
                "ANALYSIS_ID": analysis_id,
                "ANALYSIS_DATE": datetime.utcnow().strftime("%Y-%m-%d")
            },
            "listIds": [self.list_id],
            "updateEnabled": True  # Update if exists
        }
        
        # Prepare tags based on data
        tags = [
            f"analyzer-{industry.lower()}",
        ]
        
        if has_chatbot:
            tags.append("has-chatbot")
            if chatbot_type:
                tags.append(f"has-{chatbot_type.lower()}")
        
        if chatbot_priority == "HIGH":
            tags.append("high-priority")
        elif chatbot_priority == "MEDIUM":
            tags.append("medium-priority")
        else:
            tags.append("low-priority")
        
        try:
            # Create/update contact
            response = requests.post(
                f"{self.base_url}/contacts",
                headers=self.headers,
                json=contact_data,
                timeout=10
            )
            
            if response.status_code in [201, 204]:
                # Success (201 = created, 204 = updated)
                contact_id = None
                action = 'updated'
                
                if response.status_code == 201:
                    action = 'created'
                    try:
                        contact_id = response.json().get('id')
                    except:
                        pass
                
                # Add tags (separate API call)
                try:
                    self._add_tags(email, tags)
                except:
                    pass  # Tags are optional
                
                return {
                    'status': 'success',
                    'action': action,
                    'contact_id': contact_id,
                    'tags_added': tags
                }
            else:
                # Error
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    pass
                
                return {
                    'status': 'error',
                    'error': f"Brevo API error ({response.status_code}): {error_msg}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'status': 'error',
                'error': 'Brevo API timeout'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _add_tags(self, email: str, tags: list) -> bool:
        """
        Add tags to contact (internal helper)
        """
        try:
            # Get contact ID first
            response = requests.get(
                f"{self.base_url}/contacts/{email}",
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                contact_id = response.json().get('id')
                
                # Add tags
                tag_response = requests.put(
                    f"{self.base_url}/contacts/{contact_id}",
                    headers=self.headers,
                    json={"tags": tags},
                    timeout=5
                )
                
                return tag_response.status_code in [200, 204]
        except:
            pass
        
        return False
