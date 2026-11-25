"""P63 stage-one qualification: synthetic fixtures only, never a DEV draw.

Authored statically. The sole native count fixture is the two-mode, two-photon
HOM case below. No test samples the 18-photon architecture or generates a graph.
"""
from fractions import Fraction
from contextlib import nullcontext
import importlib.util
import io
import itertools
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def p63():
    # Load only when the authorized qualification executes, not at collection.
    sys.path.insert(0, str(ROOT / "research"))
    spec = importlib.util.spec_from_file_location(
        "p63_stage_qualification", ROOT / "research/P63_spsa_fast_stage.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def toy_adjacency(np):
    return np.asarray([[0, 2, 0, 1], [2, 0, 3, 0],
                       [0, 3, 0, 4], [1, 0, 4, 0]], dtype=np.int64)


def scalar_cut(adjacency, subset):
    chosen = set(map(int, subset))
    return sum(int(adjacency[i, j])
               for i in range(len(adjacency))
               for j in range(i + 1, len(adjacency))
               if (i in chosen) != (j in chosen))


def theta_fixture():
    return tuple(Fraction(index - 4, 11) for index in range(10))


def result_fixture(best=11, *, scan=True, eligible=True, early_cap=False):
    return {
        "has_eligible_result": eligible,
        "best_cut": best if eligible else None,
        "best_subset": [0, 1] if eligible else None,
        "overall_completed_best_cut": 0,  # A late audit value is never credited.
        "comparison_acceptance_eligible": eligible and not early_cap,
        "first_scan_completed_before_deadline": scan,
        "early_cap_inconclusive": early_cap,
        "early_wall_inconclusive": False,
        "eligible_checkpoint_cpu_seconds": .5 if eligible else None,
        "cpu_budget_seconds": 1.,
        "best_snapshot_cached_online": eligible,
        "trace": {"cpu_seconds": []},
    }


def graph_record(p63, case, random_best=11, spectral_best=11, *, scan=True):
    return {
        "case": case,
        "B_paid_best": 10,
        "FAST": {
            "random": p63.fast_summary(result_fixture(random_best, scan=scan)),
            "spectral": p63.fast_summary(result_fixture(spectral_best, scan=scan)),
        },
    }


def test_fixed_architecture_parameters_and_prospective_seven_arm_seed_freeze(p63):
    assert (p63.N, p63.D, p63.K) == (18, 6, 9)
    assert tuple(p63.PARAMETERS) == tuple((b, i) for b in (1, 2) for i in range(1, 6))
    assert tuple(p63.ARMS) == (
        "bosonic", "j_aligned", "continuous_phase", "distinguishable",
        "independent_B_marginals", "uniform_subset", "phase_average",
    )
    frozen = json.loads((ROOT / "research/P63_spsa_fast_stage_spec.json").read_text())
    assert frozen == p63.expected_spec()
    assert len(frozen["cases"]) == 2
    assert [case["seed"] for case in frozen["cases"]] == [6301801, 6301802]
    assert [case["family"] for case in frozen["cases"]] == ["ER", "RR"]
    namespaces = p63.seed_namespaces(frozen)
    assert namespaces
    owners = {}
    for label, value in namespaces.items():
        assert type(value) is int and 0 <= value < 2**32
        assert value not in owners, (owners.get(value), label, value)
        owners[value] = label
    labels = "\n".join(map(str, namespaces))
    assert all(arm in labels for arm in p63.ARMS)
    assert "direction" in labels and "observation" in labels and "priority" in labels
    assert "random" in labels and "spectral" in labels
    assert p63.seed_for(6318000, "fixture", "embedding") == p63.seed_for(
        6318000, "fixture", "embedding"
    )
    assert p63.seed_for(6330000, "fixture", "+") != p63.seed_for(
        6330000, "fixture", "-"
    )


def test_matrix18_unitarity_fixed_q_and_full_source_means_without_sampling(p63):
    np = p63.np
    base = p63.compile_base()
    expected_q = np.full((18, 18), 1 / 18)
    expected_q[0] = np.repeat(np.asarray([1, 37, 37]) / 450, 6)
    expected_q[6] = np.repeat(np.asarray([49, 13, 13]) / 450, 6)
    for theta in ((Fraction(0),) * 10, theta_fixture()):
        u = p63.circuit(theta, base)
        assert u.shape == (18, 18)
        assert u.conj().T @ u == pytest.approx(np.eye(18), abs=3e-14)
        assert u @ u.conj().T == pytest.approx(np.eye(18), abs=3e-14)
        assert abs(u)**2 == pytest.approx(expected_q, abs=3e-15)
        diagnostics = p63.phase_matrix_diagnostics(u)
        assert diagnostics["q"] == pytest.approx(expected_q, abs=3e-15)
        for name in ("row_gram_residual", "column_gram_residual", "q_residual",
                     "row_mass_residual", "column_mass_residual"):
            assert diagnostics[name] <= 3e-12


def test_all_ten_output_generators_have_exact_three_mode_support(p63):
    np = p63.np
    base = p63.compile_base()
    u0 = p63.circuit((Fraction(0),) * 10, base)
    for index, (b, color) in enumerate(p63.PARAMETERS):
        theta = [Fraction(0)] * 10
        theta[index] = Fraction(2, 7)
        relative = p63.circuit(tuple(theta), base) @ u0.conj().T
        vector = np.zeros(18, dtype=complex)
        for a in range(3):
            vector[a * 6 + color] = np.exp(2j * np.pi * a * b / 3) / np.sqrt(3)
        expected = np.eye(18, dtype=complex) + (
            np.exp(2j / 7) - 1
        ) * np.outer(vector, vector.conj())
        assert relative == pytest.approx(expected, abs=3e-14)
        support = {a * 6 + color for a in range(3)}
        outside = sorted(set(range(18)) - support)
        assert relative[outside] == pytest.approx(np.eye(18)[outside], abs=3e-14)


def test_outside_counts_and_ALL_color_total_projectors_commute_jointly(p63):
    np = p63.np
    base = p63.compile_base()
    u0 = p63.circuit((Fraction(0),) * 10, base)
    u = p63.circuit(theta_fixture(), base)
    relative = u @ u0.conj().T
    assert u[[0, 6, 12]] == pytest.approx(u0[[0, 6, 12]], abs=3e-14)
    for color in range(6):
        diagonal = np.asarray([int(port % 6 == color) for port in range(18)])
        projector = np.diag(diagonal)
        assert relative @ projector == pytest.approx(projector @ relative, abs=3e-14)
    for port in (0, 6, 12):
        projector = np.zeros((18, 18), dtype=complex)
        projector[port, port] = 1
        assert relative @ projector == pytest.approx(projector @ relative, abs=3e-14)


def test_j_aligned_three_photon_columns_share_a_row_phase_at_every_j(p63):
    np = p63.np
    u = p63.circuit(theta_fixture(), p63.compile_base())
    reference = u[:, [0, 6, 12]]
    for j in range(6):
        diagonal = np.asarray([np.exp(2j * np.pi * (port % 6) * j / 6)
                               for port in range(18)])
        assert u[:, [j, 6 + j, 12 + j]] == pytest.approx(
            diagonal[:, None] * reference, abs=3e-14
        )


def test_c6_support_follows_input_cycle_and_rejects_collision_free18(p63):
    np = p63.np
    u = p63.circuit(theta_fixture(), p63.compile_base())
    columns = [b * 6 + (j + 1) % 6 for b in range(3) for j in range(6)]
    diagonal = np.asarray([np.exp(2j * np.pi * (port % 6) / 6)
                           for port in range(18)])
    assert u[:, columns] == pytest.approx(diagonal[:, None] * u, abs=3e-14)
    assert p63.c6_support(np.asarray([18] + [0] * 17, dtype=np.int64))
    assert not p63.c6_support(np.ones(18, dtype=np.int64))
    assert sum((port % 6) for port in range(18)) % 6 == 3


@pytest.mark.parametrize("bad", ["float", "bool", "negative", "wrong_total", "wrong_shape", "overflow"])
def test_c6_guard_never_casts_or_reconditions_invalid_counts(p63, bad):
    np = p63.np
    counts = np.asarray([18] + [0] * 17, dtype=np.int64)
    if bad == "float":
        counts = counts.astype(float)
    elif bad == "bool":
        counts = np.ones(18, dtype=bool)
    elif bad == "negative":
        counts[0], counts[1] = 19, -1
    elif bad == "wrong_total":
        counts[0] = 17
    elif bad == "wrong_shape":
        counts = counts[:-1]
    else:
        counts = np.zeros(18, dtype=np.uint64)
        counts[0], counts[6] = np.uint64(2**64 - 1), np.uint64(19)
    assert not p63.c6_support(counts)


def test_uniform_ties_are_exact_for_every_small_priority_order(p63):
    frequencies = {}
    for priority in itertools.permutations(range(4)):
        physical, vertices = p63.rank_counts([0, 0, 0, 0], priority, range(4))
        key = tuple(sorted(map(int, physical)))
        assert set(vertices) == set(physical) == set(priority[:2])
        frequencies[key] = frequencies.get(key, 0) + 1
    assert frequencies == {subset: 4 for subset in itertools.combinations(range(4), 2)}


def test_counts_are_ranked_before_mapping_and_carried_relabeling_preserves_cut(p63):
    np = p63.np
    adjacency = toy_adjacency(np)
    counts, priority, mapping = [2, 0, 2, 0], [2, 0, 3, 1], [3, 2, 0, 1]
    physical, vertices = p63.rank_counts(counts, priority, mapping)
    assert set(physical) == {0, 2} and set(vertices) == {0, 3}
    assert p63.base.cut(adjacency, vertices) == scalar_cut(adjacency, vertices) == 6
    relabel = np.asarray([2, 0, 3, 1])
    carried = np.zeros_like(adjacency)
    carried[np.ix_(relabel, relabel)] = adjacency
    other_physical, other_vertices = p63.rank_counts(counts, priority, relabel[mapping])
    assert set(other_physical) == set(physical)
    assert set(other_vertices) == set(relabel[list(vertices)])
    assert scalar_cut(carried, other_vertices) == scalar_cut(adjacency, vertices)


def test_paired_probes_share_ONE_delta_and_keep_exact_fraction_angles(p63):
    theta = theta_fixture()
    delta = tuple(1 if index % 2 else -1 for index in range(10))
    plus, minus = p63.paired_probes(theta, delta, Fraction(1, 4))
    assert all(isinstance(value, Fraction) for value in tuple(plus) + tuple(minus))
    for center, direction, right, left in zip(theta, delta, plus, minus):
        assert right == center + Fraction(1, 4) * direction
        assert left == center - Fraction(1, 4) * direction
        assert (right + left) / 2 == center
        assert right - left == Fraction(1, 2) * direction


def test_spsa_uses_ALL_four_normalized_losses_and_minimizes_without_incumbent_clipping(p63):
    theta, delta = (Fraction(0),) * 10, (1, -1) * 5
    plus, minus = [0, 10, 10, 10], [4, 4, 4, 4]
    assert p63.normalized_batch_loss(plus, 10) == Fraction(3, 4)
    assert p63.normalized_batch_loss(minus, 10) == Fraction(2, 5)
    next_theta, gradient, plus_loss, minus_loss = p63.spsa_update(
        theta, delta, plus, minus, 10
    )
    assert (plus_loss, minus_loss) == (Fraction(3, 4), Fraction(2, 5))
    assert tuple(gradient) == tuple(Fraction(7, 10) * direction for direction in delta)
    assert tuple(next_theta) == tuple(-Fraction(7, 20) * direction for direction in delta)
    assert all(isinstance(value, Fraction) for value in tuple(next_theta) + tuple(gradient))


def test_extreme_loss_bounds_are_coordinatewise_and_zero_weight_normalization_fails(p63):
    theta, delta = (Fraction(0),) * 10, (1,) * 10
    for step in range(3):
        probes = p63.paired_probes(theta, delta, Fraction(1, 4))
        assert max(abs(value) for probe in probes for value in probe) <= Fraction(9, 4)
        theta, gradient, _, _ = p63.spsa_update(theta, delta, [10] * 4, [0] * 4, 10)
        assert max(abs(value) for value in gradient) == 2
        assert max(abs(value) for value in theta) == step + 1
    assert max(abs(value) for value in theta) == 3
    with pytest.raises((ValueError, p63.RetainedFailure)):
        p63.normalized_batch_loss([0] * 4, 0)


def test_TWO_mocked_trajectories_pay80_shots_and_freeze_FINAL_theta_before16_fresh_each(p63, monkeypatch):
    calls, guard_calls, direction_seeds = [], [], []
    stream = io.StringIO()
    base_matrices = object()
    class FixedDirectionGenerator:
        def __init__(self, seed):
            direction_seeds.append(seed)
        def integers(self, low, high, size):
            assert (low, high, size) == (0, 2, 10)
            return p63.np.asarray([0, 1] * 5, dtype=p63.np.int64)
    monkeypatch.setattr(p63.np.random, "PCG64", lambda seed: seed)
    monkeypatch.setattr(p63.np.random, "Generator", FixedDirectionGenerator)
    def fake_batch(arm, theta, label, draws, target, matrices):
        assert matrices is base_matrices and target is stream
        stage, step, sign, trial = label
        if stage == "training":
            assert draws == 4 and trial == 0
            plus, minus = (([0, 10, 10, 10], [4] * 4),
                           ([1] * 4, [9] * 4), ([10] * 4, [0] * 4))[step]
            cuts = plus if sign == "plus" else minus
        else:
            assert (stage, step, sign) == ("evaluation", 3, "final")
            assert draws == 8 and trial in (0, 1)
            cuts = [9] * 8
        calls.append({"case": arm["case"], "theta": tuple(theta), "label": label,
                      "draws": draws, "cuts": list(cuts)})
        target.write(json.dumps({"record_type": "fixture_batch", "case": arm["case"],
                                 "stage": stage}) + "\n")
        arm["completed_shots"] += draws
        current = min(cuts)
        if arm["paid_best"] is None or current < arm["paid_best"]["cut"]:
            arm["paid_best"] = {"cut": current, "stage": stage}
        return {"stage": stage, "cuts": list(cuts), "proposals": draws, "theta": tuple(theta)}
    monkeypatch.setattr(p63, "run_batch", fake_batch)
    results = []
    for case in ("qualification_trajectory_A", "qualification_trajectory_B"):
        arm = {"case": case, "denominator": 10, "paid_wall": 0.,
               "completed_shots": 0, "paid_best": None}
        results.append(p63.run_trajectory(arm, stream, base_matrices,
                                         lambda: guard_calls.append(case)))
    assert len(calls) == 16 and len(guard_calls) == 16
    assert len(direction_seeds) == len(set(direction_seeds)) == 6
    assert sum(row["draws"] for row in calls) == 80
    assert sum(result["completed_shots"] for result in results) == 80
    events = [json.loads(line) for line in stream.getvalue().splitlines()]
    for result in results:
        own = [row for row in calls if row["case"] == result["case"]]
        assert [row["label"] for row in own] == [
            ("training", step, sign, 0) for step in range(3) for sign in ("plus", "minus")
        ] + [("evaluation", 3, "final", trial) for trial in (0, 1)]
        assert sum(row["draws"] for row in own[:6]) == 24
        assert sum(row["draws"] for row in own[6:]) == 16
        assert len(result["trajectory"]) == 3 and result["B_paid_best"] == 0
        assert result["B_paid_best_record"]["stage"] == "training"
        assert result["B_fresh_normalized_mean"] == Fraction(9, 10)
        assert tuple(result["theta_final"]) == tuple(result["trajectory"][-1]["theta_after"])
        assert all(tuple(row["theta"]) == tuple(result["theta_final"]) for row in own[6:])
        for step, item in enumerate(result["trajectory"]):
            plus, minus = own[2 * step:2 * step + 2]
            for center, direction, right, left in zip(
                    item["theta_before"], item["delta"], plus["theta"], minus["theta"]):
                assert right == center + Fraction(direction, 4)
                assert left == center - Fraction(direction, 4)
        frozen_index = next(index for index, event in enumerate(events)
                            if event["case"] == result["case"]
                            and event["record_type"] == "frozen_final_theta")
        fresh_index = next(index for index, event in enumerate(events)
                           if event["case"] == result["case"]
                           and event["record_type"] == "fixture_batch"
                           and event["stage"] == "evaluation")
        assert frozen_index < fresh_index
        assert events[frozen_index]["selected_iterate"] == 3
        assert events[frozen_index]["frozen_before_fresh"]


def synthetic_batch_arm(p63, case):
    # A hardcoded one-edge fixture, not a generated DEV graph or a source draw.
    adjacency = p63.np.zeros((18, 18), dtype=p63.np.int64)
    adjacency[0, 1] = adjacency[1, 0] = 10
    return {"case": case, "a": adjacency, "denominator": 10, "mapping": list(range(18)),
            "networks": {}, "paid_wall": 0., "paid_best": None,
            "attempted_shots": 0, "completed_shots": 0}


def stub_priority_generators(p63, monkeypatch):
    seeds = []
    class FixedPriorityGenerator:
        def __init__(self, seed):
            seeds.append(seed)
        def permutation(self, size):
            assert size == 18
            return p63.np.arange(size, dtype=p63.np.int64)
    monkeypatch.setattr(p63.np.random, "PCG64", lambda seed: seed)
    monkeypatch.setattr(p63.np.random, "Generator", FixedPriorityGenerator)
    return seeds


def test_mock_factory_batches_keep_full_counts_and_cache_ONLY_their_private_exact_theta(p63, monkeypatch):
    np = p63.np
    priority_seeds = stub_priority_generators(p63, monkeypatch)
    compilations, diagnostics, factories, source_draws = [], [], [], []
    def circuit(theta, matrices):
        compilations.append(tuple(theta))
        return np.eye(18, dtype=complex)
    def diagnostic(matrix):
        diagnostics.append(matrix)
        return {"mock_physics_diagnostic": True}
    def factory(unitary, source, model, seed):
        factories.append((unitary, tuple(source), model, seed))
        def primitive():
            source_draws.append(1)
            return np.asarray([18] + [0] * 17, dtype=np.int64), False
        return primitive, 0.
    monkeypatch.setattr(p63, "circuit", circuit)
    monkeypatch.setattr(p63, "phase_matrix_diagnostics", diagnostic)
    monkeypatch.setattr(p63.base, "make_optical_sampler", factory)
    arm = synthetic_batch_arm(p63, "qualification_batch_cache")
    theta, stream = (Fraction(0),) * 10, io.StringIO()
    for trial in (0, 1):
        record = p63.run_batch(arm, theta, ("evaluation", 3, "final", trial), 8, stream, object())
        assert record["proposals"] == 8 and len(record["cuts"]) == 8
    assert len(compilations) == len(diagnostics) == len(arm["networks"]) == 1
    assert len(factories) == 2 and len(source_draws) == arm["completed_shots"] == 16
    assert arm["attempted_shots"] == 16
    assert len(priority_seeds) == len(set(priority_seeds)) == 16
    assert factories[0][3] != factories[1][3]
    assert all(source == tuple(range(18)) and model == "bosonic"
               for _, source, model, _ in factories)
    events = [json.loads(line) for line in stream.getvalue().splitlines()]
    assert sum(row["record_type"] == "network" for row in events) == 1
    shots = [row for row in events if row["record_type"] == "shot"]
    assert len(shots) == 16
    assert all(row["counts"] == [18] + [0] * 17 and row["collision"] for row in shots)
    assert all(len(row["subset"]) == 9 and row["C6_residue"] == 0 for row in shots)
    other = synthetic_batch_arm(p63, "qualification_batch_other_case")
    p63.run_batch(other, theta, ("training", 0, "plus", 0), 4, io.StringIO(), object())
    assert len(compilations) == 2 and len(other["networks"]) == 1
    assert other["networks"] is not arm["networks"]


def test_invalid_second_mock_count_is_retained_after_first_shot_without_retry(p63, monkeypatch):
    np = p63.np
    priority_seeds = stub_priority_generators(p63, monkeypatch)
    calls = []
    monkeypatch.setattr(p63, "circuit", lambda *args: np.eye(18, dtype=complex))
    monkeypatch.setattr(p63, "phase_matrix_diagnostics", lambda matrix: {"mock": True})
    def factory(*args):
        def primitive():
            calls.append(1)
            counts = [18] + [0] * 17 if len(calls) == 1 else [1] * 18
            return np.asarray(counts, dtype=np.int64), False
        return primitive, 0.
    monkeypatch.setattr(p63.base, "make_optical_sampler", factory)
    arm, stream = synthetic_batch_arm(p63, "qualification_batch_failure"), io.StringIO()
    with pytest.raises(p63.RetainedFailure) as caught:
        p63.run_batch(arm, (Fraction(0),) * 10, ("training", 0, "plus", 0), 4, stream, object())
    assert len(calls) == arm["attempted_shots"] == 2 and arm["completed_shots"] == 1
    assert len(priority_seeds) == 1
    assert len(caught.value.evidence["completed_cuts"]) == 1
    assert caught.value.evidence["counts"].tolist() == [1] * 18
    events = [json.loads(line) for line in stream.getvalue().splitlines()]
    assert sum(row["record_type"] == "shot" for row in events) == 1
    assert sum(row["record_type"] == "shot_requested" for row in events) == 2
    assert events[-1]["record_type"] == "failed_batch"
    assert events[-1]["counts"] == [1] * 18


def test_factory_preclock_prefix_is_paid_and_diagnostics_are_excluded_with_CPU_unknown(p63):
    accounting = p63.factory_setup_accounting(9., 6., 5., 0.)
    assert accounting["classical_wall"] == 4.
    assert accounting["factory_total_cpu"] == 6.
    assert accounting["backend_cpu"] is None
    assert not accounting["CPU_split_available"]
    diagnostics_excluded = p63.factory_setup_accounting(9., 6., 5., 1.)
    assert diagnostics_excluded["classical_wall"] == 3.
    assert diagnostics_excluded["backend_cpu"] is None


@pytest.mark.parametrize("times", [(1., 1., 2., 0.), (3., 1., 2., 2.),
                                   (float("nan"), 1., 0., 0.)])
def test_invalid_nested_timers_are_retained_failures_not_free_negative_cost(p63, times):
    with pytest.raises((ValueError, p63.RetainedFailure)):
        p63.factory_setup_accounting(*times)


def test_native_threads_are_set_and_verified_before_factory_and_after_work(p63):
    xq = SimpleNamespace(Config=SimpleNamespace(compute_max_thread_count=8))
    receipt = p63.configure_native_threads(xq)
    assert receipt["before"] == 8 and receipt["configured_before_work"] == 1
    assert p63.native_thread_readback(xq) == 1
    xq.Config.compute_max_thread_count = 2
    with pytest.raises(p63.RetainedFailure):
        p63.native_thread_readback(xq)


def test_only_native_count_fixture_is_two_photon_HOM_no18_draw(p63):
    np = p63.np
    import exqalibur as xq
    p63.configure_native_threads(xq)
    unitary = np.asarray([[1., 1.], [1., -1.]]) / math.sqrt(2)
    primitive, backend_wall = p63.base.make_optical_sampler(
        unitary, [0, 1], "bosonic", p63.seed_for(6399000, "qualification", "HOM2")
    )
    assert backend_wall >= 0
    for _ in range(8):
        counts, fallback = primitive()
        assert not fallback and counts.dtype.kind in "iu"
        assert tuple(map(int, counts)) in {(2, 0), (0, 2)}
    assert p63.native_thread_readback(xq) == 1


def test_small_bunched_PNR_normalization_requires_BOTH_input_and_output_factorials():
    # Integer entries before the common 1/sqrt(2) Hadamard normalization.
    # A two-photon permanent has common scale 1/2, hence squared scale 1/4.
    integer_hadamard = ((1, 1), (1, -1))
    outcomes = ((2, 0), (1, 1), (0, 2))
    for inputs, expected in (
        ((2, 0), [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)]),
        ((1, 1), [Fraction(1, 2), Fraction(0), Fraction(1, 2)]),
    ):
        columns = [mode for mode, count in enumerate(inputs) for _ in range(count)]
        probabilities = []
        for output in outcomes:
            rows = [mode for mode, count in enumerate(output) for _ in range(count)]
            repeated = [[integer_hadamard[row][column] for column in columns] for row in rows]
            permanent = repeated[0][0] * repeated[1][1] + repeated[0][1] * repeated[1][0]
            denominator = (4 * math.prod(math.factorial(value) for value in inputs)
                           * math.prod(math.factorial(value) for value in output))
            probabilities.append(Fraction(permanent**2, denominator))
        assert probabilities == expected and sum(probabilities) == 1


