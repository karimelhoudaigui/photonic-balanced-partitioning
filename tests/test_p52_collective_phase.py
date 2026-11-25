"""P52 hand cases and bounded code fixtures, no DEV graph or optimizer result."""
import importlib.util
import io
import itertools
import json
import math
from pathlib import Path
import sys
import warnings

import numpy as np
import pytest
from scipy.optimize import OptimizeWarning

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"research"))
SPEC=importlib.util.spec_from_file_location("p52_probe",ROOT/"research/P52_collective_phase_probe.py")
p52=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(p52)


def permanent(matrix):
    return sum((np.prod([matrix[i,j] for i,j in enumerate(order)])
                for order in itertools.permutations(range(len(matrix)))),0j)


def direct_amplitudes(u,sources,counts):
    result=[]
    for row in counts:
        slots=[i for i,n in enumerate(row) for _ in range(int(n))]
        result.append(permanent(u[np.ix_(slots,sources)])/math.sqrt(math.prod(math.factorial(int(n)) for n in row)))
    return np.asarray(result)


@pytest.mark.parametrize("m,r",[(2,2),(3,3),(4,4),(8,8)])
def test_compact_support_is_complete_including_all_zeros(m,r):
    space=p52.FockSpace(m,r)
    for total,rows in enumerate(space.counts):
        assert rows.shape==(math.comb(m+total-1,total),m)
        assert np.all(rows>=0) and np.all(rows.sum(axis=1)==total)
        assert len(np.unique(space.keys[total]))==len(rows)
        assert np.array_equal(space.lookup_keys(space.keys[total],total),np.arange(len(rows)))
    if m==8:
        assert len(space.counts[8])==6435 and len(space.counts[4])==330
        assert sum(np.all(space.counts[8]==1,axis=1))==1


@pytest.mark.parametrize("m,r",[(2,2),(3,3),(4,4)])
def test_creation_amplitudes_match_direct_permanents_and_fock_factorials(m,r):
    indices=np.arange(m)
    u=np.exp(2j*np.pi*indices[:,None]*indices[None,:]/m)/math.sqrt(m)
    u=np.exp(1j*indices*.37)[:,None]*u
    space=p52.FockSpace(m,r)
    amplitude,probability=p52.creation_law(u,range(r),space)
    expected=direct_amplitudes(u,list(range(r)),space.counts[r])
    assert amplitude==pytest.approx(expected,abs=3e-12)
    assert probability.sum()==pytest.approx(1.,abs=3e-12)
    assert len(probability)==len(space.counts[r])


def test_HOM_is_bunched_with_output_factorial_normalization():
    u=np.asarray([[1,1],[1,-1]])/math.sqrt(2)
    space=p52.FockSpace(2,2)
    _,p=p52.creation_law(u,[0,1],space)
    law={tuple(row):v for row,v in zip(space.counts[2],p)}
    assert law[(1,1)]==pytest.approx(0.,abs=1e-25)
    assert law[(2,0)]==pytest.approx(.5) and law[(0,2)]==pytest.approx(.5)


def test_CF_creation_commutes_in_input_order_and_rejects_duplicate_sources():
    u=p52.w4().astype(complex)
    space=p52.FockSpace(4,4)
    first=p52.creation_law(u,[0,1,3],space)[0]
    other=p52.creation_law(u,[3,0,1],space)[0]
    assert first==pytest.approx(other,abs=2e-13)
    with pytest.raises(ValueError):p52.creation_law(u,[0,0],space)


def test_monomial_eight_photon_law_has_full_unpruned_support():
    space=p52.FockSpace(8,8)
    amplitude,p=p52.creation_law(np.eye(8,dtype=complex),range(8),space)
    index=np.flatnonzero(np.all(space.counts[8]==1,axis=1))[0]
    assert len(amplitude)==6435 and len(p)==6435
    assert p[index]==1 and np.count_nonzero(p)==1


