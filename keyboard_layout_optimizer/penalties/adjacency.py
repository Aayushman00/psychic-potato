import math

from ..models.mapping import Mapping
from ..models.piano import chromatic_neighbors


def key_distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def score(mapping: Mapping) -> float:
    total = 0.0
    for left, right in chromatic_neighbors(mapping.notes.values()):
        key_a = mapping.keys[mapping.assignment[left.label()]]
        key_b = mapping.keys[mapping.assignment[right.label()]]
        total += key_distance(key_a, key_b) ** 2
    return total
