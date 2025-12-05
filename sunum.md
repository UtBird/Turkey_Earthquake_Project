# Deprem Risk ve Tespit Paneli - Proje Sunumu

## 1. Proje Özeti
Bu proje, Türkiye genelindeki deprem riskini analiz etmek, aktif fay hatlarını görselleştirmek ve gerçek zamanlı veri akışı sağlamak amacıyla geliştirilmiş kapsamlı bir masaüstü uygulamasıdır. Python programlama dili kullanılarak geliştirilen bu sistem, kullanıcı dostu bir arayüz üzerinden karmaşık veri analizlerini anlaşılır bir formatta sunmaktadır.

## 2. Teknik Altyapı ve Kullanılan Teknolojiler
Projenin geliştirilmesinde modern yazılım kütüphaneleri ve teknikleri kullanılmıştır:
- **Arayüz (GUI):** Python `tkinter` ve `CustomTkinter` kütüphaneleri ile modern, karanlık mod destekli ve kullanıcı dostu bir arayüz tasarlanmıştır.
- **Veri Analizi:** `Pandas` kütüphanesi ile büyük veri setleri (deprem katalogları, fay hattı verileri) işlenmekte ve analiz edilmektedir.
- **Haritalama:** `Folium` kütüphanesi kullanılarak interaktif haritalar oluşturulmakta, fay hatları ve deprem merkez üsleri katmanlar halinde gösterilmektedir.
- **Risk Motoru:** Özel olarak geliştirilen `EarthquakeRiskEngine`, tarihsel veriler ve coğrafi konum bilgilerini kullanarak olasılıksal risk hesaplamaları yapmaktadır.

## 3. Uygulama Arayüzü ve Kullanım
Uygulama açıldığında kullanıcıyı sade ve işlevsel bir ana ekran karşılamaktadır. Sol tarafta yer alan menü çubuğu üzerinden temel fonksiyonlara (Kamera Tespiti, Risk Hesapla, Harita) erişim sağlanmaktadır.

![Ana Arayüz](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/gui_replica_main_1764927081720.png)
*Şekil 1: Uygulamanın ana giriş ekranı ve kontrol paneli.*

## 4. Temel Özellikler

### 4.1. Şehir Bazlı Risk Analizi
Kullanıcılar belirli bir şehir için risk analizi talep ettiğinde, sistem arka planda çalışan risk motorunu devreye sokar. Bu motor:
1. Seçilen şehrin koordinatlarını belirler.
2. Şehre 150 km yarıçapındaki tarihsel deprem verilerini tarar.
3. Aktif fay hatlarına olan mesafeyi hesaplar.
4. Sonuç olarak 0-10 arasında bir risk skoru ve tahmini şiddet değeri üretir.

![Risk Analizi Sonucu](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/gui_replica_risk_1764927114711.png)
*Şekil 2: İstanbul için yapılan örnek bir risk analizi sonucu.*

### 4.2. İnteraktif Harita Görselleştirme
Analiz sonuçları, `Folium` tabanlı interaktif bir harita üzerinde detaylandırılır. Bu harita üzerinde:
- **Isı Haritaları (Heatmap):** Deprem yoğunluğunun yüksek olduğu bölgeleri gösterir.
- **Fay Hatları:** Aktif fay hatları turuncu çizgilerle belirginleştirilmiştir.
- **Deprem Noktaları:** Büyüklüklerine göre renk kodlu (yeşil, turuncu, kırmızı) daireler ile gösterilir.

![Harita Görünümü](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/risk_map_screenshot_1764926925121.png)
*Şekil 3: Fay hatları ve deprem merkez üslerinin harita üzerindeki gösterimi.*

### 4.3. Kamera Destekli Tespit (Gelecek Vizyonu)
Sisteme entegre edilen kamera modülü, gelecekteki geliştirmelerde anlık sarsıntı tespiti ve görüntü işleme tabanlı hasar analizi için bir altyapı sunmaktadır. Şu anki sürümde kamera bağlantısı ve temel görüntü akışı sağlanmıştır.

