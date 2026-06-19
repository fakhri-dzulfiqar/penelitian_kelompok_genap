"""
Script 01: Pembersihan & Persiapan Data
Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "output"

# --- 1. LOAD & GABUNG SEMUA FILE CSV ---
tahun_list = [2023, 2024, 2025, 2026]
df_all = []

for tahun in tahun_list:
    fname = f"Nilai Ekspor Bulanan Hasil Pertanian Menurut Komoditas , {tahun}.csv"
    file_path = DATA_DIR / fname

    if not file_path.exists():
        print(f"[WARN] File tidak ditemukan: {file_path}, dilewati.")
        continue

    # Header asli: baris 1-4, data mulai baris 5 (0-indexed: skiprows=4)
    df = pd.read_csv(file_path, skiprows=4, header=None)
    df.columns = ["Komoditas"] + [
        "Januari","Februari","Maret","April","Mei","Juni",
        "Juli","Agustus","September","Oktober","November","Desember","Tahunan"
    ]
    df["Tahun"] = tahun
    df_all.append(df)
    print(f"✔  {fname} — {len(df)} baris komoditas")

df_raw = pd.concat(df_all, ignore_index=True)
print(f"\nTotal gabungan: {len(df_raw)} baris x {len(df_raw.columns)} kolom")

# --- 2. RESHAPE KE FORMAT PANJANG (TIDY DATA) ---
bulan_map = {
    "Januari":1,"Februari":2,"Maret":3,"April":4,"Mei":5,"Juni":6,
    "Juli":7,"Agustus":8,"September":9,"Oktober":10,"November":11,"Desember":12
}
bulan_kolom = list(bulan_map.keys())

df_long = pd.melt(
    df_raw,
    id_vars=["Komoditas","Tahun"],
    value_vars=bulan_kolom,
    var_name="Bulan_Str",
    value_name="Nilai_Ekspor_Juta_USD"
)
df_long["Bulan"] = df_long["Bulan_Str"].map(bulan_map)
df_long.drop(columns=["Bulan_Str"], inplace=True)

# Konversi nilai numerik
df_long["Nilai_Ekspor_Juta_USD"] = pd.to_numeric(
    df_long["Nilai_Ekspor_Juta_USD"], errors="coerce"
)

# Buat kolom tanggal (untuk time series)
df_long["Tanggal"] = pd.to_datetime(
    df_long["Tahun"].astype(str) + "-" + df_long["Bulan"].astype(str) + "-01"
)

# Urutkan
df_long.sort_values(["Komoditas","Tanggal"], inplace=True)
df_long.reset_index(drop=True, inplace=True)

print(f"Data panjang: {len(df_long)} baris, {len(df_long.columns)} kolom")
print(df_long.head())

# --- 3. PISAHKAN KOMODITAS INTI VS AGREGAT ---
# Agregat: "Lainnya" dan "Jumlah"
komoditas_unggulan = [
    "Sayur-sayuran", "Tembakau", "Jagung", "Kopi",
    "Tanaman Obat, Aromatik, dan Rempah-Rempah", "Lada Hitam", "Lada Putih",
    "Biji Kakao", "Buah-buahan Tahunan", "Sarang Burung",
    "Hasil Hutan Bukan Kayu Lainnya", "Ikan Segar/Dingin Hasil Tangkapan",
    "Rumput Laut dan Ganggang Lainnya"
]

df_inti = df_long[df_long["Komoditas"].isin(komoditas_unggulan)].copy()
df_agregat = df_long[~df_long["Komoditas"].isin(komoditas_unggulan)].copy()

print(f"\nKomoditas inti: {df_inti['Komoditas'].nunique()} item")
print(f"  → {df_inti['Komoditas'].unique().tolist()}")
print(f"Agregat: {df_agregat['Komoditas'].nunique()} item")
print(f"  → {df_agregat['Komoditas'].unique().tolist()}")

# --- 4. CEK DATA HILANG ---
missing = df_inti.isna().sum()
print(f"\nData hilang per kolom:\n{missing[missing > 0]}")

# --- 5. SIMPAN ---
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df_clean_path = OUTPUT_DIR / "tables"
df_clean_path.mkdir(exist_ok=True)

df_long.to_csv(df_clean_path / "dataset_lengkap.csv", index=False)
df_inti.to_csv(df_clean_path / "dataset_komoditas_inti.csv", index=False)
df_agregat.to_csv(df_clean_path / "dataset_agregat.csv", index=False)

print(f"\n✅ Semua data tersimpan di: {df_clean_path}")
print("Selesai — script 01.")
