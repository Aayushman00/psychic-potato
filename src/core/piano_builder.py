"""
Build the musical relationship matrix W from first‑principles
auditory dissonance (Plomp‑Levelt) and equal‑tempered tuning.
"""
from __future__ import annotations
import numpy as np
from typing import Literal

# Constants from Glasberg & Moore (1990) ERB formula
_ERB_CONST_A = 24.7
_ERB_CONST_B = 4.37
_REF_FREQ = 1000.0  # Hz

def _erb(freq: float) -> float:
    """Equivalent Rectangular Bandwidth in Hz."""
    return _ERB_CONST_A * (_ERB_CONST_B * freq / 1000.0 + 1.0)

# Precompute b1, b2 based on reference frequency
_b1 = 2.0 / _erb(_REF_FREQ)
_b2 = 1.0 / _erb(_REF_FREQ)

# Harmonic amplitude model for piano: A_k proportional to 1/k^2
def _harmonic_amplitude(k: int) -> float:
    return 1.0 / (k * k)

def build_weight_matrix(num_notes: int,
                        start_midi: int = 0,
                        tuning: Literal["equal_tempered"] = "equal_tempered") -> np.ndarray:
    """
    Return a symmetric matrix W of shape (num_notes, num_notes) where
    W[i,j] = 1 / D(r_ij) with D the sensory dissonance of the two notes.
    The matrix is zero‑diagonal.
    """
    # MIDI numbers for the considered notes
    midi_numbers = np.arange(start_midi, start_midi + num_notes, dtype=int)
    # Frequency of each note in Hz (A4 = 440 Hz, MIDI 69)
    freqs = 440.0 * 2.0 ** ((midi_numbers - 69) / 12.0)

    # Prepare output
    W = np.zeros((num_notes, num_notes), dtype=float)

    # Limit harmonics to, say, 1..20 (covers >99% of energy)
    harmonics = np.arange(1, 21)
    amp = np.array([_harmonic_amplitude(k) for k in harmonics], dtype=float)  # shape (H,)

    for i in range(num_notes):
        Fi = freqs[i]
        for j in range(i + 1, num_notes):
            Fj = freqs[j]
            # Compute dissonance sum over all harmonic pairs
            # Using vectorization over harmonics
            # kF_i - lF_j outer product
            kf = (harmonics[:, None] * Fi)  # shape (H,1)
            lf = (harmonics[None, :] * Fj)  # shape (1,H)
            diff = np.abs(kf - lf)          # shape (H,H)
            term1 = np.exp(-_b1 * diff)
            term2 = 1.0 - np.exp(-_b2 * diff)
            # Outer product of amplitudes
            A = amp[:, None] * amp[None, :]  # (H,H)
            D = np.sum(A * term1 * term2)
            # Avoid division by zero (should not happen for i!=j)
            w = 1.0 / D if D > 0 else 0.0
            W[i, j] = w
            W[j, i] = w
    # Optional normalisation (does not affect argmin)
    max_w = np.max(W)
    if max_w > 0:
        W = W / max_w
    return W
