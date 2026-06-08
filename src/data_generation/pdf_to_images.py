from pdf2image import convert_from_path
from pathlib import Path

pdf_root = Path("data/raw")
img_root = Path("data/processed/images")

img_root.mkdir(parents=True, exist_ok=True)

pdfs = list(pdf_root.rglob("*.pdf"))

for pdf in pdfs:
    doc_type = pdf.parent.name

    output_dir = img_root / doc_type
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(str(pdf), dpi=300)

    img_file = output_dir / f"{pdf.stem}.png"

    pages[0].save(img_file, "PNG")

    print(img_file)