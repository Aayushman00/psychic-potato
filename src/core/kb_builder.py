"""
Keyboard geometry and biomechanical cost matrix builder.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
from .movement_model import MovementModel
from .keyboard_graph import KeyboardGraph

class KeyboardState:
    def __init__(self, label: str, x: float, y: float,
                 finger: str, hand: str, modifier: bool):
        self.label = label
        self.x = x
        self.y = y
        self.finger = finger   # e.g., 'index', 'middle', 'ring', 'pinky', 'thumb'
        self.hand = hand       # 'L' or 'R'
        self.modifier = bool(modifier)  # True if this state requires a held modifier (e.g., Shift)

def load_keyboard_json(path: Path, modifiers: List[bool] | None = None) -> List[KeyboardState]:
    """
    Load keyboard definitions from a JSON file.
    If modifiers is provided, each base key is duplicated for each modifier value.
    Each entry in the JSON should contain: label, x, y, finger, hand, modifier (optional, default False).
    Returns a list of KeyboardState instances.
    """
    if modifiers is None:
        modifiers = [False]
    data = json.loads(path.read_text())
    states = []
    for item in data:
        base_label = item["label"]
        base_x = float(item["x"])
        base_y = float(item["y"])
        base_finger = item["finger"]
        base_hand = item["hand"]
        base_mod_base = item.get("modifier", False)
        for mod in modifiers:
            # Effective modifier is base_mod_base OR mod? We'll treat mod as override.
            # For simplicity, we ignore base_mod_base and use mod.
            effective_mod = bool(mod)
            label = f"{base_label}+{'' if not effective_mod else 'Shift'}" if effective_mod else base_label
            states.append(KeyboardState(
                label=label,
                x=base_x,
                y=base_y,
                finger=base_finger,
                hand=base_hand,
                modifier=effective_mod
            ))
    return states

def build_cost_matrix(states: List[KeyboardState],
                      params: Dict[str, float] | None = None) -> np.ndarray:
    """
    Build the C matrix (movement time) for all ordered pairs of states.
    Uses the Version 1 movement model (see docs/architecture/adr/ADR-014.md).
    The `params` argument is retained for backward compatibility but is ignored.
    Returns a dense numpy array of shape (M, M).
    """
    # Use MovementModel v1 to assign edge weights
    model = MovementModel()  # loads default config
    graph = model.build_weighted_graph(states)
    return graph.distance_matrix()