"""Prospective deterministic P82a qualification.

Authored without executing or importing this module or production code.
The single native item has exactly 183 planned Naive amplitude queries:
three HOM and 3 phases x 6 sources x 10 two-photon occupations.  It performs
no stochastic sampling.  All other items use tiny literals or scripted
workflow hooks, never DEV generation, a PCG stream or an eight-photon matrix.
"""
from collections import defaultdict
from fractions import Fraction
import hashlib
import importlib.metadata
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p82a_qualification_candidate", ROOT / "research/P82a_split_scatter_veto.py")
p = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = p
SPEC.loader.exec_module(p)

ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
I = (Fraction(0), Fraction(1))


def _add(a, b):
    return a[0] + b[0], a[1] + b[1]


def _mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def _scale(a, q):
    return a[0] * q, a[1] * q


def _norm2(a):
    return a[0] * a[0] + a[1] * a[1]


def _fraction_w(z):
    """Independent normalized K4 matrix, not production compiler output."""
    half = Fraction(1, 2)
    minus_one = (-ONE[0], -ONE[1])
    minus_z = (-z[0], -z[1])
    rows = [
        [ONE, ONE, ONE, ONE],
        [ONE, minus_one, z, minus_z],
        [ONE, ONE, minus_one, minus_one],
        [ONE, minus_one, minus_z, z],
    ]
    return [[_scale(value, half) for value in row] for row in rows]


def _complex_w(z):
    return [[complex(float(a), float(b)) for a, b in row] for row in _fraction_w(z)]


def _occupations_two(m):
    return [tuple(int(j == a) + int(j == b) for j in range(m))
            for a in range(m) for b in range(a, m)]


def _probability_two(matrix, source, occupation):
    rows = [r for r, count in enumerate(occupation) for _ in range(count)]
    a = _mul(matrix[rows[0]][source[0]], matrix[rows[1]][source[1]])
    b = _mul(matrix[rows[0]][source[1]], matrix[rows[1]][source[0]])
    denominator = math.prod(math.factorial(x) for x in occupation)
    return _norm2(_add(a, b)) / denominator


def _removed_weight(source):
    probabilities = (Fraction(1, 3), Fraction(3, 5),
                     Fraction(1, 3), Fraction(3, 5))
    return math.prod(probabilities[i] if i in source else 1 - probabilities[i]
                     for i in range(4))


def _repair_subsets(occupation):
    support = tuple(i for i, value in enumerate(occupation) if value)
    need = sum(occupation) - len(support)
    empty = tuple(i for i in range(len(occupation)) if i not in support)
    completions = tuple(itertools.combinations(empty, need))
    return tuple(tuple(sorted(support + completion)) for completion in completions)


def _one_receiving_edge_cost(selected):
    return int((0 in selected) != (1 in selected))


def _exact_r2_mean(z):
    matrix = _fraction_w(z)
    answer = Fraction(0)
    for source in itertools.combinations(range(4), 2):
        for occupation in _occupations_two(4):
            choices = _repair_subsets(occupation)
            decoder = sum(Fraction(_one_receiving_edge_cost(choice), len(choices))
                          for choice in choices)
            answer += _removed_weight(source) * _probability_two(
                matrix, source, occupation) * decoder
    return answer


def _tiny_graph():
    # Eight vertices, with the sole edge on receiving plus ports4,5.
    return ((0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 1, 0, 0),
            (0, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0))


def _scalar_cut(graph, subset):
    inside = frozenset(subset)
    return sum(graph[i][j] for i in range(len(graph))
               for j in range(i + 1, len(graph))
               if (i in inside) != (j in inside))


def _trace(clocks=((0.1, 0.1), (0.2, 0.2), (0.3, 2.0)),
           cuts=(9, 8, 0), masks=((255, 0), (127, 1), (63, 3))):
    return {"cpu_seconds": [x[0] for x in clocks],
            "wall_seconds": [x[1] for x in clocks],
            "best_cut": list(cuts),
            "best_subset_packbits_little": [list(x) for x in masks],
            "stage": ["initialization", "initial_scan", "descent_scan"],
            "proposal_count": [1, 65, 129]}


class _ScriptedClock:
    def __init__(self):
        self.ticks = 0
        self.wall_offset = 0.0

    def now(self):
        self.ticks += 1
        value = self.ticks / 10000
        return value, value + self.wall_offset


class _ScriptedRng:
    """A literal control script, not a pseudorandom generator."""
    def permutation(self, values):
        return list(range(values)) if isinstance(values, int) else list(values)

    def integers(self, *arguments):
        if len(arguments) == 1:
            return 0
        low, high, count = arguments
        return [low] * count

    def uniform(self, low, high):
        return low + (high - low) / 4


