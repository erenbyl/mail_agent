# 📧 Otomatik E-posta Cevaplama ve Stok Kontrol Sistemi

Yerel LLM (Ollama) kullanarak müşteri e-postalarını analiz eden ve stok durumuna göre profesyonel yanıtlar üreten bir Python uygulaması.

## 🚀 Özellikler

- **Akıllı Stok Kontrolü**: LLM, envanter verilerini analiz ederek stok durumunu belirler
- **Profesyonel E-posta Yanıtları**: Müşterilere otomatik, nazik yanıtlar üretir
- **Yerel LLM Desteği**: Ollama ile llama3 veya mistral modelleri kullanır
- **Hata Yönetimi**: Kapsamlı try-except blokları ile güvenli çalışma
- **Modüler Yapı**: Temiz ve bakımı kolay kod mimarisi

## 📁 Proje Yapısı

```
email-stock-system/
├── data/
│   └── inventory.json      # Ürün veritabanı
├── src/
│   ├── __init__.py
│   ├── llm_client.py       # Ollama API istemcisi
│   └── stock_manager.py    # Stok yönetim modülü
├── main.py                 # Ana uygulama
├── requirements.txt        # Bağımlılıklar
└── README.md
```

## 📋 Gereksinimler

1. **Python 3.8+**
2. **Ollama** - [Kurulum](https://ollama.ai/)
3. **LLM Modeli** - llama3 veya mistral

## 🔧 Kurulum

### 1. Ollama Kurulumu

```bash
# Windows için Ollama'yı indirin ve kurun
# https://ollama.ai/download

# Model indirin
ollama pull llama3
# veya
ollama pull mistral
```

### 2. Python Bağımlılıkları

```bash
cd email-stock-system
pip install -r requirements.txt
```

## 🎮 Kullanım

### Demo Modu (Varsayılan)

```bash
python main.py
```

Örnek bir müşteri e-postasını işleyip sonucu gösterir.

### Etkileşimli Mod

```bash
python main.py --interactive
```

Kendi e-posta metinlerinizi girip test edebilirsiniz.

## 📦 Örnek Envanter

```json
{
  "products": [
    {"name": "iPhone 15 Pro", "quantity": 12, "price": 59999.99},
    {"name": "MacBook Air M3", "quantity": 8, "price": 54999.99},
    {"name": "Samsung Galaxy S24 Ultra", "quantity": 15, "price": 49999.99}
  ]
}
```

## 💡 Örnek Kullanım

**Girdi (Müşteri E-postası):**
```
Merhaba, iPhone 15 Pro ve MacBook Air var mı? Fiyatları nedir?
```

**Çıktı (LLM Yanıtı):**
```
Sayın Müşterimiz,

E-postanız için teşekkür ederiz.

Sorduğunuz ürünlerle ilgili bilgiler:

✅ iPhone 15 Pro: Stokta mevcuttur. Fiyatı: 59.999,99 TL
✅ MacBook Air M3: Stokta mevcuttur. Fiyatı: 54.999,99 TL

Siparişiniz için bizimle iletişime geçebilirsiniz.

Saygılarımızla,
TechStore Elektronik
```

## ⚠️ Hata Durumları

- **Ollama çalışmıyorsa**: `ollama serve` komutunu çalıştırın
- **Model bulunamadıysa**: `ollama pull llama3` ile indirin
- **Bağlantı hatası**: Ollama'nın 11434 portunda çalıştığını kontrol edin

## 📝 Lisans

MIT License
