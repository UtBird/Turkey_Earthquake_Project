# Deprem Risk ve Tespit Paneli - Kapsamlı Teknik Rapor

## 1. Yönetici Özeti
Bu rapor, Türkiye genelindeki deprem riskini analiz etmek, aktif fay hatlarını görselleştirmek ve gerçek zamanlı veri akışı sağlamak amacıyla geliştirilen "Deprem Risk ve Tespit Paneli" projesinin teknik detaylarını, mimarisini ve uygulama süreçlerini kapsamaktadır. Proje, Python tabanlı modüler bir mimari üzerine inşa edilmiş olup, makine öğrenmesi algoritmaları ve coğrafi bilgi sistemleri (GIS) teknolojilerini entegre etmektedir.

## 2. Proje Kapsamı ve Amaç
Projenin temel amacı, kullanıcıların belirli bir şehir veya bölge için deprem riskini saniyeler içinde analiz edebilmesini sağlamaktır. Sistem, tarihsel deprem verilerini, aktif fay hattı haritalarını ve canlı deprem bildirimlerini birleştirerek bütüncül bir risk skoru üretir.

**Hedefler:**
*   Şehir bazlı kısa ve uzun vadeli risk tahmini.
*   Aktif fay hatlarının ve deprem merkez üslerinin harita üzerinde görselleştirilmesi.
*   Kandilli Rasathanesi verileriyle canlı deprem takibi.
*   Kamera tabanlı görüntü işleme ile yapısal hasar tespiti (prototip aşaması).

## 3. Sistem Mimarisi
Proje, MVC (Model-View-Controller) benzeri bir yapıda tasarlanmıştır. Veri yönetimi, iş mantığı ve kullanıcı arayüzü birbirinden bağımsız modüller halinde geliştirilmiştir.

### 3.1. Modül Diyagramı
*   **Veri Katmanı:** `data_manager.py` (Veri çekme ve saklama)
*   **İş Mantığı Katmanı:** `risk_engine.py` (Risk hesaplama ve ML modelleri)
*   **Görselleştirme Katmanı:** `map_visualizer.py` (Harita üretimi)
*   **Sunum Katmanı:** `gui_app.py` (Kullanıcı arayüzü)
*   **Algılama Katmanı:** `camera_manager.py` (Görüntü işleme)

## 4. Detaylı Bileşen Analizi

### 4.1. Kullanıcı Arayüzü (`gui_app.py`)
Uygulamanın ön yüzü, `CustomTkinter` kütüphanesi kullanılarak geliştirilmiştir. Modern, karanlık mod destekli ve yüksek çözünürlüklü ekranlara uyumlu bir tasarım dili benimsenmiştir.

**Özellikler:**
*   **Responsive Tasarım:** Linux, Windows ve macOS üzerinde tutarlı görünüm.
*   **Asenkron İşlem:** `threading` modülü sayesinde arayüz donmadan arka planda ağır hesaplamalar yapılabilir.
*   **Dinamik İçerik:** Analiz sonuçlarına göre güncellenen durum çubukları ve metin alanları.

![Ana Arayüz](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/gui_replica_main_1764927081720.png)
*Şekil 1: Uygulamanın ana kontrol paneli.*

![GUI Kodu](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/code_gui_app_1764927344385.png)
*Şekil 2: `gui_app.py` kaynak kodundan bir kesit.*

### 4.2. Risk Hesaplama Motoru (`risk_engine.py`)
Sistemin en kritik bileşeni olan bu modül, istatistiksel ve yapay zeka tabanlı yöntemleri birleştirir.

**Algoritmik Yaklaşım:**
1.  **Veri Temizleme (Declustering):** Ana şokları artçı şoklardan ayırmak için uzay-zaman penceresi yöntemi kullanılır.
2.  **Özellik Çıkarımı:** Deprem büyüklüklerinin 7 günlük hareketli ortalamaları, standart sapmaları ve maksimum değerleri hesaplanır.
3.  **Makine Öğrenmesi:** `CatBoostClassifier` kullanılarak, bir bölgede önümüzdeki 30 gün içinde M≥4.0 büyüklüğünde bir deprem olma olasılığı tahmin edilir.
4.  **Poisson Süreci:** Uzun vadeli (10 yıl) büyük deprem (M≥6.0) olasılığı hesaplanır.
5.  **Fay Mesafesi:** Kullanıcının sorguladığı konumun bilinen aktif fay hatlarına (NAF, EAF vb.) olan en kısa mesafesi `Haversine` formülü ile hesaplanır.