def test_FAST_late_audit_best_is_never_an_eligible_incumbent(p63):
    summary = p63.fast_summary(result_fixture(eligible=False))
    assert summary["best_cut"] is None
    assert not summary["prefix_eligible_for_veto"]
    assert not summary["comparison_acceptance_eligible"]


@pytest.mark.parametrize("invalid", ["late", "nonfinite", "missing", "uncached"])
def test_FAST_helper_flags_do_not_override_deadline_or_online_snapshot_evidence(p63, invalid):
    result = result_fixture(0)
    if invalid == "late":
        result["eligible_checkpoint_cpu_seconds"] = 1.25
    elif invalid == "nonfinite":
        result["eligible_checkpoint_cpu_seconds"] = float("nan")
    elif invalid == "missing":
        result["eligible_checkpoint_cpu_seconds"] = None
    else:
        result["best_snapshot_cached_online"] = False
    summary = p63.fast_summary(result)
    assert summary["best_cut"] is None
    assert not summary["prefix_eligible_for_veto"]
    assert not summary["comparison_acceptance_eligible"]


def test_FAST_timely_initialization_can_refute_without_first_scan_but_never_pass_gate(p63):
    summary = p63.fast_summary(result_fixture(10, scan=False))
    assert summary["best_cut"] == 10 and summary["prefix_eligible_for_veto"]
    assert not summary["comparison_acceptance_eligible"]
    records = [graph_record(p63, case, 10, 11, scan=False) for case in ("toy_a", "toy_b")]
    verdict = p63.classify_stage1(records)
    assert verdict["status"] == "DEV_REJECTED_FIXED_FAST" and not verdict["positive_accepted"]


