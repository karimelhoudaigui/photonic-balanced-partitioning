"""Physical and graph conventions for a genuinely changed exploratory route."""
import importlib.util
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('p43_probe', ROOT/'research/P43_global_gain_probe.py')
p43 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p43)


def graph():
    return np.array([[0,2,3,0],[2,0,1,4],[3,1,0,5],[0,4,5,0]],dtype=float)


def test_gradient_is_linear_not_the_signed_single_flip_feature():
    a = graph()
    source = [0,1]
    x = np.array([1,1,0,0])
    gradient = a.sum(axis=1)-2*a@x
    for i in source:
        for j in [2,3]:
            target = (set(source)-{i})|{j}
            assert p43.cut(a,target)-p43.cut(a,source) == gradient[j]-gradient[i]+2*a[i,j]


def test_true_echo_identity_and_graph_relabel_covariance():
    a, source = graph(), [0,1]
    assert np.allclose(p43.echo(a,source,(0,1.1,.7)),np.eye(4),atol=1e-13)
    theta = (np.pi/2,np.pi/4,np.pi/2)
    perm = np.array([2,0,3,1])
    transformed = p43.echo(a[np.ix_(perm,perm)],np.argsort(perm)[source].tolist(),theta)
    expected = p43.echo(a,source,theta)[np.ix_(perm,perm)]
    assert np.allclose(transformed,expected,atol=1e-13)


def test_phase_field_subset_has_fixed_size_and_charged_degeneracy():
    rng = np.random.default_rng(4301)
    assert p43.weighted_subset([0,2,0,3],2,rng) == [1,3]
    assert p43.weighted_subset([0,0,0,1],2,rng) is None
    assert p43.weighted_subset([0,0,0,0],2,rng) is None
    with pytest.raises(ValueError):
        p43.weighted_subset([1,-1,1],2,rng)


def test_local_clifford_sampler_preserves_hom_and_fixed_seed():
    u = np.array([[1,1j],[1j,1]])/np.sqrt(2)
    b,_ = p43.make_optical_sampler(u,[0,1],'bosonic',4302)
    first = [b()[0].tolist() for _ in range(32)]
    assert all(row in ([2,0],[0,2]) for row in first)
    repeat,_ = p43.make_optical_sampler(u,[0,1],'bosonic',4302)
    assert [repeat()[0].tolist() for _ in range(32)] == first
    d,_ = p43.make_optical_sampler(u,[0,1],'distinguishable',4303)
    assert any(d()[0].tolist() == [1,1] for _ in range(32))


def test_species_groups_and_inputs_do_not_drop_or_duplicate_photons():
    b,_ = p43.make_optical_sampler(np.eye(8),list(range(8)),'species4',4304)
    assert b()[0].tolist() == [1]*8
    with pytest.raises(ValueError):
        p43.make_optical_sampler(np.eye(2),[0,0],'bosonic',4305)


def test_zero_intra_layer_has_a_declared_duplicate_law_not_an_extra_mechanism():
    a, source = graph(), [0,1]
    plus = p43.echo(a,source,(np.pi/2,np.pi/4,0))
    minus = p43.echo(a,source,(-np.pi/2,np.pi/4,0))
    r = np.diag([1,1,-1,-1])
    assert np.allclose(minus,r@plus.conj()@r,atol=1e-13)


def test_common_anchor_charges_every_scan_and_retains_the_no_gain_case():
    import io
    stream = io.StringIO()
    source, receipt = p43.prepare_anchor(np.zeros((4,4)),4306,8,stream,'zero')
    assert len(source) == 2 and receipt['final_cut'] == 0
    assert receipt['candidate_scores_including_initial'] == 5
    assert receipt['one_swap_local_minimum_certified']
    assert len(stream.getvalue().splitlines()) == 4
