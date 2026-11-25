"""P49 finite physics, objective isolation and cost-envelope fixtures."""
import cmath
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
SPEC=importlib.util.spec_from_file_location("p49_probe",ROOT/"research/P49_trained_source_probe.py")
p49=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(p49)


def permanent_explicit(matrix):
    return sum((np.prod([matrix[i,j] for i,j in enumerate(order)])
                for order in itertools.permutations(range(len(matrix)))),0j)


def fock_law(v):
    n,r=v.shape; output={}
    for slots in itertools.combinations_with_replacement(range(n),r):
        counts=tuple(slots.count(i) for i in range(n))
        amplitude=permanent_explicit(v[np.ix_(slots,range(r))])
        output[counts]=abs(amplitude)**2/math.prod(math.factorial(x) for x in counts)
    return output


@pytest.mark.parametrize("r",[1,2,3,13,17])
def test_source_rotation_is_unitary_with_exact_null_angle(r):
    rotation=p49.source_rotation(r,math.pi/4,.37)
    assert rotation.conj().T@rotation==pytest.approx(np.eye(r),abs=2e-12)
    assert p49.source_rotation(r,0.,.37)==pytest.approx(np.eye(r),abs=1e-15)


def test_even_times_odd_order_for_overlapping_layers():
    g=p49.two_mode(math.pi/4,.37)
    even=np.eye(3,dtype=complex); odd=np.eye(3,dtype=complex)
    even[:2,:2]=g; odd[1:,1:]=g
    actual=p49.source_rotation(3,math.pi/4,.37)
    assert actual==pytest.approx(even@odd,abs=1e-15)
    assert np.linalg.norm(actual-odd@even)>.1


@pytest.mark.parametrize("phi",[0.,.37,math.pi/2])
def test_HOM_complex_coherence_fixes_the_general_phase_convention(phi):
    g=p49.two_mode(math.pi/4,phi)
    amplitude20=permanent_explicit(g[[0,0],:])/math.sqrt(2)
    amplitude02=permanent_explicit(g[[1,1],:])/math.sqrt(2)
    amplitude11=permanent_explicit(g)
    assert amplitude20==pytest.approx(-cmath.exp(1j*phi)/math.sqrt(2),abs=1e-12)
    assert amplitude02==pytest.approx(cmath.exp(-1j*phi)/math.sqrt(2),abs=1e-12)
    assert amplitude11==pytest.approx(0j,abs=1e-12)
    assert amplitude20*amplitude02.conjugate()==pytest.approx(-cmath.exp(2j*phi)/2,abs=1e-12)


@pytest.mark.parametrize("phi",[0.,math.pi/2])
def test_mixing_preserves_projector_mu_but_can_change_q(phi):
    e=p49.p48.fourier_basis(6,3,[2,0,4,1,5,3]); v=e@p49.source_rotation(3,math.pi/4,phi)
    assert v.conj().T@v==pytest.approx(np.eye(3),abs=2e-12)
    assert v@v.conj().T==pytest.approx(e@e.conj().T,abs=2e-12)
    assert np.sum(abs(v)**2,axis=1)==pytest.approx(np.sum(abs(e)**2,axis=1),abs=2e-12)
    assert np.linalg.norm(abs(v)**2-abs(e)**2)>.01


def test_every_rotated_basis_needs_new_marginals_covariance_and_mask():
    e=np.eye(4,2,dtype=complex); v=e@p49.source_rotation(2,math.pi/4,0.)
    before=p49.p48.build_network(e,"fixture"); after=p49.p48.build_network(v,"fixture")
    table0,_,_,_=p49.p48.all_marginals(before,[0,1]); table1,_,_,_=p49.p48.all_marginals(after,[0,1])
    assert before["Gaussian_structurally_occupied_deterministic_rows"]==[0,1]
    assert after["Gaussian_structurally_occupied_deterministic_rows"]==[]
    assert before["variance"][0]==0 and after["variance"][0]==pytest.approx(1.)
    for model in ("bosonic","distinguishable","species4","continuous_phase"):
        assert not np.allclose(table0[model],table1[model],atol=1e-12)
    assert table0["spherical_coherent"]==pytest.approx(table1["spherical_coherent"],abs=2e-12)


