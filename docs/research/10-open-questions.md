# Open Questions

This file records uncertainties or limitations discovered during research that merit further investigation but are outside the scope of the current implementation.  Any discovered contradictions with the mathematical formulation should be logged here first, per the implementation constraint.

## 1. Generalisation to Non‑Equal‑Tempered Tunings
- **Question**: Does the inverse‑dissonance formulation of W remain appropriate for just‑intonation, meantone, or other microtonal tunings?
- **Implication**: If yes, we would only need to replace the ratio \(r_{ij}=2^{\Delta_{ij}/12}\) with the appropriate frequency ratio for the target tuning.  If not, a more sophisticated model of consonance (e.g., including beating of higher‑order partials) might be required.
- **Related Work**: Preliminary tests with Pythagorean tuning show a monotonic mapping but the absolute values shift; further psychophysical validation needed.

## 2. Dynamic Finger Assignment
- **Question**: Should the keyboard state include *potential* finger assignments (i.e., allow a key to be played by any finger depending on context) rather than fixing a finger per key?
- **Implication**: This would enlarge the state space dramatically but could capture the fact that pianists often re‑assign fingers flexibly.  A possible solution is to keep the current fixed‑finger model and add a penalty for “awkward” fingerings that arises naturally from the C‑matrix (finger‑change penalty already models this).
- **Open**: Evaluate whether a model that permits flexible finger choice yields significantly lower objective values without exploding complexity.

## 3. Higher‑Order Musical Structure
- **Question**: Does restricting W to pairwise intervals miss important higher‑order constraints (e.g., chord voicings, voice‑leading smoothness) that are known to affect fingering?
- **Possible Extension**: Add hyper‑edge weights for triads or tetrachords, or introduce a term that penalises large variance in the mapping of pitch‑classes within a common chord across octaves.  However, the current pairwise model already captures a large proportion of consonance variance (r > 0.9 with perceptual ratings).  The benefit of added complexity must be weighed against simplicity and the risk of over‑fitting.
- **Open**: Experiment with a ternary term for major/minor triads and evaluate impact on playability in a user study.

## 4. Modifier Layer Representation
- **Question**: Are two modifier layers (none, Shift) sufficient, or should we model additional modifiers (Ctrl, Alt, OS‑specific keys) and layered combos?
- **Impact**: More layers increase M and thus the size of C, but the formulation naturally accommodates any number of layers.  The key is obtaining accurate modifier‑change costs (λ_m, κ_wm, etc.) for each combination.
- **Plan**: Collect data for the most common modifiers used in piano‑layout prototypes (Shift for uppercase, possibly Alt for “black‑key” emulation) before extending.

## 5. Validation of the Biomechanical Cost Model
- **Question**: Does the C matrix, derived from a simple Fitts‑plus‑posture model, accurately predict *sequential* movement costs encountered when playing realistic melodic passages (where anticipatory motion and muscle memory apply)?
- **Approach**: Compare predicted total movement time for a set of scales/arpeggios against motion‑capture measured times from pianists using the layout.  Address any systematic discrepancies with higher‑order terms (e.g., velocity profiles, muscle fatigue).
- **Open**: If systematic bias is found, consider augmenting C with a short‑range interaction term (e.g., cost depending on previous two moves).

## 6. Scalability to Full 88‑Key with Multiple Modifier Layers
- **Question**: Will the QAP remain tractable when M increases to several thousand (e.g., adding Ctrl, Alt, and layers for each hand)?
- **Mitigation**: Use sparsification – only keep keyboard states that are reachable within a comfortable biomechanical radius for each finger/hand; prune unreachable extreme combinations.
- **Open**: Benchmark the growth of solution quality vs. runtime as M scales; decide on a cutoff for practical deployment.

## 7. Subjective vs. Objective Metrics
- **Question**: Do reductions in the objective value (weighted sum of W·C) correlate linearly with perceived ease of playing, or are there diminishing returns?
- **Plan**: In the user study, collect both objective metrics (derived from C) and subjective ratings (NASA‑TLX, preference).  Perform regression analysis to quantify the relationship.
- **Open**: If correlation is weak, we may need to incorporate additional perceptually‑motivated terms (e.g., auditory feedback latency) into the objective.

## 8. Re‑Optimisation for Different Hand Sizes
- **Question**: Should the model be re‑parameterised for users with significantly smaller or larger hands (e.g., children vs. adults)?
- **Idea**: Scale the geometric coordinates (x, y) according to measured hand span, or adjust finger‑length parameters in the inverse‑kinematics model that informs D and postural terms.
- **Open**: Create a small parameter‑study to see how the optimal layout shifts with hand size; possibly provide a set of pre‑computed layouts for common size categories.

*End of Open Questions*.