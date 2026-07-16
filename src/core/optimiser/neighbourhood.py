"""
Neighbourhood operators for the Simulated Annealing optimiser.
"""
from __future__ import annotations
import random
from typing import Tuple, List

def random_swap(n: int) -> Tuple[str, Tuple[int, int]]:
    i = random.randrange(n)
    j = random.randrange(n)
    while j == i:
        j = random.randrange(n)
    return ("swap", (i, j))

def random_block_shift(n: int, max_length: float) -> Tuple[str, Tuple[int, int, int]]:
    """
    max_length: proportion of n (0<max_length<=1) giving the maximum block size.
    """
    if max_length <= 0.0:
        max_length = 0.1
    max_len = max(1, int(n * max_length))
    length = random.randint(2, max_len)  # block size at least 2 to make a change
    start = random.randrange(n)
    direction = random.choice([-1, 1])
    return ("block_shift", (start, length, direction))

def random_rotation(n: int) -> Tuple[str, Tuple[int, int, int]]:
    indices = random.sample(range(n), 3)
    i, j, k = indices
    return ("rotation", (i, j, k))

def random_move(n: int, max_length: float) -> Tuple[str, tuple]:
    """Pick a move type according to default probabilities."""
    # probabilities could be passed as argument; for now use fixed weights
    r = random.random()
    if r < 0.5:
        return random_swap(n)
    elif r < 0.8:
        return random_block_shift(n, max_length)
    else:
        return random_rotation(n)