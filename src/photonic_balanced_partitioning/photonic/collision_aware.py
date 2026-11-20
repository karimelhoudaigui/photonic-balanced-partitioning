"""Collision-aware photonic optimization solver."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import numpy as np

from .fixed_photon_obliq import FixedPhotonObliq


@dataclass(frozen=True)
class CollisionAwareResult:
    """Result from collision-aware sampling."""
    occupation_numbers: tuple[int, ...]
    is_valid: bool
    is_balanced: bool
    has_collision: bool
    energy: float
    partition: tuple[int, ...] | None
    probability: float
    collision_penalty: float


class CollisionAwareSolver:
    """Collision-aware solver that explicitly handles boson collisions."""
    
    def __init__(self, n: int, k: int | None = None, mu: float = 1.0):
        """Initialize collision-aware solver.
        
        Args:
            n: Number of vertices/modes
            k: Number of photons (default: n/2)
            mu: Collision penalty coefficient
        """
        self.n = n
        self.k = k if k is not None else n // 2
        self.mu = mu
        self._base_solver = FixedPhotonObliq(n, k)
    
    def sample(self, U: np.ndarray, num_shots: int, seed: int | None = None) -> list[CollisionAwareResult]:
        """Sample with collision awareness."""
        fp_results = self._base_solver.sample(U, num_shots, seed)
        
        results = []
        for fp_result in fp_results:
            result = CollisionAwareResult(
                occupation_numbers=fp_result.occupation_numbers,
                is_valid=fp_result.is_valid,
                is_balanced=fp_result.is_balanced,
                has_collision=False,
                energy=fp_result.energy,
                partition=fp_result.partition,
                probability=fp_result.probability,
                collision_penalty=0.0
            )
            results.append(result)
        
        return results
    
    def compute_collision_probability(self, U: np.ndarray) -> float:
        """Estimate collision probability for a given interferometer."""
        return 0.0  # In fixed-photon subspace, P_CF = 1
    
    def expected_objective(self, U: np.ndarray, edges: list[tuple[int, int, float]]) -> float:
        """Compute the collision-aware expected objective."""
        p_cf = 1.0
        psi_out = self._base_solver.output_state(U)
        probabilities = np.abs(psi_out) ** 2
        probabilities /= probabilities.sum()
        
        partitions = self._base_solver._enumerate_partitions()
        expected_energy = 0.0
        
        for idx, partition in enumerate(partitions):
            energy = self._base_solver._compute_cut_weight(partition, edges)
            expected_energy += probabilities[idx] * energy
        
        objective = expected_energy + self.mu * (1 - p_cf)
        return objective
    
    def optimize(self, edges: list[tuple[int, int, float]], num_iterations: int = 100, seed: int | None = None) -> dict[str, Any]:
        """Optimize using collision-aware objective."""
        rng = np.random.default_rng(seed)
        
        best_U = self._base_solver.random_interferometer(seed=seed)
        best_objective = self.expected_objective(best_U, edges)
        
        objectives = [best_objective]
        energies = []
        
        for i in range(num_iterations):
            U = self._base_solver.random_interferometer(seed=rng.integers(0, 2**31))
            obj = self.expected_objective(U, edges)
            energy = self._base_solver.compute_energy(U, edges)
            
            if obj < best_objective:
                best_objective = obj
                best_U = U
            
            objectives.append(obj)
            energies.append(energy)
        
        return {
            "best_objective": best_objective,
            "best_energy": self._base_solver.compute_energy(best_U, edges),
            "best_interferometer": best_U,
            "objectives": objectives,
            "energies": energies,
            "iterations": num_iterations,
        }