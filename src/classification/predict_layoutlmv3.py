import json
import sys
from pathlib import Path

import torch
from PIL import Image
from transformers import LayoutLMv3ForSequenceClassification, LayoutLMv3Processor


MODEL_DIR = "models/layoutlmv3-trade-doc-classifier/final"


def predict(image_path, layout_path):
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

    label = model.config.id2label[pred_id]
    confidence = probs[pred_id].item()

    print(f"Prediction: {label}")
    print(f"Confidence: {confidence:.4f}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("python src/classification/predict_layoutlmv3.py <image_path> <layout_json_path>")
        sys.exit(1)

    predict(sys.argv[1], sys.argv[2])