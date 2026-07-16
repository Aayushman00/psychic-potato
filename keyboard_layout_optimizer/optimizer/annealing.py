import math
import random
import time
from typing import Dict, List

from .optimizer import OptimizationResult, Optimizer
from .objective import Objective
from ..models.keyboard import KeyboardKey
from ..models.mapping import Mapping, baseline_sequential_mapping
from ..models.piano import PianoNote


class SimulatedAnnealing(Optimizer):
    def optimize(
        self,
        keyboard: List[KeyboardKey],
        piano: List[PianoNote],
        objective: Objective,
        config: Dict,
        seed: int,
    ) -> OptimizationResult:
        random.seed(seed)
        start_time = time.time()

        current_mapping = baseline_sequential_mapping(piano, keyboard)
        current_score = objective.score(current_mapping)
        best_mapping = Mapping.from_assignment(current_mapping.assignment, piano, keyboard)
        best_score = current_score

        temperature = config["initial_temperature"]
        cooling_rate = config["cooling_rate"]
        iterations = config["iterations"]
        history = []
        accepted = 0
        rejected = 0

        note_labels = [note.label() for note in piano]

        for iteration in range(1, iterations + 1):
            candidate = Mapping.from_assignment(current_mapping.assignment, piano, keyboard)
            note_a, note_b = random.sample(note_labels, 2)
            key_a = candidate.assignment[note_a]
            key_b = candidate.assignment[note_b]
            candidate.assign(note_a, key_b)
            candidate.assign(note_b, key_a)

            candidate_score = objective.score(candidate)
            delta = candidate_score - current_score
            accepted_move = delta < 0 or random.random() < math.exp(-delta / max(temperature, 1e-8))

            if accepted_move:
                current_mapping = candidate
                current_score = candidate_score
                accepted += 1
                if candidate_score < best_score:
                    best_mapping = Mapping.from_assignment(candidate.assignment, piano, keyboard)
                    best_score = candidate_score
            else:
                rejected += 1

            temperature *= cooling_rate
            history.append(
                {
                    "iteration": iteration,
                    "temperature": temperature,
                    "current_score": current_score,
                    "best_score": best_score,
                    "accepted": accepted,
                    "rejected": rejected,
                }
            )

        runtime_seconds = time.time() - start_time
        return OptimizationResult(
            best_mapping=best_mapping,
            best_score=best_score,
            history=history,
            accepted=accepted,
            rejected=rejected,
            runtime_seconds=runtime_seconds,
            metadata={"seed": seed, "algorithm": "simulated_annealing", "iterations": iterations},
        )
