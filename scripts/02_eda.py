"""
Script 02: Eksplorasi Data (EDA)
Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import (
    BASE_DIR, PLOT_DIR, TABLE_DIR,
    KOMODITAS_SINGKAT, KOMODITAS_UNGGULAN,
    BULAN_LABEL, aman_filename, init_rcparams,
)

init_rcparams()
PLOT_DIR.mkdir(parents=True, exist_ok=True)

# --- LOAD DATA ---
df = pd.read_csv(TABLE_DIR / "dataset_lengkap.csv")
df["Tanggal"] = pd.to_datetime(df["Tanggal"])

kom_inti = KOMODITAS_UNGGULAN

# =====================================================================
# 2.1 STATISTIKA DESKRIPTIF
# =====================================================================
df_inti = df[df["Komoditas"].isin(kom_inti)].copy()

stats = df_inti.groupby("Komoditas")["Nilai_Ekspor_Juta_USD"].describe()
stats["CV %"] = (stats["std"] / stats["mean"]) * 100
stats["Range"] = stats["max"] - stats["min"]
stats = stats.sort_values("mean", ascending=False)

stats.to_csv(TABLE_DIR / "statistik_deskriptif.csv")
print("=== STATISTIKA DESKRIPTIF (urut rata-rata) ===")
print(stats.round(2))

# =====================================================================
# 2.2 LINE PLOT TREN — setiap komoditas dalam figure sendiri
# =====================================================================
for komoditas in kom_inti:
    fig, ax = plt.subplots(figsize=(10, 4))
    sub = df_inti[df_inti["Komoditas"] == komoditas]
    ax.plot(sub["Tanggal"], sub["Nilai_Ekspor_Juta_USD"],
            marker="o", markersize=3, linewidth=1.5, color="steelblue")
    ax.set_title(f"Tren Ekspor: {KOMODITAS_SINGKAT[komoditas]} (2023–Feb 2026)",
                 fontweight="bold")
    ax.set_ylabel("Nilai Ekspor (Juta US$)")
    ax.set_xlabel("")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fname = f"tren_{aman_filename(komoditas)}.png"
    fig.savefig(PLOT_DIR / fname)
    plt.close(fig)

print(f"\n✅ {len(kom_inti)} plot tren tersimpan.")

# =====================================================================
# 2.3 OVERLAY — semua komoditas dalam satu plot
# =====================================================================
fig, ax = plt.subplots(figsize=(12, 6))
for komoditas in kom_inti:
    sub = df_inti[df_inti["Komoditas"] == komoditas]
    ax.plot(sub["Tanggal"], sub["Nilai_Ekspor_Juta_USD"],
            label=KOMODITAS_SINGKAT[komoditas], linewidth=1.2)
ax.set_title("Perbandingan Tren Ekspor Seluruh Komoditas Unggulan", fontweight="bold")
ax.set_ylabel("Nilai Ekspor (Juta US$)")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=7)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(PLOT_DIR / "tren_overlay.png", bbox_inches="tight")
plt.close(fig)
print("✅ Plot overlay tersimpan.")

# =====================================================================
# 2.4 HEATMAP KORELASI ANTARKOMODITAS
# =====================================================================
pivot = df_inti.pivot_table(
    index="Tanggal", columns="Komoditas", values="Nilai_Ekspor_Juta_USD"
)
pivot.columns = [KOMODITAS_SINGKAT[c] for c in pivot.columns]

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(pivot.corr(), annot=True, fmt=".2f", cmap="RdYlBu",
            vmin=-1, vmax=1, center=0, linewidths=0.5, ax=ax)
ax.set_title("Korelasi Nilai Ekspor Antarkomoditas", fontweight="bold")
fig.tight_layout()
fig.savefig(PLOT_DIR / "heatmap_korelasi.png")
plt.close(fig)
print("✅ Heatmap korelasi tersimpan.")

# =====================================================================
# 2.5 SEASONAL SUB SERIES PLOT — rata-rata per bulan
# =====================================================================
n_kom = len(kom_inti)
fig, axes = plt.subplots(4, 4, figsize=(14, 12), sharex=True)
axes = axes.flatten()

for i, komoditas in enumerate(kom_inti):
    ax = axes[i]
    sub = df_inti[df_inti["Komoditas"] == komoditas]
    means = sub.groupby("Bulan")["Nilai_Ekspor_Juta_USD"].mean()
    ax.bar(BULAN_LABEL, means.values, color="steelblue", edgecolor="white")
    ax.set_title(KOMODITAS_SINGKAT[komoditas], fontsize=9)
    ax.tick_params(axis="x", rotation=45)

# Sembunyikan axes kosong
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

fig.suptitle("Rata-rata Nilai Ekspor per Bulan (2023–Feb 2026)", fontweight="bold", y=1.01)
fig.tight_layout()
fig.savefig(PLOT_DIR / "seasonal_subseries.png", bbox_inches="tight")
plt.close(fig)
print("✅ Seasonal subseries plot tersimpan.")

# =====================================================================
# 2.6 KOMODITAS DOMINAN — pie chart rata-rata ekspor
# =====================================================================
rata_rata = df_inti.groupby("Komoditas")["Nilai_Ekspor_Juta_USD"].mean().sort_values(ascending=False)
labels_short = [KOMODITAS_SINGKAT.get(k, k) for k in rata_rata.index]

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    rata_rata.values, labels=labels_short, autopct="%1.1f%%",
    startangle=140, textprops={"fontsize": 8}
)
ax.set_title("Komposisi Rata-rata Ekspor per Komoditas", fontweight="bold")
fig.savefig(PLOT_DIR / "pie_komoditas.png")
plt.close(fig)
print("✅ Pie chart komoditas dominan tersimpan.")

print(f"\n✅ EDA Selesai — semua plot di: {PLOT_DIR}")
