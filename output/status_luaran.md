## G. STATUS LUARAN

Bagian ini menjelaskan jenis, identitas, dan status ketercapaian setiap luaran wajib dan luaran tambahan yang dijanjikan pada proposal penelitian. Seluruh status luaran didukung oleh bukti kemajuan yang telah dihasilkan selama pelaksanaan penelitian.

### 1. Luaran Wajib

| Jenis Luaran | Identitas Luaran | Status Ketercapaian | Bukti Kemajuan |
|---|---|---|---|
| Publikasi ilmiah | Artikel ilmiah pada jurnal terakreditasi Sinta 3 dengan topik *Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia* | **Sedang disusun** | Naskah artikel disiapkan berdasarkan hasil analisis tren, dekomposisi musiman, CAGR, CV, dan segmentasi komoditas. Struktur data, tabel hasil, dan visualisasi pendukung telah tersedia dalam folder `output/` dan dashboard interaktif. |
| Laporan penelitian | Laporan penelitian komprehensif sesuai format laporan kemajuan/akhir penelitian | **Sedang disusun** | Draft bagian hasil pelaksanaan penelitian telah dibuat dalam file `output/hasil_pelaksanaan_penelitian.md`, memuat ringkasan data, analisis tren, pola musiman, volatilitas, matriks strategis, serta rencana tahap selanjutnya. |

### 2. Luaran Tambahan

| Jenis Luaran | Identitas Luaran | Status Ketercapaian | Bukti Kemajuan |
|---|---|---|---|
| Dashboard interaktif | Dashboard web berbasis Streamlit untuk visualisasi tren, pola musiman, volatilitas, clustering, dan matriks strategis komoditas | **Selesai** | Script dashboard tersedia pada `scripts/06_dashboard.py` dan telah diuji berjalan lokal dengan perintah `streamlit run scripts/06_dashboard.py`. Dashboard menampilkan grafik interaktif, tabel rangkuman, dan matriks strategis. |
| Policy brief | Dokumen policy brief berisi rekomendasi strategis pengelolaan risiko ekspor komoditas pertanian | **Selesai** | Dokumen tersedia pada file `output/policy_brief.md` dan memuat ringkasan temuan utama, segmentasi kuadran strategis, serta rekomendasi kebijakan bagi pemangku kepentingan dan pelaku ekspor. |
| Matriks strategis | Analisis matriks CAGR × CV × Mean untuk klasifikasi komoditas ke dalam kuadran Andalan, Potensial, Stabil, dan Risiko Tinggi | **Selesai** | Script `scripts/05b_matriks_strategis.py` menghasilkan tabel `output/tables/matriks_strategis.csv` dan visualisasi interaktif `output/plots/matriks_strategis.html`. Hasil analisis juga diintegrasikan ke dashboard. |

### 3. Bukti Kemajuan Ketercapaian Luaran

Bukti kemajuan ketercapaian luaran penelitian telah tersedia dalam bentuk dokumen, script, tabel, dan visualisasi sebagai berikut:

1. **Dataset hasil pengolahan**: `output/tables/dataset_lengkap.csv`, `output/tables/dataset_komoditas_inti.csv`, dan `output/tables/dataset_agregat.csv`.
2. **Tabel hasil analisis**: `output/tables/statistik_deskriptif.csv`, `output/tables/cagr.csv`, `output/tables/volatilitas_cv.csv`, `output/tables/amplitudo_musiman.csv`, `output/tables/clustering_hasil.csv`, dan `output/tables/matriks_strategis.csv`.
3. **Visualisasi hasil analisis**: seluruh file gambar pada folder `output/plots/`.
4. **Dashboard interaktif**: script `scripts/06_dashboard.py`.
5. **Policy brief**: file `output/policy_brief.md`.
6. **Draft laporan pelaksanaan penelitian**: file `output/hasil_pelaksanaan_penelitian.md`.

### 4. Ringkasan Status Luaran

Secara keseluruhan, luaran tambahan berupa **dashboard interaktif**, **policy brief**, dan **matriks strategis** telah selesai dicapai. Sementara itu, luaran wajib berupa **artikel ilmiah** dan **laporan penelitian komprehensif** masih berada pada tahap penyusunan akhir dan siap untuk disempurnakan berdasarkan hasil pelaksanaan penelitian yang telah diperoleh.
