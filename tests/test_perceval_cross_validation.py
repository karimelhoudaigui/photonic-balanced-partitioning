"""Compare raw full Fock probabilities and complex amplitudes against Perceval.

The gate is NOT met by skipped tests. Install the pinned [qpu] validation extra
and run the dedicated report runner to produce a PASS artifact.
"""
import numpy as np
import pytest

from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq

pcvl = pytest.importorskip('perceval', reason='Perceval absent: validation gate remains CLOSED')


@pytest.mark.parametrize('n,k', [(2, 1), (2, 2), (4, 2), (4, 3), (6, 3), (8, 4)])
@pytest.mark.parametrize('seed', range(6))
def test_full_fock_distribution_and_amplitudes_against_slos(n, k, seed):
    solver = FixedPhotonObliq(n, k)
    u = solver.random_interferometer(seed=23000 + 100 * n + seed)
    backend = pcvl.SLOSBackend()
    backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
    for s in [tuple([1] * k + [0] * (n - k)), tuple([k] + [0] * (n - 1))]:
        backend.set_input_state(pcvl.BasicState(s))
        reference = backend.prob_distribution()
        actual = solver.output_state(u, input_occupation=s)
        assert abs(sum(reference.values()) - 1) < 1e-10
        for t, amp in zip(solver._enumerate_all_fock_states(), actual):
            state = pcvl.BasicState(t)
            assert abs(abs(amp) ** 2 - reference.get(state, 0)) < 1e-10
            assert abs(amp - backend.prob_amplitude(state)) < 1e-10


def test_perceval_hom_and_vacuum():
    for k in [0, 2]:
        solver = FixedPhotonObliq(2, k)
        u = np.array([[1, -1], [1, 1]], complex) / np.sqrt(2)
        backend = pcvl.SLOSBackend()
        backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
        backend.set_input_state(pcvl.BasicState([1, 1] if k else [0, 0]))
        actual = solver.output_state(u)
        for t, amp in zip(solver._enumerate_all_fock_states(), actual):
            assert abs(amp - backend.prob_amplitude(pcvl.BasicState(t))) < 1e-10
