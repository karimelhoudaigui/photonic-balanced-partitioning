"""Prospective P90a qualification fixtures: CODE ONLY until a reviewed slot.

No test in this file has been run during authoring.  The native population is
exactly 254 deterministic Naive amplitudes, with at most four receiver modes and
four photons.  There is no stochastic backend, production role digest, PCG,
DEV graph, real K12 optical matrix, optimizer replay, or QPU dependency here.
The all-attempt workflow is entirely scripted through the frozen dependency API.

The exact oracle below uses Fraction pairs, explicit permutations (r <= 4), and
all uniform repair completions.  It imports no production probability routine.
Scientific imports are local to the explicit tiny numeric/native fixtures.
"""

from array import array
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import importlib.util
from importlib import metadata
from itertools import combinations, permutations, product
import json
import math
import os
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/P90a_source_bound_nonflat_veto.py"
SPEC = ROOT / "research/P90a_execution_spec.json"
THREAD_ENV = (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
)
NATIVE_ATOL = 2e-12
ZERO = (F(0), F(0))
ONE = (F(1), F(0))
I = (F(0), F(1))


def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def qmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def qabs2(a):
    return a[0] * a[0] + a[1] * a[1]


def qpow(a, exponent):
    value = ONE
    for _ in range(exponent):
        value = qmul(value, a)
    return value


def permanent_pair(matrix):
    """Explicit Gaussian-rational permanent; never a native/library permanent."""
    n = len(matrix)
    assert n <= 4 and all(len(row) == n for row in matrix)
    result = ZERO
    for order in permutations(range(n)):
        term = ONE
        for row, col in enumerate(order):
            term = qmul(term, matrix[row][col])
        result = qadd(result, term)
    return result


def occupations(modes, photons):
    """All weak compositions, in a fixed lexicographic order, including zeros."""
    if modes == 1:
        return ((photons,),)
    return tuple(
        (first,) + tail
        for first in range(photons + 1)
        for tail in occupations(modes - 1, photons - first)
    )


def subsets(modes):
    return tuple(s for r in range(modes + 1) for s in combinations(range(modes), r))


@dataclass(frozen=True)
class ExactUnitary:
    # Each physical column is numerator / sqrt(column_denominator).
    numerator: tuple
    column_denominator: tuple

    @property
    def modes(self):
        return len(self.numerator)

    def floating(self):
        return [
            [complex(*entry) / math.sqrt(self.column_denominator[j])
             for j, entry in enumerate(row)]
            for row in self.numerator
        ]


def hom_unitary():
    return ExactUnitary(((ONE, ONE), (ONE, (-F(1), F(0)))), (2, 2))


def flat_unitary():
    return ExactUnitary(
        tuple(tuple(qpow(I, a * j) for j in range(4)) for a in range(4)),
        (4, 4, 4, 4),
    )


def toy_unitary():
    return ExactUnitary(
        ((ONE, ONE, ZERO, ZERO), (ONE, (-F(1), F(0)), ZERO, ZERO),
         (ZERO, ZERO, ONE, ZERO), (ZERO, ZERO, ZERO, ONE)),
        (2, 2, 1, 1),
    )


def exact_amplitude_squared(unitary, removed, counts):
    assert len(removed) <= 4 and unitary.modes <= 4
    assert len(counts) == unitary.modes and sum(counts) == len(removed)
    rows = tuple(a for a, count in enumerate(counts) for _ in range(count))
    numerator = permanent_pair(
        tuple(tuple(unitary.numerator[a][j] for j in removed) for a in rows)
    )
    denominator = math.prod(unitary.column_denominator[j] for j in removed)
    denominator *= math.prod(math.factorial(value) for value in counts)
    return numerator, F(denominator), qabs2(numerator) / denominator


def exact_bosonic_law(unitary, removed):
    return {
        counts: exact_amplitude_squared(unitary, removed, counts)[2]
        for counts in occupations(unitary.modes, len(removed))
    }


def exact_distinguishable_law(unitary, removed):
    """Enumerate labeled particle routes, rather than reuse the permanent."""
    law = {counts: F(0) for counts in occupations(unitary.modes, len(removed))}
    for assignment in product(range(unitary.modes), repeat=len(removed)):
        probability = F(1)
        for receiver, source in zip(assignment, removed):
            probability *= qabs2(unitary.numerator[receiver][source])
            probability /= unitary.column_denominator[source]
        counts = tuple(assignment.count(a) for a in range(unitary.modes))
        law[counts] += probability
    return law


def exact_group2_law(unitary, removed):
    """Independent convolution of blocks {0,1}, {2}, {3}, for the toy only."""
    assert unitary == toy_unitary()
    law = {(0, 0, 0, 0): F(1)}
    for block in ((0, 1), (2,), (3,)):
        occupied = tuple(j for j in block if j in removed)
        # The active two-photon block is evaluated independently of the full law.
        partial = exact_bosonic_law(unitary, occupied)
        combined = defaultdict(F)
        for before, before_probability in law.items():
            for after, after_probability in partial.items():
                combined[tuple(a + b for a, b in zip(before, after))] += (
                    before_probability * after_probability
                )
        law = dict(combined)
    complete = {counts: F(0) for counts in occupations(4, len(removed))}
    complete.update(law)
    return complete


def all_repairs(counts):
    """Return every repaired receiver subset and its exact completion mass."""
    r = sum(counts)
    support = tuple(a for a, count in enumerate(counts) if count)
    unused = tuple(a for a, count in enumerate(counts) if not count)
    deficit = r - len(support)
    completions = tuple(combinations(unused, deficit))
    assert completions
    return tuple((tuple(sorted(support + fill)), F(1, len(completions)))
                 for fill in completions)


def repaired_law(raw_law):
    repaired = defaultdict(F)
    for counts, probability in raw_law.items():
        for receiving, completion_mass in all_repairs(counts):
            repaired[receiving] += probability * completion_mass
    return dict(repaired)


def raw_joint_law(unitary, law_function):
    # At p=1/2 EVERY labeled source subset has unconditioned mass 1/16.
    joint = {}
    for removed in subsets(4):
        law = law_function(unitary, removed)
        assert sum(law.values()) == 1
        for counts, probability in law.items():
            for receiving, repair_mass in all_repairs(counts):
                key = (removed, counts, receiving)
                joint[key] = probability * repair_mass / 16
    return joint


def one_edge_raw_mean(joint):
    return sum(
        probability * int((2 not in removed) != (2 in receiving))
        for (removed, _counts, receiving), probability in joint.items()
    )


def _native_population():
    points = []
    for counts in occupations(2, 2):
        points.append(("HOM", (0, 1), counts))
    for removed in combinations(range(4), 2):
        for counts in occupations(4, 2):
            points.append(("flat", removed, counts))
    for removed in subsets(4)[1:]:
        for counts in occupations(4, len(removed)):
            points.append(("toy", removed, counts))
    return tuple(points)


NATIVE_POINTS = _native_population()
NATIVE_IDS = tuple(
    family + "_R" + "".join(map(str, removed)) + "_Y" + "".join(map(str, counts))
    for family, removed, counts in NATIVE_POINTS
)


@pytest.fixture(scope="module")
def target():
    """Load only the P90a module, not P82 or any scientific/native dependency."""
    name = "p90a_qualification_target"
    descriptor = importlib.util.spec_from_file_location(name, SOURCE)
    module = importlib.util.module_from_spec(descriptor)
    sys.modules[name] = module
    try:
        descriptor.loader.exec_module(module)
        yield module
    finally:
        sys.modules.pop(name, None)


@pytest.fixture(scope="module")
def literal_spec():
    return json.loads(SPEC.read_text(encoding="utf-8"))


def _actual_identity(module):
    path = Path(module.__file__).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _read_native_thread(stack):
    try:
        return {"value": int(stack.xq.Config.compute_max_thread_count), "error_repr": None}
    except Exception as error:
        return {"value": None, "error_repr": repr(error)}


def _native_provenance(np, scipy, pcvl, xq):
    """Archive portable actual identities; never enforce a workstation path."""
    import perceval.backends._naive as naive
    import perceval.backends._abstract_backends as abstract
    import numpy.linalg._linalg as linalg
    import numpy.linalg._umath_linalg as native_linalg
    import numpy._core._multiarray_umath as native_array
    import scipy.linalg._matfuncs as matfuncs
    import scipy.linalg._matfuncs_expm as native_expm
    import exqalibur.exqalibur as native_xq
    return {
        "python": {"version": sys.version, "executable": sys.executable,
                   "resolved": str(Path(sys.executable).resolve()),
                   "sha256": hashlib.sha256(Path(sys.executable).resolve().read_bytes()).hexdigest()},
        "versions": {name: metadata.version(name) for name in
                     ("numpy", "scipy", "perceval-quandela", "exqalibur", "pytest")},
        "critical_python": {name: _actual_identity(module) for name, module in
                            (("naive", naive), ("abstract", abstract),
                             ("linalg", linalg), ("matfuncs", matfuncs))},
        "actual_modules": {name: _actual_identity(module) for name, module in
                           (("numpy", np), ("scipy", scipy),
                            ("perceval", pcvl), ("exqalibur", xq))},
        "actual_native": {name: _actual_identity(module) for name, module in
                          (("exqalibur", native_xq), ("linalg", native_linalg),
                           ("array", native_array), ("expm", native_expm))},
        "spec_schema": json.loads(SPEC.read_text(encoding="utf-8"))["schema"],
        "spec_sha256": hashlib.sha256(SPEC.read_bytes()).hexdigest(),
    }


