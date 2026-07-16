from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from .keyboard import KeyboardKey
from .piano import PianoNote


@dataclass
class Mapping:
    assignment: Dict[str, str] = field(default_factory=dict)
    notes: Dict[str, PianoNote] = field(default_factory=dict, repr=False)
    keys: Dict[str, KeyboardKey] = field(default_factory=dict, repr=False)

    def assign(self, note_label: str, key_label: str) -> None:
        self.assignment[note_label] = key_label

    def unassign(self, note_label: str) -> None:
        self.assignment.pop(note_label, None)

    def get_key_label(self, note_label: str) -> str:
        return self.assignment[note_label]

    def get_keyboard_key(self, note_label: str) -> KeyboardKey:
        return self.keys[self.assignment[note_label]]

    def get_note_label(self, key_label: str) -> Optional[str]:
        for note_label, assigned_key in self.assignment.items():
            if assigned_key == key_label:
                return note_label
        return None

    def items(self) -> Iterable[tuple[str, str]]:
        return self.assignment.items()

    def validate(self, notes: Iterable[PianoNote], keys: Iterable[KeyboardKey]) -> bool:
        note_labels = {note.label() for note in notes}
        key_labels = {key.label for key in keys}
        assigned_notes = set(self.assignment.keys())
        assigned_keys = set(self.assignment.values())
        return (
            assigned_notes == note_labels
            and assigned_keys <= key_labels
            and len(self.assignment) == len(set(self.assignment.values()))
        )

    def to_json(self) -> Dict[str, str]:
        return dict(self.assignment)

    def to_csv_rows(self) -> List[dict]:
        rows = []
        for note_label, key_label in self.assignment.items():
            note = self.notes[note_label]
            key = self.keys[key_label]
            rows.append(
                {
                    "key_label": key.label,
                    "note_label": note.label(),
                    "note_index": note.index,
                    "octave": note.octave,
                    "modifier": key.modifier,
                }
            )
        return rows

    @classmethod
    def from_assignment(
        cls,
        assignment: Dict[str, str],
        notes: Iterable[PianoNote],
        keys: Iterable[KeyboardKey],
    ) -> "Mapping":
        note_map = {note.label(): note for note in notes}
        key_map = {key.label: key for key in keys}
        return cls(assignment=dict(assignment), notes=note_map, keys=key_map)


def baseline_sequential_mapping(notes: List[PianoNote], keys: List[KeyboardKey]) -> Mapping:
    mapping = Mapping.from_assignment({}, notes, keys)
    sorted_keys = sorted(keys, key=lambda key: (key.row, key.x, key.y, key.label))
    for note, key in zip(notes, sorted_keys):
        mapping.assign(note.label(), key.label)
    return mapping
