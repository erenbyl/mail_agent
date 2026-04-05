# 🏭 Industrial-LLM: E-posta Otomasyon Ajanı

Bu proje, ** Sac Ticaret** için geliştirilmiş, yerel bir LLM (Llama 3.2) tarafından yönetilen akıllı bir e-posta asistanıdır. Sistem, gelen müşteri taleplerini analiz eder, envanter kontrolü yapar ve stokta bulunmayan ürünler için tedarikçilerle (supplier) iletişim sürecini otomatik olarak yönetir. [cite: 2026-02-11]



## 🚀 Öne Çıkan Özellikler

* **Akıllı Aracı (Broker) Modeli:** Ürün stokta yoksa tedarikçiye otomatik teknik talep (RFQ) gönderir ve gelen yanıtı kâr marjı ekleyerek müşteriye iletir. [cite: 2026-02-11]
* **Otomatik Kar Marjı Hesaplama:** LLM, tedarikçiden gelen ham fiyat metinlerini algılar ve belirlenen oran (örn: %10) üzerinden son müşteri fiyatını otomatik hesaplar. [cite: 2026-02-11]
* **Gelişmiş Takip Sistemi:** E-posta başlıklarındaki `Message-ID` ve `In-Reply-To` verilerini kullanarak asenkron mail trafiğini hatasız eşleştirir. [cite: 2026-02-11]
* **Müşteri Hafızası (CRM):** Müşterilerin geçmiş taleplerini ve verilen teklifleri hatırlar, kurumsal bir dille kişiselleştirilmiş yanıtlar üretir.
* **Yönetim Paneli:** Streamlit tabanlı arayüz üzerinden stok durumu, bekleyen talepler ve müşteri geçmişi görsel olarak takip edilebilir. [cite: 2026-02-11]

## 🛠️ Teknoloji Yığını

* **Dil:** Python 3.10+
* **AI:** Ollama (Llama 3.2 / GPT-OSS)
* **Arayüz:** Streamlit [cite: 2026-02-11]
* **Protokoller:** IMAP (Mail Okuma) & SMTP (Mail Gönderme)
* **Veri Yönetimi:** JSON (Envanter, Müşteri Verileri, Takip Dosyaları)

## 📁 Proje Yapısı

```text
mail_agent/
├── src/
│   ├── tracker.py          # Tedarikçi yanıtlarını takip eden modül
│   ├── llm_client.py       # Ollama API iletişimi ve prompt yönetimi
│   ├── stock_manager.py    # JSON tabanlı envanter kontrolü
│   └── customer_manager.py # Müşteri etkileşim geçmişi yönetimi
├── data/
│   ├── inventory.json      # Beyçelik güncel stok verileri
│   └── customers.json      # Müşteri konuşma kayıtları (Hafıza)
├── main.py                 # Arka planda çalışan mail motoru
├── app.py                  # Streamlit yönetim paneli (Dashboard)
├── pending_requests.json   # Aktif satıcı-müşteri eşleşmeleri
└── requirements.txt        # Gerekli kütüphaneler



Örnek Senaryo
Müşteri: "12mm Rulo Sac var mı?" diye sorar.

Ajan: Envanterde bulamazsa pending_requests.json'a kaydeder ve tedarikçiye mail atar. [cite: 2026-02-11]

Tedarikçi: "Ton fiyatı 680 USD" yanıtını döner.

Ajan: Fiyatı algılar, %10 kâr koyar ve müşteriye "748 USD" teklifini otomatik iletir. [cite: 2026-02-11]



Bağımlılıkları Yükleyin:
pip install -r requirements.txt


Ollama Sunucusunu Başlatın:
ollama serve
ollama pull llama3.2


Sistemi Başlatın:
Mail Motoru: python main.py --email
Yönetim Paneli: streamlit run app.py
