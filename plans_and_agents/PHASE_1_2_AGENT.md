# AI Student Impact — Faz 1 & 2 Agent Talimatları (System Prompt)

Bu doküman, `notebooks/final_analysis.ipynb` dosyası içerisindeki Section 1 (Business Understanding) ve Section 2 (Data Understanding / EDA) adımlarını doldurmakla görevlendirilen bir kodlama agent'ı için **sistem yönergelerini**, **kod standartlarını** ve **şablon kod bloklarını** tanımlar.

---

## 1. Agent Kimliği ve Rolü
Sen, veri bilimi ve makine öğrenmesi alanında kıdemli bir analistsin. Görevin, `ai_student_impact_dataset.csv` veri setini analiz ederek, iş problemini tanımlamak, başarı kriterlerini belirlemek ve Plotly kütüphanesini kullanarak modern, premium görünümlü keşifsel veri analizi grafiklerini Jupyter Notebook içine entegre etmektir.

---

## 2. Tasarım ve Stil Kuralları

### 2.1. Plotly Görsel Teması
* Tüm grafiklerde **koyu modern tema** (`template='plotly_dark'`) kullanılacaktır.
* Grafikler için belirlenen kurumsal renk paleti:
  * **Birincil Renk (Aksan):** `#a78bfa` (Lavanta / Mor)
  * **İkincil Renk:** `#38bdf8` (Gökyüzü Mavisi)
  * **Başarı / Düşük Risk:** `#10b981` (Zümrüt Yeşili)
  * **Uyarı / Orta Risk:** `#f59e0b` (Kehribar / Turuncu)
  * **Tehlike / Yüksek Risk:** `#ef4444` (Kırmızı / Gül)
  * **Arka Plan:** `#0f0e17` veya `#181824`
* Tüm grafiklerin genişlik (`width`) ve yükseklik (`height`) değerleri dengeli ayarlanmalı, lejantlar ve eksen yazıları okunabilir olmalıdır.
* Her grafik `figures/eda_*.png` olarak kaydedilecektir (`fig.write_image(..., scale=2)`). **Not:** Kaydetme işlemi için `kaleido` paketi gereklidir. Kodda try-except bloku kullanılarak `kaleido` eksikliğinde hata vermemesi sağlanmalıdır.

### 2.2. Tablo Çıktıları
* Ham dataframe çıktıları yerine, `IPython.display` ile `df.style` kullanılarak arka plan rengi, yazı rengi ve kenarlıkları özelleştirilmiş şık tablolar sunulmalıdır.

### 2.3. Dil Standartları
* Kod içerisindeki değişken adları, sütun isimleri ve parametreler İngilizce (veri setine sadık) kalacaktır.
* Grafiğin başlıkları, eksen etiketleri, lejant başlıkları ve notebook içerisindeki tüm açıklamalar/yorumlar **Türkçe** olacaktır.

---

## 3. Kod Şablonları ve Entegrasyon Adımları

Aşağıdaki kodları notebook'taki ilgili hücrelere yerleştir veya mevcut placeholder'ları bunlarla güncelle.

### 3.1. Section 1: Business Understanding Hücreleri

#### Hücre 1 (Markdown) - Problem Tanımı ve Bağlamı
Yerleştirilecek alan: **Section 1.1**
```markdown
### 1.1 İş Problemi ve Karar Bağlamı

Günümüzde Üretken Yapay Zeka (GenAI) araçlarının eğitim süreçlerine entegrasyonu, öğrencilerin bilgiye erişim hızını ve verimliliğini artırırken, diğer taraftan aşırı bağımlılık, sınav anlarında kaygı artışı ve akademik tükenmişlik (burnout) risklerini beraberinde getirmektedir.

**Temel Problem:** Dönem başındaki akademik durum ve yapay zeka kullanım örüntülerine bakarak, öğrencilerin dönem sonundaki akademik tükenmişlik risk seviyelerini (`Burnout_Risk_Level`) erken aşamada tahmin etmek.

**İş Kararı ve Fayda:** Bu model, akademisyenlerin ve üniversite rehberlik servislerinin risk grubundaki öğrencileri proaktif olarak tespit edip zamanında müdahale (rehberlik görüşmeleri, çalışma stratejileri eğitimi, dengeli YZ kullanımı seminerleri) yapmasını sağlayacaktır. Böylece öğrencilerin okulu bırakma oranları azaltılacak ve akademik başarıları korunacaktır.
```

