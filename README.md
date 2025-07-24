# Graph-RAG360

# Phase 1 — Baseline RAG Pipeline

## Overview
This project implements a minimal, working Retrieval-Augmented Generation (RAG) pipeline using vector search and local LLM inference. The pipeline is evaluated on a set of QA pairs about "Famous Inventions" and provides a baseline for future hybrid and knowledge-graph-augmented approaches.

---

## Features
- **Document Ingestion & Chunking:**
  - Ingests a document about famous inventions.
  - Cleans and splits the document into semantic chunks.
- **Vector Indexing & Retrieval:**
  - Embeds chunks using a HuggingFace model.
  - Stores embeddings in a local Qdrant vector database.
  - Retrieves top-k relevant chunks for a query.
- **LLM Answering:**
  - Uses Ollama to run a local LLM (e.g., Llama 3) for answer generation with citations.
- **Evaluation:**
  - Evaluates the pipeline on 10 QA pairs.
  - Saves results and (optionally) computes RAGAS metrics.

---

## Project Structure
```
graph-rag-360/
├── app/
├── data/
│   ├── qa/
│   │   └── eval_set.csv         # 10 QA pairs (Famous Inventions)
│   ├── processed/
│   │   └── corpus.jsonl         # Chunked document
│   └── raw/
│       └── docs.txt             # Source document
├── eval/
│   ├── run_ragas.py             # Evaluation script
├── ingest/
│   ├── clean_chunk.py           # Chunking script
├── retrieval/
│   ├── index_qdrant.py          # Indexing script
│   ├── retrieve.py              # Retrieval script
├── utils/
│   └── config.py                # Loads environment variables
├── rag_pipeline.py              # Main RAG pipeline
├── requirements.txt
├── .env / .env.example
├── Dockerfile
└── eval_results_baseline.csv    # Evaluation results
```

---

## Setup
1. **Clone the repo and install dependencies:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Graph-RAG360.git
   cd Graph-RAG360
   pip install -r requirements.txt
   ```
2. **Set up environment variables:**
   - Edit `.env` (see `.env.example`):
     ```
     OLLAMA_MODEL=llama3
     QDRANT_URL=http://localhost:6333
     EMBED_MODEL=sentence-transformers/all-mpnet-base-v2
     RAG_TOP_K=5
     ```
3. **Start Qdrant:**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```
4. **Start Ollama and pull a model:**
   ```bash
   ollama serve
   ollama pull llama3
   ```

---

## Usage
1. **Prepare the data:**
   - Edit `data/raw/docs.txt` with your document (default: famous inventions).
   - Run:
     ```bash
     python3 ingest/clean_chunk.py
     ```
2. **Index the data:**
   ```bash
   python3 retrieval/index_qdrant.py
   ```
3. **Run the evaluation:**
   ```bash
   python3 eval/run_ragas.py
   ```
4. **View results:**
   - Check `eval_results_baseline.csv` for answers and metrics.

---

## Evaluation
- The pipeline is evaluated on 10 QA pairs about famous inventions.
- Results are saved in `eval_results_baseline.csv`.
- (Optional) RAGAS metrics are computed and printed in the terminal.

---

## Next Steps
- Use this baseline to compare with future hybrid and knowledge-graph-augmented pipelines.
- For Phase 2, see the project wiki or next branch.

---

## License
MIT
