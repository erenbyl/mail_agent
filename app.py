import streamlit as st
import json
import pandas as pd
from pathlib import Path

import subprocess
import threading

# Mail servisini arka planda (ayrı bir thread'de) çalıştıran fonksiyon
def start_mail_engine():
    subprocess.Popen(["python", "main.py", "--email"])

# Uygulama açıldığında bir kez çalıştır
if "engine_started" not in st.session_state:
    threading.Thread(target=start_mail_engine, daemon=True).start()
    st.session_state["engine_started"] = True
    st.success("🚀 Mail motoru arka planda başlatıldı!")

# Sayfa Ayarları
st.set_page_config(page_title="Beyçelik Yönetim Paneli", layout="wide", page_icon="🏭")

st.title("🏭 Beyçelik Sac Ticaret - AI Yönetim Paneli")
st.markdown("---")

# Yan Panel (Sidebar) - Ayarlar ve Durum
st.sidebar.header("⚙️ Sistem Ayarları")
st.sidebar.write("**AI Model:** gpt-oss:120b-cloud")
profit_margin = st.sidebar.slider("Kâr Marjı (%)", 0, 50, 10)

# 1. BÖLÜM: Envanter Durumu
st.header("📦 Güncel Envanter")
try:
    with open("data/inventory.json", "r", encoding="utf-8") as f:
        inventory = json.load(f)
        df_inv = pd.DataFrame(inventory["products"])
        # Tabloyu daha şık gösterelim
        st.dataframe(df_inv, use_container_width=True)
except Exception as e:
    st.error(f"Envanter dosyası okunamadı: {e}")

st.markdown("---")

# 2. BÖLÜM: Bekleyen Talepler (Aracı Modeli)
st.header("⏳ Satıcıdan Cevap Bekleyen Talepler")
pending_path = Path("pending_requests.json")

if pending_path.exists():
    with open(pending_path, "r", encoding="utf-8") as f:
        pending_data = json.load(f)
    
    if pending_data:
        # Talepleri bir döngü ile ekrana basıyoruz
        for req_id, details in pending_data.items():
            with st.expander(f"📩 {details['customer_email']} - {details['subject']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**Gelen Mesaj İçeriği:**")
                    # Değişkeni burada tanımlıyoruz:
                    email_body = details.get('product', 'Mesaj içeriği alınamadı.')
                    st.info(email_body) # Artık NameError almazsın
                with col2:
                    st.write(f"**Durum:** `{details['status']}`")
                    st.write(f"**Tarih:** {details['timestamp']}")
                    if st.button("Talebi Sil", key=req_id):
                        st.warning("Bu özellik bir sonraki güncellemede eklenecek.")
    else:
        st.write("Şu an bekleyen bir talep bulunmuyor.")
else:
    st.info("Henüz bir 'pending_requests.json' dosyası oluşturulmamış.")

st.markdown("---")

# 3. BÖLÜM: Müşteri Etkileşim Geçmişi
st.header("📜 Müşteri Geçmişi")
cust_path = Path("data/customers.json")
if cust_path.exists():
    with open(cust_path, "r", encoding="utf-8") as f:
        customers = json.load(f)
    
    # Müşteri seçme kutusu
    selected_cust = st.selectbox("Geçmişini görmek istediğiniz müşteriyi seçin:", list(customers.keys()))
    if selected_cust:
        for interaction in customers[selected_cust]["history"]:
            st.text(f"📅 {interaction['date']}")
            st.write(f"👤 **Müşteri:** {interaction['message']}")
            st.write(f"🤖 **AI Cevabı:** {interaction['response']}")
            st.markdown("---")