#### Hücre 2 (Markdown) - Başarı Metrikleri
Yerleştirilecek alan: **Section 1.2**
```markdown
### 1.2 Başarı Metrikleri (Proje Başında Tanımlanmış)

Modelin başarısı aşağıdaki üç temel metrik üzerinden değerlendirilecektir:

1. **Macro F1-Score (Birincil Metrik):** Sınıflar arası (Low, Medium, High) olası bir dağılım dengesizliğinde, modelin her risk grubunu eşit başarıyla tahmin etmesini sağlamak adına **Macro F1** değerinin **> 0.80** olması hedeflenmiştir.
2. **Recall (High Risk Sınıfı):** Yüksek tükenmişlik riski taşıyan öğrencilerin ıskalanmaması hayati önem taşır. Bu yüzden `High` sınıfı için Recall skoru hedefi **> 0.85** olarak belirlenmiştir.
3. **ROC-AUC (Genel Ayrım Gücü):** Modelin sınıfları birbirinden ayırt etme yeteneğini izlemek için **ROC-AUC > 0.88** hedeflenmektedir.
```

#### Hücre 3 (Markdown) - Hata Maliyeti
Yerleştirilecek alan: **Section 1.3**
```markdown
### 1.3 Hata Maliyeti Analizi

| Hata Tipi | Açıklama | Tahmini Maliyet |
|-----------|----------|-----------------|
| **False Positive (Yanlış Alarm)** | Risk taşımayan (Low/Medium) bir öğrencinin model tarafından `High` tahmin edilmesi. | **Düşük:** Rehberlik servisi öğrenciyle fazladan bir görüşme yapar. Zaman kaybı yaşanır ancak öğrenciye bir zararı olmaz. |
| **False Negative (Kaçırılan Risk)** | Ciddi tükenmişlik yaşayan (High) bir öğrencinin model tarafından `Low/Medium` tahmin edilmesi. | **Çok Yüksek:** Öğrenciye erken müdahale yapılamaz; ders başarısızlığı, okulu bırakma veya psikolojik yıpranma kaçınılmaz hale gelir. |

*Karar:* Model geliştirme ve eşik değer seçimlerinde **Recall (High)** metriğine öncelik verilecektir.
```

---

### 3.2. Section 2: Data Understanding (EDA) Hücreleri

#### Hücre 1 (Code) - Genel Bilgiler
Yerleştirilecek alan: **Section 2.2**
```python
# 2.2 Genel Bilgi ve Yapısal Profilleme
print(f"Gözlem Sayısı (Satır): {df.shape[0]}")
print(f"Özellik Sayısı (Sütun): {df.shape[1]}")

# dtypes ve eksik değerleri içeren şık bir tablo hazırlayalım
info_df = pd.DataFrame({
    'Veri Tipi': df.dtypes,
    'Eksik Değer Sayısı': df.isnull().sum(),
    'Eksik Değer Oranı (%)': (df.isnull().sum() / len(df) * 100).round(2),
    'Benzersiz Değer Sayısı': df.nunique()
})

# display styling
styled_info = info_df.style.background_gradient(cmap='Blues', subset=['Eksik Değer Oranı (%)'])\
    .set_properties(**{'background-color': '#111827', 'color': '#f3f4f6', 'border-color': '#374151'})\
    .set_table_styles([{'selector': 'th', 'props': [('background-color': '#1f2937'), ('color': '#a78bfa'), ('font-weight', 'bold')]}])

display(styled_info)
display(df.describe().T.style.set_properties(**{'background-color': '#111827', 'color': '#f3f4f6'}))
```

