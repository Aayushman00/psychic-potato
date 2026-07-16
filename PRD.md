# Product Requirements Document: Ergonomic QWERTY Piano Layout Optimizer

## 1. Overview

This product generates and evaluates ergonomic mappings from piano notes to laptop keyboard keys. Unlike standard virtual piano tools that preserve visual or chromatic row order, this product optimizes for physical playability, biomechanical comfort, octave consistency, and hardware feasibility.

The core product is an optimization engine plus visualization interface for designing digital musical instrument layouts on QWERTY keyboards.

## 2. Problem Statement

Existing virtual piano mappings in DAWs and standalone tools typically assign piano notes sequentially across QWERTY rows. These layouts are easy to understand visually but do not optimize for human motor comfort, octave muscle memory, finger independence, hand balance, or laptop key rollover constraints.

The product addresses a topological assignment problem: embedding piano relationships into a staggered laptop keyboard grid while minimizing ergonomic distortion and strain.

## 3. Goals

- Generate playable QWERTY piano layouts using formal ergonomic constraints.
- Preserve important piano relationships, especially chromatic adjacency and octave equivalence.
- Minimize biomechanical strain, especially ring-pinky alternation and excessive pinky reach.
- Avoid common hardware ghosting patterns for chords.
- Provide measurable layout scores so generated mappings can be compared.
- Support an MVP path that validates the objective function before attempting a full 88-key mapping.

## 4. Non-Goals

- Replacing professional MIDI controllers or acoustic/digital pianos.
- Modeling expressive velocity from laptop key pressure in the first release.
- Producing a perfect globally optimal mapping through exhaustive search.
- Supporting every international keyboard layout in the MVP.
- Building a full DAW or notation editor.

## 5. Target Users

- Musicians who want to practice or compose on a laptop keyboard.
- HCI researchers studying digital musical instruments.
- Algorithmic optimization developers interested in ergonomic layout generation.
- Experimental instrument designers.
- Keyboard layout enthusiasts familiar with projects such as Colemak, Workman, or Carpalx.

## 6. MVP Scope

The MVP should optimize a smaller 61-key, five-octave playable prototype before expanding to a full 88-key layout. This lowers implementation risk and allows the ergonomic objective function to be tested quickly.

### MVP Includes

- A modeled QWERTY keyboard as staggered 2D coordinates.
- A modeled piano note graph for 61 notes.
- Simulated annealing optimizer.
- Cost function with ergonomic and musical-structure penalties.
- Static export of the generated mapping.
- Visualization of note-to-key assignments.
- Evaluation report comparing generated layout against a sequential baseline.

### MVP Excludes

- Full 88-key mapping.
- Modifier-layer optimization.
- Real-time MIDI output.
- User-specific hand calibration.
- Full keyboard ghosting database per laptop model.

## 7. Future Scope

- Full 88-key support using modifier layers.
- MIDI input/output integration.
- Per-user hand size and keyboard model calibration.
- Genetic algorithm and tabu-search comparison modes.
- Hardware matrix configuration for specific laptop or external keyboards.
- Velocity approximation using timing, repeated-key behavior, or optional external input.
- Interactive layout editor with manual pinning constraints.

## 8. Functional Requirements

### Keyboard Model

- The system must represent physical QWERTY keys as Cartesian coordinates.
- The model must account for row staggering.
- Each key must include metadata:
  - Key label
  - Row
  - Column or approximate x-position
  - Assigned hand
  - Assigned finger
  - Optional hardware matrix group
  - Whether the key requires a modifier layer

### Piano Model

- The system must represent piano notes as indexed pitch nodes.
- The model must include chromatic adjacency edges between note `i` and note `i + 1`.
- The model must include octave equivalence edges between note `i` and note `i + 12`.
- Each note must include metadata:
  - MIDI number or relative pitch index
  - Pitch name
  - Octave
  - White-key or black-key class

### Optimization Engine

- The system must assign every modeled piano note to exactly one keyboard state.
- The system must prevent assigning multiple piano notes to the same keyboard state.
- The optimizer should use simulated annealing for the MVP.
- The optimizer must support repeatable runs using a random seed.
- The optimizer must expose configurable penalty weights.
- The optimizer must compare candidate mappings using a total objective score.

### Cost Function

The objective function must include:

- Absolute placement penalty for assigning important notes to awkward keys.
- Physical distance penalty for structurally related notes.
- Octave consistency penalty when octave distances vary across the layout.
- Finger strain penalty for awkward adjacent-note assignments.
- Hand crossing penalty when lower pitches are placed significantly right of higher pitches.
- Modifier overload penalty for frequently used middle-octave notes.
- Hardware ghosting penalty for likely triad conflicts.

