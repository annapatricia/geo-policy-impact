import folium
from folium.plugins import HeatMap, MarkerCluster

def create_folium_heatmap(df, out_html: str, zoom_start: int = 12):
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=zoom_start, tiles="cartodbpositron")
    HeatMap(df[["lat", "lon"]].values.tolist(), radius=10, blur=12).add_to(m)
    m.save(out_html)

def create_folium_cluster(df, out_html: str, zoom_start: int = 12):
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=zoom_start, tiles="cartodbpositron")
    cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=3,
            fill=True
        ).add_to(cluster)

    m.save(out_html)
