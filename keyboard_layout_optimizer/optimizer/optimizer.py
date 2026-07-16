from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Optional

from ..models.keyboard import KeyboardKey
from ..models.piano import PianoNote
from .objective import Objective


class OptimizationResult:
    def __init__(
        self,
        best_mapping,
        best_score: float,
        history: list[Dict[str, float]],
        accepted: int,
        rejected: int,
        runtime_seconds: float,
        metadata: Optional[Dict] = None,
    ):
        self.best_mapping = best_mapping
        self.best_score = best_score
        self.history = history
        self.accepted = accepted
        self.rejected = rejected
        self.runtime_seconds = runtime_seconds
        self.metadata = metadata or {}


class Optimizer(ABC):
    @abstractmethod
    def optimize(
        self,
        keyboard: list[KeyboardKey],
        piano: list[PianoNote],
        objective: Objective,
        config: Dict,
        seed: int,
    ) -> OptimizationResult:
        raise NotImplementedError
