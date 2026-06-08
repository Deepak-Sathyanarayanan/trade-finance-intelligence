import json
import re
import sys
from pathlib import Path

import torch
from PIL import Image
from transformers import LayoutLMv3ForSequenceClassification, LayoutLMv3Processor


MODEL_DIR = "models/layoutlmv3-trade-doc-classifier/final"


PATTERNS = {
    "invoice_number": r"Invoice Number:\s*(.+)",
    "seller": r"Seller:\s*(.+)",
    "buyer": r"Buyer:\s*(.+)",
    "amount": r"(?:Total Amount|Credit Amount):\s*USD\s*([\d,]+)",
    "country": r"(?:Country of Origin|Country):\s*(.+)",
    "goods": r"(?:Description of Goods|Goods Description|Goods):\s*(.+)",
    "lc_number": r"Letter of Credit Number:\s*(.+)",
    "container_number": r"Container Number:\s*(.+)",
    "port_loading": r"Port of Loading:\s*(.+)",
    "port_discharge": r"Port of Discharge:\s*(.+)",
}


def classify_document(image_path, layout_path):
    processor = LayoutLMv3Processor.from_pretrained(MODEL_DIR, apply_ocr=False)
    model = LayoutLMv3ForSequenceClassification.from_pretrained(MODEL_DIR)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    image = Image.open(image_path).convert("RGB")

    with open(layout_path, "r") as f:
        layout = json.load(f)

    words = [w["word"] for w in layout["words"]]
    boxes = [w["bbox"] for w in layout["words"]]

    encoding = processor(
        image,
        words,
        boxes=boxes,
        truncation=True,
        padding="max_length",
        max_length=512,
        return_tensors="pt",
    )

    encoding = {k: v.to(device) for k, v in encoding.items()}

    with torch.no_grad():
        outputs = model(**encoding)

    probs = torch.softmax(outputs.logits, dim=-1)[0]
    pred_id = torch.argmax(probs).item()

    return {
        "doc_type": model.config.id2label[pred_id],
        "confidence": round(probs[pred_id].item(), 4),
    }


def extract_entities(ocr_text_path):
    text = Path(ocr_text_path).read_text(errors="ignore")
    entities = {}

    for field, pattern in PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        entities[field] = match.group(1).strip() if match else None

    return entities


def process_document(image_path, layout_path, ocr_text_path):
    classification = classify_document(image_path, layout_path)
    entities = extract_entities(ocr_text_path)

    return {
        "classification": classification,
        "entities": entities,
        "inputs": {
            "image_path": image_path,
            "layout_path": layout_path,
            "ocr_text_path": ocr_text_path,
        },
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:")
        print(
            "python src/process_document.py "
            "<image_path> <layout_json_path> <ocr_text_path>"
        )
        sys.exit(1)

    result = process_document(sys.argv[1], sys.argv[2], sys.argv[3])
    print(json.dumps(result, indent=2))