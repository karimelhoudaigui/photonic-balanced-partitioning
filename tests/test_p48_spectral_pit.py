"""P48 independent finite physical fixtures; no DEV graph outcomes."""
import importlib.util
import io
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"research"))
SPEC=importlib.util.spec_from_file_location("p48_probe",ROOT/"research/P48_spectral_pit_probe.py")
p48=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p48)


def permanent_explicit(matrix):
    return sum((np.prod([matrix[i,j] for i,j in enumerate(order)])
                for order in itertools.permutations(range(len(matrix)))),0j)


def fock_law(u,source):
    m,r=len(u),len(source); result={}
    for slots in itertools.combinations_with_replacement(range(m),r):
        counts=tuple(slots.count(i) for i in range(m))
        result[counts]=abs(permanent_explicit(u[np.ix_(slots,source)]))**2/math.prod(math.factorial(x) for x in counts)
    return result


def labeled_law(u,source):
    result={}
    for slots in itertools.product(range(len(u)),repeat=len(source)):
        counts=tuple(slots.count(i) for i in range(len(u)))
        value=math.prod(abs(u[slots[j],source[j]])**2 for j in range(len(source)))
        result[counts]=result.get(counts,0.)+value
    return result


def example(encoder="spectral_graph"):
    a=np.asarray([[0,3,0,2,4,0],[3,0,1,0,3,2],[0,1,0,2,1,4],
                  [2,0,2,0,4,1],[4,3,1,4,0,2],[0,2,4,1,2,0]],dtype=float)
    marks=np.asarray([.1,.7,.3,.5,.9,.2]); priority=[2,0,4,1,5,3]
    spectral=p48.spectral_data(a,marks,priority,3)
    v=spectral["v"] if encoder=="spectral_graph" else p48.fourier_basis(6,3,priority)
    context=p48.build_network(v,encoder)
    return a,marks,priority,spectral,context


@pytest.mark.parametrize("encoder",["Fourier_blind","spectral_graph"])
def test_count_marginals_and_covariance_against_independent_enumeration(encoder):
    _,_,_,spectral,context=example(encoder)
    assert spectral["numerical_status"]=="PASS"
    assert len(spectral["guarded_gaps"])==3 and len(spectral["all_gaps"])==5
    tables,_,_,_=p48.all_marginals(context,[2,0,1])
    b=fock_law(context["u"],[0,1,2]); d=labeled_law(context["u"],[0,1,2])
    assert sum(b.values())==pytest.approx(1.,abs=2e-12)
    assert sum(d.values())==pytest.approx(1.,abs=2e-12)
    for model,law in (("bosonic",b),("distinguishable",d)):
        for i in range(6):
            actual=[sum(mass for counts,mass in law.items() if counts[i]==s) for s in range(4)]
            assert tables[model][i]==pytest.approx(actual,abs=2e-12)
    assert tables["species4"]==pytest.approx(tables["bosonic"],abs=2e-12)
    mean=np.zeros(6); second=np.zeros((6,6))
    for counts,mass in b.items():
        mean+=mass*np.asarray(counts); second+=mass*np.outer(counts,counts)
    assert context["mu"]==pytest.approx(mean,abs=2e-12)
    assert context["cov"]==pytest.approx(second-np.outer(mean,mean),abs=3e-12)
    assert context["source_ports"]==[0,1,2]
    assert context["u"][:,:3]==pytest.approx(context["v"],abs=1e-15)


@pytest.mark.parametrize("encoder",["Fourier_blind","spectral_graph"])
def test_analytic_phase_marginals_by_all_small_phase_assignments(encoder):
    _,_,_,_,context=example(encoder)
    tables,_,_,_=p48.all_marginals(context,[0,1,2]); v=context["v"]
    expected=np.zeros((6,4))
    # r+1 roots reproduce the count polynomial exactly here; production uses
    # continuous phases, including for NONPOLYNOMIAL top-K baseline rounding.
    for exponents in itertools.product(range(4),repeat=3):
        z=np.exp(2j*np.pi*np.asarray(exponents)/4)/math.sqrt(3)
        probabilities=abs(v@z)**2
        assert probabilities.sum()==pytest.approx(1.,abs=2e-12)
        for i,probability in enumerate(probabilities):
            for count in range(4):
                expected[i,count]+=math.comb(3,count)*probability**count*(1-probability)**(3-count)/64
    assert tables["continuous_phase"]==pytest.approx(expected,abs=2e-12)


