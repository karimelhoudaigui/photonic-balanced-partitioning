"""Independent full-Fock, Perceval, and analytic tests for occupation moments."""
from itertools import combinations
import math
import numpy as np
import pytest
from photonic_balanced_partitioning.photonic.occupation_objective import (
    occupation_cost,occupation_moments,occupation_expectation,occupation_statistics_gap,
)
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
from photonic_balanced_partitioning.photonic.optical_penalty import _fock_amplitudes

PATH=[(0,1,1.),(1,2,1.),(2,3,1.)]


def probabilities_distinguishable(columns):
    states={(0,)*len(columns):1.}
    for column in columns.T:
        updated={}
        for state,p in states.items():
            for i,q in enumerate(column):
                t=list(state);t[i]+=1;t=tuple(t)
                updated[t]=updated.get(t,0.)+p*q
        states=updated
    assert abs(sum(states.values())-1)<1e-10
    return states


def reference_moments(probabilities):
    states=np.asarray(list(probabilities),dtype=float)
    p=np.array(list(probabilities.values()))
    mean=p@states;second=np.einsum('a,ai,aj->ij',p,states,states)
    collision=float(p@np.sum(states*(states-1)/2,axis=1))
    return mean,second,collision


def check_reference(V,edges,mu,model,probabilities):
    mean,second,collision=reference_moments(probabilities)
    actual=occupation_moments(V,model)
    np.testing.assert_allclose(actual.mean,mean,atol=2e-11,rtol=0)
    np.testing.assert_allclose(actual.second,second,atol=2e-11,rtol=0)
    assert actual.collision_pairs==pytest.approx(collision,abs=2e-11)
    expected=sum(p*occupation_cost(t,edges,mu) for t,p in probabilities.items())
    assert occupation_expectation(V,edges,mu,model)==pytest.approx(expected,abs=2e-10)


def test_identity_and_permutation_preserve_feasible_cost():
    V=np.eye(4,dtype=complex)[:,:2]
    for model in ('bosonic','distinguishable'):
        assert occupation_expectation(V,PATH,4.,model)==pytest.approx(1.)
        assert occupation_moments(V,model).collision_pairs==0
        assert occupation_expectation(V[[0,2,1,3]],PATH,4.,model)==pytest.approx(3.)


def test_hom_hand_computation_and_same_projector_different_frame():
    V=np.eye(4,dtype=complex)[:,:2]
    hom=V.copy();hom[:2,:]=np.array([[1,-1],[1,1]])/np.sqrt(2)
    np.testing.assert_allclose(hom@hom.conj().T,V@V.conj().T,atol=1e-15)
    b,d=occupation_moments(hom),occupation_moments(hom,'distinguishable')
    np.testing.assert_allclose(b.mean,[1,1,0,0],atol=1e-15)
    np.testing.assert_allclose(np.diag(b.second),[2,2,0,0],atol=1e-15)
    np.testing.assert_allclose(np.diag(d.second),[1.5,1.5,0,0],atol=1e-15)
    assert b.second[0,1]==pytest.approx(0.,abs=1e-15)
    assert d.second[0,1]==pytest.approx(.5)
    assert b.collision_pairs==pytest.approx(1.)
    assert d.collision_pairs==pytest.approx(.5)
    edges=[(0,1,1.)]
    assert occupation_expectation(hom,edges,2.)==pytest.approx(6.)
    assert occupation_expectation(hom,edges,2.,'distinguishable')==pytest.approx(3.)
    assert occupation_expectation(V,edges,2.)==pytest.approx(0.)


@pytest.mark.parametrize('n',[4,6])
@pytest.mark.parametrize('seed',range(12))
def test_full_creation_distribution_and_independent_scattering(n,seed):
    U=FixedPhotonObliq(n).random_interferometer(20261121+100*n+seed)
    k=n//2;V=U[:,:k]
    edges=[(i,j,.2+((i+2*j+seed)%7)/5) for i,j in combinations(range(n),2) if (i+j+seed)%3]
    mu=sum(w for _,_,w in edges)+.5
    amplitudes=_fock_amplitudes(U,(1,)*k+(0,)*(n-k),1000)
    boson={t:abs(a)**2 for t,a in amplitudes.items()}
    dist=probabilities_distinguishable(abs(V)**2)
    check_reference(V,edges,mu,'bosonic',boson)
    check_reference(V,edges,mu,'distinguishable',dist)
    moments_b=occupation_moments(V);moments_d=occupation_moments(V,'distinguishable')
    np.testing.assert_allclose(moments_b.second@np.ones(n),k*moments_b.mean,atol=2e-11,rtol=0)
    delta=moments_b.second-moments_d.second
    assert np.linalg.eigvalsh(delta).min()>-2e-12
    np.testing.assert_allclose(delta@np.ones(n),0,atol=2e-12,rtol=0)
    gap=occupation_statistics_gap(V,edges,mu)
    assert gap.total>=0
    assert gap.total==pytest.approx(occupation_expectation(V,edges,mu)-occupation_expectation(V,edges,mu,'distinguishable'),abs=2e-11)


