"""Synthetic-only auditor qualification: no main role hashes, RNG or native API."""
from copy import deepcopy
from fractions import Fraction
import importlib.util
import json
import math
from pathlib import Path

import pytest


PATH = Path(__file__).resolve().parents[1] / "research/P82a_independent_raw_audit.py"
SPEC = importlib.util.spec_from_file_location("p82a_recorded_checker_fixture", PATH)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def toy_graph():
    return [[0, 0, 1, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]


def toy_scores():
    return [
        {"sequence": 0, "mask_hex": "03", "cut": 1, "method": "scalar_cut"},
        {"sequence": 1, "mask_hex": "09", "cut": 1, "method": "exact_swap_delta",
         "batch": 1, "batch_index": 0, "removed": 0, "added": 2},
        {"sequence": 2, "mask_hex": "05", "cut": 0, "method": "exact_swap_delta",
         "batch": 1, "batch_index": 1, "removed": 0, "added": 3},
        {"sequence": 3, "mask_hex": "05", "cut": 0, "method": "exact_swap_delta",
         "batch": 1, "batch_index": 2, "removed": 1, "added": 2},
        {"sequence": 4, "mask_hex": "09", "cut": 1, "method": "exact_swap_delta",
         "batch": 1, "batch_index": 3, "removed": 1, "added": 3},
    ]


def z(value):
    return {"real": value.real, "imag": value.imag}


def checkpoints():
    return [
        {"index": 0, "stage": "initialization", "work": 0, "cpu_seconds": 0.1,
         "wall_seconds": 0.1, "cut": 1, "mask_hex": "03"},
        {"index": 1, "stage": "initial_scan", "work": 1, "cpu_seconds": 0.2,
         "wall_seconds": 5.0, "cut": 0, "mask_hex": "05"},
    ]


def ledger_fixture():
    common = {"case": "toy", "context": {}}
    direct = {**common, "id": "toy/1", "kind": "OBSERVED_SPAN", "paid": True,
              "label": "case_private_setup", "start_cpu": 0.0, "end_cpu": 1.0,
              "start_wall": 0.0, "end_wall": 1.0, "cpu_seconds": 1.0, "wall_seconds": 1.0}
    outer = {**common, "id": "toy/2", "kind": "OBSERVED_SPAN", "paid": False,
             "label": "factory_total", "start_cpu": 1.0, "end_cpu": 5.0,
             "start_wall": 1.0, "end_wall": 7.0, "cpu_seconds": 4.0, "wall_seconds": 6.0}
    reported = {"case": "toy", "id": "toy/3", "kind": "REPORTED_DURATION", "paid": False,
                "label": "P43_backend_setup_reported", "wall_seconds": 4.0, "cpu_seconds": None,
                "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
                "helper_source_path": "research/P43_global_gain_probe.py",
                "helper_source_sha256": audit.P43_SHA, "outer_ref": "toy/2"}
    difference = {"case": "toy", "id": "toy/4", "kind": "DURATION_DIFF", "paid": True,
                  "label": "factory_prefix_plus_return_residual", "wall_seconds": 2.0,
                  "cpu_seconds": None, "start_cpu": None, "end_cpu": None,
                  "start_wall": None, "end_wall": None, "outer_ref": "toy/2", "reported_ref": "toy/3",
                  "reported_setup_wall_seconds": 4.0, "formula": "factory_outer_wall - setup_reported_wall"}
    return [direct, outer, reported, difference]


def test_integer_cut_canonical_and_no_weighted_degree_assumption():
    graph = audit.graph_checked(toy_graph())
    assert audit.integer_cut(graph, 3) == 1
    assert audit.integer_cut(graph, 5) == 0
    assert audit.integer_cut(graph, 3 ^ 15) == 1
    assert audit.orient(3, [3, 1, 0, 2]) == 12
    with pytest.raises(audit.AuditIssue):
        audit.graph_checked([[0, True], [True, 0]])


def test_masks_validate_balance_padding_and_little_order():
    assert audit.mask_read("03", 4) == 3
    assert audit.mask_hex(5, 4) == "05"
    with pytest.raises(audit.AuditIssue):
        audit.mask_read("1f04", 10)
    with pytest.raises(audit.AuditIssue):
        audit.mask_read("01", 4)


def test_rank_order_enumerates_every_neighbor_including_duplicates():
    assert audit.swap_list(toy_graph(), 3, [0, 1, 2, 3]) == [
        (0, 2, 9), (0, 3, 5), (1, 2, 5), (1, 3, 9)]


def test_quench_is_best_scored_not_last_and_not_local_certificate():
    result = audit.descent_check(toy_graph(), [0, 1, 2, 3], toy_scores(), 3, 1, "toy")
    assert result == {"subset": [0, 2], "cut": 0, "scans": 1, "local_optimum": False}
    assert toy_scores()[-1]["cut"] == 1


def test_quench_rejects_missing_neighbor_and_false_recorded_cut():
    with pytest.raises(audit.AuditIssue):
        audit.descent_check(toy_graph(), [0, 1, 2, 3], toy_scores()[:-1], 3, 1, "toy")
    rows = toy_scores()
    rows[2]["cut"] = 1
    with pytest.raises(audit.AuditIssue):
        audit.descent_check(toy_graph(), [0, 1, 2, 3], rows, 3, 1, "toy")


def test_fraction_features_are_independent_exact_F4_arithmetic():
    graph = [[0] * 16 for _ in range(16)]  # literal synthetic one-edge fixture, not DEV
    graph[8][9] = graph[9][8] = 5
    a, q, j = audit.exact_features(graph, list(range(8, 16)),
        [Fraction(1, 2), Fraction(5, 6), Fraction(7, 6), Fraction(3, 2)])
    assert a[0][0] == (1, 0)
    assert a[0][1] == (Fraction(-1, 6), Fraction(1, 6))
    assert q[0][1] == 5
    assert j[0][1] == Fraction(5, 18)


def test_actual_rounded_tiny_H_is_not_replaced_by_theoretical_zero():
    tiny = 1e-300
    h0 = complex(0, tiny)
    a0 = complex(math.cos(math.atan2(h0.imag, h0.real)), math.sin(math.atan2(h0.imag, h0.real)))
    h1 = tiny * a0
    a1 = complex(math.cos(math.atan2(h1.imag, h1.real)), math.sin(math.atan2(h1.imag, h1.real)))
    rows = [{"sweep": 0, "coordinate": 0, "before": z(1 + 0j), "H": z(h0), "after": z(a0)},
            {"sweep": 0, "coordinate": 1, "before": z(1j), "H": z(h1), "after": z(a1)}]
    assert abs(audit.phase_trace_check([[0, tiny], [tiny, 0]], [0, 1], rows, sweeps=1)[0] - 1j) < 1e-12
    rows[0]["H"] = z(0j)
    with pytest.raises(audit.AuditIssue):
        audit.phase_trace_check([[0, tiny], [tiny, 0]], [0, 1], rows, sweeps=1)


def test_eta_zero_trace_requires_exact_zero_and_unchanged_roots():
    roots = [-1 + 0j, -1j]
    rows = [{"sweep": sweep, "coordinate": r, "before": z(roots[r]),
             "H": z(0j), "after": z(roots[r])} for sweep in range(2) for r in range(2)]
    assert audit.phase_trace_check([[0, 0], [0, 0]], [2, 3], rows, analytic_zero=True) == roots
    rows[0]["H"] = z(1e-300j)
    with pytest.raises(audit.AuditIssue):
        audit.phase_trace_check([[0, 0], [0, 0]], [2, 3], rows, analytic_zero=True)


def test_full_counts_collisions_and_scripted_repair():
    record = {"repair": [6], "repair_rng_used": True, "full_counts": [0, 0, 1, 1, 2, 0, 0, 0],
              "vertex_counts": [0, 0, 1, 1, 2, 0, 0, 0], "subset": [2, 3, 4, 6],
              "R": [0, 1], "r": 2, "h": 1}
    calls = []
    def fill(available, count):
        calls.append((available, count))
        return [6]
    assert audit.decoded_check([0, 1, 2, 3], [4, 5, 6, 7], [0, 1], [2, 0, 0, 0], record, fill) == 92
    assert calls == [([5, 6, 7], 1)]
    with pytest.raises(audit.AuditIssue):
        audit.decoded_check([0, 1, 2, 3], [4, 5, 6, 7], [0, 1], [1, 0, 0, 0], record, fill)


def test_zero_full_transfer_do_not_consume_repair_coins():
    def forbidden(*args):
        pytest.fail("deterministic branch invoked repair")
    zero = {"repair": [], "repair_rng_used": False, "full_counts": [1, 1, 0, 0],
            "vertex_counts": [1, 1, 0, 0], "subset": [0, 1], "R": [], "r": 0, "h": 0}
    full = {"repair": [3], "repair_rng_used": False, "full_counts": [0, 0, 2, 0],
            "vertex_counts": [0, 0, 2, 0], "subset": [2, 3], "R": [0, 1], "r": 2, "h": 1}
    assert audit.decoded_check([0, 1], [2, 3], [], [0, 0], zero, forbidden) == 3
    assert audit.decoded_check([0, 1], [2, 3], [0, 1], [2, 0], full, forbidden) == 12


def test_null_fill_exact_small_identity_all_cardinalities():
    for k in range(1, 5):
        for r in range(k + 1):
            for h in range(r + 1):
                assert audit.null_fill_identity(k, r, h) == Fraction(1, math.comb(k, r))


def test_factory_typed_operands_and_unknown_cpu_sum_only_once():
    result = audit.grant_audit(ledger_fixture(), "toy", True)
    assert result["grant"] == 3
    assert result["known_direct_paid_cpu"] == 1
    assert result["factory_cpu_allocation"] is None
    assert result["paid_ids"] == ["toy/1", "toy/4"]


def test_factory_ref_endpoints_and_double_count_fail():
    rows = ledger_fixture()
    rows[2]["start_wall"] = 1.0
    with pytest.raises(audit.AuditIssue):
        audit.grant_audit(rows, "toy", True)
    rows = ledger_fixture()
    repeated = deepcopy(rows[-1])
    repeated["id"] = "toy/5"
    rows.append(repeated)
    with pytest.raises(audit.AuditIssue):
        audit.grant_audit(rows, "toy", True)
    rows = ledger_fixture()
    rows[2]["wall_seconds"] = 7.0
    with pytest.raises(audit.AuditIssue):
        audit.grant_audit(rows, "toy", True)


def test_gap_charges_both_domains_without_inventing_endpoints():
    assert audit.duration_gap((8, 9), (1, 2), (5, 4)) == (2, 3)
    with pytest.raises(audit.AuditIssue):
        audit.duration_gap((1, 1), (1, 1), (1, 1))


def test_dual_clock_chooses_latest_existing_timely_not_later_cheapest():
    selected, first = audit.select_checkpoint(checkpoints(), 0.1, 0.1, 1, toy_graph())
    assert selected["index"] == 0 and selected["cut"] == 1
    assert first is False


def test_conservative_call_gap_can_only_remove_direct_witness():
    rows = checkpoints()
    rows[1]["cpu_seconds"] = rows[1]["wall_seconds"] = 0.5
    direct, _ = audit.select_checkpoint(rows, 0.1, 0.1, 1, toy_graph())
    charged, first = audit.select_checkpoint(rows, 0.7, 0.7, 1, toy_graph())
    assert direct["index"] == 1
    assert charged["index"] == 0 and not first


def test_nonmonotone_trace_and_custom_wrong_cached_lineage_fail():
    rows = checkpoints()
    rows[1]["cpu_seconds"] = 0.01
    with pytest.raises(audit.AuditIssue):
        audit.select_checkpoint(rows, 0, 0, 1, toy_graph())
    scores = [{"work": 1, "cut": 1, "mask_hex": "03"}, {"work": 2, "cut": 0, "mask_hex": "05"}]
    custom = [{"index": 0, "stage": "initialization", "work": 1, "cpu_seconds": 0.1, "wall_seconds": 0.1,
               "cached_best": {"cut": 1, "mask_hex": "03"}},
              {"index": 1, "stage": "initial_scan", "work": 2, "cpu_seconds": 0.2, "wall_seconds": 0.2,
               "cached_best": {"cut": 0, "mask_hex": "05"}}]
    assert audit.select_checkpoint(custom, 0, 0, 1, toy_graph(), True, scores)[0]["index"] == 1
    custom[1]["cached_best"] = {"cut": 1, "mask_hex": "09"}
    with pytest.raises(audit.AuditIssue):
        audit.select_checkpoint(custom, 0, 0, 1, toy_graph(), True, scores)


def test_same_fixed_mode_both_anchors_not_per_graph_portfolio():
    b = {case: {"all_paid_best": {"cut": 10}} for case in audit.CASES}
    panel = [{"mode": mode, "case": case, "normal_return": True,
              "selected": {"cut": 9 if (mode, case) in ((audit.FAST[0], audit.CASES[0]),
                                                       (audit.FAST[1], audit.CASES[1])) else 11}}
             for mode in audit.FAST for case in audit.CASES]
    assert audit.fixed_winner(panel, b, audit.FAST) is None
    panel[1]["selected"]["cut"] = 9
    assert audit.fixed_winner(panel, b, audit.FAST) == "FAST_RANDOM"


def test_json_duplicate_nonfinite_and_scalar_types_fail():
    for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1e999}'):
        with pytest.raises(audit.AuditIssue):
            audit.decode_json(raw, "synthetic")
    with pytest.raises(audit.AuditIssue):
        audit.integer(True, "synthetic")


def test_unbound_or_wrong_token_rejects_before_any_main_replay(monkeypatch):
    def forbidden(*args):
        pytest.fail("qualification reached numerical import/version boundary")
    monkeypatch.setattr(audit.importlib.metadata, "version", forbidden)
    with pytest.raises(audit.AuditIssue):
        audit.authorize_binding({"schema": "P82a.independent-recorded-audit-binding.v1",
                                 "binding_state": "TEMPLATE_UNBOUND_NO_EXECUTION"})
    with pytest.raises(audit.AuditIssue):
        audit.MainReplay(object())


def test_synthetic_jsonl_partial_and_exclusive_output(tmp_path):
    path = tmp_path / "scripted.jsonl"
    path.write_text('{"type":"fixture"}\n{"type":', encoding="ascii")
    iterator = audit.lines(path, 2)
    assert next(iterator) == {"type": "fixture"}
    with pytest.raises(audit.AuditIssue) as caught:
        next(iterator)
    assert caught.value.category == "PARTIAL"
    output = tmp_path / "audit"
    audit.output_pair(output, {"status": "SYNTHETIC"}, None)
    assert json.loads((output / "audit_failure.json").read_text()) is None
    with pytest.raises(FileExistsError):
        audit.output_pair(output, {}, None)
