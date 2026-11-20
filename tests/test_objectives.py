"""Analytic regression cases for collision-aware objectives and sampling."""
import math
import numpy as np
import pytest
from photonic_balanced_partitioning.photonic.objectives import (
    distribution_metrics, objective_value, weighted_lower_cvar, conditional_cvar,
    wilson_interval, expected_shots_interval,
)
from photonic_balanced_partitioning.photonic.collision_aware import CollisionAwareSolver
from photonic_balanced_partitioning.photonic.cvar_fixed_photon import CVaRFixedPhoton
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonResult

STATES = [(1,1,0,0),(1,0,1,0),(2,0,0,0)]
EDGES = [(0,1,1.0),(1,2,1.0),(2,3,1.0)]


def test_collision_leakage_cannot_improve_conditional_objective():
    a = distribution_metrics([0.5,0.5,0.0],STATES,EDGES,1.0)
    b = distribution_metrics([0.05,0.05,0.9],STATES,EDGES,1.0)
    assert a.conditional_energy == pytest.approx(b.conditional_energy)
    assert b.unconditional_cf_energy == pytest.approx(a.unconditional_cf_energy/10)
    assert b.p_success == pytest.approx(a.p_success/10)
    assert objective_value(b,"collision_aware",mu=2) > objective_value(a,"collision_aware",mu=2)
    assert objective_value(b,"log_barrier") > objective_value(a,"log_barrier")
    assert objective_value(b,"success") == pytest.approx(objective_value(b,"factorized"))
    assert b.expected_shots == pytest.approx(20)


def test_zero_cf_is_never_free_energy():
    m = distribution_metrics([0.,0.,1.],STATES,EDGES,1.)
    assert m.p_cf == 0
    assert math.isnan(m.p_opt_given_cf)
    assert m.p_success == 0
    assert math.isinf(m.conditional_energy)
    assert math.isinf(objective_value(m,"collision_aware"))
    assert math.isinf(conditional_cvar([0.,0.,1.],STATES,EDGES))


def test_weights_and_boundary_atom_in_lower_tail_cvar():
    # Lower half takes all mass .2 at cost 1 and .3 at cost 4.
    assert weighted_lower_cvar([1.,4.,9.],[.2,.5,.3],.5) == pytest.approx(2.8)
    assert weighted_lower_cvar([1.,4.,9.],[.2,.5,.3],1.) == pytest.approx(4.9)
    assert weighted_lower_cvar([1.,4.,9.],[.2,.5,.3],.1) == pytest.approx(1.)
    assert weighted_lower_cvar([1.,4.,9.],[2.,5.,3.],.5) == pytest.approx(2.8)
    assert weighted_lower_cvar([1.,4.,9.],alpha=.5) == pytest.approx(2.)
    assert math.isinf(weighted_lower_cvar([]))


@pytest.mark.parametrize("alpha",[0,-.1,1.1,float("nan")])
def test_cvar_rejects_invalid_alpha(alpha):
    with pytest.raises(ValueError):
        weighted_lower_cvar([1,2],alpha=alpha)
    with pytest.raises(ValueError):
        CVaRFixedPhoton(4,alpha=alpha)


def test_cvar_conditions_on_cf_and_uses_probabilities():
    # Non-CF state has .8 mass; conditional optimum mass is 1/4.
    assert conditional_cvar([.05,.15,.8],STATES,EDGES,alpha=.5) == pytest.approx(2.)
    assert conditional_cvar([.05,.15,.8],STATES,EDGES,alpha=1) == pytest.approx(2.5)


def test_invalid_distribution_is_not_silently_renormalized():
    with pytest.raises(ValueError):
        distribution_metrics([.1,.1,.1],STATES,EDGES)


def hom_unitary():
    u = np.eye(4,dtype=complex)
    u[:2,:2] = np.array([[1,-1],[1,1]])/np.sqrt(2)
    return u


def test_collision_wrapper_reports_hom_and_preserves_shots():
    solver = CollisionAwareSolver(4,mu=3)
    assert solver.compute_collision_probability(hom_unitary()) == pytest.approx(1.)
    draws = solver.sample(hom_unitary(),50,seed=18,edges=EDGES)
    assert len(draws) == 50
    assert all(r.has_collision and not r.is_valid and not r.is_balanced for r in draws)
    assert all(r.collision_penalty == 3 for r in draws)
    assert math.isinf(solver.expected_objective(hom_unitary(),EDGES))


def test_collision_wrapper_seed_is_forwarded_as_keyword():
    solver = CollisionAwareSolver(4)
    u = solver._base_solver.random_interferometer(seed=22)
    a = solver.sample(u,50,seed=71,edges=EDGES)
    b = solver.sample(u,50,seed=71,edges=EDGES)
    assert [r.occupation_numbers for r in a] == [r.occupation_numbers for r in b]
    np.testing.assert_allclose([r.energy for r in a],[r.energy for r in b],equal_nan=True)


def test_cvar_sample_keeps_partition_after_rejection(monkeypatch):
    solver = CVaRFixedPhoton(4,alpha=1)
    samples = [
        FixedPhotonResult((2,0,0,0),False,True,float("nan"),None,.5),
        FixedPhotonResult((1,0,1,0),True,True,3.,(0,2),.25),
        FixedPhotonResult((1,1,0,0),True,True,1.,(0,1),.25),
    ]
    monkeypatch.setattr(solver._base_solver,"sample",lambda *args,**kwargs:samples)
    r = solver.sample(np.eye(4),3,EDGES,seed=1)
    assert r.partition == (0,1)
    assert r.energy == 1.
    assert r.cvar == pytest.approx(2.)
    monkeypatch.setattr(solver._base_solver,"sample",lambda *args,**kwargs:samples[:1])
    r = solver.sample(np.eye(4),1,EDGES,seed=1)
    assert r.partition is None and math.isinf(r.cvar)


def test_binomial_and_reciprocal_intervals():
    low,high = wilson_interval(50,100)
    assert low == pytest.approx(1-high)
    assert low < .5 < high
    a,b = expected_shots_interval(50,100)
    assert a == pytest.approx(1/high)
    assert b == pytest.approx(1/low)
    assert math.isinf(expected_shots_interval(0,100)[1])
    assert wilson_interval(100,100)[1] == 1
