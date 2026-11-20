"""Fixed-k photon interferometer implementation based on ObliQ.

CORRECTED VERSION: Properly handles full Fock space vs collision-free subspace.

Key correction: Fixed photon number (∑n_i = k) does NOT imply collision-free
occupations (n_i ∈ {0,1}). We must simulate the full Fock space and measure
collision probability separately.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations, product
from typing import Any
import numpy as np
from scipy.special import comb


@dataclass(frozen=True)
class FixedPhotonResult:
    """Result from a single photon sampling."""
    occupation_numbers: tuple[int, ...]  # n_i for each mode
    is_valid: bool  # True if collision-free (all n_i <= 1)
    is_balanced: bool  # True if sum(n_i) = k (always True for fixed-k)
    energy: float  # Cut weight of decoded partition (only valid if is_valid)
    partition: tuple[int, ...] | None  # Vertices in V0 (only valid if is_valid)
    probability: float  # Probability of this outcome


class FixedPhotonObliq:
    """Fixed-k photon interferometer for balanced graph partitioning.
    
    This implements the constraint-preserving approach where:
    - n photons are injected into n modes
    - A passive linear interferometer U is applied
    - We measure collision-free probability separately
    - Only collision-free outcomes correspond to balanced partitions
    
    CRITICAL: Fixed photon number does NOT guarantee collision-free outcomes.
    """
    
    def __init__(self, n: int, k: int | None = None):
        """Initialize the fixed-photon interferometer.
        
        Args:
            n: Number of vertices/modes (must be even)
            k: Number of photons (default: n/2 for bisection)
        """
        if n % 2 != 0:
            raise ValueError(f"n must be even, got {n}")
        self.n = n
        self.k = k if k is not None else n // 2
        
        # Full Fock space dimension: C(n+k-1, k)
        self._full_dimension = int(comb(self.n + self.k - 1, self.k, exact=True))
        
        # Collision-free dimension: C(n, k)
        self._cf_dimension = int(comb(self.n, self.k, exact=True))
    
    @property
    def full_dimension(self) -> int:
        """Dimension of the full k-photon Fock space."""
        return self._full_dimension
    
    @property
    def cf_dimension(self) -> int:
        """Dimension of the collision-free subspace."""
        return self._cf_dimension
    
    def random_interferometer(self, seed: int | None = None) -> np.ndarray:
        """Generate a random unitary interferometer."""
        rng = np.random.default_rng(seed)
        Z = rng.standard_normal((self.n, self.n)) + 1j * rng.standard_normal((self.n, self.n))
        Q, R = np.linalg.qr(Z)
        Lambda = np.diag(np.diag(R) / np.abs(np.diag(R)))
        return Q @ Lambda
    
    def input_state(self) -> np.ndarray:
        """Return the input state vector in the full Fock space.
        
        Input is |1, 1, 0, ..., 0⟩ (first k modes have one photon each).
        """
        psi = np.zeros(self.full_dimension, dtype=complex)
        psi[0] = 1.0
        return psi
    
    def _enumerate_all_fock_states(self) -> list[tuple[int, ...]]:
        """Enumerate all Fock states with k photons in n modes.
        
        This includes collision states like |2,0,0,0⟩.
        """
        states = []
        for combo in product(range(self.k + 1), repeat=self.n):
            if sum(combo) == self.k:
                states.append(combo)
        return states
    
    def _enumerate_cf_states(self) -> list[tuple[int, ...]]:
        """Enumerate only collision-free Fock states (n_i ∈ {0,1})."""
        # Each state is a tuple of occupation numbers (n_0, n_1, ..., n_{n-1})
        # where exactly k of them are 1 and the rest are 0
        states = []
        for combo in combinations(range(self.n), self.k):
            state = [0] * self.n
            for i in combo:
                state[i] = 1
            states.append(tuple(state))
        return states
    
    def _fock_state_to_index(self, state: tuple[int, ...], all_states: list[tuple[int, ...]]) -> int:
        """Convert a Fock state to its index in the enumeration."""
        return all_states.index(state)
    
    def _compute_amplitude(self, U: np.ndarray, input_state: tuple[int, ...], 
                           output_state: tuple[int, ...]) -> complex:
        """Compute the bosonic transition amplitude.
        
        For input occupation s and output occupation t:
        A(s→t) = Per(U_{t,s}) / sqrt(∏s_i! ∏t_j!)
        
        where U_{t,s} is the submatrix with rows indexed by t and columns by s.
        """
        # Build the submatrix
        # For each mode i with s_i photons in, we need s_i columns from U
        # For each mode j with t_j photons out, we need t_j rows from U
        
        # Get row indices (with multiplicity)
        rows = []
        for j, tj in enumerate(output_state):
            rows.extend([j] * tj)
        
        # Get column indices (with multiplicity)
        cols = []
        for i, si in enumerate(input_state):
            cols.extend([i] * si)
        
        if not rows or not cols:
            return 0.0
        
        U_sub = U[np.ix_(rows, cols)]
        
        # Permanent
        perm = self._permanent(U_sub)
        
        # Normalization
        norm = 1.0
        for si in input_state:
            norm *= math.sqrt(math.factorial(si))
        for tj in output_state:
            norm *= math.sqrt(math.factorial(tj))
        
        return perm / norm
    
    def _permanent(self, M: np.ndarray) -> complex:
        """Compute the permanent using Ryser's formula."""
        n = M.shape[0]
        if n == 0:
            return 1.0
        if n == 1:
            return M[0, 0]
        
        total = 0.0
        for k in range(1, 2**n):
            subset = [i for i in range(n) if (k >> i) & 1]
            prod = 1.0
            for i in range(n):
                row_sum = sum(M[i, j] for j in subset)
                prod *= row_sum
            sign = (-1) ** (n - len(subset))
            total += sign * prod
        
        return total * ((-1) ** n)
    
    def output_state(self, U: np.ndarray) -> np.ndarray:
        """Compute the output state in the full Fock space."""
        all_states = self._enumerate_all_fock_states()
        psi_out = np.zeros(self.full_dimension, dtype=complex)
        
        # Input state: first k modes have 1 photon each
        input_state = tuple([1] * self.k + [0] * (self.n - self.k))
        
        for j, output_state in enumerate(all_states):
            amplitude = self._compute_amplitude(U, input_state, output_state)
            psi_out[j] = amplitude
        
        # Normalize
        norm = np.sqrt(np.sum(np.abs(psi_out) ** 2))
        if norm > 0:
            psi_out = psi_out / norm
        
        return psi_out
    
    def measure_collision_free_probability(self, U: np.ndarray) -> float:
        """Measure the probability of collision-free detection."""
        psi_out = self.output_state(U)
        all_states = self._enumerate_all_fock_states()
        cf_states = self._enumerate_cf_states()
        
        p_cf = 0.0
        for j, state in enumerate(all_states):
            if state in cf_states:
                p_cf += np.abs(psi_out[j]) ** 2
        
        return float(p_cf)
    
    def sample(self, U: np.ndarray, num_shots: int, 
               edges: list[tuple[int, int, float]] | None = None,
               seed: int | None = None) -> list[FixedPhotonResult]:
        """Sample from the output distribution in the full Fock space."""
        rng = np.random.default_rng(seed)
        
        psi_out = self.output_state(U)
        probabilities = np.abs(psi_out) ** 2
        probabilities /= probabilities.sum()
        
        all_states = self._enumerate_all_fock_states()
        cf_states = set(self._enumerate_cf_states())
        
        results = []
        for _ in range(num_shots):
            idx = rng.choice(self.full_dimension, p=probabilities)
            state = all_states[idx]
            prob = probabilities[idx]
            
            is_valid = state in cf_states
            is_balanced = sum(state) == self.k  # Always True for fixed-k
            
            # Compute energy only for valid (collision-free) states
            energy = 0.0
            partition = None
            if is_valid:
                partition = tuple(i for i, ni in enumerate(state) if ni == 1)
                if edges is not None:
                    v0 = set(partition)
                    v1 = set(range(self.n)) - v0
                    energy = sum(w for i, j, w in edges 
                                if (i in v0 and j in v1) or (i in v1 and j in v0))
            
            result = FixedPhotonResult(
                occupation_numbers=state,
                is_valid=is_valid,
                is_balanced=is_balanced,
                energy=energy,
                partition=partition,
                probability=prob
            )
            results.append(result)
        
        return results
    
    def compute_energy(self, U: np.ndarray, edges: list[tuple[int, int, float]]) -> float:
        """Compute expected cut energy."""
        psi_out = self.output_state(U)
        probabilities = np.abs(psi_out) ** 2
        probabilities /= probabilities.sum()
        
        all_states = self._enumerate_all_fock_states()
        cf_states = set(self._enumerate_cf_states())
        
        expected_energy = 0.0
        for j, state in enumerate(all_states):
            if state in cf_states:
                partition = tuple(i for i, ni in enumerate(state) if ni == 1)
                v0 = set(partition)
                v1 = set(range(self.n)) - v0
                energy = sum(w for i, j, w in edges 
                            if (i in v0 and j in v1) or (i in v1 and j in v0))
                expected_energy += probabilities[j] * energy
        
        return expected_energy
    
    def _compute_cut_weight(self, partition: tuple[int, ...], 
                            edges: list[tuple[int, int, float]]) -> float:
        """Compute cut weight for a partition."""
        v0 = set(partition)
        v1 = set(range(self.n)) - v0
        
        cut_weight = 0.0
        for i, j, w in edges:
            if (i in v0 and j in v1) or (i in v1 and j in v0):
                cut_weight += w
        
        return cut_weight
    
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
