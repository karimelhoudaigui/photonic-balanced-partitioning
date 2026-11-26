"""Prospective tiny/scripted P90a auditor qualification; never production RNG.

No parameter generator, DEV role digest, graph generator, native backend,
producer helper or optimizer is used, including during module collection.
"""
import copy
import math
from pathlib import Path

import pytest

from research import P90a_independent_raw_audit as audit


def graph():
    return [[0, 2, 5, 0], [2, 0, 1, 3], [5, 1, 0, 4], [0, 3, 4, 0]]


def z(z):
    return {"real": float(z.real), "imag": float(z.imag)}


def matrix(raw):
    return [[z(complex(v)) for v in row] for row in raw]


def span(identity, label, tick, paid=True, context=None):
    return {"id": identity, "case": audit.CASES[0], "kind": "OBSERVED_SPAN", "label": label,
        "paid": paid, "context": context or {}, "start_cpu": float(tick), "start_wall": float(tick),
        "end_cpu": float(tick+1), "end_wall": float(tick+1), "cpu_seconds": 1.0, "wall_seconds": 1.0}


def record_batch(owner, start, mask, phase, cuts, masks, inside, outside):
    best = min(range(4), key=lambda i: (cuts[i], i))
    return {"type": "scored_batch", "id": owner+"/scores/"+str(start), "phase": phase,
        "owner_span": owner, "score_start": start, "count": 4, "source_mask_u32": mask,
        "base_cut": 9 if mask == 3 else 7, "inside": inside, "outside": outside,
        "cuts": cuts[:], "masks_u32": masks[:], "best_index": best, "best_cut": cuts[best],
        "best_mask_u32": masks[best], "order": "i-major/a-minor"}


def scalar(owner, sequence, mask, value, phase):
    return {"type": "scalar_score", "owner_span": owner, "sequence": sequence, "phase": phase,
            "mask_u32": mask, "mask_hex": audit.mask_hex(mask, 4), "cut": value}


def analytic_eigen(h):
    a, d, b = h[0][0].real, h[1][1].real, h[0][1]
    radius = math.sqrt(((a-d)/2)**2+abs(b)**2)
    return [(a+d)/2-radius, (a+d)/2+radius]


def closed_compiler(base=7, coupling=2):
    d = base+coupling
    theta, off = base/d, coupling/d
    phase = complex(math.cos(theta), -math.sin(theta))
    v = [[phase*math.cos(off), phase*complex(0, -math.sin(off))],
         [phase*complex(0, -math.sin(off)), phase*math.cos(off)]]
    error = audit.gram_error(v)
    compiled = {"source_order": [0, 2], "target_order": [1, 3], "M": [[base, coupling], [coupling, base]],
        "H": matrix([[base, coupling], [coupling, base]]), "eigenvalues": [float(base-coupling), float(base+coupling)],
        "d": float(d), "V": matrix(v), "v_gram_error": error,
        "nonflat_max": max(abs(abs(x)**2-0.5) for row in v for x in row),
        "ipr_sum": sum(abs(x)**4 for row in v for x in row)}
    frame = max(abs(0.5*int(i == j)+0.5*sum(v[a][i].conjugate()*v[a][j] for a in range(2))-int(i == j))
                for i in range(2) for j in range(2))
    return compiled, {"W": matrix(v), "w_gram_error": error, "frame_gram_error": frame}


class ScriptedReplay:
    def permutation(self, case, arm, name, values, chain=-1, step=-1):
        return list(values)

    def role(self, case, arm, name, chain=-1, step=-1):
        return ["SYNTHETIC_ONLY", case, arm, name, chain, step]

    def seed(self, role, native=False):
        return 42 if native else 43

    def split_coins(self, case, chain, step, k):
        return [1]*k


