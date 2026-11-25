"""P55 synthetic preflight only; unopened DEV graph seeds never used here."""
from fractions import Fraction
from contextlib import nullcontext
import importlib.util
import io
import json
import math
from pathlib import Path
import random
import sys
from types import SimpleNamespace

import numpy as np
import pytest
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))
SPEC = importlib.util.spec_from_file_location("p55_probe", ROOT / "research/P55_finite_neutrality_probe.py")
p55 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p55)


def graph(n=4):
    a = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        a[i, (i+1) % n] = a[(i+1) % n, i] = 1 + i % 3
    return a


def case(n=4):
    return {"id": "fixture", "m": n, "k": n//2, "r": n, "family": "ER", "seed": 550012}


def test_exact_spec_grids_retuned_nulls_and_equal_training_effort():
    frozen = json.loads((ROOT / "research/P55_finite_neutrality_spec.json").read_text())
    assert frozen == p55.expected_spec()
    assert len(p55.MODELS) == 6
    assert all(sum(p["training_draws"] for p in p55.policies(m)) == 24 for m in p55.MODELS)
    b = {p["t"] for p in p55.policies("bosonic")}
    d = {p["t"] for p in p55.policies("distinguishable")}
    inc = {p["horizon_tau"] for p in p55.policies("inclusion_walk")}
    assert b <= d and {math.sqrt(2)*t for t in b} <= d
    assert {int(t*t) for t in b} <= inc and {int(2*t*t) for t in b} <= inc
    assert len(p55.policies("species4")) == 6


def test_GLOBAL_seed_freshness_for_ALL_training_and_ALL_possible_fresh_policies_before_data():
    """Metadata only: fixed hashes, no graph, RNG construction, count or phase draw."""
    owners = {}
    def unique(label, value):
        assert type(value) is int and 0 <= value < 2**32
        assert value not in owners, (owners.get(value), label, value)
        owners[value] = label
    for case in p55.expected_spec()["cases"]:
        case_id = case["id"]
        for group in (0, 1):
            unique((case_id, "group", group), p55.base.seed_for(p55.NAMESPACES[f"group{group}"], case_id))
        for mode in p55.FAST_MODES:
            unique((case_id, "FAST", mode), p55.base.seed_for(p55.NAMESPACES["FAST"], case_id, mode))
        for model in p55.MODELS:
            for policy in p55.policies(model):
                for stage in ("training", "evaluation"):
                    trials = range(policy["training_draws"]//4) if stage == "training" else (0, 1)
                    for trial in trials:
                        label = (case_id, model, policy["id"], stage, trial)
                        master = p55.base.seed_for(p55.NAMESPACES[stage], case_id, model, policy["id"], trial)
                        unique(label + ("master",), master)
                        observation = p55.base.seed_for(master, "observation")
                        unique(label + ("observation",), observation)
                        unique(label + ("neutral_rank",), p55.base.seed_for(master, "neutral_rank"))
                        if model == "continuous_phase":
                            for role in ("coherent_coefficients", "coherent_multinomial"):
                                unique(label + (role,), p55.base.seed_for(observation, role))
    assert len(owners) == 596


@pytest.mark.parametrize("bad", ["float", "odd", "asymmetric", "negative", "loop", "overflow"])
def test_integer_graph_guards_do_not_round_or_silently_overflow(bad):
    a = graph()
    if bad == "float": a = a.astype(float)
    elif bad == "odd": a = a[:3, :3]
    elif bad == "asymmetric": a[0, 1] += 1
    elif bad == "negative": a[0, 1] = a[1, 0] = -1
    elif bad == "loop": a[0, 0] = 1
    else: a[0, 1] = a[1, 0] = np.iinfo(np.int64).max
    with pytest.raises(ValueError): p55.validated_graph(a)


@pytest.mark.parametrize("family", ["ER", "RR"])
def test_graph_recipe_uses_non_DEV_fixture_seeds_only(family):
    fixture = {"m": 10, "family": family, "seed": 550012}
    a, b = p55.make_graph(fixture), p55.make_graph(fixture)
    assert np.array_equal(a, b) and np.array_equal(a, a.T)
    assert a.dtype == np.int64 and np.diag(a).sum() == 0
    assert np.all((a[a > 0] >= 1) & (a[a > 0] <= 5))
    if family == "RR": assert np.count_nonzero(a, axis=1).tolist() == [4]*10


@pytest.mark.parametrize("time_label,t", [("1", 1.), ("2", 2.), ("4", 4.)])
def test_generator_uses_sqrt_weights_and_normalized_operator_exponential(time_label, t):
    a = graph()
    arm = p55.prepare_arm(a, case(), "bosonic")
    h = np.sqrt(a.astype(float))
    rho = np.linalg.norm(h, 2)
    u = arm["contexts"][time_label]["u"]
    assert arm["Hbar"] == pytest.approx(h/rho, abs=1e-14)
    assert u == pytest.approx(expm(1j*t*h/rho), abs=2e-14)
    assert (abs(u)**2).sum(axis=1) == pytest.approx(np.ones(4), abs=2e-14)


def test_zero_graph_scale_and_relabeling_do_not_require_spectral_gaps():
    a, perm = graph(), [2, 0, 3, 1]
    first = p55.prepare_arm(a, case(), "bosonic")
    scaled = p55.prepare_arm(4*a, case(), "bosonic")
    other = p55.prepare_arm(a[np.ix_(perm, perm)], case(), "bosonic")
    zero = p55.prepare_arm(np.zeros_like(a), case(), "bosonic")
    for key in first["contexts"]:
        u = first["contexts"][key]["u"]
        assert scaled["contexts"][key]["u"] == pytest.approx(u, abs=2e-14)
        assert other["contexts"][key]["u"] == pytest.approx(u[np.ix_(perm, perm)], abs=2e-14)
        assert zero["contexts"][key]["u"] == pytest.approx(np.eye(4), abs=1e-14)


@pytest.mark.parametrize("kind", ["identity", "uniform", "mixed"])
def test_r20_Decimal80_PGF_matches_independent_exact_Fraction_coefficients(kind):
    if kind == "identity":
        row, shifted = (Fraction(1),) + (Fraction(0),)*19, [Fraction(1), Fraction(1)] + [Fraction(0)]*19
    elif kind == "uniform":
        row = (Fraction(1, 20),)*20
        shifted = [Fraction(math.factorial(h)*math.comb(20, h), 20**h) for h in range(21)]
    else:
        row = tuple(Fraction(i, 210) for i in range(1, 21))
        # Independent closed family: e_h(1,..,20)=unsigned Stirling(21,21-h).
        stirling = [1]
        for size in range(1, 22):
            previous = stirling
            stirling = [0] + [(previous[k-1] if k-1 < len(previous) else 0)
                              + (size-1)*(previous[k] if k < len(previous) else 0)
                              for k in range(1, size+1)]
        shifted = [Fraction(math.factorial(h)*stirling[21-h], 210**h) for h in range(21)]
    expected = [sum(((-1)**(h-s)*math.comb(h, s)*shifted[h] for h in range(s, 21)), Fraction(0)) for s in range(21)]
    actual, receipt = p55.p48.factorial_marginal(row, True)
    assert sum(expected) == 1 and min(expected) >= 0
    assert actual == pytest.approx([float(x) for x in expected], abs=3e-15)
    assert sum(s*expected[s] for s in range(21)) == 1
    assert receipt["precision"] == 80 and Fraction(receipt["pmf_correction_L1"]) <= Fraction(3, 10**12)


def test_marginal_preparation_is_owned_by_its_control_and_guard_is_prospective(monkeypatch):
    def forbidden(*args, **kwargs): raise AssertionError("Other-model marginal work entered B")
    with monkeypatch.context() as m:
        m.setattr(p55, "product_marginals", forbidden)
        p55.prepare_arm(graph(), case(), "bosonic")
    original = p55.p48.factorial_marginal
    def excessive(row, bosonic):
        pmf, receipt = original(row, bosonic)
        return pmf, {**receipt, "pmf_correction_L1": "4e-12"}
    monkeypatch.setattr(p55.p48, "factorial_marginal", excessive)
    with pytest.raises(p55.RetainedFailure): p55.product_marginals(np.eye(4))


def test_full_source_probability_deficit_is_not_a_hidden_vacuum_or_rescaled_row():
    q = np.eye(4); q[0, 0] -= 4e-12
    with pytest.raises(p55.RetainedFailure): p55.product_marginals(q)
    values, receipt = p55.p48.repair_probability_row(q[0])
    assert sum(values) < 1 and not receipt["subunit_row_rescaled_to1"]


def test_independent_counts_keep_variable_M_and_maximum_fixture_DP_is_bounded():
    pmf = np.zeros((20, 21)); pmf[:, 2] = 1
    counts, metadata = p55.independent_counts(np.cumsum(pmf, axis=1), np.random.default_rng(550019))
    assert counts.dtype.kind in "iu" and counts.sum() == 40 and not metadata["total_count_conditioned"]
    observation = p55.decode_observation(graph(20), np.full(20, 20, dtype=np.int64), random.Random(550020), "independent_B_marginals")
    assert observation["total_count"] == 400 and observation["DP_cells"] == 92631
    assert observation["ways"] == math.comb(20, 10) and len(observation["subset"]) == 10


class OneHop:
    def __init__(self): self.calls = 0
    def exponential(self, scale):
        self.calls += 1
        return .1 if self.calls == 1 else 10.
    def choice(self, size, p):
        assert size == 16 and p.sum() == pytest.approx(1.) and p[1] > 0
        return 1


def test_CTMC_starts_fullCF_and_horizon_or_event_cap_never_decodes_a_truncated_chain():
    q = np.zeros((4, 4)); q[0, 1] = q[1, 0] = .25
    counts, extra = p55.inclusion_draw(q, 1, OneHop())
    assert counts.tolist() == [2, 0, 1, 1] and extra["horizon_completed"] and extra["inclusion_events"] == 1
    with pytest.raises(p55.RetainedFailure) as caught: p55.inclusion_draw(q, 1, OneHop(), event_cap=0)
    assert caught.value.evidence["counts"].tolist() == [1]*4
    assert not caught.value.evidence["horizon_completed"] and caught.value.evidence["rate_total"] == 1.
    assert caught.value.evidence["elapsed"] == 0. and caught.value.evidence["proposed_next_event_time"] == .1
    counts, extra = p55.inclusion_draw(np.zeros((4, 4)), 32, OneHop())
    assert counts.tolist() == [1]*4 and extra["inclusion_events"] == 0


def test_CTMC_horizon_tau_is_passed_directly_not_squared():
    rng = SimpleNamespace(exponential=lambda scale: 3., choice=lambda *args, **kwargs: pytest.fail("tau was squared"))
    q = np.zeros((4, 4)); q[0, 1] = q[1, 0] = .25
    counts, extra = p55.inclusion_draw(q, horizon_tau=2, rng=rng)
    assert counts.tolist() == [1]*4 and extra["inclusion_events"] == 0 and extra["horizon_tau"] == 2


def test_phase_is_full_count_sampler_and_exact_rank_seed_is_separate(monkeypatch):
    arm = p55.prepare_arm(graph(), case(), "continuous_phase")
    calls = []
    def coherent(context, model, seed):
        calls.append((context["v"].shape, model, seed))
        return lambda: (np.asarray([4, 0, 0, 0], dtype=np.int64), {"fixture": True})
    monkeypatch.setattr(p55.p48, "coherent_counts", coherent)
    monkeypatch.setattr(p55.base, "weighted_subset", lambda *args: pytest.fail("Wrong CF-only phase sampler"))
    draw, rank_rng, roles = p55.observation_components(arm, p55.policies("continuous_phase")[0], 550021, p55.Meter())
    counts, _ = draw()
    assert calls[0][:2] == ((4, 4), "continuous_phase") and counts.sum() == 4
    assert len(set(roles.values())) == len(roles) and all(isinstance(x, int) for x in roles.values())
    decoded = p55.decode_observation(arm["a"], counts, rank_rng, arm["model"])
    assert decoded["ways"] == 6 and isinstance(decoded["uniform_rank"], int)


@pytest.mark.parametrize("model", ["bosonic", "distinguishable", "species4"])
def test_existing_optical_factory_receives_full_input_and_preserves_integer_counts(monkeypatch, model):
    arm = p55.prepare_arm(graph(8), case(8), model)
    called = []
    def factory(u, source, name, seed):
        called.append((u.shape, list(source), name, seed))
        return (lambda: (np.ones(8, dtype=np.int64), False)), 0.
    monkeypatch.setattr(p55.base, "make_optical_sampler", factory)
    draw, _, _ = p55.observation_components(arm, p55.policies(model)[0], 550022, p55.Meter())
    counts, _ = draw()
    assert called[0][0] == (8, 8) and sorted(called[0][1]) == list(range(8))
    assert called[0][2] == model and isinstance(called[0][3], int) and counts.sum() == 8


@pytest.mark.parametrize("bad_counts", [[1., 1., 1., 1.], [True]*4, [-1, 1, 2, 2], [5, 0, 0, 0], [0, 0, 0, 0]])
def test_physical_counts_are_never_silently_cast_or_reconditioned(bad_counts):
    with pytest.raises(p55.RetainedFailure):
        p55.decode_observation(graph(), np.asarray(bad_counts), random.Random(1), "bosonic")


def test_native_maximum_thread_setter_and_both_readbacks_are_explicit():
    xq = SimpleNamespace(Config=SimpleNamespace(compute_max_thread_count=8))
    receipt = p55.configure_native_threads(xq)
    assert receipt["before"] == 8 and receipt["configured_before_work"] == 1
    assert p55.native_thread_readback(xq) == 1
    xq.Config.compute_max_thread_count = 2
    with pytest.raises(p55.RetainedFailure): p55.native_thread_readback(xq)


def test_setup_clock_subtraction_and_B_only_allowance_exclude_backend_controls_and_IO():
    assert p55.classical_setup({"wall_seconds": 7., "cpu_seconds": 4.}, {"wall_seconds": 5., "cpu_seconds": 3.}) == {"wall_seconds": 2., "cpu_seconds": 1.}
    with pytest.raises(p55.RetainedFailure): p55.classical_setup({"wall_seconds": 1., "cpu_seconds": 1.}, {"wall_seconds": 2., "cpu_seconds": 1.})
    arm = {"model": "bosonic", "case": "fixture", "classical_preparation": {"wall_seconds": .01}}
    rows = [{"model": "bosonic", "case": "fixture", "classical_setup": {"wall_seconds": .002},
             "postprocessing": {"wall_seconds": .03}, "aggregation": {"wall_seconds": .001},
             "backend": {"wall_seconds": 1000}, "count_generation": {"wall_seconds": 2000},
             "other_model": 3000, "serialization": 4000}]
    assert p55.B_allowance(arm, rows, .002) == pytest.approx(.045)
    with pytest.raises(ValueError): p55.B_allowance(arm, [{**rows[0], "model": "continuous_phase"}], 0.)


def test_immutable_factory_preclock_RNG_validation_prefix_is_paid_and_CPU_split_is_unknown(monkeypatch):
    arm = p55.prepare_arm(graph(), case(), "bosonic")
    backend = p55.Meter()
    class FactoryMeter:
        wall, cpu = 7., 4.
        def measure(self): return nullcontext()
        def record(self): return {"wall_seconds": self.wall, "cpu_seconds": self.cpu}
    monkeypatch.setattr(p55, "Meter", FactoryMeter)
    monkeypatch.setattr(p55.base, "make_optical_sampler", lambda *args:
                        ((lambda: (np.ones(4, dtype=np.int64), False)), 5.))
    p55.observation_components(arm, p55.policies("bosonic")[0], 550023, backend)
    assert backend.wall == 5. and backend.cpu is None
    assert backend.record()["factory_total"] == {"wall_seconds": 7., "cpu_seconds": 4.}
    # Two seconds inside the factory precede its timer; two more are caller setup.
    charged = p55.classical_setup({"wall_seconds": 9., "cpu_seconds": 6.}, backend.record())
    assert charged["wall_seconds"] == 4. and charged["cpu_seconds"] is None
    assert not charged["CPU_split_available"]


def training_rows(model, cases, winner):
    return [{"model": model, "case": case["id"], "policy": p["id"], "stage": "training", "trial": trial,
             "proposals": 4, "cuts": [1 if p["id"] == winner else 10]*4,
             "sum_cuts": 4 if p["id"] == winner else 40, "weight_denominator": case["weight_denominator"]}
            for p in p55.policies(model) for case in cases for trial in range(p["training_draws"]//4)]


def test_ALL_shot_Fraction_selection_is_independent_complete_and_precedes_fresh():
    cases = [{"id": "a", "weight_denominator": 10}, {"id": "b", "weight_denominator": 100}]
    b = training_rows("bosonic", cases, 1)
    d = training_rows("distinguishable", cases, 4)
    assert p55.select_policy(b, cases, "bosonic")[0] == 1
    assert p55.select_policy(d, cases, "distinguishable")[0] == 4
    bad = [dict(row) for row in b]
    for row in bad:
        if row["policy"] == 0:
            row["cuts"] = [0, 0, 0, 10]; row["sum_cuts"] = 10
    assert p55.select_policy(bad, cases, "bosonic")[0] == 1
    with pytest.raises(ValueError): p55.select_policy(b[:-1], cases, "bosonic")
    with pytest.raises(ValueError): p55.select_policy([{**b[0], "stage": "evaluation"}] + b[1:], cases, "bosonic")
    for row in b: row["cuts"] = [5]*4; row["sum_cuts"] = 20
    assert p55.select_policy(b, cases, "bosonic")[0] == 0


def test_failed_batch_retains_counts_partial_work_and_never_resamples(monkeypatch):
    arm = p55.prepare_arm(graph(), case(), "bosonic")
    calls = []
    def components(*args):
        def draw():
            calls.append(1)
            if len(calls) == 2: raise p55.RetainedFailure("synthetic fail", {"counts": [2, 0, 1, 1]})
            return np.ones(4, dtype=np.int64), {}
        return draw, random.Random(1), {"fixture": 1}
    monkeypatch.setattr(p55, "observation_components", components)
    stream = io.StringIO()
    with pytest.raises(p55.RetainedFailure) as caught:
        p55.run_batch(arm, p55.policies("bosonic")[0], "training", 0, 4, stream)
    events = [json.loads(line) for line in stream.getvalue().splitlines()]
    assert len(calls) == 2 and len(events) == 2 and events[-1]["record_type"] == "failed_shot"
    assert len(caught.value.evidence["completed_cuts"]) == 1
    assert caught.value.evidence["evidence"]["counts"] == [2, 0, 1, 1]


def test_FAST_caller_uses_only_eligible_nullable_online_prefix(monkeypatch):
    arm = {"model": "bosonic", "case": "fixture", "classical_preparation": {"wall_seconds": .01}}
    seen = []
    def solve(raw, **kwargs):
        seen.append(kwargs)
        return {"has_eligible_result": True, "comparison_acceptance_eligible": True,
                "early_cap_inconclusive": False, "early_wall_inconclusive": False,
                "first_scan_completed_before_deadline": True,
                "best_cut": 7, "best_subset": [0, 1], "overall_completed_best_cut": 0}
    monkeypatch.setattr(p55.fast, "solve_from_raw", solve)
    row = p55.fast_comparison(graph(), arm, [], 0., "random")
    assert row["eligible_best_cut"] == 7 and row["comparison_acceptance_eligible"]
    assert set(seen[0]) == {"seed", "initialization", "cpu_budget_seconds", "max_proposals"}
    assert seen[0]["cpu_budget_seconds"] <= .01 and isinstance(seen[0]["seed"], int)


def test_veto_requires_one_FIXED_FAST_algorithm_on_BOTH_graphs_not_free_portfolio():
    cases = [{"id": "a", "weight_denominator": 100}, {"id": "b", "weight_denominator": 100}]
    records = [{"case": case["id"], "model": model, "stage": stage, "proposals": count,
                "cuts": [10 if model == "bosonic" else 20]*count,
                "sum_cuts": (10 if model == "bosonic" else 20)*count}
               for case in cases for model in p55.MODELS for stage, count in (("training", 24), ("evaluation", 16))]
    fast = [{"case": case["id"], "mode": mode, "comparison_acceptance_eligible": True,
             "prefix_eligible_for_veto": True,
             "eligible_best_cut": value} for case, values in zip(cases, ((9, 11), (11, 9)))
            for mode, value in zip(p55.FAST_MODES, values)]
    mixed = p55.summarize(records, cases, fast)
    assert not mixed["fixed_FAST_veto_algorithms"] and mixed["status"] == "INCONCLUSIVE_MIXED_DEV"
    fast[2]["eligible_best_cut"] = 10
    rejected = p55.summarize(records, cases, fast)
    assert rejected["fixed_FAST_veto_algorithms"] == ["random"]
    assert rejected["status"] == "DEV_REJECTED_FIXED_FAST" and not rejected["positive_accepted"]
    assert p55.summarize(records, cases, fast[:-1])["status"] == "INCONCLUSIVE_FAST_ELIGIBILITY"


def test_followup_requires_EVERY_control_on_EVERY_graph_and_nonstrict_D_mean_rejects():
    cases = [{"id": "a", "weight_denominator": 100}, {"id": "b", "weight_denominator": 100}]
    rows = [{"case": c["id"], "model": m, "stage": stage, "proposals": count,
             "cuts": [10 if m == "bosonic" else 20]*count,
             "sum_cuts": (10 if m == "bosonic" else 20)*count}
            for c in cases for m in p55.MODELS for stage, count in (("training", 24), ("evaluation", 16))]
    fast = [{"case": c["id"], "mode": mode, "comparison_acceptance_eligible": True,
             "prefix_eligible_for_veto": True, "eligible_best_cut": 11}
            for c in cases for mode in p55.FAST_MODES]
    assert p55.summarize(rows, cases, fast)["status"] == "FOLLOW_UP_ONLY"
    for row in rows:
        if row["case"] == "a" and row["model"] == "continuous_phase" and row["stage"] == "evaluation":
            row["cuts"] = [5]*16; row["sum_cuts"] = 80
    assert p55.summarize(rows, cases, fast)["status"] == "INCONCLUSIVE_MIXED_DEV"
    for row in rows:
        if row["case"] == "a" and row["model"] == "distinguishable" and row["stage"] == "evaluation":
            row["cuts"] = [0]*16; row["sum_cuts"] = 0
    assert p55.summarize(rows, cases, fast)["status"] == "DEV_REJECTED_REQUIRED_CONTROL_MEAN"


def test_paid_FAST_initialization_without_scan_can_refute_but_never_open_followup(monkeypatch):
    arm = {"model": "bosonic", "case": "fixture", "classical_preparation": {"wall_seconds": .01}}
    def solve(raw, **kwargs):
        return {"has_eligible_result": True, "comparison_acceptance_eligible": True,
                "early_cap_inconclusive": False, "early_wall_inconclusive": False,
                "first_scan_completed_before_deadline": False, "best_cut": 7, "best_subset": [0, 1]}
    monkeypatch.setattr(p55.fast, "solve_from_raw", solve)
    row = p55.fast_comparison(graph(), arm, [], 0., "random")
    assert row["prefix_eligible_for_veto"] and not row["comparison_acceptance_eligible"]


@pytest.mark.parametrize("scenario", ["none", "early_cap", "no_scan"])
def test_FAST_null_or_incomplete_prefix_never_becomes_positive_eligible(monkeypatch, scenario):
    arm = {"model": "bosonic", "case": "fixture", "classical_preparation": {"wall_seconds": .01}}
    def solve(raw, **kwargs):
        return {"has_eligible_result": scenario != "none", "comparison_acceptance_eligible": scenario != "none",
                "early_cap_inconclusive": scenario == "early_cap", "early_wall_inconclusive": False,
                "first_scan_completed_before_deadline": scenario != "no_scan",
                "best_cut": None if scenario == "none" else 7, "best_subset": None if scenario == "none" else [0, 1]}
    monkeypatch.setattr(p55.fast, "solve_from_raw", solve)
    row = p55.fast_comparison(graph(), arm, [], 0., "spectral")
    assert not row["comparison_acceptance_eligible"]
    if scenario == "none": assert row["eligible_best_cut"] is None and not row["prefix_eligible_for_veto"]


def test_batch_training_and_fresh_seeds_differ_and_ALL_synthetic_shots_are_preserved(monkeypatch):
    arm = p55.prepare_arm(graph(), case(), "bosonic")
    def components(arm, policy, seed, backend):
        return lambda: (np.ones(4, dtype=np.int64), {}), random.Random(seed), {"fixture": seed}
    monkeypatch.setattr(p55, "observation_components", components)
    stream = io.StringIO()
    train = p55.run_batch(arm, p55.policies("bosonic")[0], "training", 0, 4, stream)
    fresh = p55.run_batch(arm, p55.policies("bosonic")[0], "evaluation", 0, 8, stream)
    rows = [json.loads(line) for line in stream.getvalue().splitlines()]
    assert train["seed"] != fresh["seed"] and train["proposals"] == 4 and fresh["proposals"] == 8
    assert len(rows) == 12 and sum(train["cuts"]) == train["sum_cuts"] and sum(fresh["cuts"]) == fresh["sum_cuts"]
    assert all(isinstance(row["uniform_rank"], int) and len(row["subset"]) == 2 for row in rows)


def test_main_preserves_failure_json_without_actual_DEV_graph_or_native_import(monkeypatch, tmp_path):
    # Entire workflow is mocked before graph/arm/sample construction; no DEV population is opened.
    monkeypatch.setitem(sys.modules, "exqalibur", SimpleNamespace(Config=SimpleNamespace(compute_max_thread_count=4)))
    monkeypatch.setattr(p55, "make_graph", lambda case: np.zeros((20, 20), dtype=np.int64))
    payload = {"counts": [2, 0] + [1]*18, "elapsed": .1, "rate_total": 2.,
               "proposed_next_event_time": .2, "horizon_tau": 1, "horizon_completed": False}
    def fail(*args): raise p55.RetainedFailure("synthetic CTMC cap payload", payload)
    monkeypatch.setattr(p55, "prepare_arm", fail)
    target = tmp_path/"data"
    monkeypatch.setattr(sys, "argv", ["p55", "--spec", str(ROOT/"research/P55_finite_neutrality_spec.json"), "--output", str(target)])
    assert p55.main() == 1
    failure = json.loads((target/"failure.json").read_text())["failure"]
    summary = json.loads((target/"summary.json").read_text())
    assert failure["evidence"] == payload and not summary["positive_accepted"]
    assert summary["status"] == "INCONCLUSIVE_FIRST_FAILURE" and summary["completed_shots"] == 0
