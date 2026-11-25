"""Synthetic exact/mocked guards; no physical P53 target or native LP call."""
from fractions import Fraction as Q
import gzip
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace
import warnings

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))
SPEC = importlib.util.spec_from_file_location("p53b", ROOT / "research/P53b_fixed_point_discriminator.py")
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)


def labels():
    result = []
    for phase in ("0", "pi/2"):
        for group in itertools.combinations(range(8), 4):
            if 0 in group:
                result.append({"kind": "b4", "theta": phase,
                               "groups": [list(group), [i for i in range(8) if i not in group]]})
    return result + [{"kind": "uniform70"}]


def uniform_inputs():
    power = [[{"numerator": 4, "denominator": 7}] +
             [{"numerator": 0, "denominator": 1}] * 6 for _ in range(28)]
    return ({"kernel_denominator": p.KERNEL_DEN, "crossing_power": power},
            {"denominator": p.KERNEL_DEN, "labels": labels(),
             "crossing_numerators": [[4 * p.KERNEL_DEN // 7] * 28 for _ in range(71)]})


def balanced_target(shift):
    value = [Q(4, 7)] * 28
    for edge, sign in (((0, 1), 1), ((2, 3), 1), ((0, 2), -1), ((1, 3), -1)):
        value[p.EDGES.index(edge)] += sign * shift
    return tuple(value)


def numerical_primal(weights, solved=True):
    return {"solver_fit_solved": solved, "solver_status": 0 if solved else 1,
            "solver_success": solved, "status": "NO_VERIFIED_TOLERANCE_MATCH",
            "verification": {"verified": True, "used_coefficients": weights}}


def numerical_dual(weights, solved=True):
    return {"solver_fit_solved": solved, "solver_status": 0 if solved else 1,
            "solver_success": solved, "signed_float_coordinates": weights}


def mock_native(monkeypatch, result, callback=None, warning=None):
    monkeypatch.setattr(p.lp_provider, "native_single_thread_check", lambda: {
        "threads": 1, "parallel": "off", "random_seed": 5201001, "time_limit": 1.})
    def solver(*args, **kwargs):
        if callback is not None:
            callback(*args, **kwargs)
        if warning is not None:
            warnings.warn(warning[0], warning[1])
        return result
    monkeypatch.setattr(p, "linprog", solver)


def test_canonical_rationals_reject_floats_noncanonical_and_invalid_denominators():
    assert p.rational_pair({"numerator": -2, "denominator": 3}) == Q(-2, 3)
    for value in (.5, {"numerator": 1., "denominator": 2},
                  {"numerator": True, "denominator": 2}, {"numerator": 2, "denominator": 4},
                  {"numerator": 1, "denominator": 0}, {"numerator": 1, "denominator": -2}):
        with pytest.raises(TypeError):
            p.rational_pair(value)


def test_fixed_point_horner_has_no_phase_parameter_and_preserves_exact_balanced_identities():
    source, control = uniform_inputs()
    power, library, actual_labels = p.extract_proof_data(source, control)
    assert p.fixed_target(power) == (Q(4, 7),) * 28
    changed = [list(row) for row in power]
    for edge, sign in (((0, 1), 1), ((2, 3), 1), ((0, 2), -1), ((1, 3), -1)):
        changed[p.EDGES.index(edge)][1] = Q(sign, 100)
    assert p.fixed_target(changed) == balanced_target(Q(1, 400))
    assert len(library) == 71 and actual_labels == labels()
    changed[0][1] = .1
    with pytest.raises(TypeError):
        p.fixed_target(changed)


def test_proof_schema_rejects_missing_endpoint_label_or_mean_coordinate():
    for mutation in ("label", "vertex", "coordinate", "numerator", "denominator", "incident"):
        source, control = uniform_inputs()
        if mutation == "label": control["labels"][0]["theta"] = "pi/3"
        if mutation == "vertex": control["crossing_numerators"].pop()
        if mutation == "coordinate": control["crossing_numerators"][0].pop()
        if mutation == "numerator": control["crossing_numerators"][0][0] = .5
        if mutation == "denominator": source["kernel_denominator"] = 1
        if mutation == "incident": source["crossing_power"][0][0] = {"numerator": 1, "denominator": 2}
        with pytest.raises((TypeError, ValueError, ArithmeticError)):
            p.extract_proof_data(source, control)


def test_hash_pinned_gzip_input_rejects_tampering_floats_and_inflation(tmp_path, monkeypatch):
    path = tmp_path / "proof.gz"
    path.write_bytes(gzip.compress(b'{"proof":1}', mtime=0))
    assert p.read_pinned_json(path, p.sha256(path)) == {"proof": 1}
    with pytest.raises(ValueError): p.read_pinned_json(path, "0" * 64)
    path.write_bytes(gzip.compress(b'{"proof":0.5}', mtime=0))
    with pytest.raises(TypeError): p.read_pinned_json(path, p.sha256(path))
    path.write_bytes(gzip.compress(b'{"proof":123}', mtime=0))
    monkeypatch.setattr(p, "MAX_INFLATED_INPUT", 4)
    with pytest.raises(ValueError): p.read_pinned_json(path, p.sha256(path))


def test_exact_binary_rule_is_not_decimal_rounding_and_large_L1_is_rescaled():
    library = [(Q(4, 7),) * 28]
    target = balanced_target(Q(-1, 100))
    witness = p.verify_dual(library, target, [.1] + [0.] * 27)
    assert witness["verified"] and witness["binary_signed_coordinates"][0] == Q.from_float(.1)
    assert witness["binary_signed_coordinates"][0] != Q(1, 10)
    rescaled = p.verify_dual(library, target, [2.] + [0.] * 27)
    assert rescaled["exact_rescaling_divisor"] == 2 and rescaled["exact_L1"] == 1
    assert rescaled["strict_margin"] == Q(1, 100)


def test_separator_verifies_every_vertex_including_a_single_adversarial_exception():
    target = balanced_target(Q(-1, 100))
    library = [(Q(4, 7),) * 28] * 70 + [balanced_target(Q(-2, 100))]
    witness = p.verify_dual(library, target, [1.] + [0.] * 27)
    assert not witness["verified"] and len(witness["all_vertex_margins"]) == 71
    assert witness["all_vertex_margins"][-1] == Q(-1, 100)


def test_zero_or_nonpositive_gap_never_counts_as_separation():
    row = (Q(4, 7),) * 28
    for weights in ([0.] * 28, [1.] + [0.] * 27):
        witness = p.verify_dual([row], row, weights)
        assert not witness["verified"] and witness["strict_margin"] == 0


def test_invalid_dual_vector_or_truncated_kernel_is_rejected():
    row = (Q(4, 7),) * 28
    for weights in (None, [0.] * 27, [math.inf] + [0.] * 27, [math.nan] + [0.] * 27):
        assert not p.verify_dual([row], row, weights)["verified"]
    with pytest.raises(ValueError): p.verify_dual([row[:-1]], row, [0.] * 28)
    with pytest.raises(ValueError): p.dot(row, row[:-1])


def test_nonnegative_graph_shift_uses_common_sixteen_and_exact_normalized_gap():
    library = [(Q(4, 7),) * 28] * 71
    target = balanced_target(Q(1, 100))
    dual = p.verify_dual(library, target, [-1.] + [0.] * 27)
    graph = p.nonnegative_graph(dual, library, target)
    assert graph["weights_nonnegative"] == (Q(0),) + (Q(1),) * 27
    assert graph["uniform_edge_shift"] == 1 and graph["weight_sum"] == 27
    assert graph["strict_mean_gap"] == Q(1, 100)
    assert graph["normalized_strict_mean_gap"] == Q(1, 2700)
    assert sum(graph["weights_normalized_sum_one"]) == 1
    with pytest.raises(ArithmeticError): p.nonnegative_graph(dual, library, (Q(0),) * 28)


def test_dual_lp_objective_constraints_bounds_and_flags_match_independent_known_separator(monkeypatch):
    row = (Q(4, 7),) * 28
    target = balanced_target(Q(-1, 100))
    raw = np.zeros(57); raw[0] = 1; raw[-1] = float(Q(4, 7))
    result = SimpleNamespace(x=raw, status=0, success=True, message="mock solved", fun=-.01)
    def check(objective, **kwargs):
        assert objective.shape == (57,) and kwargs["A_ub"].shape == (2, 57)
        assert np.max(kwargs["A_ub"] @ raw - kwargs["b_ub"]) == 0
        assert float(objective @ raw) == pytest.approx(-.01)
        assert kwargs["bounds"][-1] == (None, None)
        assert kwargs["method"] == "highs-ds" and kwargs["options"] == p.LP_OPTIONS
    mock_native(monkeypatch, result, callback=check, warning=(
        "Unrecognized options detected: {'threads': 1}. These will be passed to HiGHS verbatim.", p.OptimizeWarning))
    proposal = p.dual_proposal([row], target)
    assert proposal["solver_fit_solved"] and proposal["native_options_readback"]["parallel"] == "off"
    assert p.verify_dual([row], target, proposal["signed_float_coordinates"])["verified"]


def test_unknown_option_warning_blocks_solver_gate_without_hidden_retry(monkeypatch):
    result = SimpleNamespace(x=np.zeros(57), status=0, success=True, message="mock", fun=0.)
    calls = []
    mock_native(monkeypatch, result, callback=lambda *a, **k: calls.append(1),
                warning=("Option threads was ignored", p.OptimizeWarning))
    proposal = p.dual_proposal([(Q(4, 7),) * 28], (Q(4, 7),) * 28)
    assert proposal["status"] == "INCONCLUSIVE_SOLVER" and not p.solver_gate(proposal)
    assert calls == [1]


def test_timeout_failure_or_false_success_keeps_candidate_but_blocks_gate(monkeypatch):
    raw = np.zeros(57); raw[0] = 1.
    for status, success in ((1, False), (4, False), (0, False)):
        mock_native(monkeypatch, SimpleNamespace(x=raw, status=status, success=success, message="mock", fun=0.))
        proposal = p.dual_proposal([(Q(4, 7),) * 28], balanced_target(Q(-1, 100)))
        assert proposal["candidate_available"] and not p.solver_gate(proposal)
        assert p.verify_dual([(Q(4, 7),) * 28], balanced_target(Q(-1, 100)),
                             proposal["signed_float_coordinates"])["verified"]


def test_primal_solved_nonmatch_can_exactify_to_different_weights_and_still_runs_dual(monkeypatch):
    calls = []
    def primal(*args): calls.append("primal"); return numerical_primal([.5, .5])
    def dual(*args): calls.append("dual"); return numerical_dual([0.] * 28)
    monkeypatch.setattr(p.lp_provider, "convex_fit", primal)
    monkeypatch.setattr(p, "dual_proposal", dual)
    result = p.discriminate([(Q(0),) * 28, (Q(1),) * 28], (Q(1, 3),) * 28)
    assert result["status"] == "EXACT_POINT_MEMBERSHIP_CERTIFIED"
    assert result["primal_exact"]["weights"] == [Q(2, 3), Q(1, 3)]
    assert calls == ["primal", "dual"] and result["LP_provider_calls"] == 2


def test_primal_timeout_retains_exact_membership_but_does_not_accept(monkeypatch):
    monkeypatch.setattr(p.lp_provider, "convex_fit", lambda *a: numerical_primal([.5, .5], solved=False))
    monkeypatch.setattr(p, "dual_proposal", lambda *a: numerical_dual([0.] * 28))
    result = p.discriminate([(Q(0),) * 28, (Q(1),) * 28], (Q(1, 3),) * 28)
    assert result["primal_exact"]["verified"] and result["status"] == "INCONCLUSIVE_AT_FIXED_X"


def test_successful_strict_dual_yields_only_posthoc_endpoint_graph_witness(monkeypatch):
    monkeypatch.setattr(p.lp_provider, "convex_fit", lambda *a: {"verification": {"verified": False}})
    monkeypatch.setattr(p, "dual_proposal", lambda *a: numerical_dual([1.] + [0.] * 27))
    result = p.discriminate([(Q(4, 7),) * 28] * 71, balanced_target(Q(-1, 100)))
    assert result["status"] == "EXACT_POINT_ENDPOINT71_SEPARATION_CERTIFIED"
    assert result["nonnegative_graph_witness"]["label"].endswith("ENDPOINT71_ONLY")


def test_dual_timeout_retains_strict_exact_candidate_without_accepting_it(monkeypatch):
    monkeypatch.setattr(p.lp_provider, "convex_fit", lambda *a: {"verification": {"verified": False}})
    monkeypatch.setattr(p, "dual_proposal", lambda *a: numerical_dual([1.] + [0.] * 27, solved=False))
    result = p.discriminate([(Q(4, 7),) * 28] * 71, balanced_target(Q(-1, 100)))
    assert result["dual_exact"]["verified"] and result["status"] == "INCONCLUSIVE_AT_FIXED_X"


def test_mutually_inconsistent_exact_witnesses_override_any_solver_status():
    assert p.classify(True, True, True, True) == "INCONSISTENCY_EXACT_PRIMAL_AND_DUAL"
    assert p.classify(True, True, False, False) == "INCONSISTENCY_EXACT_PRIMAL_AND_DUAL"
    assert p.classify(False, False, True, True) == "INCONCLUSIVE_AT_FIXED_X"


def test_frozen_spec_disallows_new_point_library_call_count_or_resource_cap():
    p.validate_spec(p.frozen_spec())
    for key, value in (("x_numerator", 3), ("library", "continuous_b4"),
                       ("maximum_LP_calls", 3), ("maximum_cpu_seconds", 21)):
        spec = p.frozen_spec(); spec[key] = value
        with pytest.raises(ValueError): p.validate_spec(spec)


def test_bounded_gzip_output_is_exact_exclusive_and_rejects_uncompressed_overrun(tmp_path):
    path = tmp_path / "witness.json.gz"
    p.save_bounded_gzip(path, {"margin": Q(1, 2700)})
    with gzip.open(path, "rt") as stream: value = json.load(stream)
    assert value == {"margin": {"numerator": 1, "denominator": 2700}}
    with pytest.raises(FileExistsError): p.save_bounded_gzip(path, {})
    overrun = tmp_path / "overrun.gz"
    with pytest.raises(RuntimeError): p.save_bounded_gzip(overrun, {"large": "x" * 40}, maximum_bytes=16)
    assert not overrun.exists()


def test_no_candidate_bad_native_readback_or_nonfinite_signed_difference_is_inconclusive(monkeypatch):
    row = (Q(4, 7),) * 28
    mock_native(monkeypatch, SimpleNamespace(x=None, status=1, success=False, message="limit", fun=None))
    assert not p.dual_proposal([row], row)["candidate_available"]
    raw = np.zeros(57); raw[0] = 1e308; raw[28] = -1e308
    mock_native(monkeypatch, SimpleNamespace(x=raw, status=0, success=True, message="mock", fun=0.))
    assert not p.dual_proposal([row], row)["candidate_available"]
    def bad_native(): raise RuntimeError("readback mismatch")
    monkeypatch.setattr(p.lp_provider, "native_single_thread_check", bad_native)
    assert p.dual_proposal([row], row)["status"] == "INCONCLUSIVE_SOLVER"