def test_pre_mixing_source_gauge_is_relevant_post_mixing_column_gauge_is_null():
    e=np.zeros((4,2),dtype=complex);e[:2]=np.asarray([[1,1],[1,-1]])/math.sqrt(2)
    rotation=p49.source_rotation(2,math.pi/4,0.); gauge=np.diag([1,1j])
    v=e@rotation; before_mix=e@gauge@rotation; after_mix=v@gauge
    first=fock_law(v); altered=fock_law(before_mix); null=fock_law(after_mix)
    assert first[(1,1,0,0)]==pytest.approx(1.)
    assert altered[(1,1,0,0)]==pytest.approx(0.,abs=1e-25)
    assert list(first.values())==pytest.approx(list(null.values()),abs=2e-12)


def training_fixture(cases,cut_rule):
    rows=[]
    for model in p49.MODELS:
        for policy in p49.policies(model):
            for case in cases:
                cuts=cut_rule(model,policy,case)
                rows.append({"stage":"training","case":case["id"],"model":model,"policy":policy["id"],
                    "proposals":policy["training_draws"],"sum_cuts":sum(cuts),"cuts":cuts,
                    "weight_denominator":case["weight_denominator"]})
    return rows


def test_mean_selection_includes_worse_shots_not_best_or_success_only():
    cases=[{"id":str(i),"weight_denominator":100} for i in range(4)]
    def rule(model,policy,case):
        draws=policy["training_draws"]
        return ([0]+[10]*(draws-1)) if policy["id"]==0 else ([7]*draws if policy["id"]==1 else [20]*draws)
    selected,losses=p49.select_policies(training_fixture(cases,rule),cases)
    assert set(selected.values())=={1}
    assert all(Fraction(values["1"]["exact_fraction"])==Fraction(7,100) for values in losses.values())


def test_graphs_are_equal_weighted_with_exact_fraction_ties():
    cases=[{"id":str(i),"weight_denominator":(1 if i%2==0 else 100)} for i in range(4)]
    def rule(model,policy,case):
        small=case["weight_denominator"]==1
        cut=(0 if small else 10) if policy["id"]==0 else ((1 if small else 0) if policy["id"]==1 else case["weight_denominator"])
        return [cut]*policy["training_draws"]
    selected,losses=p49.select_policies(training_fixture(cases,rule),cases)
    assert set(selected.values())=={0}
    assert all(Fraction(values["0"]["exact_fraction"])==Fraction(1,20) for values in losses.values())
    ties=training_fixture(cases,lambda model,policy,case:[0]*policy["training_draws"])
    assert set(p49.select_policies(ties,cases)[0].values())=={0}
    assert p49.total_weight(np.zeros((4,4),dtype=np.int64))==1


@pytest.mark.parametrize("mode",["evaluation_leak","missing_graph"])
def test_selection_rejects_evaluation_leak_or_successful_subpopulation(mode):
    cases=[{"id":str(i),"weight_denominator":100} for i in range(4)]
    rows=training_fixture(cases,lambda model,policy,case:[5]*policy["training_draws"])
    if mode=="evaluation_leak":
        rows[-1]=dict(rows[-1],stage="evaluation")
    else:
        rows.pop()
    with pytest.raises(ValueError):
        p49.select_policies(rows,cases)


def test_nonredundant_grids_have_equal_training_effort_and_contiguous_b4_ports(monkeypatch):
    for model in p49.MODELS:
        assert sum(policy["training_draws"] for policy in p49.policies(model))==32
    assert len(p49.policies("spherical_coherent"))==4
    assert {policy["basis"] for policy in p49.policies("spherical_coherent")}=={0,1}
    assert len(p49.policies("iid_uniform"))==2
    assert {policy["basis"] for policy in p49.policies("iid_uniform")}=={None}
    seen={}
    def sampler(u,source,model,seed):
        seen.update(source=source,model=model)
        return lambda:(np.asarray([1,1,1,0,0,0]),False),0.
    monkeypatch.setattr(p49.base,"make_optical_sampler",sampler)
    context={"v":np.eye(6,3),"u":np.eye(6),"tables":{}}
    p49.observation_components(context,"species4",490080)
    assert seen=={"source":[0,1,2],"model":"species4"}


def test_fixed_policy_evaluation_has_two_fresh_namespaces_without_reselection(monkeypatch):
    calls=[];policy=p49.policies("bosonic")[5]
    def batch(a,contexts,common,model,chosen,stage,trial,draws,stream):
        calls.append((chosen,stage,trial,draws));return {"trial":trial}
    monkeypatch.setattr(p49,"run_batch",batch)
    p49.evaluate_fixed_policy(None,None,None,"bosonic",policy,None)
    assert calls==[(policy,"evaluation",0,16),(policy,"evaluation",1,16)]
    seeds=[p49.base.seed_for(namespace,"fixture","bosonic",5,trial)
           for namespace,trial in [(491100,0),(491200,0),(491200,1)]]
    assert len(set(seeds))==3


