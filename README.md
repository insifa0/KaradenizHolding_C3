# 🚢 Karadeniz AI — Proje Özeti
### Karadeniz Holding | Kurumsal Bilgi Asistanı | Young Talent Demo

---

## 🎯 Problem

Karadeniz Holding bünyesindeki **8 departmana** ait **120+ kurumsal belge** (prosedür, politika, talimat, form) farklı klasörlerde dağınık halde tutulmaktadır. Çalışanlar ihtiyaç duydukları bilgiye ulaşmakta zorlanmakta, bu durum aşağıdaki sorunlara yol açmaktadır:

| Sorun | Etkisi |
|-------|--------|
| ⏱️ Ortalama 8-15 dk / bilgi arama | Operasyonel verimlilik kaybı |
| 📋 Aylık 250+ BT/İK destek bileti | Departman iş yükü artışı |
| ❌ Yanlış/eski belge kullanımı | Uyumsuzluk riski |
| 🔓 Gizli belgelere yetkisiz erişim riski | Kurumsal güvenlik açığı |

---

## 💡 Çözüm: Karadeniz AI

**RAG (Retrieval-Augmented Generation)** mimarisi üzerine kurulu, kurumsal belgelerden anlık bilgi üreten **yapay zeka destekli chatbot** sistemi.

> **"Sorun, cevabı bilgi tabanımızdan saniyeler içinde buluyoruz."**

---

## 🏗️ Teknik Mimari

```
Çalışan Soruyor  →  FastAPI Backend  →  ChromaDB Vektör Arama
                                              ↓
                                    Gemini Embedding-2
                                    (Anlamsal Eşleştirme)
                                              ↓
                                    Gemini 2.5 Flash (LLM)
                                    Cevap Üretiyor
                                              ↓
                              HTML/JS Arayüzü → Çalışana Cevap
```

**Teknolojiler:** Python · FastAPI · ChromaDB · Google Gemini API · LangChain · HTML5/CSS3/TailwindCSS · WebGL

---

## ⭐ Öne Çıkan Özellikler

### 1. 🔍 Anlamsal Arama (Semantic Search)
Geleneksel arama: **"şifre"** ≠ **"parola"** → Sonuç bulunamaz ❌  
Karadeniz AI: **"şifre"** ≈ **"parola"** ≈ **"kimlik bilgisi"** → Doğru belge bulunur ✅

### 2. 🔐 Rol Tabanlı Yetkilendirme
5 farklı kullanıcı rolü (Tüm Çalışanlar → Yönetim) ile **ChromaDB metadata filtresi** üzerinden çalışan, belge seviyesinde güvenlik.  
Yetkisiz erişim girişimlerinde belgenin **adı bile gösterilmez.**

### 3. 📊 Canlı KPI Takibi
Her sorgu ile otomatik güncellenen: Zaman Tasarrufu · Önlenen Bilet Sayısı · Finansal Kazanç · Yanıt Başarı Oranı

### 4. ☁️ Azure'a Hazır Mimari
Mevcut yerel prototip, Azure AI Studio + Azure AI Search + Azure OpenAI + Entra ID ile doğrudan kurumsal buluta taşınabilir tasarımda.

---

## 📈 Ölçülen İş Değeri (Demo Verileri)

| KPI | Değer | Hesaplama |
|-----|-------|-----------|
| ⏰ Kazanılan Zaman | **21.2 saat** | 254 sorgu × 5 dk tasarruf |
| 🎫 Önlenen Destek Bileti | **101 adet** | Toplam sorgunun %40'ı |
| 💰 Finansal Tasarruf | **$1,010** | Bilet başına $10 maliyet |
| 👍 Yanıt Başarı Oranı | **%96.5** | 193 beğeni / 200 toplam |
| 🔒 Engellenen Yetkisiz Erişim | **12 adet** | Rol tabanlı filtre |

---

## 📁 Kapsanan Belge Yapısı

```
120 Kurumsal Belge
├── 📋 Prosedür (PR)    — Adım adım iş süreçleri
├── 📜 Politika (PO)    — Kurumsal kural ve standartlar
├── 📝 Talimat (TA)     — Teknik kullanım kılavuzları
└── 📄 Form (FR)        — Başvuru ve onay formları

8 Departman: İK · BT · SA · Finans · İSG · Operasyon · İletişim · Hukuk
```

---

## 🗺️ Gelecek Yol Haritası

| Aşama | Geliştirme | Öncelik |
|-------|-----------|---------|
| 🔐 Güvenlik | Azure Entra ID SSO entegrasyonu | Yüksek |
| 🚀 Performans | Streaming cevap (SSE) | Orta |
| 🔍 Arama | Hibrit Arama (BM25 + Vektör) | Orta |
| ☁️ Bulut | Azure AI Studio geçişi | Planlanıyor |

---

## 🚀 Sistemi Çalıştırma

```bash
# 1. Gereksinimleri kur
pip install -r requirements.txt

# 2. Sunucuyu başlat
python app_api.py

# 3. Tarayıcıda aç
http://localhost:8000

# 4. Gemini API anahtarını gir ve "Sistemi Başlat"'a tıkla
```

---

## 📂 Proje Belgeler Rehberi

| Belge | İçerik |
|-------|--------|
| [ornek_soru_cevap_senaryolari.md](./ornek_soru_cevap_senaryolari.md) | 7 gerçekçi demo senaryosu |
| [bilgi_mimarisi_şeması.md](./bilgi_mimarisi_şeması.md) | Sistem mimarisi, akış diyagramları |
| [sistem_calisma_rehberi.md](./sistem_calisma_rehberi.md) | Teknik mimari ve çalışma prensibi |
| [static/index.html](./static/index.html) | Canlı web arayüzü |
| [app_api.py](./app_api.py) | FastAPI backend sunucusu |
| [src/database.py](./src/database.py) | ChromaDB ve embedding motoru |

---

*Karadeniz Holding — Kurumsal Bilgi Asistanı | Young Talent Program Demo | 2026*