@pytest.fixture(scope="module")
def native_stack():
    """Only deterministic Naive is constructed; setup errors become evidence."""
    stack = SimpleNamespace(error=None, provenance=None)
    stack.environment_before = {name: os.environ.get(name) for name in THREAD_ENV}
    for name in THREAD_ENV:
        os.environ[name] = "1"
    stack.environment_configured = {name: os.environ.get(name) for name in THREAD_ENV}
    try:
        import exqalibur as xq
        stack.xq = xq
        stack.native_before = int(xq.Config.compute_max_thread_count)
        xq.Config.compute_max_thread_count = 1
        stack.native_configured = int(xq.Config.compute_max_thread_count)
        import numpy as np
        import scipy
        import perceval as pcvl
        from perceval.backends import NaiveBackend
        stack.np, stack.pcvl, stack.backend_type = np, pcvl, NaiveBackend
        stack.native_after_imports = int(xq.Config.compute_max_thread_count)
        stack.provenance = _native_provenance(np, scipy, pcvl, xq)
    except Exception as error:
        stack.error = error
    yield stack
    # Read back after all 254 point items; individual items also archive readbacks.
    stack.environment_end = {name: os.environ.get(name) for name in THREAD_ENV}
    if hasattr(stack, "xq"):
        stack.native_end = _read_native_thread(stack)


@pytest.mark.parametrize("family,removed,counts", NATIVE_POINTS, ids=NATIVE_IDS)
def test_native_naive_point(family, removed, counts, native_stack, literal_spec,
                            record_property):
    """One native amplitude call per item, including zero-probability outputs."""
    unitary = {"HOM": hom_unitary, "flat": flat_unitary, "toy": toy_unitary}[family]()
    numerator, denominator, expected_probability = exact_amplitude_squared(
        unitary, removed, counts,
    )
    expected_amplitude = complex(*numerator) / math.sqrt(denominator)
    observation = {
        "family": family, "removed": removed, "counts": counts,
        "expected_amplitude": [expected_amplitude.real, expected_amplitude.imag],
        "expected_probability_exact": str(expected_probability),
        "abs_tolerance": NATIVE_ATOL, "relative_tolerance": 0,
        "max_modes": 4, "max_photons": 4, "native_calls_planned": 1,
        "environment_before": native_stack.environment_before,
        "environment_configured": native_stack.environment_configured,
        "provenance": native_stack.provenance,
        "amplitude": None, "probability": None, "error_repr": None,
    }
    observed = None
    error = native_stack.error
    try:
        if error is not None:
            raise error
        backend = native_stack.backend_type()
        matrix = native_stack.pcvl.Matrix(unitary.floating())
        circuit = native_stack.pcvl.Circuit(unitary.modes).add(
            0, native_stack.pcvl.Unitary(matrix),
        )
        backend.set_circuit(circuit)
        backend.set_input_state(native_stack.pcvl.BasicState(
            [int(j in removed) for j in range(unitary.modes)],
        ))
        observed = complex(backend.prob_amplitude(native_stack.pcvl.BasicState(list(counts))))
        observation["amplitude"] = [observed.real, observed.imag]
        observation["probability"] = abs(observed) ** 2
    except Exception as failure:
        error = failure
        observation["error_repr"] = repr(failure)
    finally:
        observation["environment_after"] = {name: os.environ.get(name) for name in THREAD_ENV}
        if hasattr(native_stack, "xq"):
            observation["native_after_readback"] = _read_native_thread(native_stack)
            observation["native_after"] = observation["native_after_readback"]["value"]
            observation["native_before"] = getattr(native_stack, "native_before", None)
            observation["native_configured"] = getattr(native_stack, "native_configured", None)
            observation["native_after_imports"] = getattr(native_stack, "native_after_imports", None)
        # Evidence is retained BEFORE EVERY numeric/thread/version assertion.
        record_property("p90a_native_observation", json.dumps(observation, sort_keys=True))
    assert error is None, repr(error)
    assert all(value == "1" for value in observation["environment_after"].values())
    assert observation["native_configured"] == observation["native_after_imports"] == 1
    assert observation["native_after"] == 1
    for package, actual in native_stack.provenance["versions"].items():
        assert actual == literal_spec["software"][package]
    assert observed == pytest.approx(expected_amplitude, abs=NATIVE_ATOL, rel=0)
    assert abs(observed) ** 2 == pytest.approx(float(expected_probability), abs=NATIVE_ATOL, rel=0)


def test_native_population_is_exactly_254_and_vacuum_is_analytic():
    assert len(NATIVE_POINTS) == len(set(NATIVE_IDS)) == 254
    assert NATIVE_IDS == EXPECTED_NATIVE_IDS
    assert sum(family == "HOM" for family, _, _ in NATIVE_POINTS) == 3
    assert sum(family == "flat" for family, _, _ in NATIVE_POINTS) == 60
    assert sum(family == "toy" for family, _, _ in NATIVE_POINTS) == 191
    assert all(1 <= len(removed) <= 4 and 2 <= len(counts) <= 4
               for _, removed, counts in NATIVE_POINTS)
    assert exact_bosonic_law(toy_unitary(), ()) == {(0, 0, 0, 0): F(1)}
    assert len(occupations(4, 1)) == 4
    assert len(occupations(4, 2)) == 10
    assert len(occupations(4, 3)) == 20
    assert len(occupations(4, 4)) == 35


def test_fraction_pair_permanent_preserves_complex_phase_and_factorials():
    assert permanent_pair(()) == ONE
    assert permanent_pair(((I,),)) == I
    assert permanent_pair(((ONE, I), (I, ONE))) == ZERO
    unitary = hom_unitary()
    assert exact_bosonic_law(unitary, (0, 1)) == {
        (0, 2): F(1, 2), (1, 1): F(0), (2, 0): F(1, 2),
    }
    assert exact_amplitude_squared(unitary, (0, 1), (0, 2))[0] == (-F(2), F(0))


def test_flat_fixed_R_inclusion_and_uniform_R_pair_mean_null(record_property):
    unitary = flat_unitary()
    average_pair_difference = defaultdict(F)
    fixed_R_differences = []
    # An arbitrary fixed eight-vertex graph supplies nonzero S/T and T/T terms.
    weights = {(s, 4 + a): 1 + ((3 * s + a) % 5) for s in range(4) for a in range(4)}
    weights.update({(4 + a, 4 + b): 1 + ((a + 2 * b) % 5)
                    for a, b in combinations(range(4), 2)})
    mean_difference = F(0)
    for removed in combinations(range(4), 2):
        b_law = repaired_law(exact_bosonic_law(unitary, removed))
        d_law = repaired_law(exact_distinguishable_law(unitary, removed))
        assert sum(b_law.values()) == sum(d_law.values()) == 1
        for a in range(4):
            assert sum((b_law[y] - d_law[y]) for y in b_law if a in y) == 0
        fixed_difference = {y: b_law[y] - d_law[y] for y in b_law}
        fixed_R_differences.append((removed, {str(y): str(p) for y, p in fixed_difference.items()}))
        for receiving, delta in fixed_difference.items():
            average_pair_difference[receiving] += delta / 6
            chosen = (set(range(4)) - set(removed)) | {4 + a for a in receiving}
            cut = sum(weight for (a, b), weight in weights.items() if (a in chosen) != (b in chosen))
            mean_difference += delta * cut / 6
    record_property("p90a_flat_exact_fixed_R_pair_differences", json.dumps(fixed_R_differences))
    assert all(value == 0 for value in average_pair_difference.values())
    assert mean_difference == 0
    # A fixed-R receiving pair law need not coincide; joint (R,Y) equality and
    # nonlinear-quench-history equality are deliberately NOT the flat null.
    assert any(value != "0" for _, row in fixed_R_differences for value in row.values())


def test_toy_all_16_R_all_counts_all_fills_exact_raw_mean_and_group2_veto(record_property):
    unitary = toy_unitary()
    b_joint = raw_joint_law(unitary, exact_bosonic_law)
    d_joint = raw_joint_law(unitary, exact_distinguishable_law)
    group_joint = raw_joint_law(unitary, exact_group2_law)
    sector_records = []
    for removed in subsets(4):
        b = exact_bosonic_law(unitary, removed)
        d = exact_distinguishable_law(unitary, removed)
        group = exact_group2_law(unitary, removed)
        assert b == group
        assert sum(b.values()) == sum(d.values()) == 1
        rb, rd = repaired_law(b), repaired_law(d)
        edge_mean = lambda law: sum(
            probability * int((2 not in removed) != (2 in receiving))
            for receiving, probability in law.items()
        )
        difference = edge_mean(rb) - edge_mean(rd)
        sector_records.append({"R": removed, "B_minus_D": str(difference),
                               "counts": len(b), "fill_points": sum(len(all_repairs(y)) for y in b)})
        if removed == (0, 1):
            assert difference == -F(1, 6)
        elif removed == (0, 1, 3):
            assert difference == -F(1, 4)
        else:
            assert difference == 0
    record_property("p90a_toy_exact_all_R", json.dumps(sector_records, sort_keys=True))
    assert len(sector_records) == 16
    assert sum(b_joint.values()) == sum(d_joint.values()) == sum(group_joint.values()) == 1
    assert b_joint == group_joint  # Entire PNR/fill joint law, not merely a mean.
    assert one_edge_raw_mean(b_joint) - one_edge_raw_mean(d_joint) == -F(5, 192)
    assert one_edge_raw_mean(b_joint) - one_edge_raw_mean(group_joint) == 0
    assert not (one_edge_raw_mean(b_joint) < one_edge_raw_mean(group_joint))


