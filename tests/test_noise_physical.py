"""Physical identities and a separate internal-mode creation-operator oracle."""
from collections import defaultdict
from itertools import combinations_with_replacement, permutations
import math

import numpy as np
import pytest

from photonic_balanced_partitioning.noise import (
    apply_independent_loss,
    gram_from_internal_states,
    noisy_distribution,
    partial_distinguishability_distribution as distribution,
    validate_internal_gram,
)


def haar(m, seed):
    rng = np.random.default_rng(seed)
    q, r = np.linalg.qr(rng.normal(size=(m, m)) + 1j*rng.normal(size=(m, m)))
    return q @ np.diag(np.diag(r)/abs(np.diag(r)))


def colored_fock_reference(u, modes, internal):
    """Expand creation operators in spatial x internal modes, tracing internal.

    This has no permutation-Gram weights and independently checks their phase
    orientation and output factorials. Distinct spatial input modes normalize
    the creation-operator product even for overlapping internal states.
    """
    m, d = len(u), internal.shape[1]
    state = {(0,)*(m*d): 1+0j}
    for a, mode in enumerate(modes):
        nxt = defaultdict(complex)
        for occupation, amplitude in state.items():
            for i in range(m):
                for alpha in range(d):
                    j = i*d+alpha
                    target = list(occupation)
                    target[j] += 1
                    nxt[tuple(target)] += (
                        amplitude*u[i, mode]*internal[a, alpha]*math.sqrt(target[j])
                    )
        state = nxt
    answer = defaultdict(float)
    for occupation, amplitude in state.items():
        spatial = tuple(sum(occupation[i*d:(i+1)*d]) for i in range(m))
        answer[spatial] += abs(amplitude)**2
    assert sum(answer.values()) == pytest.approx(1, abs=2e-12)
    return answer


@pytest.mark.parametrize("overlap", [0, .3, .7j, np.exp(.41j)])
def test_hom_pair_overlap_modulus_and_phase(overlap):
    u = np.array([[1, 1j], [1j, 1]])/np.sqrt(2)
    s = np.array([[1, overlap], [np.conj(overlap), 1]])
    law = distribution(u, [0, 1], s)
    assert law[1, 1] == pytest.approx((1-abs(overlap)**2)/2, abs=2e-15)
    assert law[2, 0] == pytest.approx((1+abs(overlap)**2)/4, abs=2e-15)
    assert sum(law.values()) == pytest.approx(1, abs=2e-15)


@pytest.mark.parametrize("k", [0, 1, 2, 3, 4])
def test_bosonic_and_distinguishable_limits_without_existing_simulator(k):
    u = haar(4, 24000+k)
    modes = tuple(range(k))
    b = distribution(u, modes)
    d = distribution(u, modes, np.eye(k))
    for rows in combinations_with_replacement(range(4), k):
        state = tuple(rows.count(i) for i in range(4))
        amplitudes = [math.prod(u[rows[j], modes[p[j]]] for j in range(k))
                      for p in permutations(range(k))]
        norm = math.prod(math.factorial(n) for n in state)
        assert b[state] == pytest.approx(abs(sum(amplitudes))**2/norm, abs=2e-13)
        assert d[state] == pytest.approx(sum(abs(a)**2 for a in amplitudes)/norm, abs=2e-13)
    assert b.raw_total_probability == pytest.approx(1, abs=2e-13)
    assert d.raw_total_probability == pytest.approx(1, abs=2e-13)


def test_complex_three_photon_gram_against_independent_colored_expansion():
    internal = np.array([[1, 0], [1, 1], [1, 1j]], complex)
    internal[1:] /= np.sqrt(2)
    s = gram_from_internal_states(internal)
    u = haar(4, 20261124)
    modes = [3, 0, 2]
    actual = distribution(u, modes, s)
    expected = colored_fock_reference(u, modes, internal)
    for state, p in actual.items():
        assert p == pytest.approx(expected[state], abs=2e-13)
    # The internal triad is complex; replacing S by conjugate(S) is a real bug.
    wrong_phase = distribution(u, modes, s.conj())
    assert max(abs(actual[t]-wrong_phase[t]) for t in actual) > 1e-4
    phases = np.exp(1j*np.array([.2, -.9, 1.7]))
    gauge = phases.conj()[:, None]*s*phases[None, :]
    rephased = distribution(u, modes, gauge)
    assert max(abs(actual[t]-rephased[t]) for t in actual) < 2e-13


def test_three_photon_partial_gram_is_not_a_global_convex_interpolation():
    u = haar(4, 21991)
    s = np.full((3, 3), .5, complex)
    np.fill_diagonal(s, 1)
    p, b, d = (distribution(u, [0, 1, 2], g) for g in (s, np.ones((3, 3)), np.eye(3)))
    direction = np.array([b[t]-d[t] for t in p])
    partial = np.array([p[t]-d[t] for t in p])
    best_scalar = direction@partial/(direction@direction)
    assert np.linalg.norm(partial-best_scalar*direction) > 1e-3


