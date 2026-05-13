"""Generate MLflow comparison charts as PNGs for submission."""
import mlflow
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

mlflow.set_tracking_uri(
    "sqlite:////Users/xd/Final_Project/final-project-deliverables/mlflow-experiments/mlruns.db"
)

runs_df = mlflow.search_runs(
    experiment_names=["requirement-extraction-prompt-optimization"],
    order_by=["metrics.get_real_f1 DESC"],
)

runs_df = runs_df.sort_values("metrics.get_real_f1", ascending=False).reset_index(drop=True)
names = [r["tags.mlflow.runName"] for _, r in runs_df.iterrows()]
# Short names for display
short_names = ["Baseline\nComposite", "QA Audit\n(r8-v3)", "Agent Exhaustive\n(r1-v5)", "Architect\n(r1-v2)"]

outdir = "/Users/xd/Final_Project/final-project-deliverables/mlflow-experiments/screenshots"
plt.rcParams.update({"font.size": 11, "axes.titlesize": 13, "axes.titleweight": "bold"})

# Chart 1: Get Real metrics
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(short_names))
w = 0.25
p = runs_df["metrics.get_real_precision"].values
r = runs_df["metrics.get_real_recall"].values
f = runs_df["metrics.get_real_f1"].values
b1 = ax.bar(x - w, p, w, label="Precision", color="#4A90D9")
b2 = ax.bar(x, r, w, label="Recall", color="#67B26F")
b3 = ax.bar(x + w, f, w, label="F1", color="#F5A623")
ax.set_ylabel("Score")
ax.set_title("Get Real 0.2 — Metrics Comparison")
ax.set_xticks(x)
ax.set_xticklabels(short_names, fontsize=10)
ax.legend(loc="upper right")
ax.set_ylim(0, 1)
for bar in b1 + b2 + b3:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
plt.savefig(f"{outdir}/chart_get_real.png", dpi=150)
plt.close()
print(f"Saved: chart_get_real.png")

# Chart 2: Mashboot metrics (weighted combination)
fig, ax = plt.subplots(figsize=(9, 5))
mp = runs_df["metrics.mashboot_precision"].values
mr = runs_df["metrics.mashboot_recall"].values
mf = runs_df["metrics.mashboot_f1"].values
b1 = ax.bar(x - w, mp, w, label="Precision", color="#4A90D9")
b2 = ax.bar(x, mr, w, label="Recall", color="#67B26F")
b3 = ax.bar(x + w, mf, w, label="F1", color="#F5A623")
ax.set_ylabel("Score")
ax.set_title("Mashboot (Weighted Combination) — Metrics Comparison")
ax.set_xticks(x)
ax.set_xticklabels(short_names, fontsize=10)
ax.legend(loc="upper right")
ax.set_ylim(0, 1)
for bar in b1 + b2 + b3:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
plt.savefig(f"{outdir}/chart_mashboot.png", dpi=150)
plt.close()
print(f"Saved: chart_mashboot.png")

# Chart 3: All 5 datasets F1 (new - replaces union recall)
fig, ax = plt.subplots(figsize=(10, 5))
datasets = ["Get Real", "Mashboot", "Space Frac.", "Inventory", "Gamma J"]
metric_keys = ["get_real_f1", "mashboot_f1", "space_fractions_f1", "inventory_f1", "gamma_j_f1"]
# Only Run 3 has all 5 dataset metrics
run3_row = runs_df[runs_df["tags.mlflow.runName"].str.contains("Agent Exhaustive", na=False)]
if len(run3_row) > 0 and "metrics.space_fractions_f1" in run3_row.columns:
    vals = [run3_row[f"metrics.{k}"].values[0] for k in metric_keys]
    bars = ax.barh(datasets, vals, color=["#4A90D9", "#67B26F", "#F5A623", "#E05555", "#8B5CF6"], height=0.5)
    ax.set_xlabel("F1 Score")
    ax.set_title("3-Run Agent Exhaustive — F1 Across 5 PURE Datasets")
    ax.set_xlim(0, 1)
    for bar in bars:
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f"{bar.get_width():.2f}", ha="left", va="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{outdir}/chart_5dataset_f1.png", dpi=150)
    plt.close()
    print(f"Saved: chart_5dataset_f1.png")
else:
    print("Skipping 5-dataset chart (metrics not logged yet)")

# Chart 4: Type accuracy (unchanged logic, different column name not needed - uses generic)
fig, ax = plt.subplots(figsize=(8, 4))
colors = ["#4A90D9", "#67B26F", "#F5A623", "#E05555"]
if "metrics.type_accuracy" in runs_df.columns:
    ta = runs_df["metrics.type_accuracy"].values
    bars = ax.barh(short_names[::-1], ta[::-1], color=colors[::-1], height=0.5)
    ax.set_xlabel("Accuracy")
    ax.set_title("Type Classification Accuracy (FR vs NFR)")
    ax.set_xlim(0.9, 1.0)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    for bar in bars:
        ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                f"{bar.get_width()*100:.1f}%", ha="left", va="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{outdir}/chart_type_accuracy.png", dpi=150)
    plt.close()
    print(f"Saved: chart_type_accuracy.png")

print("\nAll charts saved successfully.")