def test_backend_counts_JSON_excluded_but_classical_setup_is_charged(monkeypatch):
    class FakeTime:
        now=0.
        def perf_counter(self):return self.now
        def process_time(self):return self.now
        def advance(self,value):self.now+=value
    clock=FakeTime();monkeypatch.setattr(p49,"time",clock)
    def components(context,model,seed):
        clock.advance(7)
        def sample():clock.advance(5);return np.asarray([1,1,0,0]),{}
        def post(observation):clock.advance(2);return np.zeros(4),observation[0],{}
        return sample,post,{"backend_setup_wall_seconds":5.,"backend_setup_cpu_seconds":5.}
    def complete(a,field,k,lam,priority,q):
        clock.advance(3)
        return {"cut":2,"subset":[0,1],"seed_vertices":[0],"completion":[],
                "marginal_evaluations":3,"feasible_scores":1,"score_units":4}
    class Writer(io.StringIO):
        def write(self,value):clock.advance(100);return super().write(value)
    monkeypatch.setattr(p49,"observation_components",components)
    monkeypatch.setattr(p49.adaptive,"complete",complete)
    common={"case_id":"fixture","Cref":4,"reference_subset":[0,2],"weight_denominator":4,"vertex_priority":[0,1,2,3]}
    row=p49.run_batch(np.zeros((4,4),dtype=np.int64),[{}],common,"bosonic",p49.policies("bosonic")[0],"training",0,2,Writer())
    assert row["observation_setup_wall_seconds"]==7
    assert row["backend_setup_wall_seconds"]==5
    assert row["classical_postprocessing_setup_wall_seconds"]==2
    assert row["classical_postprocessing_setup_cpu_seconds"]==2
    assert row["observation_generation_wall_seconds"]==10
    assert row["classical_postprocessing_wall_seconds"]==10
    assert common["Cref"]==4 and clock.now==227


def test_training_incumbents_remain_paid_and_model_specific():
    common={"fixture":{"Cref":4,"reference_subset":[0,2]}}
    rows=[{"model":"bosonic","case":"fixture","stage":"training","best_cut":1,"best_subset":[0,1]},
          {"model":"bosonic","case":"fixture","stage":"evaluation","best_cut":2,"best_subset":[0,3]},
          {"model":"distinguishable","case":"fixture","stage":"training","best_cut":3,"best_subset":[1,2]}]
    result=p49.arm_incumbents(rows,common)
    assert result["bosonic"]["fixture"]["paid_total_deployment_best_cut"]==1
    assert result["bosonic"]["fixture"]["fresh_evaluation_only_best_cut"]==2
    assert result["distinguishable"]["fixture"]["paid_total_deployment_best_cut"]==3
    assert common["fixture"]["Cref"]==4


@pytest.mark.parametrize("early_cap",[False,True])
def test_FAST_uses_rank_vector_zero_optical_grant_and_admissible_prefix(monkeypatch,early_cap):
    captured={}
    def solver(a,incumbent,**kwargs):
        captured.update(kwargs)
        return {"best_cut":2,"best_subset":np.asarray([0,2]),"overall_completed_best_cut":0,
                "overall_completed_best_subset":np.asarray([0,1]),
                "early_cap_inconclusive":early_cap,"early_wall_inconclusive":False}
    monkeypatch.setattr(p49.fast,"solve_balanced",solver)
    a=np.asarray([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],dtype=np.int64)
    common={"case_id":"fixture","reference_subset":[0,2],"Cref":2,
            "classical_compute_wall_seconds":.01,"vertex_priority_by_vertex":[1,3,0,2]}
    records=[{"classical_postprocessing_wall_seconds":.03,"classical_postprocessing_setup_wall_seconds":.004,
              "observation_setup_wall_seconds":100.,
              "observation_generation_wall_seconds":1000.}]
    result=p49.fast_comparison(a,common,records,.001,{"fast_max_proposals":100000000})
    assert captured["vertex_priority"]==[1,3,0,2]
    assert captured["cpu_budget_seconds"]<=.045 and captured["wall_budget_seconds"] is None
    assert result["total_CPU_allowance_including_adapter"]==pytest.approx(.045)
    assert result["training_and_eval_classical_setup_wall_grant"]==.004
    assert result["eligible_best_cut"]==2
    assert result["comparison_acceptance_eligible"] is (not early_cap)
    assert result["optical_simulation_setup_or_count_seconds_granted"]==0
    assert result["audit_JSON_seconds_granted"]==0