class _ScriptedDeps:
    """Workflow protocol only: no graph generator, matrix, RNG or native call."""
    def __init__(self, *, failed_sample=None, failed_fast=None, mixed_fast=False,
                 late_nonstart=False):
        self.clock = _ScriptedClock()
        self.events = []
        self.split_count = self.sample_count = 0
        self.failed_sample, self.failed_fast = failed_sample, failed_fast
        self.mixed_fast = mixed_fast
        self.late_nonstart = late_nonstart
        self.fast_calls = []
        self.seed_roles = []
        self.control_roles = []

    def guard(self):
        return None

    def generate_graph(self, case):
        self.events.append(("graph", case["id"]))
        return [[0] * 16 for _ in range(16)]

    def permutation(self, role, values):
        self.events.append(("permutation", tuple(role)))
        return list(values)

    def integers(self, role, high, count):
        self.events.append(("integers", tuple(role)))
        return [i % high for i in range(count)]

    def split_draws(self, role, denominators):
        r = self.split_count % 9
        self.split_count += 1
        self.events.append(("split", tuple(role), r))
        return [0 if i < r else denominator - 1
                for i, denominator in enumerate(denominators)]

    def native_seed(self, role):
        self.seed_roles.append(tuple(role))
        return 10000 + len(self.seed_roles)

    def control_seed(self, role):
        self.control_roles.append(tuple(role))
        return 20000 + len(self.control_roles)

    def control_rng(self, role):
        self.events.append(("scripted_control_rng", tuple(role)))
        return _ScriptedRng()

    def cache_factory(self, d):
        self.events.append(("cache", d))
        return {"profile": p.profile(d), "qualification_mock": True}

    def compiler(self, graph, source, target, phase_ids, *, cache):
        self.events.append(("compile", tuple(source), tuple(target), tuple(phase_ids)))
        return {"W": "qualification-placeholder-no-eight-mode-matrix",
                "J": [], "A": [], "phases": [1 + 0j] * len(phase_ids), "phase_trace": [],
                "analytic_uniform_null": False, "qualification_mock": True}

    def score(self, graph, subset):
        self.events.append(("score", tuple(subset)))
        if self.late_nonstart and tuple(subset) != tuple(range(8)):
            self.clock.wall_offset = 2.0
        return 100 if tuple(subset) == tuple(range(8)) else 90

    def scan(self, graph, subset, rank, base_cut):
        current = set(subset)
        rows = []
        for removed in sorted(current, key=lambda v: rank[v]):
            for added in sorted(set(range(16)) - current, key=lambda v: rank[v]):
                rows.append({"subset": p.canonical((current - {removed}) | {added},
                                                    16, rank),
                             "cut": base_cut, "removed": removed,
                             "added": added, "delta": 0})
        self.events.append(("scan", tuple(subset), len(rows)))
        return rows

    def make_sampler(self, matrix, source, native_seed):
        assert matrix == "qualification-placeholder-no-eight-mode-matrix"
        assert tuple(source) == tuple(sorted(source))
        self.events.append(("factory", tuple(source), native_seed))
        def sample():
            index = self.sample_count
            self.sample_count += 1
            counts = [len(source)] + [0] * 7
            self.events.append(("sample", tuple(source), tuple(counts)))
            if index == self.failed_sample:
                return counts, True
            return counts, False
        return sample, 0.00005

    def fast_solver(self, graph, seed, initialization, cpu_budget_seconds, max_proposals):
        call = len(self.fast_calls)
        self.fast_calls.append({"seed": seed, "initialization": initialization,
                                "budget": cpu_budget_seconds,
                                "max_proposals": max_proposals})
        if call == self.failed_fast:
            raise p.RetainedFailure("scripted FAST exception", {"call": call})
        value = 101 if self.mixed_fast and call in (1, 2) else 0
        stages = ["initialization"] if self.mixed_fast else ["initialization", "initial_scan"]
        trace = {"cpu_seconds": [0.00001] * len(stages),
                 "wall_seconds": [0.00001] * len(stages),
                 "best_cut": [value] * len(stages),
                 "best_subset_packbits_little": [[255, 0] for _ in stages],
                 "stage": stages, "proposal_count": [1 + 64*i for i in range(len(stages))]}
        return {"trace": trace, "best_cut": value, "best_subset": list(range(8)),
                "overall_completed_best_cut": value, "has_eligible_result": True,
                "comparison_acceptance_eligible": not self.mixed_fast,
                "first_scan_completed_before_deadline": not self.mixed_fast,
                "best_snapshot_cached_online": True, "early_cap_inconclusive": False,
                "early_stop_max_proposals": False, "early_wall_inconclusive": False,
                "compute_cpu_seconds": 0.00005, "compute_wall_seconds": 0.00005,
                "proposal_count": 65, "stop_reason": "cpu_budget_seconds"}

    def verify_candidate(self, graph, subset, cut):
        self.events.append(("verify", tuple(subset), cut))

    def native_readback(self):
        self.events.append(("native_readback",))
        return {"readback": 1, "compute_max_thread_count": 1,
                "qualification_mock": True}


def _workflow_spec():
    return json.loads((ROOT / "research/P82a_execution_spec.json").read_text())


def _file_digest(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(131072), b""):
            digest.update(block)
    return digest.hexdigest()


