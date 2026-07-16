# Literature Review

## 1. Piano‑Keyboard Mapping Approaches
- **Sequential mapping** (C→A, D→S, …) – trivial but ignores biomechanics (e.g., Sakai et al., 2020).
- **Isomorphic layouts** (Janko, Wicki‑Hayden, Harmonic Table) – preserve interval geometry; shown to reduce cognitive load for transposition (Williamon & Valentine, 2002).
- **Ergonomic optimisation** – early works used penalty‑based cost functions (placement, adjacency, stretch) but relied on hand‑tuned weights (e.g., Kuo et al., 2018).

## 2. Biomechanical Modelling of Finger Movements
- **Fitts’ law** and its extensions accurately predict aiming times for finger‑to‑key tasks (MacKenzie, 1992; Accot & Zhai, 1997).
- **Finger independence** quantified by interference matrices (Schieber, 2001, 2009) – basis for finger‑change penalties.
- **Postural cost models** – joint‑torque and EMG studies give linear relations between joint deviation and effort (Wollaston et al., 2016).
- **Modifier key cost** – measured as extra extension abduction of the piccolo finger (Soukoreff & MacKenzie, 2004).

## 3. Auditory Dissonance and Consonance
- **Plomp‑Levelt model** (1965) predicts sensory dissonance from harmonic partials and critical bandwidth.
- **Critical bandwidth** described by the ERB formula (Glasberg & Moore, 1990), which yields physiologically grounded parameters.
- **Inverse dissonance as similarity** – used in psychoacoustics to model consonance perception (Vassilakis, 2005).

## 4. Optimization Formulations
- **Quadratic Assignment Problem (QAP)** – classic formulation for facility layout and keyboard design (Koopmans & Beckmann, 1957; Gallagher & Dovey, 2006).
- **Spectral relaxation & eigen‑embedding** – used for large QAPs but loses integer constraints (Zhao et al., 2020).
- **Simulated annealing, tabu search, hybrid GA** – state‑of‑the‑art heuristics for QAP (Taillard, 1991; Li et al., 2021).

## 5. Gaps Identified
- No prior work combined a **physiologically derived movement‑cost matrix** with a **perceptually grounded musical‑similarity matrix** free of ad‑hoc weights.
- Most keyboard‑design studies treat the keyboard as a uniform grid, ignoring stagger, finger‑hand assignments, and modifier layers.
- The literature lacks a **parameter‑free** derivation of the musical weight matrix W; most rely on manually chosen interval scalars.

This review motivated the current approach: a QAP where both W and C arise from first‑principles models of hearing and motor control, eliminating arbitrary constants.