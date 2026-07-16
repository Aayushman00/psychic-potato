from collections import Counter

from ..models.mapping import Mapping


def score(mapping: Mapping) -> float:
    hand_counts = Counter()
    for _, key_label in mapping.items():
        key = mapping.keys[key_label]
        hand_counts[key.hand] += 1
    left = hand_counts.get("left", 0)
    right = hand_counts.get("right", 0)
    return abs(left - right) ** 1.5
