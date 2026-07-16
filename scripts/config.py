"""
Shared configuration & helpers for all analysis scripts.
Centralizes paths, constants, and utility functions.
"""

from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────
# __file__ = scripts/config.py → parent.parent = project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "output"
PLOT_DIR = OUTPUT_DIR / "plots"
TABLE_DIR = OUTPUT_DIR / "tables"

# ── Month helpers ──────────────────────────────────────────────
BULAN_MAP = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6,
    "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12,
}
BULAN_KOLOM = list(BULAN_MAP.keys())
BULAN_LABEL = [
    "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
    "Jul", "Agu", "Sep", "Okt", "Nov", "Des",
]

# ── Commodities ────────────────────────────────────────────────
KOMODITAS_UNGGULAN = [
    "Sayur-sayuran", "Tembakau", "Jagung", "Kopi",
    "Tanaman Obat, Aromatik, dan Rempah-Rempah", "Lada Hitam", "Lada Putih",
    "Biji Kakao", "Buah-buahan Tahunan", "Sarang Burung",
    "Hasil Hutan Bukan Kayu Lainnya", "Ikan Segar/Dingin Hasil Tangkapan",
    "Rumput Laut dan Ganggang Lainnya",
]

KOMODITAS_SINGKAT = {
    "Sayur-sayuran": "Sayuran",
    "Tembakau": "Tembakau",
    "Jagung": "Jagung",
    "Kopi": "Kopi",
    "Tanaman Obat, Aromatik, dan Rempah-Rempah": "Tanaman Obat & Rempah",
    "Lada Hitam": "Lada Hitam",
    "Lada Putih": "Lada Putih",
    "Biji Kakao": "Kakao",
    "Buah-buahan Tahunan": "Buah Tahunan",
    "Sarang Burung": "Sarang Burung",
    "Hasil Hutan Bukan Kayu Lainnya": "Hasil Hutan Lain",
    "Ikan Segar/Dingin Hasil Tangkapan": "Ikan Segar",
    "Rumput Laut dan Ganggang Lainnya": "Rumput Laut",
}

# ── Plot colours ──────────────────────────────────────────────
WARNA_KUADRAN = {
    "Andalan": "#2ECC71",
    "Potensial": "#F39C12",
    "Stabil": "#3498DB",
    "Risiko Tinggi": "#E74C3C",
}

# ── Helpers ────────────────────────────────────────────────────


def aman_filename(s: str) -> str:
    """Sanitise string so it can be used as a filename."""
    return s.replace("/", "_").replace("\\", "_").replace(" ", "_").replace(",", "").lower()


def init_rcparams(dpi: int = 150, font_size: int = 10):
    """Apply consistent matplotlib global style."""
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.dpi": dpi,
        "font.size": font_size,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
    })


def hitung_cagr(nilai_awal: float, nilai_akhir: float, tahun: int = 2) -> float:
    """Compound Annual Growth Rate as a decimal (not percent)."""
    if nilai_awal <= 0 or nilai_akhir <= 0:
        return float("nan")
    return (nilai_akhir / nilai_awal) ** (1 / tahun) - 1
