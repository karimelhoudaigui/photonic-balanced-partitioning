"""Nine pure exact fixtures. No NumPy, Perceval, native API, graph or RNG."""
from fractions import Fraction as F
import importlib.util
import json
import math
from pathlib import Path

_PATH = Path(__file__).resolve().parents[1]/"research/P96_column_loss_validation.py"
_SPEC = importlib.util.spec_from_file_location("p96_pure_fixtures", _PATH)
p96 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(p96)


def record(record_property, report):
    rows = [{"n": n, "p": str(p), "q": str(report["q"].get(n, 0))} for n, p in report["p"].items()]
    record_property("p96_exact", json.dumps({"rows": rows, "mu": str(report["mu"]),
                                           "status": report["status"], "tv": str(report.get("tv"))}))


def test_vacuum(record_property):
    report = p96.audit(p96.matrix([[]]))
    record(record_property, report)
    assert report["p"] == {(0,): F(1)} == report["q"]
    assert report["mu"] == report["tv"] == report["e3"] == 0


def test_unary_attenuation(record_property):
    report = p96.audit(p96.matrix([["1/2"]]))
    record(record_property, report)
    assert report["p"] == {(0,): F(3, 4), (1,): F(1, 4)} == report["q"]
    assert report["tv"] == report["g2"][0][0] == 0


def test_scaled_hom_factorial_and_zero(record_property):
    report = p96.audit(p96.matrix([["1/4", "1/4"], ["1/4", "-1/4"]]))
    record(record_property, report)
    expected = {(0, 0): F(49, 64), (1, 0): F(7, 64), (0, 1): F(7, 64),
                (2, 0): F(1, 128), (1, 1): F(0), (0, 2): F(1, 128)}
    assert report["p"] == expected == report["q"]
    assert report["g2"] == [[F(1, 64), F(0)], [F(0), F(1, 64)]]
    assert report["tv"] == 0


def test_nonorthogonal_two_input_hand_table(record_property):
    report = p96.audit(p96.matrix([["1/4", 0], ["-1/4", "1/4"]]))
    record(record_property, report)
    expected = {(0, 0): F(211, 256), (1, 0): F(15, 256), (0, 1): F(27, 256),
                (2, 0): F(0), (1, 1): F(1, 256), (0, 2): F(1, 128)}
    assert report["p"] == expected == report["q"]
    assert report["mu"] == F(3, 16) and report["tv"] == 0


def test_three_input_rank_one_hand_table(record_property):
    report = p96.audit(p96.matrix([["1/4"]*3]))
    record(record_property, report)
    assert report["p"] == {(0,): F(1709, 2048), (1,): F(297, 2048),
                           (2,): F(39, 2048), (3,): F(3, 2048)}
    assert report["q"] == {(0,): F(107, 128), (1,): F(9, 64), (2,): F(3, 128)}
    assert report["tv"] == report["weighted_tail"] == report["bound24"] == F(3, 512)
    assert report["tv"] == 4*report["p"][(3,)]


def test_smaller_rank_one_independent_table(record_property):
    report = p96.audit(p96.matrix([["1/8"]*3]))
    record(record_property, report)
    assert report["p"] == {(0,): F(125117, 131072), (1,): F(5769, 131072),
                           (2,): F(183, 131072), (3,): F(3, 131072)}
    assert report["q"] == {(0,): F(1955, 2048), (1,): F(45, 1024), (2,): F(3, 2048)}
    assert report["tv"] == report["bound24"] == F(3, 32768)


def test_physical_outside_domain_is_preserved(record_property):
    report = p96.audit(p96.matrix([["1/2"]*4]), valid=False)
    record(record_property, report)
    assert report["status"] == "EXPECTED_OUTSIDE_DOMAIN" and not report["theorem_applied"]
    assert report["mu"] == 1 and report["q"][(1,)] == F(-1, 2)
    assert report["p"] == {(0,): F(15, 32), (1,): F(1, 4), (2,): F(3, 16), (3,): F(0), (4,): F(3, 32)}
    assert "tv" not in report


def test_boundary_rank_one_four_input_table(record_property):
    report = p96.audit(p96.matrix([["1/4"]*4, ["1/4"]*4]))
    record(record_property, report)
    totals = [sum(p for n, p in report["p"].items() if sum(n) == degree) for degree in range(5)]
    assert totals == [F(331, 512), F(31, 128), F(21, 256), F(3, 128), F(3, 512)]
    assert report["mu"] == F(1, 2) and report["q"][(0, 0)] == F(11, 16)
    assert report["q"][(1, 0)] == report["q"][(0, 1)] == F(1, 16)
    assert report["g2"] == [[F(3, 32)]*2]*2 and report["tv"] == F(75, 512)


def test_registered_population_counts_and_iterator(record_property):
    rows = p96.cases()
    shapes = [(name, len(t), len(t[0]), valid, native) for name, t, valid, native in rows]
    assert [name for name, _, _, _, native in shapes if native] == ["V0", "U1", "H2", "R3a", "B4"]
    assert sum(valid for _, _, _, valid, _ in shapes) == 12 and len(shapes) == 13
    assert sum(math.comb(m+k, k) for _, m, k, valid, _ in shapes if valid) == 162
    assert sum(math.comb(m+k, k) for _, m, k, _, _ in shapes) == 167
    assert sum(math.comb(m+2*k-1, k) for _, m, k, _, native in shapes if native) == 159
    assert len(list(p96.occupations(4, 6))) == 126
    record_property("p96_population", json.dumps(shapes))
