<<<<<<< HEAD
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
=======
# 🏗️ Industrial-LLM: Heavy Industry Email Automation Agent

Bu proje; ağır sanayi ve sac ticareti sektöründeki müşteri iletişim süreçlerini modernize etmek amacıyla geliştirilmiş, **Local LLM (Yerel Büyük Dil Modeli)** tabanlı bir uçtan uca otomasyon sistemidir. Sistem, gelen teknik e-postaları doğal dil işleme (NLP) yöntemleriyle analiz eder, dinamik bir JSON envanterini sorgular ve saniyeler içinde kurumsal standartlarda teknik yanıtlar üretir.



## 🌟 Öne Çıkan Özellikler

* **🛡️ Veri Gizliliği (Local LLM):** Şirket içi envanter ve müşteri verileri buluta çıkmadan, tüm işlemler **Ollama** üzerinden yerel makinede yürütülür.
* **🎯 Akıllı Niyet Analizi:** Filtreleme mekanizması sayesinde sadece "fiyat, stok, tonaj" gibi ticari niyet içeren mailler işlenir; alakasız içerikler elenir.
* **📊 Dinamik Envanter Entegrasyonu:** `inventory.json` tabanlı yapı ile stok miktarları, teknik kodlar (S355MC, GZR vb.) ve döviz bazlı fiyatlar anlık sorgulanır.
* **💼 Endüstriyel Terminoloji:** Yanıtlar; depo teslimi, fabrika sahası sevk ve ton bazlı fiyatlandırma gibi ağır sanayi standartlarına tam uyumludur.

## 🛠️ Teknoloji Yığını

| Katman | Teknoloji | Açıklama |
| :--- | :--- | :--- |
| **Programlama** | Python 3.10+ | Ana uygulama mantığı ve otomasyon döngüsü. |
| **Yapay Zeka** | Ollama / Llama 3.2 | Yerel çalışan, düşük gecikmeli dil modeli. |
| **Veri Yönetimi** | Dynamic JSON | Gerçek zamanlı envanter ve mağaza verisi yönetimi. |
| **Protokoller** | IMAP & SMTP | Gelen kutusu takibi ve otomatik yanıt iletimi. |



## ⚙️ Sistem Mimarisi

Sistem üç temel modül üzerinde kurgulanmıştır:

1.  **StockManager:** Envanter verilerini parse eder ve LLM için teknik bağlam (context) oluşturur.
2.  **OllamaClient:** Yerel LLM sunucusu ile API üzerinden iletişim kurarak yanıt üretimini yönetir.
3.  **EmailService:** Gmail üzerinden `UNSEEN` (okunmamış) mailleri tarih filtreli olarak tarar ve yanıt döngüsünü tetikler.

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimler
Sisteminizde **Ollama**'nın yüklü olduğundan emin olun ve gerekli modeli çekin:
```bash
ollama serve
ollama pull llama3.2:1b


EMAIL_USER = "isminiz@gmail.com"
EMAIL_PASS = "xxxx xxxx xxxx xxxx" # Gmail Uygulama Şifresi


# E-posta servis modunda çalıştırmak için:
python main.py --email



├── data/
│   └── inventory.json      # Teknik ürün, stok ve fiyat verileri
├── src/
│   ├── llm_client.py       # Ollama API ve model yönetimi
│   └── stock_manager.py    # Dinamik prompt ve envanter yönetimi
└── main.py                 # Ana giriş noktası ve servis döngüsü



>>>>>>> 19134b85abf2b231f95efa17ff7c83ab0ba7135f
