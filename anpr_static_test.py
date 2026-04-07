import cv2
from plate_detector import detect_plate
from plate_reader import read_plate
from plate_utils import best_plate_candidate
from plate_stabilizer import PlateStabilizer

# -----------------------------
# CONFIG
# -----------------------------
IMAGE_PATH = "test_images/truck1.jpg"

# Require plate to appear at least twice to be considered stable
stabilizer = PlateStabilizer(min_hits=2, timeout=3.0)

# -----------------------------
# LOAD IMAGE
# -----------------------------
image = cv2.imread(IMAGE_PATH)

if image is None:
    raise RuntimeError("❌ Image not found or cannot be loaded")

print("✅ Image loaded")

# -----------------------------
# PLATE DETECTION
# -----------------------------
plate_img, det_conf = detect_plate(image)

if plate_img is None:
    print("❌ No plate detected")
    exit()

print(f"✅ Plate detected (confidence: {det_conf:.2f})")

# -----------------------------
# OCR
# -----------------------------
texts, scores = read_plate(plate_img)

print("Raw OCR output:")
for t, s in zip(texts, scores):
    print(f"  {t} ({s:.2f})")

# -----------------------------
# PLATE MERGE + CLEAN
# -----------------------------
plate, confidence = best_plate_candidate(texts, scores)

print("\nMERGED RESULT")
print("Plate:", plate)
print("Confidence:", confidence)

# -----------------------------
# STABILIZATION LOGIC
# -----------------------------
stable_plate = stabilizer.update(plate)

if stable_plate:
    print("\n✅ STABLE PLATE CONFIRMED")
    print("Final Plate:", stable_plate)
else:
    print("\n⏳ Plate detected but not yet stable")

# -----------------------------
# DISPLAY CROPPED PLATE
# -----------------------------
cv2.imshow("Detected Plate", plate_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
