"""
Script 06: Dashboard Interaktif (Streamlit) — Full Interaktif
Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose

from config import (
    BASE_DIR, TABLE_DIR, PLOT_DIR,
    KOMODITAS_UNGGULAN, KOMODITAS_SINGKAT,
    BULAN_LABEL, WARNA_KUADRAN,
)

st.set_page_config(page_title="Dashboard Ekspor Pertanian", layout="wide")

# =====================================================================
# LOAD DATA
# =====================================================================
@st.cache_data
def load_data():
    df = pd.read_csv(TABLE_DIR / "dataset_lengkap.csv")
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    return df


@st.cache_data
def load_csv(name, index_col=None):
    try:
        return pd.read_csv(TABLE_DIR / name, index_col=index_col)
    except Exception:
        return None


df = load_data()
stats = load_csv("statistik_deskriptif.csv", index_col=0)
df_cv = load_csv("volatilitas_cv.csv")
df_cagr = load_csv("cagr.csv")
df_cluster = load_csv("clustering_hasil.csv")
df_amp = load_csv("amplitudo_musiman.csv")
df_matriks = load_csv("matriks_strategis.csv")

kom_inti = [k for k in df["Komoditas"].unique() if k not in ["Lainnya", "Jumlah"]]

# =====================================================================
# SIDEBAR
# =====================================================================
st.sidebar.title("🌾 Ekspor Pertanian")
st.sidebar.markdown("Analisis Tren & Pola Musiman")
st.sidebar.markdown("**Data:** Jan 2023 – Feb 2026")
st.sidebar.markdown("**Institusi:** STIESIA Surabaya")
st.sidebar.markdown("---")

pilih_kom = st.sidebar.multiselect(
    "Pilih Komoditas",
    options=kom_inti,
    default=kom_inti[:5],
)
if not pilih_kom:
    st.warning("Pilih minimal satu komoditas di sidebar.")
    st.stop()

# =====================================================================
# TABS
# =====================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tren Ekspor", "📊 Perbandingan", "🔬 Analisis",
    "📋 Matriks Strategis", "📁 Tabel Data",
])

# ===== TAB 1: TREN EKSPOR (Plotly interaktif) =====
with tab1:
    st.header("Tren Nilai Ekspor Bulanan")

    df_filt = df[df["Komoditas"].isin(pilih_kom)]

    options = ["Aktual"]
    if df_cagr is not None:
        options.append("MA-3")
        options.append("MA-6")
    metode_tren = st.radio("Tampilkan:", options, horizontal=True)

    if metode_tren == "Aktual":
        df_plot = df_filt
    else:
        window = 3 if metode_tren == "MA-3" else 6
        rows = []
        for kom in pilih_kom:
            sub = df_filt[df_filt["Komoditas"] == kom].copy()
            sub = sub.sort_values("Tanggal")
            sub["Nilai_Ekspor_Juta_USD"] = (
                sub["Nilai_Ekspor_Juta_USD"].rolling(window, center=True).mean()
            )
            rows.append(sub)
        df_plot = pd.concat(rows)

    fig = px.line(
        df_plot.dropna(subset="Nilai_Ekspor_Juta_USD"),
        x="Tanggal", y="Nilai_Ekspor_Juta_USD",
        color="Komoditas",
        title=f"Nilai Ekspor Bulanan — {metode_tren} (Juta US$)",
        markers=True,
    )
    fig.update_layout(legend_title="Komoditas", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    if stats is not None:
        st.subheader("Ringkasan Statistik")
        stats_filt = stats[stats.index.isin(pilih_kom)][["mean", "std", "min", "max"]]
        stats_filt.columns = ["Rata-rata", "Std", "Min", "Max"]
        st.dataframe(stats_filt.round(2), use_container_width=True)

# ===== TAB 2: PERBANDINGAN (100% Plotly interaktif) =====
with tab2:
    st.header("Perbandingan Kinerja Antar Komoditas")

    metrik = st.selectbox(
        "Pilih Metrik",
        ["CV (%) — Volatilitas", "CAGR (%) — Pertumbuhan", "Amplitudo Musiman"],
    )

    col_a, col_b = st.columns(2)

    with col_a:
        if metrik == "CV (%) — Volatilitas" and df_cv is not None:
            df_plot = df_cv[df_cv["Komoditas"].isin(pilih_kom)].sort_values("CV_%")
            fig = px.bar(df_plot, x="CV_%", y="Singkat", orientation="h",
                         title="Coefficient of Variation (%) — Stabilitas",
                         color="CV_%", color_continuous_scale="RdYlGn_r", text_auto=".1f")
            fig.update_layout(yaxis=dict(title=None))
            st.plotly_chart(fig, use_container_width=True)

        elif metrik == "CAGR (%) — Pertumbuhan" and df_cagr is not None:
            df_plot = df_cagr[df_cagr["Komoditas"].isin(pilih_kom)].sort_values("CAGR_%")
            fig = px.bar(df_plot, x="CAGR_%", y="Komoditas", orientation="h",
                         title="CAGR 2023–2025 (%)",
                         color="CAGR_%", color_continuous_scale="RdYlGn", text_auto=".1f")
            fig.add_vline(x=0, line_dash="dash", line_color="gray")
            fig.update_layout(yaxis=dict(title=None))
            st.plotly_chart(fig, use_container_width=True)

        elif metrik == "Amplitudo Musiman" and df_amp is not None:
            df_plot = df_amp[df_amp["Komoditas"].isin(pilih_kom)].sort_values("Amplitudo")
            fig = px.bar(df_plot, x="Amplitudo", y="Komoditas", orientation="h",
                         title="Amplitudo Musiman (Juta US$)",
                         color="Amplitudo", color_continuous_scale="Blues", text_auto=".1f")
            fig.update_layout(yaxis=dict(title=None))
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Pola Musiman (Heatmap Interaktif)")
        heat_data = []
        heat_labels = []
        for kom in pilih_kom:
            sub = df[df["Komoditas"] == kom]
            means = sub.groupby("Bulan")["Nilai_Ekspor_Juta_USD"].mean()
            heat_data.append(means.values)
            heat_labels.append(KOMODITAS_SINGKAT.get(kom, kom)[:12])

        if heat_data:
            fig = go.Figure(data=go.Heatmap(
                z=heat_data,
                x=BULAN_LABEL,
                y=heat_labels,
                colorscale="YlOrRd",
                hovertemplate="<b>%{y}</b><br>%{x}: %{z:.2f} Juta US$<extra></extra>",
            ))
            fig.update_layout(
                title="Rata-rata Ekspor per Bulan",
                xaxis=dict(title=None),
                yaxis=dict(title=None),
                height=max(200, len(pilih_kom) * 40 + 80),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ===== SEASONAL SUB SERIES =====
    st.divider()
    st.subheader("🌊 Pola Musiman — Seasonal Subseries")

    kom_ss = st.selectbox("Pilih komoditas:", pilih_kom, key="ss_komoditas")

    df_ss = df[df["Komoditas"] == kom_ss].copy()
    df_ss["Tahun"] = df_ss["Tanggal"].dt.year
    df_ss["Bulan_Angka"] = df_ss["Tanggal"].dt.month

    fig_ss = go.Figure()
    for tahun in sorted(df_ss["Tahun"].unique()):
        sub = df_ss[df_ss["Tahun"] == tahun]
        fig_ss.add_trace(go.Scatter(
            x=sub["Bulan_Angka"], y=sub["Nilai_Ekspor_Juta_USD"],
            mode="lines+markers", name=str(tahun),
            line=dict(width=2),
        ))

    monthly_mean = df_ss.groupby("Bulan_Angka")["Nilai_Ekspor_Juta_USD"].mean()
    fig_ss.add_trace(go.Scatter(
        x=monthly_mean.index, y=monthly_mean.values,
        mode="lines+markers", name="Rata-rata",
        line=dict(color="black", width=3, dash="dash"),
        marker=dict(size=8, symbol="diamond"),
    ))

    fig_ss.update_layout(
        xaxis=dict(tickmode="array", tickvals=list(range(1, 13)), ticktext=BULAN_LABEL),
        title=f"Pola Musiman per Bulan — {kom_ss}",
        yaxis=dict(title="Nilai Ekspor (Juta US$)"),
        height=400,
    )
    st.plotly_chart(fig_ss, use_container_width=True)

    # ===== TABEL RANGKUMAN SEMUA METRIK =====
    st.divider()
    st.subheader("📊 Rangkuman Lengkap Semua Komoditas")

    if df_matriks is not None and df_amp is not None:
        rangkum = df_matriks[["Komoditas", "Singkat", "Mean_Juta_USD", "CV_%", "CAGR_%", "Kuadran"]].copy()
        amp_sub = df_amp[["Komoditas", "Puncak", "Lembah", "Amplitudo"]].copy().rename(
            columns={
                "Puncak": "Bulan Puncak",
                "Lembah": "Bulan Lembah",
                "Amplitudo": "Amplitudo (Juta US$)",
            },
        )
        rangkum = rangkum.merge(amp_sub, on="Komoditas", how="left")
        rangkum = rangkum.drop(columns=["Komoditas"])
        rangkum = rangkum.rename(columns={
            "Singkat": "Komoditas", "Mean_Juta_USD": "Mean (Juta US$)",
            "CV_%": "CV (%)", "CAGR_%": "CAGR (%)",
        })

        rangkum["Rank CAGR"] = rangkum["CAGR (%)"].rank(ascending=False).astype(int)
        rangkum["Rank Stabilitas"] = rangkum["CV (%)"].rank(ascending=True).astype(int)
        rangkum = rangkum.sort_values("Kuadran")

        st.dataframe(rangkum, use_container_width=True, hide_index=True)

        csv_export = rangkum.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download Rangkuman CSV",
            data=csv_export,
            file_name="rangkuman_kinerja_komoditas.csv",
            mime="text/csv",
        )
    else:
        st.info("Jalankan script 05b_matriks_strategis.py untuk melihat rangkuman.")

    # ===== TABEL DETAIL CAGR 2023–2025 =====
    with st.expander("📈 Tabel Detail CAGR 2023–2025", expanded=False):
        if df_cagr is not None:
            st.dataframe(
                df_cagr.style.format({"Total_2023": "{:,.1f}", "Total_2025": "{:,.1f}", "CAGR_%": "{:.2f}"}),
                use_container_width=True, hide_index=True,
            )
            st.caption("Sumber: diolah dari data BPS (2023–2025)")
        else:
            st.info("Data CAGR belum tersedia.")

    # ===== TABEL RANKING CV =====
    with st.expander("📊 Ranking Volatilitas (CV) dan Statistik Deskriptif", expanded=False):
        if df_cv is not None:
            st.dataframe(
                df_cv[["Komoditas", "Singkat", "Mean", "Std", "CV_%", "Min", "Max"]]
                .sort_values("CV_%")
                .round(2),
                use_container_width=True, hide_index=True,
            )
            st.caption("CV = Coefficient of Variation. Semakin rendah CV, semakin stabil ekspor komoditas.")
        else:
            st.info("Data CV belum tersedia.")

# ===== TAB 3: ANALISIS LANJUTAN (100% Plotly interaktif) =====
with tab3:
    st.header("Analisis Lanjutan")

    kom_analisis = st.selectbox("Pilih satu komoditas:", pilih_kom)

    if kom_analisis:
        sub = df[df["Komoditas"] == kom_analisis].set_index("Tanggal")
        sub = sub["Nilai_Ekspor_Juta_USD"].sort_index()
        sub_filled = sub.fillna(0)

        if len(sub_filled) >= 24:
            model_dekomp = st.radio("Model Dekomposisi:", ["additive", "multiplicative"], horizontal=True)

            try:
                sub_input = sub_filled.replace(0, 0.001) if model_dekomp == "multiplicative" else sub_filled
                result = seasonal_decompose(sub_input, model=model_dekomp, period=12)

                fig = make_subplots(
                    rows=4, cols=1, shared_xaxes=True,
                    vertical_spacing=0.08,
                    subplot_titles=("Observed", "Tren", "Musiman", "Residual"),
                )

                for row, (data, name) in enumerate([
                    (result.observed, "Observed"),
                    (result.trend, "Tren"),
                    (result.seasonal, "Musiman"),
                    (result.resid, "Residual"),
                ], 1):
                    fig.add_trace(
                        go.Scatter(
                            x=data.index, y=data.values,
                            mode="lines", name=name,
                            line=dict(width=1.5 if name != "Residual" else 0.8,
                                      color="gray" if name == "Residual" else None),
                        ),
                        row=row, col=1,
                    )

                fig.update_layout(
                    title=f"Dekomposisi {model_dekomp.title()}: {kom_analisis}",
                    height=700,
                    showlegend=False,
                    hovermode="x unified",
                )
                st.plotly_chart(fig, use_container_width=True)

                # Indeks musiman
                seasonal_idx = result.seasonal.groupby(result.seasonal.index.month).mean()

                fig_idx = go.Figure()
                fig_idx.add_trace(go.Bar(
                    x=BULAN_LABEL,
                    y=seasonal_idx.values,
                    marker_color=["#e74c3c" if v < 0 else "#2ecc71" for v in seasonal_idx.values],
                ))
                fig_idx.add_hline(y=0, line_dash="dash", line_color="gray")
                fig_idx.update_layout(
                    title="Indeks Musiman",
                    xaxis=dict(title=None),
                    yaxis=dict(title="Indeks"),
                    height=300,
                )
                st.plotly_chart(fig_idx, use_container_width=True)

            except Exception as e:
                st.error(f"Dekomposisi gagal: {e}")
        else:
            st.warning("Minimal 24 bulan data untuk dekomposisi.")

    if df_cluster is not None:
        st.subheader("Segmentasi Komoditas (K-Means)")
        cols_show = [c for c in ["Singkat", "Cluster", "Mean", "CV", "CAGR", "Amplitudo"] if c in df_cluster.columns]
        st.dataframe(df_cluster[cols_show].round(2), use_container_width=True)

    # ===== VISUALISASI CLUSTERING =====
    if df_cluster is not None:
        st.subheader("📌 Scatter Plot Segmentasi K-Means")

        df_cluster_plot = df_cluster.copy()
        df_cluster_plot["CAGR_%"] = df_cluster_plot["CAGR"] * 100

        fig_cluster = px.scatter(
            df_cluster_plot,
            x="Mean", y="CAGR_%",
            color="Cluster",
            size="Scale",
            text="Singkat",
            hover_data={"Mean": ":.2f", "CAGR_%": ":.2f", "CV": ":.2f", "Amplitudo": ":.2f"},
            labels={
                "Mean": "Rata-rata Ekspor (Juta US$)",
                "CAGR_%": "CAGR Tahunan (%)",
                "Cluster": "Cluster",
            },
            title="Segmentasi Komoditas — Mean vs CAGR",
        )
        fig_cluster.update_traces(textposition="top center")
        fig_cluster.update_layout(height=500)
        st.plotly_chart(fig_cluster, use_container_width=True)

        # Elbow method & Silhouette
        st.subheader("📐 Evaluasi Jumlah Cluster")
        col_elbow, col_sil = st.columns([2, 1])
        with col_elbow:
            try:
                st.image(str(PLOT_DIR / "elbow_method.png"),
                         caption="Metode Elbow untuk menentukan k optimal", use_container_width=True)
            except Exception:
                st.info("Gambar elbow_method.png belum tersedia. Jalankan scripts/05_clustering.py.")
        with col_sil:
            st.metric("Silhouette Score (k=2)", "0.48",
                      help="Rentang -1 hingga 1. Semakin mendekati 1, semakin baik pemisahan cluster.")
            st.markdown("""
            **Interpretasi:**
            - **k=2** konfigurasi optimal (silhouette score tertinggi)
            - Kopi (Cluster 1) terpisah dari 12 komoditas lain (Cluster 0)
            - Matriks Strategis 4 kuadran sebagai pendekatan komplementer
            """)

# ===== TAB 4: MATRIKS STRATEGIS (baru — 100% Plotly interaktif) =====
with tab4:
    st.header("📋 Matriks Strategis: Pertumbuhan vs Risiko")

    if df_matriks is not None:
        median_cv = df_matriks["CV_%"].median()
        median_cagr = df_matriks["CAGR_%"].median()

        # ---- Ringkasan Kuadran ----
        st.subheader("Ringkasan Kuadran")
        ringkasan = df_matriks.groupby("Kuadran").agg(
            Jumlah=("Singkat", "count"),
            Anggota=("Singkat", lambda x: ", ".join(x)),
            Rata_Ekspor=("Mean_Juta_USD", "mean"),
            Rata_CAGR=("CAGR_%", "mean"),
            Rata_CV=("CV_%", "mean"),
        ).round(2).reset_index()
        ringkasan.columns = ["Kuadran", "Jumlah", "Anggota", "Rata Ekspor (Juta US$)", "Rata CAGR %", "Rata CV %"]

        def warnai_kuadran(val):
            warna = {
                "Andalan": "background-color: #2ECC71; color: white",
                "Potensial": "background-color: #F39C12; color: white",
                "Stabil": "background-color: #3498DB; color: white",
                "Risiko Tinggi": "background-color: #E74C3C; color: white",
            }
            return warna.get(val, "")

        st.dataframe(
            ringkasan.style.applymap(warnai_kuadran, subset=["Kuadran"]),
            use_container_width=True, hide_index=True,
        )

        # ---- Bubble Chart Utama: CAGR vs CV ----
        st.subheader("Bubble Chart: CAGR vs CV (ukuran bubble = skala ekspor)")

        fig = px.scatter(
            df_matriks,
            x="CV_%", y="CAGR_%",
            size="Mean_Juta_USD",
            color="Kuadran",
            color_discrete_map=WARNA_KUADRAN,
            text="Singkat",
            hover_data={
                "Singkat": False, "Komoditas": True,
                "Mean_Juta_USD": ":.2f", "CV_%": ":.2f", "CAGR_%": ":.2f",
            },
            labels={
                "CV_%": "CV (%) — Volatilitas (makin kanan makin fluktuatif)",
                "CAGR_%": "CAGR (%) — Pertumbuhan Tahunan",
            },
            title="Pemetaan Strategis Komoditas Ekspor",
        )
        fig.add_hline(y=median_cagr, line_dash="dash", line_color="gray",
                      annotation_text=f"Median CAGR {median_cagr:.1f}%",
                      annotation_position="bottom left")
        fig.add_vline(x=median_cv, line_dash="dash", line_color="gray",
                      annotation_text=f"Median CV {median_cv:.1f}%",
                      annotation_position="top right")
        fig.update_traces(textposition="top center",
                          marker=dict(line=dict(width=1, color="black")))
        fig.update_layout(width=900, height=600)
        st.plotly_chart(fig, use_container_width=True)

        # ---- Detail Tabel Matriks ----
        with st.expander("📊 Lihat Detail Semua Komoditas", expanded=False):
            st.dataframe(
                df_matriks[["Singkat", "Kuadran", "Mean_Juta_USD", "CV_%", "CAGR_%", "Amplitudo_Musiman"]]
                .sort_values(["Kuadran", "Mean_Juta_USD"], ascending=[True, False])
                .round(2),
                use_container_width=True,
                hide_index=True,
            )

        # ---- Interpretasi Cepat ----
        st.subheader("📝 Interpretasi & Rekomendasi")
        for kuadran, deskripsi in [
            ("Andalan", "Pertumbuhan tinggi, risiko rendah. **Prioritas utama** — optimalkan ekspor, jaga kualitas, perluas pasar."),
            ("Potensial", "Pertumbuhan tinggi tapi fluktuatif. **Dikelola aktif** — butuh stabilisasi harga/volume, lindung nilai."),
            ("Stabil", "Volume stabil tapi pertumbuhan rendah. **Dipertahankan** — efisiensi biaya, cari diferensiasi produk."),
            ("Risiko Tinggi", "Pertumbuhan rendah/negatif dengan volatilitas tinggi. **Evaluasi** — butuh intervensi kebijakan atau restrukturisasi."),
        ]:
            anggota = df_matriks[df_matriks["Kuadran"] == kuadran]["Singkat"].tolist()
            if anggota:
                st.markdown(f"**{kuadran}:** {', '.join(anggota)}")
                st.markdown(f"> {deskripsi}")

    else:
        st.warning("Jalankan `scripts/05b_matriks_strategis.py` dulu untuk melihat matriks.")
        st.code("python scripts/05b_matriks_strategis.py", language="bash")

# ===== TAB 5: TABEL DATA =====
with tab5:
    st.header("Data Mentah")

    df_tabel = df[df["Komoditas"].isin(pilih_kom)]
    df_tabel = df_tabel[["Tanggal", "Komoditas", "Nilai_Ekspor_Juta_USD"]]
    df_tabel.columns = ["Tanggal", "Komoditas", "Nilai Ekspor (Juta US$)"]

    st.dataframe(
        df_tabel.sort_values(["Komoditas", "Tanggal"]),
        use_container_width=True, hide_index=True,
    )

    csv = df_tabel.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="ekspor_pertanian.csv",
        mime="text/csv",
    )
