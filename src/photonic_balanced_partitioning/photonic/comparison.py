"""Exact small-instance bosonic, distinguishable and iid classical controls."""
from __future__ import annotations

from itertools import combinations, permutations
import math
import numpy as np


class CollisionFreeEvaluator:
    """Enumerate CF events only without renormalizing their physical mass.

    All omitted probability belongs to collisions. This exact evaluator is
    exponential and is restricted to small instances; it is not a sampler
    speedup. Input has one photon in each of the first k modes.
    """
    def __init__(self, n, k=None):
        self.n, self.k = n, n//2 if k is None else k
        if not 0 <= self.k <= n:
            raise ValueError("Require 0<=k<=n")
        self.partitions = tuple(combinations(range(n), self.k))
        self.rows = np.asarray(self.partitions, dtype=int)
        self.permutations = np.asarray(list(permutations(range(self.k))), dtype=int)

    def probabilities(self, U, model="bosonic"):
        U = np.asarray(U, dtype=complex)
        if U.shape != (self.n, self.n):
            raise ValueError("Wrong unitary shape")
        if not np.all(np.isfinite(U)) or not np.allclose(U.conj().T @ U, np.eye(self.n), atol=1e-10, rtol=0):
            raise ValueError("A finite unitary is required")
        if self.k == 0:
            return np.ones(1)
        if model == "multinomial":
            # k iid draws from the average occupied-column intensity. This
            # differs from distinguishable photons, whose columns are fixed.
            q = np.abs(U[:, :self.k])**2
            return math.factorial(self.k) * np.prod(q.mean(axis=1)[self.rows], axis=1)
        matrices = U[self.rows, :self.k]
        if model == "distinguishable":
            matrices = np.abs(matrices)**2
        elif model != "bosonic":
            raise ValueError("Unknown model")
        # Explicit permutation sum, independent of the full simulator's Ryser.
        terms = np.prod(matrices[:, np.arange(self.k)[None, :], self.permutations], axis=-1)
        permanent = terms.sum(axis=1)
        return np.abs(permanent)**2 if model == "bosonic" else permanent.real

    def energies(self, edges):
        bits = np.zeros((len(self.partitions), self.n), dtype=int)
        for row, partition in zip(bits, self.partitions):
            row[list(partition)] = 1
        result = np.zeros(len(self.partitions))
        for i, j, weight in edges:
            result += weight * (bits[:, i] != bits[:, j])
        return result


def cf_metrics(probabilities, energies, optimum):
    p = np.asarray(probabilities, dtype=float)
    mass = float(p.sum())
    if not np.all(np.isfinite(p)) or mass < -1e-10 or mass > 1+1e-9 or np.any(p < -1e-12):
        raise ValueError("Unphysical CF probabilities")
    success = float(p[np.isclose(energies, optimum, rtol=0, atol=1e-9)].sum())
    return dict(p_cf=mass, p_success=success,
                p_opt_given_cf=success/mass if mass > 1e-14 else None,
                conditional_energy=float(p @ energies / mass) if mass > 1e-14 else None,
                unconditional_cf_energy=float(p @ energies),
                expected_shots=1/success if success > 0 else None)