def test_species4_plus_one_by_independent_fock_groups():
    v=p48.fourier_basis(10,5,list(range(10)))
    context=p48.build_network(v,"fixture")
    tables,_,_,_=p48.all_marginals(context,[4,0,3,1,2])
    group=fock_law(context["u"],[4,0,3,1]); singleton=labeled_law(context["u"],[2])
    for mode in range(10):
        expected=np.zeros(6)
        first=np.asarray([sum(mass for counts,mass in group.items() if counts[mode]==s) for s in range(5)])
        last=np.asarray([sum(mass for counts,mass in singleton.items() if counts[mode]==s) for s in range(2)])
        for a,mass in enumerate(first):
            for b,other in enumerate(last):
                expected[a+b]+=mass*other
        assert tables["species4"][mode]==pytest.approx(expected,abs=2e-12)


def test_vacuum_completion_does_not_change_the_occupied_state():
    _,_,_,_,context=example(); u=context["u"]; v=context["v"]
    rotation=np.exp(2j*np.pi*np.arange(3)[:,None]*np.arange(3)[None,:]/3)/math.sqrt(3)
    altered=np.column_stack((v,u[:,3:]@rotation))
    assert altered.conj().T@altered==pytest.approx(np.eye(6),abs=3e-12)
    assert list(fock_law(altered,[0,1,2]).values())==pytest.approx(list(fock_law(u,[0,1,2]).values()),abs=3e-12)


def test_source_basis_rotations_are_not_silently_haar_averaged():
    v=np.eye(4,2,dtype=complex)
    rotation=np.asarray([[1,1],[1,-1]])/math.sqrt(2)
    original=p48.build_network(v,"fixture"); rotated=p48.build_network(v@rotation,"fixture")
    assert original["projection"]==pytest.approx(rotated["projection"],abs=1e-12)
    before=fock_law(original["u"],[0,1]); after=fock_law(rotated["u"],[0,1])
    assert before[(1,1,0,0)]==pytest.approx(1.)
    assert after[(1,1,0,0)]==pytest.approx(0.,abs=1e-25)
    assert after[(2,0,0,0)]==pytest.approx(.5)


def test_carried_marks_orders_and_occupied_columns_under_relabeling():
    a,marks,priority,spectral,_=example()
    permutation=np.asarray([3,0,5,1,4,2])
    carried=np.zeros_like(a); carried[np.ix_(permutation,permutation)]=a
    carried_marks=np.zeros_like(marks); carried_marks[permutation]=marks
    shifted=p48.spectral_data(carried,carried_marks,permutation[priority].tolist(),3)
    assert shifted["numerical_status"]=="PASS"
    assert shifted["v"][permutation]==pytest.approx(spectral["v"],abs=3e-11)
    blind=p48.fourier_basis(6,3,priority)
    shifted_blind=p48.fourier_basis(6,3,permutation[priority].tolist())
    assert shifted_blind[permutation]==pytest.approx(blind,abs=1e-15)


def test_zero_graph_mu0_mu1_and_empty_gaussian_rows():
    spectral=p48.spectral_data(np.zeros((6,6)),np.asarray([.1,.2,.3,.4,.5,.6]),list(range(6)),3)
    assert spectral["numerical_status"]=="PASS"
    context=p48.build_network(spectral["v"],"zero_fixture")
    tables,_,_,_=p48.all_marginals(context,[0,1,2])
    for mode in range(6):
        if context["mu"][mode]==0:
            for table in tables.values():
                assert table[mode].tolist()==[1.,0.,0.,0.]
            assert context["variance"][mode]==0
        else:
            assert context["mu"][mode]==1
            assert tables["bosonic"][mode].tolist()==[0.,1.,0.,0.]
            assert tables["spherical_coherent"][mode]==pytest.approx([.4,.3,.2,.1])
    draw=p48.make_field(context,[0,1,2],"gaussian_Bcov",480081,tables)
    field,counts,_=draw()
    assert counts is None and len(set(field))>1
    assert all(-.5<=value<=.5 for value in field)


