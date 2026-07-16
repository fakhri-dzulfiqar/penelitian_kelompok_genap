"""
Script 05: Segmentasi Komoditas dengan K-Means Clustering

Proposal: Analisis Tren dan Pola Musiman Ekspor Komoditas Pertanian Unggulan Indonesia
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

from config import (
    PLOT_DIR, TABLE_DIR,
    KOMODITAS_SINGKAT, KOMODITAS_UNGGULAN,
    init_rcparams,
)

init_rcparams()
PLOT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLE_DIR / "dataset_komoditas_inti.csv")
df["Tanggal"] = pd.to_datetime(df["Tanggal"])

kom_inti = KOMODITAS_UNGGULAN

# =====================================================================
# 5.1 FEATURE ENGINEERING
# =====================================================================
features = []
for kom in kom_inti:
    sub = df[df["Komoditas"] == kom]["Nilai_Ekspor_Juta_USD"].dropna()

    mean_val = sub.mean()
    cv = (sub.std() / mean_val * 100) if mean_val > 0 else 0

    # CAGR 2023→2025
    total_tahunan = df[df["Komoditas"] == kom].groupby("Tahun")["Nilai_Ekspor_Juta_USD"].sum()
    if 2023 in total_tahunan.index and 2025 in total_tahunan.index:
        awal, akhir = total_tahunan[2023], total_tahunan[2025]
        cagr = ((akhir / awal) ** (1 / 2) - 1) if awal > 0 and akhir > 0 else 0
    else:
        cagr = 0

    # Amplitudo musiman
    monthly_avg = df[df["Komoditas"] == kom].groupby("Bulan")["Nilai_Ekspor_Juta_USD"].mean()
    amplitude = monthly_avg.max() - monthly_avg.min()

    # Tren: slope regresi linear
    sub_sorted = sub.sort_index()
    x = np.arange(len(sub_sorted))
    y = sub_sorted.values
    slope = np.polyfit(x, y, 1)[0] if len(x) > 1 else 0

    features.append({
        "Komoditas": kom,
        "Singkat": KOMODITAS_SINGKAT[kom],
        "Mean": mean_val,
        "CV": cv,
        "CAGR": cagr,
        "Amplitudo": amplitude,
        "Slope": slope,
        "Scale": mean_val,
    })

df_feat = pd.DataFrame(features)
print("=== FITUR UNTUK CLUSTERING ===")
print(df_feat.round(3).to_string(index=False))

# =====================================================================
# 5.2 ELBOW METHOD — cari k optimal
# =====================================================================
X = df_feat[["Mean", "CV", "CAGR", "Amplitudo", "Slope"]].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

inertias = []
silhouettes = []
K_range = range(2, min(7, len(df_feat)))

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil = silhouette_score(X_scaled, labels)
    silhouettes.append(sil)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(list(K_range), inertias, marker="o", color="steelblue")
ax1.set_xlabel("Jumlah Cluster (k)")
ax1.set_ylabel("Inertia")
ax1.set_title("Elbow Method")
ax1.grid(True, alpha=0.3)

ax2.plot(list(K_range), silhouettes, marker="o", color="crimson")
ax2.set_xlabel("Jumlah Cluster (k)")
ax2.set_ylabel("Silhouette Score")
ax2.set_title("Silhouette Score")
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(PLOT_DIR / "elbow_method.png")
plt.close(fig)

k_opt = list(K_range)[np.argmax(silhouettes)]
print(f"\n✅ Cluster optimal (silhouette): k = {k_opt}")

# =====================================================================
# 5.3 K-MEANS FINAL
# =====================================================================
k_final = k_opt
km = KMeans(n_clusters=k_final, random_state=42, n_init=10)
df_feat["Cluster"] = km.fit_predict(X_scaled)
df_feat.to_csv(TABLE_DIR / "clustering_hasil.csv", index=False)

print(f"\n=== PROFIL CLUSTER (k={k_final}) ===")
for c in sorted(df_feat["Cluster"].unique()):
    anggota = df_feat[df_feat["Cluster"] == c]
    print(f"\nCluster {c}:")
    print(f"  Anggota: {', '.join(anggota['Singkat'].values)}")
    print(f"  Rata-rata Mean: {anggota['Mean'].mean():.1f}")
    print(f"  Rata-rata CV: {anggota['CV'].mean():.1f}%")
    print(f"  Rata-rata CAGR: {anggota['CAGR'].mean() * 100:.1f}%")

# =====================================================================
# 5.4 VISUALISASI CLUSTER — scatter plot 2D
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Mean vs CV
ax = axes[0]
scatter = ax.scatter(
    df_feat["Mean"], df_feat["CV"],
    c=df_feat["Cluster"], cmap="Set2", s=100, edgecolors="black",
)
for _, row in df_feat.iterrows():
    ax.annotate(row["Singkat"], (row["Mean"], row["CV"]),
                fontsize=7, ha="center", va="bottom")
ax.set_xlabel("Rata-rata Ekspor (Juta US$)")
ax.set_ylabel("CV (%) — Volatilitas")
ax.set_title("Mean vs CV (per Cluster)")
ax.grid(True, alpha=0.3)

# Plot 2: Mean vs CAGR
ax = axes[1]
scatter = ax.scatter(
    df_feat["Mean"], df_feat["CAGR"] * 100,
    c=df_feat["Cluster"], cmap="Set2", s=100, edgecolors="black",
)
for _, row in df_feat.iterrows():
    ax.annotate(row["Singkat"], (row["Mean"], row["CAGR"] * 100),
                fontsize=7, ha="center", va="bottom")
ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
ax.set_xlabel("Rata-rata Ekspor (Juta US$)")
ax.set_ylabel("CAGR (%) — Pertumbuhan")
ax.set_title("Mean vs CAGR (per Cluster)")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(PLOT_DIR / "clustering_scatter.png")
plt.close(fig)

print(f"\n✅ Clustering selesai. Hasil di: {TABLE_DIR}")
print(f"   Plot di: {PLOT_DIR}")
