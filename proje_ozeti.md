# Teknosel Deprem Risk ve Tespit Paneli - Proje Özeti

## 1. Projenin Önemi
Türkiye, aktif fay hatları üzerinde bulunan ve sık sık yıkıcı depremlerle karşı karşıya kalan bir ülkedir. Deprem öncesi risk analizi ve binaların mevcut durumunun (çatlak, hasar) tespiti, can ve mal kaybını en aza indirmek için hayati önem taşımaktadır. **Teknosel Deprem Paneli**, makine öğrenmesi algoritmalarıyla şehir bazlı risk analizi yaparak ve görüntü işleme teknolojisiyle bina hasarlarını tespit ederek, hem bireysel kullanıcılar hem de yetkililer için hızlı, veri odaklı bir karar destek mekanizması sunar. Bu proje, teknolojinin afet yönetimi ve hazırlık süreçlerine entegrasyonu açısından kritik bir rol oynamaktadır.

## 2. Projenin Amacı ve Hedefi
**Amaç:**
Kullanıcılara, bulundukları veya merak ettikleri şehirlerin deprem risk durumunu bilimsel verilerle sunmak ve binalardaki yapısal hasarları (çatlak vb.) yapay zeka destekli görüntü işleme yöntemleriyle tespit etmektir.

**Hedefler:**
*   **Veri Odaklı Risk Analizi:** Geçmiş deprem verilerini ve fay hatlarına olan uzaklığı kullanarak, CatBoost algoritması ile kısa ve uzun vadeli risk tahminleri oluşturmak.
*   **Görsel Tespit:** YOLOv8 tabanlı görüntü işleme modelleri ile kamera üzerinden bina çatlaklarını ve yapısal bozuklukları gerçek zamanlı tespit etmek.
*   **Haritalama:** Riskli bölgeleri, fay hatlarını ve geçmiş depremleri interaktif bir harita üzerinde görselleştirmek.
*   **Canlı Takip:** Kandilli Rasathanesi verileriyle anlık deprem takibi sağlamak.
*   **Kullanıcı Dostu Arayüz:** Tüm bu karmaşık analizleri, teknik bilgi gerektirmeyen basit ve anlaşılır bir masaüstü arayüzü (GUI) ile sunmak.

## 3. Projenin İş-Zaman Çizelgesi (14 Hafta)

Projenin geliştirme süreci, başlangıçtan finale kadar aşağıdaki gibi planlanmıştır:

*   **1. Hafta: Proje Planlama, Literatür ve Veri Seti Araştırması**
    *   **Araştırma:** Deprem verileri (Kandilli API) ve yapısal çatlak görüntü veri setleri toplanır.
    *   **Literatür:** CatBoost ve YOLOv8 gibi algoritmaların literatür taraması yapılır.
    *   **Planlama:** Proje mimarisi ve kullanılacak Python kütüphaneleri (Tkinter, Folium, Pandas) belirlenir.

*   **2. Hafta: Sistem Mimarisi ve Arayüz Tasarımı**
    *   **Tasarım:** Masaüstü uygulaması için kullanıcı dostu arayüz (GUI) taslakları çizilir. "Kamera Tespiti", "Risk Analizi" ve "Harita" sayfaları planlanır.
    *   **Akış:** Kullanıcının veri girişi yapıp sonucu alana kadar geçecek süreç şematize edilir.

*   **3. Hafta: Veri Altyapısı ve API Entegrasyonu**
    *   **Veri Yönetimi:** Deprem verilerinin tutulacağı yerel yapıların (CSV/Pandas) oluşturulması ve temizlenmesi.
    *   **API:** Kandilli Rasathanesi'nden canlı veri çeken modüllerin kodlanması.

*   **4. Hafta: Masaüstü Arayüzü (GUI) Geliştirme**
    *   **Kodlama:** Python Tkinter/CustomTkinter ile ana pencere ve menülerin oluşturulması.
    *   **Navigasyon:** Sol menü ve sayfalar arası geçiş altyapısının kurulması.

*   **5. Hafta: Deprem Risk Haritası Entegrasyonu**
    *   **Harita:** Folium kütüphanesi ile interaktif harita modülünün geliştirilmesi.
    *   **Görselleştirme:** Fay hatları ve deprem noktalarının harita üzerine işlenmesi.

*   **6. Hafta: Görüntü İşleme ve Kamera Entegrasyonu**
    *   **Kamera:** OpenCV ile bilgisayar kamerasından görüntü alma modülünün yazılması.
    *   **Ön İşleme:** Görüntülerin model için uygun formata (boyutlandırma, iyileştirme) getirilmesi.

