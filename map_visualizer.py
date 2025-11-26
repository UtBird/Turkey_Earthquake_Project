import webbrowser
import os
import folium
from folium.plugins import MarkerCluster, HeatMap

import webbrowser
import os
import folium
from folium.plugins import MarkerCluster, HeatMap

def generate_map(city_name, lat, lon, fault_points, fault_lines=None, geojson_paths=None, all_quakes_df=None, output_file="risk_map.html"):
    """
    Generates a focused map showing the city, its risk radius, and local earthquakes.
    Includes Heatmap, Fault Lines, and GeoJSON layers.
    """
    # 1. Temel Harita
    m = folium.Map(location=[lat, lon], zoom_start=8, tiles="CartoDB dark_matter")

    # 2. Hedef Şehir (Özel İkon)
    folium.Marker(
        [lat, lon],
        popup=f"<div style='font-size: 14px; font-weight: bold;'>{city_name}</div>",
        tooltip="Analiz Edilen Şehir",
        icon=folium.Icon(color="red", icon="info-sign", prefix='fa')
    ).add_to(m)

    # 3. Kapsama Alanı (150km Yarıçap)
    folium.Circle(
        location=[lat, lon],
        radius=150000, # Metre cinsinden
        color="#3388ff",
        fill=True,
        fill_opacity=0.1,
        popup="150km Risk Analiz Yarıçapı"
    ).add_to(m)

    # 4. Basit Fay Hatları Katmanı (Manuel Çizim)
    if fault_lines:
        fault_group = folium.FeatureGroup(name="Ana Fay Hatları (Basit)")
        for line in fault_lines:
            folium.PolyLine(
                line,
                color="red",
                weight=3,
                opacity=0.7,
                tooltip="Ana Fay Hattı"
            ).add_to(fault_group)
        fault_group.add_to(m)

    # 5. Detaylı GeoJSON Fay Hatları
    if geojson_paths:
        for path in geojson_paths:
            if os.path.exists(path):
                name = os.path.basename(path).replace(".geojson", "").replace("_", " ").title()
                try:
                    folium.GeoJson(
                        path,
                        name=f"Detaylı Faylar: {name}",
                        style_function=lambda x: {
                            'color': '#ff9900', 
                            'weight': 1, 
                            'opacity': 0.6
                        },
                        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Fay Adı:'], localize=True) if 'name' in str(open(path, encoding='utf-8').read(1000)) else None
                    ).add_to(m)
                except Exception as e:
                    print(f"GeoJSON yüklenemedi ({path}): {e}")

    if all_quakes_df is not None and not all_quakes_df.empty:
        # 6. Isı Haritası (Heatmap) Katmanı
        heat_data = all_quakes_df[['latitude', 'longitude', 'mag']].values.tolist()
        HeatMap(
            heat_data,
            name="Deprem Yoğunluğu (Isı Haritası)",
            radius=15,
            max_zoom=10,
        ).add_to(m)

        # 7. Geçmiş Depremler (Kümeleme)
        marker_cluster = MarkerCluster(name="Bölgesel Depremler").add_to(m)
        
        # Performans için filtre
        significant_quakes = all_quakes_df[all_quakes_df['mag'] >= 3.0]
        
        for _, row in significant_quakes.iterrows():
            # Renk belirle
            mag = row['mag']
            color = "green"
            if mag >= 4.0: color = "orange"
            if mag >= 5.0: color = "red"
            if mag >= 6.0: color = "darkred"
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=4 + (mag - 3) * 2, 
                popup=f"Tarih: {row['time']}<br>Büyüklük: <b>{mag}</b><br>Derinlik: {row['depth']} km",
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(marker_cluster)

    # Katman Kontrolü
    folium.LayerControl(collapsed=False).add_to(m)

    # Haritayı kaydet
    m.save(output_file)
    
    # Tarayıcıda aç
    webbrowser.open("file://" + os.path.realpath(output_file))
    return os.path.realpath(output_file)