@pytest.mark.parametrize("eta", [0, .2, .9, 1])
def test_all_loss_sectors_vacuum_and_all_photons_detected(eta):
    u = haar(4, 19284)
    gram = np.full((3, 3), .4, complex)
    np.fill_diagonal(gram, 1)
    ideal = distribution(u, [0, 2, 3], gram)
    law = apply_independent_loss(ideal, eta)
    assert sum(law.values()) == pytest.approx(1, abs=3e-13)
    assert law[0, 0, 0, 0] == pytest.approx((1-eta)**3, abs=3e-13)
    for n, mass in law.sector_probabilities().items():
        assert mass == pytest.approx(math.comb(3, n)*eta**n*(1-eta)**(3-n), abs=3e-13)
    for state, probability in ideal.items():
        assert law[state] == pytest.approx(eta**3*probability, abs=3e-13)
    assert sum(p for state, p in law.items() if sum(state) == 3) == pytest.approx(eta**3, abs=3e-13)
    composed = noisy_distribution(u, [0, 2, 3], gram, eta=eta)
    assert dict(composed) == dict(law)


def test_output_mode_dependent_loss_bunching_and_vacuum():
    law = apply_independent_loss({(2, 1): 1.0}, [.25, .8])
    assert law[1, 1] == pytest.approx(2*.25*.75*.8)
    assert law[0, 0] == pytest.approx(.75**2*.2)
    assert law[2, 1] == pytest.approx(.25**2*.8)
    assert sum(law.values()) == pytest.approx(1)
    assert dict(noisy_distribution(np.eye(2), [], np.empty((0, 0)), eta=.3)) == {(0, 0): 1}


def test_uniform_loss_equals_surviving_input_subset_mixture():
    u = haar(3, 124)
    states = np.array([[1, 0], [1, 1], [1, 1j]], complex)
    states[1:] /= np.sqrt(2)
    gram = gram_from_internal_states(states)
    eta = .61
    after = noisy_distribution(u, [2, 0, 1], gram, eta=eta)
    before = defaultdict(float)
    for mask in range(8):
        survivors = [a for a in range(3) if mask & (1 << a)]
        inputs = [[2, 0, 1][a] for a in survivors]
        sub = distribution(u, inputs, gram[np.ix_(survivors, survivors)])
        weight = eta**len(survivors)*(1-eta)**(3-len(survivors))
        for state, p in sub.items():
            before[state] += weight*p
    assert max(abs(after[t]-before[t]) for t in after) < 3e-13


def test_four_photon_all_detected_success_arithmetic():
    assert .537*.9**4 == pytest.approx(.3523257, abs=1e-15)
    assert sum(p for t, p in noisy_distribution(np.eye(4), range(4), eta=.9).items()
               if t == (1, 1, 1, 1)) == pytest.approx(.9**4)


@pytest.mark.parametrize("bad", [
    np.eye(2), np.array([[1, .2], [.1, 1]]), np.array([[1, 2], [2, 1]]),
    np.array([[.9, 0], [0, 1]]), np.array([[1, np.nan], [np.nan, 1]]),
])
def test_reject_bad_gram_shape_hermiticity_psd_diagonal_finiteness(bad):
    k = 3 if np.array_equal(bad, np.eye(2)) else 2
    with pytest.raises(ValueError):
        validate_internal_gram(bad, k)


@pytest.mark.parametrize("u,modes", [
    (np.array([[1, 0], [0, .9]]), [0, 1]), (np.ones((2, 3)), [0]),
    (np.eye(2), [0, 0]), (np.eye(2), [0, 2]), (np.eye(2), [0, .5]),
    (np.eye(6), range(6)),
])
def test_reject_nonunitary_shape_and_unsupported_inputs(u, modes):
    with pytest.raises(ValueError):
        distribution(u, modes)


@pytest.mark.parametrize("eta", [-.1, 1.1, np.nan, [1], [1, np.inf], 1j])
def test_reject_invalid_survival(eta):
    with pytest.raises(ValueError):
        apply_independent_loss({(1, 1): 1.0}, eta)


def test_validation_and_budget_fail_before_unbounded_enumeration():
    with pytest.raises(ValueError, match="max_terms"):
        distribution(np.eye(4), range(4), max_terms=10)
    with pytest.raises(ValueError, match="thinning terms"):
        apply_independent_loss({(2, 2): 1.0}, .5, max_terms=2)
    with pytest.raises(ValueError, match="normalized"):
        apply_independent_loss({(1, 0): .8}, .5)
    with pytest.raises(ValueError):
        apply_independent_loss({(-1, 1): 1.0}, .5)
    with pytest.raises(ValueError):
        gram_from_internal_states([[2, 0]])
    result = distribution(np.eye(2), [0, 1])
    assert result.numerical_semantics == "FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED"
    assert result.roundoff_clipped_mass == 0
    with pytest.raises(TypeError):
        result.probabilities[1, 1] = 0


def test_ideal_small_circuits_against_installed_perceval():
    pcvl = pytest.importorskip("perceval")
    for m, modes, seed in [(2, [0, 1], 120), (3, [2, 0], 121), (4, [3, 0, 2], 122)]:
        u = haar(m, seed)
        actual = distribution(u, modes)
        backend = pcvl.SLOSBackend()
        backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
        backend.set_input_state(pcvl.BasicState([int(i in modes) for i in range(m)]))
        reference = backend.prob_distribution()
        assert sum(reference.values()) == pytest.approx(1, abs=1e-12)
        assert max(abs(p-reference.get(pcvl.BasicState(t), 0)) for t, p in actual.items()) < 2e-12
