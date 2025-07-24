import requests
import os

def fetch_docs(url, out_path):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(response.text)

if __name__ == "__main__":
    url = "https://docs.qdrant.tech/"  # Example doc URL
    fetch_docs(url, "graph-rag-360/data/raw/docs.txt")