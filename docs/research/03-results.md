# Results (Outline)

This document will be filled after running the optimisation and evaluation experiments.

## Planned Experiments
1. **Baseline comparison** – Sequential mapping (C4→A, D4→S, …) vs. optimized mapping for the 25‑note MVP.
2. **Full‑keyboard evaluation** – 88‑note mapping with optional modifier layers.
3. **Ablation study** – Impact of removing each term in C (finger‑change, hand‑change, posture) on cost and playability.
4. **User study** – N=6 pianists play sight‑reading excerpts on both layouts; collect timing accuracy, error rate, NASA‑TLX.
5. **Robustness test** – Re‑run optimisation with different random seeds and compute solution variance.

## Metrics to Report
- Total weighted objective value.
- Octave consistency (variance of f(i+12)−f(i)).
- Interval preservation ratio (percentage of chromatic, fifth, third, octave pairs whose keyboard distance ≤ threshold).
- Average finger‑change count per octave.
- Hand‑alternation rate.
- Predicted movement time (sum of C over a repertoire).
- Subjective scores (comfort, learnability, preference).

Placeholders for figures and tables will be inserted once data are available.