SMALL_GRAPH = (
    (0, 1, 4, 0), (1, 0, 2, 3), (4, 2, 0, 5), (0, 3, 5, 0),
)


def independent_cut(graph, mask):
    return sum(graph[a][b] for a in range(len(graph)) for b in range(a + 1, len(graph))
               if bool(mask & (1 << a)) != bool(mask & (1 << b)))


def independent_canonical(mask, n, rank):
    first = min(range(n), key=lambda v: rank[v])
    return mask if mask & (1 << first) else mask ^ ((1 << n) - 1)


def independent_batch(target, graph, mask, rank, base_cut):
    n, k = len(graph), len(graph) // 2
    inside = tuple(sorted((v for v in range(n) if mask & (1 << v)), key=lambda v: rank[v]))
    outside = tuple(sorted((v for v in range(n) if not mask & (1 << v)), key=lambda v: rank[v]))
    masks = [independent_canonical(mask ^ (1 << i) ^ (1 << a), n, rank)
             for i in inside for a in outside]
    return target.CutBatch(n, mask, base_cut, inside, outside,
                           array("q", [independent_cut(graph, value) for value in masks]),
                           array("I", masks))


def test_numeric_caps_accept_exact_numeric_90_0_but_reject_nonfinite_coercions(target, literal_spec):
    assert target.numeric_cap(90, 90, "wall") == 90
    assert target.numeric_cap(90.0, 90, "wall") == 90
    assert target.numeric_cap(60.0, 60, "cpu") == 60
    for bad in (True, False, "90", None, float("nan"), float("inf"), 90.0000000001, 89.9999999999):
        with pytest.raises(target.AuditFailure):
            target.numeric_cap(bad, 90, "wall")
    numeric_metadata = json.loads(json.dumps(literal_spec))
    numeric_metadata["limits"]["wall_seconds"] = 90.0
    target.validate_spec(numeric_metadata)
    # An exact numeric cap is separate from a cut, mask, count or loop bound.
    for key in ("K", "chains", "steps"):
        malformed = json.loads(json.dumps(numeric_metadata))
        malformed[key] = float(malformed[key])
        with pytest.raises(target.AuditFailure):
            target.validate_spec(malformed)


def test_masks_graphs_and_all_tiny_cuts_are_strict_integer(target):
    rank = (0, 1, 2, 3)
    assert target.validate_graph(SMALL_GRAPH) is not None
    for chosen in combinations(range(4), 2):
        mask = sum(1 << v for v in chosen)
        assert target.mask_from_subset(chosen, 4) == mask
        assert tuple(target.mask_vertices(mask, 4)) == chosen
        assert target.read_mask_hex(target.mask_hex(mask, 4), 4) == mask
        assert target.scalar_cut(SMALL_GRAPH, mask) == independent_cut(SMALL_GRAPH, mask)
        assert target.canonical_mask(mask, 4, rank) == independent_canonical(mask, 4, rank)
    for bad in (True, 3.0, "3", -1, 16, 1):
        with pytest.raises(target.AuditFailure):
            target.canonical_mask(bad, 4, rank)
    for bad in ("", "f0", "0001", "gg", "0x03"):
        with pytest.raises(target.AuditFailure):
            target.read_mask_hex(bad, 4)
    for bad_subset in ((0, 0), (0, 4), (False, 1), (0.0, 1)):
        with pytest.raises(target.AuditFailure):
            target.mask_from_subset(bad_subset, 4)
    for bad_graph in (
        ((0, 1), (0, 0)), ((1, 0), (0, 0)), ((0, -1), (-1, 0)),
        ((0, 1.0), (1.0, 0)), ((0, True), (True, 0)), ((0,),),
    ):
        with pytest.raises(target.AuditFailure):
            target.validate_graph(bad_graph)


def test_tiny_every_swap_materializes_canonical_masks_and_target_row_M_transpose(target):
    for rank in ((0, 1, 2, 3), (2, 0, 3, 1)):
        for chosen in combinations(range(4), 2):
            source = independent_canonical(sum(1 << v for v in chosen), 4, rank)
            base = independent_cut(SMALL_GRAPH, source)
            expected = independent_batch(target, SMALL_GRAPH, source, rank, base)
            actual = target.exact_swap_batch(SMALL_GRAPH, source, rank, base)
            assert actual.inside == expected.inside and actual.outside == expected.outside
            assert actual.cuts.typecode == "q" and actual.masks.typecode == "I"
            assert list(actual.cuts) == list(expected.cuts)
            assert list(actual.masks) == list(expected.masks)
            assert actual.count == 4
            assert actual.best_index() == min(range(4), key=lambda index: expected.cuts[index])
            matrix = target.m_matrix(actual)
            assert [list(row) for row in matrix] == [
                [actual.cuts[i * 2 + a] - base for i in range(2)] for a in range(2)
            ]
    # Asymmetry makes a missing transpose observable independently of the loops.
    batch = target.CutBatch(4, 3, 20, (0, 1), (2, 3),
                            array("q", (21, 22, 23, 24)), array("I", (5, 9, 9, 5)))
    assert [list(row) for row in target.m_matrix(batch)] == [[1, 3], [2, 4]]


def test_tiny_2x2_compiler_matches_independent_pauli_exponential_and_transport(target, native_stack, record_property):
    # Explicitly registered future tiny SciPy fixture; never a real K12 matrix.
    assert native_stack.error is None, repr(native_stack.error)
    import numpy as np
    from scipy.linalg import expm
    batch = target.CutBatch(4, 3, 20, (0, 1), (2, 3),
                            array("q", (21, 22, 23, 24)), array("I", (5, 9, 9, 5)))
    compiled = target.compile_feature(batch, np, expm)
    # M=[[1,3],[2,4]], H=[[1,2.5+.5j],[2.5-.5j,4]].
    expected_H = [[1 + 0j, 2.5 + .5j], [2.5 - .5j, 4 + 0j]]
    h0, radius = 2.5, math.sqrt(8.75)
    eigenvalues = (h0 - radius, h0 + radius)
    d = max(1, *(abs(value) for value in eigenvalues))
    phase = complex(math.cos(h0 / d), -math.sin(h0 / d))
    c, s = math.cos(radius / d), math.sin(radius / d) / radius
    analytic = [[phase * (c * int(a == b) - 1j * s *
                 (expected_H[a][b] - h0 * int(a == b))) for b in range(2)] for a in range(2)]
    observation = {"M": [[1, 3], [2, 4]], "H": [[repr(z) for z in row] for row in expected_H],
                   "eigenvalues": eigenvalues, "d": d,
                   "actual_V": [[repr(complex(z)) for z in row] for row in compiled.V],
                   "analytic_V": [[repr(z) for z in row] for row in analytic],
                   "numpy": metadata.version("numpy"), "scipy": metadata.version("scipy")}
    record_property("p90a_tiny_compiler", json.dumps(observation, sort_keys=True))
    assert compiled.source_order == (0, 1) and compiled.target_order == (2, 3)
    assert np.asarray(compiled.H) == pytest.approx(np.asarray(expected_H), abs=2e-12, rel=0)
    assert list(compiled.eigenvalues) == pytest.approx(eigenvalues, abs=2e-12, rel=0)
    assert compiled.d == pytest.approx(d, abs=2e-12, rel=0)
    assert np.asarray(compiled.V) == pytest.approx(np.asarray(analytic), abs=2e-12, rel=0)
    routed = target.transport_feature(compiled, (1, 0), (3, 2))
    assert np.asarray(routed.W) == pytest.approx(np.asarray(analytic)[[1, 0]][:, [1, 0]], abs=2e-12, rel=0)
    assert compiled.v_gram_error <= 3e-12
    assert routed.w_gram_error <= 3e-12 and routed.frame_gram_error <= 3e-12
    # Null/monomial features are retained; flatness is never a pass/fail guard.
    null = target.CutBatch(4, 3, 0, (0, 1), (2, 3), array("q", [0] * 4), array("I", (5, 9, 9, 5)))
    identity = target.compile_feature(null, np, expm)
    assert np.asarray(identity.V) == pytest.approx(np.eye(2), abs=2e-12, rel=0)


def test_tiny_compiler_guard_fails_without_reorthogonalization(target, native_stack):
    assert native_stack.error is None, repr(native_stack.error)
    import numpy as np
    batch = target.CutBatch(4, 3, 0, (0, 1), (2, 3), array("q", [0] * 4), array("I", (5, 9, 9, 5)))
    for bad in (np.zeros((2, 2), dtype=complex), np.full((2, 2), np.nan, dtype=complex)):
        with pytest.raises(target.AuditFailure):
            target.compile_feature(batch, np, lambda _matrix, bad=bad: bad)


