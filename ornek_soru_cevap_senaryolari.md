# 💬 Karadeniz AI — Örnek Soru-Cevap Senaryoları

> Bu belge, Karadeniz Holding Kurumsal Bilgi Asistanı'nın (Karadeniz AI) için hazırlanmış gerçek kullanım senaryolarını içermektedir. Her senaryo; kullanıcı rolü, sorulan soru, sistemin nasıl davrandığı ve ürettiği örnek cevabı göstermektedir.

---

## 🎯 Sistemin Amacı

Karadeniz Holding bünyesinde 8 farklı departmana ait 120+ kurumsal belge (prosedür, politika, talimat, form) mevcuttur. Çalışanlar ihtiyaç duydukları bilgiye ulaşmak için saatler harcamakta, bu durum operasyonel verimsizliğe ve BT/İK destek biletlerinin artışına yol açmaktadır.

**Karadeniz AI**, bu belgelere doğal dil ile sorular sorarak saniyeler içinde ulaşmayı sağlar. Aynı zamanda **rol tabanlı yetkilendirme** sayesinde her çalışan yalnızca görev kapsamındaki belgelere erişebilir.

---

## 📋 Senaryo 1: İnsan Kaynakları — Yıllık İzin Sorgulama

| Alan                 | Detay                                     |
| -------------------- | ----------------------------------------- |
| **Kullanıcı Rolü**   | Tüm Çalışanlar                            |
| **Sorgulanan Belge** | İK-PR-02 — Yıllık İzin Yönetimi Prosedürü |
| **Erişim Yetkisi**   | Tüm Çalışanlar ✅                          |

### 💬 Kullanıcı Sorusu:
> *"Kaç günlük yıllık iznim var? Nasıl kullanırım?"*

### 🤖 Karadeniz AI Cevabı:
> Karadeniz Holding yıllık izin politikasına göre çalışma sürenize bağlı olarak aşağıdaki izin hakları geçerlidir:
>
> - **0-1 yıl:** 14 iş günü
> - **1-5 yıl:** 20 iş günü  
> - **5 yıl ve üzeri:** 26 iş günü
>
> İzin talebinizi **en az 5 iş günü öncesinden** amirinize bildirmeniz ve İnsan Kaynakları Departmanı'na **İK-FR-07 (İzin Talep Formu)** ile iletmeniz gerekmektedir. Onaylanan izinler İK sistemine işlenerek tarafınıza e-posta ile bildirilir.
>
> 📄 **Referans Belge:** İK-PR-02 — Yıllık İzin Yönetimi Prosedürü

### ✅ Test Sonucu:
Sistem, "yıllık izin" ile "tatil hakkı" gibi anlamca benzer ifadeleri de tanıyarak doğru belgeye yönlendirir (Semantic Search).

---

## 📋 Senaryo 2: Bilgi Teknolojileri — VPN Erişimi

| Alan                 | Detay                               |
| -------------------- | ----------------------------------- |
| **Kullanıcı Rolü**   | Tüm Çalışanlar                      |
| **Sorgulanan Belge** | BT-TA-01 — VPN Uzak Erişim Talimatı |
| **Erişim Yetkisi**   | Tüm Çalışanlar ✅                    |

### 💬 Kullanıcı Sorusu:
> *"Evden çalışırken şirket sistemlerine nasıl bağlanabilirim?"*

### 🤖 Karadeniz AI Cevabı:
> Şirket sistemlerine uzaktan erişim için Karadeniz Holding'in onaylı **VPN (Virtual Private Network)** çözümünü kullanmanız gerekmektedir. Adımlar:
>
> 1. BT Departmanı'ndan **VPN istemcisini** (Cisco AnyConnect) bilgisayarınıza yükleyin
> 2. Şirket e-postanız ile gelen **kimlik bilgilerinizi** kullanarak giriş yapın
> 3. Ağa bağlandıktan sonra dahili sistemlere normal masaüstünüzdeymiş gibi erişebilirsiniz
> 4. Çalışma bitiminde bağlantıyı **mutlaka kesin**
>
> Sorun yaşarsanız BT Destek Hattı'nı (dahili: 1234) arayın veya servicedesk@karadeniz.com adresine e-posta gönderin.
>
> 📄 **Referans Belge:** BT-TA-01 — VPN Uzak Erişim Talimatı

