# 🎓 Karadeniz AI — 1 Sayfalık Öğrenme Özeti (Microsoft Learn Çalışma Raporu)

Bu rapor, **Karadeniz AI** projesinin geliştirilme sürecinde kendi kendine öğrenme (**self-study**) metodolojisi kapsamında kullanılan **Microsoft Learn** eğitim modüllerini, edinilen kazanımları ve bunların yerel prototipten kurumsal mimariye geçişteki izdüşümünü özetlemektedir.

---

## 🎯 1. Öğrenme Yolculuğu ve Amaç
Proje hedeflerini gerçekleştirmek için, kurumsal standartlarda bir yapay zeka (AI) ve vektörel arama altyapısının teorisini anlamak amacıyla **Microsoft Learn** platformu bir kılavuz olarak kullanılmıştır. Yerel prototip (FastAPI + ChromaDB + Gemini) geliştirilirken, sistem tasarımı ve güvenlik filtreleme mantığı tamamen Microsoft'un bulut mimarisi en iyi pratikleri (**Best Practices**) referans alınarak kurgulanmıştır.

---

## 📚 2. Referans Alınan Microsoft Learn Modülleri

Sunumda ve jüri değerlendirmesinde öne çıkarılan ve proje geliştirilirken tamamlanan temel öğrenme modülleri:

| Microsoft Learn Modülü / Öğrenme Yolu | Edinilen Kritik Bilgi / Konsept | Projeye / Tasarıma Katkısı |
| :--- | :--- | :--- |
| **1. Develop Generative AI Solutions with Azure OpenAI Service** | RAG (Retrieval-Augmented Generation) mimarisinin çalışma prensipleri ve prompt mühendisliği. | Projenin LLM entegrasyonu ve bağlam (context) besleme şablonları bu standartlara göre yazılmıştır. |
| **2. Build an Azure AI Search Solution (Vektör Arama)** | Metinlerin vektör uzayına (Embedding) dönüştürülmesi ve kosinüs benzerliği ile anlamsal arama. | Yerel ChromaDB veri tabanımızın anlamsal arama (şifre = parola eşleşmesi) mantığına temel oluşturmuştur. |
| **3. Implement Security in Azure AI Search** | Vektör aramalarında meta-veri (metadata) filtreleme ve rol bazlı erişim denetimi. | Projedeki **Rol Tabanlı Güvenlik Filtresi** bu modülden esinlenerek vektör veri tabanı seviyesinde kodlanmıştır. |
| **4. Secure Access to Cloud Resources by using Microsoft Entra ID** | Çalışan kimliklerinin (OAuth/OIDC) güvenli doğrulanması ve dinamik yetki yönetimi. | Projedeki simüle edilen 5 farklı rolün, canlı sürümde otomatik olarak Entra ID SSO'dan çekilmesi planlanmıştır. |

---

## 🛠️ 3. Teoriden Pratiğe: Bilgilerin Uygulamaya Dönüştürülmesi

Microsoft Learn modüllerinden edinilen teorik bilgiler, projede 3 temel alanda somut çıktılara dönüştürülmüştür:

1. **Güvenlik Öncelikli Arama (Security Trimming):**
   * *Learn Çıktısı:* Microsoft Learn'de yer alan *"security filters in search indexes"* konsepti incelenmiştir.
   * *Uygulama:* Vektör veritabanı sorgulanırken yetkisiz dökümanların LLM bağlamına (context) girmemesi için sorgu anında metal-veri filtrelemesi (`allowed_roles` dizisi ile `$in` filtresi) yapılmıştır. Yetkisiz belge isimleri arayüzde dahi gizlenmiştir.

2. **İş Problemine Odaklanma ve KPI Yaklaşımı:**
   * *Learn Çıktısı:* Bulut projelerinde iş değeri ölçümleme metrikleri referans alınmıştır.
   * *Uygulama:* Çalışanların zaman kayıpları ve IT/HR servis masası operasyon maliyetlerini düşürmek üzere projeye canlı güncellenen bir **KPI Dashboard** eklenmiştir.

3. **Bulut Entegrasyonuna Hazır Tasarım (Azure Transition Roadmap):**
   * *Learn Çıktısı:* Azure AI Studio ve Prompt Flow ile ölçeklenebilir yapay zeka akış tasarımı.
   * *Uygulama:* Geliştirilen yerel RAG mimarisi, doğrudan **Azure AI Search** ve **Azure OpenAI (GPT-4o)** altyapısına taşınabilecek şekilde modüler API yapısında kurulmuştur.

---

## 🌟 4. Kazanımlar & Değerlendirme
Bu öğrenim süreci sayesinde;
* Sıfırdan başlanan bir **RAG (Retrieval-Augmented Generation)** yapay zeka pipeline'ı başarıyla ayağa kaldırılmış,
* Karmaşık bulut güvenliği standartları (Metadata filtering) yerel SQLite/ChromaDB üzerinde simüle edilmiş,
* Fikirden, jürinin canlı test edebileceği çalışan bir **prototipe** 48 saat içinde ulaşılmıştır.

*Microsoft Learn kullanımı, sadece yerel kod yazmayı değil; projenin kurumsal standartlarda nasıl ölçekleneceğini ve Azure üzerinde nasıl güvenliğe kavuşturulacağını anlamamı sağlayan en güçlü araç olmuştur.*