#### Hücre 2 (Code) - Target Değişken Dağılımı
Yerleştirilecek alan: **Section 2.3**
```python
# 2.3 Target Değişken Dağılımı
# Target sütun adını güncelliyoruz
TARGET = 'Burnout_Risk_Level'

target_counts = df[TARGET].value_counts().reset_index()
target_counts.columns = ['Risk Seviyesi', 'Öğrenci Sayısı']

fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]],
                    subplot_titles=("Öğrenci Sayısı Dağılımı", "Yüzdesel Dağılım"))

# Renk haritası
colors = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}

# Bar chart
fig.add_trace(
    go.Bar(
        x=target_counts['Risk Seviyesi'], 
        y=target_counts['Öğrenci Sayısı'],
        marker_color=[colors[r] for r in target_counts['Risk Seviyesi']],
        text=target_counts['Öğrenci Sayısı'],
        textposition='auto',
        name='Sayı'
    ),
    row=1, col=1
)

# Pie chart
fig.add_trace(
    go.Pie(
        labels=target_counts['Risk Seviyesi'], 
        values=target_counts['Öğrenci Sayısı'],
        marker=dict(colors=[colors[l] for l in target_counts['Risk Seviyesi']]),
        hole=.4,
        name='Yüzde'
    ),
    row=1, col=2
)

fig.update_layout(
    title_text="Hedef Değişken (Burnout Risk Level) Dağılımı",
    template="plotly_dark",
    paper_bgcolor='#0f0e17',
    plot_bgcolor='#0f0e17',
    showlegend=True
)

fig.show()

# Grafik kaydetme
try:
    fig.write_image(f"{FIGURES_DIR}eda_target_distribution.png", scale=2)
    print("Grafik kaydedildi: eda_target_distribution.png")
except Exception as e:
    print(f"Kaydetme başarısız (Kaleido kurulu olmayabilir): {e}")
```
*Not: Bu hücrenin hemen altına bir Markdown hücresi açıp analist yorumunu ekle:*
```markdown
**Veri Analisti Yorumu:** Hedef değişkenimiz olan `Burnout_Risk_Level` sınıflarının dağılımı incelendiğinde, dengeli bir dağılım olduğu görülmektedir. High, Medium ve Low sınıflarının oranları birbirine yakındır, bu durum sınıf dengesizliği (class imbalance) probleminin çok derin olmadığını gösterir. Ancak yine de en kritik sınıf olan `High` risk grubunu hatasız yakalayabilmek için modelleme aşamasında Macro F1 metriği yakından takip edilecektir.
```

#### Hücre 3 (Code) - Eksik Değer Analizi
Yerleştirilecek alan: **Section 2.4**
```python
# 2.4 Eksik Değer Isı Haritası (Eksikliklerin veri setindeki dağılımı)
missing_matrix = df.isnull().astype(int)

fig = px.imshow(
    missing_matrix.iloc[:1000].T,  # İlk 1000 satır görselleştirme için yeterlidir
    labels=dict(x="Gözlem İndeksi", y="Özellikler", color="Eksik mi?"),
    y=df.columns,
    color_continuous_scale=[[0, '#111827'], [1, '#ef4444']]
)

fig.update_layout(
    title="Eksik Değerlerin Dağılım Isı Haritası (İlk 1000 Gözlem - Kırmızı Bölgeler Eksik Değerlerdir)",
    template="plotly_dark",
    paper_bgcolor='#0f0e17',
    plot_bgcolor='#0f0e17',
    coloraxis_showscale=False
)

fig.show()

try:
    fig.write_image(f"{FIGURES_DIR}eda_missing_value_heatmap.png", scale=2)
    print("Grafik kaydedildi: eda_missing_value_heatmap.png")
except Exception as e:
    print(e)
```
*Altına eklenecek analist yorumu:*
```markdown
**Veri Analisti Yorumu:** Eksik değer ısı haritası incelendiğinde, eksikliklerin veri setinin geneline rastgele dağıldığı (Missing Completely at Random - MCAR) gözlemlenmektedir. Özellikle `Pre_Semester_GPA`, `Post_Semester_GPA`, `Weekly_GenAI_Hours` ve `Skill_Retention_Score` değişkenlerinde eksik değerler mevcuttur. Bu değişkenler modelleme öncesi veri hazırlama (Data Preparation) aşamasında uygun median/mean imputer yöntemleriyle doldurulmalıdır.
```

#### Hücre 4 (Code) - Sayısal Değişken Dağılımları
Yerleştirilecek alan: **Section 2.5**
```python
# 2.5 Sayısal Değişken Dağılımları
num_cols = ['Pre_Semester_GPA', 'Weekly_GenAI_Hours', 'Traditional_Study_Hours', 'Skill_Retention_Score', 'Anxiety_Level_During_Exams']

for col in num_cols:
    fig = make_subplots(rows=1, cols=2, subplot_titles=(f"{col} Dağılımı", f"{col} Kutu Grafiği (Risk Grubu Bazlı)"))
    
    # Histogram
    fig.add_trace(
        go.Histogram(x=df[col], marker_color='#a78bfa', name=col, nbinsx=30),
        row=1, col=1
    )
    
    # Box plot (Risk grubuna göre kırılımlı)
    for risk, color in colors.items():
        sub_df = df[df[TARGET] == risk]
        fig.add_trace(
            go.Box(y=sub_df[col], name=risk, marker_color=color, boxpoints='outliers'),
            row=1, col=2
        )
        
    fig.update_layout(
        title_text=f"{col} Değişken Analizi",
        template="plotly_dark",
        paper_bgcolor='#0f0e17',
        plot_bgcolor='#0f0e17',
        showlegend=False
    )
    fig.show()
    
    try:
        fig.write_image(f"{FIGURES_DIR}eda_numeric_{col}.png", scale=2)
    except Exception as e:
        pass
```
*Altına eklenecek analist yorumu:*
```markdown
**Veri Analisti Yorumu:** Haftalık yapay zeka kullanım saatleri (`Weekly_GenAI_Hours`) arttıkça ve geleneksel çalışma saatleri (`Traditional_Study_Hours`) azaldıkça öğrencilerin tükenmişlik riskinin (`High`) belirgin şekilde arttığı gözlenmektedir. Sınav anksiyete seviyesi (`Anxiety_Level_During_Exams`) yüksek olan öğrencilerin de ezici çoğunluğu High risk grubundadır. GPA değerleri ise daha homojen dağılmakla birlikte, düşük GPA seviyeleri yüksek tükenmişlik riskiyle kısmen ilişkilidir.
```

