# Architecture Overview

This document describes the high‑level structure of the Piano‑to‑Keyboard Mapping Optimizer.

## Components
1. **Input Module** – loads keyboard geometry (key coordinates, finger/hand assignments, modifier maps) and optional user‑specific calibration parameters.
2. **Weight Matrix Builder** – computes the musical relationship matrix **W** from the equal‑tempered tuning and the ERB‑based Plomp‑Levelt dissonance model (see research/07-musical-relationship-model.md).
3. **Cost Matrix Builder** – builds the biomechanical movement‑cost matrix **C** using the Fitts‑type model with finger, hand, modifier, and posture terms (see research/06-keyboard-biomechanics.md).
4. **Optimiser** – simulated annealing with problem‑specific neighbourhood moves (swap, block shift, rotation) that operates on the assignment matrix **X** and evaluates the QAP objective  $$\sum_{i,j} W_{ij} C_{f(i),f(j)}$$.
5. **Output Module** – writes the optimal mapping (note → key) to JSON/CSV and generates visualisations (heat‑map, fingering diagram).
6. **Evaluation & Validation** – optional scripts that compute objective value, interval‑preservation metrics, and run user‑study protocols.

## Data Flow
```
[Keyboard Geometry] --> Cost Matrix Builder --> C
[Keyboard Geometry] --> (optional) Calibration --> C parameters
[Equal Temperament Tuning] --> Weight Matrix Builder --> W
[W, C] --> Optimiser --> Assignment X
[X] --> Output Module --> Mapping + Reports
```

The system is deliberately modular: swapping the optimiser (e.g., to a tabu search) or replacing the W or C builders with alternative models requires only changes to the respective module, without affecting the rest of the pipeline.

## Technology Stack
- Language: Python 3.11 (core), optional C++/CUDA for accelerated cost‑delta calculations.
- Dependencies: NumPy, SciPy, matplotlib, tqdm, pytest.
- Build: No compilation needed for the pure‑python version; optional extensions compiled with `python setup.py build_ext --inplace`.
- Deployment: Single‑directory installable via `pip .`; configuration files are JSON/YAML.

## Scalability
The most expensive step is the construction of the dense \(M\times M\) cost matrix **C** (M = number of keyboard states). For the typical laptop (~47 keys × 2 hands × 5 fingers × 2 modifier layers ≈ 940) this is < 1 MB and easily handled. The **W** matrix is size \(N\times N\) with N ≤ 88 (≈ 7 KB). The optimiser itself operates in O(N²) per evaluation but uses incremental Δcost updates, making each iteration effectively O(L) where L is the size of the neighbourhood (≤ 10).

*End of Architecture Overview*.