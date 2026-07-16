# Data Flow Description

This document details how data moves through the system from raw inputs to the final mapping output, referencing the modules defined in the architecture.

## 1. Input Ingestion
- **Keyboard JSON/YAML** (provided by the user or shipped as a default template) contains:
  - `keys`: list of objects with fields `label`, `x` (mm), `y` (mm), `finger`, `hand`, `modifier` (bool indicating if the key requires a held modifier like Shift to produce the intended character).  
  - Optional fields: `key_width` (mm), `home_row_y` (for posture model).  
  This file is read by `src/core/kb_builder.py` and turned into a list of `KeyboardState` objects.
- **Calibration Parameters** (if a prior calibration run has been performed) are stored in `config/calibration.json` and loaded by the same module to override the default estimates for `TP`, `w_x`, `w_y`, lambda’s, kappa’s, alpha’s, and `c_0`. If absent, the builder falls back to the default values derived from the literature (see research/06-keyboard-biomechanics.md).

## 2. Building the Cost Matrix **C**
1. From the list of `KeyboardState`s, generate every ordered pair (a,b) within a configurable **neighbourhood radius** (default: Chebyshev distance ≤ 2 keys) to keep the matrix sparse yet still capture all feasible moves in a typical fingering span.
2. For each pair compute:
   - Geometric term `D_ab` (section 2 of the biomechanics model).
   - Effective width `W_e` using the approach angle and effector modifiers.
   - Fitts ID: `log2(D_ab/W_e + 1)`.
   - Postural term `P_ab` via the inverse‑kinematics finger‑hand‑arm model.
   - Total time: `C_ab = (1/TP) * ID + P_ab + c_0`.
3. Populate a dense `numpy.ndarray` of shape `(M, M)`; entries for pairs outside the neighbour radius are set to a large penalty value (effectively forbidding those moves) or simply retained as the computed cost if the full matrix is desired.
The resulting matrix is stored in `src/core/kb_builder.C`.

## 3. Building the Musical Weight Matrix **W**
- Input: the 12‑tone equal‑tempered tuning (hard‑coded) or an optional alternative tuning file (e.g., just‑intonation ratios) read by `src/core/piano_builder.py`.
- For each ordered pair of MIDI note numbers (0‑107) compute:
  - Pitch‑class distance Δ.
  - Frequency ratio r = 2^{Δ/12}.
  - Plomp‑Levelt dissonance D(r) using the harmonic amplitude series A_k = 1/k² and the ERB‑derived constants b₁, b₂.
  - Weight = 1 / D (with a small epsilon to avoid division by zero for identical notes).
- Symmetrise (the computation already yields symmetric values).  
- Optionally normalise by dividing by the global max to keep values in (0,1] for numerical stability.
The resulting matrix is stored in `src/core/piano_builder.W`.

## 4. Optimisation Core
- The **Objective** class (`src/core/objective.py`) holds references to `W` and `C` and provides two main methods:
  1. `evaluate(mapping) -> float` – computes Σ W[i][j] * C[ f(i) ][ f(j) ] in O(N²) (used for initial solution and final reporting).
  2. `delta_cost(move, mapping) -> float` – returns the change in objective caused by a neighbourhood move (swap, block‑shift, rotation) using only the affected indices; this is O(N) per move.
- The **SimulatedAnnealing** optimizer (`src/core/optimiser/simulated_annealing.py`) maintains:
  - Current mapping as a length‑N list of integers (indices into the keyboard state list).
  - Temperature `T`.
  - Iteration counter.
  - At each step:
      - Randomly selects a move type (with configurable probabilities).
      - Computes Δcost via the objective’s delta method.
      - Accepts with probability `min(1, exp(-Δcost / T))` (Metropolis criterion).
      - Updates the mapping if accepted.
      - After a fixed number of steps per temperature, reduces `T` by the cooling factor α.
- The loop terminates when `T < T_min` or no improvement over a given number of temperature levels.

## 5. Output Generation
Once the annealing finishes:
- The best mapping encountered is converted to a human‑readable format:
  - JSON: `{ "C4": "A", "D4": "S", ... }` (note name → key label).
  - CSV with columns `note, midi, key_label, finger, hand, modifier`.
- Visualisation script (`src/evaluation/plots.py`) creates:
  - A heat‑map of the keyboard showing which note occupies each key (color‑coded by pitch class).
  - A fingering diagram overlay indicating the assigned finger for each note.
  - Optionally, a plot of objective value versus iteration to show convergence.
- Evaluation script (`src/evaluation/metrics.py`) computes:
  - Total objective value.
  - Octave consistency: variance of `f(i+12) - f(i)` across i.
  - Interval preservation ratios for chromatic, perfect fifth, major/minor third, and octave pairs.
  - Average finger changes per octave, hand‑alternation rate.
  - Total predicted movement time for a standard repertoire (e.g., C‑major scale, arpeggios, simple chorale) using the C matrix.
All outputs are written to `experiments/<timestamp>/`.

## 6. Feedback Loop (Optional Calibration)
If the user wishes to personalize the model to their own anatomy:
1. Run `calibration/run_calibration.py`, which guides them through a series of Fitts‑style tasks (horizontal/vertical moves, finger‑change, hand‑change, modifier‑change,姿勢調整).
2. The script estimates the parameters (`TP`, `w_x`, `w_y`, λ’s, κ’s, α’s, `c_0`) via ordinary least squares and writes them to `config/calibration.json`.
3. Subsequent optimisation runs will load these customized values, producing a tailor‑made keyboard cost matrix **C**.

The data flow thus remains strictly unidirectional from input → matrices → optimisation → output, with calibration as an optional preprocessing step that feeds into the cost‑matrix builder.

*End of Data Flow Description*.