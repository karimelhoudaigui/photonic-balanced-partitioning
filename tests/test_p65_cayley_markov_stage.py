"""Prospective P65 qualification; no DEV graph or true ten-photon draw.

Only the explicitly marked four-mode/two-photon HOM fixture uses a native
sampler. Twenty-mode arrays below are hardcoded mock-state bookkeeping, never
compiled or supplied to a real backend. No code was executed while authoring.
"""
from fractions import Fraction
from collections import Counter
from contextlib import contextmanager
import gzip
import hashlib
import importlib.util
import io
import itertools
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))
SPEC = importlib.util.spec_from_file_location("p65_stage_candidate",
                                            ROOT / "research/P65_cayley_markov_stage.py")
p = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = p
SPEC.loader.exec_module(p)


def _inverse(matrix):
    """Independent tiny dense Gauss--Jordan reference, no np.linalg.solve."""
    n = len(matrix)
    work = [[complex(matrix[i][j]) for j in range(n)] +
            [complex(i == j) for j in range(n)] for i in range(n)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(work[row][column]))
        work[column], work[pivot] = work[pivot], work[column]
        divisor = work[column][column]
        assert abs(divisor) > 1e-14
        work[column] = [entry / divisor for entry in work[column]]
        for row in range(n):
            if row != column:
                factor = work[row][column]
                work[row] = [a - factor * b for a, b in zip(work[row], work[column])]
    return np.array([row[n:] for row in work])


def _mock_adjacency():
    a = np.zeros((20, 20), dtype=np.int64)
    a[0, 1] = a[1, 0] = 1
    return a


def _mock_arm():
    # The opaque network tokens MUST only reach injected mock factories.
    return {"case": "synthetic_twenty_slot_bookkeeping", "model": "bosonic",
            "a": _mock_adjacency(), "W": 1,
            "networks": [{"U": object()} for _ in range(8)],
            "paid_wall": 0.0, "paid_components": [], "paid_best": None,
            "attempted": 0, "completed": 0,
            "score_counts": {"initial": 0, "proposal": 0, "current": 0}}


def _counts(source):
    answer = np.zeros(20, dtype=np.int64)
    answer[list(source)] = 1
    return answer


def _identity_mock_factory(calls):
    def factory(u, source, model, seed):
        calls.append({"network": u, "source": list(source), "model": model, "seed": seed})
        return lambda: (_counts(source), False), 0.0
    return factory


def _solver_result(best=7, budget=2.0, timestamp=0.1, early=False, scan=True):
    return {"cpu_budget_seconds": budget, "eligible_checkpoint_cpu_seconds": timestamp,
            "best_cut": best, "has_eligible_result": True,
            "best_snapshot_cached_online": True, "comparison_acceptance_eligible": not early,
            "early_cap_inconclusive": early, "early_wall_inconclusive": False,
            "first_scan_completed_before_deadline": scan,
            "overall_completed_best_cut": 0, "trace": {"cpu_seconds": [timestamp]}}


def _stage_rows(random=(9, 9), spectral=(12, 12)):
    return [{"case": "case" + str(i), "B_paid_best": 10,
             "FAST": {"random": p.fast_summary(_solver_result(best=random[i])),
                      "spectral": p.fast_summary(_solver_result(best=spectral[i]))}}
            for i in range(2)]


class _VirtualClock:
    def __init__(self):
        self.wall = self.cpu = 0.0
    def advance(self, wall, cpu):
        self.wall += wall
        self.cpu += cpu


def _patch_clock(monkeypatch, clock):
    # Replace this module's binding, not global time functions used by pytest.
    monkeypatch.setattr(p, "time", SimpleNamespace(perf_counter=lambda: clock.wall,
                                                 process_time=lambda: clock.cpu))


def test_two_mode_cayley_has_independent_rational_closed_form():
    a = np.array([[0, 7], [7, 0]], dtype=np.int64)
    u, construction = p.cayley_matrix(a, Fraction(1, 2), Fraction(0))
    expected = np.array([[3 / 5, 4j / 5], [4j / 5, 3 / 5]])
    assert np.max(abs(u - expected)) < 2e-14
    assert construction["denominator"] == 7
    assert construction["weighted_degrees"].tolist() == [7, 7]
    assert max(p.matrix_diagnostics(u).values()) <= p.TOLERANCE


