"""
LLM Client Modülü - Güncellenmiş
"""
import requests
from typing import Optional
def generate_decision(self, customer_email, inventory_json):
        system_prompt = f"""
        Sen bir ticaret uzmanısın. Envanteri kontrol et.
        ENVANTER: {inventory_json}
        
        KURAL:
        1. Ürün stokta VARSA: 'ACTION: REPLY_CUSTOMER' yaz ve teklif hazırla.
        2. Ürün stokta YOKSA: 'ACTION: ASK_SUPPLIER' yaz ve satıcıya gönderilecek teknik ürün detayını belirt.
        """
class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gpt-oss:120b-cloud"):
        self.base_url = base_url
        self.model = model
        self.generate_endpoint = f"{base_url}/api/generate"
    
    def check_connection(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.check_connection():
            raise ConnectionError("Ollama sunucusuna bağlanılamadı!")
        
        # /api/generate yerine /api/chat yapısını deneyelim
        chat_endpoint = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt if system_prompt else "Sen bir asistansın."},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {"temperature": 0.1}
        }
        
        # Zaman aşımı süresini (timeout) 300 saniyeye çıkarın (120B model yavaş olabilir)
        response = requests.post(chat_endpoint, json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "").strip()

def create_client(model: str = "gpt-oss:120b-cloud") -> OllamaClient:
    return OllamaClient(model=model)