---

## 📋 Senaryo 3: BT Güvenlik — YETKİSİZ ERİŞİM ENGELLENDİ 🔐

| Alan                 | Detay                                               |
| -------------------- | --------------------------------------------------- |
| **Kullanıcı Rolü**   | Tüm Çalışanlar (düşük yetki)                        |
| **Sorgulanan Belge** | BT-PR-01 — BT Altyapısı Güvenlik ve Erişim Yönetimi |
| **Erişim Yetkisi**   | BT Departmanı 🔒                                     |

### 💬 Kullanıcı Sorusu:
> *"Karadeniz Holding'in güvenlik duvarı ve sunucu erişim politikası nedir?"*

### 🤖 Karadeniz AI Cevabı:
> ⛔ Bu bilgiye erişim yetkiniz bulunmamaktadır.
>
> Talep ettiğiniz bilgi **BT Departmanı** yetkisi gerektirmektedir. Erişim ihtiyacınız iş gereksinimi nedeniyle oluşmuşsa lütfen amiriniz aracılığıyla BT Departmanı ile iletişime geçiniz.

### ✅ Test Sonucu:
Sistem, yetkisiz kullanıcıya belgenin adını veya içeriğini **hiçbir şekilde** göstermez. Bu, Veri Tabanı seviyesinde ChromaDB metadata filtresi (`Erisim_Yetkisi: BT Departmanı`) ile güvence altına alınmıştır.

---

## 📋 Senaryo 4: BT Departmanı — YETKİ YÜKSELTİLDİ ✅

| Alan                 | Detay                                               |
| -------------------- | --------------------------------------------------- |
| **Kullanıcı Rolü**   | BT Departmanı                                       |
| **Sorgulanan Belge** | BT-PR-01 — BT Altyapısı Güvenlik ve Erişim Yönetimi |
| **Erişim Yetkisi**   | BT Departmanı ✅                                     |

### 💬 Kullanıcı Sorusu:
> *"Sunucu erişim talep prosedürü nedir?"*

### 🤖 Karadeniz AI Cevabı:
> Karadeniz Holding BT altyapısına sunucu erişim talebi için aşağıdaki adımları izleyin:
>
> 1. **Talep Formu:** BT-FR-01 formunu doldurun ve doğrudan amirinizdeki onayı alın
> 2. **BT Güvenlik İncelemesi:** Form BT Departmanı Güvenlik ekibine iletilir; iş gerekçesi incelenir
> 3. **Erişim Seviyesi Belirleme:** Minimum yetki prensibi (Least Privilege) uygulanır
> 4. **Onay ve Aktivasyon:** Onaylanan talepler 2 iş günü içinde aktive edilir
>
> ⚠️ Yetkisiz erişim girişimleri loglanmakta ve disiplin sürecini başlatmaktadır.
>
> 📄 **Referans Belge:** BT-PR-01 — BT Altyapısı Güvenlik ve Erişim Yönetimi

---

## 📋 Senaryo 5: Satın Alma — Tedarikçi Onay Süreci

| Alan                 | Detay                                                 |
| -------------------- | ----------------------------------------------------- |
| **Kullanıcı Rolü**   | Tüm Çalışanlar                                        |
| **Sorgulanan Belge** | SA-PR-01 — Satın Alma ve Tedarikçi Yönetimi Prosedürü |
| **Erişim Yetkisi**   | Tüm Çalışanlar ✅                                      |

### 💬 Kullanıcı Sorusu:
> *"Yeni bir tedarikçiyle çalışmak istiyorum. Onay süreci nasıl işliyor?"*

### 🤖 Karadeniz AI Cevabı:
> Karadeniz Holding'de yeni tedarikçi onay süreci şu adımlardan oluşmaktadır:
>
> **Aşama 1 — Ön Değerlendirme:**
> - SA-FR-03 (Tedarikçi Başvuru Formu) doldurulur
> - Tedarikçinin ticari sicil, vergi levhası ve referans belgelerini toplanır
>
> **Aşama 2 — Satın Alma Onayı:**
> - 50.000 TL altı alımlar: Birim Yöneticisi onayı yeterlidir
> - 50.000 TL – 500.000 TL: Satın Alma Müdürü onayı gerekir
> - 500.000 TL üzeri: Genel Müdür onayı zorunludur
>
> **Aşama 3 — Sözleşme:**
> - Hukuk departmanı sözleşmeyi inceler, imzalanır ve tedarikçi sisteme kaydedilir.
>
> 📄 **Referans Belge:** SA-PR-01 — Satın Alma Prosedürü

