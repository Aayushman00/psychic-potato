"""
Tests for the Movement Model (Version 1).
"""
import numpy as np
import pytest
from pathlib import Path

from src.core.kb_builder import KeyboardState
from src.core.movement_model import MovementModel
from src.core.keyboard_graph import EdgeType, build_semantic_keyboard_graph


def test_movement_model_loads_defaults():
    model = MovementModel()
    # Check that all expected edge types have positive weights
    assert model.weight(EdgeType.SAME_FINGER) > 0
    assert model.weight(EdgeType.FINGER_CHANGE) > model.weight(EdgeType.SAME_FINGER)
    assert model.weight(EdgeType.HAND_SHIFT) > model.weight(EdgeType.FINGER_CHANGE)
    assert model.weight(EdgeType.MODIFIER_TOGGLE) > 0
    # Optional: ensure ordering matches expectations
    assert model.weight(EdgeType.SAME_FINGER) < model.weight(EdgeType.FINGER_CHANGE)
    assert model.weight(EdgeType.FINGER_CHANGE) < model.weight(EdgeType.HAND_SHIFT)


def test_model_applies_weights_to_graph():
    # three states differing in finger, hand, modifier
    s1 = KeyboardState("A", 0.0, 0.0, "index", "L", False)
    s2 = KeyboardState("B", 0.0, 0.0, "index", "L", True)   # same finger/hand, diff modifier
    s3 = KeyboardState("C", 0.0, 0.0, "middle", "L", False) # diff finger, same hand
    s4 = KeyboardState("D", 0.0, 0.0, "index", "R", False)  # diff hand
    states = [s1, s2, s3, s4]
    model = MovementModel()
    graph = model.build_weighted_graph(states)
    # retrieve weights via graph.weight(i,j)
    w_sf = model.weight(EdgeType.SAME_FINGER)
    w_fc = model.weight(EdgeType.FINGER_CHANGE)
    w_hs = model.weight(EdgeType.HAND_SHIFT)
    w_mt = model.weight(EdgeType.MODIFIER_TOGGLE)
    # same finger (s1 vs s2? actually same finger & hand, diff modifier -> not same finger)
    # need a pair with same finger, hand, modifier: s1 and a clone? Let's create a specific pair.
    # For simplicity, we test known pairs:
    # Modifier toggle: s1-s2
    assert graph.weight(0, 1) == pytest.approx(w_mt, rel=1e-6)
    # Finger change: s1-s3 (same hand, diff finger)
    assert graph.weight(0, 2) == pytest.approx(w_fc, rel=1e-6)
    # Hand shift: s1-s4 (same finger, diff hand)
    assert graph.weight(0, 3) == pytest.approx(w_hs, rel=1e-6)
    # Ensure symmetry
    assert graph.weight(1, 0) == pytest.approx(w_mt, rel=1e-6)
    assert graph.weight(2, 0) == pytest.approx(w_fc, rel=1e-6)
    assert graph.weight(3, 0) == pytest.approx(w_hs, rel=1e-6)


def test_shortest_path_respects_weights():
    # Create a line of three states where we can manipulate direct edge weight
    s_a = KeyboardState("A", 0.0, 0.0, "index", "L", False)
    s_b = KeyboardState("B", 0.0, 0.0, "middle", "L", False)  # finger change from A to B
    s_c = KeyboardState("C", 0.0, 0.0, "ring", "L", False)   # finger change from B to C
    states = [s_a, s_b, s_c]
    model = MovementModel()
    graph = model.build_weighted_graph(states)
    # By default, all edges have weight according to their type (finger_change = 1.8 * scale)
    # Let's override direct A-C edge to be very high, forcing path A-B-C
    # Note: A and C differ by two finger steps? Actually A index -> C ring, still finger change.
    # We'll manually set weight to large number.
    high_weight = 100.0
    graph.set_edge_weight(0, 2, high_weight)
    dist = graph.distance_matrix()
    # Expected: A-B weight, B-C weight, A-C via B = sum of two finger changes
    w_fc = model.weight(EdgeType.FINGER_CHANGE)
    assert dist[0, 1] == pytest.approx(w_fc, rel=1e-6)
    assert dist[1, 2] == pytest.approx(w_fc, rel=1e-6)
    assert dist[0, 2] == pytest.approx(2 * w_fc, rel=1e-6)  # via B
    # Ensure direct high weight not used
    assert dist[0, 2] < high_weight / 2  # definitely less than direct


def test_modifier_toggle_cost():
    s1 = KeyboardState("ShiftOff", 0.0, 0.0, "index", "L", False)
    s2 = KeyboardState("ShiftOn", 0.0, 0.0, "index", "L", True)
    states = [s1, s2]
    model = MovementModel()
    graph = model.build_weighted_graph(states)
    w_mt = model.weight(EdgeType.MODIFIER_TOGGLE)
    assert graph.weight(0, 1) == pytest.approx(w_mt, rel=1e-6)
    # distance matrix should be same as direct edge (only two nodes)
    dist = graph.distance_matrix()
    assert dist[0, 1] == pytest.approx(w_mt, rel=1e-6)


def test_custom_config_scales():
    # create a temporary yaml file with custom scale
    import tempfile
    import yaml
    content = """
scale: 2.0
same_finger: 1.0
finger_change: 1.8
hand_shift: 2.5
modifier_toggle: 1.2
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        model = MovementModel(Path(fname))
        # weights should be doubled
        assert model.weight(EdgeType.SAME_FINGER) == pytest.approx(2.0, rel=1e-6)
        assert model.weight(EdgeType.FINGER_CHANGE) == pytest.approx(3.6, rel=1e-6)
        assert model.weight(EdgeType.HAND_SHIFT) == pytest.approx(5.0, rel=1e-6)
        assert model.weight(EdgeType.MODIFIER_TOGGLE) == pytest.approx(2.4, rel=1e-6)
    finally:
        import os
        os.unlink(fname)
