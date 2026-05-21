"""
Missing value injection — v2
Orijinal dosyadan baslar, satir bazli olasilik ile eksik deger enjekte eder.
Calistir: python data/raw/inject_missing.py
"""

import pandas as pd
import numpy as np
import shutil

SEED = 42
rng = np.random.default_rng(SEED)

ORIGINAL = "C:/Users/cenkg/Desktop/apex-v2/data/raw/ai_student_impact_dataset_original.csv"
OUT      = "C:/Users/cenkg/Desktop/apex-v2/data/raw/ai_student_impact_dataset.csv"

orig = pd.read_csv(ORIGINAL)
df   = orig.copy()
n    = len(df)

def inject(df, col, p_array, rng):
    """Satir bazli olasilik ile NaN enjekte et."""
    p = np.clip(p_array, 0, 1)
    mask = rng.binomial(1, p).astype(bool)
    df.loc[mask, col] = np.nan
    return df

# ══════════════════════════════════════════════════════════════════
# 1. Weekly_GenAI_Hours  — MNAR, yaklasik %4
#    Hic kullanmayan veya cok az kullanan ogrenciler "N/A" birakti.
#    Yuksek kullanicilarda da kucuk rastlantisal dropout var.
# ══════════════════════════════════════════════════════════════════
h = orig["Weekly_GenAI_Hours"].values
p = np.where(h < 1,  0.28,
    np.where(h < 3,  0.09,
    np.where(h < 6,  0.02,
                     0.012)))
# Bireysel gurultu — ayni grupta bile herkes ayni oranda degil
p = p * rng.uniform(0.6, 1.4, n)
df = inject(df, "Weekly_GenAI_Hours", p, rng)

# ══════════════════════════════════════════════════════════════════
# 2. Prompt_Engineering_Skill — MAR, yaklasik %4
#    Strict_Ban kurumlarinda ogrenciler becerilerini aciklamak istemiyor.
#    Diger kurumlarda da kucuk ama sifir olmayan bir dropout var.
# ══════════════════════════════════════════════════════════════════
policy = orig["Institutional_Policy"]
p = np.where(policy == "Strict_Ban",          0.13,
    np.where(policy == "Allowed_With_Citation", 0.030,
                                                0.018))
p = p * rng.uniform(0.5, 1.5, n)
df = inject(df, "Prompt_Engineering_Skill", p, rng)

# ══════════════════════════════════════════════════════════════════
# 3. Skill_Retention_Score — MAR, yaklasik %3.5
#    Donem sonu degerlendirmesi; High burnout'lu ogrenciler bazi
#    degerlendirmelere girmedi veya sonuclari eksik yuklendi.
#    Graduate ogrencilerde de ek bir kayma var (farkli degerlendirme sistemi).
# ══════════════════════════════════════════════════════════════════
burnout = orig["Burnout_Risk_Level"]
year    = orig["Year_of_Study"]
p = np.where(burnout == "High",   0.11,
    np.where(burnout == "Medium", 0.030,
                                  0.012))
# Graduate ek etkisi
p = np.where(year == "Graduate", p + 0.025, p)
p = p * rng.uniform(0.6, 1.4, n)
df = inject(df, "Skill_Retention_Score", p, rng)

# ══════════════════════════════════════════════════════════════════
# 4. Anxiety_Level_During_Exams — MNAR, yaklasik %2.5
#    Cok yuksek kaygili ogrenciler soruyu atladi.
#    Cok dusuk kaygili ogrenciler de kimi zaman "bu bana uymuyor" diye
#    cevap vermedi — iki ucta da kucuk bir dropout var.
# ══════════════════════════════════════════════════════════════════
anx = orig["Anxiety_Level_During_Exams"].values
# U-sekli olasilik: dusuk ve yuksek ucta biraz daha fazla eksik
p = 0.008 + 0.055 * ((anx - 5.5) / 4.5) ** 2
p = p * rng.uniform(0.5, 1.5, n)
df = inject(df, "Anxiety_Level_During_Exams", p, rng)

# ══════════════════════════════════════════════════════════════════
# 5. Pre_Semester_GPA — MAR, yaklasik %3
#    Freshman ogrencilerin onceki GPA kaydi sistemde yok.
#    Graduate ogrencilerin bir kismi yurt disi veya farkli sistemden geldi.
#    Diger yillarda cok kucuk ama sifir olmayan rastlantisal kayma.
# ══════════════════════════════════════════════════════════════════
year = orig["Year_of_Study"]
p = np.where(year == "Freshman",  0.125,
    np.where(year == "Graduate",  0.028,
    np.where(year == "Sophomore", 0.012,
                                  0.009)))