---

## 📋 Senaryo 6: Finans — Yönetim Yetkisi Gerektiren Sorgulama 🔐

| Alan                 | Detay                                                      |
| -------------------- | ---------------------------------------------------------- |
| **Kullanıcı Rolü**   | Tüm Çalışanlar (düşük yetki)                               |
| **Sorgulanan Belge** | FN-PO-01 — Bütçe Yönetimi ve Finansal Raporlama Politikası |
| **Erişim Yetkisi**   | Finans Departmanı / Yönetim 🔒                              |

### 💬 Kullanıcı Sorusu:
> *"Holding'in bütçe planlama süreci nasıl işliyor?"*

### 🤖 Karadeniz AI Cevabı:
> ⛔ Bu bilgiye erişim yetkiniz bulunmamaktadır.
>
> Bütçe planlama ve finansal raporlama bilgileri **Finans Departmanı ve Yönetim** yetkisi kapsamındadır. Erişim ihtiyacınız varsa Finans Departmanı ile iletişime geçiniz.

---

## 📋 Senaryo 7: Anlamsal Arama — Eş Anlamlı Kelime Testi

| Alan               | Detay                                    |
| ------------------ | ---------------------------------------- |
| **Kullanıcı Rolü** | Tüm Çalışanlar                           |
| **Amaç**           | RAG sisteminin anlamsal gücünü göstermek |

### 💬 Kullanıcı Sorusu:
> *"Şifre güvenliği kuralları neler?"* ← "parola" kelimesi değil, "şifre" kullanıldı

### 🤖 Karadeniz AI Cevabı:
> Karadeniz Holding Şifre (Parola) Güvenliği kuralları:
>
> - Şifreler **en az 12 karakter** uzunluğunda olmalıdır
> - Büyük harf, küçük harf, rakam ve özel karakter (!@#$) içermelidir
> - Şifreler **90 günde bir** değiştirilmelidir
> - Son 5 şifre yeniden kullanılamaz
> - 5 başarısız girişimde hesap **otomatik kilitlenir**
>
> 📄 **Referans Belge:** BT-PR-04 — Erişim Yetkilendirme ve Şifre Güvenliği Prosedürü

### ✅ Gösterilen Yetenek:
Belgede "parola" yazmasına rağmen sistem, "şifre" sorusunu doğru belgeyle eşleştirdi. Bu **Gemini Embedding'in anlamsal arama gücünü** kanıtlar — geleneksel keyword aramasının başaramayacağı bir eşleştirme.

---

## 📊 Senaryo Özet Tablosu

| #   | Soru Konusu            | Rol            | Beklenen Sonuç      | Test Durumu |
| --- | ---------------------- | -------------- | ------------------- | ----------- |
| 1   | Yıllık İzin Hakkı      | Tüm Çalışanlar | Cevap + Kaynak      | ✅ Çalışıyor |
| 2   | VPN / Uzaktan Erişim   | Tüm Çalışanlar | Cevap + Kaynak      | ✅ Çalışıyor |
| 3   | BT Güvenlik (Kısıtlı)  | Tüm Çalışanlar | ⛔ Erişim Engellendi | ✅ Çalışıyor |
| 4   | BT Güvenlik (Yetkili)  | BT Departmanı  | Cevap + Kaynak      | ✅ Çalışıyor |
| 5   | Tedarikçi Onay Süreci  | Tüm Çalışanlar | Cevap + Kaynak      | ✅ Çalışıyor |
| 6   | Finans Bütçe (Kısıtlı) | Tüm Çalışanlar | ⛔ Erişim Engellendi | ✅ Çalışıyor |
| 7   | Anlamsal Eşleştirme    | Tüm Çalışanlar | Doğru belge bulundu | ✅ Çalışıyor |

---
