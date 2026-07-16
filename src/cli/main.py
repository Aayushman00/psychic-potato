#!/usr/bin/env python3
"""
Command‑line interface for the Piano‑to‑Keyboard Mapping Optimizer.
"""

import argparse
import json
import sys
from pathlib import Path

# Import core modules
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from core.piano_builder import build_weight_matrix
from core.kb_builder import load_keyboard_json, build_cost_matrix
from core.objective import Objective
from core.optimiser.simulated_annealing import SimulatedAnnealing
from core.mapping import Mapping

def build_piano_notes(num_notes: int, start_midi: int = 36):
    """Build list of PianoNote objects for the given range."""
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class PianoNote:
        index: int
        midi: int
        name: str
        octave: int
        is_black: bool

        @property
        def label(self) -> str:
            return f"{self.name}{self.octave}"

    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    notes = []
    midi = start_midi
    for idx in range(num_notes):
        note_name = note_names[midi % 12]
        octave = (midi // 12) - 1
        is_black = note_name in ["C#", "D#", "F#", "G#", "A#"]
        notes.append(PianoNote(index=idx, midi=midi, name=note_name, octave=octave, is_black=is_black))
        midi += 1
    return notes

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimise a mapping from piano notes to laptop‑keyboard keys."
    )
    parser.add_argument(
        "-k",
        "--keyboard",
        type=Path,
        help="Path to a JSON file describing the keyboard layout (base keys only).",
        default=None,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Where to write the resulting mapping (JSON).",
        default=Path("mapping.json"),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for the optimiser.",
    )
    parser.add_argument(
        "--notes",
        type=int,
        default=61,
        help="Number of piano notes to optimise (MVP default is 61).",
    )
    parser.add_argument(
        "--start-midi",
        type=int,
        default=36,
        help="Starting MIDI note number (default 36 = C2).",
    )
    args = parser.parse_args()

    # Determine path to base keyboard JSON
    if args.keyboard is not None:
        kb_path = args.keyboard
    else:
        kb_path = Path(__file__).resolve().parents[2] / "src" / "config" / "default_keyboard.json"

    # Load base keyboard (modifier = false) and generate states with modifiers none and shift
    keyboard_states = load_keyboard_json(kb_path, modifiers=[False, True])

    # Build piano notes and weight matrix
    piano_notes = build_piano_notes(args.notes, args.start_midi)
    W = build_weight_matrix(args.notes, args.start_midi)

    # Build cost matrix
    C = build_cost_matrix(keyboard_states, params=None)

    # Compute label lists
    note_labels = [note.label for note in piano_notes]
    key_labels = [state.label for state in keyboard_states]
    # Create objective with label lists for output
    objective = Objective(W, C, note_labels=note_labels, key_labels=key_labels)

    # Set up simulated annealing optimizer
    optimizer = SimulatedAnnealing(
        objective=objective,
        seed=args.seed,
    )

    # Run optimization
    best_mapping, best_score = optimizer.optimize()

    # Save the best mapping
    output_data = objective.assignment_dict()
    args.output.write_text(json.dumps(output_data, indent=2))
    print(f"Optimization completed. Best score: {best_score}")
    print(f"Mapping saved to {args.output}")

if __name__ == "__main__":
    sys.exit(main())