def test_decode_all_r_all_occupations_and_every_uniform_completion(target):
    source_ports, target_ports = (2, 0, 3, 1), (6, 4, 7, 5)
    for removed in subsets(4):
        for counts in occupations(4, len(removed)):
            available = tuple(target_ports[a] for a, count in enumerate(counts) if count == 0)
            deficit = len(removed) - sum(count > 0 for count in counts)
            for fill in combinations(sorted(available), deficit):
                calls = []
                def choose(unused, count):
                    calls.append((tuple(unused), count))
                    return fill
                decoded = target.repair_counts(source_ports, target_ports, removed, counts, choose)
                kept = tuple(int(port not in removed) for port in range(4))
                expected_mask = sum(1 << source_ports[j] for j in range(4) if j not in removed)
                expected_mask |= sum(1 << target_ports[a] for a, count in enumerate(counts) if count)
                expected_mask |= sum(1 << vertex for vertex in fill)
                assert decoded.mask == expected_mask and decoded.mask.bit_count() == 4
                assert tuple(decoded.kept_counts) == kept
                assert tuple(decoded.receiver_counts) == counts
                assert tuple(decoded.full_counts) == kept + counts
                assert sum(decoded.full_counts) == 4
                assert tuple(decoded.vertex_counts) == tuple(
                    (kept[source_ports.index(v)] if v in source_ports else counts[target_ports.index(v)])
                    for v in range(8)
                )
                assert tuple(decoded.removed_vertices) == tuple(source_ports[j] for j in removed)
                assert (decoded.r, decoded.h) == (len(removed), sum(count > 0 for count in counts))
                assert tuple(decoded.fill) == fill
                random_fill = 0 < deficit < len(available)
                assert bool(decoded.repair_used) == random_fill
                assert len(calls) == int(random_fill)
                if calls:
                    assert calls == [(tuple(sorted(available)), deficit)]


def test_decode_rejects_loss_malformed_counts_ports_and_bad_repair_without_loss_fill(target):
    calls = []
    def forbidden(*args):
        calls.append(args)
        raise AssertionError("repair RNG must not hide invalid/lost counts")
    for removed, counts in (
        ((0, 1), (1, 0, 0, 0)), ((0,), (2, 0, 0, 0)),
        ((0,), (-1, 2, 0, 0)), ((0,), (True, 0, 0, 0)),
        ((0,), (1.0, 0, 0, 0)), ((0,), (1, 0, 0)),
        ((0, 0), (2, 0, 0, 0)), ((4,), (1, 0, 0, 0)),
    ):
        with pytest.raises(target.AuditFailure):
            target.repair_counts((0, 1, 2, 3), (4, 5, 6, 7), removed, counts, forbidden)
    assert calls == []
    for fill in ((4,), (5, 5), (99,), (), (5.0,)):
        with pytest.raises(target.AuditFailure):
            target.repair_counts((0, 1, 2, 3), (4, 5, 6, 7), (0, 1), (2, 0, 0, 0),
                                 lambda _available, _count, fill=fill: fill)


def test_decode_all_13_r_keeps_full_source_cost_and_deterministic_fill_boundaries(target):
    # Twelve label ports are allowed here: this is pure integer decoding, with
    # no K12 optical matrix, native source, sampled event, RNG or graph scoring.
    for r in range(13):
        removed, source_ports, target_ports = tuple(range(r)), tuple(range(12)), tuple(range(12, 24))
        for collision in (False, True):
            counts = ((r,) + (0,) * 11 if r and collision else
                      tuple(int(a < r) for a in range(12)))
            calls = []
            def choose(available, need):
                calls.append((tuple(available), need))
                return tuple(available[:need])
            decoded = target.repair_counts(source_ports, target_ports, removed, counts, choose)
            assert decoded.r == r and decoded.mask.bit_count() == 12
            assert sum(decoded.kept_counts) == 12 - r
            assert sum(decoded.receiver_counts) == r and sum(decoded.full_counts) == 12
            assert len(decoded.full_counts) == len(decoded.vertex_counts) == 24
            assert len(calls) == int(collision and 2 <= r <= 11)
            assert decoded.repair_used == bool(calls)


def test_source_import_is_stdlib_only_in_fresh_interpreter(record_property):
    # Future qualification executes this isolated import, never main().  No
    # scientific module may be imported, even accidentally during annotation.
    import subprocess
    script = r'''
import importlib.abc
import importlib.util
from pathlib import Path
import sys
class NoScience(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'numpy','scipy','networkx','perceval','exqalibur'}:
            raise AssertionError('scientific import at module load: ' + fullname)
        if 'P43_' in fullname or 'P50_' in fullname or 'P82' in fullname:
            raise AssertionError('production helper imported at module load: ' + fullname)
sys.meta_path.insert(0, NoScience())
descriptor = importlib.util.spec_from_file_location('p90a_portable_import', Path(sys.argv[1]))
module = importlib.util.module_from_spec(descriptor)
sys.modules[descriptor.name] = module
descriptor.loader.exec_module(module)
assert callable(module.run_workflow)
assert callable(module.compile_feature)
assert not any(name in sys.modules for name in ('numpy','scipy','networkx','perceval','exqalibur'))
'''
    result = subprocess.run([sys.executable, "-I", "-c", script, str(SOURCE)],
                            capture_output=True, text=True, check=False)
    record_property("p90a_portable_import", json.dumps({
        "interpreter": sys.executable, "returncode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr,
    }, sort_keys=True))
    assert result.returncode == 0, result.stderr


class ScriptClock:
    def __init__(self, before_read=None, step=0.001):
        self.value = 0.0
        self.step = step
        self.before_read = before_read
        self.reads = []

    def now(self):
        if self.before_read is not None:
            self.before_read()
        self.value += self.step
        point = (self.value, self.value)
        self.reads.append(point)
        return point


class TinyScoreDependencies:
    def __init__(self, target):
        self.target = target
        self.clock = ScriptClock()
        self.clock_checks = []
        self.cut_calls = []
        self.batch_calls = []
        self.book = None

    def cut(self, graph, mask):
        self.cut_calls.append(mask)
        return independent_cut(graph, mask)

    def swap_batch(self, graph, mask, rank, base_cut, degree=None):
        batch = independent_batch(self.target, graph, mask, rank, base_cut)
        self.batch_calls.append(batch)
        return batch

    def guard(self):
        return None


def test_scorebook_all_144_candidates_and_bests_exist_before_owner_end_clock(target, monkeypatch):
    # Literal mock adjacency only; all scoring is scripted and no K12 M is built.
    graph = tuple((0,) * 24 for _ in range(24))
    rank = tuple(range(24))
    mask = (1 << 12) - 1
    inside, outside = tuple(range(12)), tuple(range(12, 24))
    masks = array("I", [independent_canonical(mask ^ (1 << i) ^ (1 << a), 24, rank)
                         for i in inside for a in outside])
    cuts = array("q", [100] * 144)
    cuts[73] = cuts[130] = 7  # First actual score wins the tie, including duplicates.
    batch = target.CutBatch(24, mask, 101, inside, outside, cuts, masks)
    deps = TinyScoreDependencies(target)
    deps.cut = lambda _graph, _mask: 101
    deps.swap_batch = lambda *_args, **_kwargs: batch
    book = target.ScoreBook(graph, rank, deps, "B_ER")
    book.start_chain(0)
    book.owner_span = "fixture/reset"
    initial = book.scalar(mask, "reset")
    assert initial == 101
    before_count = book.count
    before_pending = len(book.pending)
    checked = []
    def inspect_preclock():
        # The first read opens the owning span; the next observes completed work.
        if book.count == before_count + 144:
            assert cuts.typecode == "q" and len(cuts) == len(masks) == 144
            assert book.global_best.cut == book.chain_best.cut == 7
            assert book.global_best.mask == book.chain_best.mask == masks[73]
            assert book.global_best.sequence == before_count + 73
            checked.append(book.global_best)
    deps.clock.before_read = inspect_preclock
    def forbidden_json(*_args, **_kwargs):
        raise AssertionError("audit JSON constructed inside scoring span")
    writer = target.MemoryWriter()
    ledger = target.Ledger("fixture", deps.clock, writer)
    with monkeypatch.context() as patch:
        patch.setattr(target.json, "dumps", forbidden_json)
        patch.setattr(target.ScalarEvent, "to_record", forbidden_json)
        patch.setattr(target.BatchEvent, "to_record", forbidden_json)
        with ledger.span("compiler", paid=True) as span:
            book.owner_span = span
            actual = book.batch(mask, initial, "compiler_M")
    assert actual is batch
    assert book.count == before_count + 144
    assert len(book.pending) == before_pending + 1
    assert all(not isinstance(event, dict) for event in book.pending)
    assert book.pending[-1].batch.cuts is cuts and book.pending[-1].batch.masks is masks
    assert book.compiler_best == book.global_best
    assert checked
    # Audit flushing may only serialize values that already exist; any rescoring
    # or fresh mask synthesis after the paid clock would create an unpaid witness.
    def forbidden_work(*_args, **_kwargs):
        raise AssertionError("candidate/cut constructed during audit flush")
    with monkeypatch.context() as patch:
        patch.setattr(deps, "cut", forbidden_work)
        patch.setattr(deps, "swap_batch", forbidden_work)
        patch.setattr(target, "scalar_cut", forbidden_work)
        patch.setattr(target, "canonical_mask", forbidden_work)
        patch.setattr(target, "mask_from_subset", forbidden_work)
        book.flush(writer)
    assert book.pending == []
    records = writer.records["B_ER.jsonl"]
    scored = [record for record in records if record.get("type") == "scored_batch"]
    assert len(scored) == 1
    assert scored[0]["count"] == 144
    assert scored[0]["cuts"] == list(cuts)
    assert scored[0]["masks_u32"] == list(masks)
    assert scored[0]["score_start"] == before_count
    assert scored[0]["owner_span"] is not None