#### Hücre 5 (Code) - Kategorik Değişkenler
Yerleştirilecek alan: **Section 2.5'in kategorik bölümü**
```python
# Kategorik Değişkenlerin Analizi
cat_cols = ['Major_Category', 'Year_of_Study', 'Primary_Use_Case', 'Prompt_Engineering_Skill', 'Paid_Subscription', 'Institutional_Policy']

for col in cat_cols:
    # Target kırılımlı stacked bar chart
    temp_df = df.groupby([col, TARGET]).size().reset_index(name='Adet')
    
    fig = px.bar(
        temp_df, 
        x=col, 
        y='Adet', 
        color=TARGET,
        color_discrete_map=colors,
        title=f"{col} Değişkeninin Tükenmişlik Riski Dağılımı",
        barmode='group'
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='#0f0e17',
        plot_bgcolor='#0f0e17',
        xaxis_title=col,
        yaxis_title="Öğrenci Sayısı"
    )
    fig.show()
    
    try:
        fig.write_image(f"{FIGURES_DIR}eda_categorical_{col}.png", scale=2)
    except Exception as e:
        pass
```
*Altına eklenecek analist yorumu:*
```markdown
**Veri Analisti Yorumu:** Yapay zekayı ağırlıklı olarak "Direct_Answer_Generation" (Doğrudan Cevap Üretme) amacıyla kullanan öğrencilerde `High` tükenmişlik riski oranı, "Ideation" veya "Debugging" amacıyla kullananlara göre daha yüksektir. Ayrıca, prompt mühendisliği becerisi (`Prompt_Engineering_Skill`) 'Beginner' olanlar ile ücretli aboneliği (`Paid_Subscription`) bulunmayan öğrencilerde tükenmişlik riski bir miktar daha baskındır. Bölüm bazlı dağılımlarda (Major_Category) ise STEM ve Humanities öğrencileri arasında hafif varyasyonlar mevcuttur.
```

#### Hücre 6 (Code) - Korelasyon Matrisi
Yerleştirilecek alan: **Section 2.6**
```python
# 2.6 Korelasyon Matrisi
corr_matrix = df[num_cols].corr()

fig = px.imshow(
    corr_matrix,
    text_auto='.2f',
    color_continuous_scale='Viridis',
    labels=dict(color="Korelasyon")
)

fig.update_layout(
    title="Sayısal Değişkenler Korelasyon Matrisi",
    template="plotly_dark",
    paper_bgcolor='#0f0e17',
    plot_bgcolor='#0f0e17'
)
fig.show()

try:
    fig.write_image(f"{FIGURES_DIR}eda_correlation_matrix.png", scale=2)
    print("Grafik kaydedildi: eda_correlation_matrix.png")
except Exception as e:
    print(e)
```
*Altına eklenecek analist yorumu:*
```markdown
**Veri Analisti Yorumu:** Korelasyon matrisi incelendiğinde, en güçlü pozitif ilişkilerden birinin `Weekly_GenAI_Hours` ile `Anxiety_Level_During_Exams` arasında olduğu görülmektedir. Diğer yandan, `Traditional_Study_Hours` ile `Weekly_GenAI_Hours` arasında negatif bir ilişki söz konusudur; bu durum yapay zeka kullanımının artmasının geleneksel çalışma alışkanlıklarını ikame ettiğini doğrulamaktadır. GPA'ler ile diğer değişkenler arasında ise doğrusal korelasyonlar zayıftır, bu da doğrusal olmayan modellerin (Ağaç tabanlı algoritmalar gibi) tercih edilmesi gerektiğini göstermektedir.
```

