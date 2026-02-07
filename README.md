🏭 Automated Industrial Email Assistant
Bu proje, sanayi tipi sac ve çelik envanter yönetimi için geliştirilmiş, Ollama (Llama 3.2) tabanlı bir otomatik e-posta yanıt sistemidir. Müşterilerden gelen teknik stok sorgularını (GZR, RPKK, S355MC vb.) yerel bir yapay zeka modeli kullanarak analiz eder ve saniyeler içinde kurumsal bir dille yanıtlar.

🌟 Öne Çıkan Özellikler
Yerel Yapay Zeka (Local LLM): Veri gizliliğini korumak amacıyla tüm işlemler Ollama üzerinden yerel makinede yürütülür.

Akıllı Filtreleme: Sadece belirlenen ürün grupları ve "fiyat, stok, tonaj" gibi ticari niyet içeren e-postalar işleme alınır.

Dinamik Envanter Yönetimi: inventory.json dosyası üzerinden anlık stok ve USD bazlı fiyat kontrolü sağlanır.

Endüstriyel Terminoloji: Yanıtlar, ağır sanayi lojistik standartlarına (Depo teslimi, fabrika sahası sevk vb.) uygun şekilde üretilir.

🛠️ Teknik Yığın (Tech Stack)
Dil: Python 3.10+

Yapay Zeka: Ollama (Llama 3.2 1B / 3B)

Protokoller: IMAP (Gelen Posta), SMTP_SSL (Giden Posta)

Veri Yönetimi: JSON tabanlı dinamik envanter sistemi

🚀 Kurulum
Ollama Kurulumu: Yerel sunucunuzu başlatın ve gerekli modeli indirin:

Bash
ollama serve
ollama pull llama3.2:1b
Bağımlılıklar: Gerekli Python kütüphanelerini yükleyin:

Bash
pip install requests
Yapılandırma: main.py içerisindeki EMAIL_USER ve EMAIL_PASS alanlarını Gmail "Uygulama Şifresi" ile güncelleyin.

📈 Sistem Akışı
Sistem, belirli aralıklarla (CHECK_INTERVAL) gelen kutusunu tarar. Teknik bir sac sorgusu tespit edildiğinde, ürün bilgileri envanterden çekilir ve LLM tarafından şu formatta bir yanıt oluşturulur:

Sayın Müşterimiz, Erdemir Asitli S355MC RPKK kodlu ürünümüz 11.99 ton stokta olup, ton fiyatı 680 USD'dir. Depo teslimi yapılacaktır. Hayırlı işler dileriz.
