from ultralytics import YOLO

if __name__ == "__main__":

    model = YOLO("yolov8s.pt")

    model.train(
        data="dataset/data.yaml",
        epochs=60,
        imgsz=416,
        batch=8,
        name="final_model1",
        fliplr=0.0,
        patience=20,
        device=0,
    )