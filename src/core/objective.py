"""
Objective function for the QAP formulation with efficient delta evaluation.
"""
from __future__ import annotations
import numpy as np
from typing import List, Dict, Optional
from .mapping import Mapping

class Objective:
    def __init__(self, W: np.ndarray, C: np.ndarray, mapping: Mapping | None = None,
                 note_labels: Optional[List[str]] = None,
                 key_labels: Optional[List[str]] = None):
        """
        Parameters
        ----------
        W : np.ndarray, shape (N, N)
            Musical relationship matrix (symmetric, non‑negative, zero diagonal).
        C : np.ndarray, shape (M, M)
            Biomechanical movement‑cost matrix (generally asymmetric).
        mapping : Mapping, optional
            Initial assignment; if None, a default mapping to the first N keyboard
            states is created (requires M >= N).
        note_labels : list[str], optional
            Human‑readable labels for the piano notes (length N).
        key_labels : list[str], optional
            Human‑readable labels for the keyboard states (length M).
        """
        self.W = W.astype(float)   # (N, N)
        self.C = C.astype(float)   # (M, M)
        self.N = W.shape[0]
        self.M = C.shape[0]
        self.note_labels = note_labels
        self.key_labels = key_labels
        if mapping is None:
            if self.M >= self.N:
                init = list(range(self.N))
            else:
                # fallback: wrap around (should not happen in practice)
                init = [i % self.M for i in range(self.N)]
            mapping = Mapping(init, self.M)
        else:
            # ensure the mapping knows M
            if mapping.M is None:
                mapping.M = self.M
            elif mapping.M != self.M:
                raise ValueError("Provided mapping has mismatched M")
        self.mapping = mapping
        self._score: float = self._compute_score()

    def _update_score(self) -> None:
        """Recompute the cached score after replacing the mapping."""
        self._score = self._compute_score()

    # -----------------------------------------------------------------
    # Internal score computation
    # -----------------------------------------------------------------
    def _compute_score(self) -> float:
        f = np.array(self.mapping.assignment, dtype=int)
        # C[f[:, None], f] gives NxN matrix
        cost_matrix = self.C[f[:, None], f]
        return float(np.sum(self.W * cost_matrix))

    # -----------------------------------------------------------------
    # Static helper to compute delta from two assignment vectors
    # -----------------------------------------------------------------
    @staticmethod
    def _delta_from_arrays(W: np.ndarray, C: np.ndarray, f_old: np.ndarray, f_new: np.ndarray) -> float:
        """
        Compute Δscore = score_new - score_old.
        Score = Σ_iⱼ W[i,j] * C[f[i], f[j]].
        """
        C_old = C[f_old[:, None], f_old]   # (N, N)
        C_new = C[f_new[:, None], f_new]   # (N, N)
        diff = C_new - C_old               # (N, N)
        return float(np.sum(W * diff))

    # -----------------------------------------------------------------
    # Public delta for a move evaluations (given current mapping)
    # -----------------------------------------------------------------
    def delta_swap(self, i: int, j: int) -> float:
        if i == j:
            return 0.0
        f_old = np.array(self.mapping.assignment, dtype=int)
        f_new = f_old.copy()
        f_new[i], f_new[j] = f_new[j], f_new[i]
        return self._delta_from_arrays(self.W, self.C, f_old, f_new)

    def delta_block_shift(self, start: int, length: int, direction: int) -> float:
        if length <= 0:
            return 0.0
        f_old = np.array(self.mapping.assignment, dtype=int)
        f_new = f_old.copy()
        n = self.N
        m = self.M
        if m is None:
            raise RuntimeError("M (number of keyboard states) must be set for delta_block_shift")
        start = start % n
        indices = [(start + offset) % n for offset in range(length)]
        for idx in indices:
            f_new[idx] = (f_new[idx] + direction) % m
        return self._delta_from_arrays(self.W, self.C, f_old, f_new)

    def delta_rotation(self, i: int, j: int, k: int) -> float:
        if len({i, j, k}) < 3:
            return 0.0
        f_old = np.array(self.mapping.assignment, dtype=int)
        f_new = f_old.copy()
        vi, vj, vk = f_old[i], f_old[j], f_old[k]
        f_new[i] = vj
        f_new[j] = vk
        f_new[k] = vi
        return self._delta_from_arrays(self.W, self.C, f_old, f_new)

    # -----------------------------------------------------------------
    # Generic delta dispatcher used by optimiser
    # -----------------------------------------------------------------
    def delta(self, move_type: str, *args) -> float:
        if move_type == "swap":
            i, j = map(int, args)
            return self.delta_swap(i, j)
        elif move_type == "block_shift":
            start, length, direction = map(int, args)
            return self.delta_block_shift(start, length, direction)
        elif move_type == "rotation":
            i, j, k = map(int, args)
            return self.delta_rotation(i, j, k)
        else:
            raise ValueError(f"Unknown move type: {move_type}")

    # -----------------------------------------------------------------
    # Apply a move (mutates internal mapping) and update score
    # -----------------------------------------------------------------
    def apply_move(self, move_type: str, *args) -> None:
        """Mutate self.mapping according to the move and update internal score."""
        delta = self.delta(move_type, *args)
        if move_type == "swap":
            i, j = map(int, args)
            self.mapping.apply_swap(i, j)
        elif move_type == "block_shift":
            start, length, direction = map(int, args)
            self.mapping.apply_block_shift(start, length, direction)
        elif move_type == "rotation":
            i, j, k = map(int, args)
            self.mapping.apply_rotation(i, j, k)
        else:
            raise ValueError(f"Unknown move type: {move_type}")
        # Update cached score
        self._score += delta

    # Expose current score
    @property
    def score(self) -> float:
        return self._score

    # -----------------------------------------------------------------
    # Convenience: return assignment as dict of labels
    # -----------------------------------------------------------------
    def assignment_dict(self) -> Dict[str, str]:
        if self.note_labels is None or self.key_labels is None:
            raise ValueError("Label lists not provided to Objective")
        return {
            self.note_labels[i]: self.key_labels[self.mapping.assignment[i]]
            for i in range(len(self.mapping.assignment))
        }
