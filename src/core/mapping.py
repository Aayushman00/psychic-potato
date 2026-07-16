"""
Mapping representation and helper functions for applying neighbourhood moves.
"""
from __future__ import annotations
from typing import List, Optional

class Mapping:
    """
    Represents an assignment of piano notes to keyboard states.

    Attributes
    ----------
    assignment : list[int]
        For each piano note index i, assignment[i] gives the index of the
        keyboard state it is mapped to.
    M : int | None
        Number of keyboard states (size of the codomain). If None, modulo
        operations will raise an error; it should be set after construction
        or provided via the constructor.
    """

    def __init__(self, assignment: List[int], M: Optional[int] = None):
        self.assignment = list(assignment)  # mutable list
        self.M = M
        self._length = len(self.assignment)

    def __len__(self) -> int:
        return self._length

    def __getitem__(self, idx: int) -> int:
        return self.assignment[idx]

    def __setitem__(self, idx: int, value: int) -> None:
        self.assignment[idx] = value

    def copy(self) -> "Mapping":
        return Mapping(self.assignment.copy(), self.M)

    def to_list(self) -> List[int]:
        return self.assignment.copy()

    def validate(self, piano_notes, keyboard_states) -> bool:
        """Return True when every note maps to one unique, in-range state."""
        if len(self.assignment) != len(piano_notes):
            return False
        if len(set(self.assignment)) != len(self.assignment):
            return False
        return all(0 <= state_index < len(keyboard_states) for state_index in self.assignment)

    # -----------------------------------------------------------------
    # Mutation methods used by the optimiser
    # -----------------------------------------------------------------
    def apply_swap(self, i: int, j: int) -> None:
        """Exchange the keyboard states assigned to notes i and j."""
        self.assignment[i], self.assignment[j] = (
            self.assignment[j],
            self.assignment[i],
        )

    def apply_block_shift(self, start: int, length: int, direction: int) -> None:
        """
        Shift a contiguous block of notes by one keyboard step.
        Parameters
        ----------
        start : int
            Index of the first note in the block (0‑based).
        length : int
            Number of consecutive notes in the block.
        direction : int
            Either +1 (forward) or -1 (backward) in keyboard index space.
        """
        if self.M is None:
            raise RuntimeError("M (number of keyboard states) must be set before applying block shift")
        n = len(self)
        m = self.M
        start = start % n
        for offset in range(length):
            idx = (start + offset) % n
            self.assignment[idx] = (self.assignment[idx] + direction) % m

    def apply_rotation(self, i: int, j: int, k: int) -> None:
        """Cycle assignments: i<-j, j<-k, k<-i."""
        if len({i, j, k}) < 3:
            return
        vi, vj, vk = self.assignment[i], self.assignment[j], self.assignment[k]
        self.assignment[i] = vj
        self.assignment[j] = vk
        self.assignment[k] = vi
