import imaplib
import smtplib
import email
import time
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.header import decode_header
from src.llm_client import OllamaClient, create_client
from src.stock_manager import StockManager, load_stock_manager

# --- E-POSTA YAPILANDIRMASI ---
EMAIL_USER = "erenboylu1111@gmail.com" 
EMAIL_PASS = "eyac kdkl eqlg botk"  # Google Uygulama Şifresi
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
CHECK_INTERVAL = 30  # Saniye bazında kontrol aralığı

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║     🏭 BEYÇELİK Sac Ticaret - Otomatik Yanıt Sistemi         ║
║                Powered by Ollama & Eren Boylu                ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def send_email_reply(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = f"Re: {subject}"
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"✅ Yanıt gönderildi: {to_email}")
    except Exception as e:
        print(f"❌ Mail gönderme hatası: {e}")

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode(errors='ignore')
                break
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')
    return body

def process_customer_email(customer_email: str, llm_client: OllamaClient, stock_manager: StockManager) -> str:
    """Müşteri e-postasını analiz eder ve Beyçelik standartlarında yanıt üretir."""
    inventory_data = stock_manager.get_inventory_json()
    system_prompt = f"""Sen Beyçelik firmasının profesyonel satış temsilcisisin. 
Aşağıdaki envanter verisini kullanarak sac/çelik taleplerine yanıt ver.

ENVANTER:
{inventory_data}

KURALLAR:
1. Cevabına "Sayın müşterimiz," diye başla ve "Hayırlı işler dileriz." diye bitir.
2. SADECE envanterdeki teknik verileri (Tonaj, Fiyat $, Yükleme Yeri) kullan.
3. Fiyatlar ton başınadır ve Amerikan Doları ($) cinsindendir.
4. Asla "Özdemir" veya "Ahmet" gibi isimlerle imza atma.
5. Teknik terimleri (GZR, RPKK, S355MC) doğru kullan.
6. Müşterinin talebine göre en uygun ürünü öner.
7. Amacın sadece ürün hakkında bilgi vermek. ürünü depoya yüklüyoruz tarzında şeyler söyleme.
8. Tonaj, Fiyat $, Yükleme Yeri dışında bilgi verme. Müşteri sorarsa bile başka bilgileri paylaşma.
"""

    user_prompt = f"Müşteri mesajı:\n{customer_email}"
    print("⏳ LLM yanıt üretiyor...")
    return llm_client.generate_response(prompt=user_prompt, system_prompt=system_prompt)

def run_email_service():
    print_banner()
    today = datetime.now().strftime("%d-%b-%Y")
    print(f"🚀 Servis Aktif. Sadece {today} tarihli mailler işleniyor...")
    
    try:
        stock_manager = load_stock_manager()
        llm_client = create_client(model="gpt-oss:120b-cloud") # Ollama'daki model isminle eşleşmeli
        
        intents = ["fiyat", "ton", "sac", "plaka", "rulo", "galvaniz", "teklif", "stok", "usd"]
        brands = [p['name'].split()[0].lower() for p in stock_manager.get_products()]

        while True:
            try:
                print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Yeni mailler taranıyor...")
                mail = imaplib.IMAP4_SSL(IMAP_SERVER)
                mail.login(EMAIL_USER, EMAIL_PASS)
                mail.select("inbox")

                search_criteria = f'(UNSEEN ON "{today}")'
                _, messages = mail.search(None, search_criteria)
                email_ids = messages[0].split()

                if email_ids:
                    print(f"📩 {len(email_ids)} yeni mesaj bulundu.")
                    for e_id in email_ids:
                        _, data = mail.fetch(e_id, '(RFC822)')
                        msg = email.message_from_bytes(data[0][1])
                        
                        subject_header = decode_header(msg["Subject"])[0]
                        subject = subject_header[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(subject_header[1] or "utf-8")
                        
                        sender = msg.get("From")
                        raw_body = get_email_body(msg)
                        content_lower = raw_body.lower()

                        # Filtreleme
                        is_relevant = any(i in content_lower for i in intents) or \
                                      any(b in content_lower for b in brands)

                        if is_relevant:
                            print(f"📧 İşleniyor: {subject} ({sender})")
                            response = process_customer_email(raw_body, llm_client, stock_manager)
                            send_email_reply(sender, subject, response)
                        else:
                            print(f"⏭️ Alakasız: {subject}")
                
                mail.logout()
            except Exception as e:
                print(f"⚠️ Hata: {e}")
            
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n👋 Kapatılıyor...")

if __name__ == "__main__":
    if "--email" in sys.argv:
        run_email_service()
    else:
        print("❌ Hata: Lütfen '--email' parametresini kullanın.")