"""Prospective small qualification; no native18 probability query or draw.

Only actual native queries: fixed two-photon/two-mode HOM and bunched input.
The independent paired F6 source test imports no production sampler.
"""
from fractions import Fraction
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_file(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT/relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def pair_source():
    return load_file("p64_independent_F6_qualification", "research/P64_independent_F6_pair_source.py")


@pytest.fixture(scope="module")
def check():
    sys.path.insert(0, str(ROOT/"research"))
    return load_file("p64_naive18_qualification", "research/P64_naive18_probability_check.py")


def test_independent_paired_quadratics_are_exactly_twelve_terms(pair_source):
    assert pair_source.product((0, 1), (0, 1)) == (-1, 1)
    assert pair_source.modulus_squared((3, -4)) == 13
    for j in range(3):
        factor = pair_source.quadratic_terms(j)
        assert len(factor) == len({term[0] for term in factor}) == 12
        assert all(sum(powers) == 2 for powers, _ in factor)
    zero_factor = dict(pair_source.quadratic_terms(0))
    assert zero_factor[(2, 0, 0, 0, 0, 0)] == (1, 0)
    assert zero_factor[(0, 2, 0, 0, 0, 0)] == (-1, 0)
    assert zero_factor[(1, 0, 1, 0, 0, 0)] == (2, 0)
    assert zero_factor[(0, 1, 0, 1, 0, 0)] == (-2, 0)


def test_all_462_independent_source_coefficients_match_sealed_table_without_production_import(pair_source, tmp_path):
    # This function uses only the separately loaded pure-standard-library helper.
    primary = json.loads((ROOT/"research/P64_qualification/run_001/data/source_table.json").read_text())
    actual = pair_source.exact_source_table()
    compared = pair_source.comparison(actual, primary)
    requested = os.environ.get("P64_NAIVE18_QUAL_OUTPUT")
    directory = Path(requested) if requested else tmp_path/"independent-source"
    directory.mkdir(parents=True, exist_ok=False)
    with (directory/"independent_source.json").open("x", encoding="utf8") as stream:
        json.dump({"independent": actual, "comparison": compared}, stream, allow_nan=False, indent=2)
    assert actual["products_visited"] == 1728 and actual["all_occupations"] == 462
    assert all(actual["checks"].values())
    assert actual["denominator"] == 6**6
    assert sum(row["weight"] for row in actual["rows"]) == actual["denominator"]
    assert compared["all_rows_equal"] and compared["discrepancies"] == []
    assert len(actual["rows"]) == len({tuple(row["occupation"]) for row in actual["rows"]}) == 462


def test_exact_source_comparison_detects_coefficient_and_weight_changes(pair_source):
    actual = pair_source.exact_source_table()
    reference = json.loads(json.dumps(actual))
    reference["rows"][0]["coefficient"][0] += 1
    assert not pair_source.comparison(actual, reference)["all_rows_equal"]
    reference = json.loads(json.dumps(actual))
    reference["rows"][0]["weight"] += 1
    assert not pair_source.comparison(actual, reference)["all_rows_equal"]


def test_spec_freezes_seven_counts_two_exact_phases_and_fourteen_points(check):
    spec = json.loads((ROOT/"research/P64_naive18_probability_spec.json").read_text())
    assert spec == check.expected_spec()
    assert spec["points"] == 14 and len(spec["occupations"]) == 7
    assert len(spec["phase_arrays"]) == 2
    phases = spec["phase_arrays"][1]["exact"]
    assert all(Fraction(phases[0][i]) == 0 for i in range(6))
    assert all(Fraction(phases[b][0]) == 0 for b in range(3))
    assert [Fraction(phases[b][i]) for b in (1, 2) for i in range(1, 6)] == [Fraction(i, 11) for i in range(1, 11)]
    expected_totals = [(18, 0, 0, 0, 0, 0), (3,)*6, (6, 6, 6, 0, 0, 0),
                       (4, 4, 4, 2, 2, 2), (8, 2, 2, 2, 2, 2), (6, 6, 0, 0, 0, 6),
                       (18, 0, 0, 0, 0, 0)]
    for entry, totals in zip(spec["occupations"], expected_totals):
        counts = check.validate_counts(entry["counts"], 6)
        assert tuple(map(sum, entry["triples"])) == totals
        assert counts == tuple(entry["triples"][i][a] for a in range(3) for i in range(6))
    counts = spec["occupations"][4]["counts"]
    assert tuple(sum(counts[6*a:6*a+6]) for a in range(3)) == (7, 6, 5)
    assert spec["occupations"][-1]["counts"][12] == 18


def test_C6_forbidden_CF_case_is_retained_without_replacement(check):
    entries = check.occupations_frozen()
    residues = [sum(i*sum(entry["triples"][i]) for i in range(6)) % 6 for entry in entries]
    assert residues == [0, 3, 0, 0, 0, 0, 0]
    assert entries[1]["counts"] == [1]*18


def test_independent_dense_and_scalar_architectures_match_without_native18_queries(check):
    for phase in check.expected_spec()["phase_arrays"]:
        theta = tuple(tuple(float(Fraction(v)) for v in row) for row in phase["exact"])
        dense, scalar = check.dense_reference_matrix(theta), check.scalar_architecture_matrix(theta)
        diagnostics = check.matrix_diagnostics(dense, scalar)
        assert max(diagnostics.values()) <= check.MATRIX_TOLERANCE
        for row in range(18):
            expected = ([1/450]*6+[37/450]*12 if row == 0 else
                        [49/450]*6+[13/450]*12 if row == 6 else [1/18]*18)
            assert [abs(z)**2 for z in dense[row]] == pytest.approx(expected, abs=2e-14, rel=0)


@pytest.mark.parametrize("counts", [[1.0]*6, [True]*6, [-1, 7, 0, 0, 0, 0], [1]*5, [0]*6])
def test_count_guards_do_not_cast_clip_or_recondition(check, counts):
    with pytest.raises(ValueError):
        check.validate_counts(counts, 2)


def source_mock():
    row = SimpleNamespace(occupation=(2, 0), weight=1)
    return SimpleNamespace(support=(row,), lookup={(2, 0): row}, denominator=1)


def test_exact_zero_M_never_calls_conditional_normalization_or_project(check):
    def forbidden(*args):
        raise AssertionError("zero-M conditioning must not be called")
    fake = SimpleNamespace(d=2, source=source_mock(), conditional_state=forbidden,
                           local_distribution=forbidden, project=forbidden)
    p, receipt = check.structured_probability(fake, ((0, 0),)*3, (1,)*6)
    assert p == 0 and receipt["exact_color_mass"] == "0"
    assert receipt["zero_is_exact_color_mass"] and receipt["path"] == []


def test_wrapper_uses_normalized_probabilities_at_EVERY_color(check):
    epsilon = 1e-10
    class FakeSampler:
        d, source = 2, source_mock()
        def conditional_state(self, totals, theta):
            assert totals == (6, 0)
            return {"color": 0}, Fraction(1)
        def local_distribution(self, state, color):
            if color == 0:
                return ((2, 2, 2), (6, 0, 0)), [.25*(1+epsilon), .75*(1+epsilon)], (), ()
            return ((0, 0, 0),), [1+epsilon], (), ()
        def project(self, *args):
            return {"projected": True}
    p, receipt = check.structured_probability(FakeSampler(), ((0, 0),)*3, (2, 0, 2, 0, 2, 0))
    assert p == pytest.approx(.25, abs=1e-15, rel=0)
    assert len(receipt["path"]) == 2
    assert receipt["path"][1]["normalized_selected_mass"] == 1


def test_rounded_zero_branch_is_not_labelled_an_exact_source_zero(check):
    class FakeSampler:
        d, source = 2, source_mock()
        def conditional_state(self, *args): return {"one": True}, Fraction(1)
        def local_distribution(self, *args): return ((2, 2, 2), (6, 0, 0)), [0., 1.], (), ()
        def project(self, *args): raise AssertionError("cannot divide by zero")
    p, receipt = check.structured_probability(FakeSampler(), ((0, 0),)*3, (2, 0, 2, 0, 2, 0))
    assert p == 0 and not receipt["zero_is_exact_color_mass"]
    assert receipt["zero_origin"] == "rounded_local_Born_mass_not_exact_source_zero"


def test_tolerance_reports_relative_error_and_absolute_dominance_without_TV_claim(check):
    tiny = check.comparison(0., 5e-13)
    assert tiny["within_frozen_tolerance"] and tiny["absolute_term_dominates"]
    assert tiny["relative_error"] == 1
    assert not tiny["relative_precision_certified"] and not tiny["global_TV_certified"]
    assert not check.comparison(.1, .2)["within_frozen_tolerance"]
    assert check.comparison(0., 0.)["relative_error"] == 0


@pytest.mark.parametrize("value", [-1e-9, float("nan"), float("inf"), 2.])
def test_invalid_probabilities_fail_without_tolerance_repair(check, value):
    with pytest.raises(check.RetainedFailure):
        check.comparison(value, 0.)


def test_native_thread_control_rejects_readback_drift_without_backend(check):
    xq = SimpleNamespace(Config=SimpleNamespace(compute_max_thread_count=1))
    assert check.native_readback(xq) == 1
    xq.Config.compute_max_thread_count = 2
    with pytest.raises(check.RetainedFailure):
        check.native_readback(xq)


def test_ONLY_native_fixture_is_HOM2_and_bunched_input_factorials(check):
    api, metadata = check.load_naive_api()
    h = [[1/math.sqrt(2), 1/math.sqrt(2)], [1/math.sqrt(2), -1/math.sqrt(2)]]
    backend = check.backend_for(h, [1, 1], api)
    p_cf, _ = check.naive_probability(backend, [1, 1], api)
    p_bunch, _ = check.naive_probability(backend, [2, 0], api)
    assert p_cf == pytest.approx(0., abs=1e-28, rel=0)
    assert p_bunch == pytest.approx(.5, abs=2e-14, rel=0)
    bunched = check.backend_for(h, [2, 0], api)
    probabilities = [check.naive_probability(bunched, n, api)[0] for n in ([2, 0], [1, 1], [0, 2])]
    assert probabilities == pytest.approx([.25, .5, .25], abs=2e-14, rel=0)
    assert math.fsum(probabilities) == pytest.approx(1., abs=2e-14, rel=0)
    assert metadata["maximum_threads_configured"] == check.native_readback(api[1]) == 1


def test_evidence_files_are_exclusive_and_existing_data_is_preserved(check, tmp_path):
    path = tmp_path/"partial.json"
    check.save_json(path, {"counts": [1]*6, "error": "synthetic", "invalid_probability": float("inf")})
    original = path.read_bytes()
    assert json.loads(original)["invalid_probability"] == {"nonfinite_binary64": "inf"}
    with pytest.raises(FileExistsError):
        check.save_json(path, {"replacement": True})
    assert path.read_bytes() == original
