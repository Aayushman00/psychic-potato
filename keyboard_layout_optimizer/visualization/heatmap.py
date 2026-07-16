import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict


def plot_heatmap(values: Dict[str, float], path: Path) -> None:
    labels = list(values.keys())
    scores = list(values.values())

    plt.figure(figsize=(8, 4))
    plt.bar(labels, scores, color="#4C72B0")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Score")
    plt.title("Penalty Heatmap")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
