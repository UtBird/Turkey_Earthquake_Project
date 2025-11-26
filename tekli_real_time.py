import cv2
import time
from ultralytics import YOLO

# 1. Modeli yükle
model = YOLO("yeniçatlak.pt")

# 2. Webcam başlat
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı.")
    exit()

# 3. Gerçek zamanlı döngü
while True:
    ret, frame = cap.read()
    if not ret:
        print("Görüntü alınamadı.")
        break

    # Aynalama (ayna görüntüsü)
    frame = cv2.flip(frame, 1)

    # YOLO ile tahmin yap
    results = model(frame, conf=0.7)

    # Tahminleri işle ve çiz
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]


            print(f"Algılandı: {label} - Güven: %{conf * 100:.2f}")

            # Belirli nesne tespit edilirse ekran görüntüsü kaydet
            #cv2.imwrite(f"algılananlar/detected_{label}_{int(time.time())}.jpg", annotated_frame)

        # Görsel üzerine çizim
        annotated_frame = r.plot()

    # Ekranda göster
    cv2.imshow("YOLOv8 Real-Time Detection", annotated_frame)

    # 'q' tuşuna basıldığında çık
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Temizlik
cap.release()
cv2.destroyAllWindows()