def test_weighted_degree_differs_from_neighbor_count_and_reference_inverse():
    a = np.array([[0, 7, 0, 0], [7, 0, 2, 0],
                  [0, 2, 0, 3], [0, 0, 3, 0]], dtype=np.int64)
    u, details = p.cayley_matrix(a, Fraction(1, 2), Fraction(1, 4))
    # Weighted maximum9, not the maximum unweighted degree2.
    assert details["denominator"] == Fraction(39, 4)
    assert details["weighted_degrees"].tolist() == [7, 9, 5, 3]
    h = (4 * a + np.ones((4, 4)) - np.eye(4)) / 39
    expected = (np.eye(4) + 0.5j * h) @ _inverse(np.eye(4) - 0.5j * h)
    assert np.max(abs(details["H"] - h)) < 2e-15
    assert np.max(abs(u - expected)) < 2e-14


def test_small_graph_relabeling_covariance_and_disconnected_scope():
    a = np.array([[0, 3, 0, 0], [3, 0, 0, 0],
                  [0, 0, 0, 1], [0, 0, 1, 0]], dtype=np.int64)
    permutation = [2, 0, 3, 1]
    for lam in [Fraction(0), Fraction(1, 4)]:
        u, _ = p.cayley_matrix(a, Fraction(1, 2), lam)
        relabeled, _ = p.cayley_matrix(a[np.ix_(permutation, permutation)], Fraction(1, 2), lam)
        assert np.max(abs(relabeled - u[np.ix_(permutation, permutation)])) < 2e-14
    uncoupled, _ = p.cayley_matrix(a, Fraction(1, 2), Fraction(0))
    coupled, _ = p.cayley_matrix(a, Fraction(1, 2), Fraction(1, 4))
    assert np.max(abs(uncoupled[:2, 2:])) == 0
    assert np.max(abs(coupled[:2, 2:])) > 1e-4
    # This one coupling fixture does not certify general ergodicity.


@pytest.mark.parametrize("kind", ["nonunitary", "asymmetric_unitary", "nonfinite"])
def test_small_matrix_diagnostics_fail_without_silent_repair(kind):
    bad = np.eye(2, dtype=complex)
    if kind == "nonunitary": bad[0, 0] = 2
    if kind == "asymmetric_unitary": bad = np.array([[0, 1], [-1, 0]], dtype=complex)
    if kind == "nonfinite": bad[0, 0] = float("nan")
    original = bad.copy()
    with pytest.raises(p.RetainedFailure):
        p.matrix_diagnostics(bad)
    assert np.array_equal(bad, original, equal_nan=True)


@pytest.mark.parametrize("kind", ["unsorted", "float", "duplicate", "out_of_range", "bool"])
def test_mock_source_index_guard_rejects_without_preparation(kind):
    source = list(range(10))
    if kind == "unsorted": source.reverse()
    if kind == "float": source[2] = 2.0
    if kind == "duplicate": source = sorted([0, 0] + list(range(1, 9)))
    if kind == "out_of_range": source[-1] = 20
    if kind == "bool": source[0] = False
    with pytest.raises(p.RetainedFailure, match="current source"):
        p.validated_source(source)


