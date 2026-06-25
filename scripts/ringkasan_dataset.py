"""
Ringkasan dataset penelitian + gambar alur pengolahan data.

Output:
- Ringkasan dataset ke console
- Daftar 13 komoditas ke console
- Gambar alur ke output/plots/alur_pengolahan_data.png
- CSV ringkasan ke output/tables/ringkasan_dataset_penelitian.csv
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE_DIR = Path(r"f:\PC Mas Indra\Project\ekspor")
TABLE_DIR = BASE_DIR / "output" / "tables"
PLOT_DIR = BASE_DIR / "output" / "plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# 1) RINGKASAN DATASET
# =========================================================
df = pd.read_csv(TABLE_DIR / "dataset_komoditas_inti.csv")

ringkasan = pd.DataFrame({
    "Komponen": [
        "Jumlah file CSV",
        "Periode",
        "Jumlah komoditas",
        "Jumlah observasi inti",
        "Sumber data"
    ],
    "Nilai": [
        4,
        "Januari 2023 – Februari 2026",
        df["Komoditas"].nunique(),
        int(df["Nilai_Ekspor_Juta_USD"].notna().sum()),
        "Badan Pusat Statistik (BPS)"
    ]
})

print("=== Ringkasan Dataset Penelitian ===")
print(ringkasan.to_string(index=False))

print("\nDaftar 13 Komoditas yang Dianalisis")
for i, kom in enumerate(sorted(df["Komoditas"].unique()), start=1):
    print(f"{i}. {kom}")

ringkasan.to_csv(TABLE_DIR / "ringkasan_dataset_penelitian.csv", index=False)

# =========================================================
# 2) GAMBAR ALUR PENGOLAHAN DATA
# =========================================================
def kotak(ax, x, y, text, width=2.3, height=0.9, facecolor="#ecf0f1"):
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.5, edgecolor="#2c3e50", facecolor=facecolor
    )
    ax.add_patch(box)
    ax.text(x + width / 2, y + height / 2, text,
            ha="center", va="center", fontsize=10, weight="bold")


def panah(ax, x1, y1, x2, y2):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="->", mutation_scale=15,
        linewidth=1.5, color="#2c3e50"
    )
    ax.add_patch(arrow)


fig, ax = plt.subplots(figsize=(14, 6))
ax.set_xlim(0, 14)
ax.set_ylim(0, 6)
ax.axis("off")

ax.text(7, 5.6, "Alur Pengolahan Data Penelitian",
        ha="center", va="center", fontsize=14, weight="bold")

# Baris utama
kotak(ax, 0.5, 3.8, "CSV mentah\n2023–2026")
kotak(ax, 3.2, 3.8, "Data cleaning\n& standardisasi")
kotak(ax, 5.9, 3.8, "Tidy dataset\n(dataset_lengkap)")
kotak(ax, 8.6, 3.8, "Dataset inti\n13 komoditas")
kotak(ax, 11.3, 3.8, "Analisis\nTren / Musiman /\nCV / CAGR / Cluster", width=2.5)

panah(ax, 2.8, 4.25, 3.2, 4.25)
panah(ax, 5.5, 4.25, 5.9, 4.25)
panah(ax, 8.2, 4.25, 8.6, 4.25)
panah(ax, 11.0, 4.25, 11.3, 4.25)

# Baris output
kotak(ax, 1.4, 1.4, "output/tables\nCSV hasil analisis")
kotak(ax, 5.2, 1.4, "output/plots\nGambar hasil analisis")
kotak(ax, 9.1, 1.4, "Dashboard\nStreamlit")
kotak(ax, 11.8, 1.4, "Policy brief\n& laporan", width=2.4)

# Panah turun dari analisis
panah(ax, 12.5, 3.8, 2.5, 2.35)
panah(ax, 12.5, 3.8, 6.3, 2.35)
panah(ax, 12.5, 3.8, 10.2, 2.35)
panah(ax, 12.5, 3.8, 12.9, 2.35)

ax.text(7, 0.4, "Data mentah → pembersihan → analisis → luaran penelitian",
        ha="center", va="center", fontsize=10, style="italic")

output_path = PLOT_DIR / "alur_pengolahan_data.png"
plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"\nGambar tersimpan di: {output_path}")