def test_bounded_descent_strict_ties_caps_and_no_false_local_optimum(target):
    class Book:
        graph, rank = SMALL_GRAPH, (0, 1, 2, 3)
        def __init__(self, batches):
            self.batches, self.phases = list(batches), []
        def batch(self, mask, value, phase):
            self.phases.append((mask, value, phase))
            return self.batches.pop(0)
    def make(cuts, masks=(5, 9, 9, 5)):
        return target.CutBatch(4, 3, 10, (0, 1), (2, 3), array("q", cuts), array("I", masks))
    equal = Book([make((10, 11, 10, 12))])
    endpoint = target.bounded_descent(equal, 3, 10, 1)
    assert (endpoint.mask, endpoint.cut, endpoint.scans, endpoint.local_optimum) == (3, 10, 1, True)
    capped = Book([make((9, 8, 8, 10))])
    endpoint = target.bounded_descent(capped, 3, 10, 1)
    assert (endpoint.mask, endpoint.cut, endpoint.scans, endpoint.local_optimum) == (9, 8, 1, False)
    no_scan = Book([])
    endpoint = target.bounded_descent(no_scan, 3, 10, 0)
    assert (endpoint.mask, endpoint.cut, endpoint.scans, endpoint.local_optimum) == (3, 10, 0, False)
    assert no_scan.phases == []
    complete = Book([make((9, 8, 8, 10)), make((8, 9, 10, 11))])
    endpoint = target.bounded_descent(complete, 3, 10, 2)
    assert (endpoint.mask, endpoint.cut, endpoint.scans, endpoint.local_optimum) == (9, 8, 2, True)


def _trace(target, n=4):
    return {
        "cpu_seconds": [0.05, 0.20, 0.40, 0.50],
        "wall_seconds": [0.05, 0.30, 0.45, 0.75],
        "best_cut": [12, 10, 8, 7],
        "best_subset_packbits_little": [[3], [5], [9], [3]],
        "proposal_count": [1, 5, 9, 13],
        "stage": ["initialization", "initial_scan", "descent_scan", "anneal"],
    }


def test_dual_clock_selects_last_chronological_cached_witness_never_cpu_only(target):
    trace = _trace(target)
    # Conservative direct+gap costs .1 CPU and .2 WALL; final CPU qualifies,
    # final WALL does not, so the third complete cached checkpoint is selected.
    chosen = target.select_dual_trace(trace, 0.1, 0.2, 0.8, 4)
    assert chosen is not None
    assert chosen["index"] == 2
    assert chosen["cut"] == 8
    assert chosen["mask_hex"] == target.mask_hex(9, 4)
    assert chosen["total_cpu"] == pytest.approx(0.5, abs=1e-15, rel=0)
    assert chosen["total_wall"] == pytest.approx(0.65, abs=1e-15, rel=0)
    assert target.select_dual_trace(trace, 0.1, 0.2, 0.1, 4) is None
    # Repeated equal-time checkpoints retain chronological lastness, not a
    # fabricated post-return reconstruction of the minimum cut.
    trace["cpu_seconds"] = [0.1] * 4
    trace["wall_seconds"] = [0.1] * 4
    assert target.select_dual_trace(trace, 0.1, 0.2, 0.4, 4)["index"] == 3


def test_dual_clock_rejects_malformed_trace_and_never_trims_cap(target):
    for key, value in (
        ("cpu_seconds", [0.1, 0.3, 0.2, 0.4]),
        ("wall_seconds", [0.1, float("nan"), 0.3, 0.4]),
        ("best_cut", [12, 10, 8.0, 7]),
        ("best_cut", [12, 10, 11, 7]),
        ("proposal_count", [1, 5, 4, 13]),
        ("best_subset_packbits_little", [[3], [5], [16], [3]]),
        ("stage", ["initialization", "initial_scan", "invented", "anneal"]),
        ("stage", ["initialization"]),
    ):
        trace = _trace(target)
        trace[key] = value
        with pytest.raises(target.AuditFailure):
            target.select_dual_trace(trace, 0.0, 0.0, 1.0, 4)
    trace = {key: [values[0]] * 40001 for key, values in _trace(target).items()}
    with pytest.raises(target.AuditFailure):
        target.select_dual_trace(trace, 0.0, 0.0, 1.0, 4)


def test_call_boundary_differences_are_dual_unclipped_and_reject_negative_nonfinite(target):
    gap = target.call_boundary_difference(0.8, 1.0, 0.1, 0.2, 0.5, 0.6)
    assert gap["cpu_seconds"] == pytest.approx(0.2, abs=1e-15, rel=0)
    assert gap["wall_seconds"] == pytest.approx(0.2, abs=1e-15, rel=0)
    assert gap["start_cpu"] is None and gap["start_wall"] is None
    assert gap["end_cpu"] is None and gap["end_wall"] is None
    for operands in ((0.5, 1.0, 0.1, 0.2, 0.5, 0.6),
                     (0.8, 0.7, 0.1, 0.2, 0.5, 0.6),
                     (float("nan"), 1.0, 0.1, 0.2, 0.5, 0.6),
                     (0.8, 1.0, -0.1, 0.2, 0.5, 0.6)):
        with pytest.raises(target.AuditFailure):
            target.call_boundary_difference(*operands)


def test_factory_duration_difference_is_typed_linked_unknown_CPU_and_no_clipping(target):
    outer = {"id": "outer-1", "kind": "OBSERVED_SPAN", "case": "ER9002401",
             "start_cpu": 1.0, "end_cpu": 1.2, "start_wall": 4.0, "end_wall": 4.6,
             "cpu_seconds": 0.2, "wall_seconds": 0.6, "paid": False}
    reported = {"id": "reported-1", "kind": "REPORTED_DURATION", "case": "ER9002401",
                "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
                "cpu_seconds": None, "wall_seconds": 0.4, "paid": False,
                "source_sha256": target.P43_SHA256}
    residual = target.duration_difference(outer, reported, "residual-1")
    assert residual["kind"] == "DURATION_DIFF" and residual["paid"] is True
    assert residual["wall_seconds"] == pytest.approx(0.2, abs=1e-15, rel=0)
    assert residual["cpu_seconds"] is None
    assert all(residual[key] is None for key in ("start_cpu", "end_cpu", "start_wall", "end_wall"))
    assert (residual["outer_ref"], residual["reported_ref"]) == ("outer-1", "reported-1")
    for patch in ({"wall_seconds": 0.7}, {"wall_seconds": -0.1},
                  {"wall_seconds": float("nan")}, {"paid": True},
                  {"kind": "OBSERVED_SPAN"}, {"case": "RR9002402"},
                  {"cpu_seconds": 0.1}, {"start_wall": 1.0}):
        with pytest.raises(target.AuditFailure):
            target.duration_difference(outer, {**reported, **patch}, "bad")


def _panel(case_ids, B_cut=8, control_cut=9):
    b = {case: {"requested": 48, "completed": 48, "full_source_photons": 576,
                "all_paid_best": {"cut": B_cut}} for case in case_ids}
    controls = [{"case": case, "mode": mode, "normal_return": True,
                 "adequate": True, "selected": {"cut": control_cut}}
                for mode in ("FAST_RANDOM", "FAST_SPECTRAL") for case in case_ids]
    return b, controls


def test_four_control_panel_strict_gate_inadequacy_and_never_positive_acceptance(target):
    case_ids = ("ER9002401", "RR9002402")
    b, controls = _panel(case_ids)
    result = target.classify_panel(b, controls, case_ids)
    assert result == "FOLLOWUP_REQUIRED"
    for index in range(4):
        changed = [dict(control) for control in controls]
        changed[index] = {**changed[index], "selected": {"cut": 8}}
        result = target.classify_panel(b, changed, case_ids)
        assert result == "NO_POSITIVE_SIGNAL"
        changed[index] = {**changed[index], "adequate": False}
        result = target.classify_panel(b, changed, case_ids)
        assert result == "INCONCLUSIVE_BASELINE_ELIGIBILITY"
    for changed in (controls[:3], controls + [controls[0]], [controls[0]] * 4):
        assert target.classify_panel(b, changed, case_ids) == "INCONCLUSIVE_BASELINE_ELIGIBILITY"
    b[case_ids[0]]["completed"] = 47
    with pytest.raises(target.AuditFailure):
        target.classify_panel(b, controls, case_ids)


