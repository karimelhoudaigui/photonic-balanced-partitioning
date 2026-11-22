"""Small interacting-block proposals around a classically prepared bisection.

This is a falsifiable local-search mechanism, not a claimed quantum speedup.
Only r<=3 photons in 2r modes interact. Spectators remain deterministic. A
classical exact block replacement is therefore always available at fixed cost
independent of the global graph size; every proposal retains collision mass.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations
import math

import numpy as np
from scipy.linalg import expm

from .fixed_photon_obliq import FixedPhotonObliq


def cut_energy(adjacency, partition):
    a = np.asarray(adjacency, dtype=float)
    x = np.zeros(len(a))
    x[list(partition)] = 1
    return float(x @ a.sum(axis=1) - x @ a @ x)


def swap_deltas(adjacency, partition):
    """All occupied/vacant swap costs; each entry counts as a scored proposal."""
    a = np.asarray(adjacency, dtype=float)
    occupied = np.asarray(sorted(partition), dtype=int)
    vacant = np.asarray([i for i in range(len(a)) if i not in set(partition)], dtype=int)
    x = np.zeros(len(a)); x[occupied] = 1
    flip = (1 - 2*x) * (a.sum(axis=1) - 2 * a @ x)
    deltas = flip[occupied, None] + flip[vacant][None, :] + 2*a[np.ix_(occupied, vacant)]
    return occupied, vacant, deltas


def classical_anchor(adjacency, seed, max_steps=2):
    """Random feasible start followed by a bounded best-swap classical descent.

    No optimum is supplied or computed. None means descend to a strict single
    swap local minimum. Every scored single swap and full-cut evaluation is
    returned; a final scan is deliberately included for informed block choice.
    """
    a = np.asarray(adjacency, dtype=float)
    n = len(a)
    if a.shape != (n, n) or n % 2 or not np.allclose(a, a.T) or not np.allclose(np.diag(a), 0):
        raise ValueError('Expected an even simple weighted undirected adjacency')
    if max_steps is not None and max_steps < 0:
        raise ValueError('max_steps must be nonnegative or None')
    rng = np.random.default_rng(seed)
    partition = set(rng.choice(n, n//2, replace=False).tolist())
    initial_energy = cut_energy(a, partition)
    energy = initial_energy
    scored = steps = 0
    while True:
        occupied, vacant, delta = swap_deltas(a, partition)
        scored += delta.size
        minimum = float(delta.min())
        if minimum >= -1e-10 or (max_steps is not None and steps >= max_steps):
            break
        choices = np.argwhere(np.isclose(delta, minimum, atol=1e-12, rtol=0))
        i, j = choices[rng.integers(len(choices))]
        partition.remove(int(occupied[i])); partition.add(int(vacant[j]))
        energy += minimum
        steps += 1
        if steps > 10000:
            raise RuntimeError('Descent exceeded guard; preserve as failed run')
    return dict(partition=tuple(sorted(partition)), initial_energy=initial_energy,
                energy=energy, steps=steps, swap_deltas_scored=scored,
                full_cut_evaluations=1, local_minimum=minimum >= -1e-10,
                final_occupied=occupied, final_vacant=vacant, final_deltas=delta)


def informed_block(anchor, r, seed):
    """Select r disjoint low-cost single swaps, without scoring multi-swaps."""
    occupied, vacant, deltas = anchor['final_occupied'], anchor['final_vacant'], anchor['final_deltas']
    if not 1 <= r <= min(3, len(occupied), len(vacant)):
        raise ValueError('Require 1<=r<=3 and r vertices on each side')
    rng = np.random.default_rng(seed)
    tie = rng.random(deltas.shape)
    order = sorted(np.ndindex(deltas.shape), key=lambda ij: (deltas[ij], tie[ij]))
    selected_o, selected_v = [], []
    for i, j in order:
        if int(occupied[i]) not in selected_o and int(vacant[j]) not in selected_v:
            selected_o.append(int(occupied[i])); selected_v.append(int(vacant[j]))
            if len(selected_o) == r:
                return tuple(selected_o), tuple(selected_v)
    raise RuntimeError('Failed to construct disjoint matching')


def pair_unitary(r, angle):
    """Disjoint occupied/vacant rotations: exact CF=1 classical product sampler."""
    if not 1 <= r <= 3 or not np.isfinite(angle):
        raise ValueError('Unsupported r or angle')
    c, s = np.cos(angle), np.sin(angle)
    u = np.eye(2*r, dtype=complex)
    for i in range(r):
        u[i, i], u[i, i+r], u[i+r, i], u[i+r, i+r] = c, -s, s, c
    return u


def interacting_unitary(r, pair_angle, interaction_angle):
    """Closed 4/6-mode phase-coherent mixing after the product proposal.

    At r=2 the Hermitian generator is a normalized Walsh matrix. At r=3
    it is the Hermitian part of the six-mode Fourier matrix. Zero interaction
    recovers the product control exactly. Angles are frozen after training.
    """
    if r not in (2, 3) or not np.isfinite(interaction_angle):
        raise ValueError('Require r=2 or 3 and finite angle')
    if r == 2:
        h = np.array([[1, 1, 1, 1], [1, 1, -1, -1],
                      [1, -1, 1, -1], [1, -1, -1, 1]], dtype=complex)/2
    else:
        indices = np.arange(2*r)
        f = np.exp(2j*np.pi*indices[:, None]*indices[None, :]/(2*r))/np.sqrt(2*r)
        h = (f + f.conj().T)/2
    return expm(1j*interaction_angle*h) @ pair_unitary(r, pair_angle)


def classical_full_probabilities(unitary, r, indistinguishable=True):
    """Exact constant-size classical routing enumerator, independent of Ryser.

    It includes all collisional outputs. Complexity grows exponentially with r;
    bounded r<=3 makes it a constant-size replacement, not a large-scale boson
    sampling algorithm. Input has one photon in each of the first r modes.
    """
    u = np.asarray(unitary, dtype=complex)
    if not 1 <= r <= 3 or u.shape != (2*r, 2*r):
        raise ValueError('Expected 2r-mode block with 1<=r<=3')
    if not np.allclose(u.conj().T@u, np.eye(2*r), atol=1e-10, rtol=0):
        raise ValueError('Expected unitary block')
    states = FixedPhotonObliq(2*r, r)._enumerate_all_fock_states()
    routings = tuple(permutations(range(r)))
    probability = []
    for t in states:
        rows = [i for i, count in enumerate(t) for _ in range(count)]
        terms = [math.prod(u[rows[j], pi[j]] for j in range(r)) for pi in routings]
        numerator = abs(sum(terms))**2 if indistinguishable else sum(abs(term)**2 for term in terms)
        probability.append(numerator/math.prod(math.factorial(c) for c in t))
    return states, np.asarray(probability, dtype=float)


@dataclass(frozen=True)
class LocalBlockProposal:
    anchor: tuple[int, ...]
    occupied: tuple[int, ...]
    vacant: tuple[int, ...]

    def __post_init__(self):
        if (not 1 <= len(self.occupied) <= 3 or len(self.occupied) != len(self.vacant)
                or len(set(self.anchor)) != len(self.anchor)
                or len(set(self.occupied+self.vacant)) != 2*len(self.occupied)
                or not set(self.occupied) <= set(self.anchor)
                or set(self.vacant) & set(self.anchor)):
            raise ValueError('Require disjoint occupied/vacant block and valid anchor')

    @property
    def r(self):
        return len(self.occupied)

    @property
    def modes(self):
        return self.occupied+self.vacant

    @property
    def candidates(self):
        spectators = set(self.anchor)-set(self.occupied)
        return tuple(tuple(sorted(spectators | {self.modes[j] for j in selected}))
                     for selected in combinations(range(2*self.r), self.r))

    def distribution(self, unitary=None, model='bosonic'):
        """Return feasible partitions followed by None (all collisions) and mass."""
        candidates = self.candidates
        if model == 'uniform_feasible':
            return candidates+(None,), np.r_[np.full(len(candidates), 1/len(candidates)), 0.]
        if model == 'correlated_batch':
            p = np.zeros(len(candidates)+1)
            p[0] = p[-2] = .5  # combinations first=anchor, last=all r replacements
            return candidates+(None,), p
        if model not in ['bosonic', 'distinguishable', 'classical_exact_bosonic']:
            raise ValueError('Unknown model')
        if model == 'bosonic':
            solver = FixedPhotonObliq(2*self.r, self.r)
            states, full = solver._enumerate_all_fock_states(), abs(solver.output_state(unitary))**2
        else:
            states, full = classical_full_probabilities(unitary, self.r,
                                                      indistinguishable=model=='classical_exact_bosonic')
        if abs(full.sum()-1) > 1e-10:
            raise ArithmeticError('Unnormalized complete local distribution')
        by_state = dict(zip(states, full))
        feasible = [by_state[tuple(int(j in selected) for j in range(2*self.r))]
                    for selected in combinations(range(2*self.r), self.r)]
        collision = sum(float(p) for t, p in zip(states, full) if max(t)>1)
        return candidates+(None,), np.r_[feasible, collision]

    def statistics(self, adjacency, probabilities):
        """Evaluation-only labels; never fed back to a test-time circuit."""
        p = np.asarray(probabilities, dtype=float)
        if p.shape != (len(self.candidates)+1,) or np.any(p < -1e-12) or abs(p.sum()-1)>1e-10:
            raise ValueError('Invalid complete proposal probabilities')
        energy = np.array([cut_energy(adjacency, candidate) for candidate in self.candidates])
        current = cut_energy(adjacency, self.anchor)
        gains = np.maximum(current-energy, 0)
        improve = energy < current-1e-10
        return dict(p_cf=float(p[:-1].sum()), p_improve=float(p[:-1][improve].sum()),
                    expected_accepted_gain=float(p[:-1]@gains),
                    expected_cost_after_one_attempt=float(current-p[:-1]@gains),
                    improvement_possible=bool(improve.any()),
                    local_best_gain=float(gains.max()), local_cost_labels=len(energy),
                    energies=energy, improving_mask=improve, gains=gains)
