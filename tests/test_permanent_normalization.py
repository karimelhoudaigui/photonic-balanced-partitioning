"""Independent permanent and Fock-normalization checks; no renormalization allowed."""
from itertools import permutations
import math

import numpy as np
import pytest

from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq


@pytest.mark.parametrize('k', range(6))
def test_ryser_against_explicit_permutations(k):
    rng = np.random.default_rng(1040 + k)
    a = rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k))
    exact = sum(math.prod(a[i, j] for i, j in enumerate(p)) for p in permutations(range(k)))
    assert np.isclose(FixedPhotonObliq(6, k)._permanent(a), exact, atol=1e-10, rtol=0)


@pytest.mark.parametrize('n,k', [(2, 0), (2, 1), (4, 2), (4, 3), (6, 3), (8, 4), (10, 5)])
def test_full_distribution_raw_normalization_and_cf_subset(n, k):
    solver = FixedPhotonObliq(n, k)
    u = solver.random_interferometer(seed=111 + k)
    p = np.abs(solver.output_state(u)) ** 2
    assert abs(p.sum() - 1) < 1e-10
    subset = [p[solver._fock_state_to_index(s)] for s in solver._enumerate_cf_states()]
    np.testing.assert_allclose(subset, solver.collision_free_probabilities(u), atol=1e-12, rtol=0)


def test_three_photon_phase_is_not_global_sign_flipped():
    solver = FixedPhotonObliq(4, 3)
    phases = np.array([.17, -.3, .61, .8])
    actual = solver.output_state(np.diag(np.exp(1j * phases)))
    expected = solver.input_state() * np.exp(1j * phases[:3].sum())
    np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)


def test_collisional_input_multinomial():
    solver = FixedPhotonObliq(4, 3)
    u = solver.random_interferometer(seed=19)
    p = abs(solver.output_state(u, input_occupation=(3, 0, 0, 0))) ** 2
    for state, prob in zip(solver._enumerate_all_fock_states(), p):
        expected = math.factorial(3) / math.prod(math.factorial(c) for c in state)
        expected *= math.prod(abs(u[j, 0]) ** (2 * state[j]) for j in range(4))
        assert abs(prob - expected) < 1e-12


def test_identity_matches_documented_input_basis():
    for n, k in [(4, 2), (6, 3)]:
        solver = FixedPhotonObliq(n, k)
        np.testing.assert_allclose(solver.output_state(np.eye(n)), solver.input_state(), atol=1e-12)


@pytest.mark.parametrize('bad_u', [np.zeros((4, 4)), np.eye(3), np.full((4, 4), np.nan)])
def test_invalid_unitary_is_not_silently_renormalized(bad_u):
    with pytest.raises(ValueError):
        FixedPhotonObliq(4).output_state(bad_u)


@pytest.mark.parametrize('n,k', [(0, 0), (3, 1), (4, -1), (4, 5), (4, 1.5)])
def test_invalid_dimensions(n, k):
    with pytest.raises(ValueError):
        FixedPhotonObliq(n, k)
