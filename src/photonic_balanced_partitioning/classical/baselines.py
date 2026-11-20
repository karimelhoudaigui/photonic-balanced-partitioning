"""Classical baseline solvers for balanced graph partitioning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import itertools
import numpy as np


@dataclass(frozen=True)
class ClassicalResult:
    """Result from a classical solver."""
    energy: float
    partition: tuple[int, ...]
    is_balanced: bool
    solver_name: str


def enumerate_all_balanced(n: int, k: int) -> list[tuple[int, ...]]:
    """Enumerate all balanced partitions."""
    return [tuple(c) for c in itertools.combinations(range(n), k)]


def exact_enumeration(n: int, edges: list[tuple[int, int, float]], k: int | None = None) -> ClassicalResult:
    """Solve by exact enumeration."""
    if k is None:
        k = n // 2
    
    best_energy = float("inf")
    best_partition = None
    
    for partition in enumerate_all_balanced(n, k):
        v0 = set(partition)
        v1 = set(range(n)) - v0
        
        energy = 0.0
        for i, j, w in edges:
            if (i in v0 and j in v1) or (i in v1 and j in v0):
                energy += w
        
        if energy < best_energy:
            best_energy = energy
            best_partition = partition
    
    return ClassicalResult(
        energy=best_energy,
        partition=best_partition,
        is_balanced=True,
        solver_name="exact_enumeration"
    )


def greedy_balanced(n: int, edges: list[tuple[int, int, float]], k: int | None = None) -> ClassicalResult:
    """Greedy balanced partitioning."""
    if k is None:
        k = n // 2
    
    v0 = set(range(k))
    v1 = set(range(k, n))
    
    adj = {i: {} for i in range(n)}
    for i, j, w in edges:
        adj[i][j] = w
        adj[j][i] = w
    
    improved = True
    while improved:
        improved = False
        
        for i in v0:
            for j in v1:
                gain = 0.0
                for neighbor, w in adj[i].items():
                    if neighbor in v0 and neighbor != i:
                        gain -= w
                    elif neighbor in v1:
                        gain += w
                
                for neighbor, w in adj[j].items():
                    if neighbor in v1 and neighbor != j:
                        gain -= w
                    elif neighbor in v0:
                        gain += w
                
                if gain < 0:
                    v0.remove(i)
                    v0.add(j)
                    v1.remove(j)
                    v1.add(i)
                    improved = True
                    break
            
            if improved:
                break
    
    partition = tuple(sorted(v0))
    energy = sum(w for i, j, w in edges if (i in v0 and j in v1) or (i in v1 and j in v0))
    
    return ClassicalResult(
        energy=energy,
        partition=partition,
        is_balanced=True,
        solver_name="greedy_balanced"
    )


def spectral_partitioning(n: int, edges: list[tuple[int, int, float]], k: int | None = None) -> ClassicalResult:
    """Spectral partitioning using Fiedler vector."""
    if k is None:
        k = n // 2
    
    L = np.zeros((n, n))
    for i, j, w in edges:
        L[i, i] += w
        L[j, j] += w
        L[i, j] -= w
        L[j, i] -= w
    
    eigenvalues, eigenvectors = np.linalg.eigh(L)
    fiedler = eigenvectors[:, 1]
    
    v0 = set(i for i in range(n) if fiedler[i] <= 0)
    v1 = set(range(n)) - v0
    
    if len(v0) > k:
        sorted_v0 = sorted(v0, key=lambda i: abs(fiedler[i]), reverse=True)
        for i in sorted_v0[:len(v0) - k]:
            v0.remove(i)
            v1.add(i)
    elif len(v0) < k:
        sorted_v1 = sorted(v1, key=lambda i: abs(fiedler[i]))
        for i in sorted_v1[:k - len(v0)]:
            v0.add(i)
            v1.remove(i)
    
    partition = tuple(sorted(v0))
    energy = sum(w for i, j, w in edges if (i in v0 and j in v1) or (i in v1 and j in v0))
    
    return ClassicalResult(
        energy=energy,
        partition=partition,
        is_balanced=True,
        solver_name="spectral"
    )


def simulated_annealing(n: int, edges: list[tuple[int, int, float]], k: int | None = None,
                        num_iterations: int = 10000, seed: int | None = None) -> ClassicalResult:
    """Simulated annealing for balanced partitioning."""
    if k is None:
        k = n // 2
    
    rng = np.random.default_rng(seed)
    
    vertices = list(range(n))
    rng.shuffle(vertices)
    v0 = set(vertices[:k])
    v1 = set(vertices[k:])
    
    def compute_energy(v0: set, v1: set) -> float:
        return sum(w for i, j, w in edges if (i in v0 and j in v1) or (i in v1 and j in v0))
    
    current_energy = compute_energy(v0, v1)
    best_energy = current_energy
    best_partition = tuple(sorted(v0))
    
    T = 1.0
    T_min = 0.001
    alpha = 0.9995
    
    for _ in range(num_iterations):
        i = rng.choice(list(v0))
        j = rng.choice(list(v1))
        
        v0_new = v0 - {i} | {j}
        v1_new = v1 - {j} | {i}
        
        new_energy = compute_energy(v0_new, v1_new)
        
        delta = new_energy - current_energy
        if delta < 0 or rng.random() < np.exp(-delta / T):
            v0 = v0_new
            v1 = v1_new
            current_energy = new_energy
            
            if current_energy < best_energy:
                best_energy = current_energy
                best_partition = tuple(sorted(v0))
        
        T *= alpha
        if T < T_min:
            break
    
    return ClassicalResult(
        energy=best_energy,
        partition=best_partition,
        is_balanced=True,
        solver_name="simulated_annealing"
    )


def random_balanced_sampling(n: int, edges: list[tuple[int, int, float]], k: int | None = None,
                             num_samples: int = 1000, seed: int | None = None) -> ClassicalResult:
    """Random balanced sampling baseline."""
    if k is None:
        k = n // 2
    
    rng = np.random.default_rng(seed)
    
    best_energy = float("inf")
    best_partition = None
    
    for _ in range(num_samples):
        vertices = list(range(n))
        rng.shuffle(vertices)
        partition = tuple(sorted(vertices[:k]))
        
        v0 = set(partition)
        v1 = set(range(n)) - v0
        energy = sum(w for i, j, w in edges if (i in v0 and j in v1) or (i in v1 and j in v0))
        
        if energy < best_energy:
            best_energy = energy
            best_partition = partition
    
    return ClassicalResult(
        energy=best_energy,
        partition=best_partition,
        is_balanced=True,
        solver_name="random_balanced"
    )


def get_all_baselines() -> dict[str, Any]:
    """Return dictionary of all baseline solvers."""
    return {
        "exact_enumeration": exact_enumeration,
        "greedy_balanced": greedy_balanced,
        "spectral": spectral_partitioning,
        "simulated_annealing": simulated_annealing,
        "random_balanced": random_balanced_sampling,
    }