def test_small_complete_cf_kernels_and_physical_collision_mass():
    # Mixing Hamiltonian only: this is NOT the graph-cost barrier example.
    adjacency = np.array([[0, 0, 1, 1], [0, 0, 1, 1],
                          [1, 1, 0, 0], [1, 1, 0, 0]], dtype=np.int64)
    u, _ = p.cayley_matrix(adjacency, Fraction(1), Fraction(0))
    subsets = list(itertools.combinations(range(4), 2))
    kernels = []
    for bosonic in [True, False]:
        kernel = np.zeros((6, 6))
        for s, source in enumerate(subsets):
            for t, target in enumerate(subsets):
                paths = [u[target[0], source[0]] * u[target[1], source[1]],
                         u[target[0], source[1]] * u[target[1], source[0]]]
                kernel[s, t] = abs(sum(paths))**2 if bosonic else sum(abs(x)**2 for x in paths)
            kernel[s, s] += 1 - math.fsum(kernel[s])
        assert np.max(abs(kernel - kernel.T)) < 2e-14
        assert np.max(abs(kernel.sum(axis=1) - 1)) < 2e-14
        assert np.min(kernel) >= -2e-14
        kernels.append(kernel)
    first, last = subsets.index((0, 1)), subsets.index((2, 3))
    assert kernels[0][first, last] == pytest.approx(1 / 4, abs=2e-14)
    assert kernels[1][first, last] == pytest.approx(1 / 8, abs=2e-14)
    # Direct full two-photon law, including bunched Fock normalization.
    occupations = [tuple(int(i == a) + int(i == b) for i in range(4))
                   for a in range(4) for b in range(a, 4)]
    full = []
    for counts in occupations:
        rows = [i for i, multiplicity in enumerate(counts) for _ in range(multiplicity)]
        permanent = u[rows[0], 0] * u[rows[1], 1] + u[rows[0], 1] * u[rows[1], 0]
        full.append(abs(permanent)**2 / math.prod(math.factorial(c) for c in counts))
    assert math.fsum(full) == pytest.approx(1, abs=2e-14)
    assert math.fsum(value for n, value in zip(occupations, full) if max(n) > 1) == pytest.approx(1 / 2)
    # A symmetric proposal with paid self-loops obeys Metropolis balance.
    costs = np.array([3, 1, 2, 2, 1, 3], dtype=float)
    mass = np.exp(-0.3 * costs)
    mass /= mass.sum()
    for kernel in kernels:
        transition = kernel.copy()
        for i in range(6):
            for j in range(6):
                if i != j:
                    transition[i, j] *= min(1, math.exp(-0.3 * (costs[j] - costs[i])))
            transition[i, i] = 1 - sum(transition[i, j] for j in range(6) if j != i)
        flow = mass[:, None] * transition
        assert np.max(abs(flow - flow.T)) < 2e-14


def test_only_true_native_fixture_is_two_photon_four_mode_hom(record_property):
    import exqalibur as xq
    native = p.configure_native_threads(xq)
    u = np.eye(4, dtype=complex)
    u[:2, :2] = np.array([[1, 1j], [1j, 1]]) / math.sqrt(2)
    draw, setup = p.base.make_optical_sampler(u, [0, 1], "bosonic", 6599001)
    observations = []
    for _ in range(8):
        counts, fallback = draw()
        value = tuple(int(c) for c in counts)
        assert not fallback and value in {(2, 0, 0, 0), (0, 2, 0, 0)}
        observations.append(value)
    assert math.isfinite(setup) and setup >= 0
    assert p.native_readback(xq) == 1
    record_property("P65_HOM_seed", "6599001")
    record_property("P65_HOM_all_eight_counts", json.dumps(observations))
    record_property("P65_native_threads", json.dumps(native))


def test_current_source_factory_is_fresh_and_cf_coins_include_probability_one():
    arm = _mock_arm()
    initial, changed = list(range(10)), [0] + list(range(2, 11))
    initial_cut = p.score(arm, initial, "initial", ("synthetic_start",))
    state = {"current": list(initial), "current_cut": initial_cut,
             "best_cut": initial_cut, "current_cuts": []}
    sources, coins = [], []
    def factory(u, source, model, seed):
        sources.append(list(source))
        index = len(sources) - 1
        if index < 2:
            output = _counts(changed)
        else:
            output = _counts(changed)
            output[0], output[2] = 2, 0
        return lambda: (output, False), 0.0
    def coin(seed):
        coins.append(seed)
        return 0.25
    stream, rows = io.StringIO(), []
    for step in range(3):
        rows.append(p.run_attempt(arm, state, 0, ("fresh", "selected", 0, step),
                                  0.0, stream, factory=factory, coin_draw=coin))
    assert sources == [initial, changed, changed]
    assert len(coins) == 2 and coins[0] != coins[1]
    assert rows[0]["accepted"] and rows[0]["acceptance_probability"] == 1
    assert rows[1]["proposal"] == changed and rows[1]["source"] == changed
    assert rows[1]["coin_seed_used"] and rows[1]["acceptance_probability"] == 1
    assert rows[2]["collision"] and rows[2]["coin"] is None and not rows[2]["coin_seed_used"]
    assert rows[2]["current"] == changed and rows[2]["current_cut"] == 1
    assert arm["score_counts"] == {"initial": 1, "proposal": 2, "current": 3}
    assert arm["attempted"] == arm["completed"] == 3


