import webbrowser
import os
import json
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

    # 3. Kapsama Alanı (150km Yarıçap) - İPTAL EDİLDİ (Kullanıcı isteği)
    # folium.Circle(
    #     location=[lat, lon],
    #     radius=150000, # Metre cinsinden
    #     color="#3388ff",
    #     fill=True,
    #     fill_opacity=0.1,
    #     popup="150km Risk Analiz Yarıçapı"
    # ).add_to(m)

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
                    # UTF-8 encoding ile oku
                    with open(path, "r", encoding="utf-8") as f:
                        geo_data = json.load(f)
                    
                    folium.GeoJson(
                        geo_data,
                        name=f"Detaylı Faylar: {name}",
                        zoom_on_click=False, # Tıklayınca zoom yapmayı/kare içine almayı engelle
                        style_function=lambda x: {
                            'color': '#ff9900', 
                            'weight': 1, 
                            'opacity': 0.6
                        },
                        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Fay Adı:'], localize=True) if 'name' in str(geo_data).lower() else None
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

        # 7. Geçmiş Depremler (Tekil - Etki Alanı)
        # Kümeleme yerine FeatureGroup kullanıyoruz
        quake_group = folium.FeatureGroup(name="Bölgesel Depremler (Etki Alanı)")
        
        # Performans için filtre
        significant_quakes = all_quakes_df[all_quakes_df['mag'] >= 3.0]
        
        for _, row in significant_quakes.iterrows():
            mag = row['mag']
            
            # Renk belirle
            color = "green"
            if mag >= 4.0: color = "orange"
            if mag >= 5.0: color = "red"
            if mag >= 6.0: color = "darkred"
            
            # Etki alanı yarıçapı (Heuristik: 10^(0.5*M - 1) km)
            impact_radius_km = int(10**(0.5 * mag - 1))
            impact_radius_m = impact_radius_km * 1000
            
            # Popup içeriği
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px;">
                <b>Tarih:</b> {row['time']}<br>
                <b>Büyüklük:</b> <span style="color: {color}; font-weight: bold;">{mag}</span><br>
                <b>Derinlik:</b> {row['depth']} km<br>
                <b>Tahmini Etki Yarıçapı:</b> ~{impact_radius_km} km
                <span id="impact_radius_m" hidden>{int(impact_radius_m)}</span>
            </div>
            """

            # 1. Merkez Noktası
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=4,
                color=color,
                fill=True,
                fill_opacity=0.8,
                popup=folium.Popup(popup_html, max_width=250)
            ).add_to(quake_group)

        quake_group.add_to(m)

    # Katman Kontrolü
    folium.LayerControl(collapsed=False).add_to(m)

    # --- Custom JS: Tıklanan depremin etki alanını göster ---
    map_id = m.get_name()
    js_script = f"""
    <script>
    var currentImpactCircle = null;
    
    // Harita yüklendiğinde çalışacak
    window.addEventListener('load', function() {{
        var map = {map_id};
        
        map.on('popupopen', function(e) {{
            // Eğer önceki bir çember varsa kaldır
            if (currentImpactCircle) {{
                map.removeLayer(currentImpactCircle);
                currentImpactCircle = null;
            }}
            
            // Popup içeriğinden yarıçapı al
            var content = e.popup.getContent();
            // HTML string olabilir, element olabilir. String ise regex ile al.
            if (typeof content === 'string') {{
                var match = content.match(/id="impact_radius_m" hidden>(\\d+)</);
                if (match) {{
                    var radius = parseInt(match[1]);
                    var latlng = e.popup.getLatLng();
                    
                    // Yeni çemberi çiz
                    currentImpactCircle = L.circle(latlng, {{
                        radius: radius,
                        color: 'red',
                        weight: 1,
                        fillColor: 'red',
                        fillOpacity: 0.2,
                        interactive: false // Tıklamaları engellemesin
                    }}).addTo(map);
                }}
            }}
        }});

        map.on('popupclose', function(e) {{
            // Popup kapanınca çemberi kaldır
            if (currentImpactCircle) {{
                map.removeLayer(currentImpactCircle);
                currentImpactCircle = null;
            }}
        }});
    }});
    </script>
    """
    m.get_root().html.add_child(folium.Element(js_script))

    # Haritayı kaydet
    m.save(output_file)
    
    # Tarayıcıda aç
    webbrowser.open("file://" + os.path.realpath(output_file))
    return os.path.realpath(output_file)