### Visualization

- The system must display the keyboard layout with each assigned note.
- The system must distinguish note pitch classes visually.
- The system must show unassigned keys.
- The system must show summary scores for the current layout.
- The system should allow comparison between optimized and sequential baseline layouts.

### Export

- The system must export mappings as JSON.
- The system should export mappings as CSV.
- The exported mapping must include keyboard key, note name, note index, octave, and modifier state.

## 9. Mathematical Formulation

Let `i in {1, ..., N}` represent piano notes.

Let `j in {1, ..., K}` represent keyboard states, including modifier combinations when supported.

Let `x_ij` be a boolean assignment variable where `x_ij = 1` if piano note `i` is assigned to keyboard state `j`.

Constraints:

```text
sum_j x_ij = 1 for every piano note i
sum_i x_ij <= 1 for every keyboard state j
```

Objective:

```text
minimize Z =
  sum_i sum_j C_ij * x_ij
  + sum_i sum_k sum_j sum_l P(i, k) * D(j, l) * x_ij * x_kl
```

Where:

- `C_ij` is the absolute placement penalty.
- `P(i, k)` is the structural relationship weight between piano notes.
- `D(j, l)` is the physical ergonomic distance or strain between keyboard states.

## 10. Evaluation Metrics

- Adjacency preservation: percentage of chromatic neighbors placed on physically adjacent or low-distance keys.
- Octave consistency: variance in physical distance between all `i` and `i + 12` note pairs.
- Max isotonic stretch: maximum single-hand distance required to play an octave.
- Hand balance: variance in workload and travel distance between left and right hand.
- Finger strain score: penalty accumulation for high-risk finger combinations.
- Ghosting risk score: count or weighted score of common chord shapes mapped to risky hardware groups.
- Baseline improvement: percent improvement against a sequential virtual-piano mapping.

## 11. User Stories

- As a musician, I want a laptop-keyboard piano layout that is more comfortable than a standard sequential mapping.
- As a researcher, I want objective metrics so I can compare layout quality across optimization runs.
- As a developer, I want configurable penalty weights so I can test different ergonomic assumptions.
- As an instrument designer, I want octave relationships preserved so repeated musical shapes feel consistent.
- As a user with a normal laptop keyboard, I want common chords to avoid ghosting where possible.

## 12. UX Requirements

- The first screen should show the generated keyboard mapping, not a marketing or explanatory landing page.
- The layout view should make pitch direction easy to scan from low to high.
- The user should be able to switch between optimized and baseline mappings.
- Scores should be visible beside the layout.
- Penalty weights should be adjustable in an advanced settings panel.
- Export actions should be clearly available from the main interface.

## 13. Technical Requirements

- The optimizer should be implemented so the objective evaluator can later be moved to C, Rust, or another low-level language if performance requires it.
- The MVP may use a high-level language for speed of iteration.
- Data models should be serializable to JSON.
- The optimizer should support millions of candidate evaluations in long-running local experiments.
- The system should maintain deterministic behavior when supplied with the same seed and configuration.

## 14. Risks

- The cost function may optimize mathematically valid but musically unintuitive layouts.
- Laptop keyboard geometry varies across devices.
- Hardware matrix ghosting behavior is not standardized.
- Without a musical corpus, frequency assumptions may underrepresent real playing behavior.
- Binary laptop keys cannot naturally represent velocity.
- Full 88-key mapping may require modifier usage that reduces playability.

## 15. Open Questions

- Should the first validated prototype remain a 25-key two-octave layout, or should it immediately include an 88-key modifier-layer mode?
- How important is preserving black-key and white-key topology on a flat keyboard?
- Should the optimizer incorporate common musical patterns, or remain corpus-free and topology-driven?
- How should velocity be approximated, if at all?
- Should users be able to pin certain notes to certain keys before optimization?

## 16. Success Criteria

The MVP is successful if:

- It generates a complete 61-note mapping with no duplicate key assignments.
- It produces a lower total ergonomic score than a sequential baseline.
- It improves chromatic adjacency preservation or octave consistency over the baseline.
- It exports a valid JSON mapping.
- A user can visually inspect the layout and understand which key plays each note.
- The optimizer can run multiple seeded experiments and produce comparable score reports.

## 17. Reference Concepts

- Fitts's Law for movement-time and target-distance modeling.
- Quadratic Assignment Problem for assignment with pairwise relationship costs.
- Graph embedding for mapping piano topology into keyboard topology.
- Carpalx-style simulated annealing for keyboard layout optimization.
- QMK firmware concepts for key rollover, ghosting, and keyboard matrix constraints.
