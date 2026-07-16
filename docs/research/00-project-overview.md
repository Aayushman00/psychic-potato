# Project Overview

**Goal**: Derive a mathematically principled, biomechanically grounded optimization problem that maps the 88 keys of a piano onto the keys of a standard laptop keyboard (including optional modifier layers) such that the resulting layout preserves the musical and motor structures that expert pianists actually learn.

**Motivation**: Existing virtual‑piano maps assign notes sequentially across QWERTY rows. While easy to understand, they ignore biomechanical cost, finger independence, hand balance, octave consistency, and tactile landmarks, leading to layouts that feel awkward and unintuitive.

**Approach**: Treat the problem as a **Quadratic Assignment Problem (QAP)** where we minimize the distortion between two weighted graphs:

- **Piano graph** \(G_P = (V_P, E_P, W)\) – vertices are piano notes; edge weight \(W_{ij}\) reflects the perceptual/musical importance of preserving the relationship between notes \(i\) and \(j\).
- **Keyboard graph** \(G_K = (V_K, E_K, C)\) – vertices are keyboard states (key + hand + finger + modifier); edge weight \(C_{ab}\) is the predicted movement time/effort to go from state \(a\) to state \(b\) (derived from Fitts’ law and joint‑level biomechanics).

The decision variable is a bijective assignment \(f: V_P \rightarrow V_K\) (or injective if more keyboard states exist). The objective is  

\[
\min_{f}\;\sum_{i,j\in V_P} W_{ij}\; C_{f(i),f(j)} .
\]

All constants in \(W\) and \(C\) are derived from first principles (equal temperament, auditory dissonance, Fitts’ law, finger‑independence, posture costs) – no arbitrary interval weights or penalty terms remain.

**Outcome**: A mapping that, when evaluated by pianists, yields scales, arpeggios, and chords with comfortable finger transitions, preserved octave relationships, and low predicted movement cost.

**Key Deliverables** (to be produced after implementation):

- Source code implementing the QAP solver (simulated annealing with problem‑specific neighbourhood moves).
- Pre‑computed matrices \(W\) and \(C\) for the 25‑note MVP and full 88‑note keyboard.
- Visualizations of the generated layout (keyboard heat‑map, note‑to‑key annotation).
- Benchmark reports comparing the optimized layout against a naive sequential baseline on biomechanical cost, interval preservation, and subjective playability (via a small user study).