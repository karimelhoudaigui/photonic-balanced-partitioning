"""Collision-aware photonic optimization with explicit physical rejection cost."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import numpy as np
from .fixed_photon_obliq import FixedPhotonObliq
from .objectives import cut_energies
from ..optimization.objectives import training_loss


@dataclass(frozen=True)
class CollisionAwareResult:
    occupation_numbers: tuple[int, ...]
    is_valid: bool
    is_balanced: bool
    has_collision: bool
    energy: float
    partition: tuple[int, ...] | None
    probability: float
    collision_penalty: float


class CollisionAwareSolver:
    def __init__(self, n: int, k: int | None = None, mu: float = 1.0):
        if not np.isfinite(mu) or mu < 0:
            raise ValueError("mu must be finite and nonnegative")
        self._base_solver = FixedPhotonObliq(n, k)
        self.n, self.k, self.mu = n, self._base_solver.k, mu

    def sample(self, U: np.ndarray, num_shots: int, seed: int | None = None,
               edges=None) -> list[CollisionAwareResult]:
        fp_results = self._base_solver.sample(U, num_shots, edges=edges, seed=seed)
        return [CollisionAwareResult(
            occupation_numbers=r.occupation_numbers, is_valid=r.is_valid,
            is_balanced=r.is_valid and r.is_balanced,
            has_collision=any(count > 1 for count in r.occupation_numbers),
            energy=r.energy, partition=r.partition, probability=r.probability,
            collision_penalty=self.mu if not r.is_valid else 0.0,
        ) for r in fp_results]

    def compute_collision_probability(self, U: np.ndarray) -> float:
        return float(np.clip(1.0 - self._base_solver.measure_collision_free_probability(U), 0.0, 1.0))

    def expected_objective(self, U: np.ndarray, edges) -> float:
        p = np.abs(self._base_solver.output_state(U))**2
        states = np.asarray(self._base_solver._enumerate_all_fock_states())
        feasible = np.all((states == 0) | (states == 1), axis=1)
        return training_loss(p, cut_energies(states, edges), feasible, mu=self.mu)

    def optimize(self, edges, num_iterations=100, seed=None) -> dict[str, Any]:
        """Haar random-search baseline, *not* a variational algorithm.

        Reports exactly num_iterations + 1 distribution evaluations and zero
        physical shots. Exact distributions are not shot-based training data.
        """
        if num_iterations < 0:
            raise ValueError("num_iterations must be nonnegative")
        rng = np.random.default_rng(seed)
        objectives, energies = [], []
        best_objective, best_U = float("inf"), None
        states = np.asarray(self._base_solver._enumerate_all_fock_states())
        feasible = np.all((states == 0) | (states == 1), axis=1)
        costs = cut_energies(states, edges)
        for _ in range(num_iterations + 1):
            U = self._base_solver.random_interferometer(seed=int(rng.integers(2**31)))
            p = np.abs(self._base_solver.output_state(U))**2
            obj = training_loss(p, costs, feasible, mu=self.mu)
            objectives.append(obj)
            energies.append(training_loss(p, costs, feasible, "conditional_energy"))
            if best_U is None or obj < best_objective:
                best_objective, best_U = obj, U
        return {"best_objective": best_objective,
                "best_energy": energies[int(np.argmin(objectives))],
                "best_interferometer": best_U, "objectives": objectives,
                "energies": energies, "iterations": num_iterations,
                "n_evaluations": num_iterations+1, "n_shots": 0,
                "training_mode": "exact_distribution", "uses_optimum_oracle": False,
                "reference_state_count": len(states)}