def tiny_case():
    cid = audit.CASES[0]
    records = [span(cid+"/1", "case_private_setup", 0),
        span(cid+"/2", "reset_start_warmstart", 2, context={"chain": 0}),
        span(cid+"/3", "compile_all_M_transport_split", 4, context={"chain": 0, "step": 0}),
        span(cid+"/4", "decode_raw_Q_accept_bests", 6, context={"chain": 0, "step": 0}),
        span(cid+"/5", "own_chain_finalization", 8, context={"chain": 0}),
        span(cid+"/6", "case_algorithm_finalization", 10)]
    ledger = audit.ledger_checked(records)
    best = {"mask_u32": 5, "mask_hex": "05", "cut": 7, "sequence": 2}
    compiler_best = {"mask_u32": 3, "mask_hex": "03", "cut": 9, "sequence": 10}
    warm = {"mask": 5, "cut": 7, "scans": 2, "local_optimum": True}
    quench = {"mask": 5, "cut": 7, "scans": 1, "local_optimum": True}
    state = {"mask_u32": 5, "mask_hex": "05", "cut": 7}
    c, routed = closed_compiler()
    rows = [{"type": "case_start", "case": cid, "priority_rank": [0, 1, 2, 3],
             "total_edge_weight": 15, "case_start_clocks": [0.0, 0.0]},
        scalar(cid+"/2", 0, 3, 9, "reset"),
        record_batch(cid+"/2", 1, 3, "warmstart", [14, 7, 7, 14], [9, 5, 5, 9], [0, 1], [2, 3]),
        record_batch(cid+"/2", 5, 5, "warmstart", [14, 9, 9, 14], [9, 3, 3, 9], [0, 2], [1, 3]),
        {"type": "reset", "chain": 0, "reset_mask_u32": 3, "reset_cut": 9, "warmstart": warm, "own_scored_best": best},
        record_batch(cid+"/3", 9, 5, "compiler_M", [14, 9, 9, 14], [9, 3, 3, 9], [0, 2], [1, 3]),
        {"type": "attempt_request", "case": cid, "chain": 0, "step": 0, "current_before": state,
         "compiler": c, "routed": routed, "source_ports": [0, 2], "target_ports": [1, 3],
         "split_coins": [1, 1], "removed_ports": [], "native_role": ScriptedReplay().role(cid, "B", "native", 0, 0),
         "native_seed": 42, "repair_role": ScriptedReplay().role(cid, "B", "repair", 0, 0), "repair_seed": 43,
         "full_source_photons": 2},
        {"type": "native_not_called", "chain": 0, "step": 0, "reason": "r=0"},
        {"type": "native_observation", "chain": 0, "step": 0, "receiver_counts": [0, 0], "fallback": False},
        scalar(cid+"/4", 13, 5, 7, "raw_proposal"),
        record_batch(cid+"/4", 14, 5, "quench", [14, 9, 9, 14], [9, 3, 3, 9], [0, 2], [1, 3]),
        {"type": "attempt_outcome", "chain": 0, "step": 0,
         "decoded": {"mask": 5, "kept_counts": [1, 1], "receiver_counts": [0, 0], "full_counts": [1, 1, 0, 0],
             "vertex_counts": [1, 0, 1, 0], "removed_vertices": [], "r": 0, "h": 0, "fill": [], "repair_used": False},
         "raw_cut": 7, "quench": quench, "accepted": False, "current_after": state,
         "endpoint_best": state, "own_scored_best": best, "all_paid_best": best},
        {"type": "case_result", "case": cid, "requested": 1, "completed": 1, "full_source_photons": 2,
         "conditional_receiver_photons": 0, "r_histogram": [1, 0, 0], "chains": [{"chain": 0, "warmstart_cut": 7,
             "own_scored_best": best, "own_scored_best_phase": "warmstart", "endpoint_best": state, "current": state}],
         "accepted_steps": 0, "raw_mean_cut": {"numerator": 7, "denominator": 1},
         "q_mean_cut": {"numerator": 7, "denominator": 1}, "raw_mean_normalized": {"numerator": 7, "denominator": 15},
         "q_mean_normalized": {"numerator": 7, "denominator": 15}, "all_paid_best": best,
         "all_paid_best_phase": "warmstart", "compiler_only_best": compiler_best, "scored_candidates": 18,
         "grant_wall_seconds": 6.0, "paid_component_ids": [r["id"] for r in records],
         "case_start_clocks": [0.0, 0.0], "case_end_clocks": [12.0, 12.0]},
        {"type": "native_readback", "case": cid,
         "readback": {"native_threads": 1, "environment_threads": {key: "1" for key in audit.THREADS}}}]
    return rows, ledger


def tiny_trace():
    return {"cpu_seconds": [0.1, 0.2, 0.4], "wall_seconds": [0.1, 0.3, 0.8],
        "best_cut": [9, 7, 7], "mask_hex": ["03", "05", "05"],
        "proposal_count": [0, 4, 8], "stage_code": [0, 1, 2]}


def trace_result(work=8):
    return {"proposal_count": work, "compute_cpu_seconds": 0.5, "compute_wall_seconds": 0.9}