@pytest.mark.parametrize("marks,expected",[
    ([.1,.1,.3,.4,.5,.6],"INCONCLUSIVE"),
    ([.1,.2,.3,.3,.5,.6],"INCONCLUSIVE"),
    ([.1,.2,.3,.6,.6,.6],"PASS"),
    ([0,0,0,0,0,0],"INCONCLUSIVE")])
def test_gap_guards_cover_occupied_basis_and_boundary_not_empty_complement(marks,expected):
    result=p48.spectral_data(np.zeros((6,6)),np.asarray(marks),list(range(6)),3)
    assert result["numerical_status"]==expected
    assert len(result["all_gaps"])==5 and len(result["guarded_gaps"])==3


def test_subunit_rows_are_preserved_and_tiny_excess_is_explicit():
    original=[.1,.2]; row,diagnostic=p48.repair_probability_row(original)
    assert row==tuple(Fraction.from_float(x) for x in original)
    assert sum(row)<1 and diagnostic["input_roundoff_repair_L1"]=="0"
    repaired,record=p48.repair_probability_row([np.nextafter(1.,2.),0.])
    assert sum(repaired)==1 and Fraction(record["input_roundoff_repair_L1"])>0
    assert record["subunit_row_rescaled_to1"] is False
    with pytest.raises(p48.NumericalInconclusive):
        p48.repair_probability_row([1.01,0.])


def test_randomized_pit_and_actual_gaussian_variance():
    _,_,_,_,context=example(); table=np.asarray([[.2,.3,.5],[1.,0.,0.]])
    assert p48.pit([1,0],table,np.asarray([.4,.7]))==pytest.approx([.32,.7])
    with pytest.raises(ValueError):
        p48.pit([.5,0],table,np.asarray([.4,.7]))
    draw=p48.make_field(context,[0,1,2],"gaussian_Bcov",480082,{})
    fields,counts,metadata=draw(); raw=np.asarray(metadata["gaussian_raw"])
    actual=np.einsum("ij,ij->i",context["factor"],context["factor"])
    assert context["variance"]==pytest.approx(actual,abs=1e-15)
    assert fields==pytest.approx(p48.ndtr(raw/np.sqrt(actual))-.5,abs=1e-15)
    assert counts is None


