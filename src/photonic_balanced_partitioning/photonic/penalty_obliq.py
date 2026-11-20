"""Penalty-based ObliQ implementation for comparison."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import numpy as np

from .fixed_photon_obliq import FixedPhotonObliq


@dataclass(frozen=True)
class PenaltyObliqResult:
    """Result from penalty-based ObliQ."""
    occupation_numbers: tuple[int, ...]
    is_valid: bool
    is_balanced: bool
    energy: float
    partition: tuple[int, ...] | None
    penalty: float
    total: float


class PenaltyObliq:
    """Penalty-based ObliQ implementation.
    
    This implements the standard ObliQ approach where:
    - n modes represent n vertices
    - k photons are injected (k = n/2 for bisection)
    - A penalty term λ(Σx_i - k)² is added to the cost
    - The interferometer can explore non-balanced states
    """
    
    def __init__(self, n: int, k: int | None = None, lam: float = 10.0):
        """Initialize penalty-based ObliQ.
        
        Args:
            n: Number of vertices/modes
            k: Target number of photons (default: n/2)
            lam: Penalty coefficient λ
        """
        self.n = n
        self.k = k if k is not None else n // 2
        self.lam = lam
        self._base_solver = FixedPhotonObliq(n, k)
    
    def compute_penalty(self, partition: tuple[int, ...]) -> float:
        """Compute the penalty term for a partition."""
        sum_x = len(partition)
        return self.lam * (sum_x - self.k) ** 2
    
    def compute_total_energy(self, partition: tuple[int, ...], edges: list[tuple[int, int, float]]) -> float:
        """Compute total energy including penalty."""
        cut_weight = self._base_solver._compute_cut_weight(partition, edges)
        penalty = self.compute_penalty(partition)
        return cut_weight + penalty
    
    def sample(self, U: np.ndarray, num_shots: int, edges: list[tuple[int, int, float]], seed: int | None = None) -> list[PenaltyObliqResult]:
        """Sample from the penalty-based distribution."""
        fp_results = self._base_solver.sample(U, num_shots, seed)
        
        results = []
        for fp_result in fp_results:
            partition = fp_result.partition
            if partition is None:
                continue
            
            cut_weight = self._base_solver._compute_cut_weight(partition, edges)
            penalty = self.compute_penalty(partition)
            total = cut_weight + penalty
            
            result = PenaltyObliqResult(
                occupation_numbers=fp_result.occupation_numbers,
                is_valid=fp_result.is_valid,
                is_balanced=fp_result.is_balanced,
                energy=cut_weight,
                partition=partition,
                penalty=penalty,
                total=total
            )
            results.append(result)
        
        return results
    
    def optimize(self, edges: list[tuple[int, int, float]], num_iterations: int = 100, seed: int | None = None) -> dict[str, Any]:
        """Optimize using penalty-based objective."""
        rng = np.random.default_rng(seed)
        
        best_U = self._base_solver.random_interferometer(seed=seed)
        best_energy = self._base_solver.compute_energy(best_U, edges)
        
        energies = [best_energy]
        
        for i in range(num_iterations):
            U = self._base_solver.random_interferometer(seed=rng.integers(0, 2**31))
            energy = self._base_solver.compute_energy(U, edges)
            
            if energy < best_energy:
                best_energy = energy
                best_U = U
            
            energies.append(energy)
        
        return {
            "best_energy": best_energy,
            "best_interferometer": best_U,
            "energies": energies,
            "iterations": num_iterations,
        }