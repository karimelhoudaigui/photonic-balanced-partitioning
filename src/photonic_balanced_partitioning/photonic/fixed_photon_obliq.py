"""Exact ideal passive linear optics, including every collisional Fock outcome.

Rows of U label output modes and columns label input modes.  The default input
has one photon in each of the first k modes.  No postselection or normalization
is applied to calculated amplitudes.  The historical class name does not imply
an implementation of the ObliQ binary encoding.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from numbers import Integral
from typing import Any

import numpy as np


@lru_cache(maxsize=None)
def _fock_states(m: int, k: int) -> tuple[tuple[int, ...], ...]:
    """Weak compositions, in the previous lexicographic basis order."""
    if m == 1:
        return ((k,),)
    return tuple((j,) + rest for j in range(k + 1)
                 for rest in _fock_states(m - 1, k - j))


@lru_cache(maxsize=None)
def _ryser_subsets(k: int) -> tuple[np.ndarray, np.ndarray]:
    masks = np.arange(1, 1 << k, dtype=np.int64)
    bits = ((masks[:, None] >> np.arange(k)) & 1).astype(float)
    signs = np.where((k - bits.sum(axis=1).astype(int)) % 2, -1., 1.)
    return bits, signs


@dataclass(frozen=True)
class FixedPhotonResult:
    occupation_numbers: tuple[int, ...]
    is_valid: bool
    is_balanced: bool
    energy: float
    partition: tuple[int, ...] | None
    probability: float


class FixedPhotonObliq:
    """Ideal k-photon simulation; balanced bitstrings require collision-free detection."""

    def __init__(self, n: int, k: int | None = None):
        if not isinstance(n, Integral) or n < 2 or n % 2:
            raise ValueError("n must be a positive even integer (at least 2)")
        k = n // 2 if k is None else k
        if not isinstance(k, Integral) or not 0 <= k <= n:
            raise ValueError("k must be an integer between 0 and n")
        self.n, self.k = int(n), int(k)
        self._full_dimension = math.comb(self.n + self.k - 1, self.k)
        self._cf_dimension = math.comb(self.n, self.k)
        self._default_input = (1,) * self.k + (0,) * (self.n - self.k)
        self._all_states = _fock_states(self.n, self.k)
        self._cf_states = tuple(tuple(int(i in selected) for i in range(self.n))
                                for selected in combinations(range(self.n), self.k))
        self._state_index = {state: j for j, state in enumerate(self._all_states)}
        self._cf_indices = np.array([self._state_index[s] for s in self._cf_states])
        self._rows = {}
        self._norms = {}
        for label, states in (("full", self._all_states), ("cf", self._cf_states)):
            self._rows[label] = np.array([[i for i, count in enumerate(s) for _ in range(count)]
                                         for s in states], dtype=int).reshape(len(states), self.k)
            self._norms[label] = np.sqrt([math.prod(math.factorial(c) for c in s) for s in states])

    @property
    def full_dimension(self) -> int:
        return self._full_dimension

    @property
    def cf_dimension(self) -> int:
        return self._cf_dimension

    def random_interferometer(self, seed: int | None = None) -> np.ndarray:
        """Haar unitary from complex Gaussian QR with diagonal phase correction."""
        rng = np.random.default_rng(seed)
        z = rng.standard_normal((self.n, self.n)) + 1j * rng.standard_normal((self.n, self.n))
        q, r = np.linalg.qr(z)
        d = np.diag(r)
        return q @ np.diag(d / np.abs(d))

    def _validate_unitary(self, U: np.ndarray) -> np.ndarray:
        U = np.asarray(U, dtype=complex)
        if U.shape != (self.n, self.n) or not np.all(np.isfinite(U)):
            raise ValueError("U must be a finite n by n matrix")
        if not np.allclose(U.conj().T @ U, np.eye(self.n), atol=1e-10, rtol=0):
            raise ValueError("U must be unitary; loss requires a separate model")
        return U

    def _validate_occupation(self, occupation) -> tuple[int, ...]:
        occupation = tuple(occupation)
        if (len(occupation) != self.n or any(not isinstance(c, Integral) or c < 0 for c in occupation)
                or sum(occupation) != self.k):
            raise ValueError("occupation must have n nonnegative integer entries summing to k")
        return occupation

    def input_state(self) -> np.ndarray:
        """Default input in the SAME basis as output_state (not basis index zero)."""
        psi = np.zeros(self.full_dimension, dtype=complex)
        psi[self._state_index[self._default_input]] = 1
        return psi

    def _enumerate_all_fock_states(self) -> list[tuple[int, ...]]:
        return list(self._all_states)

    def _enumerate_cf_states(self) -> list[tuple[int, ...]]:
        return list(self._cf_states)

    def _enumerate_partitions(self) -> list[tuple[int, ...]]:
        return [tuple(i for i, c in enumerate(s) if c) for s in self._cf_states]

    def _fock_state_to_index(self, state, all_states=None) -> int:
        return self._state_index[tuple(state)] if all_states is None else all_states.index(tuple(state))

    def _permanent(self, M: np.ndarray) -> complex:
        """Ryser's formula, including correct phases for odd photon numbers."""
        M = np.asarray(M)
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            raise ValueError("permanent requires a square matrix")
        k = M.shape[0]
        if k == 0:
            return 1.0 + 0j
        bits, signs = _ryser_subsets(k)
        return complex(np.prod(M @ bits.T, axis=0) @ signs)

    def _compute_amplitude(self, U, input_state, output_state) -> complex:
        s = self._validate_occupation(input_state)
        t = self._validate_occupation(output_state)
        rows = [i for i, count in enumerate(t) for _ in range(count)]
        cols = [i for i, count in enumerate(s) for _ in range(count)]
        norm = math.sqrt(math.prod(math.factorial(c) for c in s + t))
        return self._permanent(np.asarray(U)[np.ix_(rows, cols)]) / norm

    def _amplitudes(self, U, label="full", input_occupation=None):
        U = self._validate_unitary(U)
        s = self._default_input if input_occupation is None else self._validate_occupation(input_occupation)
        count = self.full_dimension if label == "full" else self.cf_dimension
        if self.k == 0:
            return np.ones(count, dtype=complex)
        cols = np.array([i for i, c in enumerate(s) for _ in range(c)])
        matrices = U[self._rows[label][:, :, None], cols[None, None, :]]
        bits, signs = _ryser_subsets(self.k)
        row_sums = matrices @ bits.T
        permanents = np.prod(row_sums, axis=1) @ signs
        input_norm = math.sqrt(math.prod(math.factorial(c) for c in s))
        return permanents / (input_norm * self._norms[label])

    def output_state(self, U, input_occupation=None) -> np.ndarray:
        """Unrenormalized full Fock amplitudes. Reject a normalization failure."""
        psi = self._amplitudes(U, "full", input_occupation)
        if not np.isclose(np.vdot(psi, psi).real, 1., atol=1e-9, rtol=0):
            raise ArithmeticError("full Fock distribution failed normalization")
        return psi

    def collision_free_probabilities(self, U) -> np.ndarray:
        """Unconditioned CF probabilities in _enumerate_cf_states order."""
        return np.abs(self._amplitudes(U, "cf")) ** 2

    def measure_collision_free_probability(self, U) -> float:
        return float(self.collision_free_probabilities(U).sum())

    def sample(self, U, num_shots: int, edges=None, seed=None) -> list[FixedPhotonResult]:
        if not isinstance(num_shots, Integral) or num_shots < 0:
            raise ValueError("num_shots must be a nonnegative integer")
        rng = np.random.default_rng(seed)
        p = np.abs(self.output_state(U)) ** 2
        # output_state has independently checked raw normalization; this division
        # accommodates roundoff solely for numpy.random.choice's stricter check.
        indices = rng.choice(len(p), size=num_shots, p=p / p.sum())
        results = []
        for j in indices:
            state = self._all_states[j]
            valid = all(c <= 1 for c in state)
            partition = tuple(i for i, c in enumerate(state) if c) if valid else None
            energy = self._compute_cut_weight(partition, edges) if valid and edges is not None else float("nan")
            results.append(FixedPhotonResult(state, valid, valid, energy, partition, float(p[j])))
        return results

    def _cf_energies(self, edges):
        return np.array([self._compute_cut_weight(p, edges) for p in self._enumerate_partitions()])

    def compute_energy(self, U, edges) -> float:
        """Conditional expectation E[C|CF]; undefined/no-support is +infinity."""
        p = self.collision_free_probabilities(U)
        p_cf = float(p.sum())
        return float(p @ self._cf_energies(edges) / p_cf) if p_cf > 1e-14 else float("inf")

    def compute_unconditional_energy(self, U, edges) -> float:
        """Diagnostic subnormalized CF moment, NOT a valid minimization objective."""
        return float(self.collision_free_probabilities(U) @ self._cf_energies(edges))

    def compute_success_probability(self, U, edges, optimal_energy) -> float:
        p = self.collision_free_probabilities(U)
        return float(p[np.isclose(self._cf_energies(edges), optimal_energy, atol=1e-10, rtol=0)].sum())

    def _compute_cut_weight(self, partition, edges) -> float:
        selected = set(partition)
        return float(sum(w for i, j, w in edges if (i in selected) != (j in selected)))

    def optimize(self, edges: list[tuple[int, int, float]], 
                 num_iterations: int = 100, seed: int | None = None) -> dict[str, Any]:
        """Optimize the interferometer to minimize expected cut energy."""
        rng = np.random.default_rng(seed)
        
        best_U = self.random_interferometer(seed=seed)
        best_energy = self.compute_energy(best_U, edges)
        
        energies = [best_energy]
        
        for i in range(num_iterations):
            U = self.random_interferometer(seed=rng.integers(0, 2**31))
            energy = self.compute_energy(U, edges)
            
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
