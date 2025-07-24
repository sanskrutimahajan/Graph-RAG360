import json
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "docs"
QDRANT_URL = "http://localhost:6333"
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"

client = QdrantClient(QDRANT_URL)
model = SentenceTransformer(EMBED_MODEL)

with open("graph-rag-360/data/processed/corpus.jsonl") as f:
    docs = [json.loads(line)["text"] for line in f]

embeddings = model.encode(docs).tolist()
payload = [{"text": doc} for doc in docs]

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={"size": len(embeddings[0]), "distance": "Cosine"}
)
client.upload_collection(
    collection_name=COLLECTION_NAME,
    vectors=embeddings,
    payload=payload
)
print("Indexed to Qdrant!")
