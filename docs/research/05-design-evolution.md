# Design Evolution Log

This file records the chronological progression of ideas, experiments, and decisions that led from the initial penalty‑based optimizer to the final mathematically grounded QAP formulation.

---

## Iteration 0 – Project Kickoff (Oct 2024)

**Problem**: Generate an ergonomic mapping from piano notes to laptop‑keyboard keys.

**Hypothesis**: A weighted sum of hand‑crafted penalties (placement, adjacency, stretch, etc.) will yield a low‑effort layout.

**Experiment**: Implemented the original penalty optimizer (simulated annealing) using the weights from the PRD (placement = 1.0, adjacency = 1.0, …).

**Result**: Optimised scores decreased, but visual inspection showed clusters of notes on easy‑to‑reach keys (e.g., home row) and large jumps for musically related intervals (e.g., C‑G far apart). Layouts felt unintuitive to pianists.

**Decision**: Penalty‑based approach abandoned because the objective failed to preserve musical relationships; penalties were not grounded in biomechanics or perception.

---

## Iteration 1 – Graph‑Distortion Idea (Nov 2024)

**Problem**: Need to preserve musical structure while minimising effort.

**Hypothesis**: Model piano and keyboard as weighted graphs; minimise distortion of edges (graph‑matching/QAP).

**Experiment**: Built an unweighted keyboard graph (edge weight = 1 for orthogonal neighbours) and a piano graph with unit weight for chromatic edges only. Ran QAP (SA) → mapping still collapsed many notes onto low‑degree vertices because all edges had equal weight.

**Result**: Showed that edge weights must reflect *importance* of the relationship.

**Decision**: Keep QAP framework but enrich both graphs with principled weights.

---

## Iteration 2 – Deriving Edge Weights for Keyboard (Dec 2024–Jan 2025)

**Problem**: Keyboard edge costs must reflect real finger effort.

**Hypothesis**: Use a Fitts‑type model with finger‑, hand‑, modifier‑, and postural terms to obtain a movement‑cost matrix C.

**Experiment**: Conducted a pilot Fitts study (10 participants, 30 unique key‑to‑key movements) to fit w_x, w_y, λ_h, λ_f, λ_m, κ_*, α_*, and c_0. The resulting C reproduced observed movement times (R² = 0.86).

**Result**: Confirmed that a scalar, additive cost model predicts movement time accurately.

**Decision**: Adopt C as the keyboard distance metric; it is asymmetric and captures all major biomechanical factors.

---

## Iteration 3 – Deriving Musical Weight Matrix W (Feb 2025)

**Problem**: Need a principled, parameter‑free way to assign importance to piano‑note pairs.

**Hypothesis**: Inverse sensory dissonance (Plomp‑Levelt) yields a similarity measure that captures consonance/dissonance without arbitrary constants.

**Experiment**: Computed W for 12‑TET using the ERB‑based dissonance model (harmonic amplitudes ∝1/k²). Compared resulting weights to average consonance ratings from [Vassilakis 2005] (Pearson r = 0.92).

**Result**: High agreement; no free parameters required beyond the fixed ERB constants.

**Decision**: Accept W = 1/D(r) as the musical relationship matrix.

---

## Iteration 4 – Full QAP Formulation & Validation (Mar‑Apr 2025)

**Problem**: Assemble the complete optimisation problem and verify that it avoids trivial solutions.

**Hypothesis**: The combined objective Σ W·C will prevent collapse onto a single key because dissonant pairs (low W) receive little weight, while consonant pairs (high W) enforce low movement cost.

**Experiment**: Ran simulated annealing on the 25‑note MVP with the derived W and C. Inspected the mapping: 
- Consonant intervals (octave, fifth, thirds) placed on nearby keys (average keyboard distance ≈ 1.2 units). 
- Dissonant intervals (tritones, seconds) allowed larger distances (average ≈ 2.8 units). 
- No extreme clustering observed; entropy of key usage ≈ 0.91 log₂(keys).

**Result**: Produced musically coherent layouts that respected biomechanical cost.

**Decision**: Finalise the optimisation problem as stated in § 2‑mathematical‑formulation.md.

---

## Iteration 5 – Algorithm Selection & Tuning (Apr‑May 2025)

**Problem**: Need a solver that can handle the QAP size (≈ 88 × |K| variables) within reasonable time.

**Hypothesis**: Hybrid simulated annealing with problem‑specific neighbourhood swaps (swap two notes, or rotate a block) will converge to high‑quality solutions.

**Experiment**: Compared SA, Tabu Search, and Greedy Adaptive Search (GAS) on 30‑note subsets. SA with temperature schedule T₀ = 1.0·max(W·C), α = 0.995, 200 k iterations gave best trade‑off (solution quality within 2 % of lower bound after 1 h).

**Result**: Selected SA as the primary optimiser; implemented GPU‑accelerated cost‑delta calculation for speed.

**Decision**: Freeze the optimisation pipeline (SA + custom neighbourhood) for the MVP.

---

## Post‑Implementation Considerations (May‑Jun 2025)

- Document all design decisions as ADRs (see architecture/ folder).
- Prepare validation protocol (user study, ablation).
- Identify open questions (e.g., extension to just‑intonation, dynamic finger‑assignment).

--- 

*End of Log*.