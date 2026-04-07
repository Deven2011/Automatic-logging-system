from paddleocr import PaddleOCR
import re

# -------------------------------
# OCR INITIALIZATION
# -------------------------------
ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="en"
)

# -------------------------------
# CONSTANTS
# -------------------------------
MIN_OCR_CONF = 0.5

# Len-based sanity check (truck + car safe)
PLATE_REGEX = r"^[A-Z0-9]{6,12}$"

# -------------------------------
# HELPERS
# -------------------------------
def center_y(bbox):
    """
    Robust Y-center extractor.
    Handles all PaddleOCR bbox formats.
    """
    try:
        # Convert numpy array → list
        if hasattr(bbox, "tolist"):
            bbox = bbox.tolist()

        # Flat list: [x1,y1,x2,y2,...]
        if isinstance(bbox[0], (int, float)):
            ys = bbox[1::2]
            return sum(ys) / len(ys)

        # List of [x,y]
        ys = [pt[1] for pt in bbox if isinstance(pt, (list, tuple)) and len(pt) >= 2]
        return sum(ys) / len(ys)

    except Exception:
        return 0


# -------------------------------
# OCR READER
# -------------------------------
def read_plate(plate_image):
    """
    Returns:
        lines = [
            {
              "text": str,
              "score": float,
              "bbox": list
            }
        ]
    """
    result = ocr.predict(plate_image)

    if not result:
        return []

    data = result[0]

    texts = data.get("rec_texts", [])
    scores = data.get("rec_scores", [])
    boxes = data.get("rec_boxes", [])

    lines = []

    for text, score, box in zip(texts, scores, boxes):
        if score >= MIN_OCR_CONF and text.strip():
            lines.append({
                "text": text.strip().upper(),
                "score": float(score),
                "bbox": box
            })

    return lines


# -------------------------------
# MERGE + VALIDATE LOGIC
# -------------------------------
def merge_plate_lines(lines):
    if not lines:
        return None, "LOW"

    # Sort top → bottom using geometry
    lines = sorted(lines, key=lambda l: center_y(l["bbox"]))

    # Single-line (cars)
    if len(lines) == 1:
        final_plate = lines[0]["text"]
        avg_conf = lines[0]["score"]

    # Multi-line (trucks)
    else:
        top = lines[0]["text"]
        bottom = lines[1]["text"]

        # Ensure alphabetic part comes first
        if top.isdigit() and not bottom.isdigit():
            final_plate = bottom + top
        else:
            final_plate = top + bottom

        avg_conf = (lines[0]["score"] + lines[1]["score"]) / 2

    # Sanity validation (do NOT be overly strict)
    if not re.match(PLATE_REGEX, final_plate):
        return None, "LOW"

    if avg_conf >= 0.8:
        confidence = "HIGH"
    elif avg_conf >= 0.6:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return final_plate, confidence


# -------------------------------
# PUBLIC API
# -------------------------------
def recognize_plate(plate_image):
    lines = read_plate(plate_image)
    return merge_plate_lines(lines)


# -------------------------------
# DEBUG
# -------------------------------
if __name__ == "__main__":
    print("Plate OCR module loaded correctly")
