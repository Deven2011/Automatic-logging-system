from ultralytics import YOLO

# Load your trained plate detection model
model = YOLO("runs/detect/train7/weights/best.pt")
  # adjust path if needed
print("Loaded model:", model.model.args['model'])



def detect_plate(frame):
    # Run inference with LOWER confidence
    results = model(frame, conf=0.25, verbose=False)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            if conf >= 0.25:
                plate_crop = frame[y1:y2, x1:x2]
                return plate_crop, conf

    return None, 0
