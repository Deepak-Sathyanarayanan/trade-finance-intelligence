import pandas as pd
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer


DB_DIR = "models/chroma_trade_docs"
COLLECTION_NAME = "trade_finance_docs"


def main():
    manifest = pd.read_csv("data/processed/manifest.csv")

    client = chromadb.PersistentClient(path=DB_DIR)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    docs = []
    ids = []
    metadatas = []

    for _, row in manifest.iterrows():
        ocr_path = Path(row["ocr_path"])

        if not ocr_path.exists():
            continue

        text = ocr_path.read_text(errors="ignore").strip()

        if not text:
            continue

        docs.append(text)
        ids.append(row["doc_id"])
        metadatas.append(
            {
                "doc_id": row["doc_id"],
                "doc_type": row["doc_type"],
                "image_path": row["image_path"],
                "ocr_path": row["ocr_path"],
                "layout_path": row["layout_path"],
            }
        )

    embeddings = model.encode(docs, show_progress_bar=True).tolist()

    collection.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Indexed {len(ids)} documents into {DB_DIR}")


if __name__ == "__main__":
    main()