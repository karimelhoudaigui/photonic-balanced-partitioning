from itertools import combinations
import numpy as np
import pytest

from photonic_balanced_partitioning.photonic.structured_search import (
    LocalBlockProposal, classical_anchor, classical_full_probabilities,
    cut_energy, informed_block, interacting_unitary, pair_unitary, swap_deltas,
)
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq


def test_swap_gain_formula_against_all_exact_cuts():
    rng = np.random.default_rng(421)
    for n in [8, 12]:
        a = rng.uniform(0, 2, (n, n));a=np.triu(a,1);a+=a.T
        anchor = tuple(rng.choice(n,n//2,replace=False))
        occupied,vacant,deltas=swap_deltas(a,anchor)
        current=cut_energy(a,anchor)
        for i,x in enumerate(occupied):
            for j,y in enumerate(vacant):
                proposed=(set(anchor)-{x})|{y}
                assert abs(cut_energy(a,proposed)-current-deltas[i,j])<1e-10


def test_anchor_is_classical_local_minimum_and_budgeted():
    rng=np.random.default_rng(52)
    a=rng.uniform(size=(12,12));a=np.triu(a,1);a+=a.T
    result=classical_anchor(a,seed=91,max_steps=None)
    assert result['local_minimum']
    assert result['final_deltas'].min()>=-1e-10
    assert abs(result['energy']-cut_energy(a,result['partition']))<1e-10
    limited=classical_anchor(a,seed=91,max_steps=2)
    assert limited['steps']<=2
    assert limited['swap_deltas_scored']==(limited['steps']+1)*36
    assert limited['full_cut_evaluations']==1
    occupied,vacant=informed_block(limited,3,seed=177)
    assert len(set(occupied+vacant))==6
    assert set(occupied)<=set(limited['partition'])
    assert not set(vacant)&set(limited['partition'])


@pytest.mark.parametrize('r',[2,3])
@pytest.mark.parametrize('theta',[0,np.pi/8,np.pi/4,np.pi/2])
def test_pair_control_is_collision_free_and_classical(r,theta):
    proposal=LocalBlockProposal(tuple(range(r)),tuple(range(r)),tuple(range(r,2*r)))
    u=pair_unitary(r,theta)
    _,p=proposal.distribution(u,'bosonic')
    _,d=proposal.distribution(u,'distinguishable')
    np.testing.assert_allclose(p,d,atol=1e-12)
    assert p[-1]<1e-12
    assert abs(p[-2]-np.sin(theta)**(2*r))<1e-12


@pytest.mark.parametrize('r',[2,3])
def test_independent_classical_block_replacement_is_exact(r):
    solver=FixedPhotonObliq(2*r,r)
    for seed in range(4):
        u=solver.random_interferometer(904+seed)
        _,expected=classical_full_probabilities(u,r)
        np.testing.assert_allclose(expected,abs(solver.output_state(u))**2,atol=1e-12)
        proposal=LocalBlockProposal(tuple(range(r)),tuple(range(r)),tuple(range(r,2*r)))
        _,p=proposal.distribution(u,'bosonic')
        _,c=proposal.distribution(u,'classical_exact_bosonic')
        np.testing.assert_allclose(p,c,atol=1e-12)


def test_genuine_interference_can_enrich_but_classical_controls_match_or_beat():
    # Explicit non-oracle local graph: only replacing both 0,1 with 2,3 improves.
    a=np.zeros((8,8))
    for i,j,w in [(0,1,5),(2,3,5),(0,6,1),(1,6,1)]:a[i,j]=a[j,i]=w
    proposal=LocalBlockProposal((0,1,4,5),(0,1),(2,3))
    u=interacting_unitary(2,0,np.pi/2) # i times normalized Walsh
    models={}
    for model,unitary in [('bosonic',u),('distinguishable',u),
                          ('pair',pair_unitary(2,np.pi/4)),('correlated_batch',None)]:
        _,p=proposal.distribution(unitary, 'bosonic' if model=='pair' else model)
        models[model]=proposal.statistics(a,p)
    assert abs(models['bosonic']['p_cf']-.5)<1e-12
    assert abs(models['bosonic']['p_improve']-.25)<1e-12
    assert abs(models['distinguishable']['p_improve']-.125)<1e-12
    assert abs(models['pair']['p_improve']-.25)<1e-12
    assert abs(models['correlated_batch']['p_improve']-.5)<1e-12


@pytest.mark.parametrize('r',[2,3])
def test_local_physics_export_perceval(r):
    pcvl=pytest.importorskip('perceval')
    u=interacting_unitary(r,.37,.81)
    np.testing.assert_allclose(u.conj().T@u,np.eye(2*r),atol=1e-12)
    backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
    backend.set_input_state(pcvl.BasicState([1]*r+[0]*r))
    states,p=classical_full_probabilities(u,r)
    reference=backend.prob_distribution()
    np.testing.assert_allclose(p,[reference.get(pcvl.BasicState(s),0) for s in states],atol=1e-12)


def test_spectator_mapping_and_invalid_block():
    p=LocalBlockProposal((0,2,4,6),(2,6),(3,7))
    assert all(len(c)==4 and {0,4}<=set(c) for c in p.candidates)
    assert p.candidates[0]==p.anchor
    assert p.candidates[-1]==(0,3,4,7)
    with pytest.raises(ValueError):LocalBlockProposal((0,1),(0,1),(1,2))
    with pytest.raises(ValueError):LocalBlockProposal((0,1),(0,0),(2,3))