def test_scalar_integer_cuts_and_noncubic_weighted_graph():
    assert audit.integer_cut(graph(), 3) == 9
    assert audit.integer_cut(graph(), 5) == 7
    assert audit.integer_cut(graph(), 9) == 14
    assert audit.graph_checked(graph()) == graph()


def test_strict_types_do_not_accept_float_cuts_or_boolean_masks():
    for value in (True, 7.0, "7"):
        with pytest.raises(audit.AuditIssue):
            audit.integer(value, "fixture")
    with pytest.raises(audit.AuditIssue):
        audit.same([1.0], [1], "strict-nested")


def test_mask_packing_padding_balance_canonical_complement():
    assert audit.mask_read("05", 4) == 5
    assert audit.orient(10, [0, 1, 2, 3]) == 5
    for value in ("f5", "00", "05ff", "zz"):
        with pytest.raises(audit.AuditIssue):
            audit.mask_read(value, 4)


def test_full_neighbor_order_keeps_duplicate_complements_and_first_tie():
    inside, outside, masks, cuts = audit.swap_data(graph(), 3, [0, 1, 2, 3])
    assert (inside, outside, masks, cuts) == ([0, 1], [2, 3], [9, 5, 5, 9], [14, 7, 7, 14])


def test_score_batch_independent_cuts_every_row_sequence_credit():
    rows, ledger = tiny_case()
    book = audit.ScoreAudit(graph(), [0, 1, 2, 3], ledger, audit.CASES[0])
    book.scalar(rows[1], 3, "reset", 0, None)
    assert book.batch(rows[2], 3, "warmstart", 0, None) == (5, 7)
    assert book.sequence == 5 and book.best["sequence"] == 2


def test_missing_or_wrong_nonbest_batch_neighbor_is_detected():
    rows, ledger = tiny_case()
    rows[2]["cuts"][0] = 15
    book = audit.ScoreAudit(graph(), [0, 1, 2, 3], ledger, audit.CASES[0])
    book.scalar(rows[1], 3, "reset", 0, None)
    with pytest.raises(audit.AuditIssue):
        book.batch(rows[2], 3, "warmstart", 0, None)


def test_taylor40_zero_scalar_and_complex_hermitian_pauli():
    assert audit.taylor40([[0j]], 1.0) == [[1+0j]]
    got = audit.taylor40([[0j, 1j], [-1j, 0j]], 1.0)
    expected = [[math.cos(1), math.sin(1)], [-math.sin(1), math.cos(1)]]
    assert max(abs(got[a][i]-expected[a][i]) for a in range(2) for i in range(2)) < 1e-13


def test_taylor_rejects_unbounded_normalized_matrix_and_bad_d():
    for h, d in (([[5+0j]], 1.0), ([[0j]], 0.0)):
        with pytest.raises(audit.AuditIssue):
            audit.taylor40(h, d)


def test_compiler_transpose_shared_normalizer_closed_two_by_two():
    compiled, routed = closed_compiler()
    audit.compiler_check(graph(), 5, [0, 1, 2, 3], compiled, routed, [0, 2], [1, 3], analytic_eigen)


def test_compiler_wrong_sign_or_source_label_transport_fails():
    compiled, routed = closed_compiler()
    compiled["M"][0][1] = -2
    with pytest.raises(audit.AuditIssue):
        audit.compiler_check(graph(), 5, [0, 1, 2, 3], compiled, routed, [0, 2], [1, 3], analytic_eigen)
    compiled, routed = closed_compiler()
    with pytest.raises(audit.AuditIssue):
        audit.compiler_check(graph(), 5, [0, 1, 2, 3], compiled, routed, [2, 0], [1, 3], analytic_eigen)


def test_decode_collision_uniform_fill_and_full_source_identity():
    record = {"mask": 12, "kept_counts": [0, 0], "receiver_counts": [2, 0], "full_counts": [0, 0, 2, 0],
        "vertex_counts": [0, 0, 2, 0], "removed_vertices": [0, 1], "r": 2, "h": 1,
        "fill": [3], "repair_used": False}
    assert audit.decoded_check([0, 1], [2, 3], [0, 1], [2, 0], record,
                               lambda *_: pytest.fail("deterministic full fill")) == 12
    scripted = {"mask": 44, "kept_counts": [0, 0, 1], "receiver_counts": [2, 0, 0],
        "full_counts": [0, 0, 1, 2, 0, 0], "vertex_counts": [0, 0, 1, 2, 0, 0],
        "removed_vertices": [0, 1], "r": 2, "h": 1, "fill": [5], "repair_used": True}
    calls = []
    def choose(available, count):
        calls.append((available, count))
        return [5]
    assert audit.decoded_check([0, 1, 2], [3, 4, 5], [0, 1], [2, 0, 0], scripted, choose) == 44
    assert calls == [([4, 5], 1)]