def test_fresh_chain_best_is_own_start_and_repeated_starts_are_retained(monkeypatch):
    arm = _mock_arm()
    starts, calls, coins = [], [], []
    initial, repeated_fresh = list(range(10)), [0] + list(range(2, 11))
    def start(a, stage, chain):
        starts.append((stage, chain))
        return list(initial if stage == "training" else repeated_fresh), 100 + chain
    monkeypatch.setattr(p, "uniform_start", start)
    result = p.run_arm(arm, io.StringIO(), lambda: None,
                       factory=_identity_mock_factory(calls),
                       coin_draw=lambda seed: coins.append(seed) or 0.25)
    assert starts == [("training", 0), ("fresh", 0), ("fresh", 1), ("fresh", 2)]
    assert len(calls) == len(coins) == 40
    assert result["selected_candidate"] == 0
    assert result["fitnesses"] == [Fraction(0)] * 8
    assert result["B_paid_best"] == 0
    assert [chain["initial"] for chain in result["fresh"]] == [repeated_fresh] * 3
    assert [chain["chain_best_cut"] for chain in result["fresh"]] == [1, 1, 1]
    assert result["B_fresh_chain_best_normalized_mean"] == 1
    assert result["score_counts"] == {"initial": 4, "proposal": 40, "current": 40}
    assert [len(chain["current_cuts"]) for chain in result["fresh"]] == [8, 8, 8]


def test_rejected_cf_still_scores_current_and_keeps_its_fresh_coin():
    arm, initial = _mock_arm(), list(range(10))
    initial_cut = p.score(arm, initial, "initial", ("start",))
    state = {"current": initial, "current_cut": initial_cut,
             "best_cut": initial_cut, "current_cuts": []}
    proposal, coins = [0] + list(range(2, 11)), []
    def factory(*args):
        return lambda: (_counts(proposal), False), 0.0
    row = p.run_attempt(arm, state, 0, ("training", 0, 0, 0), math.log(4),
                        io.StringIO(), factory=factory,
                        coin_draw=lambda seed: coins.append(seed) or 0.75)
    assert row["acceptance_probability"] == pytest.approx(1 / 4)
    assert not row["accepted"] and row["current"] == initial
    assert row["current_cut"] == 0 and row["proposal_cut"] == 1
    assert len(coins) == 1 and arm["score_counts"] == {"initial": 1, "proposal": 1, "current": 1}


def test_nonzero_paid_ledger_reconstructs_from_independent_nested_raw_meters(monkeypatch):
    class SyntheticMeter:
        def __init__(self): self.wall = self.cpu = 0.0
        @contextmanager
        def measure(self):
            try: yield
            finally:
                self.wall += 1.0
                self.cpu += 0.25
        def record(self):
            return {"wall_seconds": self.wall, "cpu_seconds": self.cpu}
    monkeypatch.setattr(p, "Meter", SyntheticMeter)
    arm = _mock_arm()
    monkeypatch.setattr(p, "uniform_start", lambda a, stage, chain: (list(range(10)), 100 + chain))
    def factory(u, source, model, seed):
        return lambda: (_counts(source), False), 0.4
    result = p.run_arm(arm, io.StringIO(), lambda: None, factory=factory, coin_draw=lambda seed: 0.2)
    components = result["paid_components"]
    expected_counts = {"training_start": 1, "chain_reset": 11, "beta": 40,
                       "attempt_setup": 40, "attempt_postprocessing": 40,
                       "factory_classical_prefix": 40, "fitness": 8, "selection": 1,
                       "fresh_start": 3, "chain_final": 11, "arm_final": 1}
    assert Counter(component["label"][0] for component in components) == expected_counts
    assert all(component["wall_seconds"] > 0 for component in components)
    assert all(component["cpu_seconds"] is None for component in components
               if component["label"][0] == "factory_classical_prefix")
    reconstructed = (result["training_start_compute"]["wall_seconds"] +
                     result["selection_compute"]["wall_seconds"] +
                     result["final_aggregation"]["wall_seconds"])
    reconstructed += sum(row["fitness_compute"]["wall_seconds"] for row in result["training"])
    reconstructed += sum(row["start_compute"]["wall_seconds"] for row in result["fresh"])
    for chain in result["training"] + result["fresh"]:
        reconstructed += chain["reset_compute"]["wall_seconds"]
        reconstructed += chain["final_aggregation"]["wall_seconds"]
        reconstructed += sum(timer["wall_seconds"] for timer in chain["beta_compute"])
        for attempt in chain["attempts"]:
            reconstructed += attempt["setup"]["wall_seconds"]
            reconstructed += attempt["postprocessing"]["wall_seconds"]
            reconstructed += (attempt["factory_total"]["wall_seconds"] -
                              attempt["factory_accounting"]["returned_backend_wall"])
    assert reconstructed == pytest.approx(result["B_classical_wall"], abs=1e-10)
    assert math.fsum(component["wall_seconds"] for component in components) == pytest.approx(
        result["B_classical_wall"], abs=1e-10)
    # Native setup/count-generation or fictitious optional-arm costs cannot hide
    # in an unexplained remainder: all trajectory costs are reconstructed.
    assert result["B_classical_wall"] == pytest.approx(220.0, abs=1e-10)


