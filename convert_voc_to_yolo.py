import os
import xml.etree.ElementTree as ET
from pathlib import Path
from sklearn.model_selection import train_test_split
import shutil

# ---------------- CONFIG ----------------
DATASET_ROOT = "datasets/archive"
OUTPUT_ROOT = "yolo_dataset"
CLASS_ID = 0  # license_plate
IMAGE_EXTS = [".jpg", ".png"]

# ----------------------------------------

os.makedirs(OUTPUT_ROOT, exist_ok=True)

images_all = []

# Collect all image+xml pairs
for root, _, files in os.walk(DATASET_ROOT):
    for file in files:
        if file.lower().endswith(".xml"):
            xml_path = os.path.join(root, file)
            img_base = os.path.splitext(file)[0]

            for ext in IMAGE_EXTS:
                img_path = os.path.join(root, img_base + ext)
                if os.path.exists(img_path):
                    images_all.append((img_path, xml_path))
                    break

print(f"Found {len(images_all)} annotated images")

# Train/val split
train, val = train_test_split(images_all, test_size=0.2, random_state=42)

for split_name, split_data in [("train", train), ("val", val)]:
    img_out = Path(OUTPUT_ROOT) / "images" / split_name
    lbl_out = Path(OUTPUT_ROOT) / "labels" / split_name
    img_out.mkdir(parents=True, exist_ok=True)
    lbl_out.mkdir(parents=True, exist_ok=True)

    for img_path, xml_path in split_data:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        w = int(root.find("size/width").text)
        h = int(root.find("size/height").text)

        label_lines = []

        for obj in root.findall("object"):
            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)

            x_center = ((xmin + xmax) / 2) / w
            y_center = ((ymin + ymax) / 2) / h
            bw = (xmax - xmin) / w
            bh = (ymax - ymin) / h

            label_lines.append(
                f"{CLASS_ID} {x_center:.6f} {y_center:.6f} {bw:.6f} {bh:.6f}"
            )

        # Copy image
        shutil.copy(img_path, img_out / Path(img_path).name)

        # Write label
        label_file = lbl_out / (Path(img_path).stem + ".txt")
        with open(label_file, "w") as f:
            f.write("\n".join(label_lines))

print("✅ Conversion complete")