def test_FIXED_FAST_veto_requires_same_mode_on_BOTH_cases_not_free_portfolio(p63):
    mixed = [graph_record(p63, "toy_a", 9, 11), graph_record(p63, "toy_b", 11, 9)]
    verdict = p63.classify_stage1(mixed)
    assert verdict["status"] == "STAGE1_OPTIONAL_CONTROLS_REQUIRED"
    assert not verdict["positive_accepted"]
    mixed[1]["FAST"]["random"] = p63.fast_summary(result_fixture(10))
    rejected = p63.classify_stage1(mixed)
    assert rejected["status"] == "DEV_REJECTED_FIXED_FAST"
    assert not rejected["positive_accepted"]
    assert set(rejected["optional_models"].values()) == {"NOT_RUN_DUE_FAST_VETO"}


@pytest.mark.parametrize("scenario", ["missing_result", "no_scan", "early_cap"])
def test_survival_with_ineligible_FAST_is_inconclusive_and_accepts_no_positive(p63, scenario):
    records = [graph_record(p63, case) for case in ("toy_a", "toy_b")]
    records[1]["FAST"]["spectral"] = p63.fast_summary(result_fixture(
        eligible=scenario != "missing_result", scan=scenario != "no_scan",
        early_cap=scenario == "early_cap"
    ))
    verdict = p63.classify_stage1(records)
    assert verdict["status"] == "INCONCLUSIVE_FAST_ELIGIBILITY"
    assert not verdict["positive_accepted"]


