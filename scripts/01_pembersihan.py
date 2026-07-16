"""
Script 01: Pembersihan & Persiapan Data
Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import pandas as pd
import numpy as np
from pathlib import Path

from config import BASE_DIR, OUTPUT_DIR, TABLE_DIR, BULAN_MAP, BULAN_KOLOM, KOMODITAS_UNGGULAN

DATA_DIR = BASE_DIR

# --- 1. LOAD & GABUNG SEMUA FILE CSV ---
TAHUN_LIST = [2023, 2024, 2025, 2026]
df_all = []

for tahun in TAHUN_LIST:
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
df_long = pd.melt(
    df_raw,
    id_vars=["Komoditas","Tahun"],
    value_vars=BULAN_KOLOM,
    var_name="Bulan_Str",
    value_name="Nilai_Ekspor_Juta_USD"
)
df_long["Bulan"] = df_long["Bulan_Str"].map(BULAN_MAP)
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
df_inti = df_long[df_long["Komoditas"].isin(KOMODITAS_UNGGULAN)].copy()
df_agregat = df_long[~df_long["Komoditas"].isin(KOMODITAS_UNGGULAN)].copy()

print(f"\nKomoditas inti: {df_inti['Komoditas'].nunique()} item")
print(f"  → {df_inti['Komoditas'].unique().tolist()}")
print(f"Agregat: {df_agregat['Komoditas'].nunique()} item")
print(f"  → {df_agregat['Komoditas'].unique().tolist()}")

# --- 4. CEK DATA HILANG ---
missing = df_inti.isna().sum()
print(f"\nData hilang per kolom:\n{missing[missing > 0]}")

# --- 5. SIMPAN ---
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(exist_ok=True)

df_long.to_csv(TABLE_DIR / "dataset_lengkap.csv", index=False)
df_inti.to_csv(TABLE_DIR / "dataset_komoditas_inti.csv", index=False)
df_agregat.to_csv(TABLE_DIR / "dataset_agregat.csv", index=False)

print(f"\n✅ Semua data tersimpan di: {TABLE_DIR}")
print("Selesai — script 01.")
