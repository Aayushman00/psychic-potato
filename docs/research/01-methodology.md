# Methodology

## Overview
The project follows a **research‑through‑design** workflow: we first derived a principled mathematical formulation (see *Mathematical Formulation*), then instantiated the required data structures (W‑matrix, C‑matrix), and finally applied a combinatorial optimiser (Simulated Annealing) to obtain a near‑optimal bijection between piano notes and keyboard states.

## Steps

1. **Define the keyboard state space**  
   - Enumerate all physical keys on the target laptop (e.g., US QWERTY).  
   - For each key, record its Cartesian centre (x, y) in mm, assigned finger (based on neutral typing posture), assigned hand, and whether it requires a modifier (Shift/Alt/Ctrl).  
   - Optionally create duplicate states for each modifier layer (e.g., Shift‑A, Ctrl‑A).  

2. **Compute the biomechanical movement‑cost matrix C**  
   - For every ordered pair of states (a, b) calculate the predicted movement time using the Fitts‑type model described in *C‑derivation*.  
   - The model includes: anisotropic distance term, finger‑change penalty, hand‑change penalty, modifier‑change penalty, and postural/joint‑angle terms.  
   - Parameters (throughput TP, weighting coefficients w_x, w_y, λ_h, λ_f, λ_m, κ_*, α_*) are obtained from a short calibration experiment (≈15 min) where participants perform isolated key‑to‑key taps.  

3. **Construct the piano musical‑relationship matrix W**  
   - Derive W from the inverse of the Plomp‑Levelt sensory dissonance model (see *W‑derivation*).  
   - This requires only the equal‑tempered tuning and the standard auditory ERB model – no free musical parameters.  

4. **Formulate the QAP**  
   - Decision variables: binary assignment matrix X∈{0,1}^{N×M}.  
   - Constraints: each piano note assigned to exactly one keyboard state; each keyboard state receives at most one note (injective mapping).  
   - Objective: minimize Σ_{i,j} W_{ij}·C_{f(i),f(j)}.  

5. **Optimization**  
   - Use Simulated Annealing with problem‑specific moves:  
        *Swap* two notes’ assigned keys,  
        *Shift* a block of consecutive notes to nearby keys,  
        *Rotate* a triplet to explore different fingerings.  
   - Acceptance probability follows the Metropolis criterion with a geometrically decreasing temperature schedule.  
   - Run multiple independent seeds (e.g., 30) and keep the best solution.  

6. **Evaluation**  
   - Compute total weighted cost, preservation metrics (octave variance, interval‑preservation ratio), and biomechanical proxies (average finger‑change count, hand‑alternation rate).  
   - Compare against a baseline sequential mapping (C4→A, D4→S, …) using the same metrics.  
   - Conduct a small user study (n≈6 pianists) where participants play short melodic excerpts on both layouts; collect timing accuracy, error rate, and subjective comfort (NASA‑TLX).  

## Tools & Languages
- Python 3.11 for data generation, matrix construction, and evaluation.  
- NumPy / Sci‑J for linear algebra.  
- Custom simulated‑annealing module (no external QAP solvers required for the MVP).  
- Matplotlib / Seaborn for visualisations.  
- JSON / CSV for reproducible experiment logs.

## Reproducibility
All random seeds, configuration files, and intermediate matrices are version‑controlled. The exact calibration protocol is documented in `docs/experiments/calibration-protocol.md`.