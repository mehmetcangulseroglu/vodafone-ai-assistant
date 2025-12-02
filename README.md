# 🔴 Vodafone AI Asistan (RAG Chatbot)

Bu proje, **Google Gemini** yapay zeka modelini ve **RAG (Retrieval-Augmented Generation)** mimarisini kullanarak geliştirilmiş, kurumsal bir dijital asistandır.

Standart chatbotların aksine, **halüsinasyon görmez.** Sadece ona öğretilen kurumsal verileri (Tarife bilgileri) kullanarak cevap verir.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![AI](https://img.shields.io/badge/AI-Gemini_Flash-orange)
![Tech](https://img.shields.io/badge/Tech-RAG-green)
![Framework](https://img.shields.io/badge/Framework-LangChain-yellow)

## 🚀 Projenin Yetenekleri

* **🧠 Akıllı Hafıza:** Kullanıcıyla olan sohbeti hatırlar. "Bunun fiyatı ne?" denildiğinde hangi tarifeden bahsedildiğini anlar.
* **📚 RAG Mimarisi:** `vodafone.txt` dosyasındaki verileri yerel vektör veritabanına işler ve oradan cevap üretir.
* **🎯 Satış Odaklı (Lead Gen):** Kullanıcı bir tarifeyi beğendiğinde, yan paneldeki form üzerinden İsim/Telefon bilgilerini alıp `basvurular.csv` dosyasına kaydeder.
* **🎨 Modern Arayüz:** Streamlit ile geliştirilmiş, Vodafone kurumsal kimliğine (Kırmızı/Beyaz) uygun responsive tasarım.
* **🛡️ Güvenli & Hızlı:** Google kota sınırlarını aşmak için **Yerel Embedding (HuggingFace)** ve **Gemini 2.0 Flash** modeli hibrit olarak kullanılmıştır.

## 🛠️ Kullanılan Teknolojiler

* **LangChain:** LLM orkestrasyonu.
* **Google Gemini API:** Doğal dil işleme ve cevap üretme.
* **ChromaDB:** Vektör veritabanı (Verileri anlamlandırma).
* **Streamlit:** Web arayüzü.
* **HuggingFace Embeddings:** Yerel veri işleme modeli.

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
    GOOGLE_API_KEY=AIzaSy... (Sizin Anahtarınız)
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