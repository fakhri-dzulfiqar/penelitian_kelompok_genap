# LAPORAN PELAKSANAAN PENELITIAN

**Judul:** Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia Periode Januari 2023 - Februari 2026  
**Ketua Peneliti:** Dr. Anindhyta Budiarti, S.E., M.M.  
**Institusi:** STIESIA Surabaya  
**Tahun Pelaksanaan:** 2026  

---

## 1. HASIL PELAKSANAAN PENELITIAN

Hasil pelaksanaan penelitian yang telah dicapai selama periode observasi 38 bulan (Januari 2023 – Februari 2026) diuraikan secara ringkas di bawah ini berdasarkan metodologi kuantitatif eksplanatori yang direncanakan.

### A. Deskripsi Data dan Integrasi Dataset
Data sekunder bulanan nilai ekspor dari Badan Pusat Statistik (BPS) untuk 13 komoditas pertanian unggulan berhasil dibersihkan, di-reshape dari format lebar (*wide*) ke format panjang (*tidy*), dan digabungkan menjadi satu dataset tunggal berisi 720 baris data observasi. Komoditas tersebut meliputi: Sayuran, Tembakau, Jagung, Kopi, Tanaman Obat & Rempah, Lada Hitam, Lada Putih, Kakao, Buah Tahunan, Sarang Burung, Hasil Hutan Bukan Kayu (HHBK), Ikan Segar, dan Rumput Laut.

### B. Analisis Tren dan Moving Average (MA-3 dan MA-6)
Melalui pendekatan *Moving Average Smoothing*, fluktuasi jangka pendek berhasil diredam untuk melihat arah tren jangka menengah secara objektif.
- **Tren Pertumbuhan Positif Terkuat**: Kopi (CAGR 65,21%; kenaikan rata-rata bulanan sebesar 4,64 juta USD), Lada Hitam (CAGR 60,47%), dan Buah Tahunan (CAGR 50,96%).
- **Tren Kontraksi Terkritis**: Jagung mengalami penurunan drastis dengan CAGR -58,28%, diikuti oleh Rumput Laut (-19,51%) dan Sarang Burung (-13,46%).

### C. Analisis Pola Musiman (Dekomposisi Time Series)
Menggunakan metode dekomposisi waktu (*Additive* dan *Multiplicative*), ditemukan pola musiman yang konsisten pada komoditas tertentu:
- **Kopi**: Menunjukkan pola musiman yang sangat kuat dengan titik puncak konsisten di bulan **Oktober** (Indeks Musiman: 147,7) dan titik terendah (lembah) di bulan **April** (Indeks Musiman: 46,9), selaras dengan pola panen raya domestik.
- **Sayur-sayuran**: Mengalami lonjakan ekspor pada periode **Juni–September** (mencapai indeks tertinggi 189,4 di September) dan lembah di **Januari** (35,9).
- **Buah-buahan Tahunan**: Puncak ekspor tercatat pada bulan **November–Januari** (indeks tertinggi 146,0 di November) dan lembah di **Juni** (35,0).

### D. Karakteristik Pertumbuhan (CAGR) dan Volatilitas Relatif (CV)
Kinerja ekspor dibandingkan menggunakan *Compound Annual Growth Rate* (CAGR) untuk pertumbuhan dan *Coefficient of Variation* (CV) untuk tingkat risiko volatilitas:
- **Komoditas Paling Stabil**: Sarang Burung (CV: 21,74%, Rata-rata: 45,85 juta USD) dan Tanaman Obat & Rempah (CV: 24,13%, Rata-rata: 42,46 juta USD).
- **Komoditas Paling Volatil**: Jagung menunjukkan volatilitas ekstrem dengan CV mencapai **232,46%** akibat fluktuasi pasokan yang tidak menentu, disusul oleh Lada Hitam (CV: 101,53%).