def test_qualification_executing_interpreter_and_installed_provenance(record_property):
    """Portable metadata hashes, without importing any scientific module."""
    expected_sources = {
        "backends/_clifford2017.py": "8dad1b8f389f346bde1b902f21d74e1466eabb258aeb0e92f827ff745d27329b",
        "backends/_naive.py": "aaa26604b0866eeba61aaca80e83afe4df689711f4ce3bf965db1da74314ef4d",
        "backends/_abstract_backends.py": "53f7c4db865c2e643b9ab461da0c71b2fbb9dc1a450ad917936ca0f4e25538f1",
        "utils/_random.py": "d56c9fc42986ee3e16f3d1110962044b3a91dcb7023315ca7db8a5aa21a2cea4",
        "utils/__init__.py": "e450aeca15789cbaddfd81eed4b30f0e6c6c8165169541febc5ad45605e5daab",
    }
    result = {"software": [], "critical_python_sources": [],
              "native_extension": None, "interpreter": None, "errors": []}
    for name in ("perceval-quandela", "exqalibur"):
        try:
            result["software"].append({"name": name,
                                       "version": importlib.metadata.version(name)})
        except Exception as error:
            result["errors"].append({"stage": "metadata", "package": name,
                                      "exception_repr": repr(error)})
    try:
        distribution = importlib.metadata.distribution("perceval-quandela")
        for relative, expected in expected_sources.items():
            path = Path(distribution.locate_file("perceval/" + relative))
            actual = _file_digest(path)
            result["critical_python_sources"].append({
                "package_relative_path": "perceval/" + relative,
                "sha256": actual, "expected_sha256": expected, "match": actual == expected})
    except Exception as error:
        result["errors"].append({"stage": "critical_python_sources",
                                  "exception_repr": repr(error)})
    try:
        distribution = importlib.metadata.distribution("exqalibur")
        extensions = sorted(str(path) for path in distribution.files or []
                            if Path(str(path)).name.startswith("exqalibur")
                            and str(path).endswith((".so", ".pyd")))
        if len(extensions) != 1:
            raise ValueError("expected one exqalibur extension: " + repr(extensions))
        path = Path(distribution.locate_file(extensions[0]))
        result["native_extension"] = {"path": str(path), "sha256": _file_digest(path)}
    except Exception as error:
        result["errors"].append({"stage": "native_extension",
                                  "exception_repr": repr(error)})
    try:
        executable = Path(sys.executable)
        realpath = executable.resolve()
        result["interpreter"] = {"executable": str(executable), "realpath": str(realpath),
                                 "sha256": _file_digest(realpath), "version": sys.version}
    except Exception as error:
        result["errors"].append({"stage": "interpreter", "exception_repr": repr(error)})
    record_property("P82a_external_provenance", json.dumps(result, allow_nan=False,
                                                          separators=(",", ":")))
    assert not result["errors"]
    assert {row["name"]: row["version"] for row in result["software"]} == {
        "perceval-quandela": "1.3.0", "exqalibur": "1.4.2"}
    assert len(result["critical_python_sources"]) == 5
    assert all(row["match"] for row in result["critical_python_sources"])
    assert result["native_extension"] is not None and result["interpreter"] is not None


def test_profile_exact_probabilities_and_nonuniform_range():
    result = p.profile(4, rho=Fraction(1), eta=Fraction(1, 2))
    assert result["odds"] == [Fraction(1, 2), Fraction(5, 6),
                              Fraction(7, 6), Fraction(3, 2)]
    assert result["probabilities"] == [
        Fraction(1, 3), Fraction(5, 11), Fraction(7, 13), Fraction(3, 5),
        Fraction(1, 3), Fraction(5, 11), Fraction(7, 13), Fraction(3, 5)]
    assert min(result["probabilities"]) == Fraction(1, 3)
    assert max(result["probabilities"]) == Fraction(3, 5)


def test_eta_zero_is_analytic_graph_independent():
    first = p.compile_receiver(_tiny_graph(), (0, 1, 2, 3), (4, 5, 6, 7),
                               (0, 1), rho=Fraction(1), eta=Fraction(0), sweeps=2)
    altered = [list(row) for row in _tiny_graph()]
    altered[4][5] = altered[5][4] = 999
    second = p.compile_receiver(altered, (0, 1, 2, 3), (4, 5, 6, 7),
                                (0, 1), rho=Fraction(1), eta=Fraction(0), sweeps=2)
    assert first["analytic_uniform_null"] is True
    assert second["analytic_uniform_null"] is True
    assert all(value == 0 for row in first["J"] for value in row)
    assert all(value == 0 for row in second["J"] for value in row)
    assert first["A"] == [[1 + 0j, 0j], [0j, 1 + 0j]]
    assert all(row["H"] == 0j and row["before"] == row["after"]
               for row in first["phase_trace"] + second["phase_trace"])
    assert first["phases"] == second["phases"]
    assert first["W"] == second["W"]
    expected = _complex_w(I)
    assert max(abs(first["W"][r][c] - expected[r][c])
               for r in range(4) for c in range(4)) < 2e-14


def test_small_receiver_independent_unitarity_and_phase_update():
    direct = p.compile_receiver(_tiny_graph(), (0, 1, 2, 3), (4, 5, 6, 7),
                                (0, 1), rho=Fraction(1), eta=Fraction(1, 2), sweeps=0)
    expected = _complex_w(I)
    assert max(abs(direct["W"][r][c] - expected[r][c])
               for r in range(4) for c in range(4)) < 2e-14
    compiled = p.compile_receiver(_tiny_graph(), (0, 1, 2, 3), (4, 5, 6, 7),
                                  (0, 1), rho=Fraction(1), eta=Fraction(1, 2), sweeps=2)
    matrix = compiled["W"]
    for a in range(4):
        for b in range(4):
            gram = sum(matrix[r][a].conjugate() * matrix[r][b] for r in range(4))
            assert abs(gram - int(a == b)) < 2e-14
    assert all(abs(abs(value)**2 - Fraction(1, 4)) < 2e-14
               for row in matrix for value in row)
    assert compiled["analytic_uniform_null"] is False


def test_decoder_keeps_collisions_and_deterministic_extremes():
    source, target = (0, 1, 2, 3), (4, 5, 6, 7)
    forbidden = lambda available, need: pytest.fail("deterministic repair invoked RNG")
    vacuum = p.decode_counts(source, target, (), (0, 0, 0, 0), forbidden)
    assert tuple(vacuum["subset"]) == source
    assert vacuum["repair_rng_used"] is False
    assert sum(vacuum["full_counts"]) == 4
    full = p.decode_counts(source, target, (0, 1, 2, 3), (4, 0, 0, 0), forbidden)
    assert tuple(full["subset"]) == target
    assert full["repair_rng_used"] is False
    assert full["h"] == 1 and full["r"] == 4
    calls = []
    def choose(available, need):
        calls.append((tuple(available), need))
        return tuple(available[:need])
    bunched = p.decode_counts(source, target, (0, 2), (2, 0, 0, 0), choose)
    assert calls == [((5, 6, 7), 1)]
    assert tuple(bunched["subset"]) == (1, 3, 4, 5)
    assert sum(bunched["full_counts"]) == 4
    assert bunched["full_counts"][4] == 2
    assert bunched["repair_rng_used"] is True