@pytest.mark.parametrize("n,k,units",[(26,13,100),(34,17,173)])
def test_shared_decoder_informative_units(n,k,units):
    result=p48.adaptive.complete(np.zeros((n,n)),np.linspace(-.5,.5,n),k,1,list(range(n)),(k+1)//2)
    assert result["score_units"]==units and len(result["subset"])==k


def test_strong_rounding_baseline_scores_every_rounding_and_swap():
    blind=p48.build_network(p48.fourier_basis(6,3,list(range(6))),"Fourier_blind")
    graph=p48.build_network(np.eye(6,3,dtype=complex),"spectral_graph")
    stream=io.StringIO()
    result=p48.spectral_coherent_rounding(np.zeros((6,6)),[blind,graph],list(range(6)),0,
                                          480083,40,stream,{"case":"fixture"})
    rows=[json.loads(line) for line in stream.getvalue().splitlines()]
    assert len(rows)==result["candidate_scores"]==40
    rounded=[r for r in rows if r["kind"]=="rounding"]
    assert [(r["encoder"],r["coefficient_law"]) for r in rounded]==[
        ("Fourier_blind","continuous_phase"),("Fourier_blind","sphere"),
        ("spectral_graph","continuous_phase"),("spectral_graph","sphere")]
    assert all(len(r["subset"])==len(set(r["subset"]))==3 and r["cut"]==0 for r in rows)


def test_numerical_case_is_retained_without_redraw(monkeypatch,tmp_path):
    monkeypatch.setattr(p48.base,"make_graph",lambda case:np.zeros((6,6)))
    original=p48.spectral_data
    monkeypatch.setattr(p48,"spectral_data",lambda a,marks,priority,r,*limits:
                        original(a,np.zeros(6),priority,r,*limits))
    stream=io.StringIO(); case={"id":"guard_fixture","m":6,"k":3,"r":3,"seed":480084}
    spec={"anchor_max_scans":8,"gap_tolerance":1e-12,"residual_tolerance":3e-12,"decoder_lambda":[0,1]}
    _,contexts,common,_=p48.prepare(case,spec,stream,tmp_path)
    assert contexts is None and common["numerical_status"]=="INCONCLUSIVE"
    saved=json.loads((tmp_path/"context_guard_fixture.json").read_text())
    assert saved["numerical_status"]=="INCONCLUSIVE" and saved["networks"]==[]
    assert any(json.loads(line)["stage"]=="numerical_inconclusive" for line in stream.getvalue().splitlines())


def test_local_clifford_source_ports_and_full_observation():
    _,_,_,_,context=example()
    sample,_=p48.base.make_optical_sampler(context["u"],[0,1,2],"bosonic",480080)
    counts,rejected=sample()
    assert not rejected and len(counts)==6 and counts.sum()==3


@pytest.mark.parametrize("model",["continuous_phase","spherical_coherent"])
def test_production_coherent_generator_and_analytic_pit_interface(model):
    _,_,_,_,context=example()
    tables,_,_,_=p48.all_marginals(context,[0,1,2])
    draw=p48.make_field(context,[0,1,2],model,480085,tables)
    for _ in range(3):
        field,counts,metadata=draw()
        assert counts.sum()==3 and min(counts)>=0 and len(counts)==6
        assert metadata["coherent_probability_sum"]==pytest.approx(1.,abs=3e-12)
        assert metadata["sampler_roundoff_normalization_L1"]<3e-12
        assert all(-.5<=value<=.5 for value in field)
        reconstructed=p48.pit(counts,tables[model],np.asarray(metadata["pit_jitter"]))-.5
        assert field==pytest.approx(reconstructed,abs=1e-15)


def test_direct_preparation_roundings_and_labelled_assignment_optimum():
    _,_,priority,_,context=example()
    candidates=list(p48.preparation_candidates(context,priority,3))
    assert len(candidates)==2*(3+1)+1
    assert sum(label=="mu" for label,_,_ in candidates)==2
    assert sum(label=="source_column_intensity" for label,_,_ in candidates)==6
    label,subset,metadata=candidates[-1]
    assert label=="labelled_max_product_assignment" and len(set(subset))==3
    q=context["probabilities"]
    optimum=min(sum(-math.log(max(float(q[row,column]),1e-300)) for column,row in enumerate(rows))
                for rows in itertools.permutations(range(6),3))
    assert metadata["assignment_negative_log_product"]==pytest.approx(optimum,abs=1e-12)
    assert metadata["optimizes_exact_D_support_probability"] is False


def test_zero_intensity_assignment_and_carried_tie_priority():
    context=p48.build_network(np.eye(6,3,dtype=complex),"fixture")
    label,subset,metadata=list(p48.preparation_candidates(context,[3,1,5,0,2,4],3))[-1]
    assert label=="labelled_max_product_assignment" and subset==[0,1,2]
    assert metadata["assignment_negative_log_product"]==0
    assert metadata["assignment_floor_entries"]==15
    blind=p48.build_network(p48.fourier_basis(6,3,[2,0,4,1,5,3]),"fixture")
    priority=[3,1,5,0,2,4]; permutation=np.asarray([3,0,5,1,4,2])
    relabeled_v=np.zeros_like(blind["v"]); relabeled_v[permutation]=blind["v"]
    relabeled=p48.build_network(relabeled_v,"fixture")
    before=list(p48.preparation_candidates(blind,priority,3))
    after=list(p48.preparation_candidates(relabeled,permutation[priority].tolist(),3))
    for (label,subset,_),(new_label,new_subset,_) in zip(before,after):
        assert label==new_label and sorted(permutation[subset].tolist())==new_subset
