"""Lower-tail CVaR of cut cost, conditioned on collision-free outcomes."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import numpy as np
from .fixed_photon_obliq import FixedPhotonObliq
from .objectives import conditional_cvar, weighted_lower_cvar, distribution_metrics


@dataclass(frozen=True)
class CVaRResult:
    energy: float
    cvar: float
    alpha: float
    partition: tuple[int, ...] | None


class CVaRFixedPhoton:
    """Minimize the *lowest* alpha probability mass; no robustness claim."""
    def __init__(self, n: int, k: int | None = None, alpha: float = 0.1):
        if not np.isfinite(alpha) or not 0 < alpha <= 1:
            raise ValueError("alpha must lie in (0, 1]")
        self._base_solver = FixedPhotonObliq(n, k)
        self.n, self.k, self.alpha = n, self._base_solver.k, alpha

    def compute_cvar(self, energies: np.ndarray, alpha: float | None = None,
                     probabilities=None) -> float:
        return weighted_lower_cvar(energies, probabilities, self.alpha if alpha is None else alpha)

    def compute_cvar_energy(self, U: np.ndarray, edges) -> float:
        return conditional_cvar(np.abs(self._base_solver.output_state(U))**2,
                                self._base_solver._enumerate_all_fock_states(), edges, self.alpha)

    def sample(self, U: np.ndarray, num_shots: int, edges, seed=None) -> CVaRResult:
        samples = self._base_solver.sample(U, num_shots, edges=edges, seed=seed)
        valid = [r for r in samples if r.is_valid and r.partition is not None]
        if not valid:
            return CVaRResult(float("inf"), float("inf"), self.alpha, None)
        energies = np.array([self._base_solver._compute_cut_weight(r.partition, edges) for r in valid])
        best = int(np.argmin(energies))
        return CVaRResult(float(energies[best]), self.compute_cvar(energies),
                          self.alpha, valid[best].partition)

    def optimize(self, edges, num_iterations=100, seed=None) -> dict[str, Any]:
        """Haar random-search baseline using exact-distribution CVaR."""
        if num_iterations < 0:
            raise ValueError("num_iterations must be nonnegative")
        rng = np.random.default_rng(seed)
        cvars, energies = [], []
        best_cvar, best_U = float("inf"), None
        for _ in range(num_iterations+1):
            U = self._base_solver.random_interferometer(seed=int(rng.integers(2**31)))
            p = np.abs(self._base_solver.output_state(U))**2
            states = self._base_solver._enumerate_all_fock_states()
            cvar = conditional_cvar(p, states, edges, self.alpha)
            cvars.append(cvar)
            energies.append(distribution_metrics(p, states, edges).conditional_energy)
            if best_U is None or cvar < best_cvar:
                best_cvar, best_U = cvar, U
        return {"best_cvar": best_cvar,
                "best_energy": energies[int(np.argmin(cvars))],
                "best_interferometer": best_U, "cvars": cvars,
                "energies": energies, "iterations": num_iterations,
                "n_evaluations": num_iterations+1, "n_shots": 0,
                "training_mode": "exact_distribution"}
