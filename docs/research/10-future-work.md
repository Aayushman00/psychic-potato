# Future Work

This section outlines potential extensions and research directions that build upon the completed optimisation framework.

## 1. Alternative Optimisation Algorithms
- **Hybrid Metaheuristics** – Combine simulated annealing with tabu search or genetic algorithms to escape deeper local minima while preserving the low runtime of SA.
- **Parallel / GPU‑accelerated SA** – Exploit the independence of multiple chains to run dozens of replicas concurrently on a GPU, improving the chance of finding the global optimum.
- **Exact Methods for Reduced Sub‑problems** – Apply branch‑and‑bound on clusters of notes (e.g., octave groups) and stitch solutions together using dynamic programming.

## 2. Richer Musical Models
- **Higher‑order Hyperedges** – Incorporate triadic and seventh‑chord weights derived from auditory roughness of three‑tone combinations, or from voice‑leading smoothness metrics.
- **Context‑Dependent Weights** – Allow W to vary with local harmonic context (e.g., weighting a fifth more strongly when it occurs within a tonic–dominant progression) using a simple hidden Markov model over chains of intervals.
- **Learning from Corpora** – While the current approach is deliberately corpus‑free, a semi‑supervised refinement could adjust W based on a modest annotated piano‑performance dataset, testing whether data‑driven tweaks improve playability without over‑fitting.

## 3. Extended Biomechanical Detail
- **Dynamic Finger Assignment** – Model each key as being playable by any finger, with a cost that reflects limb‑specific effort (e.g., thumb vs pinky reach). This turns the assignment problem into a *quadratic assignment with multiple alternatives* (QAP‑MA), solvable via specialised heuristics.
- **Muscle Fatigue & Recovery** – Introduce a time‑dependent cost that accumulates with repeated use of a particular finger or hand, encouraging layouts that spread load.
- **Touch‑Force Modelling** – Incorporate key‑specific actuation force profiles (measured via force sensors) to penalise layouts that require high force on weak fingers.

## 4. Alternative Input Devices
- **Ergonomic Keyboards** – Apply the same framework to split, contour, or ortholinear layouts (e.g., ErgoDox, Kinesis) by adjusting the coordinate set and finger‑hand map.
- **Touch Surfaces** – Replace the discrete key model with a continuous 2‑D surface, where C becomes a Fitts‑law cost over a planar Fitts task and W remains unchanged; the resulting problem is a continuous assignment problem amenable to gradient‑based methods.
- **Augmented Reality / Gestural Interfaces** – Map piano notes to mid‑air gestures, where C is derived from inverse kinematics of the upper limb and Fitts‑style models for 3D pointing.

## 5. Personalisation and Adaptation
- **Per‑User Calibration** – Allow end users to run a short 5‑minute tapping test to personalise the C‑matrix (their specific TP, w_x, w_y, etc.) and generate a tailor‑made layout.
- **Online Updating** – As a pianist practices on a layout, collect actual inter‑keystroke timing and infer adjustments to W (e.g., increase weight for frequently played transitions) to gradually optimise for the individual’s repertoire.

## 6. Formal Analysis and Hardness Proofs
- **Approximation Guarantees** – Investigate whether the specific structure of W (inverse of a metric derived from auditory dissonance) and C (derived from a Fitts‑type metric) yields a bounded‑ratio approximation via spectral or semidefinite relaxation.
- **Parameter Sensitivity Theorems** – Prove that, under reasonable bounds on the ERB‑based constants and Fitts parameters, the optimal mapping varies Lipschitz‑continuously with respect to those parameters, supporting robustness.

## 7. Extended Empirical Validation
- **Larger User Studies** – Test with 15–20 pianists of varied skill levels, spanning classical, jazz, and pop repertoires.
- **Longitudinal Learning** – Measure retention and transfer after weeks of practice on the optimised layout versus a standard layout, to assess whether the predicted reductions in motor cost translate into lasting skill benefits.
- **Cross‑Modal Evaluation** – Include measurements of electromyography (EMG) and keyboard‑force to directly verify that the predicted reduction in muscular load is realized in practice.

## 8. Toolkit and Distribution
- **Open‑Source Release** – Package the code (Python core, optional C++/CUDA kernels for SA acceleration) with a simple CLI: `pianokey opt --keyboard <layout.json> --output mapping.json`.
- **Web‑Based Configurator** – Provide a React/Vue frontend where users can select their keyboard model, hand size, and desired modifier layers, then instantly download the generated mapping and a printable cheat‑sheet.
- **Integration with MIDI Software** – Develop a lightweight MIDI translator that remaps incoming note‑on messages according to the produced layout, enabling real‑time testing with any DAW or virtual instrument.

## 9. Educational Outreach
- **Workshops** – Run short sessions at conservatories or maker fairs demonstrating how physics, psychoacoustics, and optimisation combine to produce a personalized keyboard layout.
- **Course Module** – Develop a teaching unit for human‑computer interaction or biomedical engineering classes that walks students through deriving W and C from first principles and applying a QAP solver.

## 10. Timeline (Indicative)
| Month | Milestone |
|-------|-----------|
| 0‑1   | Finalise documentation & code repository (completed) |
| 1‑2   | Implement core optimisation (SA) and calibration pipeline |
| 2‑3   | Generate MVP (25‑note) layout and internal benchmarks |
| 3‑4   | Conduct pilot user study (n=6) & collect feedback |
| 4‑5   | Refine C‑matrix based on study, extend to full 88‑key |
| 5‑6   | Execute larger user study (n=15) and analysis |
| 6‑7   | Prepare open‑source release, documentation, and demo video |
| 7‑8   | Submit results to a relevant venue (e.g., CHI, ISMIR, UIST) |
| 8+    | Maintain repo, address community contributions, explore extensions listed above |

*End of Future Work*.