"""Full-cube penalty baseline: exhaustive small-instance checks."""
import numpy as np
import pytest
from photonic_balanced_partitioning.photonic.penalty_obliq import PenaltyObliq,PenaltyProductBernoulli

EDGES=[(0,1,1.),(1,2,1.),(2,3,1.)]


@pytest.mark.parametrize("lam",[0.,.2,1.,3.,10.])
def test_qubo_matches_direct_energy_on_entire_cube(lam):
    solver=PenaltyProductBernoulli(4,lam=lam)
    q=solver.qubo_coefficients(EDGES)
    expected=solver.energies(EDGES)
    computed=q["offset"] + solver.bitstrings @ q["linear"] + np.einsum("bi,ij,bj->b",solver.bitstrings,q["quadratic"],solver.bitstrings)
    np.testing.assert_allclose(expected,computed,atol=1e-12)
    for x,e in zip(solver.bitstrings,expected):
        part=tuple(np.flatnonzero(x))
        assert solver.compute_total_energy(part,EDGES) == pytest.approx(e)


def test_full_cube_has_feasible_and_infeasible_support():
    solver=PenaltyProductBernoulli(4)
    assert solver.bitstrings.shape == (16,4)
    p=solver.probabilities(np.zeros(4))
    assert np.all(p > 0)
    assert solver.metrics(np.zeros(4),EDGES)["p_feasible"] == pytest.approx(6/16)
    assert np.sum(~solver.feasible) == 10
    for params in [np.full(4,1000.),np.full(4,-1000.)]:
        assert np.all(solver.probabilities(params)>0)
    with pytest.raises(ValueError):
        solver.probabilities(np.eye(4))


def test_samples_keep_all_infeasible_shots_and_seed():
    solver=PenaltyProductBernoulli(4,lam=2)
    a=solver.sample(np.zeros(4),100,EDGES,seed=7)
    b=solver.sample(np.zeros(4),100,EDGES,seed=7)
    assert a == b
    assert len(a) == 100
    assert any(not r.is_valid for r in a)
    assert all(r.is_balanced == (sum(r.occupation_numbers)==2) for r in a)
    assert all(r.total == r.energy+r.penalty for r in a)


def test_real_penalty_changes_ground_state_feasibility():
    low=PenaltyProductBernoulli(4,lam=.1)
    high=PenaltyProductBernoulli(4,lam=4)
    e_low,e_high=low.energies(EDGES),high.energies(EDGES)
    assert not np.any(low.feasible[np.isclose(e_low,e_low.min())])
    assert np.all(high.feasible[np.isclose(e_high,e_high.min())])
    assert high.gibbs_probabilities(EDGES)[high.feasible].sum() > low.gibbs_probabilities(EDGES)[low.feasible].sum()


def test_coupling_cancellation_is_measured():
    solver=PenaltyProductBernoulli(4,lam=1.)
    q=solver.qubo_coefficients(EDGES)
    assert q["coupling_count"] == 3
    assert q["coupling_density"] == .5
    assert q["obliq_circuit_depth"] is None


def test_optimization_budget_and_sampling_cost():
    solver=PenaltyProductBernoulli(4)
    r=solver.optimize(EDGES,num_iterations=25,seed=6,method="random",shots_per_evaluation=100)
    assert r["n_evaluations"] == 25
    assert r["n_shots"] == 2500
    assert len(r["parameter_trace"]) == 25
    assert r["model"] == "classical_product_bernoulli"


def test_old_name_warns_instead_of_claiming_obliq():
    with pytest.warns(DeprecationWarning,match="never implemented"):
        s=PenaltyObliq(4)
    assert s.model_name == "classical_product_bernoulli"
