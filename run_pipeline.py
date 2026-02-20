import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_generation import generate_policy_data
from src.map_utils import create_folium_heatmap, create_folium_cluster

OUT_FIG = os.path.join("reports", "figures")
OUT_MAP = os.path.join("reports", "maps")

def ensure_dirs():
    os.makedirs(OUT_FIG, exist_ok=True)
    os.makedirs(OUT_MAP, exist_ok=True)

def save_kde(before: pd.DataFrame, after: pd.DataFrame):
    # Before
    plt.figure(figsize=(8, 6))
    sns.kdeplot(x=before["lon"], y=before["lat"], fill=True)
    plt.title("KDE Heatmap - Before Policy")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_FIG, "heatmap_before.png"), dpi=160)
    plt.close()

    # After
    plt.figure(figsize=(8, 6))
    sns.kdeplot(x=after["lon"], y=after["lat"], fill=True)
    plt.title("KDE Heatmap - After Policy")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_FIG, "heatmap_after.png"), dpi=160)
    plt.close()

def save_before_after_scatter(before: pd.DataFrame, after: pd.DataFrame):
    plt.figure(figsize=(8, 6))
    plt.scatter(before["lon"], before["lat"], s=6, alpha=0.25, label="Before")
    plt.scatter(after["lon"], after["lat"], s=6, alpha=0.25, label="After")
    plt.title("Before vs After (Synthetic Events)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_FIG, "before_after.png"), dpi=160)
    plt.close()

def dispersion_metric(df: pd.DataFrame) -> float:
    # simple dispersion: mean distance from centroid (degrees)
    lat0, lon0 = df["lat"].mean(), df["lon"].mean()
    d = np.sqrt((df["lat"] - lat0) ** 2 + (df["lon"] - lon0) ** 2)
    return float(d.mean())

def save_metrics(before: pd.DataFrame, after: pd.DataFrame):
    metrics = {
        "dispersion_mean_distance_deg_before": dispersion_metric(before),
        "dispersion_mean_distance_deg_after": dispersion_metric(after),
        "n_before": len(before),
        "n_after": len(after),
    }
    pd.DataFrame([metrics]).to_csv(os.path.join("reports", "metrics.csv"), index=False)

def save_folium_maps(before: pd.DataFrame, after: pd.DataFrame):
    create_folium_heatmap(before, os.path.join(OUT_MAP, "folium_heatmap_before.html"))
    create_folium_heatmap(after,  os.path.join(OUT_MAP, "folium_heatmap_after.html"))

    create_folium_cluster(before, os.path.join(OUT_MAP, "folium_cluster_before.html"))
    create_folium_cluster(after,  os.path.join(OUT_MAP, "folium_cluster_after.html"))

def main():
    ensure_dirs()
    before, after = generate_policy_data()

    # Save raw data too (nice for portfolio)
    before.to_csv(os.path.join("reports", "events_before.csv"), index=False)
    after.to_csv(os.path.join("reports", "events_after.csv"), index=False)

    save_kde(before, after)
    save_before_after_scatter(before, after)
    save_metrics(before, after)
    save_folium_maps(before, after)

    print("✅ Pipeline finished!")
    print("Figures: reports/figures/")
    print("Maps: reports/maps/")
    print("Metrics: reports/metrics.csv")

if __name__ == "__main__":
    main()
