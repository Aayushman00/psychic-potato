import math

from ..models.mapping import Mapping
from ..models.piano import octave_pairs


def key_distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def score(mapping: Mapping) -> float:
    distances = []
    for lower, upper in octave_pairs(mapping.notes.values()):
        key_lower = mapping.keys[mapping.assignment[lower.label()]]
        key_upper = mapping.keys[mapping.assignment[upper.label()]]
        distances.append(key_distance(key_lower, key_upper))
    if not distances:
        return 0.0
    mean = sum(distances) / len(distances)
    return sum((d - mean) ** 2 for d in distances)
