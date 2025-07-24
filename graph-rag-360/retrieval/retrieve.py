from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "docs"
QDRANT_URL = "http://localhost:6333"
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"

def retrieve(query, top_k=5):
    client = QdrantClient(QDRANT_URL)
    model = SentenceTransformer(EMBED_MODEL)
    query_vec = model.encode([query]).tolist()[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=top_k
    )
    return [hit.payload["text"] for hit in hits]

if __name__ == "__main__":
    results = retrieve("What is Qdrant?")
    for i, chunk in enumerate(results, 1):
        print(f"Chunk {i}: {chunk}\n")