def test_decoder_uniform_repair_and_d_law_exact():
    law = defaultdict(Fraction)
    for a, b in itertools.product(range(4), repeat=2):
        occupation = tuple(int(i == a) + int(i == b) for i in range(4))
        choices = _repair_subsets(occupation)
        for choice in choices:
            def choose(available, need):
                return [4 + i for i in choice if not occupation[i]]
            decoded = p.decode_counts((0, 1, 2, 3), (4, 5, 6, 7),
                                      (0, 1), occupation, choose)
            observed = tuple(vertex - 4 for vertex in decoded["subset"] if vertex >= 4)
            assert observed == choice
            law[observed] += Fraction(1, 16 * len(choices))
    assert len(law) == 6
    assert set(law.values()) == {Fraction(1, 6)}
    assert sum(law.values()) == 1
    assert [sum(value for subset, value in law.items() if v in subset)
            for v in range(4)] == [Fraction(1, 2)] * 4


def test_decoder_preserves_port_and_vertex_count_mappings():
    source, target = (6, 1, 4, 3), (0, 7, 2, 5)
    calls = []
    def choose(available, need):
        calls.append((tuple(available), need))
        return available[:need]
    result = p.decode_counts(source, target, (1, 3), (0, 2, 0, 0), choose)
    assert calls == [((0, 2, 5), 1)]
    assert result["full_counts"] == [1, 0, 1, 0, 0, 2, 0, 0]
    assert result["vertex_counts"] == [0, 0, 0, 0, 1, 0, 1, 2]
    assert tuple(result["subset"]) == (0, 4, 6, 7)
    assert result["R"] == [1, 3]
    assert result["r"] == 2 and result["h"] == 1


def test_eta_zero_all_r_combinatorial_null():
    for k in (2, 4):
        for r in range(k + 1):
            for h in range(r + 1):
                probability = Fraction(math.comb(r, h),
                                       math.comb(k, h) * math.comb(k - h, r - h))
                assert probability == Fraction(1, math.comb(k, r))


def test_exact_r2_mean_difference_independent_fraction():
    means = [_exact_r2_mean(z) for z in (ONE, I, (-ONE[0], ZERO[1]))]
    assert means[0] - means[2] == Fraction(-8, 225)
    assert 2 * means[1] == means[0] + means[2]
    for z in (ONE, I, (-ONE[0], ZERO[1])):
        matrix = _fraction_w(z)
        for source in itertools.combinations(range(4), 2):
            assert sum(_probability_two(matrix, source, occupation)
                       for occupation in _occupations_two(4)) == 1


def test_flat_r2_uniform_loading_cancels_and_marginals_are_phase_blind():
    averaged = []
    for z in (ONE, I, (-ONE[0], ZERO[1])):
        matrix = _fraction_w(z)
        law = defaultdict(Fraction)
        for source in itertools.combinations(range(4), 2):
            marginals = [Fraction(0)] * 4
            for occupation in _occupations_two(4):
                probability = _probability_two(matrix, source, occupation)
                choices = _repair_subsets(occupation)
                for choice in choices:
                    mass = probability / len(choices)
                    law[choice] += mass / 6
                    for vertex in choice:
                        marginals[vertex] += mass
            assert marginals == [Fraction(1, 2)] * 4
        averaged.append(dict(law))
    assert averaged[0] == averaged[1] == averaged[2]
    assert set(averaged[0].values()) == {Fraction(1, 6)}


def test_decoder_rejects_malformed_counts_without_retry():
    source, target = (0, 1, 2, 3), (4, 5, 6, 7)
    forbidden = lambda available, need: pytest.fail("invalid record invoked repair")
    for removed, counts in (((0, 0), (2, 0, 0, 0)),
                            ((4,), (1, 0, 0, 0)),
                            ((0,), (0, 0, 0, 0)),
                            ((0,), (-1, 2, 0, 0)),
                            ((0,), (True, 0, 0, 0)),
                            ((0,), (1, 0, 0))):
        with pytest.raises(p.RetainedFailure):
            p.decode_counts(source, target, removed, counts, forbidden)


def test_all_swap_candidates_match_independent_scalar_cuts():
    graph = ((0, 7, 0, 1), (7, 0, 2, 0), (0, 2, 0, 5), (1, 0, 5, 0))
    rank = (2, 0, 3, 1)
    source = (0, 2)
    rows = p.all_swap_candidates(graph, source, rank, _scalar_cut(graph, source))
    assert len(rows) == 4
    assert len({(row["removed"], row["added"]) for row in rows}) == 4
    for row in rows:
        assert row["cut"] == _scalar_cut(graph, row["subset"])
        assert row["cut"] == _scalar_cut(graph, source) + row["delta"]
        assert len(row["subset"]) == 2


def test_packbits_little_round_trip_padding_and_balance_guards():
    packed = p.pack_mask((0, 2, 5), 6)
    assert packed == bytes((37,))
    assert tuple(p.unpack_mask(packed, 6)) == (0, 2, 5)
    for invalid in (bytes((229,)), bytes((3,)), bytes((37, 0))):
        with pytest.raises(p.RetainedFailure):
            p.unpack_mask(invalid, 6)


