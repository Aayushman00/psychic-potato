from ..models.mapping import Mapping

KEY_AWKWARDNESS = {
    "`": 5,
    "1": 4,
    "2": 3,
    "3": 2,
    "4": 1,
    "5": 1,
    "6": 1,
    "7": 1,
    "8": 2,
    "9": 3,
    "0": 4,
    "-": 4,
    "=": 5,
    "P": 2,
    ";": 2,
    "'": 3,
    ",": 3,
    ".": 4,
    "/": 5,
}


def score(mapping: Mapping) -> float:
    total = 0.0
    for _, key_label in mapping.items():
        key = mapping.keys[key_label]
        penalty = KEY_AWKWARDNESS.get(key.label, 0)
        if key.row == 4:
            penalty += 1.0
        elif key.row == 1:
            penalty += 0.5
        total += penalty
    return total
