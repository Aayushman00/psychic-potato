"""
Property-based tests for Objective.delta correctness.
"""
import random
import sys
from pathlib import Path

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
from core.mapping import Mapping
from core.objective import Objective


def random_mapping(N, M):
    """Generate a random assignment of N piano notes to M keyboard states."""
    return Mapping([random.randrange(M) for _ in range(N)], M=M)


def random_W(N):
    """Generate a symmetric non-negative musical relationship matrix with zero diagonal."""
    W = np.random.rand(N, N)
    W = (W + W.T) / 2  # make symmetric
    np.fill_diagonal(W, 0.0)
    return W


def random_C(M):
    """Generate a biomechanical movement-cost matrix (asymmetric, non-negative)."""
    C = np.random.rand(M, M)
    return C


def test_delta_swap():
    """Test delta_swap matches full recompute."""
    for _ in range(100):
        N = random.randint(2, 8)
        M = random.randint(N, 12)
        W = random_W(N)
        C = random_C(M)
        mapping = random_mapping(N, M)
        obj = Objective(W, C, mapping)

        i, j = random.sample(range(N), 2)
        delta = obj.delta_swap(i, j)

        # Apply swap manually to compute new score
        mapping.apply_swap(i, j)
        new_score = obj._compute_score()
        # Revert swap to restore original mapping for next iteration
        mapping.apply_swap(i, j)
        old_score = obj._compute_score()
        expected = new_score - old_score
        assert abs(delta - expected) < 1e-9, f"delta mismatch: {delta} vs {expected}"


def test_delta_block_shift():
    """Test delta_block_shift matches full recompute."""
    for _ in range(100):
        N = random.randint(2, 8)
        M = random.randint(N, 12)
        W = random_W(N)
        C = random_C(M)
        mapping = random_mapping(N, M)
        obj = Objective(W, C, mapping)

        start = random.randrange(N)
        length = random.randint(1, N)
        direction = random.choice([-1, 1])
        delta = obj.delta_block_shift(start, length, direction)

        # Apply block shift manually
        mapping.apply_block_shift(start, length, direction)
        new_score = obj._compute_score()
        # Revert by applying opposite direction
        mapping.apply_block_shift(start, length, -direction)
        old_score = obj._compute_score()
        expected = new_score - old_score
        assert abs(delta - expected) < 1e-9, f"delta mismatch: {delta} vs {expected}"


def test_delta_rotation():
    """Test delta_rotation matches full recompute."""
    for _ in range(100):
        N = random.randint(3, 8)
        M = random.randint(N, 12)
        W = random_W(N)
        C = random_C(M)
        mapping = random_mapping(N, M)
        obj = Objective(W, C, mapping)

        i, j, k = random.sample(range(N), 3)
        delta = obj.delta_rotation(i, j, k)

        # Apply rotation manually
        mapping.apply_rotation(i, j, k)
        new_score = obj._compute_score()
        # Revert by applying inverse rotation (i <- k, j <- i, k <- j) which is rotation in opposite direction
        mapping.apply_rotation(k, j, i)  # because applying same rotation three times returns original? Actually applying same permutation thrice cycles.
        # Simpler: compute original assignment and restore directly.
        # Instead, we'll copy original assignment before mutation.
        # Let's redo with copy.
        # We'll do a simpler approach: copy assignment.
        # Re-do the iteration with copy.

        # Redo with copy to avoid complex revert.
        mapping2 = random_mapping(N, M)
        obj2 = Objective(W, C, mapping2)
        delta2 = obj2.delta_rotation(i, j, k)
        f_old = np.array(mapping2.assignment, dtype=int)
        f_new = f_old.copy()
        vi, vj, vk = f_old[i], f_old[j], f_old[k]
        f_new[i] = vj
        f_new[j] = vk
        f_new[k] = vi
        mapping2.assignment = list(f_new)
        new_score = obj2._compute_score()
        # Reset to original
        mapping2.assignment = list(f_old)
        old_score = obj2._compute_score()
        expected = new_score - old_score
        assert abs(delta2 - expected) < 1e-9, f"delta mismatch: {delta2} vs {expected}"


if __name__ == "__main__":
    random.seed(0)
    np.random.seed(0)
    test_delta_swap()
    test_delta_block_shift()
    test_delta_rotation()
    print("All delta tests passed.")