def test_quench_returns_best_scored_and_couples_complements():
    graph = ((0, 7, 0, 1), (7, 0, 2, 0), (0, 2, 0, 5), (1, 0, 5, 0))
    rank = (2, 0, 3, 1)
    calls = []
    def score(subset):
        value = _scalar_cut(graph, subset)
        calls.append((tuple(subset), value))
        return value
    first = p.bounded_descent(graph, (0, 2), rank, 1, score)
    minimum = min(value for _, value in calls)
    assert first["cut"] == minimum
    assert first["cut"] == _scalar_cut(graph, first["subset"])
    other = p.bounded_descent(graph, (1, 3), rank, 1,
                              lambda subset: _scalar_cut(graph, subset))
    assert first["cut"] == other["cut"]
    assert tuple(first["subset"]) == tuple(other["subset"])
    assert tuple(p.canonical(first["subset"], 4, rank)) == tuple(first["subset"])


def test_quench_best_is_not_last_and_cap_is_not_optimality():
    graph = ((0, 0, 0, 0),) * 4
    calls = []
    def mock_score(subset):
        value = 1 if not calls else 8
        calls.append((tuple(subset), value))
        return value
    result = p.bounded_descent(graph, (0, 1), (0, 1, 2, 3), 1,
                               mock_score, initial_cut=10)
    assert len(calls) == 4
    assert result["cut"] == 1
    assert result["cut"] != calls[-1][1]
    assert result["local_optimum"] is False


def test_duration_difference_has_unknown_endpoints_and_cpu():
    outer = {"id": "factory0", "kind": "OBSERVED_SPAN", "wall_seconds": 0.5,
             "cpu_seconds": 0.3, "start_wall": 4.0, "end_wall": 4.5,
             "start_cpu": 2.0, "end_cpu": 2.3}
    result = p.duration_difference(outer, 0.2, "difference0")
    assert result["kind"] == "DURATION_DIFF"
    assert result["outer_ref"] == "factory0"
    assert result["wall_seconds"] == pytest.approx(0.3, abs=1e-15)
    assert result["reported_setup_wall_seconds"] == 0.2
    assert result["cpu_seconds"] is None
    assert all(result[key] is None for key in
               ("start_wall", "end_wall", "start_cpu", "end_cpu"))
    assert "formula" in result
    assert outer["cpu_seconds"] == 0.3


def test_duration_difference_rejects_inconsistent_reported_wall():
    outer = {"id": "factory0", "kind": "OBSERVED_SPAN", "wall_seconds": 0.5,
             "cpu_seconds": 0.3, "start_wall": 4.0, "end_wall": 4.5,
             "start_cpu": 2.0, "end_cpu": 2.3}
    for reported in (-0.1, 0.6, float("nan"), float("inf")):
        with pytest.raises(p.RetainedFailure):
            p.duration_difference(outer, reported, "bad")


def test_conservative_call_boundary_binding_preserves_direct_and_rejects_late():
    difference = p.call_boundary_difference(2.0, 3.0, 0.25, 0.5, 0.75, 1.0)
    assert difference["kind"] == "CONSERVATIVE_DURATION_DIFF"
    assert difference["cpu_seconds"] == 1.0 and difference["wall_seconds"] == 1.5
    assert all(difference[key] is None for key in
               ("start_cpu", "end_cpu", "start_wall", "end_wall"))
    assert "entry plus return" in difference["scope"]
    for values in ((-0.1, 1, 0, 0, 0, 0),
                   (1, 1, 0.6, 0.6, 0.5, 0.5),
                   (1, 1, 0.5, 0.5, 0.5000000001, 0.5)):
        with pytest.raises(p.RetainedFailure):
            p.call_boundary_difference(*values)
    for index in range(6):
        for invalid in (float("nan"), float("inf")):
            values = [2.0, 3.0, 0.25, 0.5, 0.75, 1.0]
            values[index] = invalid
            with pytest.raises(p.RetainedFailure):
                p.call_boundary_difference(*values)
    class DelayedReturn(_ScriptedDeps):
        def fast_solver(self, *args, **kwargs):
            result = super().fast_solver(*args, **kwargs)
            self.clock.wall_offset = 0.75
            return result
    deps, writer = DelayedReturn(), p.MemoryWriter()
    spec = _workflow_spec()
    result = p.run_fast_control([[0] * 16 for _ in range(16)], spec["cases"][0],
                                "FAST_RANDOM", 0.5, spec, deps, writer)
    assert result["direct_selected"] is not None
    assert result["direct_selected"]["total_cpu"] <= 0.5
    assert result["direct_selected"]["total_wall"] <= 0.5
    assert result["selected"] is None and result["eligible"] is False
    assert result["first_scan_dual_timely"] is False
    residual = result["call_boundary_difference"]
    assert residual["wall_seconds"] > 0.5
    assert residual["outer_ref"] and residual["direct_adapter_ref"] and residual["reported_ref"]
    assert all(residual[key] is None for key in
               ("start_cpu", "end_cpu", "start_wall", "end_wall"))
    checkpoints = [row for row in writer.records["controls.jsonl"]
                   if row["type"] == "checkpoint"]
    assert checkpoints and all(row["direct_dual_timely"] and not row["dual_timely"]
                               for row in checkpoints)


