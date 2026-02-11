import imaplib, smtplib, email, time, sys
import email.utils
from datetime import datetime
from email.mime.text import MIMEText
from email.header import decode_header
from src.llm_client import OllamaClient, create_client
from src.stock_manager import StockManager, load_stock_manager
from src.customer_manager import load_customer_manager
from src.tracker import InquiryTracker

# --- YAPILANDIRMA ---
EMAIL_USER = "erenboylu1111@gmail.com" 
EMAIL_PASS = "xxxx xxxx xxxx xxxx" 
SUPPLIER_EMAIL = "erenboylu1@gmail.com" 
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
CHECK_INTERVAL = 30 
PROFIT_MARGIN = 1.10 

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║    🏭 BEYÇELİK Sac Ticaret - Aracı Otomasyon Sistemi         ║ 
║                Powered by Yapay Zeka Topluluğu               ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def send_mail(to_email, subject, body, in_reply_to=None):
    """E-posta gönderir ve takip için oluşturulan benzersiz Message-ID'yi döner."""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    
    # Takip için benzersiz bir Message-ID oluşturuyoruz
    msg_id = email.utils.make_msgid(domain="gmail.com")
    msg['Message-ID'] = msg_id
    
    if in_reply_to:
        msg['In-Reply-To'] = in_reply_to
        msg['References'] = in_reply_to
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        return msg_id 
    except Exception as e:
        print(f"❌ Gönderim hatası: {e}")
        return None

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # Sadece düz metin kısımlarını al, ekleri (attachment) atla
            if content_type == "text/plain" and "attachment" not in content_disposition:
                charset = part.get_content_charset() # Karakter setini al
                payload = part.get_payload(decode=True)
                
                if charset:
                    try:
                        body = payload.decode(charset)
                    except:
                        body = payload.decode('utf-8', errors='ignore')
                else:
                    body = payload.decode('utf-8', errors='ignore')
                break
    else:
        charset = msg.get_content_charset()
        payload = msg.get_payload(decode=True)
        if charset:
            try:
                body = payload.decode(charset)
            except:
                body = payload.decode('utf-8', errors='ignore')
        else:
            body = payload.decode('utf-8', errors='ignore')
            
    return body.strip()

def process_email_logic(raw_body, sender_email, subject, llm_client, stock_manager, customer_manager, tracker):
    """Müşteriden gelen maili analiz eder ve duruma göre aksiyon alır."""
    inventory_data = stock_manager.get_inventory_json()
    history = customer_manager.get_customer_history(sender_email)

    system_prompt = f"""Sen Beyçelik'in profesyonel ticaret asistanısın.
ENVANTER: {inventory_data}
GEÇMİŞ: {history}

KURAL: 
1. Ürün stokta VARSA: Yanıtını 'ACTION: REPLY' ile başlat ve teklifini yaz.
2. Ürün stokta YOKSA: Yanıtını 'ACTION: ASK_SUPPLIER' ile başlat ve satıcıya gönderilecek teknik bilgi yaz.
Sen Beyçelik firmasının satın alma sorumlususun. Görevin: Satıcıdan sadece fiyat ve termin almak. Kural: Asla tablo, uzun listeler veya CE belgesi gibi gereksiz detaylara girme. Sadece müşterinin sorduğu ürünü (kalınlık, kalite, miktar) sor ve fiyat iste. Mailin sonunda imza olarak sadece 'Beyçelik Sac Ticaret' kullan.
"""
    
    ai_response = llm_client.generate_response(prompt=raw_body, system_prompt=system_prompt)

    if "ACTION: ASK_SUPPLIER" in ai_response:
        print(f"🔍 Stokta yok, satıcıya soruluyor: {sender_email}")
        clean_msg = ai_response.replace("ACTION: ASK_SUPPLIER", "").strip()
        # Satıcıya sorarken subject'i koruyoruz ki cevap geldiğinde eşleşsin
        msg_id = send_mail(SUPPLIER_EMAIL, f"Fiyat Talebi: {subject}", clean_msg)
        tracker.add_pending(msg_id, sender_email, subject, raw_body)
    else:
        print(f"✅ Stokta var, müşteriye dönülüyor.")
        final_text = ai_response.replace("ACTION: REPLY", "").strip()
        send_mail(sender_email, f"Re: {subject}", final_text)
        customer_manager.add_interaction(sender_email, raw_body, final_text)

