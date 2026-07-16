from ..models.mapping import Mapping

MIDDLE_OCTAVE_PENALTY = 2.0


def score(mapping: Mapping) -> float:
    total = 0.0
    for note_label, key_label in mapping.items():
        note = mapping.notes[note_label]
        key = mapping.keys[key_label]
        if note.octave == 4:
            total += MIDDLE_OCTAVE_PENALTY if key.modifier else 0.0
    return total
