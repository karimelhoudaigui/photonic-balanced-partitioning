import itertools
import numpy as np
import pytest
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh, partition_permutation
from photonic_balanced_partitioning.photonic.comparison import CollisionFreeEvaluator
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq


@pytest.mark.parametrize("n", [4, 6, 8, 10])
def test_mesh_unitarity(n):
    mesh = RectangularMesh(n)
    p = np.random.default_rng(n).normal(size=mesh.num_parameters)
    np.testing.assert_allclose(mesh.unitary(p).conj().T @ mesh.unitary(p), np.eye(n), atol=1e-12)
    assert len(mesh.pairs) == n*(n-1)//2


@pytest.mark.parametrize("n", [4, 6, 8])
def test_independent_permutation_sum_matches_full_ryser(n):
    solver = FixedPhotonObliq(n)
    ev = CollisionFreeEvaluator(n)
    for seed in [2, 5]:
        U = solver.random_interferometer(seed)
        full = dict(zip(solver._enumerate_all_fock_states(), abs(solver.output_state(U))**2))
        expected = [full[tuple(int(i in part) for i in range(n))] for part in ev.partitions]
        np.testing.assert_allclose(ev.probabilities(U), expected, atol=2e-12)


def test_distinguishable_against_labelled_enumeration():
    ev = CollisionFreeEvaluator(6)
    U = FixedPhotonObliq(6).random_interferometer(17)
    by_partition = {p: 0.0 for p in ev.partitions}
    for outputs in itertools.product(range(6), repeat=3):
        if len(set(outputs)) == 3:
            by_partition[tuple(sorted(outputs))] += float(np.prod([abs(U[i, a])**2 for a, i in enumerate(outputs)]))
    np.testing.assert_allclose(ev.probabilities(U, "distinguishable"), list(by_partition.values()), atol=1e-14)


def test_oracle_permutation_and_no_interference():
    ev = CollisionFreeEvaluator(6)
    U = partition_permutation(6, (1, 3, 5))
    for model in ["bosonic", "distinguishable"]:
        p = ev.probabilities(U, model)
        assert p.sum() == 1
        assert p[ev.partitions.index((1, 3, 5))] == 1


def test_perceval_mesh_circuit():
    pytest.importorskip("perceval")
    mesh = RectangularMesh(6)
    params = np.random.default_rng(18).normal(size=mesh.num_parameters)
    np.testing.assert_allclose(np.array(mesh.to_perceval(params).compute_unitary(), dtype=complex), mesh.unitary(params), atol=1e-12)