def test_dual_clock_uses_last_timely_cached_record():
    selected = p.select_dual_checkpoint(_trace(), 0.05, 0.05, 1.0, 16)
    assert selected["index"] == 1
    assert selected["cut"] == 8
    assert selected["mask_hex"] == bytes((127, 1)).hex()
    assert selected["total_cpu"] <= 1 and selected["total_wall"] <= 1
    # The late cost0 must not influence the selected earlier snapshot.
    altered = _trace(cuts=(9, 8, 1))
    assert p.select_dual_checkpoint(altered, 0.05, 0.05, 1.0, 16)["index"] == 1


def test_dual_clock_no_wall_timely_candidate_and_adapter_subtraction():
    assert p.select_dual_checkpoint(_trace(), 0.0, 1.0, 1.0, 16) is None
    selected = p.select_dual_checkpoint(_trace(), 0.8, 0.05, 1.0, 16)
    assert selected["index"] == 1
    assert selected["total_cpu"] == pytest.approx(1.0, abs=1e-15, rel=0)
    assert selected["total_wall"] == pytest.approx(0.25, abs=1e-15, rel=0)


def test_dual_clock_trace_guards(monkeypatch):
    corruptions = []
    nonmonotone = _trace()
    nonmonotone["wall_seconds"] = [0.2, 0.1, 2.0]
    corruptions.append(nonmonotone)
    missing = _trace()
    missing["best_subset_packbits_little"].pop()
    corruptions.append(missing)
    nonfinite = _trace()
    nonfinite["cpu_seconds"][1] = float("nan")
    corruptions.append(nonfinite)
    malformed = _trace()
    malformed["best_subset_packbits_little"][0] = [3]
    corruptions.append(malformed)
    for trace in corruptions:
        with pytest.raises(p.RetainedFailure):
            p.select_dual_checkpoint(trace, 0.0, 0.0, 1.0, 16)
    # Every custom mode gets a whole separate grant and a literal own script.
    # A tiny patched work guard exercises a completed policy unit, not a DEV run.
    def forbidden_hash(*args, **kwargs):
        pytest.fail("qualification must not derive role seeds")
    monkeypatch.setattr(p, "seed_from_role", forbidden_hash)
    monkeypatch.setattr(p, "MAX_WORK", 130)
    spec = _workflow_spec()
    graph = [[0] * 16 for _ in range(16)]
    for mode in p.CUSTOM_MODES:
        deps, writer = _ScriptedDeps(), p.MemoryWriter()
        result = p.run_custom_control(graph, spec["cases"][0], mode, 1.0,
                                      spec, deps, writer)
        assert result["grant"] == 1.0
        assert result["normal_return"] is True
        assert result["stop_reason"] == "work_guard" and result["early_guard"] is True
        assert result["completed_policy_units"] >= 1
        assert result["work"] == 130
        assert result["selected"] is not None
        assert result["selected"]["total_cpu"] <= 1.0
        assert result["selected"]["total_wall"] <= 1.0
        assert result["eligible"] is False
        assert deps.control_roles and deps.control_roles[-1][3] == mode
    # A later strictly cheaper score is cached before its wall clock, then kept
    # as late evidence. The earlier timely snapshot remains the only witness.
    deps, writer = _ScriptedDeps(late_nonstart=True), p.MemoryWriter()
    result = p.run_custom_control(graph, spec["cases"][0], "MULTISWAP", 1.0,
                                  spec, deps, writer)
    assert result["stop_reason"] == "deadline"
    assert result["selected"]["cut"] == 100
    assert result["selected"]["mask_hex"] == bytes((255, 0)).hex()
    assert result["completed_policy_units"] == 0
    checkpoints = [row for row in writer.records["controls.jsonl"]
                   if row["type"] == "checkpoint"]
    assert any(row["cached_best"]["cut"] == 90 and not row["dual_timely"]
               for row in checkpoints)


def test_scientific_cap_retains_partial_stream_and_failure_reserve(tmp_path):
    output = tmp_path / "reserved-evidence"
    writer = p.EvidenceWriter(output, max_bytes=4096, reserve=2048)
    try:
        writer.append("B_ER.jsonl", {"attempt": 0, "count": [0, 2, 0, 0]})
        before = (output / "B_ER.jsonl").read_bytes()
        with pytest.raises(p.RetainedFailure):
            writer.append("B_ER.jsonl", {"oversized": "x" * 4096})
        assert (output / "B_ER.jsonl").read_bytes() == before
        summary = writer.finish(
            {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False,
             "completed_cases": [], "missing_cut": None},
            {"stage": "B_ER", "error": "scientific output cap", "attempt": 1})
    finally:
        writer.close()
    assert summary["status"] == "INCONCLUSIVE_FIRST_FAILURE"
    assert summary["positive_accepted"] is False
    assert json.loads((output / "summary.json").read_text())["missing_cut"] is None
    assert json.loads((output / "failure.json").read_text())["attempt"] == 1
    for name in ("metadata.json", "graphs.json"):
        assert json.loads((output / name).read_text())["status"] == "NOT_RUN"
    assert sum(path.stat().st_size for path in output.iterdir()) <= 4096


