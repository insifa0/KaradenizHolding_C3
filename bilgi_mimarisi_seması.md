# 🏗️ Karadeniz AI — Bilgi Mimarisi Önerisi

> Bu belge, Karadeniz Holding'in mevcut dağınık belge yapısından RAG tabanlı yapay zeka destekli bilgi yönetim sistemine geçiş mimarisini görselleştirmektedir.

---

## 📌 Mevcut Durum — Problem

```
MEVCUT PROBLEM: Dağınık Bilgi Yapısı
══════════════════════════════════════════════════════════════════
  Çalışan → "VPN'e nasıl bağlanırım?"
               │
               ├─► Klasöre bakıyor...  ❌ Hangi klasör?
               ├─► E-posta atıyor...   ❌ Yavaş, iş yükü
               ├─► IT'yi arıyor...     ❌ Destek bileti açılıyor
               └─► Herkese soruyor... ❌ Verimsizlik + hata riski

📁 BT Klasörü/
    ├── bt_prosedur_v1.docx
    ├── bt_prosedur_v2_FINAL.docx
    ├── bt_prosedur_v2_FINAL_guncellendi.docx  ← Hangisi geçerli?
    └── arsiv/
         └── eski_bt_politika.pdf

📁 İK Klasörü/
    ├── izin_yonetimi.pdf
    └── izin_yonetimi_2024.pdf    ← Hangisi güncel?

SONUÇ:
  ⏱️  Ortalama bilgi arama süresi: 8-15 dakika/sorgu
  📋  Aylık BT/İK destek bileti: 250+ adet
  ❌  Hatalı belge kullanım riski: Yüksek
  🔓  Gizli belgelere yanlış erişim riski: Mevcut
══════════════════════════════════════════════════════════════════
```

---

## ✅ Önerilen Sistem — Karadeniz AI Bilgi Mimarisi

### Katman 1: Veri Kaynakları (Belge Havuzu)

```
┌──────────────────────────────────────────────────────────────────┐
│                     📚 KURUMSAL BELGE HAVUZU                     │
│              (120 Belge / 8 Departman / 4 Tip)                   │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│ 📋 Prosedür  │ 📜 Politika  │ 📝 Talimat   │ 📄 Form            │
│  (PR kodu)   │  (PO kodu)   │  (TA kodu)   │  (FR kodu)         │
├──────────────┴──────────────┴──────────────┴────────────────────┤
│ 🏢 İnsan Kaynakları (İK)    │ 💻 Bilgi Teknolojileri (BT)       │
│ 🛒 Satın Alma (SA)          │ 💰 Finans ve Muhasebe (FN)         │
│ ⛑️  İş Sağlığı Güvenliği (İSG)│ 🚢 Operasyon ve Denizcilik (OD) │
│ 📣 Kurumsal İletişim (Kİ)   │ ⚖️  Hukuk, Etik ve Uyum (HE)     │
└──────────────────────────────────────────────────────────────────┘
```

### Katman 2: Yapay Zeka İşleme Motoru

```
┌──────────────────────────────────────────────────────────────────┐
│                   🤖 RAG İŞLEME MOTORU                          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  📖 Belge Ayrıştırıcı (database.py)                     │    │
│  │  • ID bazlı otomatik bölümleme (Regex)                  │    │
│  │  • Departman / Tip / Erişim otomatik tespit             │    │
│  │  • Anahtar kelime genişletme (Sinonim haritası)         │    │
│  └──────────────────────┬──────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🔢 Gemini Embedding-2 (Vektörleştirme)                 │    │
│  │  • Her belge → 3072 boyutlu anlam vektörü               │    │
│  │  • Anlamsal arama: "şifre" ↔ "parola" ↔ "kimlik"        │    │
│  │  • Rate-limit korumalı toplu işlem (25'er grup)         │    │
│  └──────────────────────┬──────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🗄️  ChromaDB Vektör Veritabanı                         │    │
│  │  • Tüm belge vektörleri + metadata saklanır             │    │
│  │  • Anlık Kosinüs Benzerliği hesabı                      │    │
│  │  • Rol bazlı metadata filtresi (Erisim_Yetkisi)         │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### Katman 3: Erişim ve Güvenlik Katmanı

```
┌──────────────────────────────────────────────────────────────────┐
│                  🔐 YETKİLENDİRME HİYERARŞİSİ                   │
│                                                                  │
│   ROLLAR (Düşükten Yükseğe):                                     │
│                                                                  │
│   👤 Tüm Çalışanlar ────────────────────────────────────────►   │
│      • Genel politikalar, temel talimatlar                        │
│      • İzin formları, genel prosedürler                           │
│                                                                  │
│   👥 Teknik Ekip ──────────────────────────────────────────────► │
│      • Tüm Çalışanlar kapsamı +                                  │
│      • Teknik dokümantasyon, sistem talimatları                  │
│                                                                  │
│   💻 BT Departmanı ────────────────────────────────────────────► │
│      • Teknik Ekip kapsamı +                                     │
│      • BT güvenlik prosedürleri, altyapı erişim yönetimi         │
│                                                                  │
│   💰 Finans Departmanı ─────────────────────────────────────────►│
│      • Tüm Çalışanlar kapsamı +                                  │
│      • Bütçe politikaları, finansal raporlama                    │
│                                                                  │
│   👑 Yönetim ──────────────────────────────────────────────────► │
│      • TÜM BELGELER (tam erişim)                                 │
│                                                                  │
│   ⚠️  Güvenlik: Yetkisiz erişim veri tabanı seviyesinde engellenir│
│      (Belge adı/içeriği asla gösterilmez)                        │
└──────────────────────────────────────────────────────────────────┘
```

### Katman 4: Kullanıcı Arayüzü

```
┌──────────────────────────────────────────────────────────────────┐
│                    🖥️  KULLANICI ARAYÜZÜ                         │
│               (HTML5 + TailwindCSS + WebGL)                      │
│                                                                  │
│  ┌──────────┐  ┌─────────────────────────────────────────────┐  │
│  │          │  │  HEADER: Sekme Navigasyonu                  │  │
│  │  SOL     │  │  [Sohbet] [Belge Kütüphanesi] [KPI] [Azure] │  │
│  │  PANEL   │  ├─────────────────────────────────────────────┤  │
│  │          │  │                                             │  │
│  │ API Key  │  │     💬 SOHBET EKRANI                        │  │
│  │ Rol Seç  │  │     ┌─────────────────────────────────┐     │  │
│  │ Başlat   │  │     │ 🤖 AI cevap balonu               │     │  │
│  │          │  │     │ 📄 Referans belgeler             │     │  │
│  │ Metrik-  │  │     │ 👍 Geri bildirim butonları       │     │  │
│  │ ler      │  │     └─────────────────────────────────┘     │  │
│  │          │  │                                             │  │
│  │          │  │  [Soru yazın...            ] [Gönder 🚀]    │  │
│  └──────────┘  └─────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Uçtan Uca Veri Akış Diyagramı

