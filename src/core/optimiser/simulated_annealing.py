"""
Simulated Annealing optimiser for the QAP formulation.
"""
from __future__ import annotations
import random
import math
import time
from typing import Callable, Tuple, List
import numpy as np

from ..mapping import Mapping
from ..objective import Objective
from .neighbourhood import random_move

class SimulatedAnnealing:
    def __init__(
        self,
        objective: Objective,
        *,
        t0: float | None = None,
        t_min: float = 1e-4,
        alpha: float = 0.95,
        iterations_per_temp: int | None = None,
        max_restarts: int = 1,
        seed: int | None = None,
        callback: Callable[[int, float, float], None] | None = None,
    ):
        """
        Parameters
        ----------
        objective : Objective
            The QAP objective (holds W, C and current mapping).
        t0 : float, optional
            Initial temperature. If None, set to 0.8 * max|Δcost| observed
            during a short pilot.
        t_min : float
            Stop when temperature drops below this.
        alpha : float
            Geometric cooling factor (T_{k+1} = alpha * T_k).
        iterations_per_temp : int, optional
            Number of move attempts per temperature. If None, set to 30 * N.
        max_restarts : int
            Number of independent runs (different random seeds) to perform.
        seed : int, optional
            Base seed for reproducibility; each restart uses seed + run_idx.
        callback : function(iteration, temperature, best_score) -> None, optional
            Called after each temperature level.
        """
        self.obj = objective
        self.N = objective.N
        self.M = objective.M
        self.t_min = t_min
        self.alpha = alpha
        self.max_restarts = max_restarts
        self.base_seed = seed if seed is not None else int(time.time())
        self.callback = callback

        if iterations_per_temp is None:
            self.iterations_per_temp = 30 * self.N
        else:
            self.iterations_per_temp = int(iterations_per_temp)

        if t0 is None:
            self.t0 = self._estimate_initial_temperature()
        else:
            self.t0 = float(t0)

    def _estimate_initial_temperature(self) -> float:
        """Run a small number of random moves to gauge typical |Δcost|."""
        deltas = []
        for _ in range(min(100, self.N * 10)):
            move_type, args = random_move(self.N, max_length=0.2)
            delta = self.obj.delta(move_type, *args)
            deltas.append(abs(delta))
        if not deltas:
            return 1.0
        median_delta = float(np.median(deltas))
        # set temperature so that a worsening move of median delta is accepted with prob ~0.8
        # p = exp(-delta / T) => T = -delta / ln(p)
        if median_delta == 0:
            return 1.0
        t0 = -median_delta / math.log(0.8)
        return max(t0, 1e-3)

    def _run_once(self, start_seed: int) -> Tuple[Mapping, float]:
        random.seed(start_seed)
        # reset objective to a fresh random start? We'll keep the current mapping but shuffle.
        # For simplicity, we create a random permutation of assignment.
        init = random.sample(range(self.M), self.N)
        self.obj.mapping = Mapping(init, self.M)
        self.obj._update_score()

        T = self.t0
        iteration = 0
        while T > self.t_min:
            for _ in range(self.iterations_per_temp):
                move_type, args = random_move(self.N, max_length=0.2)
                if not self._move_preserves_injectivity(move_type, args):
                    iteration += 1
                    continue
                delta = self.obj.delta(move_type, *args)
                if delta < 0 or random.random() < math.exp(-delta / T):
                    self.obj.apply_move(move_type, *args)
                iteration += 1
            if self.callback:
                self.callback(iteration, T, self.obj.score)
            T *= self.alpha
        return self.obj.mapping.copy(), self.obj.score

    def _move_preserves_injectivity(self, move_type: str, args: tuple) -> bool:
        f_new = self.obj.mapping.assignment.copy()
        if move_type == "swap":
            i, j = map(int, args)
            f_new[i], f_new[j] = f_new[j], f_new[i]
        elif move_type == "block_shift":
            start, length, direction = map(int, args)
            start = start % self.N
            for offset in range(length):
                idx = (start + offset) % self.N
                f_new[idx] = (f_new[idx] + direction) % self.M
        elif move_type == "rotation":
            i, j, k = map(int, args)
            if len({i, j, k}) < 3:
                return True
            vi, vj, vk = f_new[i], f_new[j], f_new[k]
            f_new[i] = vj
            f_new[j] = vk
            f_new[k] = vi
        return len(set(f_new)) == len(f_new)

    def optimize(self) -> Tuple[Mapping, float]:
        best_mover: Mapping | None = None
        best_score = float("inf")
        for r in range(self.max_restarts):
            seed = self.base_seed + r if self.base_seed is not None else None
            mapping, score = self._run_once(seed)
            if score < best_score:
                best_score = score
                best_mover = mapping.copy()
        # restore best mapping into objective (optional)
        self.obj.mapping = best_mover.copy()
        self.obj._update_score()
        return best_mover, best_score