def test_scripted_96_attempts_raw_counts_current_refresh_and_tier1_veto():
    deps, writer = _ScriptedDeps(), p.MemoryWriter()
    summary = p.run_workflow(_workflow_spec(), deps, writer)
    assert summary["status"] == "DEV_REJECTED_FIXED_FAST"
    assert summary["positive_accepted"] is False
    assert len(summary["B_cases"]) == 2
    assert len(deps.fast_calls) == 4
    assert summary["completed_B_attempts"] == 96
    assert summary["modeled_full_source_photons"] == 768
    assert summary["tier2"] == []
    assert summary["tier2_status"]["status"] == "NOT_RUN"
    assert [row["initialization"] for row in deps.fast_calls] == [
        "random", "random", "spectral", "spectral"]
    assert all(row["max_proposals"] == 10000 for row in deps.fast_calls)
    assert all(row["budget"] > 0 for row in deps.fast_calls)
    for invocation, result in zip(deps.fast_calls, summary["tier1"]):
        grant = summary["B_cases"][result["case"]]["grant_wall_seconds"]
        assert result["grant"] == grant
        assert invocation["budget"] == pytest.approx(
            max(0, grant - result["adapter_cpu"]), abs=1e-15, rel=0)
        assert result["selected"]["total_cpu"] <= grant
        assert result["selected"]["total_wall"] <= grant
    total_requests = total_outcomes = total_photons = 0
    for stream in ("B_ER.jsonl", "B_RR.jsonl"):
        rows = writer.records[stream]
        requests = [row for row in rows if row["type"] == "attempt_request"]
        outcomes = [row for row in rows if row["type"] == "attempt_outcome"]
        results = [row for row in rows if row["type"] == "case_result"]
        assert len(requests) == len(outcomes) == 48
        assert [(row["chain"], row["step"]) for row in requests] == [
            (chain, step) for chain in range(3) for step in range(16)]
        assert all(sum(row["decoded"]["full_counts"]) == 8 for row in outcomes)
        assert all(row["decoded"]["r"] == sum(row["receiver_counts"])
                   for row in outcomes)
        assert any(0 in row["receiver_counts"] for row in outcomes)
        assert any(max(row["receiver_counts"]) > 1 for row in outcomes)
        assert {row["decoded"]["r"] for row in outcomes} == set(range(9))
        for previous, request in zip(outcomes, requests[1:]):
            if previous["chain"] == request["chain"]:
                assert request["source_order"] == sorted(previous["current_after"]["subset"])
                assert request["current_before"] == previous["current_after"]
        assert any(row["accepted"] for row in outcomes)
        for request, outcome in zip(requests, outcomes):
            if outcome["decoded"]["r"] in (0, 8):
                assert outcome["decoded"]["repair_rng_used"] is False
            assert request["full_source_photons"] == 8
        assert len(results) == 1
        assert results[0]["requested"] == results[0]["completed"] == 48
        assert results[0]["full_source_photons"] == 384
        assert sum(results[0]["r_histogram"]) == 48
        assert all(value > 0 for value in results[0]["r_histogram"])
        scores = [row for row in rows if row["type"] == "score"]
        assert results[0]["scored_candidates"] == len(scores)
        assert results[0]["all_paid_best"]["cut"] == min(row["cut"] for row in scores)
        delta_rows = [row for row in scores if row["method"] == "exact_swap_delta"]
        assert len(delta_rows) >= 48 * 64
        by_batch = defaultdict(list)
        for row in delta_rows:
            by_batch[row["batch"]].append(row["batch_index"])
        assert all(indices == list(range(64)) for indices in by_batch.values())
        total_requests += len(requests)
        total_outcomes += len(outcomes)
        total_photons += results[0]["full_source_photons"]
    assert (total_requests, total_outcomes, total_photons) == (96, 96, 768)
    compile_indices = [i for i, event in enumerate(deps.events) if event[0] == "compile"]
    split_indices = [i for i, event in enumerate(deps.events) if event[0] == "split"]
    assert len(compile_indices) == len(split_indices) == 96
    assert all(compile_index < split_index for compile_index, split_index
               in zip(compile_indices, split_indices))
    ledger = writer.records["paid_ledger.jsonl"]
    paid_events = [row for row in ledger if row["paid"]]
    assert len({row["id"] for row in paid_events}) == len(paid_events)
    for stream in ("B_ER.jsonl", "B_RR.jsonl"):
        case = next(row for row in writer.records[stream] if row["type"] == "case_result")
        paid = [row for row in ledger if row["case"] == case["case"] and row["paid"]]
        assert case["grant_wall_seconds"] == pytest.approx(
            sum(row["wall_seconds"] for row in paid), abs=1e-12, rel=0)
    derived = [row for row in ledger if row["kind"] == "DURATION_DIFF"]
    assert derived and all(row["paid"] and row["cpu_seconds"] is None for row in derived)
    assert all(row["start_wall"] is None and row["end_wall"] is None for row in derived)
    assert all(not row["paid"] for row in ledger
               if row.get("label") in ("factory_total", "serial_native_sample"))


def test_scripted_native_fallback_is_first_failure_with_partial_raw():
    deps, writer = _ScriptedDeps(failed_sample=0), p.MemoryWriter()
    summary = p.run_workflow(_workflow_spec(), deps, writer)
    assert summary["status"] == "INCONCLUSIVE_FIRST_FAILURE"
    assert summary["positive_accepted"] is False
    assert deps.sample_count == 1 and not deps.fast_calls
    rows = writer.records["B_ER.jsonl"]
    assert len([row for row in rows if row["type"] == "attempt_request"]) == 2
    assert len([row for row in rows if row["type"] == "attempt_outcome"]) == 1
    assert not writer.records["B_RR.jsonl"]
    assert "native fallback forbidden" in json.dumps(writer.singles["failure.json"])
    assert "counts" in json.dumps(writer.singles["failure.json"])


