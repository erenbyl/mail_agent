"""
Stok Yönetim Modülü - Güncellenmiş
"""
import json
from typing import Dict, Any, Optional
from pathlib import Path

class StockManager:
    def __init__(self, inventory_path: Optional[str] = None):
        if inventory_path is None:
            base_dir = Path(__file__).parent.parent
            self.inventory_path = base_dir / "data" / "inventory.json"
        else:
            self.inventory_path = Path(inventory_path)
        
        self.inventory_data: Dict[str, Any] = {}
        self._load_inventory()
    
    def _load_inventory(self) -> None:
        try:
            with open(self.inventory_path, 'r', encoding='utf-8') as f:
                self.inventory_data = json.load(f)
            print(f"✅ Envanter başarıyla yüklendi: {self.inventory_path}")
        except Exception as e:
            print(f"❌ Envanter yükleme hatası: {e}")

    def get_inventory_json(self) -> str:
        return json.dumps(self.inventory_data, ensure_ascii=False, indent=2)
    
    def get_products(self) -> list:
        return self.inventory_data.get("products", [])
    
    def get_store_info(self) -> Dict[str, str]:
        return self.inventory_data.get("store_info", {})

def create_system_prompt(self) -> str:
    store_info = self.get_store_info()
    inventory_json = self.get_inventory_json()
    
    return f"""Sen {store_info.get('name')} firmasının profesyonel satış temsilcisisin.
2003'den beri sac ve çelik sektöründe hizmet veriyoruz.

## GÖREV
Aşağıdaki teknik envanter verisini kullanarak sac/rulo taleplerine yanıt ver.

## TEKNİK BİLGİLER
- Ürün Listesi (JSON): {inventory_json}

## KURALLAR
1. SADECE listedeki ürünler hakkında bilgi ver.
2. Müşteriye "Tonaj", "Fiyat ($)", "Kalite" ve "Yükleme Yeri" bilgilerini net paylaş.
3. Fiyatlar ton başınadır ve Amerikan Doları ($) cinsindendir.
4. Yanıtı "Sayın Müşterimiz," ile başlat ve "Hayırlı işler dileriz." ile bitir.
5. Teknik bir dil kullan (Örn: "Erdemir Galvaniz A2 kalitede stok mevcuttur").

## İMZA
{store_info.get('name')}
Tel: {store_info.get('phone')}
"""

def load_stock_manager(inventory_path=None):
    return StockManager(inventory_path)

