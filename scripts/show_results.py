import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
import numpy as np  # type: ignore
from scripts.vars import *


def show(path, output_path, name):
    df = pd.read_csv(path)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 8))

    df["nodes"] = df["nodes"].astype(str)

    ax = sns.barplot(data=df, x="graph", y="mean", hue="nodes", palette="viridis")

    ax.set_yscale("log")

    for container in ax.containers:
        labels = [f"{val:.2f}" if val > 0 else "" for val in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3, fontsize=9, rotation=45)

    plt.title(name, fontsize=16)
    plt.xlabel("Graph Name", fontsize=12)
    plt.ylabel("Mean Time (log scale)", fontsize=12)
    plt.xticks(rotation=15, ha="right")
    plt.legend(title="Nodes", loc="upper left")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    # plt.show()


if __name__ == "__main__":
    path = OUTPUT_CSV
    show(path / "bfs_results.csv", path / "bfs.png", "BFS")
    show(path / "tc_results.csv", path / "tc.png", "TC")
    show(path / "pr_results.csv", path / "pr.png", "PR")
    show(path / "sssp_results.csv", path / "sssp.png", "SSSP")
