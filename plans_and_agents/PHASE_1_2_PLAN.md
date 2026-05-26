# AI Student Impact — Faz 1 & 2 Uygulama Planı (CRISP-DM)

Bu doküman, **Feza**'nın sorumluluğunda olan **Faz 1 (Business Understanding)** ve **Faz 2 (Data Understanding / EDA)** adımlarının detaylı uygulama planını ve metodolojisini içermektedir. Projenin standartları gereği tüm görselleştirmeler Plotly ile yapılacak ve şablon notebook (`notebooks/final_analysis.ipynb`) doldurulacaktır.

---

## 1. Faz 1: Business Understanding (İş Anlamlandırma)

### 1.1. Problem Cümlesi ve İş Bağlamı
Yapay zeka (özellikle Üretken YZ / GenAI) araçlarının öğrencilerin günlük çalışma rutinlerine girmesi, akademik performansı artırma potansiyeline sahipken aynı zamanda **öğrenme bağımlılığı**, **sınav kaygısı** ve en nihayetinde **akademik tükenmişlik (burnout)** gibi psikolojik ve yapısal riskleri de beraberinde getirmiştir. 

Bu projenin amacı: **Öğrencilerin dönem başındaki akademik performansları, demografik bilgileri, yapay zeka kullanım alışkanlıkları ve kurumsal politikalar altındaki davranışlarından hareketle, dönem sonundaki akademik tükenmişlik risk seviyelerini (`Burnout_Risk_Level`) tahmin etmektir.** 

Bu tahminleme modeli, üniversite yönetimlerinin ve öğrenci rehberlik merkezlerinin (psikolojik danışmanlık birimleri) proaktif olarak risk altındaki öğrencileri tespit etmesini ve erken müdahale (görüşme, yönlendirme, YZ kullanım eğitimleri) programları düzenlemesini sağlayacaktır.

### 1.2. Hedef Değişken Tanımı
* **Hedef Değişken (`Target`):** `Burnout_Risk_Level`
* **Sınıflar:** 
  * `Low` (Düşük Risk)
  * `Medium` (Orta Risk)
  * `High` (Yüksek Risk)
* **Problem Tipi:** 3 Sınıflı (Multi-class) Sınıflandırma.

### 1.3. Proje Başarı Metrikleri
Projenin doğası gereği başarıyı tek bir metrik yerine iş hedefleriyle uyumlu üçlü bir metrik setiyle değerlendireceğiz:
1. **Macro F1-Score (Birincil Metrik):** Veri setinde sınıf dengesizliği bulunması durumunda (örneğin High risk sınıfının azınlıkta olması), modelin her üç sınıfta da dengeli bir performans göstermesi kritik önem taşır. Bu nedenle optimizasyon odağımız Macro F1 olacaktır. Hedef: **> 0.80**.
2. **Recall (High Risk Sınıfı için):** Yüksek tükenmişlik riski olan bir öğrencinin gözden kaçırılması (False Negative) kabul edilemez bir risktir. Rehberlik servisinin bu öğrencileri kesinlikle yakalaması gerekir. Hedef: **> 0.85**.
3. **ROC-AUC (Genel Ayrım Gücü):** Modelin sınıfları birbirinden ayırt etme yeteneğini ölçmek amacıyla kullanılacaktır. Hedef: **> 0.88**.

### 1.4. Hata Maliyeti Analizi (Cost of Errors)

| Hata Tipi | Model Tahmini | Gerçek Durum | Akademik / İş Açısından Etki ve Tahmini Maliyet |
|-----------|---------------|--------------|-------------------------------------------------|
| **False Positive (Yanlış Alarm)** | High Risk | Low / Medium | Model, risk taşımayan bir öğrenciyi riskli olarak işaretler. Rehberlik servisi öğrenciyle boş yere görüşme yapar. **Maliyet: Düşük.** Sadece danışmanın zamanı harcanır. Öğrenci için hafif bir anksiyete yaratabilir ancak proaktif yaklaşım kapsamında tolere edilebilir. |
| **False Negative (Kaçırılan Risk)** | Low / Medium | High Risk | Model, gerçekten tükenmişlik yaşayan ve yardıma ihtiyacı olan bir öğrenciyi sağlıklı tahmin eder. **Maliyet: Çok Yüksek.** Öğrenciye zamanında ulaşılamaz; akademik başarısı düşebilir, dersleri veya okulu bırakabilir ya da ciddi psikolojik bunalımlar yaşayabilir. |

