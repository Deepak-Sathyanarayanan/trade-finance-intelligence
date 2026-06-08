import re
import sys
from pathlib import Path


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


def extract_entities(text):
    results = {}

    for field, pattern in PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        results[field] = match.group(1).strip() if match else None

    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/extraction/extract_entities.py <ocr_text_file>")
        sys.exit(1)

    text_path = Path(sys.argv[1])
    text = text_path.read_text(errors="ignore")

    entities = extract_entities(text)

    for k, v in entities.items():
        print(f"{k}: {v}")