# PR / Session Summary — APEX-V2 Phase 1 & 2

Bu PR, APEX-V2 projesinin **Faz 1 (Business Understanding)** ve **Faz 2 (Data Understanding / EDA)** gereksinimlerini karşılamak amacıyla yapılan geliştirmeleri içermektedir.

---

## 🚀 Değişiklik Özeti (Session Summary)

### 1. İş Problemi, Başarı Metrikleri & Hata Maliyetleri (Faz 1)
* **İş Kararı Bağlamı:** Üretken Yapay Zeka (GenAI) kullanımının öğrencilerin akademik tükenmişlik (`Burnout_Risk_Level`) risklerine etkisini erken aşamada tahmin etme problemi detaylandırıldı. Proaktif müdahalelerin yönlendirme servisleri üzerindeki önemi açıklandı.
* **Başarı Metrikleri:** Birincil metrik olarak Macro F1-Score (> 0.80), Recall (High Risk sınıfı için > 0.85) ve ROC-AUC (> 0.88) başarı kriterleri tanımlandı.
* **Maliyet Odaklı Tasarım:** Yüksek risk grubundaki bir öğrenciyi gözden kaçırmanın (False Negative) maliyetinin çok yüksek olduğu gerekçelendirilerek Recall (High) metriği önceliklendirildi.

### 2. Temiz Keşifsel Veri Analizi - EDA (Faz 2)
* **Yeniden Yazım:** `final_analysis.ipynb` dosyası hücre hücre sıfırdan, en temiz ve hatasız biçimde programatik olarak yeniden oluşturuldu.
* **Görsel Standartlar:** Plotly (`plotly_dark` teması) kullanılarak kurumsal renk uyumuyla (Low: Emerald, Medium: Amber, High: Rose/Red) 14 ayrı görselleştirme hazırlandı. Grafikler `figures/` dizinine kaydedildi.
* **Yorum Temizliği ve Düzeltmeler:** Analiz yorumlarında bulunan tüm kopya ve mükerrer cümleler giderildi. Korelasyon yorumundaki `"poziyat"` yazım hatası `"pozitif"` olarak düzeltildi.

### 3. Çözülen Sistem Hataları
* **Windows Kaleido Deadlock Çözümü:** Plotly grafik kaydederken Windows sistemlerinde kilitlenmelere yol açan `py-kaleido==0.2.1` paketi, `kaleido>=1.3.0` sürümüne yükseltilerek çözüldü. `requirements.txt` dosyası güncellendi.

### 4. Dosya Düzeni & Katkı Günlüğü (Handoff Hazırlığı)
* **plans_and_agents/ Klasörü:** İş planı (`PHASE_1_2_PLAN.md`) ve agent yönergeleri (`PHASE_1_2_AGENT.md`) bu klasöre taşınarak kök dizin sadeleştirildi.
* **Faz Katılım Günlüğü:** Ortaklaşa güncellenebilir bir faz katılım günlüğü olan [plans_and_agents/phase_logs.md](file:///c:/Users/fezam/Desktop/apex-classification/apex-classification/plans_and_agents/phase_logs.md) dosyası oluşturuldu. Bu günlükte kimin, hangi fazda, neyi, neden ve nasıl yaptığı kayıt altına alındı. `CLAUDE.md` proje ağacına eklendi.

---

## 📊 Git Diff İstatistikleri (Git Diff Stats)

Aşağıda, upstream ana repo (`cenkergultekin/apex-classification`) ile yapılan değişikliklerin karşılaştırma istatistikleri yer almaktadır:

```text
 CLAUDE.md                                          |     1 +
 figures/eda_categorical_Institutional_Policy.png   |   Bin 0 -> 47216 bytes
 figures/eda_categorical_Major_Category.png         |   Bin 0 -> 48317 bytes
 figures/eda_categorical_Paid_Subscription.png      |   Bin 0 -> 44521 bytes
 figures/eda_categorical_Primary_Use_Case.png       |   Bin 0 -> 56988 bytes
 figures/eda_categorical_Prompt_Engineering_Skill.png|   Bin 0 -> 48689 bytes
 figures/eda_categorical_Year_of_Study.png          |   Bin 0 -> 47975 bytes
 figures/eda_correlation_matrix.png                 |   Bin 0 -> 73890 bytes
 figures/eda_missing_value_heatmap.png              |   Bin 0 -> 59351 bytes
 figures/eda_numeric_Anxiety_Level_During_Exams.png |   Bin 0 -> 47209 bytes
 figures/eda_numeric_Pre_Semester_GPA.png           |   Bin 0 -> 56922 bytes
 figures/eda_numeric_Skill_Retention_Score.png      |   Bin 0 -> 57017 bytes
 figures/eda_numeric_Traditional_Study_Hours.png    |   Bin 0 -> 56171 bytes
 figures/eda_numeric_Weekly_GenAI_Hours.png         |   Bin 0 -> 62935 bytes
 figures/eda_target_distribution.png                |   Bin 0 -> 67201 bytes
 notebooks/final_analysis.ipynb                     | 14180 ++++++++++++++++++-
 plans_and_agents/PHASE_1_2_AGENT.md                |   374 +
 plans_and_agents/PHASE_1_2_PLAN.md                 |    95 +
 plans_and_agents/phase_logs.md                     |    50 +
 requirements.txt                                   |     2 +
 20 files changed, 14596 insertions(+), 106 deletions(-)
```

* **Toplam Etki:** 20 dosya değiştirildi, 14.596 satır eklendi, 106 satır silindi.
* **Görsel Çıktılar:** `figures/` klasöründe 14 adet PNG formatında Plotly çıktısı başarıyla oluşturuldu ve upstream reponun görsel gereksinimleri tamamlandı.
