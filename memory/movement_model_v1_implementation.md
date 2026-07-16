---
name: movement_model_v1_implementation
description: Implementation of Version 1 ergonomic movement model for keyboard layout optimization.
metadata:
  type: project
---

## Summary
Implemented Version 1 of the ergonomic movement model as part of the keyboard layout optimization project. This model assigns principled costs to primitive ergonomic actions (same finger, finger change, hand shift, modifier toggle) based on biomechanical reasoning.

## Changes Made
1. Created `src/core/movement_model.py` containing the `MovementModel` class that loads ergonomic costs from a YAML configuration and applies them to a semantic keyboard graph.
2. Created `config/movement_model.yaml` with default values:
   - same_finger: 1.0 (baseline - sliding same finger to adjacent key)
   - finger_change: 1.8 (switching fingers - more neuromuscular coordination)
   - hand_shift: 2.5 (lateral hand movement - arm/forearm involvement)
   - modifier_toggle: 1.2 (modifier press/release - extra coordination)
   - scale: 1.0 (global multiplier)
3. Updated `src/core/kb_builder.py` function `build_cost_matrix` to delegate to `MovementModel` instead of using placeholder unit weights.
4. Added comprehensive unit tests in `tests/test_movement_model.py` verifying:
   - Proper loading of default weights and ordering (same_finger < finger_change < hand_shift)
   - Correct application of weights to the semantic graph
   - Shortest path computations respecting the weights
   - Modifier toggle cost isolation
   - Scaling behavior with custom configuration
5. Verified that existing tests remain compatible (they use random cost matrices).

## Architecture Preserved
- The overall QAP formulation remains unchanged.
- The `Objective` class and optimizer (`SimulatedAnnealing`) are untouched.
- The `KeyboardGraph` abstraction remains the same; only edge weights are now derived from the movement model.
- Keyboard state representation (`KeyboardState`) unchanged.

## Next Steps
- Run the optimizer with the new movement model to generate a 61-key layout (`mapping_61_v1.json`).
- Analyze the resulting layout for ergonomic properties (hand balance, modifier usage, etc.).
- Iterate on the movement model based on empirical results (Milestone 2C).

## Verification
- Unit tests for the movement model pass.
- Integration with the existing build pipeline confirmed via import checks.
- No breaking changes to existing interfaces.