# 📊 Karadeniz AI — Yönetici Sunumu Yol Haritası (Maksimum 5 Slayt)

Bu rehber, **Karadeniz Holding** yöneticilerine ve jüriye sunulmak üzere hazırlanmış **maksimum 5 slaytlık** stratejik sunum şablonudur. Slaytlar; teknik detaylarda boğulmadan doğrudan **iş değerine (business value), güvenliğe ve verimliliğe** odaklanacak şekilde yapılandırılmıştır.

---

## 🖥️ Slayt 1: Kapak & Temel Değer Önermesi
> **Odak:** İlk izlenim, vizyon ve projenin holding için neden kritik olduğu.

### Görsel Tasarım Önerisi:
* Arka planda holdingi simgeleyen koyu mavi tonlar ve siber dalga/enerji efektleri (Uygulamadaki WebGL shader gibi).
* Başlıklar büyük, net ve kurumsal fontlarda.

### Slayt İçeriği:
* **Ana Başlık:** 🚢 **Karadeniz AI**
* **Alt Başlık:** Kurumsal Bilgi Tabanını Tek Noktada Birleştiren Akıllı RAG Portalı
* **Değer Önermesi:** *"Dağınık departman verilerini güvenli, hızlı ve anlamsal olarak sorgulanabilir tek bir akıllı asistanda birleştirerek operasyonel kayıpları sıfıra indiriyoruz."*
* **Sunan / Proje:** Young Talent Yetenek Programı Demo Projesi - 2026

---

## 🖥️ Slayt 2: Mevcut Durum & Problem Tanımı
> **Odak:** Çözmeye çalıştığımız operasyonel ve finansal kayıplar. Yöneticinin "Neden bu projeye bütçe/zaman ayırmalıyız?" sorusuna cevap.

### Görsel Tasarım Önerisi:
* İki sütunlu düzen. Sol tarafta "Mevcut Durum", sağ tarafta "Riskler/Kayıplar" (Kırmızı/Turuncu uyarı ikonlarıyla).

### Slayt İçeriği:
* **Mevcut Durum:**
  * Holding bünyesinde **8 farklı departmana** ait **120+ canlı döküman** (prosedürler, politikalar, formlar, talimatlar) farklı dosya sunucularında dağınık durumda.
* **Operasyonel Sıkıntılar (Veri Sızıntısı & Zaman Kaybı):**
  * **⏱️ Arama Kayıpları:** Çalışanlar ihtiyaç duydukları doğru bilgiye veya forma ulaşmak için günde ortalama **8 ila 15 dakika** harcıyor.
  * **🎫 Aşırı İş Yükü:** Basit ve tekrarlayan sorular nedeniyle İK ve BT servis masalarına her ay yüzlerce gereksiz destek talebi (ticket) açılıyor.
  * **🔐 Güvenlik Açığı:** Rol tabanlı erişim kontrolü zayıf; teknik ekipler veya yetkisiz çalışanlar kritik finans/yönetim dökümanlarına erişebiliyor.

---

## 🖥️ Slayt 3: Çözüm: Akıllı Yetkilendirilmiş RAG Mimarisi
> **Odak:** Projenin sunduğu yenilikçi çözüm ve bunun güvenlik temeli.

### Görsel Tasarım Önerisi:
* Projenin akışını gösteren basit bir mimari şema (Çalışan → API Yetki Filtresi → Vektör Tabanı → LLM → Güvenli Yanıt).

### Slayt İçeriği:
* **1. Anlamsal Arama (Semantic Search):**
  * Klasik kelime araması yerine anlam analizi yapılır. Kullanıcı *"parolamı unuttum"* yazdığında, sistem dökümandaki *"Erişim Şifre Güvenliği"* maddesini otomatik eşleştirir.
* **2. Veri Tabanı Seviyesinde Güvenlik (Role-Based Filter):**
  * 5 farklı çalışan rolü tanımlanmıştır. ChromaDB vektör tabanı sorgu anında filtreleme yapar. Yetkisiz belge, LLM'e (Gemini) gitmeden elenir.
* **3. Hızlı ve Esnek Prototip:**
  * FastAPI ve Google Gemini API ile entegre, anlık sorgu yapabilen, hafif ve tarayıcı dostu kullanıcı arayüzü.

---

## 🖥️ Slayt 4: İş Değeri, Finansal Tasarruf & KPI'lar
> **Odak:** Yöneticilerin en çok önem verdiği slayt. Sistemin holdinge sağladığı somut faydaların matematiksel kanıtı.

### Görsel Tasarım Önerisi:
* KPI kartları şeklinde 3-4 büyük kutu. Rakamlar büyük puntolarla vurgulanmalı.

### Slayt İçeriği:
* **⏱️ Zaman Kazanımı:** **21.2 Saat Tasarruf**
  * *Hesaplama:* 254 başarılı sorguda, çalışan başına manuel arama süresinden 5 dakika net tasarruf sağlandı.
* **🎫 Destek Masası (IT/HR) Optimizasyonu:** **101 Adet Önlenen Ticket**
  * *Hesaplama:* Toplam sorgunun %40'ının asistan tarafından çözüldüğü ve bilet açılmasını önlediği hesaplanmıştır.
* **💰 Operasyonel Finansal Kazanç:** **$1,010 Net Tasarruf**
  * *Hesaplama:* Önlenen bilet başına holding operasyonel maliyet tasarrufu 10 USD olarak hesaplanmıştır (101 ticket × 10$).
* **🛡️ Güvenlik ve Uyum:** **12 Adet Engellenen İhlal**
  * Yetkisiz kullanıcıların yetkileri dışındaki belgelere erişim girişimleri filtrelenerek veri sızıntısının önüne geçildi.

---

## 🖥️ Slayt 5: Canlıya Geçiş (Azure Bulut Planı) & Yol Haritası
> **Odak:** Projenin geleceği, ölçeklenebilirliği ve kurumsal entegrasyon adımları.

### Görsel Tasarım Önerisi:
* Soldan sağa doğru ilerleyen 3 aşamalı bir yol haritası çizgisi (Roadmap timeline).

### Slayt İçeriği:
* **Aşama 1: Kurumsal Kimlik (Entra ID) Entegrasyonu**
  * Simüle edilen rollerin yerini holdingin aktif Microsoft Entra ID (Active Directory) altyapısı alacak. Çalışanlar doğrudan kendi kurumsal yetkileriyle sisteme giriş yapacak.
* **Aşama 2: Azure Bulut Mimarisine Geçiş (Production-Ready)**
  * Yerel ChromaDB vektör tabanı **Azure AI Search**'e taşınacak.
  * Gemini API yerine holding verilerini dışarıya sızdırmayan, tamamen kapalı **Azure OpenAI (GPT-4o)** altyapısına geçilecek.
* **Aşama 3: Sürekli Öğrenme (RLHF) & İnce Ayar**
  * Kullanıcılardan gelen 👍/👎 geri bildirimler analiz edilerek, holding belgelerine özel anlamsal arama doğruluğu %99'un üzerine çıkarılacak.