@pytest.mark.parametrize("theta",[0.,math.pi/4,math.pi/2,3*math.pi/4])
def test_U8_flat_unitary_Q_P_covariance_and_between_layer_phase(theta):
    u=p52.interferometer(theta)
    q=abs(u)**2
    assert u.conj().T@u==pytest.approx(np.eye(8),abs=2e-13)
    assert q==pytest.approx(np.full((8,8),1/8),abs=2e-14)
    mu=q.sum(axis=1);projection=u@u.conj().T
    covariance=np.diag(mu)+abs(projection)**2-2*q@q.T
    assert mu==pytest.approx(np.ones(8),abs=2e-14)
    assert covariance==pytest.approx(2*np.eye(8)-np.ones((8,8))/4,abs=2e-13)


def test_input_permutation_conjugation_identifies_theta3_full_B_law_without_seedwise_MC_claim():
    permutation=[0,1,2,3,6,7,4,5]
    u1=p52.interferometer(math.pi/4)
    u3=p52.interferometer(3*math.pi/4)
    assert u3==pytest.approx(u1.conj()[:,permutation],abs=2e-13)
    mapped=p52.grouping_permutation()
    assert sorted(mapped.tolist())==list(range(35))
    assert p52.all_groupings()[0]==((0,1,2,3),(4,5,6,7))


@pytest.mark.parametrize("theta",[math.pi/4,math.pi/2,3*math.pi/4])
def test_canonical_b4_species_frames_have_only_output_row_phases(theta):
    reference=p52.interferometer(0.)
    u=p52.interferometer(theta)
    row_phase=np.tile(np.exp(1j*np.arange(4)*theta),2)
    assert u[:,:4]==pytest.approx(reference[:,:4],abs=2e-14)
    assert u[:,4:]==pytest.approx(row_phase[:,None]*reference[:,4:],abs=2e-14)
    space=p52.FockSpace(8,4)
    for group in (range(4),range(4,8)):
        assert p52.creation_law(u,group,space)[1]==pytest.approx(
            p52.creation_law(reference,group,space)[1],abs=2e-13)


@pytest.mark.parametrize("theta,expected",[(0.,1.5),(math.pi/2,.5)])
def test_independent_analytic_collective_fourth_witness_not_a_rank_mean_claim(theta,expected):
    space=p52.FockSpace(8,8)
    _,p=p52.creation_law(p52.interferometer(theta),range(8),space)
    assert p52.collective_fourth(space.counts[8],p)==pytest.approx(expected,abs=2e-11)


def test_compact_species_convolution_matches_scalar_dictionary_without_extra_factorials():
    space=p52.FockSpace(4,4)
    first=p52.creation_law(p52.w4(),[0,1],space)[1]
    second=p52.creation_law(p52.w4(),[2,3],space)[1]
    mapping=space.convolution_map(2,2)
    actual=np.bincount(mapping.ravel(),weights=np.outer(first,second).ravel(),minlength=len(space.counts[4]))
    index={tuple(row):i for i,row in enumerate(space.counts[4])}
    expected=np.zeros(len(actual))
    for i,a in enumerate(space.counts[2]):
        for j,b in enumerate(space.counts[2]):expected[index[tuple(a+b)]]+=first[i]*second[j]
    assert actual==pytest.approx(expected,abs=1e-14)
    assert actual.sum()==pytest.approx(1.,abs=1e-13)
    full=p52.creation_law(p52.w4(),range(4),space)[1]
    assert max(abs(actual-full))>.01  # species convolution is not coherent amplitude addition


def test_all35_groupings_are_complete_unordered_splits_and_map_is_compact():
    splits=p52.all_groupings()
    assert len(splits)==35 and len(set(first for first,_ in splits))==35
    for first,second in splits:
        assert len(first)==len(second)==4 and 0 in first
        assert set(first).isdisjoint(second) and set(first)|set(second)==set(range(8))
    space=p52.FockSpace(8,8)
    mapping=space.convolution_map(4,4)
    assert mapping.shape==(330,330)
    assert mapping.nbytes==330*330*4
    assert np.array_equal(space.counts[8][mapping],space.counts[4][:,None,:]+space.counts[4][None,:,:])


def test_tie_integration_is_uniform_over_only_admissible_completions():
    rows=np.asarray([[4,0,0,0],[2,2,0,0],[2,1,1,0],[1,1,1,1]])
    decoder=p52.RankDecoder(rows,2)
    lookup={subset:i for i,subset in enumerate(decoder.subsets)}
    assert decoder.push[0,lookup[(0,1)]]==pytest.approx(1/3)
    assert np.count_nonzero(decoder.push[0])==3
    assert decoder.push[1,lookup[(0,1)]]==1
    assert decoder.push[2,lookup[(0,1)]]==decoder.push[2,lookup[(0,2)]]==.5
    assert decoder.push[3]==pytest.approx(np.full(6,1/6))
    assert decoder.push.sum(axis=1)==pytest.approx(np.ones(4))


