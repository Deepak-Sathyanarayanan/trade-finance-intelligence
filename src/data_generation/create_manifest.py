from pathlib import Path
import csv
import json

VALID_DOC_TYPES = {
    "commercial_invoice",
    "bill_of_lading",
    "letter_of_credit",
    "packing_list",
}

layout_root = Path("data/layout")
manifest_path = Path("data/processed/manifest.csv")
manifest_path.parent.mkdir(parents=True, exist_ok=True)

rows = []

for json_path in layout_root.rglob("*.json"):
    with open(json_path, "r") as f:
        item = json.load(f)

    doc_type = item["doc_type"]

    if doc_type not in VALID_DOC_TYPES:
        continue

    doc_id = item["doc_id"]

    rows.append({
        "doc_id": doc_id,
        "doc_type": doc_type,
        "image_path": item["image_path"],
        "ocr_path": f"data/ocr/{doc_type}/{doc_id}.txt",
        "layout_path": str(json_path),
    })

with open(manifest_path, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["doc_id", "doc_type", "image_path", "ocr_path", "layout_path"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {manifest_path} with {len(rows)} rows")