# 🚢 Karadeniz Holding Kurumsal Bilgi Asistanı — Arayüz Bileşenleri Kılavuzu

Bu dosya, asistan uygulamasında (Streamlit `app.py`) kullanılan tüm buton, girdi (input), sekme (tab) ve dinamik alanları listeler. Tasarımı başka bir yapay zeka ile yeniden şekillendirirken bu bileşenlerin korunması gerekmektedir.

---

## 1. Sol Panel (Sidebar - Kenar Çubuğu)

Kenar çubuğu uygulamanın yönetim, yapılandırma ve istatistik merkezidir.

| Bileşen Adı | Tipi / Yapısı | Görevi / İşlevi | Değerleri / Durumları |
| :--- | :--- | :--- | :--- |
| **Durum Göstergesi** | Özel HTML (Durum kartı ve yanıp sönen yuvarlak ışık) | Sistemin başlatılıp başlatılmadığını gösteren canlı durum paneli. | `Sistem Başlatılmadı` (Kırmızı Işık) / `Sistem Çevrimiçi / Hazır` (Yeşil Nabız Işığı) |
| **Gemini API Anahtarı** | Şifreli Metin Kutusu (`st.text_input` - password type) | Kullanıcının Gemini API Key girmesini sağlar. | `.env` dosyasındaki `GEMINI_API_KEY` değerini varsayılan alır. |
| **Yetki Simülatörü** | Açılır Liste / Dropdown (`st.selectbox`) | Kullanıcının veri erişim rolünü simüle eder ve RAG sorgusunu filtreler. | `Tüm Çalışanlar`, `Teknik Ekip`, `BT Departmanı`, `Finans Departmanı`, `Yönetim` |
| **Sistemi Başlat** | Buton (`st.button`) | API anahtarını doğrular, dökümanları yükler/indeksler ve sistemi hazır hale getirir. | Mavi/Turkuaz renkli birincil buton. |
| **Veritabanını Yeniden Oluştur** | Buton (`st.button`) | Sadece sistem hazır olduğunda görünür. ChromaDB vektör tabanını tamamen silip sıfırdan kurar. | İkincil aksiyon butonu. |
| **Gelişmiş Ayarlar** | Katlanabilir Bölüm (`st.expander`) | Jüriye gösterilmek üzere RAG parametrelerini barındırır. | Başlangıçta kapalı (collapsed). |
| **Cevap Yaratıcılığı (Temp)** | Kaydırma Çubuğu / Slider (`st.slider`) | Gelişmiş Ayarlar altında modelin yaratıcılık katsayısını yönetir. | `0.0` (Kesin) ile `1.0` (Yaratıcı) arası. Varsayılan: `0.3` |
| **Arama Derinliği (k)** | Kaydırma Çubuğu / Slider (`st.slider`) | Gelişmiş Ayarlar altında RAG'in kaç döküman referansı getireceğini seçer. | `1` ile `5` arası. Varsayılan: `3` |
| **Sohbeti Dışa Aktar (MD)** | İndirme Butonu (`st.download_button`) | Sadece konuşma başladığında görünür. Sohbeti Markdown formatında indirir. | Dosya Adı: `karadeniz_bot_sohbet_gecmisi.md` |
| **Sohbeti Temizle** | Buton (`st.button`) | Sohbet geçmişini tamamen sıfırlar ve ekranı yeniler. | Sidebar alt kısmı. |
| **Bilgi Tabanı İstatistikleri** | Katlanabilir Bölüm (`st.expander`) | ChromaDB içindeki yüklü dökümanların durumunu gösterir. | Başlangıçta kapalı. Toplam Döküman Sayısı, Tipe ve Departmana göre dağılım metriklerini barındırır. |
| **Bilgi Notu** | Özel Bilgi Kutusu (`st.markdown`) | Kullanıcıya arama yapabilmesi için ipucu ve örnekler sunar. | Statik HTML kartı. |

---

## 2. Ana İçerik Alanı (Main Area)

Ana ekran 3 sekmeli (`st.tabs`) bir yapıdan oluşur. Üst kısımda kurumsal bir başlık kartı yer alır.

### A. Üst Başlık Kartı
*   **Logo/Görsel:** Gemi emojisi (`🚢`)
*   **Ana Başlık:** `Karadeniz Holding — Kurumsal Bilgi Asistanı` (Büyük Boyut, Outfit Fontu)
*   **Alt Başlık:** `Prosedürler • Politikalar • Talimatlar • Formlar — Yapay Zeka Destekli Erişim`

### B. Sekmeler (Tabs)

#### Sekme 1: 💬 Sohbet (Chat)
*   **Hoş Geldiniz Karşılama Ekranı:** Sistem henüz başlatılmamışken ortalanmış şekilde duran karşılama yazısı ve yönlendirme.
*   **Mesaj Akışı (Chat History):**
    *   *Kullanıcı Mesajları:* Kullanıcı emojisi (`🧑‍💼`) ile sağa yaslı veya modern gri/mavi balonda gösterilir.
    *   *Asistan Mesajları:* Gemi emojisi (`🚢`) ile sola yaslı, turkuaz kenarlıklı balonda gösterilir.
    *   *Kaynak Belgeler:* Her asistan mesajının altında katlanabilir bir kart (`st.expander`) halinde yanıtın çekildiği referans belgelerin ID'leri, adları ve türleri listelenir.
*   **Sohbet Giriş Alanı (`st.chat_input`):** Ekranın en altında sabit duran, kullanıcının sorusunu yazdığı ve Gönder butonuna bastığı alan.

#### Sekme 2: 📁 Belge Kütüphanesi (Document Library)
Chatbot'a sormadan 120 belgeyi listeleyip arama ve filtreleme yapmayı sağlayan ekrandır.
*   **Arama Kutusu (`st.text_input`):** Belge adı veya ID ile anlık filtreleme yapar.
*   **Departman Filtresi (`st.selectbox`):** "Tümü" seçeneğiyle birlikte departmana göre belgeleri süzer.
*   **Belge Tipi Filtresi (`st.selectbox`):** "Tümü" seçeneğiyle birlikte (Prosedür, Politika, Talimat, Form) belgeleri süzer.
*   **Belge Kartları (`st.expander` listesi):** Filtrelenmiş her belgeyi listeler. Kart başlığı `📄 [Belge ID] — [Belge Adı]` şeklindedir. Kart açıldığında:
    *   Metadata Etiketleri (Departman, Belge Tipi, Erişim Yetkisi) renkli tagler şeklinde gösterilir (Erişim yetkisi kısıtlıysa kırmızı renkli etiket).
    *   Belgenin tam metni gösterilir.
    *   Alt kısımda `İlişkili Belgeler` ve `Anahtar Kelimeler` listelenir.

#### Sekme 3: ☁️ Azure Bulut Geçiş Planı (Azure Cloud Plan)
Jüriye projenin Azure bulut ortamına nasıl taşınacağını anlatan sunum sekmesidir.
*   **Geçiş Adımları (6 adet kart):** Veri depolama, Vektör arama, Güvenlik (Entra ID), AI Modeli (Azure OpenAI), İzleme ve Orkestrasyon adımlarını açıklayan kurumsal kutular.
*   **Mimari Şeması (2 adet kod bloğu):** Yerel (Local) RAG Mimarisi ile Hedef Azure RAG Mimarisini karşılaştıran ASCII şemaları.
