"""
CHATPRO AI ANALYZER - BREVO CRM INTEGRATION
Automatically save leads to Brevo CRM
"""

import requests
from typing import Dict, Optional
from datetime import datetime

class BrevoCRM:
    """
    Brevo (formerly Sendinblue) CRM Integration
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "YOUR_BREVO_API_KEY"  # TODO: Add to env
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
        analysis_id: str
    ) -> Dict:
        """
        Save lead to Brevo CRM
        
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
                "ROI_MONAT": roi_monat,
                "HAS_CHATBOT": has_chatbot,
                "CHATBOT_PRIORITY": chatbot_priority,
                "ANALYZER_USED": True,
                "ANALYSIS_ID": analysis_id,
                "ANALYSIS_DATE": datetime.utcnow().strftime("%Y-%m-%d")
            },
            "listIds": [7],  # Google Ads Leads list (your existing list)
            "updateEnabled": True  # Update if exists
        }
        
        try:
            # Create/update contact
            response = requests.post(
                f"{self.base_url}/contacts",
                headers=self.headers,
                json=contact_data
            )
            
            if response.status_code in [201, 204]:
                # Success (201 = created, 204 = updated)
                return {
                    'status': 'success',
                    'action': 'created' if response.status_code == 201 else 'updated',
                    'contact_id': response.json().get('id') if response.status_code == 201 else None
                }
            else:
                return {
                    'status': 'failed',
                    'error': response.text,
                    'status_code': response.status_code
                }
                
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def add_tags(self, email: str, tags: list) -> Dict:
        """
        Add tags to contact
        
        Tags examples:
        - 'analyzer-hotel'
        - 'analyzer-fitness'
        - 'high-priority'
        - 'has-zendesk'
        """
        
        try:
            # Get contact first
            contact_response = requests.get(
                f"{self.base_url}/contacts/{email}",
                headers=self.headers
            )
            
            if contact_response.status_code != 200:
                return {'status': 'failed', 'error': 'Contact not found'}
            
            contact = contact_response.json()
            existing_tags = contact.get('tags', [])
            
            # Merge tags
            new_tags = list(set(existing_tags + tags))
            
            # Update contact
            response = requests.put(
                f"{self.base_url}/contacts/{email}",
                headers=self.headers,
                json={"tags": new_tags}
            )
            
            if response.status_code == 204:
                return {'status': 'success', 'tags': new_tags}
            else:
                return {'status': 'failed', 'error': response.text}
                
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def create_automation_trigger(
        self,
        email: str,
        event_name: str = "analyzer_completed",
        event_data: Optional[Dict] = None
    ) -> Dict:
        """
        Trigger Brevo automation
        
        This can trigger:
        - Follow-up email sequence
        - SMS notification
        - Slack notification
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/automation/webhooks/{event_name}",
                headers=self.headers,
                json={
                    "email": email,
                    "event_data": event_data or {}
                }
            )
            
            if response.status_code == 200:
                return {'status': 'success'}
            else:
                return {'status': 'failed', 'error': response.text}
                
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}


# Test function
def test_brevo_crm():
    """Test Brevo CRM integration"""
    
    crm = BrevoCRM()
    
    # Test save lead
    result = crm.save_lead(
        email="robert@chatproai.io",
        company_name="ADORO Aparthotel",
        website_url="https://adoro-aparthotel.com",
        industry="hotel",
        roi_monat=13180,
        has_chatbot=True,
        chatbot_priority="HIGH",
        analysis_id="abc123"
    )
    
    print("=== BREVO CRM RESULT ===")
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Action: {result['action']}")
        print(f"Contact ID: {result.get('contact_id', 'N/A')}")
    else:
        print(f"Error: {result.get('error')}")
    
    # Test add tags
    if result['status'] == 'success':
        tags_result = crm.add_tags(
            email="robert@chatproai.io",
            tags=["analyzer-hotel", "high-priority", "has-zendesk"]
        )
        print(f"\nTags Result: {tags_result['status']}")
        if tags_result['status'] == 'success':
            print(f"Tags: {tags_result['tags']}")


if __name__ == "__main__":
    test_brevo_crm()
