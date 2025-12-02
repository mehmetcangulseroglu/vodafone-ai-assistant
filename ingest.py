import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

TXT_DOSYA_YOLU = "./vodafone.txt"
VERITABANI_KLASORU = "./chroma_db"

def main():
    print("🚀 Veritabanı hazırlanıyor...")

    if os.path.exists(VERITABANI_KLASORU):
        try: shutil.rmtree(VERITABANI_KLASORU)
        except: pass

    if not os.path.exists(TXT_DOSYA_YOLU):
        print("❌ HATA: vodafone.txt yok!")
        return

    loader = TextLoader(TXT_DOSYA_YOLU, encoding="utf-8")
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(raw_documents)

    print(f"💾 {len(documents)} veri parçası işleniyor (Bu işlem yereldir, internet kotası yemez)...")
    
    # Yerel Model 
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=VERITABANI_KLASORU)
    print("✅ İŞLEM TAMAM! Veritabanı hazır.")

if __name__ == "__main__":
    main()