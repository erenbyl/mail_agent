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



