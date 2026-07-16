from ..models.mapping import Mapping
from ..models.piano import PianoNote


def score(mapping: Mapping) -> float:
    white_penalty = 0.0
    black_penalty = 0.0
    for note_label, key_label in mapping.items():
        note = mapping.notes[note_label]
        key = mapping.keys[key_label]
        if note.is_black:
            black_penalty += 0.5
        else:
            white_penalty += 0.1
    return white_penalty + black_penalty