def test_evidence_writer_exclusive_eight_files_reserve_and_retained_prefix(target, tmp_path):
    output = tmp_path / "fresh" / "data"
    output.parent.mkdir()
    writer = target.EvidenceWriter(output, max_bytes=8192, reserve=2048)
    writer.single("metadata", {"fixture": "reserve"})
    writer.single("graphs", {"graphs": []})
    writer.append("B_ER", {"event": "prefix", "zero": 0})
    writer.append("B_RR.jsonl", {"event": "prefix", "counts": [0, 0]})
    writer.append("paid_ledger", {"type": "OBSERVED_SPAN", "paid": False})
    writer.append("controls", {"event": "prefix"})
    with pytest.raises(target.ResourceFailure):
        writer.append("B_ER", {"oversized": "x" * 7000})
    writer.finish({"status": "INCONCLUSIVE_RESOURCE_FAILURE", "positive_accepted": False},
                  {"type": "ResourceFailure", "first_failure": "fixture capacity"})
    writer.close()
    assert {path.name for path in output.iterdir()} == {
        "metadata.json", "graphs.json", "B_ER.jsonl", "B_RR.jsonl",
        "paid_ledger.jsonl", "controls.jsonl", "summary.json", "failure.json",
    }
    assert sum(path.stat().st_size for path in output.iterdir()) <= 8192
    assert json.loads((output / "summary.json").read_text())["status"] == "INCONCLUSIVE_RESOURCE_FAILURE"
    assert json.loads((output / "failure.json").read_text())["first_failure"] == "fixture capacity"
    assert json.loads((output / "B_ER.jsonl").read_text())["zero"] == 0
    with pytest.raises(FileExistsError):
        target.EvidenceWriter(output, max_bytes=8192, reserve=2048)


def test_evidence_writer_rejects_unknown_stream_duplicate_single_and_preserves_nonfinite(target, tmp_path):
    output = tmp_path / "data"
    writer = target.EvidenceWriter(output, max_bytes=8192, reserve=2048)
    try:
        for stem in ("invented", "../escape", "/absolute"):
            with pytest.raises(KeyError):
                writer.append(stem, {"event": "bad"})
        writer.single("metadata.json", {"fixture": True})
        with pytest.raises(FileExistsError):
            writer.single("metadata", {"fixture": False})
        writer.append("B_ER", {"nonfinite": float("nan")})
        assert json.loads((output / "B_ER.jsonl").read_text())["nonfinite"] == {"nonfinite_repr": "nan"}
    finally:
        writer.close()


class WorkflowDependencies:
    """A fully scripted 96-attempt world, with no science/RNG/hash execution."""
    def __init__(self, target, spec):
        self.target, self.spec = target, spec
        self.clock = ScriptClock(step=0.00001)
        self.calls = []
        self.sampler_calls = []
        self.samples = []
        self.fast_calls = []
        self.compilers = []
        self.batches = []
        self.cuts = []
        self.verifications = []
        self.guards = 0

    def guard(self):
        self.guards += 1

    def native_readback(self):
        self.calls.append(("native_readback",))
        return {"readback": 1, "compute_max_thread_count": 1,
                "environment": {name: "1" for name in THREAD_ENV}, "scripted": True}

    def generate_graph(self, case):
        self.calls.append(("generate_graph", case["id"]))
        # A literal mock adjacency: no NetworkX, generator, weights RNG, graph
        # scoring or known benchmark adjacency is consulted by qualification.
        return tuple((0,) * 24 for _ in range(24))

    def control_seed(self, role):
        self.calls.append(("control_seed", tuple(role)))
        return 1000 + len(self.calls)

    def native_seed(self, role):
        self.calls.append(("native_seed", tuple(role)))
        return 2000 + len(self.calls)

    def permutation(self, role, values):
        self.calls.append(("permutation", tuple(role), tuple(values)))
        # Scripted coordinate permutations, not a pseudo-random generator.
        return list(values) if role[6] in ("priority", "reset_start") else list(reversed(values))

    def split_draws(self, role, count):
        self.calls.append(("split_draws", tuple(role), count))
        removed_count = role[5] % 13
        return [0] * removed_count + [1] * (count - removed_count)

    def cut(self, graph, mask):
        self.cuts.append(mask)
        return 100

    def swap_batch(self, graph, mask, rank, base_cut, degree=None):
        inside = tuple(sorted((v for v in range(24) if mask & (1 << v)), key=lambda v: rank[v]))
        outside = tuple(sorted((v for v in range(24) if not mask & (1 << v)), key=lambda v: rank[v]))
        masks = array("I", [independent_canonical(mask ^ (1 << i) ^ (1 << a), 24, rank)
                            for i in inside for a in outside])
        cuts = array("q", [max(0, base_cut - 1)] * 144)
        batch = self.target.CutBatch(24, mask, base_cut, inside, outside, cuts, masks)
        self.batches.append(batch)
        return batch

    def compile_matrix(self, batch):
        assert len(batch.cuts) == len(batch.masks) == 144
        self.compilers.append(batch)
        # No actual 12x12 matrix, eigensystem or exponential is constructed.
        return self.target.Compiled(batch.inside, batch.outside, (), (), (),
                                    1.0, "SCRIPTED", 0.0, 0.0, 0.0)

    def transport(self, compiled, source_ports, target_ports):
        assert compiled.V == "SCRIPTED"
        assert sorted(source_ports) == sorted(compiled.source_order)
        assert sorted(target_ports) == sorted(compiled.target_order)
        self.calls.append(("transport", tuple(source_ports), tuple(target_ports)))
        return self.target.Routed("SCRIPTED", 0.0, 0.0)

    def make_sampler(self, W, sorted_removed_ports, native_seed):
        assert W == "SCRIPTED" and sorted_removed_ports
        assert tuple(sorted_removed_ports) == tuple(sorted(sorted_removed_ports))
        request = (W, tuple(sorted_removed_ports), native_seed)
        self.sampler_calls.append(request)
        r = len(sorted_removed_ports)
        used = []
        def sample():
            assert not used, "one immutable factory must supply exactly one serial sample"
            used.append(True)
            self.samples.append(request)
            return (r,) + (0,) * 11, False
        return sample, 0.0

    def fast_solver(self, graph, seed, initialization, cpu_budget_seconds, max_proposals):
        self.fast_calls.append({"graph": graph, "seed": seed, "initialization": initialization,
                                "cpu_budget_seconds": cpu_budget_seconds, "max_proposals": max_proposals})
        # Preclock cached witnesses and reports are literal.  No P50 factory,
        # setup, search, NumPy array, role hash, PCG or production scorer runs.
        mask = (1 << 12) - 1
        trace = {
            "cpu_seconds": [0.0, 0.0], "wall_seconds": [0.0, 0.0],
            "best_cut": [110, 110],
            "best_subset_packbits_little": [list(mask.to_bytes(3, "little"))] * 2,
            "proposal_count": [1, 145], "stage": ["initialization", "initial_scan"],
        }
        return {
            "algorithm": "SCRIPTED_P50", "initialization": initialization, "n": 24,
            "seed": seed, "cpu_budget_seconds": cpu_budget_seconds,
            "max_proposals": max_proposals, "best_cut": 110, "best_subset": list(range(12)),
            "has_eligible_result": True, "comparison_acceptance_eligible": True,
            "eligible_checkpoint_index": 1, "eligible_checkpoint_cpu_seconds": 0.0,
            "eligible_checkpoint_wall_seconds": 0.0, "best_snapshot_cached_online": True,
            "comparison_is_anytime_prefix": True, "initial_cut": 110,
            "initial_subset": list(range(12)), "initialization_completed_before_deadline": True,
            "first_scan_completed_before_deadline": True,
            "initial_descent_completed_before_deadline": True,
            "overall_completed_best_cut": 110, "overall_completed_best_subset": list(range(12)),
            "last_completed_checkpoint_index": 1, "stop_reason": "cpu_deadline",
            "cap_hit": False, "guard_blocked_full_scan": False, "early_cap_inconclusive": False,
            "early_wall_inconclusive": False, "proposal_count": 145,
            "counters": {"cut_evaluations": 1, "delta_evaluations": 144},
            "compute_cpu_seconds": 0.0, "compute_wall_seconds": 0.0,
            "online_search_cpu_seconds": 0.0, "online_search_wall_seconds": 0.0,
            "finalization_cpu_seconds": 0.0, "finalization_wall_seconds": 0.0,
            "cpu_overrun_seconds": 0.0, "validation_cpu_seconds": 0.0,
            "validation_wall_seconds": 0.0, "initialization_details": {"scripted": True},
            "trace": trace, "free_incumbent_used": False, "external_features_used": False,
            "proposal_cap_is_cost_equivalent": False,
        }

    def verify_candidate(self, graph, mask, cut):
        self.verifications.append((mask, cut))
        assert type(mask) is int and mask.bit_count() == 12
        assert type(cut) is int and cut >= 0
        return True


def _forbid_production(monkeypatch, target):
    def forbidden(*_args, **_kwargs):
        raise AssertionError("qualification reached a production hash/RNG/scorer/compiler/native dependency")
    for name in ("seed_from_role", "seed_integrity", "scalar_cut", "exact_swap_batch",
                 "compile_feature", "transport_feature", "NativeDependencies"):
        if hasattr(target, name):
            monkeypatch.setattr(target, name, forbidden)


def _records(writer, stem, event):
    return [record for record in writer.records[stem + ".jsonl"] if record.get("type") == event]


