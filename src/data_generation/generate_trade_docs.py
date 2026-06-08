import csv
import os
import random
from datetime import timedelta

from faker import Faker
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

fake = Faker()

DOC_TYPES = [
    "commercial_invoice",
    "bill_of_lading",
    "letter_of_credit",
    "packing_list",
]

GOODS = [
    "Semiconductor Components",
    "Medical Devices",
    "Industrial Pumps",
    "Automotive Parts",
    "Textile Machinery",
    "Telecom Equipment",
    "Pharmaceutical Supplies",
    "Aerospace Fasteners",
]

COUNTRIES = [
    "Singapore",
    "United States",
    "Germany",
    "India",
    "Japan",
    "United Kingdom",
    "South Korea",
    "Netherlands",
]

BANKS = [
    "JPMorgan Chase Bank",
    "Citibank N.A.",
    "HSBC Bank",
    "Standard Chartered Bank",
    "Deutsche Bank",
    "Bank of America",
]


def draw_lines(c, title, lines):
    width, height = LETTER
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, title)

    y = height - 120
    c.setFont("Helvetica", 11)

    for line in lines:
        c.drawString(72, y, line)
        y -= 22

    c.showPage()
    c.save()


def make_common_fields():
    amount = random.randint(10_000, 2_500_000)
    quantity = random.randint(10, 5000)
    unit_price = round(amount / quantity, 2)

    return {
        "seller": fake.company(),
        "buyer": fake.company(),
        "goods": random.choice(GOODS),
        "country": random.choice(COUNTRIES),
        "amount": amount,
        "currency": "USD",
        "quantity": quantity,
        "unit_price": unit_price,
        "invoice_no": f"INV-{random.randint(10000, 99999)}",
        "date": fake.date_between(start_date="-90d", end_date="today").isoformat(),
        "port_loading": random.choice(["Singapore", "Hamburg", "Mumbai", "Tokyo", "Rotterdam"]),
        "port_discharge": random.choice(["New York", "Los Angeles", "London", "Dubai", "Busan"]),
        "vessel": fake.word().title() + " Star",
        "container_no": f"CONT{random.randint(1000000, 9999999)}",
        "lc_no": f"LC-{random.randint(100000, 999999)}",
        "issuing_bank": random.choice(BANKS),
        "beneficiary_bank": random.choice(BANKS),
        "expiry_date": (fake.date_between(start_date="+30d", end_date="+180d")).isoformat(),
    }


def commercial_invoice(c, f):
    lines = [
        f"Invoice Number: {f['invoice_no']}",
        f"Invoice Date: {f['date']}",
        f"Seller: {f['seller']}",
        f"Buyer: {f['buyer']}",
        "",
        f"Description of Goods: {f['goods']}",
        f"Quantity: {f['quantity']}",
        f"Unit Price: {f['currency']} {f['unit_price']}",
        f"Total Amount: {f['currency']} {f['amount']:,}",
        "",
        f"Country of Origin: {f['country']}",
        f"Port of Loading: {f['port_loading']}",
        f"Port of Discharge: {f['port_discharge']}",
    ]
    draw_lines(c, "COMMERCIAL INVOICE", lines)


def bill_of_lading(c, f):
    lines = [
        f"Bill of Lading Number: BL-{random.randint(100000, 999999)}",
        f"Shipper: {f['seller']}",
        f"Consignee: {f['buyer']}",
        f"Notify Party: {fake.company()}",
        "",
        f"Vessel: {f['vessel']}",
        f"Container Number: {f['container_no']}",
        f"Port of Loading: {f['port_loading']}",
        f"Port of Discharge: {f['port_discharge']}",
        "",
        f"Goods Description: {f['goods']}",
        f"Number of Packages: {random.randint(1, 200)}",
        f"Gross Weight: {random.randint(100, 25000)} KG",
    ]
    draw_lines(c, "BILL OF LADING", lines)


def letter_of_credit(c, f):
    lines = [
        f"Letter of Credit Number: {f['lc_no']}",
        f"Issuing Bank: {f['issuing_bank']}",
        f"Beneficiary Bank: {f['beneficiary_bank']}",
        f"Applicant: {f['buyer']}",
        f"Beneficiary: {f['seller']}",
        "",
        f"Credit Amount: {f['currency']} {f['amount']:,}",
        f"Expiry Date: {f['expiry_date']}",
        f"Country: {f['country']}",
        "",
        f"Documents Required:",
        "1. Signed Commercial Invoice",
        "2. Full Set of Bills of Lading",
        "3. Packing List",
        "4. Certificate of Origin",
    ]
    draw_lines(c, "LETTER OF CREDIT", lines)


def packing_list(c, f):
    lines = [
        f"Packing List Number: PL-{random.randint(100000, 999999)}",
        f"Seller: {f['seller']}",
        f"Buyer: {f['buyer']}",
        "",
        f"Goods: {f['goods']}",
        f"Quantity: {f['quantity']}",
        f"Number of Cartons: {random.randint(5, 300)}",
        f"Gross Weight: {random.randint(100, 25000)} KG",
        f"Net Weight: {random.randint(80, 22000)} KG",
        "",
        f"Country of Origin: {f['country']}",
        f"Container Number: {f['container_no']}",
    ]
    draw_lines(c, "PACKING LIST", lines)


GENERATORS = {
    "commercial_invoice": commercial_invoice,
    "bill_of_lading": bill_of_lading,
    "letter_of_credit": letter_of_credit,
    "packing_list": packing_list,
}


def main(n_per_type=100):
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/labels", exist_ok=True)

    label_path = "data/labels/document_labels.csv"

    with open(label_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "doc_id",
                "doc_type",
                "pdf_path",
                "seller",
                "buyer",
                "amount",
                "currency",
                "country",
                "goods",
            ],
        )
        writer.writeheader()

        for doc_type in DOC_TYPES:
            out_dir = f"data/raw/{doc_type}"
            os.makedirs(out_dir, exist_ok=True)

            for i in range(1, n_per_type + 1):
                fields = make_common_fields()
                doc_id = f"{doc_type}_{i:03d}"
                pdf_path = f"{out_dir}/{doc_id}.pdf"

                c = canvas.Canvas(pdf_path, pagesize=LETTER)
                GENERATORS[doc_type](c, fields)

                writer.writerow(
                    {
                        "doc_id": doc_id,
                        "doc_type": doc_type,
                        "pdf_path": pdf_path,
                        "seller": fields["seller"],
                        "buyer": fields["buyer"],
                        "amount": fields["amount"],
                        "currency": fields["currency"],
                        "country": fields["country"],
                        "goods": fields["goods"],
                    }
                )

    print(f"Generated {len(DOC_TYPES) * n_per_type} PDFs")
    print(f"Labels saved to {label_path}")


if __name__ == "__main__":
    main(n_per_type=100)