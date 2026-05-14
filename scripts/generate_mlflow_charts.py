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

x = np.arange(len(short_names))
w = 0.25

def save_bar_chart(title, p_col, r_col, f_col, filename):
    """Helper: save 4-run P/R/F1 bar chart."""
    fig, ax = plt.subplots(figsize=(9, 5))
    p = runs_df[p_col].fillna(0).values
    r = runs_df[r_col].fillna(0).values
    f = runs_df[f_col].fillna(0).values
    b1 = ax.bar(x - w, p, w, label="Precision", color="#4A90D9")
    b2 = ax.bar(x, r, w, label="Recall", color="#67B26F")
    b3 = ax.bar(x + w, f, w, label="F1", color="#F5A623")
    ax.set_ylabel("Score")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, fontsize=10)
    ax.legend(loc="upper right")
    ax.set_ylim(0, 1)
    for bar in b1 + b2 + b3:
        if bar.get_height() > 0.01:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{outdir}/{filename}", dpi=150)
    plt.close()
    print(f"Saved: {filename}")

# Chart 1: Get Real
save_bar_chart("Get Real 0.2 — Metrics Comparison",
               "metrics.get_real_precision", "metrics.get_real_recall",
               "metrics.get_real_f1", "chart_get_real.png")

# Chart 2: Mashboot
save_bar_chart("Mashboot — Metrics Comparison",
               "metrics.mashboot_precision", "metrics.mashboot_recall",
               "metrics.mashboot_f1", "chart_mashboot.png")

# Chart 3: Space Fractions
save_bar_chart("Space Fractions — Metrics Comparison",
               "metrics.space_fractions_precision", "metrics.space_fractions_recall",
               "metrics.space_fractions_f1", "chart_space_fractions.png")

# Chart 4: Inventory
save_bar_chart("Inventory — Metrics Comparison",
               "metrics.inventory_precision", "metrics.inventory_recall",
               "metrics.inventory_f1", "chart_inventory.png")

# Chart 5: Gamma J
save_bar_chart("Gamma J — Metrics Comparison",
               "metrics.gamma_j_precision", "metrics.gamma_j_recall",
               "metrics.gamma_j_f1", "chart_gamma_j.png")

# Chart 6: All 5 datasets F1 (best run)
fig, ax = plt.subplots(figsize=(10, 5))
datasets = ["Get Real", "Mashboot", "Space Frac.", "Inventory", "Gamma J"]
metric_keys = ["get_real_f1", "mashboot_f1", "space_fractions_f1", "inventory_f1", "gamma_j_f1"]
# Only Run 3 (Agent Exhaustive) has all 5 dataset metrics
run3_row = runs_df[runs_df["tags.mlflow.runName"].str.contains("Agent Exhaustive", na=False)]
if len(run3_row) > 0 and "metrics.space_fractions_f1" in run3_row.columns:
    vals = [run3_row[f"metrics.{k}"].values[0] for k in metric_keys]
    bars = ax.barh(datasets, vals, color=["#4A90D9", "#67B26F", "#F5A623", "#E05555", "#8B5CF6"], height=0.5)
    ax.set_xlabel("F1 Score")
    ax.set_title("Agent Exhaustive (r1-v5) — F1 Across 5 PURE Datasets")
    ax.set_xlim(0, 1)
    for bar in bars:
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f"{bar.get_width():.2f}", ha="left", va="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{outdir}/chart_5dataset_f1.png", dpi=150)
    plt.close()
    print("Saved: chart_5dataset_f1.png")
else:
    print("Skipping 5-dataset chart (metrics not logged yet)")

# Chart 7: Type accuracy
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
    print("Saved: chart_type_accuracy.png")

print("\nAll charts saved successfully.")
