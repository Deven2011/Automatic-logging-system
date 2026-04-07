from ultralytics import YOLO

# Resume from last checkpoint
model = YOLO("runs/detect/license_plate_model/weights/last.pt")

model.train(
    data="data.yaml",
    epochs=50,          # total target epochs
    imgsz=640,
    batch=8,
    device="cpu",
    workers=4,
    patience=10,
    resume=True,
    project="runs/detect",
    name="license_plate_model"
)