@pytest.mark.parametrize('n',[4,6])
@pytest.mark.parametrize('seed',range(4))
def test_local_perceval_and_single_photon_perceval_distinguishable_control(n,seed):
    pcvl=pytest.importorskip('perceval')
    U=FixedPhotonObliq(n).random_interferometer(90100+100*n+seed)
    k=n//2;V=U[:,:k];edges=[(i,i+1,.5+i/10) for i in range(n-1)];mu=7.
    backend=pcvl.SLOSBackend()
    backend.set_circuit(pcvl.Circuit(n).add(0,pcvl.Unitary(pcvl.Matrix(U))))
    backend.set_input_state(pcvl.BasicState([1]*k+[0]*(n-k)))
    states=FixedPhotonObliq(n)._enumerate_all_fock_states()
    boson={t:float(backend.probability(pcvl.BasicState(list(t)))) for t in states}
    assert abs(sum(boson.values())-1)<2e-11
    check_reference(V,edges,mu,'bosonic',boson)
    # No misleading indistinguishable SLOS call is labelled distinguishable.
    # Scatter each labelled particle through local Perceval separately, then
    # convolve its independent categorical output; this is the exact control.
    columns=np.empty((n,k))
    for a in range(k):
        source=[0]*n;source[a]=1;backend.set_input_state(pcvl.BasicState(source))
        for i in range(n):
            out=[0]*n;out[i]=1
            columns[i,a]=float(backend.probability(pcvl.BasicState(out)))
    dist=probabilities_distinguishable(columns)
    check_reference(V,edges,mu,'distinguishable',dist)


@pytest.mark.parametrize('k',[0,1])
def test_vacuum_and_single_photon_are_identical(k):
    V=FixedPhotonObliq(4).random_interferometer(177)[:,:k]
    b,d=occupation_moments(V),occupation_moments(V,'distinguishable')
    np.testing.assert_allclose(b.mean,d.mean,atol=1e-15)
    np.testing.assert_allclose(b.second,d.second,atol=1e-15)
    assert b.collision_pairs==pytest.approx(0.,abs=1e-15)
    assert occupation_statistics_gap(V,PATH,4.).total==0


def test_disjoint_support_equality_and_mu_zero_boundary():
    V=np.zeros((4,2),complex);V[:2,0]=1/np.sqrt(2);V[2:,1]=1/np.sqrt(2)
    assert occupation_statistics_gap(V,PATH,4.).total==0
    assert occupation_expectation(V,PATH,4.)==pytest.approx(occupation_expectation(V,PATH,4.,'distinguishable'))
    # With mu=0 and disconnected graph, equality need not imply disjointness.
    W=np.array([[1,1],[1,1],[1,-1],[1,-1]])/2
    assert occupation_statistics_gap(W,[(0,1,1.),(2,3,1.)],0.).total==0
    assert occupation_moments(W).collision_pairs>0


def test_mean_dominance_does_not_order_optimal_bisection_success():
    U=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
    amplitudes=_fock_amplitudes(U,(1,1,0,0),100)
    b={t:abs(a)**2 for t,a in amplitudes.items()}
    d=probabilities_distinguishable(abs(U[:,:2])**2)
    target={(1,1,0,0),(0,0,1,1)}
    assert sum(p for t,p in b.items() if t in target)==pytest.approx(.5)
    assert sum(p for t,p in d.items() if t in target)==pytest.approx(.25)
    assert occupation_expectation(U[:,:2],PATH,4.)==pytest.approx(5.5)
    assert occupation_expectation(U[:,:2],PATH,4.,'distinguishable')==pytest.approx(4.)


@pytest.mark.parametrize('edges',[PATH,[(0,1,1.),(1,2,1.),(0,2,1.)],[(0,1,.2),(1,3,2.),(2,3,.9)]])
def test_sufficient_mu_ground_state_proposition(edges):
    mu=sum(w for _,_,w in edges)+.1
    states=FixedPhotonObliq(4)._enumerate_all_fock_states()
    energies=np.array([occupation_cost(t,edges,mu) for t in states])
    cf=np.array([max(t)<=1 for t in states])
    assert energies.min()==pytest.approx(energies[cf].min())
    assert np.all(cf[np.isclose(energies,energies.min(),atol=1e-12,rtol=0)])


def test_collision_penalty_cannot_be_omitted():
    edges=[(0,1,1.),(1,2,1.),(0,2,1.)]
    assert occupation_cost((0,0,0,2),edges,0)==0
    costs=[occupation_cost(tuple(int(i in S) for i in range(4)),edges,0) for S in combinations(range(4),2)]
    assert min(costs)==2


def test_invalid_weights_or_nonphysical_frame_are_rejected():
    V=np.eye(4)[:,:2]
    with pytest.raises(ValueError,match='nonnegative'):
        occupation_expectation(V,[(0,1,-1.)],1.)
    with pytest.raises(ValueError,match='orthonormal'):
        occupation_moments(V*2)
    with pytest.raises(ValueError,match='nonnegative'):
        occupation_cost((1,1,0,0),PATH,-1.)
    with pytest.raises(ValueError):
        occupation_cost((.5,1.5,0,0),PATH,4.)
    with pytest.raises(ValueError):occupation_moments(V,'unknown')
