# APEX-V2 Proje Geçmişi ve Faz Katkı Günlüğü

Bu dosya, projedeki tüm fazların işlem adımlarını, kararlarını ve katkılarını takip etmek amacıyla ortaklaşa güncellenebilir bir günlük olarak tasarlanmıştır. Her ekip üyesi kendi fazını tamamladığında ilgili başlık altını ne yapıldığını, neden yapıldığını ve nasıl yapıldığını açıklayacak şekilde güncellemelidir.

---

## Faz 1 & Faz 2: Feza (Business Understanding & Keşifsel Veri Analizi - EDA)

### 1. Ne Yapıldı?
* **Problem ve Karar Bağlamı Tanımlandı:** Üretken Yapay Zeka (GenAI) kullanımının öğrencilerin akademik tükenmişlik (`Burnout_Risk_Level`) risklerine etkisini erken aşamada tahmin etme problemi tanımlandı. Proaktif rehberlik müdahalelerinin faydaları belirlendi.
* **Başarı Metrikleri Belirlendi:** Model değerlendirmesi için Macro F1-Score (> 0.80), Recall (High Risk sınıfı için > 0.85) ve ROC-AUC (> 0.88) hedefleri konuldu.
* **Hata Maliyeti Analizi Yapıldı:** Yüksek risk grubundaki bir öğrenciyi gözden kaçırmanın (False Negative) maliyetinin çok yüksek olduğu gerekçelendirilerek Recall (High) metriği önceliklendirildi.
* **Yapısal Profilleme ve Dağılım Analizleri:** 50.000 gözlemli `ai_student_impact_dataset.csv` veri seti yüklenerek, hedef değişkenin ve 8 sayısal ile 6 kategorik özelliğin dağılımları incelendi.
* **Eksik Değer ve Isı Haritası Analizi:** Eksik verilerin MCAR (Missing Completely at Random) dağıldığı ısı haritasıyla tespit edildi. Veri setindeki 9 adet eksik değer içeren sütun listelendi.
* **Korelasyon ve Aykırı Değer Analizleri:** Sayısal değişkenlerin korelasyonları, hedef değişken `Burnout_Risk_Level` ordinal hale getirilerek (`0, 1, 2`) çıkarıldı. Tukey (IQR) yöntemiyle 8 sayısal değişken için aykırı değerlerin oranının %0.1'in altında olduğu saptandı.
* **Veri Sızıntısı (Data Leakage) Değerlendirmesi:** `Post_Semester_GPA` dönem sonu verisi olduğundan veri sızıntısını önlemek amacıyla modelleme öncesi veri setinden düşürülmesi kararlaştırıldı. `GPA_Change` (Not Değişimi) türetim önerisi, `Post_Semester_GPA` içerdiği için sızıntı sebebiyle iptal edildi. `Skill_Retention_Score` için sızıntı izleme kararı alındı.
* **Analist Yorumları ve Notebook Temizliği:** Notebook'taki tüm mükerrer ve kopya açıklamalar giderilerek, veri analisti yorumları sıfırdan düzenlendi. `Primary_Use_Case` analizindeki yorum uyumsuzlukları giderildi.
* **Grafik Sayısı:** Toplamda 17 Plotly grafik çıktısı üretildi ve `figures/` dizinine kaydedildi.

### 2. Neden Yapıldı?
* Modelin iş kararlarına doğrudan entegre olabilmesi ve rehberlik danışmanlarına proaktif kararlarında doğru sinyaller verebilmesi için başarı metrikleri ve hata maliyet analizleri yapıldı.
* Sonraki modelleme ve veri hazırlama fazları için temiz, yapısal veriler sunmak, veri sızıntılarını en başta kesmek ve verideki doğrusal olmayan (ağaç tabanlı algoritmalar gibi) örüntülerin gereksinimlerini belirlemek amacıyla korelasyon, dağılım ve sızıntı analizleri yapıldı.

### 3. Nasıl Yapıldı?
* `notebooks/final_analysis.ipynb` dosyası hücre hücre sıfırdan, en temiz ve hatasız biçimde programatik olarak yeniden yazıldı ve review bulgularına göre güncellendi.
* Görselleştirmeler Plotly (`plotly_dark` temasıyla) kullanılarak kurumsal renk uyumuyla (Low: Emerald, Medium: Amber, High: Rose/Red) yapıldı.
* Grafiklerin kaydedilmesini sağlayan ve Windows işletim sisteminde kilitlenmelere sebep olan Kaleido kütüphanesi sürümü `kaleido>=1.3.0` olarak güncellenerek kilitlenme aşındı.
* Notebook baştan sona `Restart & Run All` ile koşturularak 0 hata ile kaydedildi ve `figures/` klasörü altına 17 grafik PNG formatında aktarıldı.

---

## Faz 3: Cenker (Data Preparation & Pipeline)

* **Durum:** ⏳ Beklemede (Cenker tarafından güncellenecektir)
* **Kişi:** Cenker
* **Beklenen Aksiyonlar:** Feza'nın handoff notlarına uygun olarak eksik değerlerin doldurulması (GPA için median, kategorikler için mode), One-Hot ve Ordinal encoding işlemleri, robust scaling yapılması ve pipeline'ın `pipeline.joblib` olarak kaydedilmesi.

---

## Faz 4 & Faz 5: Berkay (Modeling & Evaluation)

* **Durum:** ⏳ Beklemede (Berkay tarafından güncellenecektir)
* **Kişi:** Berkay
* **Beklenen Aksiyonlar:** En az 10 farklı sınıflandırma modelinin eğitilmesi, Cross-Validation ile karşılaştırılması, en iyi modelin hiperparametre optimizasyonu, Confusion Matrix ve ROC-AUC analizlerinin yapılması ve modelin `best_model.joblib` olarak kaydedilmesi.

---

## Faz 6: Ethem (Deployment & Tanıtım)

* **Durum:** ⏳ Beklemede (Ethem tarafından güncellenecektir)
* **Kişi:** Ethem
* **Beklenen Aksiyonlar:** Streamlit veya Gradio uygulaması geliştirilmesi, model entegrasyonu, web arayüzünün tamamlanması ve sunum hazırlığı.