@pytest.mark.parametrize("missing", ["case", "unique_case", "mode"])
def test_missing_or_duplicate_fixed_FAST_call_structure_is_never_a_completed_gate(p63, missing):
    records = [graph_record(p63, case, 9, 9) for case in ("toy_a", "toy_b")]
    if missing == "case":
        records.pop()
    elif missing == "unique_case":
        records[1]["case"] = records[0]["case"]
    else:
        del records[1]["FAST"]["spectral"]
    verdict = p63.classify_stage1(records)
    assert verdict["status"] == "INCONCLUSIVE_FAST_ELIGIBILITY"
    assert not verdict["positive_accepted"]


def test_virtual_FAST_timestamps_keep_late_initialization_out_of_prefix(p63, monkeypatch):
    class TickClock:
        def __init__(self):
            self.now = -1.
        def __call__(self):
            self.now += 1.
            return self.now, self.now
    monkeypatch.setattr(p63.fast, "_clock", TickClock())
    result = p63.fast.solve_from_raw(
        toy_adjacency(p63.np), seed=6399001, initialization="random",
        cpu_budget_seconds=1.5, max_proposals=1000
    )
    assert result["initial_cut"] is not None
    assert result["trace"]["cpu_seconds"].tolist() == [2.]
    summary = p63.fast_summary(result)
    assert summary["best_cut"] is None and not summary["prefix_eligible_for_veto"]
    assert not summary["comparison_acceptance_eligible"]


