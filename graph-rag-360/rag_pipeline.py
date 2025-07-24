import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'graph-rag-360')))
from retrieval.retrieve import retrieve
from utils.config import OLLAMA_MODEL, RAG_TOP_K
import requests

print("Starting rag_pipeline.py...")
print("Using Ollama model:", OLLAMA_MODEL)

def ollama_chat(prompt, model=OLLAMA_MODEL):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    print("Ollama raw response:", response.text)  # Debug print
    try:
        data = response.json()
        if "response" in data:
            return data["response"]
        else:
            return f"No 'response' key. Full Ollama output: {data}"
    except Exception as e:
        return f"Error parsing Ollama response: {e}. Raw text: {response.text}"

def answer_query(query):
    chunks = retrieve(query, top_k=RAG_TOP_K)
    context = "\n".join(chunks)
    prompt = f"Answer the question using the context below. Cite relevant sentences.\nContext:\n{context}\nQuestion: {query}"
    return ollama_chat(prompt)

if __name__ == "__main__":
    print(answer_query("What is Qdrant?"))
