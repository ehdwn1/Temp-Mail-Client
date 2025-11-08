from curl_cffi import requests
from typing import Optional, Dict, Any

class mailbox:    
    BASE_URL = "https://web2.temp-mail.org"
    IMPERSONATE = "chrome110"
    
    def __init__(self, token: Optional[str] = None, mailbox: Optional[str] = None):
        if token and mailbox:
            self.token = token
            self._mailbox = mailbox
        else:
            self._create_mailbox()
    
    def _create_mailbox(self) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/mailbox"
        response = requests.post(url, impersonate=self.IMPERSONATE)
        
        if response.status_code != 200:
            raise Exception(f"Failed to create mailbox: {response.status_code}")
        
        data = response.json()
        self.token = data.get("token")
        self._mailbox = data.get("mailbox")
        
        return data
    
    @property
    def email(self) -> Optional[str]:
        return self._mailbox
    
    def get_mailbox_url(self) -> Optional[str]:
        if not self.token:
            return None
        return f"https://temp-mail.org/en/?token={self.token}"
    
    def get_messages(self) -> Dict[str, Any]:
        if not self.token:
            raise Exception("Token is required. Please call create_mailbox() first.")
        
        url = f"{self.BASE_URL}/messages"
        headers = {
            "authorization": f"Bearer {self.token}",
        }
        
        response = requests.get(url, headers=headers, impersonate=self.IMPERSONATE)
        
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve messages: {response.status_code}")

        data = response.json()
        messages = data.get("messages")
        return messages
    
    def get_token(self) -> Optional[str]:
        return self.token
    
    def get_mailbox(self) -> Optional[str]:
        return self._mailbox