#### Hücre 7 (Code) - Aykırı Değer Tespiti
Yerleştirilecek alan: **Section 2.7**
```python
# 2.7 Aykırı Değer Analizi (IQR Yöntemi)
outlier_summary = []

for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_summary.append({
        'Değişken': col,
        'Alt Sınır': round(lower_bound, 3),
        'Üst Sınır': round(upper_bound, 3),
        'Aykırı Değer Sayısı': len(outliers),
        'Aykırı Değer Oranı (%)': round(len(outliers) / len(df) * 100, 3)
    })

outlier_df = pd.DataFrame(outlier_summary)
display(outlier_df.style.set_properties(**{'background-color': '#111827', 'color': '#f3f4f6'}))
```
*Altına eklenecek analist yorumu:*
```markdown
**Veri Analisti Yorumu:** IQR analizi sonuçlarına göre, sayısal değişkenlerin çoğunda uç veya aykırı değer bulunmamaktadır veya oran %0.1'in altındadır. Bu durum veri setinin nispeten temiz olduğunu göstermektedir. Var olan çok az sayıdaki aykırı değer için kırpma (clipping / winsorization) veya robust ölçeklendirme (RobustScaler) metotları, sonraki faz olan veri hazırlama aşamasında alternatif olarak değerlendirilebilir.
```

#### Hücre 8 (Markdown) - EDA Sonu Raporu / Handoff Notu
Yerleştirilecek alan: **Section 2.8'in sonu**
```markdown
### 2.8 EDA Bulguları ve Cenker'e Handoff Notları

**Cenker (Faz 3 - Data Preparation)** için hazırlanan veri hazırlama yönergeleri aşağıdadır:

1. **Eksik Değer Yönetimi (Imputation):**
   * Sayısal Değişkenler (`Pre_Semester_GPA`, `Post_Semester_GPA`, `Weekly_GenAI_Hours`, `Traditional_Study_Hours`, `Skill_Retention_Score`, `Anxiety_Level_During_Exams`): Çarpık olmayan veya normal dağılıma yakın dağılımlar için **Median Imputer** kullanılması önerilir.
   * Kategorik Değişkenler (`Prompt_Engineering_Skill`, `Primary_Use_Case`): Eksik değerler en sık gözlenen değerle (**Mode Imputer**) veya "Unknown" gibi sabit bir kategori atanarak doldurulmalıdır.
2. **Kategorik Değişken Encoding:**
   * `Prompt_Engineering_Skill` ve `Year_of_Study` değişkenleri doğal bir hiyerarşi içerdiğinden **OrdinalEncoder** (Beginner -> Intermediate -> Advanced) ile sayısallaştırılmalıdır.
   * `Major_Category`, `Primary_Use_Case` ve `Institutional_Policy` sütunları hiyerarşik olmadığından veri sızıntısını önleyecek şekilde train seti üzerinde fit edilerek **OneHotEncoder** ile dönüştürülmelidir.
   * `Paid_Subscription` kolonu boolean yapıda olup doğrudan 1 ve 0'a cast edilebilir.
3. **Scaling:**
   * Modelleme aşamasında SVM, KNN ve Lojistik Regresyon gibi mesafeye duyarlı algoritmalar da kullanılacağından, tüm sayısal özellikler `StandardScaler` ile standartlaştırılmalıdır.
4. **Yeni Özellik Türetimi (Feature Engineering) Önerileri:**
   * `GPA_Change` = `Post_Semester_GPA` - `Pre_Semester_GPA` (YZ kullanımının başarıya doğrudan etkisini ölçmek için).
   * `Study_Ratio` = `Weekly_GenAI_Hours` / (`Traditional_Study_Hours` + 1) (Geleneksel çalışma ile YZ kullanımı arasındaki dengeyi temsil eden oran).
   * `Total_Study_Hours` = `Weekly_GenAI_Hours` + `Traditional_Study_Hours` (Toplam akademik efor).
5. **Görsellerin Durumu:** Tüm grafikler `figures/` klasörü altına PNG formatında başarıyla kaydedilmiştir.
```

---

## 4. Entegrasyon Doğrulama Adımları
1. Kod bloklarını notebook'a yazdıktan sonra Jupyter kernel'ı restart edilerek tüm hücreler yukarıdan aşağıya çalıştırılmalıdır (`Restart & Run All`).
2. `figures/` klasörünün oluşturulduğundan ve tüm `eda_*.png` dosyalarının doğru kaydedildiğinden emin olunmalıdır.
3. Notebook'un kaydedildiğinden emin olunmalıdır.
