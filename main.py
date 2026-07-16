import csv
import json
import os
import time
from pathlib import Path
from typing import Dict, List

import yaml

from keyboard_layout_optimizer.models.keyboard import KeyboardKey
from keyboard_layout_optimizer.models.mapping import baseline_sequential_mapping
from keyboard_layout_optimizer.models.piano import build_piano_notes
from keyboard_layout_optimizer.optimizer.annealing import SimulatedAnnealing
from keyboard_layout_optimizer.optimizer.objective import Objective, default_penalty_list
from keyboard_layout_optimizer.visualization.keyboard_plot import plot_keyboard_layout
from keyboard_layout_optimizer.visualization.score_plot import plot_score_history


def load_config(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_keyboard_layout() -> List[KeyboardKey]:
    rows = [
        (1, 0.0, "`1234567890-="),
        (2, 0.5, "QWERTYUIOP[]"),
        (3, 1.0, "ASDFGHJKL;'"),
        (4, 1.5, "ZXCVBNM,./"),
    ]
    hand_assignment = {
        "Q": "left",
        "W": "left",
        "E": "left",
        "R": "left",
        "T": "left",
        "Y": "right",
        "U": "right",
        "I": "right",
        "O": "right",
        "P": "right",
        "A": "left",
        "S": "left",
        "D": "left",
        "F": "left",
        "G": "left",
        "H": "right",
        "J": "right",
        "K": "right",
        "L": "right",
        ";": "right",
        "Z": "left",
        "X": "left",
        "C": "left",
        "V": "left",
        "B": "left",
        "N": "right",
        "M": "right",
        ",": "right",
        ".": "right",
        "/": "right",
    }
    finger_assignment = {
        "Q": "pinky",
        "W": "ring",
        "E": "middle",
        "R": "index",
        "T": "index",
        "Y": "index",
        "U": "middle",
        "I": "ring",
        "O": "pinky",
        "P": "pinky",
        "A": "pinky",
        "S": "ring",
        "D": "middle",
        "F": "index",
        "G": "index",
        "H": "index",
        "J": "middle",
        "K": "ring",
        "L": "pinky",
        ";": "pinky",
        "Z": "pinky",
        "X": "ring",
        "C": "middle",
        "V": "index",
        "B": "index",
        "N": "index",
        "M": "middle",
        ",": "ring",
        ".": "pinky",
        "/": "pinky",
    }
    keys: List[KeyboardKey] = []
    for row, y, labels in rows:
        for col, label in enumerate(labels):
            keys.append(
                KeyboardKey(
                    label=label,
                    row=row,
                    x=col + (0.0 if row == 1 else 0.5),
                    y=y,
                    hand=hand_assignment.get(label, "left"),
                    finger=finger_assignment.get(label, "index"),
                    modifier=False,
                )
            )
    return keys


def export_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def export_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_markdown(path: Path, content: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def score_report(result, objective, mapping) -> str:
    breakdown = objective.breakdown(mapping)
    lines = [
        "Optimization Report",
        "===================",
        "",
        f"Algorithm: {result.metadata['algorithm']}",
        f"Seed: {result.metadata['seed']}",
        f"Iterations: {result.metadata['iterations']}",
        "",
        f"Final Score: {result.best_score:.2f}",
        "",
        "Penalty Breakdown",
        "",
    ]
    for name, value in breakdown.items():
        lines.append(f"{name.capitalize()}: {value:.2f}")
    lines.extend(
        [
            "",
            "Runtime",
            "",
            f"{result.runtime_seconds:.2f} s",
            "",
            f"Accepted Moves: {result.accepted}",
            f"Rejected Moves: {result.rejected}",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    config = load_config("configs/default.yaml")
    keyboard = build_keyboard_layout()
    piano = build_piano_notes(
        start_octave=config["experiment"]["start_octave"],
        count=config["experiment"]["note_count"],
    )

    objective = Objective(default_penalty_list(), config["penalty_weights"])
    optimizer = SimulatedAnnealing()
    result = optimizer.optimize(
        keyboard,
        piano,
        objective,
        config["optimizer"],
        config["optimizer"]["seed"],
    )

    output_dir = Path("exports") / f"run_{int(time.time())}"
    output_dir.mkdir(parents=True, exist_ok=True)

    export_json(
        output_dir / "summary.json",
        {
            "algorithm": result.metadata["algorithm"],
            "seed": result.metadata["seed"],
            "iterations": result.metadata["iterations"],
            "best_score": result.best_score,
            "accepted": result.accepted,
            "rejected": result.rejected,
            "runtime_seconds": result.runtime_seconds,
        },
    )
    export_json(output_dir / "layout.json", result.best_mapping.to_json())
    export_csv(
        output_dir / "metrics.csv",
        result.history,
        fieldnames=["iteration", "temperature", "current_score", "best_score", "accepted", "rejected"],
    )
    export_csv(
        output_dir / "layout.csv",
        result.best_mapping.to_csv_rows(),
        fieldnames=["key_label", "note_label", "note_index", "octave", "modifier"],
    )
    export_markdown(output_dir / "score_report.md", score_report(result, objective, result.best_mapping))

    plot_keyboard_layout(result.best_mapping, output_dir / "keyboard_layout.png")
    plot_score_history(result.history, output_dir / "score_curve.png")


if __name__ == "__main__":
    main()
