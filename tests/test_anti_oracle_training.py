"""Information-flow and rejection controls, rather than favorable performance tests."""
import math
import numpy as np
import pytest
from photonic_balanced_partitioning.optimization import training_loss
from photonic_balanced_partitioning.photonic.collision_aware import CollisionAwareSolver


@pytest.mark.parametrize('name',['success','physical_success','p_success','factorized','conditional_success','p_opt_given_cf'])
def test_oracle_losses_are_not_a_blind_training_option(name):
    with pytest.raises(ValueError,match='oracle'):
        training_loss([.5,.5],[1.,3.],[True,True],name)


def test_unknown_optimum_cannot_enter_the_training_interface():
    with pytest.raises(TypeError):training_loss([1.],[3.],[True],optimal_cost=3.)
    p=[.2,.3,.5];cost=[1.,3.,100.];feasible=[True,True,False]
    assert training_loss(p,cost,feasible,'conditional_energy')==pytest.approx(2.2)
    assert training_loss(p,cost,feasible,'collision_aware',mu=2.)==pytest.approx(3.2)
    assert training_loss(p,cost,feasible,'cvar',alpha=.5)==pytest.approx(1.4)


def test_rejected_probability_cannot_be_silently_renormalized_or_rewarded():
    assert math.isinf(training_loss([1.,0.],[0.,2.],[False,True]))
    with pytest.raises(ValueError,match='normalized'):
        training_loss([.2,.3],[1.,3.],[True,True])
    with pytest.raises(ValueError,match='dominate'):
        training_loss([.5,.5],[1.,3.],[True,True],'expected_with_rejection',rejection_cost=0.)
    assert training_loss([.1,.9],[2.,0.],[True,False],'expected_with_rejection',rejection_cost=4.)==pytest.approx(3.8)


def test_collision_aware_public_trainer_does_not_call_retrospective_oracle(monkeypatch):
    import photonic_balanced_partitioning.photonic.objectives as diagnostic
    def forbidden(*a,**k):raise AssertionError('Retrospective optimum leaked into training')
    monkeypatch.setattr(diagnostic,'distribution_metrics',forbidden)
    solver=CollisionAwareSolver(4,2,mu=2.)
    edges=((0,1,1.),(1,2,1.),(2,3,1.))
    assert np.isfinite(solver.expected_objective(np.eye(4),edges))
    result=solver.optimize(edges,num_iterations=2,seed=20261124)
    assert result['uses_optimum_oracle'] is False and result['n_evaluations']==3
    assert result['n_shots']==0
