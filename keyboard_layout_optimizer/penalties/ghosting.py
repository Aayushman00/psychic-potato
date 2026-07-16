from ..models.mapping import Mapping

GHOSTING_GROUPS = [
    {"Q", "W", "E"},
    {"A", "S", "D"},
    {"Z", "X", "C"},
    {"U", "I", "O"},
    {"J", "K", "L"},
]


def score(mapping: Mapping) -> float:
    penalty = 0.0
    assigned = set(mapping.assignment.values())
    for group in GHOSTING_GROUPS:
        if group <= assigned:
            penalty += 5.0
    return penalty