@pytest.mark.parametrize("kind", ["float", "negative", "lost", "shape", "fallback", "nan"])
def test_invalid_pnr_is_first_failure_without_retry_and_preserves_payload(kind):
    arm, source = _mock_arm(), list(range(10))
    state = {"current": source, "current_cut": 0, "best_cut": 0, "current_cuts": []}
    bad, fallback = _counts(source), False
    if kind == "float": bad = bad.astype(float)
    if kind == "negative": bad[0], bad[10] = -1, 2
    if kind == "lost": bad[0] = 0
    if kind == "shape": bad = bad[:-1]
    if kind == "fallback": fallback = True
    if kind == "nan": bad = bad.astype(float); bad[0] = float("nan")
    calls = []
    def factory(*args):
        calls.append(args)
        return lambda: (bad, fallback), 0.0
    stream = io.StringIO()
    with pytest.raises(p.RetainedFailure, match="first attempt failure"):
        p.run_attempt(arm, state, 0, ("training", 0, 0, 0), 1.0, stream, factory=factory)
    assert len(calls) == 1 and arm["attempted"] == 1 and arm["completed"] == 0
    assert arm["score_counts"] == {"initial": 0, "proposal": 0, "current": 0}
    failure = json.loads(stream.getvalue().splitlines()[-1])
    assert failure["record_type"] == "failed_attempt" and failure["counts"] is not None
    if kind == "nan": assert failure["counts"][0] == {"nonfinite_float": "nan"}


def test_exact_fitness_selection_uses_mean_and_first_lex_tie():
    assert p.normalized_mean([1, 7], 8) == Fraction(1, 2)
    values = [Fraction(1, 2)] * 8
    values[2] = values[5] = Fraction(1, 3)
    assert p.choose_candidate(values) == 2
    with pytest.raises(ValueError):
        p.choose_candidate([0.5] * 8)


