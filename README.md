# Trade Finance Intelligence Platform

## Overview

Trade Finance Intelligence Platform is a multimodal AI system for processing and understanding trade-finance documents.

The platform combines:

* OCR (Optical Character Recognition)
* Layout-aware document understanding
* LayoutLMv3 multimodal classification
* Entity extraction
* Semantic search (RAG)
* FastAPI deployment

The system processes common trade-finance documents including:

* Commercial Invoices
* Bills of Lading
* Letters of Credit
* Packing Lists

---

## Architecture

```text
PDF Documents
      |
      v
Document Images
      |
      v
OCR Extraction (Tesseract)
      |
      +------------------+
      |                  |
      v                  v
Layout JSON         OCR Text
(Bounding Boxes)    (Content)
      |                  |
      +--------+---------+
               |
               v
       LayoutLMv3
 Document Classification
               |
               v
      Entity Extraction
               |
               v
         ChromaDB
      Semantic Search
               |
               v
          FastAPI
```

---

## Dataset

Synthetic trade-finance dataset generated using Python.

Document Types:

| Document Type      | Count |
| ------------------ | ----- |
| Commercial Invoice | 100   |
| Bill of Lading     | 100   |
| Letter of Credit   | 100   |
| Packing List       | 100   |

Total Documents:

```text
400
```

Generated Assets:

```text
400 PDFs
400 Images
400 OCR Files
400 Layout Files
```

---

## Features

### Document Classification

Model:

```text
LayoutLMv3
```

Input:

* Document image
* OCR text
* Bounding boxes

Output:

```json
{
  "doc_type": "commercial_invoice",
  "confidence": 0.9958
}
```

---

### Entity Extraction

Extracted fields include:

```text
Seller
Buyer
Amount
Country
Goods
Invoice Number
LC Number
Container Number
Port of Loading
Port of Discharge
```

Example:

```json
{
  "seller": "Huff LLC",
  "buyer": "Buchanan-Mason",
  "amount": "226554",
  "country": "India",
  "goods": "Pharmaceutical Supplies"
}
```

---

### Semantic Search (RAG)

Technology:

```text
Sentence Transformers
ChromaDB
```

Example Queries:

```text
Find pharmaceutical supply invoices

Find letters of credit issued by HSBC

Find documents involving Germany
```

---

## Model Results

### Baseline Model

TF-IDF + Logistic Regression

| Metric   | Value |
| -------- | ----- |
| Accuracy | 1.00  |

### Multimodal Model

LayoutLMv3

| Metric   | Value |
| -------- | ----- |
| Accuracy | 1.00  |

Dataset:

```text
400 synthetic documents
```

---

## API Endpoints

### Health Check

```http
GET /
```

### Process Document

```http
POST /process
```

Request:

```json
{
  "image_path": "...",
  "layout_path": "...",
  "ocr_text_path": "..."
}
```

### Semantic Search

```http
POST /search
```

Request:

```json
{
  "query": "Find pharmaceutical invoices",
  "n_results": 5
}
```

---

## Installation

```bash
git clone <repo>

cd trade-finance-intelligence

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

## Run API

```bash
uvicorn src.api.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Technology Stack

* Python
* WSL2
* PyTorch
* Hugging Face Transformers
* LayoutLMv3
* Tesseract OCR
* ChromaDB
* Sentence Transformers
* FastAPI
* Uvicorn

---

## Future Enhancements

* Named Entity Recognition using LayoutLMv3 Token Classification
* PDF Upload Endpoint
* LLM-based Document Summarization
* Docker Deployment
* Kubernetes Deployment
* AWS SageMaker Training
* AWS EKS Inference
