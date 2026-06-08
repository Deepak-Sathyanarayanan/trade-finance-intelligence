from reportlab.pdfgen import canvas
from faker import Faker
import os

fake = Faker()

OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf_path = f"{OUTPUT_DIR}/invoice_001.pdf"

c = canvas.Canvas(pdf_path)

c.setFont("Helvetica-Bold", 18)
c.drawString(180, 800, "COMMERCIAL INVOICE")

c.setFont("Helvetica", 12)

c.drawString(50, 750, f"Invoice Number: INV-10001")
c.drawString(50, 730, f"Seller: {fake.company()}")
c.drawString(50, 710, f"Buyer: {fake.company()}")

c.drawString(50, 670, "Goods: Medical Devices")
c.drawString(50, 650, "Quantity: 500")
c.drawString(50, 630, "Unit Price: USD 2500")
c.drawString(50, 610, "Total Amount: USD 1,250,000")

c.drawString(50, 570, "Country of Origin: Singapore")
c.drawString(50, 550, "Port of Loading: Singapore")
c.drawString(50, 530, "Port of Discharge: New York")

c.save()

print(f"Created {pdf_path}")