* **Stratejik Karar:** Modelin eşik değerleri (thresholds) veya algoritma parametreleri False Negative sayısını en aza indirecek (yani Recall'u maksimize edecek) şekilde ayarlanmalıdır.

---

## 2. Faz 2: Data Understanding (Keşifsel Veri Analizi - EDA)

EDA süreci, verideki örüntüleri ortaya çıkarmak, veri kalitesi sorunlarını tespit etmek ve modelleme öncesinde veri temizleme (imputation, scaling, encoding) kararlarını şekillendirmek için 8 adımdan oluşacaktır.

### 2.1. Adım: Veri Yükleme ve Yapısal Profilleme
* **Aksiyon:** `data/raw/ai_student_impact_dataset.csv` dosyası yüklenecek.
* **Görsel Standart:** Sütun adları, veri tipleri (`dtypes`), satır/sütun sayısı (`shape`) ve bellek kullanımı incelenerek premium bir HTML tablosu (`df.style` kullanılarak) ile gösterilecek.

### 2.2. Adım: Target Dağılımı ve Sınıf Dengesi
* **Aksiyon:** `Burnout_Risk_Level` dağılımı incelenecek.
* **Grafikler (Plotly):** Yan yana iki grafik (`make_subplots`):
  1. *Bar Chart*: Her risk seviyesinin öğrenci sayısı.
  2. *Pie Chart*: Yüzdesel dağılım (Dengeli / Dengesiz dağılım analizi için).
* **Tema:** Dark modern şablona uygun renk geçişleri (örneğin Low: Emerald, Medium: Amber, High: Rose).

### 2.3. Adım: Eksik Değer Analizi ve Isı Haritası
* **Aksiyon:** Her sütundaki eksik değer (`NaN`) sayıları ve oranları hesaplanacak.
* **Grafik (Plotly Heatmap):** Veri setindeki eksik değerlerin satır bazlı dağılımını gösteren ısı haritası. Hangi değişkenlerin eksikliklerinde korelasyon olduğu görselleştirilecek.
* **Analiz Yorumu:** Eksik değerlerin rastgele mi (MCAR/MAR) yoksa belirli örüntülere göre mi (MNAR) oluştuğu tartışılacak.

### 2.4. Adım: Sayısal Değişken Dağılımları (Univariate Analysis)
* **Aksiyon:** `Pre_Semester_GPA`, `Weekly_GenAI_Hours`, `Traditional_Study_Hours`, `Skill_Retention_Score`, `Anxiety_Level_During_Exams`, `Tool_Diversity`, `Perceived_AI_Dependency` ve `Post_Semester_GPA` (toplam 8 adet) değişkenleri incelenecek.
* **Grafik (Plotly):** Her sayısal değişken için yan yana histogram (dağılımı görmek için) ve box-plot (çeyreklikler ve yayılımı görmek için).
* **Analiz Yorumu:** Dağılımların normal dağılıma uygunluğu, çarpıklık (skewness) durumları tartışılacak. Not: `Post_Semester_GPA` değişkeninin veri sızıntısı oluşturması nedeniyle modelleme öncesi veri setinden düşürüleceği belirtilecektir.

### 2.5. Adım: Kategorik Değişken Frekans Analizi
* **Aksiyon:** `Major_Category`, `Year_of_Study`, `Primary_Use_Case`, `Prompt_Engineering_Skill`, `Paid_Subscription`, `Institutional_Policy` sütunları incelenecek.
* **Grafik (Plotly):** Her kategorik değişken için frekans bar grafikleri (Grouped or Stacked by Target - `Burnout_Risk_Level`).
* **Analiz Yorumu:** Örneğin, belirli bölümlerde (Major_Category) veya yapay zekayı belirli amaçlarla kullananlarda (Primary_Use_Case) tükenmişlik oranlarının nasıl değiştiği açıklanacak. `Primary_Use_Case` analizinde riskin tüm kullanım amaçlarında dengeli olduğu (%25-%28 bandı) ve `Debugging/Troubleshooting` grubunun hacimsel lider olduğu vurgulanacaktır.

### 2.6. Adım: Korelasyon Matrisi (Multivariate Analysis)
* **Aksiyon:** Sayısal değişkenlerin Pearson korelasyon katsayıları hesaplanacak. Hedef değişken `Burnout_Risk_Level` de ordinal olarak (`Low`: 0, `Medium`: 1, `High`: 2) matrise dahil edilecek.
* **Grafik (Plotly Heatmap):** Korelasyon katsayılarını renk skalasıyla gösteren, hücre içi değerleri yazılı matris grafiği.
* **Analiz Yorumu:** `Weekly_GenAI_Hours` ve `Perceived_AI_Dependency` gibi değişkenlerin hedef değişkenle olan doğrusal ilişkileri ile geleneksel çalışma saatleri arasındaki negatif korelasyon yorumlanacak.

### 2.7. Adım: Aykırı Değer (Outlier) Tespiti
* **Aksiyon:** 8 sayısal sütunda Tukey yöntemi (IQR = Q3 - Q1) kullanılarak alt sınır ($Q1 - 1.5 \times IQR$) ve üst sınır ($Q3 + 1.5 \times IQR$) dışındaki aykırı değerler belirlenecek.
* **Görsel:** Aykırı değerleri gösteren hedef bazlı box-plot grafikleri.
* **Analiz Yorumu:** Tespit edilen aykırı değerlerin silinmesi mi gerektiği (anomaly) yoksa veri setinin doğal bir varyasyonu mu olduğu ve modelleme öncesi kırpma (clipping) önerisi tartışılacak.

### 2.8. Adım: Veri Sızıntısı (Data Leakage) Değerlendirmesi
* **Aksiyon:** Dönem başında bilinmeyen ve hedefe bağlı olarak sızıntı yapabilecek özellikler değerlendirilecek.
* **İçerik:**
  * `Post_Semester_GPA` dönem sonu verisi olduğundan veri sızıntısını önlemek amacıyla kesinlikle modelden düşürülecektir.
  * `GPA_Change` (Not Değişimi) türetim önerisi, `Post_Semester_GPA` içerdiği için veri sızıntısı sebebiyle iptal edilmiştir.
  * `Skill_Retention_Score` (Beceri Kalıcılığı Skoru) dönem içi bir değerlendirme olarak kabul edilmiş olup, model üzerindeki etkisi sızıntı şüphesine karşı yakından izlenecektir.

### 2.9. Adım: EDA Sonu Handoff Notları ve Raporlama
* **Aksiyon:** Sonraki adımı devralacak olan **Cenker (Faz 3)** için net bir veri hazırlama stratejisi sunulacak.
* **İçerik:**
  * Eksik değer barındıran tüm 9 sütun (`Pre_Semester_GPA`, `Post_Semester_GPA`, `Weekly_GenAI_Hours`, `Skill_Retention_Score`, `Tool_Diversity`, `Perceived_AI_Dependency`, `Traditional_Study_Hours`, `Prompt_Engineering_Skill`, `Anxiety_Level_During_Exams`) ve önerilen dolgu (imputation) yöntemleri (sayısallar için median, kategorikler için mode).
  * Hangi kategorik sütunların Ordinal (örn: `Year_of_Study`, `Prompt_Engineering_Skill`) hangilerinin One-Hot (örn: `Major_Category`, `Primary_Use_Case`) encode edilmesi gerektiği.
  * Hangi sayısal sütunların ölçeklendirilmeye (scaling) ihtiyaç duyduğu.
  * `Post_Semester_GPA` sütununun veri sızıntısı nedeniyle veri setinden düşürülmesi gerektiği.
  * EDA süresince üretilen tüm 17 grafik dosyasının `figures/` klasörüne kaydedilmesi doğrulanacak.

---

## 3. Görsel ve Yazım Standartları
* **Kütüphaneler:** Tüm grafikler sadece **Plotly** (`plotly.express` veya `plotly.graph_objects`) ile oluşturulacaktır. `matplotlib` veya `seaborn` kullanılmayacaktır.
* **Tema:** Şablondaki modern koyu tema arka planı ve renk harmonisi (`ggplot2` veya özel dark temalar) korunacaktır.
* **Yorum Zorunluluğu:** Her grafiğin altında kalın (`**Veri Analisti Yorumu:**`) ile başlayan ve grafikten elde edilen iş odaklı 2-3 cümleyi içeren açıklama hücresi bulunacaktır.
* **İngilizce-Türkçe Uyumu:** Kod içi isimlendirmeler ve değişkenler orijinal veri setindeki gibi (İngilizce) bırakılacak, ancak analiz metinleri, başlıklar ve yorumlar tamamen Türkçe yazılacaktır.