def test_scripted_full_96_workflow_no_real_K12_DEV_hash_RNG_or_native(target, literal_spec, monkeypatch):
    deps = WorkflowDependencies(target, literal_spec)
    writer = target.MemoryWriter()
    with monkeypatch.context() as patch:
        _forbid_production(patch, target)
        summary = target.run_workflow(literal_spec, deps, writer)
    assert summary["status"] == "FOLLOWUP_REQUIRED"
    assert summary["positive_accepted"] is False
    assert set(writer.singles) == {"metadata.json", "graphs.json", "summary.json", "failure.json"}
    assert set(writer.records) == {"B_ER.jsonl", "B_RR.jsonl", "paid_ledger.jsonl", "controls.jsonl"}
    attempts = _records(writer, "B_ER", "attempt_outcome") + _records(writer, "B_RR", "attempt_outcome")
    requests = _records(writer, "B_ER", "attempt_request") + _records(writer, "B_RR", "attempt_request")
    assert len(attempts) == len(requests) == len(deps.compilers) == 96
    assert sum(record["full_source_photons"] for record in requests) == 1152
    assert {record["decoded"]["r"] for record in attempts} == set(range(13))
    assert len(deps.sampler_calls) == len(deps.samples) == sum(record["decoded"]["r"] > 0 for record in attempts)
    assert all(record["accepted"] is False for record in attempts)
    assert all(request["current_before"] == outcome["current_after"]
               for request, outcome in zip(requests, attempts))
    assert all(record["all_paid_best"]["cut"] <= record["endpoint_best"]["cut"] for record in attempts)
    for stem in ("B_ER", "B_RR"):
        batches = _records(writer, stem, "scored_batch")
        assert len(batches) == 3 * 2 + 48 * 2
        assert all(record["count"] == len(record["cuts"]) == len(record["masks_u32"]) == 144 for record in batches)
        assert len(_records(writer, stem, "reset")) == 3
    assert [(call["initialization"]) for call in deps.fast_calls] == ["random", "random", "spectral", "spectral"]
    assert all(call["max_proposals"] == 1000000 for call in deps.fast_calls)
    results = _records(writer, "controls", "control_result")
    traces = _records(writer, "controls", "control_trace")
    assert len(results) == len(traces) == 4
    assert [(result["mode"], result["case"]) for result in results] == [
        (mode, case["id"]) for mode in ("FAST_RANDOM", "FAST_SPECTRAL") for case in literal_spec["cases"]
    ]
    assert all(result["normal_return"] and result["adequate"] for result in results)
    assert all("trace" not in result for result in results)
    assert all("trace" not in result["result"] for result in results)
    assert all("trace" not in result["result"] for result in summary["controls"])
    assert len({id(call["graph"]) for call in deps.fast_calls}) == 4
    assert len({call["seed"] for call in deps.fast_calls}) == 4
    # Each mode receives its case's whole B grant, not a pooled/split allowance.
    grants = {(result["mode"], result["case"]): result["grant"] for result in results}
    for case in literal_spec["cases"]:
        assert grants[("FAST_RANDOM", case["id"])] == grants[("FAST_SPECTRAL", case["id"])]
    assert all(record["kind"] in ("OBSERVED_SPAN", "REPORTED_DURATION", "DURATION_DIFF", "CONSERVATIVE_DURATION_DIFF")
               for record in writer.records["paid_ledger.jsonl"])
    assert writer.singles["failure.json"] == {"status": "NO_FAILURE"}


def test_scripted_all_four_fast_calls_receive_whole_zero_grants_and_return_normally(target, literal_spec, monkeypatch):
    deps = WorkflowDependencies(target, literal_spec)
    writer = target.MemoryWriter()
    results = []
    raw = tuple((0,) * 24 for _ in range(24))
    with monkeypatch.context() as patch:
        _forbid_production(patch, target)
        for mode in ("FAST_RANDOM", "FAST_SPECTRAL"):
            for case in literal_spec["cases"]:
                results.append(target.run_fast_control(raw, case, mode, 0.0, literal_spec, deps, writer))
    assert len(results) == len(deps.fast_calls) == 4
    assert all(call["cpu_budget_seconds"] == 0.0 for call in deps.fast_calls)
    assert all(result["normal_return"] is True and result["adequate"] is False for result in results)
    assert all(result["selected"] is None for result in results)


def test_scripted_workflow_first_failure_retained_and_unrun_slots_explicit(target, literal_spec, monkeypatch):
    deps = WorkflowDependencies(target, literal_spec)
    writer = target.MemoryWriter()
    original = target.AuditFailure("fixture sampler failure", {"fixture_token": "first-failure"})
    def fail_factory(*_args, **_kwargs):
        raise original
    deps.make_sampler = fail_factory
    with monkeypatch.context() as patch:
        _forbid_production(patch, target)
        summary = target.run_workflow(literal_spec, deps, writer)
    assert summary["status"] == "INCONCLUSIVE_FIRST_FAILURE"
    assert summary["positive_accepted"] is False
    assert "fixture sampler failure" in json.dumps(writer.singles["failure.json"])
    assert "first-failure" in json.dumps(writer.singles["failure.json"])
    assert deps.fast_calls == []
    # r=0 remains a complete observation before the r=1 factory failure.
    assert len(_records(writer, "B_ER", "attempt_outcome")) == 1
    assert _records(writer, "B_RR", "attempt_outcome") == []
    assert "NOT_RUN" in json.dumps(summary)


def test_scripted_workflow_resource_failure_keeps_prefix_no_retry_or_budget_boost(target, literal_spec, monkeypatch):
    deps = WorkflowDependencies(target, literal_spec)
    writer = target.MemoryWriter()
    original_guard = deps.guard
    def resource_guard():
        original_guard()
        if deps.compilers:
            raise target.ResourceFailure("fixture global cap", {"limit": "wall", "actual": 90.0})
    deps.guard = resource_guard
    with monkeypatch.context() as patch:
        _forbid_production(patch, target)
        summary = target.run_workflow(literal_spec, deps, writer)
    assert summary["status"] == "INCONCLUSIVE_RESOURCE_FAILURE"
    assert summary["positive_accepted"] is False
    assert "fixture global cap" in json.dumps(writer.singles["failure.json"])
    assert len(deps.compilers) == 1 and deps.fast_calls == []
    assert len([call for call in deps.calls if call[0] == "generate_graph"]) <= 2
    assert len(_records(writer, "B_ER", "attempt_request")) <= 1


def test_scripted_native_fallback_is_first_failure_and_invalid_counts_are_preserved(target, literal_spec, monkeypatch):
    deps = WorkflowDependencies(target, literal_spec)
    writer = target.MemoryWriter()
    factory_requests = []
    def bad_factory(W, removed, native_seed):
        factory_requests.append((W, tuple(removed), native_seed))
        return lambda: ((0,) * 12, True), 0.0
    deps.make_sampler = bad_factory
    with monkeypatch.context() as patch:
        _forbid_production(patch, target)
        summary = target.run_workflow(literal_spec, deps, writer)
    assert summary["status"] == "INCONCLUSIVE_FIRST_FAILURE"
    assert summary["positive_accepted"] is False
    assert len(factory_requests) == 1
    failure_evidence = json.dumps(writer.singles["failure.json"]).lower()
    assert "fallback" in failure_evidence
    observation = _records(writer, "B_ER", "native_observation")[-1]
    assert observation["receiver_counts"] == [0] * 12 and observation["fallback"] is True
    assert deps.fast_calls == []


def test_literal_spec_qualification_caps_and_separate_main_claims_are_frozen(literal_spec):
    qualification = literal_spec["qualification"]
    assert qualification["native_queries"] == 254
    assert (qualification["HOM"], qualification["flat_r2"], qualification["toy_nonempty"]) == (3, 60, 191)
    assert qualification["toy_vacuum_native"] == 0
    assert qualification["native_max_modes"] == qualification["native_max_photons"] == 4
    assert qualification["native_abs_tolerance"] == 2e-12 and qualification["native_rel_tolerance"] == 0
    assert qualification["toy_B_minus_D"] == [-5, 192]
    assert qualification["toy_B_minus_group2"] == [0, 1]
    for key in ("real_K12_matrices", "DEV_graphs", "production_role_hashes", "PCG_constructions", "stochastic_native_samples"):
        assert qualification[key] == 0
    assert literal_spec["limits"]["wall_seconds"] == 90
    assert literal_spec["limits"]["CPU_seconds"] == 60
    assert literal_spec["limits"]["native_threads"] == literal_spec["limits"]["threads"] == 1
    assert literal_spec["limits"]["failed_retries"] == 0
    assert literal_spec["positive_accepted"] is False
    assert literal_spec["FAST_modes"] == ["FAST_RANDOM", "FAST_SPECTRAL"]
    assert literal_spec["FAST_trace_cap"] == 40000 and literal_spec["FAST_work_guard"] == 1000000


def test_native_final_configuration_readback_is_archived_before_assert(native_stack, record_property):
    evidence = {"environment": {name: os.environ.get(name) for name in THREAD_ENV},
                "native_readback": _read_native_thread(native_stack),
                "setup_error_repr": repr(native_stack.error) if native_stack.error else None,
                "native_queries_planned": 254}
    record_property("p90a_native_final_readback", json.dumps(evidence, sort_keys=True))
    assert native_stack.error is None, repr(native_stack.error)
    assert all(value == "1" for value in evidence["environment"].values())
    assert evidence["native_readback"] == {"value": 1, "error_repr": None}

