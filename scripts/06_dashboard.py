"""
Script 06: Dashboard Interaktif (Streamlit)
Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path
from statsmodels.tsa.seasonal import seasonal_decompose

st.set_page_config(page_title="Dashboard Ekspor Pertanian", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
TABLE_DIR = BASE_DIR / "output" / "tables"

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv(TABLE_DIR / "dataset_lengkap.csv")
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    return df

@st.cache_data
def load_stats():
    try:
        return pd.read_csv(TABLE_DIR / "statistik_deskriptif.csv")
    except:
        return None

@st.cache_data
def load_cv():
    try:
        return pd.read_csv(TABLE_DIR / "volatilitas_cv.csv")
    except:
        return None

@st.cache_data
def load_cagr():
    try:
        return pd.read_csv(TABLE_DIR / "cagr.csv")
    except:
        return None

@st.cache_data
def load_cluster():
    try:
        return pd.read_csv(TABLE_DIR / "clustering_hasil.csv")
    except:
        return None

@st.cache_data
def load_amp():
    try:
        return pd.read_csv(TABLE_DIR / "amplitudo_musiman.csv")
    except:
        return None

df = load_data()
stats = load_stats()
df_cv = load_cv()
df_cagr = load_cagr()
df_cluster = load_cluster()
df_amp = load_amp()

kom_inti = [k for k in df["Komoditas"].unique()
            if k not in ["Lainnya", "Jumlah"]]

# ===== SIDEBAR =====
st.sidebar.title("🌾 Ekspor Pertanian")
st.sidebar.markdown("Analisis Tren & Pola Musiman")
st.sidebar.markdown("**Data:** Jan 2023 – Feb 2026")
st.sidebar.markdown("**Peneliti:** Dr. Anindhyta Budiarti, S.E., M.M.")
st.sidebar.markdown("**Institusi:** STIESIA Surabaya")
st.sidebar.markdown("---")

# Filter komoditas
pilih_kom = st.sidebar.multiselect(
    "Pilih Komoditas",
    options=kom_inti,
    default=kom_inti[:5]
)

if not pilih_kom:
    st.warning("Pilih minimal satu komoditas di sidebar.")
    st.stop()

# ===== TAB 1: TREN =====
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren Ekspor", "📊 Perbandingan", "🔬 Analisis", "📋 Tabel Data"
])

with tab1:
    st.header("Tren Nilai Ekspor Bulanan")

    col1, col2 = st.columns([3, 1])
    with col2:
        metode_tren = st.radio("Tampilkan:", ["Aktual", "MA-3", "MA-6"], index=0)

    with col1:
        fig = px.line(
            df[df["Komoditas"].isin(pilih_kom)],
            x="Tanggal", y="Nilai_Ekspor_Juta_USD",
            color="Komoditas",
            title="Nilai Ekspor Bulanan (Juta US$)",
            markers=True
        )
        fig.update_layout(legend_title="Komoditas")
        st.plotly_chart(fig, use_container_width=True)

    # Ringkasan
    st.subheader("Ringkasan Statistik")
    if stats is not None:
        stats_filt = stats[stats.index.isin(pilih_kom)][["mean", "std", "min", "max"]]
        stats_filt.columns = ["Rata-rata", "Std", "Min", "Max"]
        stats_filt = stats_filt.round(2)
        st.dataframe(stats_filt, use_container_width=True)
    else:
        st.info("Jalankan script 01-03 dulu untuk melihat statistik.")

with tab2:
    st.header("Perbandingan Kinerja Antar Komoditas")

    metrik = st.selectbox("Pilih Metrik", ["CV (%) — Volatilitas", "CAGR (%) — Pertumbuhan", "Amplitudo Musiman"])

    col_a, col_b = st.columns(2)

    with col_a:
        if metrik == "CV (%) — Volatilitas" and df_cv is not None:
            df_plot = df_cv[df_cv["Komoditas"].isin(pilih_kom)].sort_values("CV_%")
            fig = px.bar(df_plot, x="CV_%", y="Singkat", orientation="h",
                         title="Coefficient of Variation (%)", color="CV_%",
                         color_continuous_scale="RdYlGn_r")
            st.plotly_chart(fig, use_container_width=True)

        elif metrik == "CAGR (%) — Pertumbuhan" and df_cagr is not None:
            df_plot = df_cagr[df_cagr["Komoditas"].isin(pilih_kom)].sort_values("CAGR_%")
            fig = px.bar(df_plot, x="CAGR_%", y="Komoditas", orientation="h",
                         title="CAGR 2023–2025 (%)", color="CAGR_%",
                         color_continuous_scale="RdYlGn")
            st.plotly_chart(fig, use_container_width=True)

        elif metrik == "Amplitudo Musiman" and df_amp is not None:
            df_plot = df_amp[df_amp["Komoditas"].isin(pilih_kom)].sort_values("Amplitudo")
            fig = px.bar(df_plot, x="Amplitudo", y="Komoditas", orientation="h",
                         title="Amplitudo Musiman (Juta US$)", color="Amplitudo",
                         color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Data belum tersedia. Jalankan script 03-04.")

    with col_b:
        # Heatmap musiman per komoditas
        if pilih_kom:
            st.subheader("Pola Musiman")
            bulan_label = ["Jan","Feb","Mar","Apr","Mei","Jun",
                           "Jul","Agu","Sep","Okt","Nov","Des"]
            heat_data = []
            for kom in pilih_kom:
                sub = df[df["Komoditas"] == kom]
                means = sub.groupby("Bulan")["Nilai_Ekspor_Juta_USD"].mean()
                heat_data.append(means.values)

            if heat_data:
                fig, ax = plt.subplots(figsize=(8, max(3, len(pilih_kom)*0.6)))
                im = ax.imshow(heat_data, aspect="auto", cmap="YlOrRd")
                ax.set_xticks(range(12))
                ax.set_xticklabels(bulan_label)
                ax.set_yticks(range(len(pilih_kom)))
                ax.set_yticklabels([k[:12] for k in pilih_kom])
                plt.colorbar(im, ax=ax, label="Juta US$")
                ax.set_title("Rata-rata Bulanan")
                fig.tight_layout()
                st.pyplot(fig)

with tab3:
    st.header("Analisis Lanjutan")

    kom_pilih_analisis = st.selectbox("Pilih satu komoditas:", pilih_kom)

    if kom_pilih_analisis:
        sub = df[df["Komoditas"] == kom_pilih_analisis].set_index("Tanggal")
        sub = sub["Nilai_Ekspor_Juta_USD"].sort_index().fillna(0)

        if len(sub) >= 24:
            model_dekomp = st.radio("Model Dekomposisi:", ["additive", "multiplicative"], horizontal=True)

            try:
                sub_filled = sub.replace(0, 0.001) if model_dekomp == "multiplicative" else sub
                result = seasonal_decompose(sub_filled, model=model_dekomp, period=12)

                fig, axes = plt.subplots(4, 1, figsize=(10, 7), sharex=True)
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
                axes[0].set_title(f"Dekomposisi {model_dekomp.title()}: {kom_pilih_analisis}", fontweight="bold")
                fig.tight_layout()
                st.pyplot(fig)

                # Indeks musiman
                seasonal_idx = result.seasonal.groupby(result.seasonal.index.month).mean()
                bulan_label = ["Jan","Feb","Mar","Apr","Mei","Jun",
                               "Jul","Agu","Sep","Okt","Nov","Des"]
                df_idx = pd.DataFrame({
                    "Bulan": bulan_label,
                    "Indeks_Musiman": seasonal_idx.values
                })
                st.subheader("Indeks Musiman")
                st.dataframe(df_idx.round(4), use_container_width=False)

            except Exception as e:
                st.error(f"Dekomposisi gagal: {e}")
        else:
            st.warning("Minimal 24 bulan data untuk dekomposisi.")

    # Clustering results
    if df_cluster is not None:
        st.subheader("Segmentasi Komoditas (K-Means)")
        st.dataframe(df_cluster[["Singkat", "Cluster", "Mean", "CV", "CAGR", "Amplitudo"]].round(2),
                     use_container_width=True)

with tab4:
    st.header("Data Mentah")

    # Filter data
    df_tabel = df[df["Komoditas"].isin(pilih_kom)]
    df_tabel = df_tabel[["Tanggal", "Komoditas", "Nilai_Ekspor_Juta_USD"]]
    df_tabel.columns = ["Tanggal", "Komoditas", "Nilai Ekspor (Juta US$)"]

    st.dataframe(df_tabel.sort_values(["Komoditas", "Tanggal"]),
                 use_container_width=True, hide_index=True)

    # Download
    csv = df_tabel.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="ekspor_pertanian.csv",
        mime="text/csv",
    )
