"""Minimum Bisection / Balanced Graph Partitioning problem formulation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
import itertools
import numpy as np
from scipy import sparse


class GraphFamily(str, Enum):
    PATH = "path"
    CYCLE = "cycle"
    COMPLETE = "complete"
    BIPARTITE = "bipartite"
    STAR = "star"
    RANDOM_REGULAR = "random_regular"
    ERDOS_RÉNYI = "erdos_renyi"
    WEIGHTED_RANDOM = "weighted_random"
    PLANTED_PARTITION = "planted_partition"


@dataclass(frozen=True)
class GraphInstance:
    """A weighted graph instance for balanced partitioning."""
    n: int
    edges: tuple[tuple[int, int, float], ...]
    family: GraphFamily | None = None
    metadata: dict[str, Any] | None = None
    
    @property
    def adjacency_matrix(self) -> np.ndarray:
        A = np.zeros((self.n, self.n), dtype=np.float64)
        for i, j, w in self.edges:
            A[i, j] = w
            A[j, i] = w
        return A
    
    @property
    def laplacian_matrix(self) -> np.ndarray:
        D = np.diag(self.adjacency_matrix.sum(axis=1))
        return D - self.adjacency_matrix
    
    @property
    def num_edges(self) -> int:
        return len(self.edges)
    
    @property
    def is_connected(self) -> bool:
        if not self.edges:
            return self.n <= 1
        
        adj = {i: set() for i in range(self.n)}
        for i, j, _ in self.edges:
            adj[i].add(j)
            adj[j].add(i)
        
        visited = set()
        stack = [0]
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            stack.extend(adj[v])
        
        return len(visited) == self.n


@dataclass(frozen=True)
class PartitionResult:
    """Result of a partition computation."""
    energy: float
    partition: tuple[int, ...]
    is_balanced: bool
    is_optimal: bool = False
    
    @property
    def v0(self) -> tuple[int, ...]:
        return self.partition
    
    @property
    def v1(self) -> tuple[int, ...]:
        return tuple(i for i in range(self.n) if i not in self.partition)


@dataclass(frozen=True)
class BalancedGraphPartitioning:
    """Balanced Graph Partitioning / Minimum Bisection problem."""
    
    n: int
    edges: tuple[tuple[int, int, float], ...]
    k: int | None = None
    
    def __post_init__(self):
        if self.n % 2 != 0:
            raise ValueError(f"Number of vertices must be even, got {self.n}")
        if self.k is None:
            object.__setattr__(self, "k", self.n // 2)
        if self.k != self.n // 2:
            raise ValueError(f"k must equal n/2 for bisection, got k={self.k}, n={self.n}")
    
    @property
    def adjacency_matrix(self) -> np.ndarray:
        """Return the weighted adjacency matrix."""
        A = np.zeros((self.n, self.n), dtype=np.float64)
        for i, j, w in self.edges:
            A[i, j] = w
            A[j, i] = w
        return A
    
    @property
    def laplacian_matrix(self) -> np.ndarray:
        """Return the weighted Laplacian matrix."""
        D = np.diag(self.adjacency_matrix.sum(axis=1))
        return D - self.adjacency_matrix
    
    @property
    def num_edges(self) -> int:
        return len(self.edges)
    
    @property
    def is_connected(self) -> bool:
        """Check if the graph is connected."""
        if not self.edges:
            return self.n <= 1
        
        adj = {i: set() for i in range(self.n)}
        for i, j, _ in self.edges:
            adj[i].add(j)
            adj[j].add(i)
        
        visited = set()
        stack = [0]
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            stack.extend(adj[v])
        
        return len(visited) == self.n
    
    @classmethod
    def from_adjacency(cls, A: np.ndarray, k: int | None = None) -> "BalancedGraphPartitioning":
        n = A.shape[0]
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] != 0:
                    edges.append((i, j, float(A[i, j])))
        return cls(n, tuple(edges), k)
    
    @classmethod
    def path_graph(cls, n: int, weight: float = 1.0) -> "BalancedGraphPartitioning":
        if n % 2 != 0:
            raise ValueError(f"Path graph requires even n, got {n}")
        edges = [(i, i + 1, weight) for i in range(n - 1)]
        return cls(n, tuple(edges))
    
    @classmethod
    def cycle_graph(cls, n: int, weight: float = 1.0) -> "BalancedGraphPartitioning":
        if n % 2 != 0:
            raise ValueError(f"Cycle graph requires even n, got {n}")
        edges = [(i, (i + 1) % n, weight) for i in range(n)]
        return cls(n, tuple(edges))
    
    @classmethod
    def complete_graph(cls, n: int, weight: float = 1.0) -> "BalancedGraphPartitioning":
        if n % 2 != 0:
            raise ValueError(f"Complete graph requires even n, got {n}")
        edges = [(i, j, weight) for i in range(n) for j in range(i + 1, n)]
        return cls(n, tuple(edges))
    
    @classmethod
    def complete_bipartite(cls, n1: int, n2: int, weight: float = 1.0) -> "BalancedGraphPartitioning":
        n = n1 + n2
        if n % 2 != 0:
            raise ValueError(f"Total vertices must be even, got {n}")
        edges = [(i, n1 + j, weight) for i in range(n1) for j in range(n2)]
        return cls(n, tuple(edges))
    
    @classmethod
    def star_graph(cls, n: int, weight: float = 1.0) -> "BalancedGraphPartitioning":
        if n % 2 != 0:
            raise ValueError(f"Star graph requires even n, got {n}")
        edges = [(0, i, weight) for i in range(1, n)]
        return cls(n, tuple(edges))
    
    @classmethod
    def random_regular(cls, n: int, degree: int, seed: int = 0, weight_range: tuple[float, float] = (1.0, 1.0)) -> "BalancedGraphPartitioning":
        if n % 2 != 0:
            raise ValueError(f"Random regular graph requires even n, got {n}")
        if degree >= n:
            raise ValueError(f"Degree must be < n, got degree={degree}, n={n}")
        
        rng = np.random.default_rng(seed)
        edges = []
        
        stubs = list(range(n)) * degree
        rng.shuffle(stubs)
        
        while len(stubs) >= 2:
            i, j = stubs[0], stubs[1]
            if i != j:
                w = rng.uniform(*weight_range)
                edges.append((min(i, j), max(i, j), w))
            stubs = stubs[2:]
        
        unique_edges = []
        seen = set()
        for i, j, w in edges:
            if i != j and (i, j) not in seen:
                seen.add((i, j))
                unique_edges.append((i, j, w))
        
        return cls(n, tuple(unique_edges))
    
    @classmethod
    def erdos_renyi(cls, n: int, p: float, seed: int = 0, weight_range: tuple[float, float] = (1.0, 1.0)) -> "BalancedGraphPartitioning":
        if n % 2 != 0:
            raise ValueError(f"Erdős-Rényi graph requires even n, got {n}")
        
        rng = np.random.default_rng(seed)
        edges = []
        
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p:
                    w = rng.uniform(*weight_range)
                    edges.append((i, j, w))
        
        return cls(n, tuple(edges))
    
    @classmethod
    def planted_partition(cls, n: int, community_size: int, intra_weight: float = 1.0, inter_weight: float = 0.1, seed: int = 0) -> "BalancedGraphPartitioning":
        if n % 2 != 0:
            raise ValueError(f"Planted partition requires even n, got {n}")
        
        rng = np.random.default_rng(seed)
        edges = []
        
        c1 = list(range(n // 2))
        c2 = list(range(n // 2, n))
        
        for i in range(n // 2):
            for j in range(i + 1, n // 2):
                if rng.random() < 0.5:
                    edges.append((i, j, intra_weight))
        
        for i in range(n // 2, n):
            for j in range(i + 1, n):
                if rng.random() < 0.5:
                    edges.append((i, j, intra_weight))
        
        for i in range(n // 2):
            for j in range(n // 2, n):
                if rng.random() < 0.3:
                    edges.append((i, j, inter_weight))
        
        return cls(n, tuple(edges))
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "n": self.n,
            "edges": [list(e) for e in self.edges],
            "k": self.k,
        }
    
    def copy(self) -> "BalancedGraphPartitioning":
        return BalancedGraphPartitioning(self.n, self.edges, self.k)
    
    def with_added_edge(self, i: int, j: int, weight: float) -> "BalancedGraphPartitioning":
        new_edges = self.edges + ((i, j, weight),)
        return BalancedGraphPartitioning(self.n, new_edges, self.k)
    
    def with_added_weight(self, i: int, j: int, delta: float) -> "BalancedGraphPartitioning":
        new_edges = []
        for a, b, w in self.edges:
            if (a, b) == (i, j) or (a, b) == (j, i):
                new_edges.append((a, b, w + delta))
            else:
                new_edges.append((a, b, w))
        return BalancedGraphPartitioning(self.n, tuple(new_edges), self.k)
    
    def solve_exact(self) -> PartitionResult:
        """Solve the problem exactly by enumeration."""
        return solve_exact_min_bisection(self.n, self.edges, self.k)


def compute_cut_weight(n: int, edges: tuple[tuple[int, int, float], ...], partition: tuple[int, ...]) -> float:
    v0 = set(partition)
    v1 = set(range(n)) - v0
    
    cut_weight = 0.0
    for i, j, w in edges:
        if (i in v0 and j in v1) or (i in v1 and j in v0):
            cut_weight += w
    
    return cut_weight


def enumerate_balanced_partitions(n: int, k: int) -> list[tuple[int, ...]]:
    return [tuple(combo) for combo in itertools.combinations(range(n), k)]


def solve_exact_min_bisection(n: int, edges: tuple[tuple[int, int, float], ...], k: int | None = None) -> PartitionResult:
    if k is None:
        k = n // 2
    
    if n > 12:
        raise ValueError(f"Exact enumeration only feasible for n <= 12, got n={n}")
    
    best_energy = float("inf")
    best_partition = None
    
    for partition in enumerate_balanced_partitions(n, k):
        energy = compute_cut_weight(n, edges, partition)
        if energy < best_energy:
            best_energy = energy
            best_partition = partition
    
    return PartitionResult(
        energy=best_energy,
        partition=best_partition,
        is_balanced=True,
        is_optimal=True
    )


def solve_qubo_with_penalty(n: int, edges: tuple[tuple[int, int, float], ...], k: int | None = None, lam: float = 10.0) -> PartitionResult:
    if k is None:
        k = n // 2
    
    best_energy = float("inf")
    best_partition = None
    
    for partition in enumerate_balanced_partitions(n, k):
        cut_weight = compute_cut_weight(n, edges, partition)
        penalty = lam * (len(partition) - k) ** 2
        total = cut_weight + penalty
        
        if total < best_energy:
            best_energy = total
            best_partition = partition
    
    return PartitionResult(
        energy=compute_cut_weight(n, edges, best_partition),
        partition=best_partition,
        is_balanced=True,
        is_optimal=True
    )


def get_worst_balanced_cut(n: int, edges: tuple[tuple[int, int, float], ...], k: int | None = None) -> float:
    if k is None:
        k = n // 2
    
    worst_energy = 0.0
    for partition in enumerate_balanced_partitions(n, k):
        energy = compute_cut_weight(n, edges, partition)
        worst_energy = max(worst_energy, energy)
    
    return worst_energy


def get_normalized_gap(n: int, edges: tuple[tuple[int, int, float], ...], energy: float, k: int | None = None) -> float:
    if k is None:
        k = n // 2
    
    optimal = solve_exact_min_bisection(n, edges, k).energy
    worst = get_worst_balanced_cut(n, edges, k)
    
    if worst == optimal:
        return 0.0
    
    return (energy - optimal) / (worst - optimal)