@pytest.mark.parametrize("mode", ["random", "spectral"])
@pytest.mark.parametrize("allowance,expected", [(2., 1.75), (.1, 0.)])
def test_FAST_adapter_subtracts_OWN_CPU_and_passes_ONLY_original_raw_graph(p63, monkeypatch, mode, allowance, expected):
    raw = toy_adjacency(p63.np)
    before, seen = raw.copy(), []
    class AdapterMeter:
        wall, cpu = .4, .25
        def measure(self):
            return nullcontext()
        def record(self):
            return {"wall_seconds": self.wall, "cpu_seconds": self.cpu}
    def solve(adjacency, **kwargs):
        assert adjacency is raw
        seen.append(kwargs)
        result = result_fixture(eligible=expected > 0)
        result["cpu_budget_seconds"] = kwargs["cpu_budget_seconds"]
        return result
    monkeypatch.setattr(p63, "Meter", AdapterMeter)
    monkeypatch.setattr(p63.fast, "solve_from_raw", solve)
    comparison = p63.fast_comparison(raw, "qualification_FAST_adapter", allowance, mode)
    assert p63.np.array_equal(raw, before)
    assert len(seen) == 1
    assert set(seen[0]) == {"seed", "initialization", "cpu_budget_seconds", "max_proposals"}
    assert seen[0]["initialization"] == mode
    assert seen[0]["cpu_budget_seconds"] == expected
    assert seen[0]["max_proposals"] == p63.FAST_MAX_PROPOSALS == 10000
    assert seen[0]["seed"] == p63.seed_for(p63.NAMESPACES["FAST"], "qualification_FAST_adapter", mode)
    assert comparison["B_classical_WALL_allowance"] == allowance
    assert comparison["solver_CPU_allowance"] == expected
    assert comparison["adapter"] == {"wall_seconds": .4, "cpu_seconds": .25}
    assert comparison["serialization_granted_seconds"] == comparison["other_arm_seconds_granted"] == 0
    assert comparison["optical_latency_assumed_seconds"] == 0 and not comparison["hardware_time_measured"]
    assert comparison["prefix_eligible_for_veto"] == (expected > 0)


def test_first_failure_preserves_partial_evidence_and_never_overwrites_it(p63, tmp_path):
    partial = {"completed_shots": 1, "cuts": [6], "counts": [18] + [0] * 17,
               "theta": ["0"] * 10, "record_type": "synthetic_partial"}
    error = p63.RetainedFailure("synthetic first failure", {"failing_shot": 1})
    p63.write_failure(tmp_path, "qualification_fixture", error, partial)
    failure_path = tmp_path / "failure.json"
    frozen = failure_path.read_bytes()
    failure = json.loads(frozen)
    assert failure["stage"] == "qualification_fixture"
    assert failure["partial"] == partial
    assert failure["failure"]["message"] == "synthetic first failure"
    assert failure["failure"]["evidence"] == {"failing_shot": 1}
    with pytest.raises(FileExistsError):
        p63.write_failure(tmp_path, "replacement_forbidden", error, {})
    assert failure_path.read_bytes() == frozen
