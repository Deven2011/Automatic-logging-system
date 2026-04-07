import cv2
from ultralytics import YOLO
from plate_reader import read_plate, merge_plate_lines

DEBUG = True

# -------------------------------
# LOAD MODEL
# -------------------------------
MODEL_PATH = r"runs/detect/train9/weights/best.pt"
model = YOLO(MODEL_PATH)

# -------------------------------
# LOAD IMAGE
# -------------------------------
image_path = "test_images/truck1.jpg"
image = cv2.imread(image_path)

if image is None:
    raise RuntimeError("❌ Image not found")

print("✅ Image loaded")

# -------------------------------
# DETECT PLATE
# -------------------------------
results = model(image, conf=0.15)[0]

if len(results.boxes) == 0:
    print("❌ No plate detected")
    exit()

box = results.boxes[results.boxes.conf.argmax()]
x1, y1, x2, y2 = map(int, box.xyxy[0])
plate_img = image[y1:y2, x1:x2]

print(f"✅ Plate detected (confidence: {float(box.conf):.2f})")

# -------------------------------
# SHOW CROP (NON-BLOCKING)
# -------------------------------
if DEBUG:
    cv2.imshow("Plate Crop", plate_img)
    cv2.waitKey(1)

# -------------------------------
# OCR
# -------------------------------
lines = read_plate(plate_img)

print("Raw OCR output:")
for line in lines:
    print(f"  {line['text']} ({line['score']:.2f})")

# -------------------------------
# MERGE
# -------------------------------
plate, confidence = merge_plate_lines(lines)

print("\nFINAL RESULT")
print("Plate:", plate if plate else "❌ Invalid / Uncertain")
print("Confidence:", confidence)

# -------------------------------
# AUTO EXIT (NO FREEZE)
# -------------------------------
cv2.waitKey(1000)   # show window briefly
cv2.destroyAllWindows()