p = p * rng.uniform(0.6, 1.4, n)
df = inject(df, "Pre_Semester_GPA", p, rng)

# ══════════════════════════════════════════════════════════════════
# 6. Post_Semester_GPA — MAR, yaklasik %1.8
#    Donem ortasinda bırakan ogrencilerin notu sisteme girilmemis.
#    High burnout grubunda bu oran belirgin sekilde daha yuksek.
# ══════════════════════════════════════════════════════════════════
burnout = orig["Burnout_Risk_Level"]
p = np.where(burnout == "High",   0.046,
    np.where(burnout == "Medium", 0.014,
                                  0.007))
p = p * rng.uniform(0.6, 1.4, n)
df = inject(df, "Post_Semester_GPA", p, rng)

# ══════════════════════════════════════════════════════════════════
# 7. Traditional_Study_Hours — MCAR, yaklasik %2
#    Rastlantisal anket dropout; soru sayfasinin sonunda yer aliyor.
#    Arts ve Humanities ogrencilerinde hafif artan dropout (yapilasik calisma
#    saatlerini belirsiz bulabilirler).
# ══════════════════════════════════════════════════════════════════
major = orig["Major_Category"]
p = np.where(major.isin(["Arts", "Humanities"]), 0.027, 0.017)
p = p * rng.uniform(0.5, 1.5, n)
df = inject(df, "Traditional_Study_Hours", p, rng)

# ══════════════════════════════════════════════════════════════════
# 8. Tool_Diversity — MCAR, yaklasik %1.5
#    Soru bazi ogrencilere belirsiz geldi; Beginner grubunda biraz daha fazla.
# ══════════════════════════════════════════════════════════════════
skill = orig["Prompt_Engineering_Skill"]
p = np.where(skill == "Beginner", 0.022, 0.012)
p = p * rng.uniform(0.6, 1.4, n)
df = inject(df, "Tool_Diversity", p, rng)

# ══════════════════════════════════════════════════════════════════
# 9. Perceived_AI_Dependency — MCAR, yaklasik %1
#    Kucuk, neredeyse tamamen rastlantisal dropout.
# ══════════════════════════════════════════════════════════════════
p = np.full(n, 0.010) * rng.uniform(0.7, 1.3, n)
df = inject(df, "Perceived_AI_Dependency", p, rng)

# ══════════════════════════════════════════════════════════════════
# RAPOR
# ══════════════════════════════════════════════════════════════════
print("\n=== EKSIKLIK RAPORU ===")
feature_cols = [c for c in df.columns if c not in ["Student_ID", "Burnout_Risk_Level"]]
missing = df[feature_cols].isnull().sum()
pct     = (missing / n * 100).round(2)
report  = pd.DataFrame({"Eksik": missing, "Oran(%)": pct})
report  = report[report["Eksik"] > 0].sort_values("Oran(%)", ascending=False)
print(report.to_string())

total_missing = missing.sum()
total_cells   = n * len(feature_cols)
print(f"\nToplam eksik  : {total_missing:,}")
print(f"Toplam hucre  : {total_cells:,}")
print(f"Genel oran    : {total_missing/total_cells*100:.2f}%")

print("\n=== SATIR BAZLI DAGILIM ===")
row_m = df.isnull().sum(axis=1)
print(row_m.value_counts().sort_index().to_string())

print("\n=== DOGALLIK KONTROL ===")
# Weekly_GenAI — MNAR sinav
mask_w = df["Weekly_GenAI_Hours"].isnull()
print(f"Weekly_GenAI | Eksik grp orijinal medyan : {orig.loc[mask_w,'Weekly_GenAI_Hours'].median():.2f}h")
print(f"Weekly_GenAI | Dolu  grp orijinal medyan : {orig.loc[~mask_w,'Weekly_GenAI_Hours'].median():.2f}h")

# Prompt_Skill — policy dagilimlari
print("\nPrompt_Skill eksiklik orani x Policy:")
print(df.groupby("Institutional_Policy")["Prompt_Engineering_Skill"]
        .apply(lambda x: f"{x.isnull().mean()*100:.1f}%").to_string())

# Skill_Retention — burnout dagilimlari
print("\nSkill_Retention eksiklik orani x Burnout:")
print(df.groupby("Burnout_Risk_Level")["Skill_Retention_Score"]
        .apply(lambda x: f"{x.isnull().mean()*100:.1f}%").to_string())

# Pre_GPA — year dagilimlari
print("\nPre_Semester_GPA eksiklik orani x Year:")
print(df.groupby("Year_of_Study")["Pre_Semester_GPA"]
        .apply(lambda x: f"{x.isnull().mean()*100:.1f}%").to_string())

df.to_csv(OUT, index=False)
print(f"\nKaydedildi: {OUT}")
