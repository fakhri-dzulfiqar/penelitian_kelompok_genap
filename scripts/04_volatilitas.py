"""
Script 04: Analisis Volatilitas & Risiko
CV (Coefficient of Variation), ranking stabilitas, outliers

Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config import (
    PLOT_DIR, TABLE_DIR,
    KOMODITAS_SINGKAT, KOMODITAS_UNGGULAN,
    BULAN_LABEL, init_rcparams,
)

init_rcparams()
PLOT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLE_DIR / "dataset_komoditas_inti.csv")
df["Tanggal"] = pd.to_datetime(df["Tanggal"])

kom_inti = list(KOMODITAS_SINGKAT.keys())

# =====================================================================
# 4.1 COEFFICIENT OF VARIATION (CV) + RANKING
# =====================================================================
cv_list = []
for kom in kom_inti:
    sub = df[df["Komoditas"] == kom]["Nilai_Ekspor_Juta_USD"].dropna()
    mean_val = sub.mean()
    std_val = sub.std()
    cv = (std_val / mean_val) * 100 if mean_val > 0 else np.nan
    cv_list.append({
        "Komoditas": kom,
        "Singkat": KOMODITAS_SINGKAT[kom],
        "Mean": round(mean_val, 2),
        "Std": round(std_val, 2),
        "CV_%": round(cv, 2),
        "Min": round(sub.min(), 2),
        "Max": round(sub.max(), 2),
        "Range": round(sub.max() - sub.min(), 2),
    })

df_cv = pd.DataFrame(cv_list)
df_cv = df_cv.sort_values("CV_%", ascending=True)
df_cv.to_csv(TABLE_DIR / "volatilitas_cv.csv", index=False)

print("=== RANKING STABILITAS EKSPOR (CV terkecil = paling stabil) ===")
print(df_cv[["Singkat", "Mean", "Std", "CV_%", "Range"]].to_string(index=False))

# Visualisasi CV
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.RdYlGn_r(df_cv["CV_%"] / df_cv["CV_%"].max())
bars = ax.barh(df_cv["Singkat"], df_cv["CV_%"], color=colors, edgecolor="white")
ax.axvline(df_cv["CV_%"].mean(), color="gray", linestyle="--", alpha=0.7,
           label=f"Rata-rata CV = {df_cv['CV_%'].mean():.1f}%")
ax.set_xlabel("Coefficient of Variation (%)")
ax.set_title("Ranking Volatilitas Ekspor per Komoditas (CV%)", fontweight="bold")
ax.legend()
fig.tight_layout()
fig.savefig(PLOT_DIR / "ranking_cv.png")
plt.close(fig)

# =====================================================================
# 4.2 IDENTIFIKASI OUTLIERS — berdasarkan IQR
# =====================================================================
outliers_all = []
for kom in kom_inti:
    sub = df[df["Komoditas"] == kom][["Tanggal", "Nilai_Ekspor_Juta_USD"]].dropna()
    Q1 = sub["Nilai_Ekspor_Juta_USD"].quantile(0.25)
    Q3 = sub["Nilai_Ekspor_Juta_USD"].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = sub[(sub["Nilai_Ekspor_Juta_USD"] < lower) | (sub["Nilai_Ekspor_Juta_USD"] > upper)].copy()
    if len(outliers) > 0:
        outliers["Komoditas"] = KOMODITAS_SINGKAT[kom]
        outliers_all.append(outliers)

if outliers_all:
    df_outliers = pd.concat(outliers_all)
    df_outliers.to_csv(TABLE_DIR / "outliers.csv", index=False)
    print(f"\n=== OUTLIERS DITEMUKAN: {len(df_outliers)} titik ===")
    print(df_outliers[["Tanggal", "Komoditas", "Nilai_Ekspor_Juta_USD"]].head(20))

# =====================================================================
# 4.3 AMPLITUDO MUSIMAN
# =====================================================================
amplitude_list = []
for kom in kom_inti:
    sub = df[df["Komoditas"] == kom].groupby("Bulan")["Nilai_Ekspor_Juta_USD"].mean()
    amplitude_list.append({
        "Komoditas": KOMODITAS_SINGKAT[kom],
        "Puncak": BULAN_LABEL[int(sub.idxmax()) - 1],
        "Puncak_Nilai": round(sub.max(), 2),
        "Lembah": BULAN_LABEL[int(sub.idxmin()) - 1],
        "Lembah_Nilai": round(sub.min(), 2),
        "Amplitudo": round(sub.max() - sub.min(), 2),
        "Rasio_Puncak_Lembah": round(sub.max() / sub.min(), 2) if sub.min() > 0 else None,
    })

df_amp = pd.DataFrame(amplitude_list).sort_values("Amplitudo", ascending=False)
df_amp.to_csv(TABLE_DIR / "amplitudo_musiman.csv", index=False)

print("\n=== AMPLITUDO MUSIMAN (selisih puncak-lembah) ===")
print(df_amp[["Komoditas", "Puncak", "Lembah", "Amplitudo", "Rasio_Puncak_Lembah"]].to_string(index=False))

# Visualisasi
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(df_amp["Komoditas"], df_amp["Amplitudo"], color="teal", edgecolor="white")
ax.set_xlabel("Amplitudo (Juta US$)")
ax.set_title("Amplitudo Musiman per Komoditas", fontweight="bold")
fig.tight_layout()
fig.savefig(PLOT_DIR / "amplitudo_musiman.png")
plt.close(fig)

print(f"\n✅ Analisis volatilitas selesai. Hasil di: {TABLE_DIR}")
