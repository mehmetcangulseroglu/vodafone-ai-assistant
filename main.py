import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. API Anahtarını ve Ayarları Yükleme
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Veritabanı ve Model Ayarları
VERITABANI_KLASORU = "./chroma_db"
EMBEDDING_MODEL = "models/text-embedding-004"
LLM_MODEL = "gemini-pro"

def chatbotu_baslat():
    """
    Bu fonksiyon yapay zeka modelini ve veritabanını hazırlar.
    """
    print("🔴 Vodafone Asistanı Hazırlanıyor... Lütfen bekleyin.")
    
    # Embedding (Vektör) modelini hazırlama
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    
    # Veritabanı klasörü var mı?
    if not os.path.exists(VERITABANI_KLASORU):
        print("HATA: Veritabanı bulunamadı! Lütfen önce terminale 'python ingest.py' yazıp çalıştırın.")
        return None

    # Veritabanını yükleme
    vector_store = Chroma(
        persist_directory=VERITABANI_KLASORU, 
        embedding_function=embeddings
    )
    
    # Yapay Zeka Modelini (LLM) Hazırlama
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0.3, # 0: Robotik cevap, 1: Çok yaratıcı cevap. 0.3 idealdir.
        convert_system_message_to_human=True
    )
    
    # --- VODAFONE PERSONASI ---
    template = """
    Sen Vodafone Türkiye'nin yardımsever, enerjik ve akıllı yapay zeka asistanısın.
    
    GÖREVİN: Aşağıdaki bağlam (context) bilgisini kullanarak kullanıcının sorusunu cevapla.
    
    KURALLAR:
    1. Sadece verilen bağlamdaki bilgileri kullan. Bilmiyorsan "Üzgünüm, şu anki veri setimde bu bilgi yok." de.
    2. Cevapların kısa, net ve anlaşılır olsun.
    3. Müşteriye hitap ederken nazik ve profesyonel ol.
    4. Uygun yerlerde emojiler kullan (🔴, 📱, 🚀, 💬, ✨ gibi).
    5. Vodafone'un "Red" dünyasına uygun, dinamik bir dil kullan.
    
    Bağlam (Context):
    {context}
    
    Soru: {question}
    
    Vodafone Asistanı Cevabı:
    """
    
    PROMPT = ChatPromptTemplate.from_template(template)
    
    # Retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # En alakalı 3 parçayı getirir
    
    # Format docs fonksiyonu
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # RAG chain'i oluşturma
    qa_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )
    
    return qa_chain

# --- TERMİNAL TESTİ (Arayüzden önceki test alanı) ---
if __name__ == "__main__":
    bot = chatbotu_baslat()
    
    if bot:
        print("\n" + "="*50)
        print("🔴 VODAFONE TARİFE ASİSTANINA HOŞ GELDİNİZ! 🔴")
        print("Size en uygun tarifeyi bulmak için buradayım.")
        print("Çıkmak için 'q' veya 'exit' yazabilirsiniz.")
        print("="*50 + "\n")
        
        while True:
            try:
                soru = input("Siz: ")
                if soru.lower() in ['q', 'exit', 'çıkış']:
                    print("🔴 Görüşmek üzere! Vodafone'la kalın.")
                    break
                
                # Cevabı üretme
                cevap = bot.invoke(soru)
                
                print(f"\n🤖 Asistan: {cevap}\n")
                print("-" * 30)
                
            except Exception as e:
                print(f"Bir hata oluştu: {e}")