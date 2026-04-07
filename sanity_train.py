from ultralytics import YOLO

# Load base YOLOv8 model
model = YOLO("yolov8n.pt")

# Sanity training on truck license plate dataset
model.train(
    data="datasets/truck_lp_yolo/data.yaml",
    epochs=5,
    imgsz=640,
    batch=8,
    device="cpu"
)
