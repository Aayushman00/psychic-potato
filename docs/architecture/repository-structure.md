# Repository Structure

```
project/
├── docs/                       # All documentation (this folder)
│   ├── README.md
│   ├── research/               # Research notes, literature, design evolution, etc.
│   │   ├── 00-project-overview.md
│   │   ├── 01-methodology.md
│   │   ├── 02-mathematical-formulation.md
│   │   ├── 03-results.md
│   │   ├── 04-literature-review.md
│   │   ├── 05-design-evolution.md
│   │   ├── 06-keyboard-biomechanics.md
│   │   ├── 07-musical-relationship-model.md
│   │   ├── 08-optimization-strategy.md
│   │   ├── 09-algorithm-analysis.md
│   │   ├── 10-open-questions.md
│   │   └── 11-future-work.md
│   └── architecture/           # High‑level architecture and ADRs
│       ├── architecture.md
│       ├── repository-structure.md
│       ├── data-flow.md
│       ├── design-decisions.md
│       └── adr/
│           ├── ADR-001-replace-penalty-with-graph-objective.md
│           ├── ADR-002-keyboard-weighted-graph.md
│           ├── ADR-003-piano-weighted-graph.md
│           ├── ADR-004-use-simulated-annealing.md
│           ├── ADR-005-movement-cost-matrix-design.md
│           ├── ADR-006-repository-architecture.md
│           ├── ADR-007-QAP-objective-function.md
│           ├── ADR-008-w-inverse-dissonance.md
│           ├── ADR-009-neighborhood-operators.md
│           └── ADR-010-calibration-procedure.md
├── src/                        # Source code
│   ├── __init__.py
│   ├── config/                 # Default configuration files (JSON/YAML)
│   │   └── sa_params.json
│   ├── core/
│   │   ├── __init__.py
│   │   ├── objective.py        # QAP objective and Δ‑cost helpers
│   │   ├── mapping.py          # Assignment representation and helpers
│   │   ├── kb_builder.py       # Builds keyboard geometry and C matrix
│   │   ├── piano_builder.py    # Builds W matrix from tuning & auditory model
│   │   └── optimiser/
│   │       ├── __init__.py
│   │       ├── simulated_annealing.py
│   │       ├── neighbourhood.py   # swap, block‑shift, rotation
│   │       └── utils.py
│   ├── cli/                    # Command‑line interface
│   │   └── __init__.py
│   │   └── main.py
│   ├── evaluation/            # Metrics, reporting, visualisation
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   ├── plots.py
│   │   └── user_study.py
│   └── calibration/           # Scripts to run the Fitts‑based calibration
│       ├── __init__.py
│       └── run_calibration.py
├── tests/                      # Unit and integration tests
│   ├── test_core.py
│   └── test_optimiser.py
├── experiments/                # Temporary outputs from runs (not committed)
├── requirements.txt            # Python dependencies
├── setup.py                    # Packaging script
└── README.md                   # Brief project intro (mirrors docs/README.md)
```

*Notes*:
- The `docs/` folder contains all research and design documentation as required.
- The `architecture/adr/` directory holds each **Architecture Decision Record (ADR)**.
- Source code resides under `src/`.
- Configuration files (e.g., SA hyper‑parameters) live in `src/config/`.
- The `experiments/` directory is intentionally excluded from version control (see `.gitignore`) to keep the repository clean.