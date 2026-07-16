import matplotlib.pyplot as plt
from pathlib import Path

from ..models.mapping import Mapping
from ..models.keyboard import KeyboardKey


def plot_keyboard_layout(mapping: Mapping, path: Path) -> None:
    x = []
    y = []
    labels = []
    colors = []

    for note_label, key_label in mapping.items():
        key = mapping.keys[key_label]
        x.append(key.x)
        y.append(key.y)
        labels.append(f"{note_label}\n{key.label}")
        colors.append("#4C72B0" if key.hand == "left" else "#55A868")

    plt.figure(figsize=(10, 4))
    plt.scatter(x, y, c=colors, s=400, edgecolors="black")

    for xi, yi, label in zip(x, y, labels):
        plt.text(xi, yi, label, ha="center", va="center", fontsize=8, color="white")

    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.title("Optimized QWERTY Piano Mapping")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