**Risk Skoru Formülü:**
```python
Final_Score = 0.4 * Short_Term_Risk + 0.3 * Long_Term_Hazard + 0.3 * Fault_Proximity_Score
```

![Risk Analizi Sonucu](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/gui_replica_risk_1764927114711.png)
*Şekil 3: Risk analizi sonuç ekranı.*

![Risk Motoru Kodu](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/code_risk_engine_1764927394751.png)
*Şekil 4: `risk_engine.py` içindeki risk hesaplama fonksiyonları.*

### 4.3. Harita Görselleştirme (`map_visualizer.py`)
Coğrafi verilerin anlaşılır hale getirilmesi için `Folium` kütüphanesi kullanılır.

**Katmanlar:**
*   **Base Map:** CartoDB Dark Matter ve OpenStreetMap seçenekleri.
*   **Isı Haritası:** Deprem yoğunluğunu gösteren dinamik katman.
*   **GeoJSON Fayları:** MTA ve GEM (Global Earthquake Model) verilerinden alınan detaylı fay hattı vektörleri.
*   **Deprem Markerları:** Büyüklüğe göre renk değiştiren (Yeşil < 4, Turuncu < 5, Kırmızı > 5) interaktif noktalar.

![Harita Görünümü](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/risk_map_screenshot_1764926925121.png)
*Şekil 5: İstanbul çevresindeki fay hatları ve deprem aktivitesini gösteren harita.*

![Harita Kodu](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/code_map_visualizer_1764927429265.png)
*Şekil 6: `map_visualizer.py` kod yapısı.*

### 4.4. Veri Yönetimi (`data_manager.py`)
Sistemin güncel kalmasını sağlayan modüldür.
*   **Kaynak:** Kandilli Rasathanesi API (`https://api.orhanaydogdu.com.tr`).
*   **İşleyiş:** Uygulama her açıldığında API'yi sorgular, yeni deprem verilerini çeker, tarih formatlarını UTC standardına dönüştürür ve yerel `query.csv` veritabanını günceller.
*   **Hata Yönetimi:** API kesintilerine ve bozuk verilere karşı dirençli bir yapıdadır.

### 4.5. Kamera ve Görüntü İşleme (`camera_manager.py`)
YOLOv8 (You Only Look Once) mimarisi kullanılarak geliştirilen nesne tespit modülüdür.
*   **Modeller:** `catlak.pt` (duvar çatlaklarını tespit eder) ve `bina.pt` (bina genel durumunu analiz eder).
*   **Performans:** `OpenCV` ile video akışını işler ve tespit sonuçlarını gerçek zamanlı olarak ekrana çizer. Ayrı bir thread üzerinde çalıştığı için ana uygulamayı yavaşlatmaz.

## 5. Kullanılan Teknolojiler ve Kütüphaneler
| Kütüphane | Amaç |
|-----------|------|
| **Python 3.10+** | Ana programlama dili |
| **CustomTkinter** | Modern GUI geliştirme |
| **Pandas & NumPy** | Veri analizi ve matematiksel işlemler |
| **CatBoost** | Makine öğrenmesi (Gradient Boosting) |
| **Folium** | Harita görselleştirme |
| **Ultralytics YOLO** | Nesne tespiti (Görüntü işleme) |
| **Geopy** | Adres-koordinat dönüşümü (Geocoding) |
| **Requests** | HTTP istekleri ve API entegrasyonu |

## 6. Kurulum ve Çalıştırma
Proje, Linux ortamında geliştirilmiş olup aşağıdaki adımlarla kurulabilir:

1.  Bağımlılıkların yüklenmesi:
    ```bash
    pip install -r requirements.txt
    ```
2.  Uygulamanın başlatılması:
    ```bash
    python gui_app.py
    ```

## 7. Sonuç ve Gelecek Çalışmalar
Bu proje, deprem risk analizi konusunda bireysel farkındalığı artırmak ve karar vericilere veri odaklı bir perspektif sunmak için güçlü bir temel oluşturmaktadır. Gelecek sürümlerde:
*   Daha geniş veri setleri ile modelin eğitilmesi,
*   3D bina modelleme entegrasyonu,
*   Mobil uygulama sürümü (Flutter entegrasyonu) hedeflenmektedir.
