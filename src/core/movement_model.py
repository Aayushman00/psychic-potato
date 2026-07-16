"""
Version 1 of the ergonomic movement model.

Assigns a cost to each primitive ergonomic action (EdgeType) based on
heuristic biomechanical reasoning. The model is intentionally simple
and configurable; it does not attempt to capture detailed tendon or
joint kinematics.

The movement cost matrix C is computed as the all-pairs shortest-path
distances on the semantic keyboard graph where edge weights are given
by this model.
"""
from __future__ import annotations
from typing import Dict, Optional
from pathlib import Path

import yaml

from .keyboard_graph import KeyboardGraph, EdgeType, build_semantic_keyboard_graph


class MovementModel:
    """
    Loads ergonomic cost parameters and applies them to a KeyboardGraph.
    """
    def __init__(self, config_path: Optional[Path] = None):
        """
        Parameters
        ----------
        config_path : pathlib.Path, optional
            Path to a YAML file containing EdgeType → cost mappings.
            If None, uses the default configuration bundled with the
            package.
        """
        if config_path is None:
            config_path = Path(__file__).resolve().parents[2] / "config" / "movement_model.yaml"
        with config_path.open('r') as f:
            raw = yaml.safe_load(f)
        # Expected keys: same_finger, finger_change, hand_shift, modifier_toggle, scale
        self.scale: float = float(raw.get("scale", 1.0))
        self.weights: Dict[EdgeType, float] = {
            EdgeType.SAME_FINGER: float(raw.get("same_finger", 1.0)) * self.scale,
            EdgeType.FINGER_CHANGE: float(raw.get("finger_change", 1.8)) * self.scale,
            EdgeType.HAND_SHIFT: float(raw.get("hand_shift", 2.5)) * self.scale,
            EdgeType.MODIFIER_TOGGLE: float(raw.get("modifier_toggle", 1.2)) * self.scale,
        }

    def weight(self, edge_type: EdgeType) -> float:
        """Return the cost for a given EdgeType."""
        return self.weights.get(edge_type, 1.0)

    def apply_to_graph(self, graph: KeyboardGraph) -> None:
        """
        Overwrite the edge weights of the supplied KeyboardGraph according
        to this model's EdgeType → cost mapping.
        """
        n = graph.n
        for i in range(n):
            for j, etype in graph.adj[i]:
                if i < j:  # set each undirected edge once
                    w = self.weight(etype)
                    graph.set_edge_weight(i, j, w)

    def build_weighted_graph(self, states) -> KeyboardGraph:
        """
        Build a semantic keyboard graph from the given states and assign
        edge weights according to this model.

        Returns
        -------
        KeyboardGraph
            A graph whose edges are labelled with EdgeType and whose
            weights reflect the ergonomic costs.
        """
        graph = build_semantic_keyboard_graph(states)
        self.apply_to_graph(graph)
        return graph