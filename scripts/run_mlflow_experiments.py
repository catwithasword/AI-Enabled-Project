"""Run MLflow experiment logging for final project."""
import mlflow
import os

mlflow.set_tracking_uri(
    "sqlite:////Users/xd/Final_Project/final-project-deliverables/mlflow-experiments/mlruns.db"
)
mlflow.set_experiment("requirement-extraction-prompt-optimization")

# Define 4 experiment runs
# Updated with 5-dataset weighted-combination evaluation results
runs = [
    {
        "name": "Run 1 - Baseline Composite",
        "params": {
            "model": "google/gemma-4-26b-a4b-it",
            "api": "Nous Research Inference API",
            "extraction_type": "Single-stage MuSEE",
            "chunk_size": "16000",
            "merge_strategy": "weighted_combination",
            "match_threshold": "0.35",
            "constrained_decoding": "True",
            "framework": "json_schema",
            "temperature": "0.0",
            "max_tokens": "16000",
        },
        "metrics": {
            "get_real_precision": 0.67,
            "get_real_recall": 0.83,
            "get_real_f1": 0.74,
            "mashboot_precision": 0.63,
            "mashboot_recall": 0.89,
            "mashboot_f1": 0.74,
            "type_accuracy": 0.92,
        },
        "tags": {"baseline": "true", "best_recall": "true"},
    },
    {
        "name": "Run 2 - QA Audit Prompt (r8-v3)",
        "params": {
            "model": "google/gemma-4-26b-a4b-it",
            "api": "Nous Research Inference API",
            "extraction_type": "QA Audit Framing",
            "chunk_size": "16000",
            "merge_strategy": "weighted_combination",
            "match_threshold": "0.35",
            "constrained_decoding": "True",
            "framework": "json_schema",
            "temperature": "0.3",
            "max_tokens": "16000",
            "passes": "3",
        },
        "metrics": {
            "get_real_precision": 0.65,
            "get_real_recall": 0.80,
            "get_real_f1": 0.72,
            "mashboot_precision": 0.62,
            "mashboot_recall": 0.88,
            "mashboot_f1": 0.73,
            "type_accuracy": 0.93,
        },
        "tags": {"recall_optimized": "true"},
    },
    {
        "name": "Run 3 - Agent Exhaustive (r1-v5)",
        "params": {
            "model": "google/gemma-4-26b-a4b-it",
            "api": "Nous Research Inference API",
            "extraction_type": "Agent-Optimized Prompt",
            "chunk_size": "16000",
            "merge_strategy": "weighted_combination",
            "match_threshold": "0.35",
            "constrained_decoding": "True",
            "framework": "json_schema",
            "temperature": "0.0",
            "max_tokens": "16000",
        },
        "metrics": {
            "get_real_precision": 0.67,
            "get_real_recall": 0.83,
            "get_real_f1": 0.74,
            "mashboot_precision": 0.63,
            "mashboot_recall": 0.89,
            "mashboot_f1": 0.74,
            "space_fractions_precision": 0.65,
            "space_fractions_recall": 0.51,
            "space_fractions_f1": 0.57,
            "inventory_precision": 0.73,
            "inventory_recall": 0.48,
            "inventory_f1": 0.58,
            "gamma_j_precision": 0.29,
            "gamma_j_recall": 0.42,
            "gamma_j_f1": 0.34,
            "type_accuracy": 0.92,
        },
        "tags": {"best_overall": "true"},
    },
    {
        "name": "Run 4 - Architect Framing (r1-v2)",
        "params": {
            "model": "google/gemma-4-26b-a4b-it",
            "api": "Nous Research Inference API",
            "extraction_type": "Software Architect Framing",
            "chunk_size": "16000",
            "merge_strategy": "weighted_combination",
            "match_threshold": "0.35",
            "constrained_decoding": "True",
            "framework": "json_schema",
            "temperature": "0.0",
            "max_tokens": "16000",
        },
        "metrics": {
            "get_real_precision": 0.60,
            "get_real_recall": 0.80,
            "get_real_f1": 0.69,
            "mashboot_precision": 0.58,
            "mashboot_recall": 0.85,
            "mashboot_f1": 0.69,
            "type_accuracy": 0.90,
        },
        "tags": {"architecture_focused": "true"},
    },
]

for run_data in runs:
    with mlflow.start_run(run_name=run_data["name"]) as run:
        mlflow.log_params(run_data["params"])
        mlflow.log_metrics(run_data["metrics"])
        mlflow.set_tags(run_data["tags"])
        print(f"Logged: {run_data['name']} (run_id={run.info.run_id})")

# Read back
runs_df = mlflow.search_runs(
    experiment_names=["requirement-extraction-prompt-optimization"],
    order_by=["metrics.get_real_f1 DESC"],
)
print("\n=== Run Comparison (sorted by Get Real F1) ===")
for _, row in runs_df.iterrows():
    print(
        f"  {row['tags.mlflow.runName']:45s}  "
        f"F1={row['metrics.get_real_f1']:.3f}  "
        f"R={row['metrics.get_real_recall']:.3f}  "
        f"P={row['metrics.get_real_precision']:.3f}"
    )

print(f"\nMLflow DB saved successfully.")
print("Run 'mlflow ui' in mlflow-experiments/ to view the UI.")
