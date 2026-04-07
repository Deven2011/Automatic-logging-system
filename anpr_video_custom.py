import cv2
import re
from collections import defaultdict
from ultralytics import YOLO
from plate_reader import read_plate, merge_plate_lines

# ================= CONFIG =================
VIDEO_PATH = "test_videos/truck_video.mp4"
MODEL_PATH = "runs/detect/train9/weights/best.pt"

CONFIRM_HITS = 3              # frames needed to confirm
CONFIDENCE_THRESHOLD = 0.3
MIN_PLATE_LENGTH = 6
# =========================================

def clean_plate(text):
    text = text.upper().replace(" ", "").replace("-", "")
    return re.sub(r"[^A-Z0-9]", "", text)

def is_reasonable_plate(plate):
    return len(plate) >= MIN_PLATE_LENGTH

# -------------------------------
# LOAD MODEL
# -------------------------------
model = YOLO(MODEL_PATH)

# -------------------------------
# OPEN VIDEO
# -------------------------------
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError("❌ Could not open video")

print("🎥 Video opened successfully")

plate_counter = defaultdict(int)
frame_id = 0

# -------------------------------
# MAIN LOOP
# -------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("✅ End of video (no plate confirmed)")
        break

    frame_id += 1

    # ---------------------------
    # PLATE DETECTION
    # ---------------------------
    results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)[0]

    if len(results.boxes) == 0:
        continue

    # Take highest-confidence detection
    box = results.boxes[results.boxes.conf.argmax()]
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    plate_img = frame[y1:y2, x1:x2]

    # ---------------------------
    # OCR + MERGE (CAR + TRUCK)
    # ---------------------------
    lines = read_plate(plate_img)
    plate, confidence = merge_plate_lines(lines)

    if not plate:
        continue

    cleaned = clean_plate(plate)

    if not is_reasonable_plate(cleaned):
        continue

    # ---------------------------
    # STABILIZATION (FRAME HITS)
    # ---------------------------
    plate_counter[cleaned] += 1
    print(f"Frame {frame_id}: {cleaned} ({plate_counter[cleaned]})")

    # ---------------------------
    # CONFIRMATION
    # ---------------------------
    if plate_counter[cleaned] >= CONFIRM_HITS:
        print("\n✅ FINAL PLATE CONFIRMED:", cleaned)
        cap.release()
        cv2.destroyAllWindows()
        exit()

# -------------------------------
# CLEANUP
# -------------------------------
cap.release()
cv2.destroyAllWindows()
