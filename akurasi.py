import csv
from ultralytics import YOLO

if __name__ == "__main__":

    model = YOLO("runs/detect/final_model1/weights/best.pt")

    metrics = model.val(data="dataset/data.yaml")

    with open("hasil_validasi.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Metric", "Value"])
        writer.writerow(["Precision", metrics.box.mp])
        writer.writerow(["Recall", metrics.box.mr])
        writer.writerow(["mAP50", metrics.box.map50])
        writer.writerow(["mAP50-95", metrics.box.map])

    print("Hasil validasi berhasil disimpan ke CSV.")