def test_decode_loss_float_counts_and_bad_mapping_fail():
    for y in ([1, 0], [2.0, 0], [True, 1], [-1, 3]):
        with pytest.raises(audit.AuditIssue):
            audit.decoded_check([0, 1], [2, 3], [0, 1], y, {}, lambda *_: [])


def test_typed_factory_residual_unknown_cpu_and_no_double_pay():
    cid = audit.CASES[0]
    outer = span(cid+"/1", "factory_total", 0, paid=False)
    reported = {"id": cid+"/2", "case": cid, "kind": "REPORTED_DURATION", "paid": False,
        "label": "P43_backend_setup_reported", "wall_seconds": 0.25, "cpu_seconds": None,
        "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
        "helper_source_path": "research/P43_global_gain_probe.py", "helper_source_sha256": audit.P43_SHA, "outer_ref": cid+"/1"}
    residual = {"id": cid+"/3", "case": cid, "kind": "DURATION_DIFF", "paid": True,
        "label": "factory_prefix_plus_return_residual", "wall_seconds": 0.75, "cpu_seconds": None,
        "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
        "outer_ref": cid+"/1", "reported_ref": cid+"/2", "formula": "factory_outer_wall - helper_reported_setup_wall"}
    assert audit.ledger_checked([outer, reported, residual])["grants"][cid] == 0.75
    residual["cpu_seconds"] = 0
    with pytest.raises(audit.AuditIssue):
        audit.ledger_checked([outer, reported, residual])


def test_paid_clock_scope_rejects_IO_and_overlap():
    for rows in ([span("x", "serialization", 0)],
                 [span("x", "case_private_setup", 0), span("y", "case_algorithm_finalization", 0)]):
        with pytest.raises(audit.AuditIssue):
            audit.ledger_checked(rows)


def test_control_gap_subtracts_reported_cpu_wall_without_clipping():
    assert audit.duration_gap((2.0, 3.0), (0.25, 0.5), (1.0, 2.0)) == (0.75, 0.5)
    with pytest.raises(audit.AuditIssue):
        audit.duration_gap((1.0, 1.0), (0.5, 0.5), (0.6, 0.4))


def test_all_trace_rows_checked_and_latest_dual_timely_not_cpu_only():
    selected, direct, first, _, _, timely, count = audit.trace_check(
        tiny_trace(), graph(), (0.05, 0.05), (0.1, 0.1), 0.5, trace_result())
    assert selected["index"] == direct["index"] == 1
    assert first == 1 and timely and count == 3


def test_late_wrong_trace_cut_is_still_audit_failure():
    trace = tiny_trace()
    trace["best_cut"][-1] = 6
    with pytest.raises(audit.AuditIssue):
        audit.trace_check(trace, graph(), (0.0, 0.0), (0.0, 0.0), 0.15, trace_result())


def test_trace_nonmonotone_or_static_checkpoint_bound_rejected():
    trace = tiny_trace()
    trace["wall_seconds"][1] = 0.05
    with pytest.raises(audit.AuditIssue):
        audit.trace_check(trace, graph(), (0.0, 0.0), (0.0, 0.0), 1.0, trace_result())
    trace = tiny_trace()
    for key in trace:
        trace[key] = trace[key]*2
    with pytest.raises(audit.AuditIssue):
        audit.trace_check(trace, graph(), (0.0, 0.0), (0.0, 0.0), 1.0, trace_result())


def test_full_panel_requires_all_four_and_strict_comparisons():
    cases = {cid: {"complete": True, "all_paid_best": {"cut": 7}} for cid in audit.CASES}
    controls = [{"case": cid, "mode": mode, "normal_return": True, "adequate": True,
                 "selected": {"cut": 8}} for mode in audit.FAST for cid in audit.CASES]
    assert audit.classify(cases, controls) == "FOLLOWUP_REQUIRED"
    controls[0]["selected"]["cut"] = 7
    assert audit.classify(cases, controls) == "NO_POSITIVE_SIGNAL"
    controls[-1]["adequate"] = False
    assert audit.classify(cases, controls) == "INCONCLUSIVE_BASELINE_ELIGIBILITY"


