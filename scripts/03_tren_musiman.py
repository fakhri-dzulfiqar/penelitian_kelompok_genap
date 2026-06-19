"""
Script 03: Analisis Tren dan Pola Musiman
Moving Average (MA-3, MA-6), CAGR, Dekomposisi Time Series

Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PLOT_DIR = BASE_DIR / "output" / "plots"
TABLE_DIR = BASE_DIR / "output" / "tables"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

def aman_filename(s):
    return s.replace("/", "_").replace("\\", "_").replace(" ", "_").replace(",", "").lower()

plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

# --- LOAD ---
df = pd.read_csv(TABLE_DIR / "dataset_komoditas_inti.csv")
df["Tanggal"] = pd.to_datetime(df["Tanggal"])
df.set_index("Tanggal", inplace=True)

komoditas_singkat = {
    "Sayur-sayuran": "Sayuran", "Tembakau": "Tembakau", "Jagung": "Jagung",
    "Kopi": "Kopi",
    "Tanaman Obat, Aromatik, dan Rempah-Rempah": "Tanaman Obat & Rempah",
    "Lada Hitam": "Lada Hitam", "Lada Putih": "Lada Putih",
    "Biji Kakao": "Kakao", "Buah-buahan Tahunan": "Buah Tahunan",
    "Sarang Burung": "Sarang Burung",
    "Hasil Hutan Bukan Kayu Lainnya": "Hasil Hutan Lain",
    "Ikan Segar/Dingin Hasil Tangkapan": "Ikan Segar",
    "Rumput Laut dan Ganggang Lainnya": "Rumput Laut",
}
kom_inti = list(komoditas_singkat.keys())

# =====================================================================
# 3.1 MOVING AVERAGE (MA-3 dan MA-6)
# =====================================================================
for komoditas in kom_inti:
    sub = df[df["Komoditas"] == komoditas]["Nilai_Ekspor_Juta_USD"].sort_index()
    if len(sub) < 6:
        continue

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(sub.index, sub, label="Aktual", linewidth=0.8, color="gray", alpha=0.6)
    ax.plot(sub.index, sub.rolling(3, center=True).mean(),
            label="MA-3", linewidth=1.5, color="steelblue")
    ax.plot(sub.index, sub.rolling(6, center=True).mean(),
            label="MA-6", linewidth=1.8, color="crimson")
    ax.set_title(f"Moving Average: {komoditas_singkat[komoditas]}", fontweight="bold")
    ax.set_ylabel("Nilai Ekspor (Juta US$)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fname = f"ma_{aman_filename(komoditas)}.png"
    fig.savefig(PLOT_DIR / fname)
    plt.close(fig)

print("✅ Plot MA-3 & MA-6 untuk semua komoditas tersimpan.")

# =====================================================================
# 3.2 CAGR (Compound Annual Growth Rate) — 2023 ke 2025
# =====================================================================
def hitung_cagr(nilai_awal, nilai_akhir, tahun):
    """CAGR = (nilai_akhir/nilai_awal)^(1/tahun) - 1, dalam persen"""
    if nilai_awal <= 0 or nilai_akhir <= 0:
        return np.nan
    return (nilai_akhir / nilai_awal) ** (1 / tahun) - 1

cagr_results = []
for komoditas in kom_inti:
    sub = df[df["Komoditas"] == komoditas]
    # Total per tahun
    total_tahunan = sub.groupby("Tahun")["Nilai_Ekspor_Juta_USD"].sum()
    if 2023 in total_tahunan.index and 2025 in total_tahunan.index:
        cagr = hitung_cagr(total_tahunan[2023], total_tahunan[2025], 2)
        cagr_results.append({
            "Komoditas": komoditas,
            "Total_2023": round(total_tahunan[2023], 1),
            "Total_2025": round(total_tahunan[2025], 1),
            "CAGR_%": round(cagr * 100, 2) if not np.isnan(cagr) else None
        })

df_cagr = pd.DataFrame(cagr_results).sort_values("CAGR_%", ascending=False)
df_cagr.to_csv(TABLE_DIR / "cagr.csv", index=False)
print("\n=== CAGR 2023–2025 ===")
print(df_cagr.to_string(index=False))

# =====================================================================
# 3.3 DEKOMPOSISI TIME SERIES (Aditif & Multiplikatif)
# =====================================================================
# Minimal 2 periode musiman penuh diperlukan. Kita punya 38 bulan (~3 tahun)
# Periode musiman = 12 bulan

for model_type in ["additive", "multiplicative"]:
    for komoditas in kom_inti:
        sub = df[df["Komoditas"] == komoditas]["Nilai_Ekspor_Juta_USD"].sort_index()
        if len(sub) < 24:  # butuh minimal 2 tahun
            continue

        # Ganti NaN dengan 0 untuk multiplikatif, atau interpolasi
        sub_filled = sub.fillna(0)
        if model_type == "multiplicative":
            sub_filled = sub_filled.replace(0, 0.001)  # hindari log(0)

        try:
            result = seasonal_decompose(sub_filled, model=model_type, period=12)
        except Exception:
            continue

        fig, axes = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
        components = [
            (result.observed, "Observed"),
            (result.trend, "Tren"),
            (result.seasonal, "Musiman"),
            (result.resid, "Residual"),
        ]
        for ax, (data_comp, label) in zip(axes, components):
            ax.plot(data_comp.index, data_comp, linewidth=1.0)
            ax.set_ylabel(label)
            ax.grid(True, alpha=0.3)

        axes[0].set_title(
            f"Dekomposisi {model_type.title()}: {komoditas_singkat[komoditas]}",
            fontweight="bold"
        )
        fig.tight_layout()
        fname = f"dekomp_{model_type}_{aman_filename(komoditas)}.png"
        fig.savefig(PLOT_DIR / fname)
        plt.close(fig)

    print(f"✅ Dekomposisi {model_type} selesai.")

# =====================================================================
# 3.4 RANGKUMAN INDEKS MUSIMAN
# =====================================================================
print("\n=== INDEKS MUSIMAN RATA-RATA ===")
for komoditas in kom_inti:
    sub = df[df["Komoditas"] == komoditas]["Nilai_Ekspor_Juta_USD"].sort_index().fillna(0)
    if len(sub) < 24:
        continue
    sub_filled = sub.replace(0, 0.001)

    try:
        result = seasonal_decompose(sub_filled, model="multiplicative", period=12)
        seasonal_avg = result.seasonal.groupby(result.seasonal.index.month).mean()
        print(f"{komoditas_singkat[komoditas]:20s} | {(seasonal_avg*100).round(1).to_string()}")
    except Exception:
        continue

print("\n✅ Analisis tren & musiman selesai.")