@pytest.mark.parametrize("phi",[0.,math.pi/2])
def test_H4_exact_full_ranked_law_known_fourth_order_checkpoint(phi):
    z=np.exp(1j*phi)
    u=np.asarray([[1,1,1,1],[1,z,-1,-z],[1,-1,1,-1],[1,-z,-1,z]],dtype=complex)/2
    space=p52.FockSpace(4,4)
    _,p=p52.creation_law(u,range(4),space)
    decoder=p52.RankDecoder(space.counts[4],2)
    rank,_=decoder.apply(p)
    t=math.cos(phi)**2
    for subset,value in zip(decoder.subsets,rank):
        assert value==pytest.approx(1/8+t/24 if subset in [(0,2),(1,3)] else 3/16-t/48,abs=2e-13)


def test_rank_crossing_row_sums4_total16_and_uniform4over7_for_entire_support():
    space=p52.FockSpace(8,8)
    decoder=p52.RankDecoder(space.counts[8],4)
    assert decoder.push.shape==(6435,70)
    assert decoder.push.sum(axis=1)==pytest.approx(np.ones(6435),abs=2e-14)
    assert p52.crossing_row_sums(decoder.crossing,decoder.edges,8)==pytest.approx(np.full((70,8),4.))
    assert decoder.crossing.sum(axis=1)==pytest.approx(np.full(70,16.))
    uniform=np.full(70,1/70)@decoder.crossing
    assert uniform==pytest.approx(np.full(28,4/7),abs=2e-14)


def test_Walsh8_B_crossing_uniformity_is_not_a_full_rank_law_assertion():
    space=p52.FockSpace(8,8)
    _,p=p52.creation_law(p52.interferometer(0.),range(8),space)
    decoder=p52.RankDecoder(space.counts[8],4)
    rank,crossing=decoder.apply(p)
    assert rank.sum()==pytest.approx(1.,abs=2e-13)
    assert crossing==pytest.approx(np.full(28,4/7),abs=2e-12)
    # AGL(3,2) is 2-transitive, not transitive on all four-subsets.
    # Deliberately no assertion that the 70 probabilities equal1/70.


def test_low_factorial_moments_H4_fixed_through_three_despite_rank_response():
    space=p52.FockSpace(4,4)
    laws=[]
    for phi in (0.,math.pi/2):
        z=np.exp(1j*phi)
        u=np.asarray([[1,1,1,1],[1,z,-1,-z],[1,-1,1,-1],[1,-z,-1,z]],dtype=complex)/2
        laws.append(p52.creation_law(u,range(4),space)[1])
    labels,moments=p52.factorial_moments(np.asarray(laws),space.counts[4],3)
    assert labels.shape==(35,4) and np.all(labels.sum(axis=1)<=3)
    assert moments[0]==pytest.approx(moments[1],abs=3e-12)
    assert list(moments[0,labels.sum(axis=1)==0])==pytest.approx([1.])


def test_phase_multinomial_counts_and_orientation_are_conditional_on_continuous_coefficients():
    class FixtureRNG:
        def uniform(self,low,high,shape):
            assert (low,high,shape)==(0.,2*math.pi,(2,2))
            return np.asarray([[0.,0.],[0.,math.pi]])
        def random(self,shape):
            assert shape==(2,2)
            return np.asarray([[.1,.9],[.3,.7]])
    counts,record=p52.phase_counts(np.asarray([[1,1],[1,-1]])/math.sqrt(2),FixtureRNG(),2,2)
    assert counts.tolist()==[[2,0],[0,2]]
    assert record["maximum_raw_probability_mass_error"]<1e-13
    assert len(record["angles_sha256"])==len(record["counts_sha256"])==64


