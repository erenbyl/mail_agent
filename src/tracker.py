import json
import os
from pathlib import Path
from datetime import datetime

class InquiryTracker:
    def __init__(self, data_path=None):
        if data_path is None:
            # Proje ana dizinindeki pending_requests.json'u hedef alır
            base_dir = Path(__file__).parent.parent
            self.data_path = base_dir / "pending_requests.json"
        else:
            self.data_path = Path(data_path)
            
        self.requests = {}
        self._load()

    def _load(self):
        """Dosyadan verileri yükler, dosya yoksa boş sözlük oluşturur."""
        if self.data_path.exists():
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    self.requests = json.load(f)
            except Exception as e:
                print(f"⚠️ Takip dosyası yükleme hatası: {e}")
                self.requests = {}
        else:
            self._save()

    def _save(self):
        """Verileri JSON dosyasına kaydeder."""
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.requests, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Takip dosyası kaydetme hatası: {e}")

    def add_pending(self, supplier_msg_id, customer_email, original_subject, product):
        """Müşteri talebini satıcı mesaj ID'si ile eşleştirerek kaydeder."""
        # supplier_msg_id bazen None gelebilir, kontrol edelim
        if not supplier_msg_id:
            supplier_msg_id = f"manual_{datetime.now().timestamp()}"

        self.requests[str(supplier_msg_id)] = {
            "customer_email": customer_email,
            "subject": original_subject,
            "product": product,
            "status": "waiting_supplier",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._save()
        print(f"💾 Talep takip listesine eklendi (ID: {supplier_msg_id})")

    def get_pending(self, reply_id):
        """ID'ye göre bekleyen talebi getirir (ID temizleme eklenmiştir)."""
        if not reply_id:
            return None
        
        clean_id = str(reply_id).strip()
        # Hem <ID> hem de ID formatını kontrol et
        res = self.requests.get(clean_id)
        if not res and not clean_id.startswith("<"):
            res = self.requests.get(f"<{clean_id}>")
        return res
    
    def mark_completed(self, msg_id):
        """İşlemi tamamlanmış olarak işaretler."""
        if str(msg_id) in self.requests:
            self.requests[str(msg_id)]["status"] = "completed"
            self._save()