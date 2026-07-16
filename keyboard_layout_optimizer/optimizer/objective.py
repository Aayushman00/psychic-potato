from __future__ import annotations
from typing import Dict, List

from ..models.mapping import Mapping
from ..penalties import (
    adjacency_score,
    finger_strain_score,
    ghosting_score,
    hand_balance_score,
    modifier_score,
    octave_score,
    placement_score,
    stretch_score,
    topology_score,
)

Penalty = Dict[str, object]


class Objective:
    def __init__(self, penalties: List[Penalty], weights: Dict[str, float]):
        self.penalties = penalties
        self.weights = weights

    def score(self, mapping: Mapping) -> float:
        total = 0.0
        for penalty in self.penalties:
            name = penalty["name"]
            score_fn = penalty["score_fn"]
            weight = self.weights.get(name, 1.0)
            total += score_fn(mapping) * weight
        return total

    def breakdown(self, mapping: Mapping) -> Dict[str, float]:
        result = {}
        for penalty in self.penalties:
            name = penalty["name"]
            score_fn = penalty["score_fn"]
            weight = self.weights.get(name, 1.0)
            result[name] = score_fn(mapping) * weight
        return result


def default_penalty_list() -> List[Penalty]:
    return [
        {"name": "placement", "score_fn": placement_score},
        {"name": "adjacency", "score_fn": adjacency_score},
        {"name": "octave", "score_fn": octave_score},
        {"name": "finger_strain", "score_fn": finger_strain_score},
        {"name": "hand_balance", "score_fn": hand_balance_score},
        {"name": "modifier", "score_fn": modifier_score},
        {"name": "ghosting", "score_fn": ghosting_score},
        {"name": "stretch", "score_fn": stretch_score},
        {"name": "topology", "score_fn": topology_score},
    ]
