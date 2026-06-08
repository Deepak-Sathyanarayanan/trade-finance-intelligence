from fastapi import FastAPI
from pydantic import BaseModel
from src.rag.search_index import search

from src.process_document import process_document

app = FastAPI(title="Trade Finance Intelligence API")

class SearchRequest(BaseModel):
    query: str
    n_results: int = 5

class DocumentRequest(BaseModel):
    image_path: str
    layout_path: str
    ocr_text_path: str


@app.get("/")
def health_check():
    return {"status": "ok", "service": "trade-finance-intelligence"}


@app.post("/process")
def process(req: DocumentRequest):
    result = process_document(
        req.image_path,
        req.layout_path,
        req.ocr_text_path,
    )
    return result

@app.post("/search")
def search_docs(req: SearchRequest):
    return {
        "query": req.query,
        "results": search(req.query, req.n_results),
    }