def test_scripted_control_exception_overrides_any_partial_veto():
    deps, writer = _ScriptedDeps(failed_fast=1), p.MemoryWriter()
    summary = p.run_workflow(_workflow_spec(), deps, writer)
    assert summary["status"] == "INCONCLUSIVE_FIRST_FAILURE"
    assert summary["positive_accepted"] is False
    assert len(deps.fast_calls) == 2
    assert "scripted FAST exception" in json.dumps(writer.singles["failure.json"])
    assert sum(row["type"] == "attempt_outcome" for stream in ("B_ER.jsonl", "B_RR.jsonl")
               for row in writer.records[stream]) == 96


def test_scripted_mixed_fast_winners_are_not_free_portfolio_veto():
    deps, writer = _ScriptedDeps(mixed_fast=True), p.MemoryWriter()
    summary = p.run_workflow(_workflow_spec(), deps, writer)
    assert summary["status"] == "INCONCLUSIVE_FAST_ELIGIBILITY"
    assert summary["positive_accepted"] is False
    assert len(deps.fast_calls) == 4


def test_native_183_deterministic_amplitudes_and_properties(record_property):
    """The ONLY native item: deterministic Naive probabilities, no sample()."""
    observations = []
    errors = []
    attempted_queries = 0
    thread_record = {"interface": "exqalibur.Config.compute_max_thread_count"}
    planned = []
    hom = [[1 / math.sqrt(2), 1j / math.sqrt(2)],
           [1j / math.sqrt(2), 1 / math.sqrt(2)]]
    for occupation, expected in zip(((2, 0), (1, 1), (0, 2)),
                                     (Fraction(1, 2), Fraction(0), Fraction(1, 2))):
        planned.append({"kind": "HOM", "matrix": hom, "source": (0, 1),
                        "occupation": occupation, "expected": expected})
    for phase_id, z in enumerate((ONE, I, (-ONE[0], ZERO[1]))):
        exact = _fraction_w(z)
        matrix = _complex_w(z)
        for source in itertools.combinations(range(4), 2):
            for occupation in _occupations_two(4):
                planned.append({"kind": "r2", "phase_id": phase_id,
                                "matrix": matrix, "source": source,
                                "occupation": occupation,
                                "expected": _probability_two(exact, source, occupation)})
    try:
        environment = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                       "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
        thread_record["environment_before"] = {name: os.environ.get(name)
                                               for name in environment}
        for name in environment:
            os.environ[name] = "1"
        thread_record["environment_configured"] = {name: os.environ.get(name)
                                                   for name in environment}
        import exqalibur as xq
        thread_record["before"] = int(xq.Config.compute_max_thread_count)
        xq.Config.compute_max_thread_count = 1
        thread_record["configured"] = int(xq.Config.compute_max_thread_count)
        import perceval as pcvl
        from perceval.backends import NaiveBackend
        thread_record["after_import"] = int(xq.Config.compute_max_thread_count)
        for number, point in enumerate(planned):
            amplitude = probability = None
            try:
                backend = NaiveBackend()
                m = len(point["matrix"])
                backend.set_circuit(pcvl.Circuit(m).add(
                    0, pcvl.Unitary(pcvl.Matrix(point["matrix"], use_symbolic=False))))
                backend.set_input_state(pcvl.BasicState(
                    [int(i in point["source"]) for i in range(m)]))
                attempted_queries += 1
                amplitude = complex(backend.prob_amplitude(
                    pcvl.BasicState(list(point["occupation"]))))
                probability = abs(amplitude)**2
                finite = (math.isfinite(amplitude.real) and math.isfinite(amplitude.imag)
                          and math.isfinite(probability))
                row = {"query": number, "kind": point["kind"],
                       "phase_id": point.get("phase_id"),
                       "source": point["source"], "occupation": point["occupation"],
                       "expected_fraction": str(point["expected"]),
                       "amplitude_repr": repr(amplitude),
                       "amplitude_real": amplitude.real if finite else None,
                       "amplitude_imag": amplitude.imag if finite else None,
                       "probability": probability if finite else None}
                observations.append(row)
                if not finite:
                    errors.append({"query": number, "exception_repr": repr(amplitude),
                                   "reason": "nonfinite native amplitude/probability"})
                    break
            except Exception as error:
                errors.append({"query": number, "kind": point["kind"],
                               "phase_id": point.get("phase_id"),
                               "source": point["source"],
                               "occupation": point["occupation"],
                               "amplitude_repr": repr(amplitude),
                               "probability_repr": repr(probability),
                               "exception_repr": repr(error)})
                break
        thread_record["after_queries"] = int(xq.Config.compute_max_thread_count)
        thread_record["environment_after_queries"] = {name: os.environ.get(name)
                                                      for name in environment}
    except Exception as error:
        errors.append({"query": None, "exception_repr": repr(error)})
    # Retain every observation and the first exception BEFORE any assertion.
    record_property("P82a_native_planned_queries", 183)
    record_property("P82a_native_attempted_queries", attempted_queries)
    record_property("P82a_native_actual_queries", len(observations))
    record_property("P82a_native_observations",
                    json.dumps(observations, allow_nan=False, separators=(",", ":")))
    record_property("P82a_native_errors",
                    json.dumps(errors, allow_nan=False, separators=(",", ":")))
    record_property("P82a_native_threads",
                    json.dumps(thread_record, allow_nan=False, separators=(",", ":")))
    assert len(planned) == 183
    assert not errors
    assert attempted_queries == 183
    assert len(observations) == 183
    assert thread_record["configured"] == thread_record["after_import"] == 1
    assert thread_record["after_queries"] == 1
    assert set(thread_record["environment_configured"].values()) == {"1"}
    assert set(thread_record["environment_after_queries"].values()) == {"1"}
    assert all(abs(row["probability"] - float(point["expected"])) <= 2e-12
               for row, point in zip(observations, planned))