## 5. Sonuç
"Deprem Risk ve Tespit Paneli", akademik araştırmalar ve sivil savunma planlamaları için veri odaklı bir karar destek sistemi olarak tasarlanmıştır. Açık kaynak kodlu yapısı ve modüler mimarisi sayesinde, yeni veri kaynaklarının eklenmesi ve özelliklerin geliştirilmesi kolaylıkla mümkündür.

## 6. Kod Yapısı ve Teknik Detaylar
Projenin başarısının arkasında yatan en önemli faktör, modüler ve sürdürülebilir kod yapısıdır. Aşağıda projenin temel bileşenlerini oluşturan kod dosyaları ve işlevleri detaylandırılmıştır.

### 6.1. Ana Uygulama Mantığı (`gui_app.py`)
Bu dosya, uygulamanın omurgasını oluşturur. Kullanıcı etkileşimlerini yönetir, arayüz elemanlarını çizer ve arka plandaki diğer modülleri koordine eder.

**Temel İşlevleri:**
*   **Arayüz Oluşturma:** `CustomTkinter` kütüphanesi kullanılarak modern ve duyarlı bir arayüz inşa eder.
*   **Thread Yönetimi:** Uzun süren işlemlerin (risk hesaplama, veri çekme) arayüzü dondurmaması için `threading` modülü ile asenkron çalışmayı sağlar.
*   **Olay Yönetimi:** Buton tıklamaları ve kullanıcı girdilerini dinleyerek ilgili fonksiyonları tetikler.

![GUI Kodu](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/code_gui_app_1764927344385.png)
*Şekil 4: `gui_app.py` dosyasından bir kesit. Arayüz elemanlarının tanımlandığı ve olay döngülerinin yönetildiği bloklar görülmektedir.*

### 6.2. Risk Hesaplama Motoru (`risk_engine.py`)
Projenin "beyni" olarak nitelendirilebilecek bu modül, veri bilimi ve makine öğrenmesi tekniklerini barındırır.

**Temel İşlevleri:**
*   **Veri İşleme:** Ham deprem verilerini temizler, "declustering" (artçı şok ayıklama) işlemi uygular.
*   **Özellik Mühendisliği (Feature Engineering):** Deprem verilerinden zaman serisi özellikleri (7 günlük ortalama, standart sapma vb.) türetir.
*   **Makine Öğrenmesi Modeli:** `CatBoost` algoritması kullanılarak kısa vadeli risk tahminleri yapar.
*   **Olasılıksal Risk Analizi:** Poisson dağılımı kullanarak uzun vadeli deprem olasılıklarını hesaplar.
*   **Fay Hattı Analizi:** Şehrin aktif fay hatlarına olan mesafesini hesaplayarak coğrafi risk faktörünü belirler.

![Risk Motoru Kodu](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/code_risk_engine_1764927394751.png)
*Şekil 5: `risk_engine.py` dosyasındaki risk hesaplama algoritmaları ve veri işleme fonksiyonları.*

### 6.3. Harita Görselleştirme (`map_visualizer.py`)
Analiz sonuçlarının coğrafi bağlamda sunulmasını sağlayan bu modül, `Folium` kütüphanesi üzerine inşa edilmiştir.

**Temel İşlevleri:**
*   **Katmanlı Harita Yapısı:** Farklı veri tiplerini (depremler, faylar, ısı haritası) ayrı katmanlar halinde yönetir.
*   **GeoJSON Entegrasyonu:** Karmaşık fay hattı verilerini GeoJSON formatında okuyarak harita üzerine işler.
*   **İnteraktif Popup'lar:** Harita üzerindeki noktalara tıklandığında detaylı bilgilerin (büyüklük, derinlik, tarih) gösterilmesini sağlayan HTML/JS tabanlı popup pencereleri oluşturur.
*   **Isı Haritası (Heatmap):** Deprem yoğunluğunu renk gradyanları ile görselleştirerek riskli bölgelerin bir bakışta anlaşılmasını sağlar.

![Harita Kodu](/home/utku/.gemini/antigravity/brain/fa36bab1-48a3-48ec-9ead-c91825ee7d3d/code_map_visualizer_1764927429265.png)
*Şekil 6: `map_visualizer.py` dosyasında harita katmanlarının ve görselleştirme parametrelerinin ayarlandığı bölüm.*