def test_complete_scripted_tiny_case_all_score_credit_reset_Q_and_photons():
    rows, ledger = tiny_case()
    result = audit.case_audit(audit.CASES[0], graph(), rows, ledger, ScriptedReplay(), analytic_eigen,
                              chains=1, steps=1)
    assert result["complete"] and result["scored_candidates"] == 18
    assert result["all_paid_best"]["sequence"] == 2 and result["r_histogram"] == [1, 0, 0]


def test_scripted_case_wrong_current_or_lost_nonoptical_credit_rejected():
    for index, field, value in ((6, "current_before", {"mask_u32": 3, "mask_hex": "03", "cut": 9}),
                                (11, "all_paid_best", {"mask_u32": 5, "mask_hex": "05", "cut": 7, "sequence": 13})):
        rows, ledger = tiny_case()
        rows[index][field] = value
        with pytest.raises(audit.AuditIssue):
            audit.case_audit(audit.CASES[0], graph(), rows, ledger, ScriptedReplay(), analytic_eigen,
                             chains=1, steps=1)


def test_partial_case_is_explicit_inconclusive_not_full_pass():
    rows, ledger = tiny_case()
    result = audit.case_audit(audit.CASES[0], graph(), rows[:9], ledger, ScriptedReplay(), analytic_eigen,
                              require_complete=False, chains=1, steps=1)
    assert result["complete"] is False and result["requested"] == 1 and result["completed"] == 0
    with pytest.raises(audit.AuditIssue):
        audit.case_audit(audit.CASES[0], graph(), rows[:9], ledger, ScriptedReplay(), analytic_eigen,
                         chains=1, steps=1)


def test_exact_numeric_runner_wall_90_accepts_float_but_nothing_nearby():
    run = {"timeout_seconds": 90.0, "max_output_bytes": 4194304,
           "resource_limits": {"cpu_seconds": 60, "max_threads": 1}}
    audit.producer_limits_checked(run)
    run["timeout_seconds"] = 90
    audit.producer_limits_checked(run)
    for value in (90.000001, float("nan"), "90", True):
        run["timeout_seconds"] = value
        with pytest.raises(audit.AuditIssue):
            audit.producer_limits_checked(run)
    run["timeout_seconds"] = 90.0
    for location, field, bad in ((run, "max_output_bytes", 4194304.0),
                                  (run["resource_limits"], "cpu_seconds", 60.0),
                                  (run["resource_limits"], "max_threads", 1.0)):
        old, location[field] = location[field], bad
        with pytest.raises(audit.AuditIssue):
            audit.producer_limits_checked(run)
        location[field] = old


def test_parser_rejects_duplicate_keys_nonfinite_truncated_or_oversized(tmp_path):
    for raw in (b'{"a":1,"a":2}', b'{"x":NaN}', b'{"a":'):
        with pytest.raises(audit.AuditIssue):
            audit.parse_json(raw)
    with pytest.raises(audit.AuditIssue):
        audit.parse_json(b" "*(audit.LINE_BYTES+1))
    path = tmp_path/"rows.jsonl"
    path.write_bytes(b'{"x":1}')
    with pytest.raises(audit.AuditIssue):
        list(audit.json_rows(path, 2))


def test_project_path_rejects_absolute_parent_and_symlink(tmp_path):
    path = tmp_path/"x"
    path.write_text("fixture")
    (tmp_path/"link").symlink_to(path)
    for value in (str(path), "../x", "link", "missing"):
        with pytest.raises(audit.AuditIssue):
            audit.project_file(tmp_path, value)


def test_wrong_postseal_token_and_unbound_state_fail_before_any_replay():
    with pytest.raises(audit.AuditIssue) as error:
        audit.MainReplay(None)
    assert error.value.category == "AUTHORIZATION"
    with pytest.raises(audit.AuditIssue):
        audit.verify_closure(Path("."), {"binding_state": "UNBOUND"})


def test_manifest_strict_result_child_and_exact_input_order():
    contract = {"planned_command": ["SCRIPTED"], "execution_artifacts": [],
                "runner_output_directory": "run", "declared_results": ["outside/result.json"]}
    manifest = {"schema_version": 2, "command": ["SCRIPTED"], "execution_artifacts": [],
        "input_artifacts": [], "declared_results": ["outside/result.json"], "output_directory": "run"}
    with pytest.raises(audit.AuditIssue):
        audit.manifest_checked(manifest, contract, {}, "fixture")


