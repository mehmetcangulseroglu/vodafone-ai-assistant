import os
import shutil
from dotenv import load_dotenv
# Yeni okuyucular
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

VERITABANI_KLASORU = "./chroma_db"

def main():
    print("🚀 Çoklu Veri İşleyici Başlatılıyor...")

    # 1. Eski veritabanı temizliği
    if os.path.exists(VERITABANI_KLASORU):
        try: shutil.rmtree(VERITABANI_KLASORU)
        except: pass

    tum_belgeler = []
    
    # 2. Klasördeki TÜM dosyaları tarayalım
    dosyalar = os.listdir(".")
    for dosya in dosyalar:
        dosya_yolu = f"./{dosya}"
        
        try:
            # .txt dosyalarını okuma (requirements.txt hariç)
            if dosya.endswith(".txt") and "requirements" not in dosya:
                print(f"📄 TXT Okunuyor: {dosya}")
                loader = TextLoader(dosya_yolu, encoding="utf-8")
                tum_belgeler.extend(loader.load())
                
            # .pdf dosyalarını okuma
            elif dosya.endswith(".pdf"):
                print(f"📕 PDF Okunuyor: {dosya}")
                loader = PyPDFLoader(dosya_yolu)
                tum_belgeler.extend(loader.load())
                
            # .xlsx (Excel) dosyalarını okuma
            elif dosya.endswith(".xlsx"):
                print(f"📊 EXCEL Okunuyor: {dosya}")
                loader = UnstructuredExcelLoader(dosya_yolu)
                tum_belgeler.extend(loader.load())
                
        except Exception as e:
            print(f"⚠️ HATA ({dosya}): {e} (Bu dosya atlandı)")

    if not tum_belgeler:
        print("❌ HATA: Hiçbir okunabilir dosya bulunamadı!")
        return

    # 3. Parçala
    print(f"✂️  Toplam {len(tum_belgeler)} sayfa/bölüm işleniyor...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(tum_belgeler)

    # 4. Kaydet
    print("💾 Veritabanına gömülüyor...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    Chroma.from_documents(
        documents=documents, 
        embedding=embeddings, 
        persist_directory=VERITABANI_KLASORU
    )
    
    print("✅ İŞLEM TAMAM! Artık PDF ve Excel dosyalarını da biliyorum.")

if __name__ == "__main__":
    main()