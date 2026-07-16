import pytest

from keyboard_layout_optimizer.models.keyboard import KeyboardKey
from keyboard_layout_optimizer.models.mapping import Mapping, baseline_sequential_mapping
from keyboard_layout_optimizer.models.piano import build_piano_notes


def test_baseline_mapping_creates_unique_assignments():
    piano = build_piano_notes(start_octave=4, count=25)
    keyboard = [KeyboardKey(label=str(i), row=1, x=float(i), y=0.0, hand="left", finger="index") for i in range(25)]
    mapping = baseline_sequential_mapping(piano, keyboard)

    assert len(mapping.assignment) == len(piano)
    assert len(set(mapping.assignment.values())) == len(piano)


def test_mapping_validation():
    piano = build_piano_notes(start_octave=4, count=3)
    keyboard = [KeyboardKey(label="A", row=1, x=0.0, y=0.0, hand="left", finger="index"), KeyboardKey(label="S", row=1, x=1.0, y=0.0, hand="left", finger="middle"), KeyboardKey(label="D", row=1, x=2.0, y=0.0, hand="left", finger="ring")]
    mapping = Mapping({"C4": "A", "C#4": "S", "D4": "D"})

    assert mapping.validate(piano, keyboard)