def test_local_count_observation_and_separate_PIT_interface():
    v=p49.p48.fourier_basis(4,2,[2,0,3,1]);context=p49.p48.build_network(v,"fixture")
    tables,_,_,_=p49.p48.all_marginals(context,[0,1]);context["tables"]=tables
    sample,post,setup=p49.observation_components(context,"bosonic",490081)
    observation=sample();field,counts,metadata=post(observation)
    assert counts.sum()==2 and len(counts)==4 and all(-.5<=x<=.5 for x in field)
    assert len(metadata["pit_jitter"])==4
    assert setup["backend_setup_wall_seconds"]>=0 and setup["backend_setup_cpu_seconds"]>=0


def test_gauge_fixed_spectral_mixing_is_covariant_with_carried_relabeling():
    a=np.asarray([[0,3,0,2,4,0],[3,0,1,0,3,2],[0,1,0,2,1,4],
                  [2,0,2,0,4,1],[4,3,1,4,0,2],[0,2,4,1,2,0]],dtype=np.int64)
    marks=np.asarray([.1,.7,.3,.5,.9,.2]);priority=[2,0,4,1,5,3]
    original=p49.p48.spectral_data(a,marks,priority,3)
    permutation=np.asarray([3,0,5,1,4,2]);carried=np.zeros_like(a)
    carried[np.ix_(permutation,permutation)]=a
    shifted_marks=np.zeros_like(marks);shifted_marks[permutation]=marks
    shifted=p49.p48.spectral_data(carried,shifted_marks,permutation[priority].tolist(),3)
    rotation=p49.source_rotation(3,math.pi/4,.37)
    v=original["v"]@rotation;other=shifted["v"]@rotation
    assert other[permutation]==pytest.approx(v,abs=3e-11)
    assert list(fock_law(other[permutation]).values())==pytest.approx(list(fock_law(v).values()),abs=3e-11)


def test_charged_anchor_keeps_the_immutable_P43_rule():
    a=np.asarray([[0,3,0,2,4,0],[3,0,1,0,3,2],[0,1,0,2,1,4],
                  [2,0,2,0,4,1],[4,3,1,4,0,2],[0,2,4,1,2,0]],dtype=np.int64)
    first,legacy=p49.base.prepare_anchor(a,490082,8,io.StringIO(),"fixture")
    second,charged=p49.charged_anchor(a,490082,8,p49.ComputeMeter(),io.StringIO(),"fixture")
    assert first==second
    for key in ("initial_cut","final_cut","candidate_scores_including_initial",
                "one_swap_local_minimum_certified","stopping_reason","trace"):
        assert legacy[key]==charged[key]


def test_preparation_recomputes_all_four_contexts_with_contiguous_groups(monkeypatch,tmp_path):
    a=np.asarray([[0,3,0,2,4,0],[3,0,1,0,3,2],[0,1,0,2,1,4],
                  [2,0,2,0,4,1],[4,3,1,4,0,2],[0,2,4,1,2,0]],dtype=np.int64)
    monkeypatch.setattr(p49.base,"make_graph",lambda case:a.copy())
    actual=p49.p48.all_marginals;calls=[]
    def marginal(context,ports):
        calls.append((context["encoder"],list(ports)))
        return actual(context,ports)
    monkeypatch.setattr(p49.p48,"all_marginals",marginal)
    case={"id":"fixture","m":6,"k":3,"r":3}
    spec={"anchor_max_scans":8,"gap_tolerance":1e-12,"residual_tolerance":3e-12}
    graph,contexts,common,_=p49.prepare(case,spec,io.StringIO(),tmp_path)
    assert graph.dtype==np.dtype("int64") and common["numerical_status"]=="PASS"
    assert calls==[(name,[0,1,2]) for name in p49.BASES]
    assert len(contexts)==4 and common["vertex_priority_by_vertex"]==np.argsort(common["vertex_priority"]).tolist()
    for context in contexts[1:]:
        assert context["projector_difference_to_E"]<3e-12
        assert context["mu_difference_to_E"]<3e-12
    assert common["classical_compute_wall_seconds"]<=common["total_frontend_wall_before_context_serialization"]
    saved=json.loads((tmp_path/"context_fixture.json").read_text())
    assert len(saved["networks"])==4 and saved["optical_source_uses_frontend_partition"] is False
