import matplotlib.pyplot as plt
from pathlib import Path
from typing import List


def plot_score_history(history: List[dict], path: Path) -> None:
    iterations = [entry["iteration"] for entry in history]
    best_scores = [entry["best_score"] for entry in history]

    plt.figure(figsize=(10, 4))
    plt.plot(iterations, best_scores, label="Best Score", color="#4C72B0")
    plt.xlabel("Iteration")
    plt.ylabel("Score")
    plt.title("Optimization Score Curve")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
