import streamlit as st
import os
import csv
import datetime
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv


import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger('googleapiclient').setLevel(logging.ERROR)

# --- AYARLAR ---
st.set_page_config(page_title="Vodafone Red Asistan", page_icon="🔴", layout="wide")
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# --- CSS TASARIMI ---
st.markdown("""
<style>
    .stApp { background-color: white; }
    .user-msg { background-color: #f4f4f4; color: #333; padding: 10px 15px; border-radius: 15px 15px 0 15px; margin-bottom: 10px; text-align: right; float: right; clear: both; max-width: 70%; border: 1px solid #ddd; }
    .bot-msg { background-color: #fff5f5; color: #333; padding: 10px 15px; border-radius: 15px 15px 15px 0; margin-bottom: 10px; text-align: left; float: left; clear: both; max-width: 70%; border-left: 5px solid #E60000; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    h1 { color: #E60000; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- PERFORMANS AYARI (CACHE) ---
@st.cache_resource
def sistemi_yukle():
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        return db
    except Exception as e:
        return None

db = sistemi_yukle()

# --- FONKSİYONLAR ---
def basvuru_kaydet(ad, tel, tarife):
    dosya = "basvurular.csv"
    yeni = not os.path.exists(dosya)
    try:
        with open(dosya, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if yeni: writer.writerow(["Tarih", "Ad Soyad", "Telefon", "Tarife"])
            writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), ad, tel, tarife])
        return True
    except: return False

def cevap_uret(soru, gecmis):
    if not db: return "Veritabanı yüklenemedi!"
    
    try:
        # 1. Arama
        belgeler = db.similarity_search(soru, k=3)
        bilgi = "\n".join([d.page_content for d in belgeler])
        
        # 2. Zeka
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        Sen Vodafone asistanı Tobi'sin.
        GÖREV: Aşağıdaki bilgileri ve geçmişi kullanarak cevap ver.
        
        GEÇMİŞ: {gecmis}
        BİLGİLER: {bilgi}
        SORU: {soru}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"HATA: {e}"

# --- ARAYÜZ ---
col1, col2 = st.columns([7, 3])

with col1:
    st.markdown("<h1>🔴 Vodafone Red Asistan</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Merhaba! 👋 Ben Tobi. Size nasıl yardımcı olabilirim?"}]

    chat_placeholder = st.container()
    with chat_placeholder:
        for msg in st.session_state.messages:
            div_class = "user-msg" if msg["role"] == "user" else "bot-msg"
            st.markdown(f"<div class='{div_class}'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

    prompt = st.chat_input("Sorunuzu buraya yazın...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_placeholder:
            st.markdown(f"<div class='user-msg'>{prompt}</div>", unsafe_allow_html=True)
        
        gecmis = "\n".join([m['content'] for m in st.session_state.messages[-3:]])
        
        with st.spinner("🔴 Tobi yazıyor..."):
            cevap = cevap_uret(prompt, gecmis)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
            with chat_placeholder:
                st.markdown(f"<div class='bot-msg'>{cevap}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 📝 Başvuru Formu")
    with st.form("lead"):
        ad = st.text_input("Ad Soyad")
        tel = st.text_input("Telefon")
        tarife = st.selectbox("Tarife", ["Red", "Genç", "Bütçe"])
        if st.form_submit_button("Gönder 📞"):
            basvuru_kaydet(ad, tel, tarife)
            st.success("Başvurunuz alındı! En kısa sürede sizi arayacağız.")