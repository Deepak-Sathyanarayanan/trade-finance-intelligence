from pathlib import Path
import json

import pytesseract
from PIL import Image

image_root = Path("data/processed/images")
layout_root = Path("data/layout")

layout_root.mkdir(parents=True, exist_ok=True)

for img_path in image_root.rglob("*.png"):
    doc_type = img_path.parent.name

    out_dir = layout_root / doc_type
    out_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(img_path)
    width, height = image.size

    ocr = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    words = []

    for i, text in enumerate(ocr["text"]):
        text = text.strip()

        if not text:
            continue

        left = int(ocr["left"][i])
        top = int(ocr["top"][i])
        w = int(ocr["width"][i])
        h = int(ocr["height"][i])

        # LayoutLM expects boxes normalized to 0-1000
        box = [
            int(1000 * left / width),
            int(1000 * top / height),
            int(1000 * (left + w) / width),
            int(1000 * (top + h) / height),
        ]

        words.append(
            {
                "word": text,
                "bbox": box,
                "raw_bbox": {
                    "left": left,
                    "top": top,
                    "width": w,
                    "height": h,
                },
            }
        )

    output = {
        "doc_id": img_path.stem,
        "doc_type": doc_type,
        "image_path": str(img_path),
        "image_width": width,
        "image_height": height,
        "words": words,
    }

    out_file = out_dir / f"{img_path.stem}.json"

    with open(out_file, "w") as f:
        json.dump(output, f, indent=2)

    print(out_file)