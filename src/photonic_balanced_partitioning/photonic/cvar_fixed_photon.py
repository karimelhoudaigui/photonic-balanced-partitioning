"""CVaR-based fixed-photon optimization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import numpy as np

from .fixed_photon_obliq import FixedPhotonObliq


@dataclass(frozen=True)
class CVaRResult:
    """Result from CVaR-based optimization."""
    energy: float
    cvar: float
    alpha: float
    partition: tuple[int, ...] | None


class CVaRFixedPhoton:
    """CVaR-based fixed-photon optimization.
    
    This implements the Conditional Value-at-Risk (CVaR) approach:
    CVaR_α[C_G(X) | CF]
    
    CVaR focuses on the tail of the energy distribution, providing
    robustness against poor outcomes.
    """
    
    def __init__(self, n: int, k: int | None = None, alpha: float = 0.1):
        """Initialize CVaR solver.
        
        Args:
            n: Number of vertices/modes
            k: Number of photons (default: n/2)
            alpha: CVaR level (fraction of worst outcomes to consider)
        """
        self.n = n
        self.k = k if k is not None else n // 2
        self.alpha = alpha
        self._base_solver = FixedPhotonObliq(n, k)
    
    def compute_cvar(self, energies: np.ndarray, alpha: float | None = None) -> float:
        """Compute CVaR from a distribution of energies."""
        if alpha is None:
            alpha = self.alpha
        
        sorted_energies = np.sort(energies)
        var_idx = int(np.ceil(alpha * len(sorted_energies))) - 1
        var = sorted_energies[var_idx]
        cvar_energies = sorted_energies[var_idx:]
        cvar = np.mean(cvar_energies)
        
        return cvar
    
    def compute_cvar_energy(self, U: np.ndarray, edges: list[tuple[int, int, float]]) -> float:
        """Compute CVaR of energy for a given interferometer."""
        psi_out = self._base_solver.output_state(U)
        probabilities = np.abs(psi_out) ** 2
        probabilities /= probabilities.sum()
        
        partitions = self._base_solver._enumerate_partitions()
        energies = []
        
        for idx, partition in enumerate(partitions):
            energy = self._base_solver._compute_cut_weight(partition, edges)
            energies.append(energy)
        
        energies = np.array(energies)
        return self.compute_cvar(energies)
    
    def sample(self, U: np.ndarray, num_shots: int, edges: list[tuple[int, int, float]], seed: int | None = None) -> list[CVaRResult]:
        """Sample and compute CVaR statistics."""
        fp_results = self._base_solver.sample(U, num_shots, seed)
        
        energies = []
        for fp_result in fp_results:
            if fp_result.partition is not None:
                energy = self._base_solver._compute_cut_weight(fp_result.partition, edges)
                energies.append(energy)
        
        energies = np.array(energies)
        cvar = self.compute_cvar(energies)
        
        best_idx = np.argmin(energies)
        best_energy = energies[best_idx]
        best_partition = fp_results[best_idx].partition
        
        return CVaRResult(
            energy=best_energy,
            cvar=cvar,
            alpha=self.alpha,
            partition=best_partition
        )
    
    def optimize(self, edges: list[tuple[int, int, float]], num_iterations: int = 100, seed: int | None = None) -> dict[str, Any]:
        """Optimize using CVaR objective."""
        rng = np.random.default_rng(seed)
        
        best_U = self._base_solver.random_interferometer(seed=seed)
        best_cvar = self.compute_cvar_energy(best_U, edges)
        
        cvars = [best_cvar]
        energies = []
        
        for i in range(num_iterations):
            U = self._base_solver.random_interferometer(seed=rng.integers(0, 2**31))
            cvar = self.compute_cvar_energy(U, edges)
            energy = self._base_solver.compute_energy(U, edges)
            
            if cvar < best_cvar:
                best_cvar = cvar
                best_U = U
            
            cvars.append(cvar)
            energies.append(energy)
        
        return {
            "best_cvar": best_cvar,
            "best_energy": self._base_solver.compute_energy(best_U, edges),
            "best_interferometer": best_U,
            "cvars": cvars,
            "energies": energies,
            "iterations": num_iterations,
        }