def test_scripted_full_control_return_header_gap_trace_and_witness_lineage():
    cid, mode = audit.CASES[0], audit.FAST[0]
    prefix = cid+"/"+mode
    outer = {"id": prefix+"/outer", "kind": "OBSERVED_SPAN", "start_cpu": 0.0, "start_wall": 0.0,
        "end_cpu": 1.0, "end_wall": 1.0, "cpu_seconds": 1.0, "wall_seconds": 1.0}
    adapter = {"id": prefix+"/adapter", "kind": "OBSERVED_SPAN", "start_cpu": 0.0, "start_wall": 0.0,
        "end_cpu": 0.125, "end_wall": 0.125, "cpu_seconds": 0.125, "wall_seconds": 0.125}
    report = {"id": prefix+"/reported_compute", "case": cid, "mode": mode, "kind": "REPORTED_DURATION",
        "label": "P50_compute_reported", "paid": False, "cpu_seconds": 0.5, "wall_seconds": 0.75,
        "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
        "helper_source_path": "research/P50_fast_from_scratch.py", "helper_source_sha256": audit.P50_SHA}
    result = {"proposal_count": 8, "compute_cpu_seconds": 0.5, "compute_wall_seconds": 0.75,
        "early_cap_inconclusive": False, "max_proposals": 1000000, "free_incumbent_used": False}
    difference = {"kind": "CONSERVATIVE_DURATION_DIFF", "cpu_seconds": 0.375, "wall_seconds": 0.125,
        "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
        "formula": "observed_outer - direct_adapter - helper_reported_compute",
        "scope": "conservative entry plus return charge, not an observed prefix interval",
        "outer_ref": outer["id"], "direct_adapter_ref": adapter["id"], "reported_ref": report["id"]}
    selected = {"index": 2, "cut": 7, "mask_hex": "05", "cpu_seconds": 0.375, "wall_seconds": 0.5,
        "total_cpu": 0.875, "total_wall": 0.75, "provenance": "archived_preclock_RAM_prefix"}
    direct = dict(selected, total_cpu=0.5, total_wall=0.625)
    common = {"case": cid, "mode": mode, "grant": 1.0}
    raw = {"type": "control_return_observation", **common, "observed_outer": outer,
        "observed_direct_adapter": adapter, "reported_compute_duration": report, "returned_scalar_metadata": result}
    trace = {"type": "control_trace", "case": cid, "mode": mode, "cpu_seconds": [0.125, 0.25, 0.375],
        "wall_seconds": [0.125, 0.25, 0.5], "best_cut": [9, 7, 7], "mask_hex": ["03", "05", "05"],
        "proposal_count": [0, 4, 8], "stage_code": [0, 1, 2]}
    header = {"type": "control_header", **common, "seed_role": ScriptedReplay().role(cid, mode, "control"),
        "seed": 43, "adapter_cpu": 0.125, "adapter_wall": 0.125, "solver_cpu_budget": 0.875,
        "observed_outer": outer, "observed_direct_adapter": adapter, "reported_compute_duration": report,
        "call_boundary_difference": difference}
    outcome = {"type": "control_result", **common, "normal_return": True, "adapter_cpu": 0.125,
        "adapter_wall": 0.125, "selected": selected, "direct_selected": direct,
        "call_boundary_difference": difference, "first_scan_index": 1, "first_scan_dual_timely": True,
        "first_scan_cpu": 0.75, "first_scan_wall": 0.5, "early_guard": False, "adequate": True, "result": result}
    checked = audit.control_audit(audit.Cursor([raw, trace, header, outcome]), graph(), cid, mode, 1.0, ScriptedReplay())
    assert checked["adequate"] is True and checked["selected"]["index"] == 2
    bad_outcome = copy.deepcopy(outcome)
    bad_outcome["selected"]["index"] = 1
    with pytest.raises(audit.AuditIssue):
        audit.control_audit(audit.Cursor([raw, trace, header, bad_outcome]), graph(), cid, mode, 1.0, ScriptedReplay())


def test_first_failure_precedence_and_unreported_failure_never_become_panel_pass():
    run = {"status": "failed", "exit_status": 1}
    summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False}
    assert audit.failure_state_checked(run, summary, {"status": "FIRST_FAILURE"}) is True
    with pytest.raises(audit.AuditIssue):
        audit.failure_state_checked(run, {"status": "FOLLOWUP_REQUIRED", "positive_accepted": False}, {"status": "NO_FAILURE"})
    with pytest.raises(audit.AuditIssue):
        audit.failure_state_checked({"status": "completed", "exit_status": 0}, dict(summary, positive_accepted=True), {"status": "FIRST_FAILURE"})
