"""
Keyboard graph where edges represent primitive ergonomic actions.
"""
from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Dict, Optional
import numpy as np

class EdgeType(Enum):
    """Semantic types of primitive ergonomic transitions."""
    SAME_FINGER = "same_finger"
    FINGER_CHANGE = "finger_change"
    HAND_SHIFT = "hand_shift"
    MODIFIER_TOGGLE = "modifier_toggle"

    def __str__(self) -> str:
        return self.value


class KeyboardGraph:
    """
    Undirected weighted graph whose nodes are KeyboardState instances.
    Edge weights are determined later by a cost model based on EdgeType.
    """
    def __init__(self, nodes: List):
        self.nodes = nodes
        self.n = len(nodes)
        # adjacency list: for each node i, list of (neighbor_index, edge_type)
        self.adj: List[List[tuple[int, EdgeType]]] = [[] for _ in range(self.n)]
        # edge weights indexed by (i, j) where i < j
        self._weights: Dict[tuple[int, int], float] = {}

    def add_edge(self, i: int, j: int, edge_type: EdgeType) -> None:
        """Add undirected edge between node i and j with given semantic type."""
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            raise IndexError("Node index out of range")
        if i == j:
            return
        # Store each undirected edge once.
        key = (i, j) if i < j else (j, i)
        if key not in self._weights:
            self.adj[i].append((j, edge_type))
            self.adj[j].append((i, edge_type))
            # initial weight placeholder; will be set later
            self._weights[key] = 1.0

    def set_edge_weight(self, i: int, j: int, weight: float) -> None:
        """Overwrite the weight of an existing edge."""
        if i == j:
            return
        key = (i, j) if i < j else (j, i)
        if key not in self._weights:
            raise ValueError(f"No edge between {i} and {j}")
        self._weights[key] = float(weight)

    def edge_type(self, i: int, j: int) -> Optional[EdgeType]:
        """Return the EdgeType of edge (i,j) if it exists."""
        if i == j:
            return None
        key = (i, j) if i < j else (j, i)
        if key not in self._weights:
            return None
        # retrieve type by scanning adjacency (small graphs)
        for nbr, typ in self.adj[i]:
            if nbr == j:
                return typ
        return None

    def weight(self, i: int, j: int) -> float:
        """Current weight of edge (i,j). Assumes edge exists."""
        if i == j:
            return 0.0
        key = (i, j) if i < j else (j, i)
        return self._weights.get(key, 1.0)

    def distance_matrix(self) -> np.ndarray:
        """
        All-pairs shortest path using Floyd‑Warshall on the current edge weights.
        Returns a distance matrix (np.ndarray) of shape (n, n).
        """
        INF = 1e9
        dist = np.full((self.n, self.n), INF, dtype=float)
        np.fill_diagonal(dist, 0.0)
        for i in range(self.n):
            for j, _ in self.adj[i]:
                w = self.weight(i, j)
                if w < dist[i, j]:
                    dist[i, j] = w
        # Floyd‑Warshall
        for k in range(self.n):
            dk = dist[k]
            for i in range(self.n):
                dik = dist[i, k]
                if dik == INF:
                    continue
                di = dist[i]
                # vectorized update for row i
                new = dik + dk
                mask = new < di
                if np.any(mask):
                    di[mask] = new[mask]
        # Replace any remaining INF (disconnected) with a large number
        dist[dist == INF] = 1e6
        return dist

    def adjacency_list(self) -> List[List[tuple[int, EdgeType, float]]]:
        """Return list of (neighbor, edge_type, weight) for each node."""
        result: List[List[tuple[int, EdgeType, float]]] = []
        for i in range(self.n):
            neighs = []
            for j, typ in self.adj[i]:
                w = self.weight(i, j)
                neighs.append((j, typ, w))
            result.append(neighs)
        return result


