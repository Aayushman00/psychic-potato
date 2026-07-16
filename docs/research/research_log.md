# Research Log

## 2026-07-17 – MVP target increased from 25 to 61 keys and architectural shift to keyboard states

- Changed MVP from a 25‑key (two‑octave) prototype to a 61‑key (five‑octave) prototype to provide a playable range while still keeping the problem tractable.
- Refactored the keyboard representation from “physical key” to **ergonomic keyboard state** (key + modifier). This enables the optimizer to consider shifted versions of the same physical key as distinct states, which is essential for realistic piano‑to‑keyboard mapping.
- Updated all core source files (`src/core/*`) to work with lists of `KeyboardState` objects instead of plain `KeyboardKey` objects.
- Modified the CLI (`src/cli/main.py`) to load a base‑key JSON and duplicate each entry with `modifier=false` (natural) and `modifier=true` (shift), yielding a keyboard‑state set suitable for optimization.
- Revised the `Objective` class to accept optional `note_labels` and `key_labels` and provide `assignment_dict()` for JSON export.
- Updated the simulated‑annealing interface call in the CLI to match the actual class signature.
- Updated documentation:
    - `PRD.md`: MVP scope and success criteria now refer to 61 notes.
    - `configs/default.yaml`: `experiment.note_count` set to 61.
    - ADR‑004 and ADR‑007: changed “N≈25 (MVP)” to “N≈61 (MVP)”.
    - Added ADR‑012: “Keyboard States instead of Physical Keys”.
    - Replaced `tests/test_models.py` with a version that uses the new core classes.
- No remaining hard‑coded assumptions about a 25‑key piano exist in the core source (`src/` or `keyboard_layout_optimizer/`); the only occurrences of “25” are in legacy documentation, legacy configuration files, and the unit‑test suite (which now uses the new API).

The system is now ready to run a 61‑key optimization via:

    python -m src.cli.main --notes 61 --output mapping_61key.json