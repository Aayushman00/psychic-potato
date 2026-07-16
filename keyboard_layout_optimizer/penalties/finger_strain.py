import math

from ..models.mapping import Mapping
from ..models.piano import chromatic_neighbors

FINGER_STRIDE = {
    "thumb": 1.0,
    "index": 1.2,
    "middle": 1.4,
    "ring": 1.8,
    "pinky": 2.0,
}


def key_distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def score(mapping: Mapping) -> float:
    total = 0.0
    for left, right in chromatic_neighbors(mapping.notes.values()):
        key_a = mapping.keys[mapping.assignment[left.label()]]
        key_b = mapping.keys[mapping.assignment[right.label()]]
        if key_a.hand == key_b.hand:
            finger_a = key_a.finger
            finger_b = key_b.finger
            finger_penalty = abs(FINGER_STRIDE.get(finger_a, 1.5) - FINGER_STRIDE.get(finger_b, 1.5))
            stretch_penalty = max(0.0, key_distance(key_a, key_b) - 1.5)
            total += finger_penalty * 0.7 + stretch_penalty * 1.3
    return total
