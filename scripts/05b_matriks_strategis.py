"""
Script 05b: Matriks Strategis — Integrasi CAGR × CV × Mean
Mengelompokkan komoditas ke kuadran strategis untuk rekomendasi kebijakan.

Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PLOT_DIR = BASE_DIR / "output" / "plots"
TABLE_DIR = BASE_DIR / "output" / "tables"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLE_DIR / "dataset_komoditas_inti.csv")
df["Tanggal"] = pd.to_datetime(df["Tanggal"])

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
# 1. HITUNG METRIK PER KOMODITAS
# =====================================================================
metrics = []
for kom in kom_inti:
    sub = df[df["Komoditas"] == kom]["Nilai_Ekspor_Juta_USD"].dropna()

    # Rata-rata ekspor
    mean_val = sub.mean()

    # CV (volatilitas)
    cv = (sub.std() / mean_val * 100) if mean_val > 0 else 0

    # CAGR 2023→2025
    total_tahunan = df[df["Komoditas"] == kom].groupby("Tahun")["Nilai_Ekspor_Juta_USD"].sum()
    if 2023 in total_tahunan.index and 2025 in total_tahunan.index:
        awal = total_tahunan[2023]
        akhir = total_tahunan[2025]
        cagr = ((akhir / awal) ** (1/2) - 1) if awal > 0 and akhir > 0 else 0
    else:
        cagr = 0

    # Tren (slope regresi linear)
    sub_sorted = sub.sort_index()
    x = np.arange(len(sub_sorted))
    y = sub_sorted.values
    slope = np.polyfit(x, y, 1)[0] if len(x) > 1 else 0

    # Amplitudo musiman
    monthly_avg = df[df["Komoditas"] == kom].groupby("Bulan")["Nilai_Ekspor_Juta_USD"].mean()
    amplitude = monthly_avg.max() - monthly_avg.min()

    metrics.append({
        "Komoditas": kom,
        "Singkat": komoditas_singkat[kom],
        "Mean_Juta_USD": round(mean_val, 2),
        "CV_%": round(cv, 2),
        "CAGR_%": round(cagr * 100, 2),
        "Slope": round(slope, 3),
        "Amplitudo_Musiman": round(amplitude, 2),
    })

df_metrics = pd.DataFrame(metrics)

# =====================================================================
# 2. KLASIFIKASI KUADRAN STRATEGIS
# =====================================================================
median_cv = df_metrics["CV_%"].median()
median_cagr = df_metrics["CAGR_%"].median()

def klasifikasi_kuadran(row):
    if row["CAGR_%"] >= median_cagr and row["CV_%"] <= median_cv:
        return "Andalan"
    elif row["CAGR_%"] >= median_cagr and row["CV_%"] > median_cv:
        return "Potensial"
    elif row["CAGR_%"] < median_cagr and row["CV_%"] <= median_cv:
        return "Stabil"
    else:
        return "Risiko Tinggi"

df_metrics["Kuadran"] = df_metrics.apply(klasifikasi_kuadran, axis=1)
df_metrics["Ukuran_Bubble"] = df_metrics["Mean_Juta_USD"]

# Simpan tabel
df_metrics.to_csv(TABLE_DIR / "matriks_strategis.csv", index=False)

print("=== MATRIKS STRATEGIS: CAGR × CV × Mean ===")
print(f"Median CV: {median_cv:.1f}%")
print(f"Median CAGR: {median_cagr:.1f}%\n")
pivot = df_metrics.pivot_table(
    index="Kuadran", aggfunc={"Singkat": list, "Mean_Juta_USD": "mean", "CAGR_%": "mean", "CV_%": "mean"}
)
pivot.columns = ["Rata_CAGR_%", "Rata_CV_%", "Rata_Mean", "Anggota"]
pivot = pivot[["Anggota", "Rata_Mean", "Rata_CAGR_%", "Rata_CV_%"]]
for _, row in pivot.iterrows():
    print(f"{row.name}:")
    print(f"  Anggota: {', '.join(row['Anggota'])}")
    print(f"  Rata-rata Ekspor: {row['Rata_Mean']:.1f} Juta USD")
    print(f"  Rata-rata CAGR: {row['Rata_CAGR_%']:.1f}%")
    print(f"  Rata-rata CV: {row['Rata_CV_%']:.1f}%\n")

# =====================================================================
# 3. VISUALISASI BUBBLE CHART INTERAKTIF (Plotly)
# =====================================================================
# Warna per kuadran
warna_kuadran = {
    "Andalan": "#2ECC71",
    "Potensial": "#F39C12",
    "Stabil": "#3498DB",
    "Risiko Tinggi": "#E74C3C",
}

# Bubble chart utama: CAGR vs CV, ukuran = Mean
fig = px.scatter(
    df_metrics,
    x="CV_%",
    y="CAGR_%",
    size="Ukuran_Bubble",
    color="Kuadran",
    color_discrete_map=warna_kuadran,
    text="Singkat",
    hover_data={
        "Singkat": False,
        "Komoditas": True,
        "Mean_Juta_USD": ":.2f",
        "CV_%": ":.2f",
        "CAGR_%": ":.2f",
        "Amplitudo_Musiman": ":.2f",
        "Ukuran_Bubble": False,
    },
    labels={
        "CV_%": "CV (%) — Volatilitas (semakin kanan semakin fluktuatif)",
        "CAGR_%": "CAGR (%) — Pertumbuhan Tahunan",
    },
    title="Matriks Strategis Ekspor: Pertumbuhan vs Risiko",
)

# Garis median sebagai pembatas kuadran
fig.add_hline(
    y=median_cagr, line_dash="dash", line_color="gray",
    annotation_text=f"Median CAGR: {median_cagr:.1f}%",
    annotation_position="bottom left"
)
fig.add_vline(
    x=median_cv, line_dash="dash", line_color="gray",
    annotation_text=f"Median CV: {median_cv:.1f}%",
    annotation_position="top right"
)

fig.update_traces(
    textposition="top center",
    marker=dict(line=dict(width=1, color="black")),
)
fig.update_layout(
    width=900, height=650,
    xaxis=dict(zeroline=False),
    yaxis=dict(zeroline=False),
)

fig.write_html(PLOT_DIR / "matriks_strategis.html")
try:
    fig.write_image(PLOT_DIR / "matriks_strategis.png", width=1000, height=700, engine="auto")
except Exception:
    pass  # kaleido gak terinstall, PNG skip
print("✅ Bubble chart matriks strategis tersimpan (HTML)")

# ---- Pendukung: CAGR vs Mean ----
fig2 = px.scatter(
    df_metrics,
    x="Mean_Juta_USD",
    y="CAGR_%",
    size="Ukuran_Bubble",
    color="Kuadran",
    color_discrete_map=warna_kuadran,
    text="Singkat",
    hover_data={"Singkat": False, "Komoditas": True, "CV_%": ":.2f"},
    labels={
        "Mean_Juta_USD": "Rata-rata Ekspor (Juta US$)",
        "CAGR_%": "CAGR (%) — Pertumbuhan Tahunan",
    },
    title="Pertumbuhan vs Skala Ekspor",
)
fig2.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="black")))
fig2.add_hline(y=median_cagr, line_dash="dash", line_color="gray")
fig2.update_layout(width=900, height=600)
fig2.write_html(PLOT_DIR / "matriks_cagr_mean.html")

# ---- Pendukung: CV vs Mean ----
fig3 = px.scatter(
    df_metrics,
    x="Mean_Juta_USD",
    y="CV_%",
    size="Ukuran_Bubble",
    color="Kuadran",
    color_discrete_map=warna_kuadran,
    text="Singkat",
    hover_data={"Singkat": False, "Komoditas": True, "CAGR_%": ":.2f"},
    labels={
        "Mean_Juta_USD": "Rata-rata Ekspor (Juta US$)",
        "CV_%": "CV (%) — Volatilitas",
    },
    title="Skala Ekspor vs Risiko",
)
fig3.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="black")))
fig3.add_vline(x=df_metrics["Mean_Juta_USD"].median(), line_dash="dash", line_color="gray")
fig3.update_layout(width=900, height=600)
fig3.write_html(PLOT_DIR / "matriks_cv_mean.html")

print("\n✅ Matriks strategis selesai — semua file di output/")
