# Design Decisions

This file provides a concise overview of the major architectural decisions made during the project, referencing the detailed **Architecture Decision Records (ADRs)** stored in `architecture/adr/`.

| ADR ID | Title | Status | Summary |
|--------|-------|--------|---------|
| ADR-001 | Replace penalty‑based objective with graph distortion (QAP) | Accepted | Switched from a weighted sum of ad‑hoc penalties to a Quadratic Assignment Problem that minimizes Σ W·C, where W encodes musical relationships and C encodes biomechanical movement cost. |
| ADR-002 | Represent keyboard as weighted directed graph | Accepted | Each keyboard state (key + hand + finger + modifier) is a node; edge weight C_ab is the predicted movement time from state a to b (derived from Fitts‑type and posture model). |
| ADR-003 | Represent piano as weighted undirected graph | Accepted | Nodes are piano notes; edge weight W_ij is the inverse of sensory dissonance (Plomp‑Levelt) derived from equal‑tempered tuning and the auditory ERB model—no arbitrary constants. |
| ADR-004 | Use Simulated Annealing as primary optimiser | Accepted | Chosen for its simplicity, ability to handle the discrete, large‑search‑space QAP, and ease of incorporating problem‑specific neighbourhood moves (swap, block‑shift, rotation). |
| ADR-005 | Define movement‑cost matrix C via Fitts‑law + finger/hand/modifier/postural terms | Accepted | Combines geometric distance, anisotropic scaling, finger‑change penalty, hand‑change penalty, modifier‑change penalty, and joint‑effort terms; all parameters obtained from a brief calibration experiment or literature values. |
| ADR-006 | Repository structure (src/ + docs/ + tests/) | Accepted | Organized code into core building blocks, optimiser, CLI, evaluation, calibration, and tests; documentation lives under docs/ with research and architecture subfolders. |
| ADR-007 | Objective function formulation (final) | Accepted | The optimisation problem is: minimize Σᵢⱼ W_{ij} C_{f(i),f(j)} subject to bijective (or injective) mapping constraints. No additional penalty terms are required. |

Each ADR can be consulted for the full rationale, alternatives considered, and consequences.  The decisions above are **final**; any future change must be documented as a new ADR and, if it affects the mathematical formulation, first logged in `docs/research/open-questions.md` per the implementation constraint.