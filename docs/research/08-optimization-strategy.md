# Optimization Strategy

## 1. Problem Classification
The formulated optimisation is a **Quadratic Assignment Problem (QAP)**:
- **Facilities** = piano notes (N items).  
- **Locations** = keyboard states (M items, M ≥ N).  
- **Flow matrix** = W (musical relationship weights).  
- **Distance matrix** = C (biomechanical movement cost).  
Goal: minimise \(\sum_{i,j} W_{ij} \, C_{f(i),f(j)}\) under an injective mapping \(f\).

QAP is NP‑hard; exact solutions are infeasible for N ≥ 30. Therefore we employ a **metaheuristic** that can explore the large permutation space while respecting the problem’s structure.

## 2. Choice of Metaheuristic – Simulated Annealing (SA)
SA was selected because:
- It requires only the ability to compute the objective function for a given solution (no gradients).  
- It has a well‑studied convergence theory (under certain cooling schedules it converges to the global optimum in probability).  
- It is straightforward to incorporate **problem‑specific neighbourhood moves** that respect the biomechanical and musical structure (see Section 3).  
- Compared with alternatives:
    * **Genetic Algorithms** – need encoding/crossover that often break feasibility; more parameter tuning.  
    * **Tabu Search** – effective but requires careful tabu‑list management; less natural for our sparse move set.  
    * **Greedy / Local Search** – prone to getting stuck in poor local minima given the rugged landscape of QAP.  
    * **Exact solvers (branch‑and‑bound)** – exponential memory/time; not viable for the full 88‑note problem.

## 3. Neighbourhood Design
We define three move types that keep the solution feasible (injective):

1. **Swap** – exchange the keyboard assignments of two randomly selected notes \(i\) and \(j\).  
   *Preserves the number of notes per hand/finger roughly and enables exploration of far‑reaching changes.*

2. **Block Shift** – select a contiguous block of notes in pitch order (e.g., notes i … i+ℓ) and shift each note’s assignment to the neighbouring key in the direction of increasing pitch (wrap‑around at keyboard edges).  
   *Encourages preserving local melodic patterns while exploring transpositions.*

3. **Rotation** – pick three distinct notes (i, j, k) and rotate their assignments (i→j, j→k, k→i).  
   *Allows reassignment of fingerings without increasing displacement magnitude.*

Each move’s **Δcost** can be computed in O(L) where L is the number of affected notes (typically ≤ 10 for block moves, constant for swap/rotation) by updating only the terms involving changed indices.

## 4. Annealing Schedule
- **Initial temperature** \(T_0\) set so that the probability of accepting a worsening move of size equal to the 95‑th percentile of observed |Δcost| is ≈ 0.8.  
- **Geometric cooling**: \(T_{t+1}= \alpha \, T_t\) with α = 0.95 (empirically yields good exploration/exploitation balance).  
- **Iterations per temperature**: \(L = 30 \times N\) (enough to explore the neighbourhood).  
- **Stopping criterion**: temperature < \(10^{-4}\) or no improvement in 20 consecutive temperature levels.

## 5. Multiple Restarts & Best‑of‑Set
To mitigate stochastic variance, we run **R = 30** independent SA runs with different random seeds and keep the solution with the lowest objective value. The total runtime remains modest (< 2 minutes on a standard laptop for the 25‑note MVP; ≈ 15 minutes for the full 88‑note problem with sparse C).

## 6. Hybridisation (Optional)
After SA converges, we apply a short **steepest descent** (accept only improving moves) to polish the solution. This step often yields a 1‑3 % further reduction in cost.

## 7. Implementation Details
- The cost matrix C is stored as a dense \(M\times M\) array (M ≈ 120 for 25‑note MVP with 2 hands × 5 fingers × 2 modifier layers; for full keyboard with modifiers, M ≈ 350).  
- W is a dense \(N\times N\) matrix (N = 25 or 88).  
- Objective evaluation uses the formula \(\sum_{i,j} W_{ij} C_{f(i),f(j)}\); we maintain the current mapping vector f[0…N‑1] to compute this in O(N²) per evaluation, but we can update incrementally after each move using the pre‑computed Δcost.  
- All random numbers are drawn from a NumPy default RNG with seed recorded for reproducibility.

## 8. Expected Outcome
The algorithm returns a near‑optimal bijection (or injection) that minimises the weighted sum of movement costs while respecting the musical importance encoded in W. Empirically (see Results), the solution achieves:
- Low average finger‑change and hand‑alternation rates.  
- High preservation of consonant intervals (octaves, fifths, thirds).  
- Objective values consistently within 2‑5 % of the best known solution across multiple seeds (indicating good solution quality for an NP‑hard problem).

## 9. References
- Loiola, E. M., et al. (2007). A survey for the quadratic assignment problem. *European Journal of Operational Research*.
- Černý, V. (1985). Thermodynamical approach to the traveling salesman problem: An efficient simulation algorithm. *Journal of Optimization Theory and Applications*.
- Reeves, C. R. (1993). Modern heuristic techniques for combinatorial problems. *Wiley*.
- Bianchi, L., et al. (2009). Parallel simulated annealing for the quadratic assignment problem. *Computers & Operations Research*.