def _edge_type_for(s1, s2) -> EdgeType:
    """
    Determine the semantic edge type between two KeyboardState instances.
    Priority: modifier change > hand change > finger change > same finger.
    Assumes s1 and s2 have attributes: finger (str), hand (str), modifier (bool).
    """
    # Modifier changes dominate because one state requires a held layer key.
    if getattr(s1, "modifier", None) != getattr(s2, "modifier", None):
        return EdgeType.MODIFIER_TOGGLE
    # Hand shift: different hand
    if getattr(s1, "hand", None) != getattr(s2, "hand", None):
        return EdgeType.HAND_SHIFT
    # Finger change: same hand, different finger
    if getattr(s1, "hand", None) == getattr(s2, "hand", None) and \
       getattr(s1, "finger", None) != getattr(s2, "finger", None):
        return EdgeType.FINGER_CHANGE
    # Same finger (and same hand, same modifier by elimination)
    return EdgeType.SAME_FINGER


def build_semantic_keyboard_graph(states: List) -> KeyboardGraph:
    """
    Build a complete graph where each edge is labelled with its primitive
    ergonomic action type (see EdgeType).
    """
    graph = KeyboardGraph(states)
    n = len(states)
    for i in range(n):
        si = states[i]
        for j in range(i + 1, n):
            sj = states[j]
            etype = _edge_type_for(si, sj)
            graph.add_edge(i, j, etype)
    return graph


def set_edge_weights_by_type(graph: KeyboardGraph,
                             weight_map: dict[EdgeType, float]) -> None:
    """
    Assign numeric weights to edges based on their EdgeType using the
    provided mapping. Missing types default to 1.0.
    """
    n = graph.n
    for i in range(n):
        for j, etype in graph.adj[i]:
            if i < j:  # set once per undirected edge
                w = weight_map.get(etype, 1.0)
                graph.set_edge_weight(i, j, w)


def build_movement_cost_matrix(states: List) -> np.ndarray:
    """
    Build movement cost matrix (C) as shortest‑path distances on the
    semantic keyboard graph, using placeholder unit weights.
    """
    graph = build_semantic_keyboard_graph(states)
    # placeholder weights = 1.0 for all edges (handled by default in add_edge)
    return graph.distance_matrix()


def plot_keyboard_graph(graph: KeyboardGraph, ax=None):
    """
    Visualize the keyboard graph using networkx and matplotlib.
    Nodes are colored by finger, edges styled by EdgeType.
    Returns the matplotlib Axes object.
    """
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except ImportError as e:
        raise ImportError("matplotlib and networkx are required for plotting") from e
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    G = nx.Graph()
    for i, node in enumerate(graph.nodes):
        G.add_node(i,
                   label=getattr(node, "label", str(i)),
                   finger=getattr(node, "finger", ""),
                   hand=getattr(node, "hand", ""),
                   modifier=getattr(node, "modifier", False))
    for i in range(graph.n):
        for j, typ in graph.adj[i]:
            if i < j:
                G.add_edge(i, j, type=typ)
    # Position nodes by their x, y coordinates
    pos = {i: (node.x, node.y) for i, node in enumerate(graph.nodes)}
    # Node colors by finger
    finger_colors = {
        "thumb": "#e41a1c",
        "index": "#377eb8",
        "middle": "#4daf4a",
        "ring": "#984ea3",
        "pinky": "#ff7f00",
        # fallback
    }
    node_colors = [finger_colors.get(getattr(node, "finger", ""), "#999999")
                   for node in graph.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax, node_size=300)
    # Edge styles by type
    style_map = {
        EdgeType.SAME_FINGER: "solid",
        EdgeType.FINGER_CHANGE: "dashed",
        EdgeType.HAND_SHIFT: "dotted",
        EdgeType.MODIFIER_TOGGLE: "dashdot",
    }
    for etype, style in style_map.items():
        edges = [(i, j) for i in range(graph.n) for j, t in graph.adj[i]
                 if i < j and t == etype]
        nx.draw_networkx_edges(G, pos, edgelist=edges, style=style,
                               ax=ax, width=2, edge_color="#555555")
    # Labels (show the node label)
    labels = {i: f"{getattr(node, 'label', i)}" for i, node in enumerate(graph.nodes)}
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=8, font_color="black")
    ax.set_title("Keyboard Graph – semantic edges")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect('equal', adjustable='datalim')
    return ax
