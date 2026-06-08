# Trade Finance Intelligence Platform

## Overview

Trade Finance Intelligence Platform is a multimodal AI system for understanding, classifying, extracting, and searching trade-finance documents.

The platform combines:

* OCR (Tesseract)
* Layout-aware Document Understanding
* LayoutLMv3 Multimodal Classification
* Entity Extraction
* Semantic Search (RAG)
* FastAPI Deployment

The system processes common trade-finance documents such as:

* Commercial Invoices
* Bills of Lading
* Letters of Credit
* Packing Lists

---

# Architecture

```text
Trade Finance Documents
        |
        v
PDF Documents
        |
        v
Document Images
        |
        v
OCR Extraction
(Tesseract)
        |
        +---------------------+
        |                     |
        v                     v
OCR Text                Layout JSON
                     (Bounding Boxes)
        |                     |
        +----------+----------+
                   |
                   v
             LayoutLMv3
        Document Classification
                   |
                   v
          Entity Extraction
                   |
                   v
      ChromaDB Semantic Search
                   |
                   v
              FastAPI
```

---

# Demo Screenshots

## FastAPI Swagger Interface

![Swagger UI](docs/images/swagger_ui.png)

---

## LayoutLMv3 Classification + Entity Extraction

![Classification](docs/images/classification_demo.png)

Example Response:

```json
{
  "classification": {
    "doc_type": "commercial_invoice",
    "confidence": 0.9998
  },
  "entities": {
    "seller": "ABC Trading Ltd",
    "buyer": "XYZ Imports LLC",
    "amount": "1250000",
    "country": "Singapore",
    "goods": "Medical Devices"
  }
}
```

---

## Semantic Search API

![Semantic Search](docs/images/semantic_search_demo.png)

Example Query:

```json
{
  "query": "Find pharmaceutical supply invoices",
  "n_results": 5
}
```

---

## RAG Retrieval Example

![RAG Retrieval](docs/images/RAG_Terminal_Output.png)

Example semantic search query:

```text
Find pharmaceutical supply invoices
```

Example retrieval result:

```text
Rank 1
Doc Type: commercial_invoice

Rank 2
Doc Type: commercial_invoice

Rank 3
Doc Type: commercial_invoice
```

The system generates dense embeddings using Sentence Transformers and performs semantic retrieval using ChromaDB.

---

# Dataset

Synthetic trade-finance dataset generated using Python.

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

# Document Classification

## Model

```text
microsoft/layoutlmv3-base
```

## Input Modalities

* Document Images
* OCR Tokens
* Bounding Boxes

## Output

```json
{
  "doc_type": "letter_of_credit",
  "confidence": 0.9984
}
```

---

# Entity Extraction

The platform extracts key trade-finance fields including:

* Seller
* Buyer
* Invoice Number
* Amount
* Country
* Goods Description
* Letter of Credit Number
* Container Number
* Port of Loading
* Port of Discharge

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

# Semantic Search (RAG)

## Technology Stack

* Sentence Transformers
* all-MiniLM-L6-v2
* ChromaDB

## Example Queries

```text
Find pharmaceutical supply invoices

Find letters of credit issued by HSBC

Find documents involving Germany

Find shipments from Singapore

Find bills of lading containing industrial pumps
```

---

# Model Performance

## Baseline Model

TF-IDF + Logistic Regression

| Metric   | Value |
| -------- | ----- |
| Accuracy | 1.00  |

---

## Multimodal Model

LayoutLMv3

| Metric   | Value |
| -------- | ----- |
| Accuracy | 1.00  |

Training Configuration:

```text
3 Epochs
GPU: NVIDIA RTX 5000 Ada Generation
```

---

# API Endpoints

## Health Check

```http
GET /
```

---

## Process Document

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

Response:

```json
{
  "classification": {
    "doc_type": "commercial_invoice",
    "confidence": 0.999
  },
  "entities": {
    "seller": "...",
    "buyer": "...",
    "amount": "..."
  }
}
```

---

## Semantic Search

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

# Repository Structure

```text
trade-finance-intelligence/
│
├── docs/
│   └── images/
│
├── reports/
│
├── src/
│   ├── api/
│   ├── classification/
│   ├── extraction/
│   ├── ocr/
│   ├── rag/
│   └── data_generation/
│
├── requirements.txt
└── README.md
```

The repository contains source code only.

The following artifacts are intentionally excluded from source control because of size constraints:

* Synthetic trade-finance dataset
* OCR outputs
* Layout JSON files
* Trained LayoutLMv3 models
* ChromaDB vector indexes

All artifacts can be regenerated using the provided scripts.

---

# Installation

```bash
git clone https://github.com/Deepak-Sathyanarayanan/trade-finance-intelligence.git

cd trade-finance-intelligence

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

# Run API

```bash
uvicorn src.api.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

# Technology Stack

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

# Future Enhancements

* LayoutLMv3 Token Classification for NER
* LLM-based Compliance Summaries
* Ollama / Llama 3 Integration
* Docker Deployment
* Kubernetes Deployment
* AWS SageMaker Training
* AWS EKS Inference

---

# Author

**Deepak Sathyanarayanan**

Document AI • Multimodal AI • Trade Finance • Generative AI
