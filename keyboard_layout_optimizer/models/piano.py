from dataclasses import dataclass
from typing import List

WHITE_KEYS = ["C", "D", "E", "F", "G", "A", "B"]
BLACK_KEYS = ["C#", "D#", "F#", "G#", "A#"]

@dataclass(frozen=True)
class PianoNote:
    index: int
    midi: int
    name: str
    octave: int
    is_black: bool

    @property
    def pitch_class(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "midi": self.midi,
            "name": self.name,
            "octave": self.octave,
            "is_black": self.is_black,
        }

    def label(self) -> str:
        return f"{self.name}{self.octave}"


def build_piano_notes(start_octave: int, count: int) -> List[PianoNote]:
    notes = []
    pitch_order = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    midi = 12 * (start_octave + 1)
    for idx in range(count):
        name = pitch_order[midi % 12]
        octave = (midi // 12) - 1
        notes.append(
            PianoNote(
                index=idx,
                midi=midi,
                name=name,
                octave=octave,
                is_black=name in BLACK_KEYS,
            )
        )
        midi += 1
    return notes


def chromatic_neighbors(notes: List[PianoNote]) -> List[tuple]:
    return [(notes[i], notes[i + 1]) for i in range(len(notes) - 1)]


def octave_pairs(notes: List[PianoNote]) -> List[tuple]:
    pairs = []
    note_by_midi = {note.midi: note for note in notes}
    for note in notes:
        target = note.midi + 12
        if target in note_by_midi:
            pairs.append((note, note_by_midi[target]))
    return pairs
