from pathlib import Path
import pytesseract
from PIL import Image

image_root = Path("data/processed/images")
ocr_root = Path("data/ocr")

ocr_root.mkdir(parents=True, exist_ok=True)

for img_path in image_root.rglob("*.png"):

    doc_type = img_path.parent.name

    out_dir = ocr_root / doc_type
    out_dir.mkdir(parents=True, exist_ok=True)

    text = pytesseract.image_to_string(Image.open(img_path))

    txt_file = out_dir / f"{img_path.stem}.txt"

    with open(txt_file, "w") as f:
        f.write(text)

    print(txt_file)