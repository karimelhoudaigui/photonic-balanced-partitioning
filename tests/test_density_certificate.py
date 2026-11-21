"""Physical and scope regressions for the candidate density certificate."""
import numpy as np
import pytest
from scipy.linalg import expm
from photonic_balanced_partitioning.photonic.density_certificate import density_certificate


def pair_frame(m):
    v=np.zeros((m,m//2),complex)
    for a in range(m//2):v[2*a:2*a+2,a]=1/np.sqrt(2)
    return v


def test_disjoint_probabilistic_orbitals_are_classical_without_deterministic_photons():
    result=density_certificate(pair_frame(12))
    assert result['expected_collision_pairs']==pytest.approx(0.,abs=1e-12)
    assert result['minimum_positive_intensity']==pytest.approx(.5)
    assert result['support_cycle_tv_bound']==pytest.approx(0.,abs=1e-12)


def test_dilute_balanced_spectators_do_not_yield_a_false_small_certificate():
    k=12;m=2*k;active=k+2;v=np.zeros((m,k),complex)
    v[:active,0]=1/np.sqrt(active)
    v[:active,1]=np.r_[np.ones(active//2),-np.ones(active//2)]/np.sqrt(active)
    for a in range(2,k):v[active+a-2,a]=1
    result=density_certificate(v)
    assert result['expected_collision_pairs']==pytest.approx(2/active)
    assert result['minimum_positive_intensity']==pytest.approx(2/active)
    assert result['density_cycle_tv_bound']==1
    assert result['dominant_support_leakage']==pytest.approx(1.)


def test_support_bound_is_invariant_under_output_labels():
    rng=np.random.default_rng(65173);h=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));h=(h+h.conj().T)/2
    v=expm(.02j*h)@pair_frame(8);first=density_certificate(v)
    second=density_certificate(v[rng.permutation(8)])
    for key in ['expected_collision_pairs','dominant_support_leakage','support_cycle_tv_bound']:
        assert first[key]==pytest.approx(second[key],abs=1e-12)


def test_nonorthogonal_frame_is_rejected():
    with pytest.raises(ValueError,match='orthonormal'):
        density_certificate(np.ones((4,2))/2)


def test_small_angle_does_not_lose_collision_mass_by_subtraction():
    angle=1e-10;c,s=np.cos(angle),np.sin(angle)
    v=pair_frame(4)@np.array([[c,-s],[s,c]])
    result=density_certificate(v);expected=2*c*c*s*s
    assert result['expected_collision_pairs']==pytest.approx(expected,rel=1e-12,abs=0.)
    assert result['dominant_support_leakage']==pytest.approx(2*s*s,rel=1e-12,abs=0.)
    assert result['support_cycle_tv_bound']>=expected*(1-1e-12)
    assert result['numerical_semantics']=='FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED'
