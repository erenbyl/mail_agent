import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class CustomerManager:
    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            # data/customers.json yolunu ayarla
            base_dir = Path(__file__).parent.parent
            self.data_path = base_dir / "data" / "customers.json"
        else:
            self.data_path = Path(data_path)
            
        self.customers: Dict = {}
        self._load_data()

    def _load_data(self):
        """Müşteri veritabanını yükler, yoksa oluşturur."""
        if not self.data_path.exists():
            self._save_data()  # Boş dosya oluştur
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.customers = json.load(f)
        except Exception as e:
            print(f"⚠️ Müşteri verisi yüklenirken hata: {e}")
            self.customers = {}

    def _save_data(self):
        """Verileri JSON dosyasına yazar."""
        # Klasör yoksa oluştur
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(self.customers, f, ensure_ascii=False, indent=2)

    def get_customer_history(self, email: str, limit: int = 3) -> str:
        """
        Bir müşterinin geçmiş konuşmalarını LLM için metin formatına çevirir.
        limit: Son kaç mesajın hatırlanacağı.
        """
        if email not in self.customers:
            return "Bu müşteriyle daha önce hiç konuşulmadı (Yeni Müşteri)."
        
        history = self.customers[email]["history"][-limit:] # Son X mesajı al
        context_str = ""
        for interaction in history:
            context_str += f"- Tarih: {interaction['date']}\n"
            context_str += f"  Müşteri: {interaction['message']}\n"
            context_str += f"  Bizim Cevabımız: {interaction['response']}\n"
            context_str += "---\n"
            
        return context_str

    def add_interaction(self, email: str, message: str, response: str):
        """Yeni bir konuşmayı veritabanına kaydeder."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if email not in self.customers:
            # Yeni müşteri kaydı
            print(f"🆕 Yeni müşteri veritabanına ekleniyor: {email}")
            self.customers[email] = {
                "first_seen": timestamp,
                "history": []
            }
        
        # Etkileşimi kaydet
        self.customers[email]["history"].append({
            "date": timestamp,
            "message": message.strip(),
            "response": response.strip()
        })
        
        self._save_data()

def load_customer_manager():
    return CustomerManager()