```
ÇALIŞAN SORUYOR: "Yıllık izin kaç gün?"
        │
        ▼
┌─────────────────────────┐
│   HTML/JS Arayüzü       │
│   Rol: "Tüm Çalışanlar"│
│   Soru → HTTP POST      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   FastAPI Backend       │
│   /api/chat             │
│   Rol → İzin Listesi    │
│   ["Tüm Çalışanlar"]    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Gemini Embedding      │
│   "yıllık izin kaç gün" │
│   → [0.23, -0.87, ...]  │
│      (3072 boyutlu)     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   ChromaDB              │
│   Filtre: Tüm Çalışanlar│
│   En yakın k=3 belge:   │
│   • İK-PR-02 ✅ (0.94)  │
│   • İK-FR-07 ✅ (0.81)  │
│   • İK-PO-01 ✅ (0.79)  │
│   BT-PR-01  ❌ (gizli)  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Gemini 2.5 Flash      │
│   System Prompt:        │
│   [Belgeler + Soru]     │
│   → Profesyonel Cevap   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   HTML/JS Arayüzü       │
│   Cevap balonu göster   │
│   Referans kartları     │
│   Geri bildirim buton.  │
└─────────────────────────┘

⏱️  Toplam Süre: ~2-4 saniye
```

---

## 📊 Belge Erişim Matrisi

| Departman | Tüm Çalışanlar | Teknik Ekip | BT Dept. | Finans Dept. | Yönetim |
|-----------|:--------------:|:-----------:|:--------:|:------------:|:-------:|
| İK — Genel İzin, İşe Alım | ✅ | ✅ | ✅ | ✅ | ✅ |
| BT — VPN, E-posta | ✅ | ✅ | ✅ | ✅ | ✅ |
| BT — Güvenlik Altyapısı | ❌ | ❌ | ✅ | ❌ | ✅ |
| Satın Alma — Prosedürler | ✅ | ✅ | ✅ | ✅ | ✅ |
| Finans — Bütçe Politikası | ❌ | ❌ | ❌ | ✅ | ✅ |
| Hukuk — Gizlilik Sözleşmesi | ❌ | ❌ | ❌ | ❌ | ✅ |
| İSG — Güvenlik Talimatları | ✅ | ✅ | ✅ | ✅ | ✅ |
| Operasyon — Gemi Prosedürleri | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🔮 Azure Üretim Ortamı Mimarisi (Gelecek Durum)

```
┌──────────────────────────────────────────────────────────────────┐
│                  ☁️  HEDEF: AZURE BULUT MİMARİSİ                 │
│                                                                  │
│  👤 Çalışan (Tarayıcı)                                           │
│       │  Azure Entra ID ile Kimlik Doğrulama (SSO)              │
│       ▼                                                          │
│  🌐 Azure App Service (Web Arayüzü)                              │
│       │                                                          │
│       ▼                                                          │
│  ⚙️  Azure AI Studio / Prompt Flow (Orkestrasyon)               │
│       │                    │                                     │
│       ▼                    ▼                                     │
│  🔍 Azure AI Search    🤖 Azure OpenAI (GPT-4o)                  │
│  (Hibrit Arama +       (Kurumsal Kapalı Devre)                  │
│   Vektör İndeks)                                                 │
│       │                                                          │
│       ▼                                                          │
│  📦 Azure Blob Storage + SharePoint (Belge Havuzu)              │
│       │                                                          │
│       ▼                                                          │
│  📊 Azure Monitor + Application Insights (İzleme)               │
│                                                                  │
│  🔐 Azure Key Vault (API Anahtarları Güvenli Yönetim)           │
└──────────────────────────────────────────────────────────────────┘
```

---

*Karadeniz Holding — Kurumsal Bilgi Asistanı Projesi | Bilgi Mimarisi Tasarım Belgesi*