# Literal item IDs are frozen for the separately authorized qualification runner.
EXPECTED_NATIVE_IDS = (
    "HOM_R01_Y02",
    "HOM_R01_Y11",
    "HOM_R01_Y20",
    "flat_R01_Y0002",
    "flat_R01_Y0011",
    "flat_R01_Y0020",
    "flat_R01_Y0101",
    "flat_R01_Y0110",
    "flat_R01_Y0200",
    "flat_R01_Y1001",
    "flat_R01_Y1010",
    "flat_R01_Y1100",
    "flat_R01_Y2000",
    "flat_R02_Y0002",
    "flat_R02_Y0011",
    "flat_R02_Y0020",
    "flat_R02_Y0101",
    "flat_R02_Y0110",
    "flat_R02_Y0200",
    "flat_R02_Y1001",
    "flat_R02_Y1010",
    "flat_R02_Y1100",
    "flat_R02_Y2000",
    "flat_R03_Y0002",
    "flat_R03_Y0011",
    "flat_R03_Y0020",
    "flat_R03_Y0101",
    "flat_R03_Y0110",
    "flat_R03_Y0200",
    "flat_R03_Y1001",
    "flat_R03_Y1010",
    "flat_R03_Y1100",
    "flat_R03_Y2000",
    "flat_R12_Y0002",
    "flat_R12_Y0011",
    "flat_R12_Y0020",
    "flat_R12_Y0101",
    "flat_R12_Y0110",
    "flat_R12_Y0200",
    "flat_R12_Y1001",
    "flat_R12_Y1010",
    "flat_R12_Y1100",
    "flat_R12_Y2000",
    "flat_R13_Y0002",
    "flat_R13_Y0011",
    "flat_R13_Y0020",
    "flat_R13_Y0101",
    "flat_R13_Y0110",
    "flat_R13_Y0200",
    "flat_R13_Y1001",
    "flat_R13_Y1010",
    "flat_R13_Y1100",
    "flat_R13_Y2000",
    "flat_R23_Y0002",
    "flat_R23_Y0011",
    "flat_R23_Y0020",
    "flat_R23_Y0101",
    "flat_R23_Y0110",
    "flat_R23_Y0200",
    "flat_R23_Y1001",
    "flat_R23_Y1010",
    "flat_R23_Y1100",
    "flat_R23_Y2000",
    "toy_R0_Y0001",
    "toy_R0_Y0010",
    "toy_R0_Y0100",
    "toy_R0_Y1000",
    "toy_R1_Y0001",
    "toy_R1_Y0010",
    "toy_R1_Y0100",
    "toy_R1_Y1000",
    "toy_R2_Y0001",
    "toy_R2_Y0010",
    "toy_R2_Y0100",
    "toy_R2_Y1000",
    "toy_R3_Y0001",
    "toy_R3_Y0010",
    "toy_R3_Y0100",
    "toy_R3_Y1000",
    "toy_R01_Y0002",
    "toy_R01_Y0011",
    "toy_R01_Y0020",
    "toy_R01_Y0101",
    "toy_R01_Y0110",
    "toy_R01_Y0200",
    "toy_R01_Y1001",
    "toy_R01_Y1010",
    "toy_R01_Y1100",
    "toy_R01_Y2000",
    "toy_R02_Y0002",
    "toy_R02_Y0011",
    "toy_R02_Y0020",
    "toy_R02_Y0101",
    "toy_R02_Y0110",
    "toy_R02_Y0200",
    "toy_R02_Y1001",
    "toy_R02_Y1010",
    "toy_R02_Y1100",
    "toy_R02_Y2000",
    "toy_R03_Y0002",
    "toy_R03_Y0011",
    "toy_R03_Y0020",
    "toy_R03_Y0101",
    "toy_R03_Y0110",
    "toy_R03_Y0200",
    "toy_R03_Y1001",
    "toy_R03_Y1010",
    "toy_R03_Y1100",
    "toy_R03_Y2000",
    "toy_R12_Y0002",
    "toy_R12_Y0011",
    "toy_R12_Y0020",
    "toy_R12_Y0101",
    "toy_R12_Y0110",
    "toy_R12_Y0200",
    "toy_R12_Y1001",
    "toy_R12_Y1010",
    "toy_R12_Y1100",
    "toy_R12_Y2000",
    "toy_R13_Y0002",
    "toy_R13_Y0011",
    "toy_R13_Y0020",
    "toy_R13_Y0101",
    "toy_R13_Y0110",
    "toy_R13_Y0200",
    "toy_R13_Y1001",
    "toy_R13_Y1010",
    "toy_R13_Y1100",
    "toy_R13_Y2000",
    "toy_R23_Y0002",
    "toy_R23_Y0011",
    "toy_R23_Y0020",
    "toy_R23_Y0101",
    "toy_R23_Y0110",
    "toy_R23_Y0200",
    "toy_R23_Y1001",
    "toy_R23_Y1010",
    "toy_R23_Y1100",
    "toy_R23_Y2000",
    "toy_R012_Y0003",
    "toy_R012_Y0012",
    "toy_R012_Y0021",
    "toy_R012_Y0030",
    "toy_R012_Y0102",
    "toy_R012_Y0111",
    "toy_R012_Y0120",
    "toy_R012_Y0201",
    "toy_R012_Y0210",
    "toy_R012_Y0300",
    "toy_R012_Y1002",
    "toy_R012_Y1011",
    "toy_R012_Y1020",
    "toy_R012_Y1101",
    "toy_R012_Y1110",
    "toy_R012_Y1200",
    "toy_R012_Y2001",
    "toy_R012_Y2010",
    "toy_R012_Y2100",
    "toy_R012_Y3000",
    "toy_R013_Y0003",
    "toy_R013_Y0012",
    "toy_R013_Y0021",
    "toy_R013_Y0030",
    "toy_R013_Y0102",
    "toy_R013_Y0111",
    "toy_R013_Y0120",
    "toy_R013_Y0201",
    "toy_R013_Y0210",
    "toy_R013_Y0300",
    "toy_R013_Y1002",
    "toy_R013_Y1011",
    "toy_R013_Y1020",
    "toy_R013_Y1101",
    "toy_R013_Y1110",
    "toy_R013_Y1200",
    "toy_R013_Y2001",
    "toy_R013_Y2010",
    "toy_R013_Y2100",
    "toy_R013_Y3000",
    "toy_R023_Y0003",
    "toy_R023_Y0012",
    "toy_R023_Y0021",
    "toy_R023_Y0030",
    "toy_R023_Y0102",
    "toy_R023_Y0111",
    "toy_R023_Y0120",
    "toy_R023_Y0201",
    "toy_R023_Y0210",
    "toy_R023_Y0300",
    "toy_R023_Y1002",
    "toy_R023_Y1011",
    "toy_R023_Y1020",
    "toy_R023_Y1101",
    "toy_R023_Y1110",
    "toy_R023_Y1200",
    "toy_R023_Y2001",
    "toy_R023_Y2010",
    "toy_R023_Y2100",
    "toy_R023_Y3000",
    "toy_R123_Y0003",
    "toy_R123_Y0012",
    "toy_R123_Y0021",
    "toy_R123_Y0030",
    "toy_R123_Y0102",
    "toy_R123_Y0111",
    "toy_R123_Y0120",
    "toy_R123_Y0201",
    "toy_R123_Y0210",
    "toy_R123_Y0300",
    "toy_R123_Y1002",
    "toy_R123_Y1011",
    "toy_R123_Y1020",
    "toy_R123_Y1101",
    "toy_R123_Y1110",
    "toy_R123_Y1200",
    "toy_R123_Y2001",
    "toy_R123_Y2010",
    "toy_R123_Y2100",
    "toy_R123_Y3000",
    "toy_R0123_Y0004",
    "toy_R0123_Y0013",
    "toy_R0123_Y0022",
    "toy_R0123_Y0031",
    "toy_R0123_Y0040",
    "toy_R0123_Y0103",
    "toy_R0123_Y0112",
    "toy_R0123_Y0121",
    "toy_R0123_Y0130",
    "toy_R0123_Y0202",
    "toy_R0123_Y0211",
    "toy_R0123_Y0220",
    "toy_R0123_Y0301",
    "toy_R0123_Y0310",
    "toy_R0123_Y0400",
    "toy_R0123_Y1003",
    "toy_R0123_Y1012",
    "toy_R0123_Y1021",
    "toy_R0123_Y1030",
    "toy_R0123_Y1102",
    "toy_R0123_Y1111",
    "toy_R0123_Y1120",
    "toy_R0123_Y1201",
    "toy_R0123_Y1210",
    "toy_R0123_Y1300",
    "toy_R0123_Y2002",
    "toy_R0123_Y2011",
    "toy_R0123_Y2020",
    "toy_R0123_Y2101",
    "toy_R0123_Y2110",
    "toy_R0123_Y2200",
    "toy_R0123_Y3001",
    "toy_R0123_Y3010",
    "toy_R0123_Y3100",
    "toy_R0123_Y4000",
)
