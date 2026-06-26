from ultralytics import YOLO
import cv2
from collections import deque, Counter

model = YOLO("runs/detect/final_model1/weights/best.pt") 

cap = cv2.VideoCapture(0)

CONF_THRESHOLD = 0.45
HISTORY_SIZE = 12
STABLE_COUNT = 8

kalimat = ""
last_char = ""
history = deque(maxlen=HISTORY_SIZE)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    detected_char = ""
    best_conf = 0.0

    for r in results:
        if r.boxes is None or len(r.boxes) == 0:
            continue
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            if conf > best_conf and conf >= CONF_THRESHOLD:
                best_conf = conf
                detected_char = model.names[cls]

    history.append(detected_char)

    if len(history) == HISTORY_SIZE:
        most_common, count = Counter(history).most_common(1)[0]
        if count >= STABLE_COUNT and most_common and most_common != last_char:
            kalimat += most_common + " "
            last_char = most_common

    annotated_frame = results[0].plot()

    cv2.putText(annotated_frame, f"Deteksi: {detected_char} ({best_conf:.2f})",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(annotated_frame, f"Kalimat: {kalimat}",
                (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

    cv2.imshow("Deteksi Bahasa Isyarat", annotated_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        kalimat = ""
        last_char = ""
        history.clear()
    elif key == ord('s'):
        cv2.imwrite(f"debug_{detected_char}_{best_conf:.2f}.jpg", annotated_frame)
        print(f"Screenshot disimpan!")

cap.release()
cv2.destroyAllWindows()