*   **7. Hafta: Makine Öğrenmesi Modellerinin Entegrasyonu**
    *   **Model Entegrasyonu:** Eğitilen CatBoost (Risk) ve YOLOv8 (Görüntü) modelleri sisteme entegre edilir.
    *   **Analiz:** Risk hesaplama motoru ve görüntü işleme algoritmaları ana uygulamaya bağlanır.

*   **8. Hafta: Arayüz ve Model Doğrulama**
    *   **Kontrol:** Arayüz fonksiyonlarının ve kullanıcı deneyiminin test edilmesi.
    *   **Doğrulama:** Yapay zekanın verdiği sonuçların doğruluğu (accuracy) test verileriyle kontrol edilir.

*   **9. Hafta: Uyarı Sistemleri ve Performans Optimizasyonu**
    *   **Bildirim:** Riskli durumlarda veya yeni deprem verisinde arayüzde görsel uyarıların (Popup) oluşturulması.
    *   **Hız:** Modelin cevap verme süresi ve harita yükleme hızının optimize edilmesi.

*   **10. Hafta: Sistem Testleri ve Hata Giderme (Debugging)**
    *   **Test:** Farklı şehir senaryoları ve kamera açılarında sistemin kararlılığının test edilmesi.
    *   **Debug:** Uygulama çökmeleri ve kod hataları giderilir.

*   **11. Hafta: Raporlama ve Geçmiş Veri Özellikleri**
    *   **Rapor:** Analiz sonuçlarının özetlendiği metin tabanlı çıktıların oluşturulması.
    *   **Geçmiş:** Kullanıcının yaptığı eski sorguların loglanması ve görüntülenmesi.

*   **12. Hafta: Veri Analizi ve Model İyileştirme**
    *   **Analiz:** Modelin gerçek dünya verileriyle performansının izlenmesi.
    *   **İyileştirme:** Yanlış tespitler varsa modellerin yeni verilerle tekrar eğitilmesi (Retraining).

*   **13. Hafta: Beta Testleri ve Geri Bildirim**
    *   **Beta:** Uygulamanın geliştirici ortamında kapsamlı testlerinin yapılması.
    *   **Feedback:** Tespit edilen eksikliklerin giderilmesi ve son kullanıcı deneyimi iyileştirmeleri.

*   **14. Hafta: Son Kontroller ve Proje Teslimi**
    *   **Dokümantasyon:** Kod dokümantasyonu ve kullanım kılavuzunun hazırlanması.
    *   **Paketleme:** Projenin çalıştırılabilir dosya (.exe) veya kurulum paketi haline getirilmesi ve sunumu.

## 4. Projede Kullanılacak Donanımlar ve Yazılımlar

### Donanımlar:
1.  **Geliştirme Bilgisayarı:**
    *   İşlemci: Intel Core i5/i7 veya AMD Ryzen 5/7 (Veri işleme ve model eğitimi için).
    *   RAM: Minimum 8GB (16GB önerilir).
    *   Depolama: SSD (Hızlı veri okuma/yazma için).
2.  **Kamera (Webcam):**
    *   Bina çatlak tespiti ve gerçek zamanlı görüntü işleme testleri için standart HD webcam.

### Yazılımlar ve Teknolojiler:
1.  **Programlama Dili:** Python 3.10+
2.  **Geliştirme Ortamı (IDE):** Visual Studio Code (VS Code)
3.  **Kütüphaneler ve Frameworkler:**
    *   **Arayüz (GUI):** `tkinter`, `customtkinter` (Modern arayüz tasarımı için).
    *   **Veri Analizi:** `pandas`, `numpy` (Veri manipülasyonu).
    *   **Makine Öğrenmesi:** `catboost`, `scikit-learn` (Risk tahmini modelleri).
    *   **Görüntü İşleme:** `ultralytics` (YOLOv8), `opencv-python` (Görüntü işleme ve kamera kontrolü).
    *   **Haritalama:** `folium` (İnteraktif harita görselleştirme).
    *   **Coğrafi İşlemler:** `geopy` (Konum ve koordinat işlemleri).
    *   **API/İnternet:** `requests` (Canlı veri çekme).
4.  **Veri Kaynakları:**
    *   Kandilli Rasathanesi API (Canlı deprem verileri).
    *   GEM (Global Earthquake Model) GeoJSON verileri (Fay hatları).
