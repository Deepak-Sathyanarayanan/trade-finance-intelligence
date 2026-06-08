import sys

import chromadb
from sentence_transformers import SentenceTransformer


DB_DIR = "models/chroma_trade_docs"
COLLECTION_NAME = "trade_finance_docs"


def search(query, n_results=5):
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    output = []

    for i in range(len(results["ids"][0])):
        output.append(
            {
                "rank": i + 1,
                "doc_id": results["ids"][0][i],
                "distance": results["distances"][0][i],
                "metadata": results["metadatas"][0][i],
                "preview": results["documents"][0][i][:500],
            }
        )

    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/rag/search_index.py '<query>'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    results = search(query)

    for r in results:
        print("\n" + "=" * 80)
        print(f"Rank: {r['rank']}")
        print(f"Doc ID: {r['doc_id']}")
        print(f"Doc Type: {r['metadata']['doc_type']}")
        print(f"Distance: {r['distance']}")
        print(r["preview"])