import os
from dotenv import load_dotenv

load_dotenv("graph-rag-360/.env")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-mpnet-base-v2")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
RAG_TOP_K = int(os.getenv("RAG_TOP_K", 5))
