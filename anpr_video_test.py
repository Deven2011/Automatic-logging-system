import cv2
from plate_detector import detect_plate
from plate_reader import read_plate
from plate_utils import best_plate_candidate
from plate_stabilizer import PlateStabilizer

VIDEO_PATH = "test_videos/truck_video.mp4"

# Plate must appear in multiple frames
stabilizer = PlateStabilizer(min_hits=3, timeout=2.0)

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise RuntimeError("❌ Cannot open video file")

print("🎥 Video opened successfully")

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Process only every 5th frame
    if frame_count % 15 != 0:
        continue

    plate_img, det_conf = detect_plate(frame)
    ...


    plate_img, det_conf = detect_plate(frame)

    if plate_img is None:
        continue

    texts, scores = read_plate(plate_img)
    plate, confidence = best_plate_candidate(texts, scores)

    if not plate:
        continue

    stable_plate = stabilizer.update(plate)

    if stable_plate:
        print("✅ STABLE PLATE CONFIRMED:", stable_plate)
        break

    # Optional: show frame
    cv2.imshow("Video Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
