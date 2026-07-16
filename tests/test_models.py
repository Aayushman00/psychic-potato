import pytest
from src.core.kb_builder import KeyboardState, load_keyboard_json
from src.core.mapping import Mapping
from src.core.piano_builder import build_weight_matrix  # not needed but import to ensure module loads
from dataclasses import dataclass

@dataclass(frozen=True)
class PianoNote:
    index: int
    midi: int
    name: str
    octave: int
    is_black: bool

    @property
    def label(self) -> str:
        return f"{self.name}{self.octave}"

def build_piano_notes(count: int, start_midi: int = 36) -> list[PianoNote]:
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    notes = []
    midi = start_midi
    for i in range(count):
        name = note_names[midi % 12]
        octave = (midi // 12) - 1
        is_black = name in ["C#", "D#", "F#", "G#", "A#"]
        notes.append(PianoNote(i, midi, name, octave, is_black))
        midi += 1
    return notes

def test_baseline_mapping_creates_unique_assignments():
    piano = build_piano_notes(25)
    # create a simple keyboard: 30 keys in a row, left hand for first 15, right for rest
    keyboard_states = []
    for i in range(30):
        hand = "left" if i < 15 else "right"
        finger = "index"  # simplify
        ks = KeyboardState(label=f"K{i}", x=float(i), y=0.0, hand=hand, finger=finger, modifier=False)
        keyboard_states.append(ks)
    mapping = Mapping(list(range(len(piano))), M=len(keyboard_states))
    # mapping.assignment is list of state indices; ensure length matches piano count
    assert len(mapping.assignment) == len(piano)
    # ensure injective (no duplicate state indices)
    assert len(set(mapping.assignment)) == len(piano)
    # ensure M attribute set correctly
    assert mapping.M == len(keyboard_states)

def test_mapping_validation():
    piano = build_piano_notes(3)
    # three keys: left index, left middle, left right
    keyboard_states = [
        KeyboardState(label="A", x=0.0, y=0.0, hand="left", finger="index", modifier=False),
        KeyboardState(label="S", x=1.0, y=0.0, hand="left", finger="middle", modifier=False),
        KeyboardState(label="D", x=2.0, y=0.0, hand="left", finger="ring", modifier=False),
    ]
    mapping = Mapping([0, 1, 2], M=3)
    assert mapping.validate(piano, keyboard_states) == True
    # invalid mapping: duplicate key
    mapping_dup = Mapping([0, 0, 1], M=3)
    assert mapping_dup.validate(piano, keyboard_states) == False
    # out-of-range key
    mapping_oob = Mapping([0, 1, 3], M=3)
    assert mapping_oob.validate(piano, keyboard_states) == False