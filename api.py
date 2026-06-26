from flask import Flask, Response, jsonify, render_template
from ultralytics import YOLO
import cv2
import threading
from collections import deque, Counter

app = Flask(__name__)

# Load model
model = YOLO("runs/detect/final_model1/weights/best.pt")

# State global
camera = None
output_frame = None
lock = threading.Lock()
detection_thread = None

CONF_THRESHOLD = 0.5
HISTORY_SIZE = 12
STABLE_COUNT = 8

kalimat = ""
last_char = ""
history = deque(maxlen=HISTORY_SIZE)
current_detection = {"char": "", "conf": 0.0, "kalimat": ""}

def detect_frames():
    global camera, output_frame, kalimat, last_char, history, current_detection

    camera = cv2.VideoCapture(0)

    while camera and camera.isOpened():
        ret, frame = camera.read()    # mengambil gambar dari kamera
        if not ret:
            break

        results = model(frame, verbose=False)  #mengirim gambar ke yolo, yolo akan mengembalikan hasil deteksi

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
            most_common, count = Counter(history).most_common(1)[0] # mengambil karakter yang paling sering muncul
            if count >= STABLE_COUNT and most_common and most_common != last_char:
                kalimat += most_common  
                last_char = most_common

        current_detection = {
            "char": detected_char,
            "conf": round(best_conf * 100, 1),
            "kalimat": kalimat.strip()
        }

        annotated = frame.copy()

        with lock:
            output_frame = annotated.copy()

def generate():
    global output_frame
    while True:
        with lock:
            if output_frame is None:
                continue
            ret, buffer = cv2.imencode('.jpg', output_frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# ===== ROUTES =====

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/detection')
def get_detection():
    return jsonify(current_detection)

@app.route('/api/start', methods=['POST'])
def start_camera():
    global detection_thread
    if not any(t.name == 'detection' for t in threading.enumerate()):
        detection_thread = threading.Thread(target=detect_frames, name='detection')
        detection_thread.daemon = True
        detection_thread.start()
    return jsonify({"status": "started"})

@app.route('/api/stop', methods=['POST'])
def stop_camera():
    global camera, output_frame
    if camera:
        camera.release()
        camera = None
    output_frame = None
    return jsonify({"status": "stopped"})

@app.route('/api/clear', methods=['POST'])
def clear_kalimat():
    global kalimat, last_char, history
    kalimat = ""
    last_char = ""
    history.clear()
    return jsonify({"status": "cleared"})

@app.route('/api/hapus', methods=['POST'])
def hapus_huruf():
    global kalimat, last_char
    kalimat = kalimat.rstrip()
    if kalimat:
        kalimat = kalimat[:-1]
    last_char = ""
    return jsonify({"status": "ok", "kalimat": kalimat})

@app.route('/api/spasi', methods=['POST'])
def tambah_spasi():
    global kalimat, last_char
    if kalimat and not kalimat.endswith(" "):
        kalimat = kalimat + " "
    last_char = ""
    return jsonify({"status": "ok", "kalimat": kalimat})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)