def test_phase_histogram_accounts_every_batch_without_using_main_source_or_seed(monkeypatch):
    monkeypatch.setattr(p52,"DRAW_COUNT",32);monkeypatch.setattr(p52,"BATCH_SIZE",8)
    monkeypatch.setattr(p52,"seed_for",lambda root,index:520008)
    space=p52.FockSpace(8,8);stream=io.StringIO()
    hist,records=p52.phase_histogram(np.eye(8),space,0,stream,draws=32,batch_size=8)
    assert hist.shape==(6435,) and hist.sum()==32 and len(records)==4
    assert [row["first_draw"] for row in records]==[0,8,16,24]
    assert all(row["seed"]==520008 for row in records)
    assert len(stream.getvalue().splitlines())==4
    assert records[0]["state_after_sha256"]==records[1]["state_before_sha256"]


def test_union392_epsilon_and_data_dependent_MC_mixture_weight_are_not_divided_by_four():
    expected=math.sqrt(math.log(2*392/.01)/(2*262144))
    assert p52.phase_epsilon()==expected
    library=np.asarray([np.zeros(28),np.ones(28),np.full(28,.5)])
    raw=np.asarray([.25,.25,.5])
    result=p52.verify_coefficients(raw,library,np.full(28,.5),mc_start=2,epsilon=expected)
    assert result["verified"] and result["verified_Linfty_residual"]<1e-14
    assert result["MC_mixture_weight"]==.5 and result["MC_uniform_bound_term"]==expected*.5
    assert result["total_residual_plus_MC_term"]==pytest.approx(expected*.5)


@pytest.mark.parametrize("raw",[[-.1,1.1],[0.,0.],[.4,.4],[float('nan'),1.]])
def test_invalid_convex_candidate_is_not_rescued_by_solver_success(raw):
    result=p52.verify_coefficients(raw,np.asarray([np.zeros(28),np.ones(28)]),np.zeros(28))
    assert result["verified"] is False
    json.dumps(result,allow_nan=False)


def test_tiny_negative_projection_is_recorded_and_residual_recomputed():
    raw=np.asarray([-1e-12,1.+1e-12])
    result=p52.verify_coefficients(raw,np.asarray([np.zeros(28),np.ones(28)]),np.ones(28))
    assert result["verified"] and result["projection_L1"]>0
    assert result["used_coefficients"]==[0.,1.]
    assert result["verified_Linfty_residual"]==0


def test_supported_pinned_LP_options_have_native_single_thread_readback_and_verified_coefficients():
    result=p52.convex_fit(np.asarray([np.zeros(28),np.ones(28)]),np.full(28,.25))
    assert result["status"]=="NUMERICAL_MEAN_MATCH"
    assert result["native_options_readback"]["threads"]==1
    assert result["native_options_readback"]["parallel"]=="off"
    assert result["native_options_readback"]["time_limit"]==1.
    assert result["verification"]["verified_Linfty_residual"]<=1e-9
    assert result["options"]["parallel"] is False
    assert any("These will be passed to HiGHS verbatim." in text for text in result["warnings"])


def test_internal_option_warning_makes_fit_inconclusive_without_solver_replacement(monkeypatch):
    monkeypatch.setattr(p52,"native_single_thread_check",lambda:{"threads":1})
    class FakeResult:
        x=np.asarray([1.,0.]);status=0;success=True;message='mock';fun=0.
    def wrong(*args,**kwargs):
        warnings.warn('Option threads ignored. Using default.',OptimizeWarning)
        return FakeResult()
    monkeypatch.setattr(p52,"linprog",wrong)
    result=p52.convex_fit(np.zeros((1,28)),np.zeros(28))
    assert result["status"]=="INCONCLUSIVE_SOLVER" and 'ignored' in result["error"]


def test_solver_status_alone_does_not_create_a_mean_match(monkeypatch):
    monkeypatch.setattr(p52,"native_single_thread_check",lambda:{"threads":1})
    class FakeResult:
        x=np.asarray([1.,0.]);status=0;success=True;message='mock';fun=0.
    monkeypatch.setattr(p52,"linprog",lambda *args,**kwargs:FakeResult())
    result=p52.convex_fit(np.zeros((1,28)),np.ones(28))
    assert result["solver_success"] is True and result["status"]=="NO_VERIFIED_TOLERANCE_MATCH"
    assert result["verification"]["verified_Linfty_residual"]==1.
