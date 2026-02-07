"""
LLM Client Modülü - Güncellenmiş
"""
import requests
from typing import Optional

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
            raise ConnectionError("Ollama sunucusuna bağlanılamadı! 'ollama serve' açık mı?")
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1  # Yaratıcılığı kısıp tutarlılığı artırır
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        response = requests.post(self.generate_endpoint, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "").strip()

def create_client(model: str = "gpt-oss:120b-cloud") -> OllamaClient:
    return OllamaClient(model=model)