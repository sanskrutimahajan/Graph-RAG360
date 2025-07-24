# Graph-RAG360

RAG Pipeline

## Overview
This project implements a, working Retrieval-Augmented Generation (RAG) pipeline using vector search and local LLM inference. The pipeline is evaluated on a set of QA pairs about "Famous Inventions" and provides a baseline for future hybrid and knowledge-graph-augmented approaches.

---
- **Ingests & chunks** a document (“Famous Inventions” by default).
- **Embeds & retrieves** chunks via a local **Qdrant** vector DB.
- **Extracts (subject, predicate, object) triplets** from those chunks using an LLM and **loads them into Neo4j** as a Knowledge Graph.
- **Retrieves from the KG** (Cypher query) to capture connected facts.
- **Combines KG facts + vector chunks** as context for a local LLM (Ollama/Llama 3) to answer with citations.
- **Evaluates** 10 QA pairs and (optionally) computes **RAGAS** metrics, saving results for baseline comparison.
---
## Features

### Document Ingestion & Chunking
- Cleans and splits a source document into semantic chunks.
- Output: `data/processed/corpus.jsonl`.

### Vector Indexing & Retrieval
- Embeds chunks with a HuggingFace model.
- Stores embeddings in **Qdrant**.
- Retrieves top‑K chunks per query.

### Triplet Extraction & Knowledge Graph
- LLM generates `(subject, predicate, object)` triples for each chunk.
- Loads them into **Neo4j** with Cypher `MERGE` (deduplicated nodes/edges).
- `kg_retrieve(query)` grabs relevant nodes/edges (2‑hop neighborhood by default).

### Hybrid Context Assembly
- Merge KG facts and vector chunks.
- (Optional later) Cross‑encoder rerank.

### LLM Answering
- Local LLM via **Ollama** (e.g., `llama3`) generates the final answer + citations.

### Evaluation
- Evaluate on **10 QA pairs** (`data/qa/eval_set.csv`).
- Save results to `eval_results_baseline.csv`.
- Optionally run **RAGAS** (faithfulness, answer relevancy).
---

## Project Structure
```
graph-rag-360/
├── app/ # (optional UI/API later)
├── data/
│ ├── qa/
│ │ └── eval_set.csv # 10 QA pairs (Famous Inventions)
│ ├── processed/
│ │ ├── corpus.jsonl # Chunked document
│ │ └── triples.jsonl # (S,P,O) triples
│ └── raw/
│ └── docs.txt # Source document
├── eval/
│ └── run_ragas.py # Evaluation script (baseline metrics)
├── ingest/
│ └── clean_chunk.py # Chunking script
├── kg/
│ ├── extract_triplets.py # LLM-based triple extraction
│ ├── load_neo4j.py # Cypher MERGE loader
│ ├── kg_retrieve.py # Graph retrieval helper
│ └── prompts/
│ └── triplet_prompt.txt # Prompt template
├── retrieval/
│ ├── index_qdrant.py # Build vector index
│ └── retrieve.py # Vector retrieval API
├── utils/
│ └── config.py # Loads env vars / shared config
├── rag_pipeline.py   # Main end-to-end pipeline
├── requirements.txt
├── .env / .env.example
├── Dockerfile
└── eval_results_baseline.csv 

yaml
Copy
Edit

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

Metric	Baseline Vector+KG	Notes
Faithfulness	0.81	
Relevancy	0.83
---

## License
MIT
