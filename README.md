# 🔴 Vodafone AI Asistan (RAG & Lead Gen)

Bu proje, **Google Gemini 2.0 Flash** yapay zeka modelini, **Yerel Embedding (HuggingFace)** teknolojisini ve **RAG (Retrieval-Augmented Generation)** mimarisini kullanarak geliştirilmiş, kurumsal bir dijital satış asistanıdır.

Standart chatbotların aksine, **halüsinasyon görmez.** Sadece ona öğretilen kurumsal verileri (TXT, PDF, Excel) kullanarak cevap verir ve potansiyel müşterileri kaydeder.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![AI](https://img.shields.io/badge/AI-Gemini_2.0-orange)
![Tech](https://img.shields.io/badge/Tech-RAG-green)
![Data](https://img.shields.io/badge/Data-PDF_%26_Excel-red)

## 🚀 Projenin Yetenekleri

* **🧠 Akıllı Hafıza (Context Awareness):** Kullanıcıyla olan sohbeti hatırlar. "Bunun fiyatı ne?" denildiğinde hangi tarifeden bahsedildiğini anlar.
* **📄 Çoklu Format Desteği:** Klasöre atılan `.txt`, `.pdf` ve `.xlsx` dosyalarını otomatik okur. 
    * *Örnek:* `kampanya.pdf` dosyasındaki "Gizli Sinema İndirimi"ni tespit edip kullanıcıya sunabilir.
* **🎯 Satış Odaklı (Lead Gen):** Kullanıcı bir tarifeyi beğendiğinde, yan paneldeki form üzerinden İsim/Telefon bilgilerini alıp `basvurular.csv` dosyasına kaydeder.
* **🎈 İnteraktif Arayüz:** Başvuru alındığında görsel geri bildirim (Balon animasyonu) verir.
* **🛡️ Hibrit Mimari:** Veri işleme için yerel model, cevap üretme için Bulut API (Gemini) kullanılarak hız optimize edilmiştir.

## 🛠️ Kullanılan Teknolojiler

* **LangChain:** LLM orkestrasyonu.
* **Google Gemini API:** Doğal dil işleme.
* **ChromaDB:** Vektör veritabanı.
* **Streamlit:** Web arayüzü.
* **HuggingFace Embeddings:** Yerel veri işleme.
* **PyPDF & OpenPyXL:** Doküman işleme.

## 💻 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için:

1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/mehmetcangulseroglu/vodafone-ai-assistant.git](https://github.com/mehmetcangulseroglu/vodafone-ai-assistant.git)
    cd vodafone-ai-assistant
    ```

2.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **API Anahtarını Ayarlayın:**
    `.env` adında bir dosya oluşturun ve içine Google API anahtarınızı ekleyin:
    ```
    GOOGLE_API_KEY=AIzaSy...
    ```

4.  **Veritabanını Oluşturun:**
    ```bash
    python ingest.py
    ```

5.  **Asistanı Başlatın:**
    ```bash
    python -m streamlit run app.py
    ```

---
**Geliştirici:** Mehmet Can Gülseroğlu