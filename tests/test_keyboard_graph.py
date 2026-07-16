"""
Tests for keyboard graph and movement cost matrix.
"""
import numpy as np
import pytest

from src.core.kb_builder import KeyboardState
from src.core.keyboard_graph import (
    KeyboardGraph,
    EdgeType,
    build_semantic_keyboard_graph,
    set_edge_weights_by_type,
    build_movement_cost_matrix,
    _edge_type_for,
)


def test_edge_type_assignment():
    s1 = KeyboardState("A", 0.0, 0.0, "index", "L", False)
    s2 = KeyboardState("B", 0.0, 0.0, "index", "L", True)   # same finger/hand, diff modifier
    s3 = KeyboardState("C", 0.0, 0.0, "middle", "L", False) # diff finger, same hand
    s4 = KeyboardState("D", 0.0, 0.0, "index", "R", False)  # diff hand
    assert _edge_type_for(s1, s2) == EdgeType.MODIFIER_TOGGLE
    assert _edge_type_for(s1, s3) == EdgeType.FINGER_CHANGE
    assert _edge_type_for(s1, s4) == EdgeType.HAND_SHIFT
    s5 = KeyboardState("E", 1.0, 0.0, "index", "L", False)  # same finger/hand, diff position
    assert _edge_type_for(s1, s5) == EdgeType.SAME_FINGER


def test_graph_construction_and_edge_types():
    states = [
        KeyboardState("K0", 0.0, 0.0, "index", "L", False),
        KeyboardState("K1", 0.0, 0.0, "index", "L", True),
        KeyboardState("K2", 0.0, 0.0, "middle", "L", False),
    ]
    graph = build_semantic_keyboard_graph(states)
    assert graph.edge_type(0, 1) == EdgeType.MODIFIER_TOGGLE
    assert graph.edge_type(0, 2) == EdgeType.FINGER_CHANGE
    # (1,2): modifier differs, finger differs, hand same -> modifier takes priority
    assert graph.edge_type(1, 2) == EdgeType.MODIFIER_TOGGLE


def test_weight_setting_and_shortest_path():
    states = [
        KeyboardState("A", 0.0, 0.0, "index", "L", False),
        KeyboardState("B", 0.0, 0.0, "middle", "L", False),
        KeyboardState("C", 0.0, 0.0, "ring", "L", False),
    ]
    graph = build_semantic_keyboard_graph(states)
    # Assign weights: finger change = 1, others default 1
    w_map = {
        EdgeType.FINGER_CHANGE: 1.0,
        EdgeType.SAME_FINGER: 1.0,
        EdgeType.HAND_SHIFT: 1.0,
        EdgeType.MODIFIER_TOGGLE: 1.0,
    }
    set_edge_weights_by_type(graph, w_map)
    # Make direct A-C edge expensive
    graph.set_edge_weight(0, 2, 10.0)
    dist = graph.distance_matrix()
    assert dist[0, 1] == pytest.approx(1.0)
    assert dist[1, 2] == pytest.approx(1.0)
    assert dist[0, 2] == pytest.approx(2.0)  # via B
    # symmetry
    assert dist[1, 0] == pytest.approx(1.0)
    assert dist[2, 1] == pytest.approx(1.0)
    assert dist[2, 0] == pytest.approx(2.0)


def test_build_movement_cost_matrix_default_weights():
    states = [
        KeyboardState("S0", 0.0, 0.0, "index", "L", False),
        KeyboardState("S1", 0.0, 0.0, "middle", "L", False),
        KeyboardState("S2", 0.0, 0.0, "ring", "L", False),
    ]
    cm = build_movement_cost_matrix(states)
    # default weight = 1 for every edge => complete graph with weight 1 => distance 1 between distinct nodes
    expected = np.array([
        [0., 1., 1.],
        [1., 0., 1.],
        [1., 1., 0.],
    ])
    np.testing.assert_allclose(cm, expected, rtol=1e-6)


def test_set_edge_weights_by_type_missing_type():
    # ensure unknown EdgeType defaults to 1.0 via set_edge_weights_by_type?
    # Our function uses weight_map.get(etype, 1.0) so missing yields 1.0.
    states = [KeyboardState("X", 0, 0, "index", "L", False), KeyboardState("Y", 0, 0, "middle", "L", False)]
    graph = build_semantic_keyboard_graph(states)
    # Provide empty map; should leave weights at default 1.0 (from add_edge)
    set_edge_weights_by_type(graph, {})
    assert graph.weight(0, 1) == 1.0


def test_graph_has_correct_number_of_edges():
    n = 5
    states = [KeyboardState(f"K{i}", float(i), 0.0, "index", "L", False) for i in range(n)]
    graph = build_semantic_keyboard_graph(states)
    # Complete undirected graph has n*(n-1)/2 edges
    expected = n * (n - 1) // 2
    actual = sum(len(neigh) for neigh in graph.adj) // 2
    assert actual == expected


# Optional visual test - only runs if matplotlib is available
def test_visualizer_import_and_call():
    try:
        import matplotlib.pyplot as plt  # noqa: F401
    except ImportError:
        pytest.skip("matplotlib not installed")
    from src.core.keyboard_graph import plot_keyboard_graph
    states = [
        KeyboardState("A", 0.0, 0.0, "index", "L", False),
        KeyboardState("B", 1.0, 0.0, "middle", "L", False),
        KeyboardState("C", 2.0, 0.0, "ring", "L", False),
    ]
    graph = build_semantic_keyboard_graph(states)
    # assign some weights for fun
    w_map = {Et: 1.0 for Et in EdgeType}
    set_edge_weights_by_type(graph, w_map)
    fig, ax = plt.subplots()
    try:
        plot_keyboard_graph(graph, ax=ax)
    finally:
        plt.close(fig)