def test_all_optional_streams_are_frozen_without_rng_or_graph(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("metadata must not construct RNG or graph")
    monkeypatch.setattr(p.np.random, "Generator", forbidden)
    monkeypatch.setattr(p, "make_graph", forbidden)
    spec = p.read_spec()
    table = p.seed_namespaces(spec)
    assert len(table) == 820 and len(set(table.values())) == 820
    for case in spec["cases"]:
        cid = case["id"]
        starts = [key for key in table if key[:2] == (cid, "start")]
        assert len(starts) == 6  # One logical alias; no per-arm duplicate stream.
        for arm in p.OPTICAL_ARMS:
            assert sum(key[0] == cid and key[1] == arm and key[-1] == "count" for key in table) == 40
            assert sum(key[0] == cid and key[1] == arm and key[-1] == "coin" for key in table) == 40
        for arm in ("r2", "r3"):
            assert sum(key[0] == cid and key[1] == arm and key[-1] == "replacement" for key in table) == 40
        assert all(value != 0 for key, value in table.items() if key[-1] == "count")
    label = (65200000, spec["cases"][0]["id"], "bosonic", "fresh", "selected", 0, 0)
    independent = int.from_bytes(hashlib.sha256("/".join(map(str, label)).encode()).digest()[:4], "little")
    assert p.attempt_roles(*label[1:])["count"] == independent


def test_seed_collision_is_failure_not_salted_or_resampled(monkeypatch):
    monkeypatch.setattr(p, "seed_for", lambda *parts: 17)
    with pytest.raises(p.RetainedFailure, match="Seed collision"):
        p.seed_namespaces(p.read_spec())


def test_zero_native_seed_is_failure_before_any_count_or_graph(monkeypatch):
    actual = p.seed_for
    monkeypatch.setattr(p, "seed_for", lambda *parts: 0 if parts[0] == p.ROOTS["count"] else actual(*parts))
    with pytest.raises(p.RetainedFailure, match="zero native seed"):
        p.seed_namespaces(p.read_spec())


def test_private_compiler_cost_paid_but_diagnostics_excluded(monkeypatch):
    clock = _VirtualClock()
    _patch_clock(monkeypatch, clock)
    original = p.validated_graph
    def validation(raw):
        clock.advance(5, 0.2)
        return original(raw)
    parameters = []
    def compiler(a, t, lam):
        clock.advance(3, 0.1)
        parameters.append((t, lam))
        return np.eye(2, dtype=complex), {"synthetic": True}
    def diagnostics(u):
        clock.advance(11, 0.7)
        return {"synthetic": True}
    monkeypatch.setattr(p, "validated_graph", validation)
    monkeypatch.setattr(p, "cayley_matrix", compiler)
    monkeypatch.setattr(p, "matrix_diagnostics", diagnostics)
    arm = p.prepare_arm(_mock_adjacency(), {"id": "mock"}, io.StringIO())
    assert parameters == list(p.CANDIDATES)
    assert arm["paid_wall"] == 29
    assert arm["compilation"]["wall_seconds"] == 24
    assert arm["excluded_matrix_diagnostics"]["wall_seconds"] == 88
    assert len({id(network["U"]) for network in arm["networks"]}) == 8
    assert {row["label"][0] for row in arm["paid_components"]} == {"preparation", "compilation"}
    assert sum(row["wall_seconds"] for row in arm["paid_components"]) == 29


def test_factory_prefix_and_counts_generation_have_separate_costs(monkeypatch):
    clock, arm = _VirtualClock(), _mock_arm()
    _patch_clock(monkeypatch, clock)
    actual_cut = p.base.cut
    def charged_cut(a, subset):
        clock.advance(2, 0.5)
        return actual_cut(a, subset)
    monkeypatch.setattr(p.base, "cut", charged_cut)
    def factory(u, source, model, seed):
        clock.advance(5, 3)
        def draw():
            clock.advance(8, 5)
            return _counts(source), False
        return draw, 4.0
    state = {"current": list(range(10)), "current_cut": 0, "best_cut": 0, "current_cuts": []}
    row = p.run_attempt(arm, state, 0, ("training", 0, 0, 0), 1, io.StringIO(),
                        factory=factory, coin_draw=lambda seed: 0.2)
    assert row["factory_accounting"]["classical_prefix_wall"] == 1
    assert row["factory_accounting"]["factory_total_cpu"] == 3
    assert row["factory_accounting"]["backend_cpu"] is None
    assert row["factory_accounting"]["classical_prefix_cpu"] is None
    assert row["excluded_count_generation"]["wall_seconds"] == 8
    assert row["postprocessing"]["wall_seconds"] == 4
    assert arm["paid_wall"] == 5


@pytest.mark.parametrize("values", [(5, 3, 6), (float("nan"), 1, 0), (1, -1, 0)])
def test_invalid_or_guessed_factory_clocks_are_rejected(values):
    with pytest.raises(p.RetainedFailure):
        p.factory_accounting(*values)


def test_fast_adapter_subtracts_cpu_and_gets_original_raw_only(monkeypatch):
    clock, raw = _VirtualClock(), np.array([[0, 1], [1, 0]], dtype=np.int64)
    _patch_clock(monkeypatch, clock)
    def seed(*parts):
        clock.advance(0.5, 0.25)
        return 6599002
    monkeypatch.setattr(p, "seed_for", seed)
    received = []
    def solve(a, **kwargs):
        assert a is raw
        received.append(kwargs)
        return _solver_result(budget=kwargs["cpu_budget_seconds"])
    monkeypatch.setattr(p.fast, "solve_from_raw", solve)
    row = p.fast_comparison(raw, "mock", 2.0, "random")
    assert row["adapter"]["cpu_seconds"] == 0.25
    assert row["solver_CPU_allowance"] == 1.75
    assert received == [{"seed": 6599002, "initialization": "random",
                         "cpu_budget_seconds": 1.75, "max_proposals": 10000}]
    assert row["other_arm_seconds_granted"] == 0 and not row["hardware_runtime_measured"]


def test_only_same_fixed_mode_both_cases_vetoes_and_failures_take_priority():
    mixed = _stage_rows(random=(9, 11), spectral=(11, 9))
    assert p.classify_stage1(mixed)["status"] == "STAGE1_OPTIONAL_CONTROLS_REQUIRED"
    rows = _stage_rows(random=(9, 10))
    result = p.classify_stage1(rows)
    assert result["status"] == "DEV_REJECTED_FIXED_FAST"
    assert result["fixed_FAST_veto_modes"] == ["random"]
    assert not result["positive_accepted"]
    assert set(result["optional_controls"].values()) == {"NOT_RUN_DUE_FAST_VETO"}
    failed = p.classify_stage1(rows, failed=True)
    assert failed["status"] == "INCONCLUSIVE_FIRST_FAILURE" and not failed["fixed_FAST_veto_modes"]
    assert p.classify_stage1(rows[:1])["status"] == "INCONCLUSIVE_FAST_ELIGIBILITY"


def test_fast_late_best_not_credited_and_early_cap_can_only_veto():
    late = p.fast_summary(_solver_result(timestamp=3.0, budget=2.0))
    assert not late["prefix_eligible_for_veto"] and late["best_cut"] is None
    early = p.fast_summary(_solver_result(best=9, early=True, scan=False))
    assert early["prefix_eligible_for_veto"] and not early["comparison_acceptance_eligible"]
    rows = _stage_rows()
    for row in rows: row["FAST"]["random"] = dict(early)
    assert p.classify_stage1(rows)["status"] == "DEV_REJECTED_FIXED_FAST"
    for row in rows: row["FAST"]["random"]["best_cut"] = 11
    assert p.classify_stage1(rows)["status"] == "INCONCLUSIVE_FAST_ELIGIBILITY"


def test_output_reserve_and_exclusive_writes_preserve_existing_data(tmp_path, monkeypatch):
    monkeypatch.setattr(p, "MAX_OUTPUT", 16)
    monkeypatch.setattr(p, "OUTPUT_RESERVE", 4)
    witness = tmp_path / "witness.txt"
    witness.write_text("x" * 13)
    with pytest.raises(p.RetainedFailure, match="reserve"):
        p.check_output(tmp_path)
    with pytest.raises(FileExistsError):
        p.save_json(witness, {"new": "data"})
    assert witness.read_text() == "x" * 13


def test_execute_metadata_first_failure_seals_raw_without_any_graph(tmp_path, monkeypatch):
    def fail(spec):
        raise p.RetainedFailure("synthetic metadata failure", {"payload": np.array([float("nan")])})
    def forbidden(*args, **kwargs):
        raise AssertionError("no graph/backend allowed after first metadata failure")
    monkeypatch.setattr(p, "seed_namespaces", fail)
    monkeypatch.setattr(p, "make_graph", forbidden)
    monkeypatch.setattr(p.base, "make_optical_sampler", forbidden)
    output = tmp_path / "fresh"
    result, failure = p.execute(p.read_spec(), output)
    assert result["status"] == "INCONCLUSIVE_FIRST_FAILURE" and failure["stage"] == "metadata"
    assert result["completed_B_shots"] == result["attempted_B_shots"] == 0
    assert not result["positive_accepted"] and result["actual_QPU_calls"] == 0
    with gzip.open(output / "raw.jsonl.gz", "rt") as raw_stream:
        raw = [json.loads(line) for line in raw_stream]
    assert raw[-1]["record_type"] == "first_failure"
    assert raw[-1]["evidence"]["payload"] == [{"nonfinite_float": "nan"}]
    assert json.loads((output / "failure.json").read_text())["failure"]["stage"] == "metadata"
    with pytest.raises(FileExistsError):
        p.execute(p.read_spec(), output)


def test_frozen_spec_byte_change_is_rejected(tmp_path):
    changed = tmp_path / "spec.json"
    changed.write_bytes(p.SPEC_PATH.read_bytes() + b" ")
    with pytest.raises(ValueError, match="spec bytes"):
        p.read_spec(changed)


def test_native_readback_guard_uses_official_interface():
    fake = SimpleNamespace(Config=SimpleNamespace(compute_max_thread_count=0))
    assert p.configure_native_threads(fake)["readback_before_work"] == 1
    fake.Config.compute_max_thread_count = 2
    with pytest.raises(p.RetainedFailure, match="maximum readback"):
        p.native_readback(fake)