### E. Segmentasi Komoditas (Matriks Strategis & K-Means)
Algoritma K-Means secara optimal membagi komoditas menjadi 2 cluster utama (Silhouette score tertinggi pada k=2), di mana Kopi memisahkan diri dari 12 komoditas lainnya karena skalanya yang sangat dominan (Mean: 138,7 juta USD; CAGR: 65,2%).

Untuk perumusan kebijakan, integrasi CAGR dan CV menghasilkan **Matriks Kuadran Strategis**:
1. **⭐ Kuadran Andalan** (CAGR Tinggi, CV Rendah): *Lada Putih dan Buah Tahunan*. Komoditas dengan pertumbuhan kuat dan stabil.
2. **📈 Kuadran Potensial** (CAGR Tinggi, CV Tinggi): *Kopi, Lada Hitam, Sayuran, Kakao, dan Ikan Segar*. Tumbuh sangat pesat namun berisiko tinggi.
3. **🟢 Kuadran Stabil** (CAGR Rendah, CV Rendah): *Sarang Burung, Tanaman Obat & Rempah, Tembakau, Rumput Laut, dan HHBK*. Risiko rendah namun pertumbuhan stagnan/negatif.
4. **⚠️ Kuadran Risiko Tinggi** (CAGR Rendah, CV Tinggi): *Jagung*. Mengalami penurunan nilai dengan volatilitas sangat tinggi.

---

## 2. STATUS LUARAN

Berikut adalah status ketercapaian luaran yang telah dijanjikan pada proposal:

| Jenis Luaran | Identitas Luaran | Target Luaran | Status Ketercapaian | Bukti Kemajuan |
| :--- | :--- | :--- | :--- | :--- |
| **Wajib** | Artikel Ilmiah di Jurnal Sinta 3 | Terpublikasi | *Drafting* (60%) | Draf artikel dalam penyusunan menggunakan hasil analisis data gabungan periode Jan 2023–Feb 2026. Target submit ke Jurnal Sinta 3 pada Bulan ke-5. |
| **Tambahan** | Laporan Penelitian Komprehensif | Selesai | Proses Finalisasi (90%) | Laporan pelaksanaan dan draf laporan akhir telah disusun berdasarkan hasil komputasi Python. |
| **Tambahan** | Dashboard Interaktif Web | Berfungsi | Selesai (100%) | Dashboard berbasis **Streamlit** selesai dibangun dan diintegrasikan dengan visualisasi interaktif Plotly. File script: `scripts/06_dashboard.py`. |
| **Tambahan** | Policy Brief & Rekomendasi | Dokumen Cetak/PDF | Selesai (100%) | Dokumen *Policy Brief* setebal 4 halaman telah selesai disusun dan disimpan pada file `output/policy_brief.md`. |

---

## 3. KENDALA PELAKSANAAN PENELITIAN

Selama pelaksanaan penelitian, terdapat beberapa kendala yang dihadapi:
1. **Ketersediaan Data Awal**: Pada tahap awal, data sekunder BPS tahun 2023 belum terkonsolidasi dengan baik di tingkat folder kerja lokal, sehingga memerlukan penelusuran tambahan pada portal resmi BPS untuk melengkapi rangkaian waktu (*time series*) 38 bulan penuh.
2. **Keterbatasan Rangkaian Waktu 2026**: Karena durasi observasi dibatasi hingga Februari 2026 sesuai ketersediaan data aktual saat penelitian berjalan, analisis musiman untuk tahun 2026 belum dapat disajikan secara penuh 12 bulan. Namun, hal ini berhasil diatasi dengan teknik pembobotan indeks musiman (*seasonal index rolling*) menggunakan data penuh 2023–2025.
3. **Eksportasi Gambar Interaktif**: Ekspor visualisasi dari library Plotly ke format statis (PNG) sempat terkendala oleh dependensi *engine* Kaleido di lingkungan lokal. Kendala ini diatasi dengan mengoptimalkan penyimpanan luaran interaktif dalam bentuk file HTML mandiri (`.html`) agar tetap dapat dieksplorasi secara dinamis oleh pengguna.

