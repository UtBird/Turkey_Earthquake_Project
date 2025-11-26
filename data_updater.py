import requests
import pandas as pd
import os
from datetime import datetime
import numpy as np

CSV_PATH = "assets/query.csv"
API_URL = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"

def fetch_and_update_data():
    """
    Kandilli API'den son depremleri çekip CSV dosyama ekliyorum.
    Sadece yeni olanları kaydediyorum.
    """
    print("Canlı veri kontrol ediliyor...")
    
    try:
        # 1. Mevcut CSV dosyasını okuyorum
        if os.path.exists(CSV_PATH):
            try:
                df_existing = pd.read_csv(CSV_PATH)
                # Tarihleri düzeltiyorum
                df_existing = df_existing.dropna(subset=['time'])
                
                # Zaman dilimi yoksa UTC yapıyorum
                else:
                    df_existing['time'] = df_existing['time'].dt.tz_convert('UTC')
                    
            except Exception as e:
                print(f"CSV okuma hatası: {e}")
                return "CSV okuma hatası."
        else:
            print("CSV dosyası bulunamadı, yeni oluşturulacak.")
            df_existing = pd.DataFrame(columns=[
                "time", "latitude", "longitude", "depth", "mag", "place", "type"
            ])

        # 2. API'den güncel verileri çekiyorum
        response = requests.get(API_URL, timeout=10)
        if response.status_code != 200:
            print(f"API Hatası: {response.status_code}")
            return f"API Hatası: {response.status_code}"
            
        data = response.json()
        if not data.get("status"):
            print("API durumu başarısız.")
            return "API veri döndürmedi."

        earthquakes = data["result"]
        new_records = []
        
        # En son hangi tarihte kaldığımı buluyorum
        if not df_existing.empty:
            last_recorded_time = df_existing['time'].max()
        else:
            last_recorded_time = pd.Timestamp.min.tz_localize('UTC')

        print(f"Son kayıtlı deprem tarihi (UTC): {last_recorded_time}")

        count = 0
        for eq in earthquakes:
            # API'den gelen tarih formatını düzeltiyorum (YYYY.MM.DD HH:MM:SS)
            date_str = eq.get("date_time")
            if not date_str:
                continue
                
            try:
                # "." ları "-" yapıp parse edelim
                # Örnek format: 2024.11.22 14:15:00
                formatted_date_str = date_str.replace(".", "-")
                # Türkiye saati (UTC+3) olarak ayarlayıp UTC'ye çeviriyorum
                eq_time = eq_time_naive.tz_localize('Etc/GMT-3') # GMT-3 is UTC+3
                eq_time_utc = eq_time.tz_convert('UTC')
                
            except Exception as e:
                # print(f"Tarih parse hatası: {e}")
                continue

            # Eğer bu deprem yeni ise listeye ekliyorum
            if eq_time_utc > last_recorded_time:
                # CSV formatına uygun kayıt oluştur
                
                record = {
                    "time": eq_time_utc, # Datetime objesi (UTC)
                    "latitude": eq.get("geojson", {}).get("coordinates", [0, 0])[1],
                    "longitude": eq.get("geojson", {}).get("coordinates", [0, 0])[0],
                    "depth": eq.get("depth"),
                    "mag": eq.get("mag"),
                    "magType": "ml", # Varsayılan
                    "place": eq.get("title"),
                    "type": "earthquake",
                    "status": "automatic"
                }
                new_records.append(record)
                count += 1

        if not new_records:
            print("Yeni deprem verisi yok.")
            return "Veriler güncel."

        # 3. Yeni verileri eskilerle birleştiriyorum
        df_new = pd.DataFrame(new_records)
        
        # Sütunları eşliyorum
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
        
        # Yeniden eskiye sıralıyorum
        df_updated = df_updated.sort_values("time", ascending=False)

        # 4. Dosyayı kaydediyorum
        # Tarih formatını CSV için standart hale getiriyorum
        df_to_save = df_updated.copy()
        df_to_save['time'] = df_to_save['time'].dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        df_to_save.to_csv(CSV_PATH, index=False)
        print(f"{count} yeni deprem eklendi.")
        return f"{count} yeni deprem eklendi."

    except Exception as e:
        print(f"Veri güncelleme hatası: {e}")
        return f"Hata: {e}"

if __name__ == "__main__":
    fetch_and_update_data()
