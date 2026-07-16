# Analisis Tren & Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia

**Peneliti:** Dr. Anindhyta Budiarti, S.E., M.M.  
**Institusi:** STIESIA Surabaya  
**Periode Data:** Januari 2023 – Februari 2026 (38 bulan)  
**Sumber Data:** BPS (Badan Pusat Statistik)

---

## 📁 Struktur Folder

```
ekspor/
├── *.csv                           # Data CSV mentah (2023–2026)
├── scripts/
│   ├── config.py                   # Shared config & helpers (paths, constants)
│   ├── 01_pembersihan.py           # Load, cleanup, reshape ke tidy data
│   ├── 02_eda.py                   # Eksplorasi data, plot tren, korelasi
│   ├── 03_tren_musiman.py          # MA-3/6, CAGR, dekomposisi time series
│   ├── 04_volatilitas.py           # CV, outliers, amplitudo musiman
│   ├── 05_clustering.py            # K-Means clustering + segmentasi
│   ├── 05b_matriks_strategis.py    # Matriks strategis CAGR × CV × Mean
│   ├── 06_dashboard.py             # Streamlit dashboard interaktif
│   └── ringkasan_dataset.py        # Ringkasan dataset & diagram alur
├── output/                         # Generated plots, tables, HTML
│   ├── plots/                      # Grafik hasil analisis (PNG/HTML)
│   └── tables/                     # Tabel hasil analisis (CSV)
├── desain penelitian.png           # Diagram desain riset
├── plaintext.md                    # Ekstraksi proposal penelitian
├── requirements.txt                # Python packages
├── README.md                       # File ini
└── .gitignore
```

## 🚀 Cara Menjalankan

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan script berurutan

```bash
# Fase 1: Pembersihan data
python scripts/01_pembersihan.py

# Fase 2: Eksplorasi
python scripts/02_eda.py

# Fase 3–5: Analisis
python scripts/03_tren_musiman.py
python scripts/04_volatilitas.py
python scripts/05_clustering.py
python scripts/05b_matriks_strategis.py
python scripts/ringkasan_dataset.py
```

### 3. Dashboard interaktif

```bash
streamlit run scripts/06_dashboard.py
```

## 📊 Metodologi

| Metode | Tujuan |
|--------|--------|
| Moving Average (MA-3, MA-6) | Menghaluskan fluktuasi, identifikasi tren jangka pendek & menengah |
| CAGR | Mengukur pertumbuhan tahunan per komoditas |
| Dekomposisi Additif & Multiplikatif | Memisahkan komponen tren, musiman, dan residual |
| Coefficient of Variation (CV) | Mengukur stabilitas/risiko per komoditas |
| K-Means Clustering | Segmentasi komoditas berdasarkan karakteristik kinerja |
| Matriks Strategis | Pemetaan kuadran: Pertumbuhan (CAGR) vs Risiko (CV) |

## 📦 Luaran

- [x] Script analisis lengkap (Python)
- [x] Dashboard interaktif (Streamlit)
- [x] Matriks strategis interaktif (Plotly HTML)
- [x] Laporan penelitian
- [x] Policy brief dan rekomendasi kebijakan
- [ ] Artikel ilmiah (target: Sinta 3)
