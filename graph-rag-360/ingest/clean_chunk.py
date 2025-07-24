import os
import json
import re

def clean_text(text):
    # Remove extra whitespace and normalize newlines
    return re.sub(r'\s+', ' ', text).strip()

def split_sentences(text):
    # Simple sentence splitter (can use nltk for more accuracy)
    return re.split(r'(?<=[.!?]) +', text)

def chunk_text(sentences, window_size=5):
    chunks = [' '.join(sentences[i:i+window_size]) for i in range(0, len(sentences), window_size)]
    return [chunk.strip() for chunk in chunks if chunk.strip()]

if __name__ == "__main__":
    in_path = "graph-rag-360/data/raw/docs.txt"
    out_path = "graph-rag-360/data/processed/corpus.jsonl"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        with open(in_path) as f:
            text = f.read()
        clean = clean_text(text)
        sentences = split_sentences(clean)
        chunks = chunk_text(sentences)
        with open(out_path, "w") as f:
            for chunk in chunks:
                f.write(json.dumps({"text": chunk}) + "\n")
        print(f"Chunked {len(chunks)} pieces and saved to {out_path}")
    except Exception as e:
        print(f"Error: {e}")