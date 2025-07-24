import sys
import os
import time
print("Starting run_ragas.py...")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'graph-rag-360')))
from rag_pipeline import answer_query
import pandas as pd

# RAGAS imports
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall, context_relevancy
from ragas import evaluate

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'qa', 'eval_set.csv'))
df = pd.read_csv(csv_path)
results = []
for _, row in df.iterrows():
    print(f"\nQuestion: {row['question']}")
    pred = answer_query(row["question"])
    print(f"Ollama answer: {pred}")
    results.append({"question": row["question"], "ground_truth": row["answer"], "prediction": pred})
    time.sleep(1)  # Add delay between requests

output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'eval_results_baseline.csv'))
eval_df = pd.DataFrame(results)
eval_df.to_csv(output_path, index=False)
print(f"Saved eval results to {output_path}")

# Prepare for RAGAS
ragas_df = pd.DataFrame({
    "question": eval_df["question"],
    "answer": eval_df["prediction"],
    "ground_truth": eval_df["ground_truth"],
    "contexts": [[] for _ in range(len(eval_df))]  # If you want to add retrieved chunks, put them here
})

# Compute RAGAS metrics
metrics = [faithfulness, answer_relevancy, context_precision, context_recall, context_relevancy]
ragas_results = evaluate(ragas_df, metrics)
print("\nRAGAS Metrics:")
print(ragas_results)
print("\nAverages:")
print(ragas_results.mean())