---

## 4. RENCANA TAHAPAN SELANJUTNYA

Berdasarkan capaian saat ini, rencana tahapan penelitian selanjutnya difokuskan pada penyelesaian luaran wajib:
1. **Submit Artikel Ilmiah (Bulan 5 - Juni 2026)**: Menyelesaikan penulisan artikel ilmiah (*drafting* draf akhir), melakukan *proofreading*, dan mendaftarkannya ke jurnal nasional terakreditasi Sinta 3 (contoh: Jurnal Ekonomi Pertanian atau Agribisnis yang relevan).
2. **Penyusunan Laporan Akhir (Bulan 6 - Juli 2026)**: Mengintegrasikan seluruh visualisasi dari folder `output/plots` dan tabel dari `output/tables` ke dalam dokumen laporan akhir penelitian untuk diserahkan ke STIESIA Surabaya.
3. **Diseminasi Policy Brief (Bulan 6 - Juli 2026)**: Mendistribusikan policy brief yang telah disusun kepada asosiasi eksportir komoditas pertanian dan dinas perdagangan daerah terkait guna memberikan rekomendasi praktis berbasis data empiris.

---

## REFERENSI ACUAN (2021-2026)

1. **Afriza, R., & Handayani, S.** (2023). *Analisis Kinerja dan Daya Saing Ekspor Kopi Indonesia di Pasar Global*. Jurnal Agribisnis Indonesia, 11(2), 245-258. https://doi.org/10.29244/jai.2023.11.2.245-258
2. **Baidowi, A., & Wibowo, A.** (2024). *Penerapan K-Means Clustering untuk Segmentasi Komoditas Ekspor Pertanian Unggulan Daerah*. Jurnal Teknologi Informasi dan Sistem Komputer, 7(1), 89-98.
3. **Daryanto, A.** (2022). *Daya Tahan Sektor Pertanian Indonesia terhadap Volatilitas Pasar Internasional Pasca Pandemi*. Jurnal Kebijakan Pembangunan, 17(1), 12-25.
4. **Fathurrahman, A., & Nugroho, S. B.** (2025). *Analisis Time Series dengan Dekomposisi Aditif dan Multiplikatif untuk Proyeksi Ekspor Komoditas Hortikultura*. Jurnal Ekonomi Kuantitatif, 13(2), 110-123.
5. **Indrawan, I. G. A., & Utama, M. S.** (2023). *Pengaruh Volatilitas Nilai Tukar dan CAGR Sektor Pertanian Terhadap Volume Ekspor Indonesia*. EJurnal Ekonomi Pembangunan Universitas Udayana, 12(4), 512-525.
6. **Kementerian Pertanian Republik Indonesia.** (2024). *Rencana Strategis Pembangunan Pertanian Nasional 2025-2029*. Jakarta: Kementan RI.
7. **Prasetyo, A., & Nur, M.** (2021). *Aplikasi Moving Average Smoothing dalam Peramalan Ekspor Produk Perkebunan Indonesia*. Jurnal Statistika Industri, 4(2), 77-88.
8. **Rahman, F., & Sitorus, S.** (2024). *Analisis Fluktuasi Musiman Ekspor Tanaman Obat dan Rempah Indonesia Menggunakan Seasonal Decompose*. Jurnal Ilmiah BPS, 15(3), 201-215.
9. **Sari, N. P., & Setiawan, B.** (2022). *Analisis Risiko Ekspor Komoditas Hortikultura Berdasarkan Koefisien Variasi (CV) dan Pola Distribusi Harga*. Jurnal Hortikultura Indonesia, 13(3), 189-199. https://doi.org/10.29244/jhi.2022.13.3.189-199
10. **Widyantara, I. W.** (2025). *Strategi Peningkatan Daya Saing Ekspor Buah Tropis Tahunan Indonesia di Pasar Asia*. Jurnal Agribisnis dan Agrowisata, 14(1), 45-56.
