"""Finite P50 hand cases and policy/resource isolation; no DEV graph opened."""
import cmath
from fractions import Fraction
import importlib.util
import io
import itertools
import math
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))
SPEC = importlib.util.spec_from_file_location("p50_probe", ROOT / "research/P50_minimal_count_field_probe.py")
p50 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p50)


def permanent(matrix):
    return sum((np.prod([matrix[i, j] for i, j in enumerate(order)])
                for order in itertools.permutations(range(len(matrix)))), 0j)


def fock_law(v):
    n, r = v.shape
    result = {}
    for slots in itertools.combinations_with_replacement(range(n), r):
        counts = tuple(slots.count(i) for i in range(n))
        amplitude = permanent(v[np.ix_(slots, range(r))])
        result[counts] = abs(amplitude)**2 / math.prod(math.factorial(x) for x in counts)
    return result


def graph(n=8):
    a = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        a[i, (i+1) % n] = a[(i+1) % n, i] = 1 + i % 3
    a[0, 3] = a[3, 0] = 2
    return a


def case(n=8, r=3):
    return {"id": "fixture", "m": n, "k": n//2, "r": r, "family": "ER", "seed": 500008}


@pytest.mark.parametrize("bad", ["float", "odd", "asymmetric", "negative", "loops", "overflow"])
def test_raw_graph_validation_has_no_silent_rounding_or_unsafe_arithmetic(bad):
    a = graph()
    if bad == "float": a = a.astype(float)
    elif bad == "odd": a = a[:7, :7]
    elif bad == "asymmetric": a[0, 1] += 1
    elif bad == "negative": a[0, 1] = a[1, 0] = -1
    elif bad == "loops": a[0, 0] = 1
    else: a[0, 1] = a[1, 0] = np.iinfo(np.int64).max
    with pytest.raises(ValueError):
        p50.validated_graph(a)


@pytest.mark.parametrize("family", ["ER", "RR"])
def test_new_generator_convention_on_small_non_DEV_seeds(family):
    fixture = {"m": 10, "family": family, "seed": 500011}
    a, b = p50.make_graph(fixture), p50.make_graph(fixture)
    assert a.dtype == np.int64 and np.array_equal(a, b)
    assert np.array_equal(a, a.T) and np.diag(a).sum() == 0
    assert np.all((a[a > 0] >= 1) & (a[a > 0] <= 5))
    if family == "RR":
        assert np.count_nonzero(a, axis=1).tolist() == [8]*10


def test_grids_preserve_equal_effort_with_declared_nonredundant_controls():
    assert len(p50.MODELS) == 10
    for model in p50.MODELS:
        assert sum(p["training_draws"] for p in p50.policies(model)) == 32
    assert len(p50.policies("bosonic")) == 16
    assert len(p50.policies("independent_B_marginals")) == 16
    for model in ("spherical_coherent", "static_preparation"):
        assert len(p50.policies(model)) == 8
        assert {p["basis"] for p in p50.policies(model)} == {0, 1}
    assert len(p50.policies("pure_jitter")) == 2
    assert {p["alpha"] for p in p50.policies("pure_jitter")} == {None}


@pytest.mark.parametrize("alpha", [0, 1])
def test_diffusion_is_nonnegative_doubly_stochastic_and_zero_graph_is_identity(alpha):
    h = p50.diffusion(graph(), alpha)
    assert h == pytest.approx(h.T, abs=1e-14)
    assert h.min() >= -1e-14
    assert h.sum(axis=0) == pytest.approx(np.ones(8), abs=1e-14)
    assert h.sum(axis=1) == pytest.approx(np.ones(8), abs=1e-14)
    assert p50.diffusion(np.zeros((8, 8), dtype=np.int64), alpha) == pytest.approx(np.eye(8))


@pytest.mark.parametrize("delta,expected", [(-1e-18, -1), (1e-18, 0)])
def test_anchored_half_up_bucket_boundary_has_a_fixed_definition(delta, expected):
    field = np.asarray([0., -.5e-12 + delta, -2e-12, -3e-12])
    _, bucket = p50.rank_balanced(field, [0, 1, 2, 3], 2)
    assert bucket[0] == 0 and bucket[1] == expected


def test_bucket_translation_invariance_and_nearly_constant_fields_are_ties():
    field = np.asarray([.25, .125, 0., -.125])
    first = p50.rank_balanced(field, [3, 2, 1, 0], 2)
    shifted = p50.rank_balanced(field+8., [3, 2, 1, 0], 2)
    assert np.array_equal(first[0], shifted[0]) and np.array_equal(first[1], shifted[1])
    subset, bucket = p50.rank_balanced([0., 1e-16, -1e-16, 2e-16], [3, 0, 2, 1], 2)
    assert bucket.tolist() == [0, 0, 0, 0] and subset.tolist() == [1, 3]


@pytest.mark.parametrize("beta", [0., .1])
@pytest.mark.parametrize("alpha", [0, 1])
def test_uniform_mu_static_and_pure_jitter_are_duplicate_laws_with_shared_jitter(alpha, beta):
    h = p50.diffusion(graph(), alpha)
    mu = np.full(8, 3/8)
    jitter = np.asarray([-.93, .72, -.21, .43, .61, -.54, .31, -.82])
    priority = np.asarray([4, 1, 6, 0, 7, 3, 5, 2])
    static = p50.rank_balanced(-h@mu+beta*jitter, priority, 4)[0]
    pure = p50.rank_balanced(beta*jitter, priority, 4)[0]
    assert np.array_equal(static, pure)


def test_carried_graph_counts_mu_priority_relabel_away_from_bucket_boundaries():
    a = graph()
    counts = np.asarray([0, 2, 0, 0, 1, 0, 0, 0])
    mu = np.asarray([.1, .4, .2, .6, .3, .4, .5, .5])
    jitter = np.asarray([-.93, .72, -.21, .43, .61, -.54, .31, -.82])
    priority = np.asarray([4, 1, 6, 0, 7, 3, 5, 2])
    perm = np.asarray([2, 5, 0, 6, 1, 7, 3, 4])
    field = p50.diffusion(a, 1)@(counts-mu)+.1*jitter
    other = p50.diffusion(a[np.ix_(perm, perm)], 1)@(counts[perm]-mu[perm])+.1*jitter[perm]
    chosen = p50.rank_balanced(field, priority, 4)[0]
    mapped = perm[p50.rank_balanced(other, priority[perm], 4)[0]]
    assert other == pytest.approx(field[perm], abs=2e-15)
    assert sorted(mapped) == chosen.tolist()


def test_positive_but_subbucket_support_gap_is_not_a_retention_guarantee():
    chosen, bucket = p50.rank_balanced([4e-13, 0., 0., 0.], [3, 0, 1, 2], 2)
    assert bucket.tolist() == [0, 0, 0, 0] and 0 not in chosen
    counts = np.asarray([0, 2, 0, 0, 1, 0, 0, 0])
    mu = np.full(8, 3/8)
    jitter = np.asarray([-.93, .72, -.21, .43, .61, -.54, .31, -.82])
    retained = p50.rank_balanced(counts-mu+.1*jitter, np.arange(8), 4)[0]
    assert set(np.flatnonzero(counts)) <= set(retained)


def test_complete_bipartite_diffusion_can_give_the_MAXIMAL_cut():
    a = np.zeros((6, 6), dtype=np.int64)
    a[:3, 3:] = 1; a[3:, :3] = 1
    counts = np.asarray([1, 0, 0, 0, 0, 0])
    field = p50.diffusion(a, 1)@(counts-np.full(6, 1/6))
    chosen = p50.rank_balanced(field, np.arange(6), 3)[0]
    assert chosen.tolist() == [3, 4, 5]
    assert p50.base.cut(a, chosen) == 9


def test_one_photon_B_D_phase_sphere_count_laws_are_one_categorical_law():
    v = np.asarray([1, 1j, -1, -1j, 2, -2j], dtype=complex)[:, None]/math.sqrt(12)
    law = fock_law(v)
    for counts, probability in law.items():
        vertex = counts.index(1)
        expected = abs(v[vertex, 0])**2
        assert probability == pytest.approx(expected, abs=1e-14)
        for phase in (0., .37, 2.8):
            assert abs((v*np.exp(1j*phase))[vertex, 0])**2 == pytest.approx(expected)
    # independent_B_marginals deliberately is NOT this r=1 law.


def test_monomial_B_and_D_are_deterministic_but_phase_and_sphere_are_not():
    v = np.eye(6, 2, dtype=complex)
    law = fock_law(v)
    assert law[(1, 1, 0, 0, 0, 0)] == pytest.approx(1.)
    assert sum(value for counts, value in law.items() if counts != (1, 1, 0, 0, 0, 0)) == pytest.approx(0.)
    q = abs(v)**2
    assert all(np.count_nonzero(q[:, j]) == 1 and q[j, j] == 1 for j in range(2))
    phase_probabilities = abs(v @ (np.ones(2)/math.sqrt(2)))**2
    assert phase_probabilities[0]**2 == pytest.approx(.25)  # P(n0=2), not deterministic
    spherical = p50.p48.coherent.spherical_marginal(1., 2)
    assert float(spherical["pmf"][2]) == pytest.approx(1/3)


def test_full_V_column_phases_and_conjugation_preserve_law_not_seedwise_samples():
    v = p50.p48.fourier_basis(6, 3, [2, 0, 4, 1, 5, 3])
    v = v @ p50.prior.source_rotation(3, math.pi/4, .37)
    law = fock_law(v)
    phases = np.diag(np.exp(1j*np.asarray([.31, -.42, 1.27])))
    after = fock_law(v@phases)
    conjugate = fock_law(v.conj())
    assert sum(law.values()) == pytest.approx(1., abs=2e-12)
    assert list(law.values()) == pytest.approx(list(after.values()), abs=2e-12)
    assert list(law.values()) == pytest.approx(list(conjugate.values()), abs=2e-12)


@pytest.mark.parametrize("r", [3, 13, 17])
def test_source_rotation_order_and_orthogonality(r):
    rotation = p50.prior.source_rotation(r, math.pi/4, .37)
    assert rotation.conj().T@rotation == pytest.approx(np.eye(r), abs=2e-12)
    if r == 3:
        g = p50.prior.two_mode(math.pi/4, .37)
        even, odd = np.eye(3, dtype=complex), np.eye(3, dtype=complex)
        even[:2, :2] = g; odd[1:, 1:] = g
        assert rotation == pytest.approx(even@odd, abs=1e-15)
        assert np.linalg.norm(rotation-odd@even) > .1


@pytest.mark.parametrize("phi", [0., .37, math.pi/2])
def test_HOM_amplitudes_and_complex_coherence_fix_the_phase_convention(phi):
    g = p50.prior.two_mode(math.pi/4, phi)
    a20 = permanent(g[[0, 0], :])/math.sqrt(2)
    a02 = permanent(g[[1, 1], :])/math.sqrt(2)
    assert a20 == pytest.approx(-cmath.exp(1j*phi)/math.sqrt(2), abs=2e-12)
    assert a02 == pytest.approx(cmath.exp(-1j*phi)/math.sqrt(2), abs=2e-12)
    assert permanent(g) == pytest.approx(0j, abs=2e-12)
    assert a20*a02.conjugate() == pytest.approx(-cmath.exp(2j*phi)/2, abs=2e-12)


def test_source_gauge_before_R_matters_but_after_R_column_phases_do_not():
    e = np.zeros((6, 2), dtype=complex)
    e[:2] = np.asarray([[1, 1], [1, -1]])/math.sqrt(2)
    rotation = p50.prior.source_rotation(2, math.pi/4, 0.)
    gauge = np.diag([1, 1j])
    first = fock_law(e@rotation)
    altered = fock_law(e@gauge@rotation)
    null = fock_law(e@rotation@gauge)
    assert first[(1, 1, 0, 0, 0, 0)] == pytest.approx(1.)
    assert altered[(1, 1, 0, 0, 0, 0)] == pytest.approx(0., abs=1e-25)
    assert list(first.values()) == pytest.approx(list(null.values()), abs=2e-12)


def test_B_covariance_matches_independent_exact_three_photon_Fock_enumeration():
    v = p50.p48.fourier_basis(6, 3, [2, 0, 4, 1, 5, 3])
    v = v@p50.prior.source_rotation(3, math.pi/4, .37)
    law = fock_law(v)
    mean = sum((prob*np.asarray(counts) for counts, prob in law.items()), np.zeros(6))
    second = sum((prob*np.outer(counts, counts) for counts, prob in law.items()), np.zeros((6, 6)))
    data = p50.gaussian_factor(v)
    assert mean == pytest.approx(np.sum(abs(v)**2, axis=1), abs=2e-12)
    assert data["covariance"] == pytest.approx(second-np.outer(mean, mean), abs=3e-12)
    assert data["factor"]@data["factor"].T == pytest.approx(data["covariance"], abs=3e-12)


def test_structurally_deterministic_rows_are_masked_BEFORE_diffusion_and_can_then_fluctuate():
    v = np.zeros((8, 3), dtype=complex)
    v[0, 0] = 1
    v[1:3, 1] = 1/math.sqrt(2)
    v[3:5, 2] = 1/math.sqrt(2)
    data = p50.gaussian_factor(v)
    assert data["structural_mask"].tolist() == [True, False, False, False, False, True, True, True]
    assert np.all(data["factor"][data["structural_mask"]] == 0)
    h = p50.diffusion(graph(), 1)
    actual = p50.final_independent_variance(h, data["factor"])
    assert data["covariance"][0, 0] == 0 and actual[0] > 0
    assert actual == pytest.approx(np.diag(h@data["factor"]@data["factor"].T@h.T), abs=1e-14)


def test_final_independent_variance_uses_actual_repaired_factor_not_a_target_diagonal():
    h = np.asarray([[.5, .5], [.25, .75]])
    factor = np.asarray([[1., 0.], [.2, .8]])
    factor[1, 0] += 1e-4  # explicit actual-factor perturbation, not a covariance oracle
    actual = p50.final_independent_variance(h, factor)
    assert actual == pytest.approx([sum(x*x for x in row) for row in h@factor], abs=1e-15)
    target_diagonal_only = h@np.diag([1., .68])@h.T
    assert abs(actual[0]-target_diagonal_only[0, 0]) > .09


def test_significant_negative_covariance_eigenvalue_is_not_silently_clipped(monkeypatch):
    monkeypatch.setattr(p50.np.linalg, "eigh", lambda a:(np.asarray([-1e-3, 1.]), np.eye(2)))
    with pytest.raises(p50.p48.NumericalInconclusive):
        p50.gaussian_factor(np.eye(2, 1, dtype=complex))


@pytest.mark.parametrize("row,expected", [
    ([Fraction(1, 4), Fraction(1, 4)], [Fraction(5, 8), Fraction(1, 4), Fraction(1, 8)]),
    ([Fraction(1, 2), Fraction(1, 2)], [Fraction(1, 2), Fraction(0), Fraction(1, 2)]),
    ([Fraction(1), Fraction(0)], [Fraction(0), Fraction(1), Fraction(0)]),
    ([Fraction(0), Fraction(0)], [Fraction(1), Fraction(0), Fraction(0)])])
def test_independent_B_uses_expanded_PGF_probabilities_not_shift_coefficients(row, expected):
    pmf, receipt = p50.p48.factorial_marginal(tuple(row), True)
    assert pmf == pytest.approx([float(value) for value in expected], abs=1e-14)
    assert abs(float(receipt["raw_pmf_sum"])-1.) < 1e-14


def test_row_repair_keeps_subunit_mass_and_saves_roundoff_excess():
    repaired, receipt = p50.p48.repair_probability_row([.2, .3])
    assert float(sum(repaired)) == pytest.approx(.5)
    assert receipt["subunit_row_rescaled_to1"] is False
    repaired, receipt = p50.p48.repair_probability_row([.5, .5+1e-14])
    assert sum(repaired) == 1 and Fraction(receipt["input_roundoff_repair_L1"]) > 0
    with pytest.raises(p50.p48.NumericalInconclusive):
        p50.p48.repair_probability_row([.6, .6])


def test_independent_B_count_total_is_NOT_conditioned_to_r():
    arm = {"a":np.zeros((6, 6),dtype=np.int64), "r":1, "k":3, "priority":np.arange(6),
           "H":{0:np.eye(6)}, "contexts":{0:{"mu":np.asarray([.5,.5,0,0,0,0]),
           "independent_cdf":np.asarray([[.5,1],[.5,1],[1,1],[1,1],[1,1],[1,1]])}}}
    sample, process, _, _ = p50.observation_components(arm,"independent_B_marginals",
                                                     p50.policies("independent_B_marginals")[0],500201)
    result = process({"counts":np.zeros(6,dtype=np.int64)})
    assert len(result[3]) == 3  # an all-zero independent draw is valid here
    totals = [int(sample()["counts"].sum()) for _ in range(32)]
    assert set(totals) <= {0,1,2} and any(value != 1 for value in totals)


def test_B_preparation_calls_no_other_model_calibration_and_diagnostics_are_separate(monkeypatch):
    def forbidden(*args, **kwargs): raise AssertionError("Other-model work entered B")
    monkeypatch.setattr(p50, "gaussian_factor", forbidden)
    monkeypatch.setattr(p50.p48, "factorial_marginal", forbidden)
    monkeypatch.setattr(p50.p48, "all_marginals", forbidden)
    arm = p50.prepare_arm(graph(), case(), "bosonic")
    assert arm["other_arm_contexts_used"] is False
    assert arm["diagnostics_enter_B_allowance"] is False
    assert arm["diagnostics"]["status"] == "PASS"
    assert set(arm["contexts"]) == {0,1,2,3}
    for context in arm["contexts"].values():
        assert "factor" not in context and "independent_pmf" not in context
        assert context["u"][:, :3] == pytest.approx(context["v"], abs=1e-15)


def test_arm_local_preparation_caches_are_not_shared_and_source_is_not_a_partition():
    a = graph()
    b = p50.prepare_arm(a,case(),"bosonic")
    d = p50.prepare_arm(a,case(),"distinguishable")
    assert not np.shares_memory(b["a"],d["a"])
    assert not np.shares_memory(b["contexts"][1]["v"],d["contexts"][1]["v"])
    assert b["contexts"][1]["v"] == pytest.approx(d["contexts"][1]["v"], abs=1e-14)
    assert b["r"] == 3 and b["k"] == 4
    assert "Cref" not in b and "source_subset" not in b


def training_rows(cases, rule):
    rows=[]
    for model in p50.MODELS:
        for policy in p50.policies(model):
            for c in cases:
                cuts=rule(model,policy,c)
                rows.append({"stage":"training","model":model,"policy":policy["id"],"case":c["id"],
                             "proposals":policy["training_draws"],"cuts":cuts,"sum_cuts":sum(cuts),
                             "weight_denominator":c["weight_denominator"]})
    return rows


def test_ALL_shot_loss_rejects_a_lucky_minimum_and_equal_weights_each_graph():
    cases=[{"id":str(i),"weight_denominator":100} for i in range(4)]
    def rule(model,p,c):
        n=p["training_draws"]
        return ([0]+[20]*(n-1)) if p["id"]==0 else ([9]*n if p["id"]==1 else [30]*n)
    selected,losses=p50.select_policies(training_rows(cases,rule),cases)
    assert set(selected.values()) == {1}
    assert all(value[1]==Fraction(9,100) for value in losses.values())
    cases=[{"id":str(i),"weight_denominator":(1 if i%2==0 else 100)} for i in range(4)]
    def weighted(model,p,c):
        value=(0 if c["weight_denominator"]==1 else 10) if p["id"]==0 else (
            (1 if c["weight_denominator"]==1 else 0) if p["id"]==1 else c["weight_denominator"])
        return [value]*p["training_draws"]
    selected,losses=p50.select_policies(training_rows(cases,weighted),cases)
    assert set(selected.values()) == {0}
    assert all(value[0]==Fraction(1,20) for value in losses.values())
    tied=training_rows(cases,lambda model,p,c:[0]*p["training_draws"])
    assert set(p50.select_policies(tied,cases)[0].values()) == {0}


@pytest.mark.parametrize("mode", ["evaluation_leak", "missing_graph", "lost_worse_cut"])
def test_selection_refuses_eval_leak_missing_graph_or_hidden_bad_shot(mode):
    cases=[{"id":str(i),"weight_denominator":100} for i in range(4)]
    rows=training_rows(cases,lambda model,p,c:[5]*p["training_draws"])
    if mode=="evaluation_leak": rows[-1]["stage"]="evaluation"
    elif mode=="missing_graph": rows.pop()
    else: rows[-1]["sum_cuts"]-=1
    with pytest.raises(ValueError): p50.select_policies(rows,cases)


def test_fresh_evaluation_has_two_new_roles_and_cannot_reselect(monkeypatch):
    captured=[]
    def batch(arm,model,p,stage,trial,draws,stream):
        captured.append((p,stage,trial,draws)); return {"trial":trial}
    monkeypatch.setattr(p50,"run_batch",batch)
    policy=p50.policies("bosonic")[9]
    p50.evaluate_fixed(None,"bosonic",policy,None)
    assert captured==[(policy,"evaluation",0,16),(policy,"evaluation",1,16)]
    seeds=[p50.base.seed_for(root,"fixture","bosonic",9,trial)
           for root,trial in [(5020001,0),(5030001,0),(5030001,1)]]
    assert len(set(seeds))==3


def test_b4_local_backend_receives_contiguous_source_ports(monkeypatch):
    captured={}
    def sampler(u,source,model,seed):
        captured.update(source=source,model=model)
        return lambda:(np.asarray([1,1,1,0,0,0,0,0]),False),0.
    monkeypatch.setattr(p50.base,"make_optical_sampler",sampler)
    arm={"a":graph(),"r":3,"k":4,"contexts":{0:{"u":np.eye(8),"mu":np.asarray([1,1,1,0,0,0,0,0])}},
         "H":{0:np.eye(8)},"priority":np.arange(8)}
    sample,process,_,_=p50.observation_components(arm,"species4",p50.policies("species4")[0],500081)
    processed=process(sample())
    assert captured=={"source":[0,1,2],"model":"species4"}
    assert len(processed[3])==4


def test_B_clock_charges_constructor_classical_work_but_excludes_backend_counts_and_JSON(monkeypatch):
    class Clock:
        now=0.
        def perf_counter(self): return self.now
        def process_time(self): return self.now
        def advance(self,x): self.now+=x
    clock=Clock(); monkeypatch.setattr(p50,"time",clock)
    def components(arm,model,policy,seed):
        clock.advance(7.)
        def sample():
            clock.advance(5.)
            return {"counts":np.asarray([1,1,0,0])}
        def process(observation):
            clock.advance(2.)
            return np.zeros(4),np.zeros(4),np.zeros(4),np.asarray([0,1]),np.zeros(4,dtype=int),2
        return sample,process,{"wall_seconds":5.,"cpu_seconds":5.},{"jitter":1,"observation":2}
    class Writer(io.StringIO):
        def write(self,value): clock.advance(100.); return super().write(value)
    monkeypatch.setattr(p50,"observation_components",components)
    arm={"case":"fixture","weight_denominator":4,"a":np.zeros((4,4),dtype=np.int64),"r":2}
    row=p50.run_batch(arm,"bosonic",p50.policies("bosonic")[0],"training",0,2,Writer())
    assert row["observation_setup_wall_seconds"]==7.
    assert row["backend_setup_wall_seconds"]==5.
    assert row["classical_setup_wall_seconds"]==2.
    assert row["classical_setup_cpu_seconds"]==2.
    assert row["observation_generation_wall_seconds"]==10.
    assert row["classical_postprocessing_wall_seconds"]==4.
    assert row["classical_generation_wall_seconds"]==0.
    assert row["classical_aggregation_wall_seconds"]==0.
    assert clock.now==221.


@pytest.mark.parametrize("safe", [True,False])
def test_FAST_gets_only_B_own_allowance_raw_A_no_free_features_and_eligible_result(monkeypatch,safe):
    captured={}
    def solve(raw,**kwargs):
        captured.update(kwargs); captured["raw"]=raw
        return {"best_cut":2 if safe else None,"best_subset":np.asarray([0,2]) if safe else None,
                "has_eligible_result":safe,"comparison_acceptance_eligible":safe,
                "early_cap_inconclusive":False,"early_wall_inconclusive":False,
                "overall_completed_best_cut":0,"overall_completed_best_subset":np.asarray([0,1])}
    monkeypatch.setattr(p50.fast,"solve_from_raw",solve)
    raw=np.zeros((4,4),dtype=np.int64)
    arm={"classical_preparation_wall_seconds":.01}
    records=[{"case":"fixture","model":"bosonic","classical_setup_wall_seconds":.004,
              "classical_postprocessing_wall_seconds":.03,"classical_aggregation_wall_seconds":.002,
              "backend_setup_wall_seconds":100.,"observation_generation_wall_seconds":1000.}]
    result=p50.fast_comparison(raw,"fixture",arm,records,.001,"random",100000000)
    assert captured["raw"] is raw and captured["cpu_budget_seconds"]<=.047
    assert set(captured)=={"raw","seed","initialization","cpu_budget_seconds","max_proposals"}
    assert result["total_CPU_allowance_including_adapter"]==pytest.approx(.047)
    assert result["eligible_best_cut"]==(2 if safe else None)
    assert result["comparison_acceptance_eligible"] is safe
    assert result["other_model_preparation_or_diagnostic_seconds_granted"]==0.
    assert result["optical_backend_or_count_seconds_granted"]==0.


def test_paid_incumbents_are_actual_private_samples_without_reference_gifts():
    rows=[{"case":"fixture","model":"bosonic","stage":"training","best_cut":7,"best_subset":[0,1]},
          {"case":"fixture","model":"bosonic","stage":"evaluation","best_cut":9,"best_subset":[0,2]},
          {"case":"fixture","model":"distinguishable","stage":"training","best_cut":8,"best_subset":[0,3]}]
    incumbents=p50.arm_incumbents(rows)
    assert incumbents["bosonic"]["fixture"]["paid_total"]["cut"]==7
    assert incumbents["bosonic"]["fixture"]["fresh_evaluation"]["cut"]==9
    assert incumbents["distinguishable"]["fixture"]["paid_total"]["cut"]==8
    assert incumbents["static_preparation"]["fixture"]=={}