def run_email_service():
    print_banner()
    today = datetime.now().strftime("%d-%b-%Y")
    
    stock_manager = load_stock_manager()
    customer_manager = load_customer_manager()
    tracker = InquiryTracker()
    llm_client = create_client(model="gpt-oss:120b-cloud")
    
    intents = ["fiyat", "ton", "sac", "plaka", "rulo", "galvaniz", "teklif", "stok"]

    while True:
        try:
            print(f"🔍 {datetime.now().strftime('%H:%M:%S')} - Yeni mailler taranıyor...")
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(EMAIL_USER, EMAIL_PASS)
            mail.select("inbox")
            
            _, messages = mail.search(None, f'(UNSEEN ON "{today}")')
            for e_id in messages[0].split():
                _, data = mail.fetch(e_id, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                
                sender_header = msg.get("From")
                sender_email = sender_header.split("<")[1].strip(">") if "<" in sender_header else sender_header
                subject_decoded = decode_header(msg["Subject"])[0]
                subject = subject_decoded[0]
                if isinstance(subject, bytes): subject = subject.decode(subject_decoded[1] or "utf-8")
                
                raw_body = get_email_body(msg)
                
                # DURUM 1: SATICIDAN CEVAP GELDİ Mİ?
                if sender_email.lower() == SUPPLIER_EMAIL.lower():
                    reply_id = msg.get("In-Reply-To")
                    print(f"DEBUG: Satıcıdan mail geldi. Aranan ID: {reply_id}")
                    
                    pending = tracker.get_pending(reply_id)
                    if pending:
                        print(f"📦 Eşleşme bulundu: {pending['customer_email']}")
                        
                        prompt = f"""
                        MÜŞTERİ TALEBİ: {pending['product']}
                        SATICIDAN GELEN CEVAP: {raw_body}
                        KAR MARJI: {PROFIT_MARGIN}
                        
                        GÖREV:
                        1. Satıcının verdiği birim fiyatı tespit et.
                        2. Bu fiyatı {PROFIT_MARGIN} ile çarparak müşteriye sunulacak SON fiyatı hesapla.
                        3. Metin içinde hesaplama formülünü (650*1.1 gibi) DEĞİL, sadece sonucu yaz.
                        4. Müşteriye profesyonel bir teklif yanıtı hazırla.
                        Sen Beyçelik'in satış temsilcisisin. Görevin: Müşteriye kâr eklenmiş fiyatı iletmek. Kural: Asla hesaplama formülünü (720*1.1 gibi) yazma. Tablo kullanma. Gereksiz teknik detaylara (yüzey durumu, CE vb.) girme. Sadece fiyatı ve termin süresini söyleyip onay iste. Samimi ama profesyonel bir dil kullan.
                        """
                        
                        cust_response = llm_client.generate_response(prompt=prompt, system_prompt="Beyçelik Satış Temsilcisi")
                        send_mail(pending['customer_email'], f"Re: {pending['subject']}", cust_response)
                        customer_manager.add_interaction(pending['customer_email'], pending['product'], cust_response)
                        tracker.mark_completed(reply_id)
                    else:
                        print(f"⚠️ Satıcıdan mail geldi ama takip ID'si bulunamadı: {reply_id}")
                
                # DURUM 2: MÜŞTERİDEN MAİL Mİ GELDİ?
                elif any(i in raw_body.lower() for i in intents):
                    process_email_logic(raw_body, sender_email, subject, llm_client, stock_manager, customer_manager, tracker)

            mail.logout()
        except Exception as e:
            print(f"⚠️ Hata: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if "--email" in sys.argv:
        run_email_service()
    else:
        print("❌ Hata: Lütfen '--email' parametresini kullanın.")