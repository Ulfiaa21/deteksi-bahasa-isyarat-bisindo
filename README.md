# Deteksi Bahasa Isyarat BISINDO (YOLOv8)

Sistem pendeteksian bahasa isyarat Indonesia (BISINDO) secara real-time menggunakan YOLOv8, mampu mengenali huruf (A-Z), angka (0-9), dan 7 kata isyarat (Ayah, Halo, Kakak, Minum, Rumah, Terima kasih, Tidur) sehingga total 43 kelas.

Tersedia 2 mode penggunaan:
- **Desktop (OpenCV)**
  jendela langsung dari webcam, dengan fitur susun kalimat otomatis.
- **Web App (Flask)** 
  antarmuka browser dengan video stream dan kontrol kalimat (clear, hapus, spasi).


## Fitur

- Deteksi 43 kelas isyarat (26 huruf + 10 angka + 7 kata) secara real-time
- Penyusunan kalimat otomatis berdasarkan stabilitas deteksi 
- Mode desktop (`detect.py`) dan mode web (`api.py` + Flask)
- Kontrol kalimat: hapus huruf terakhir, tambah spasi, clear semua
- Confidence score ditampilkan langsung di layar

## Dataset
Dataset (43 kelas: huruf A-Z, angka 0-9, dan 7 kata isyarat) tersedia di google drive
**[downloaad dataset bisindo](https://drive.google.com/drive/folders/1xS_hoPbSLsFN5464CqydCQx1E3SUVe5g?usp=drive_link)**

caranya:
1. Download dan extract isi dataset dari link di atas
2. Letakkan dengan struktur folder berikut:
```
dataset/

├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```
3. Pastikan `data.yaml` ada di root folder `dataset/` (sudah disertakan di repo ini)
4. Model hasil training (`best.pt`) juga tidak disertakan karena ukurannya besar. Jalankan `train.py` setelah dataset siap untuk menghasilkan model sendiri.

## Struktur Project
```
.
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   ├── labels/
│   │   ├── train/
│   │   └── val/
│   └── data.yaml
├── runs/
│   └── detect/
│       └── final_model1/
│           └── weights/
│               └── best.pt        # model hasil training
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── train.py              # script training YOLOv8
├── detect.py             # deteksi via webcam (mode desktop/OpenCV)
├── api.py                # backend Flask (mode web)
├── akurasi.py            # evaluasi akurasi model
├── cek_distribusi.py     # cek distribusi jumlah data per kelas
├── distribusi_kelas.png  # visualisasi distribusi kelas
├── hasil_validasi.csv    # hasil metrik validasi
├── yolov8s.pt             # pretrained weights (base model)
├── yolo26n.pt              # pretrained weights (alternatif)
└── requirements.txt
```

## Instalasi

### 1. Clone repository
```bash
git clone https://github.com/Ulfiaa21/deteksi-bahasa-isyarat-bisindo.git
cd deteksi-bahasa-isyarat-bisindo
```

### Buat virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Install dependency
```bash
pip install -r requirements.txt
```

## Cara Pakai

### A. Training Model
```bash
python train.py
```
Model hasil training akan tersimpan di `runs/detect/final_model1/weights/best.pt`.

### Mode Desktop (Webcam langsung)
```bash
python detect.py
```
**Kontrol keyboard:**
- `q` → keluar
- `c` → clear kalimat
- `s` → simpan screenshot debug

### Mode Web App (Flask)
```bash
python api.py
```
Buka browser ke:
```
http://localhost:5000
```

## Cara Kerja Deteksi

```
Webcam → Frame → YOLOv8 → Bounding Box + Class + Confidence
       → Filter confidence ≥ threshold
       → Simpan ke history (12 frame terakhir)
       → Jika 1 karakter muncul ≥ 8x dari 12 frame → tambahkan ke kalimat
```

Mekanisme ini (`deque` + `Counter`) mencegah kalimat "kacau" akibat deteksi yang tidak stabil dari frame ke frame.

---

## Evaluasi Model

```bash
python akurasi.py          # cek metrik akurasi model
python cek_distribusi.py   # cek distribusi jumlah sampel per kelas
```
Hasil evaluasi tersimpan di `hasil_validasi.csv` dan `distribusi_kelas.png`.

## Teknologi yang Digunakan

| Komponen | Teknologi |
|---|---|
| Object Detection | YOLOv8 (Ultralytics) |
| Computer Vision | OpenCV |
| Backend Web | Flask |
| Frontend | HTML, CSS, JavaScript (vanilla) |


## Lisensi

Proyek ini menggunakan [MIT License](LICENSE).
