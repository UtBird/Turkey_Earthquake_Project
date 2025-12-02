import requests
import json

def get_live_earthquakes():
    url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
    try:
        print(f"Veri çekiliyor: {url} ...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data["status"]:
                print(f"\nBaşarılı! Toplam {len(data['result'])} deprem verisi alındı.\n")
                if len(data['result']) > 0:
                    print("İlk kaydın anahtarları:", data['result'][0].keys())
                
                print("Son 3 Deprem:")
                print("-" * 50)
                for eq in data["result"][:3]:
                    # Hata almamak için güvenli erişim
                    date_val = eq.get('date') or eq.get('date_time') or "Tarih Yok"
                    title_val = eq.get('title') or eq.get('location') or "Konum Yok"
                    mag_val = eq.get('mag') or "0.0"
                    depth_val = eq.get('depth') or "0.0"
                    
                    print(f"Tarih: {date_val}")
                    print(f"Yer:   {title_val}")
                    print(f"Büyüklük: {mag_val}")
                    print(f"Derinlik: {depth_val} km")
                    print("-" * 50)
            else:
                print("API yanıt döndü ama status false.")
        else:
            print(f"Hata: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    get_live_earthquakes()
