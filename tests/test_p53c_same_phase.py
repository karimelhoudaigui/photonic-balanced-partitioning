"""Finite ring/reference/mocked qualification; no real B point or full106 fit."""
from fractions import Fraction as Q
import gzip
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"research"))
SPEC = importlib.util.spec_from_file_location("p53c", ROOT/"research/P53c_same_phase_controls.py")
p = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(p)


def reference_mul(first, second):
    """Independent basis 1,i*sqrt(3), with (i*sqrt(3))^2=-3."""
    r, s = first; t, u = second
    return r*t-3*s*u, r*u+s*t


def embed(pair):
    a, b = pair
    return Q(a)+Q(b, 2), Q(b, 2)


def reference_entry(row, source):
    j, a = row % 4, source % 4
    sign = (-1)**((j//2)*(a % 2)+(j % 2)*(a//2)+(row >= 4 and source >= 4))
    powers = ((Q(1), Q(0)), (Q(1, 2), Q(1, 2)), (Q(-1, 2), Q(1, 2)), (Q(-1), Q(0)))
    r, s = powers[j if source >= 4 else 0]
    return sign*r, sign*s


def independent_coefficient(group, occupation):
    rows = tuple(row for row, count in enumerate(occupation) for _ in range(count))
    total = Q(0), Q(0)
    for assignment in set(itertools.permutations(rows)):
        product = Q(1), Q(0)
        for row, source in zip(assignment, group):
            product = reference_mul(product, reference_entry(row, source))
        total = total[0]+product[0], total[1]+product[1]
    return total


def balanced(shift):
    result = [Q(4, 7)]*28
    for edge, sign in (((0, 1), 1), ((2, 3), 1), ((0, 2), -1), ((1, 3), -1)):
        result[p.previous.EDGES.index(edge)] += shift*sign
    return tuple(result)


def toy_checkpoint():
    library, target = ((Q(4, 7),)*28,)*71, balanced(Q(-1, 100))
    w = (Q(1),)+(Q(0),)*27
    raw = {"target_exact": target, "library_exact": library,
           "dual_exact": {"signed_weights": w, "strict_margin": Q(1, 100)},
           "nonnegative_graph_witness": {"weights_normalized_sum_one": w,
                                        "uniform_edge_shift": Q(0), "weight_sum": Q(1)}}
    return p.exact.encoded(raw), library, target


def mock_proposal(weights=None, signed=None, solved=True):
    result = {"solver_fit_solved": solved, "solver_status": 0 if solved else 1,
              "solver_success": solved}
    if weights is not None:
        result["verification"] = {"verified": True, "used_coefficients": weights}
    if signed is not None:
        result["signed_float_coordinates"] = signed
    return result


@pytest.fixture(scope="module")
def two_group_laws():
    counts = tuple(p.exact.compositions(8, 4))
    groups = ((0, 1, 4, 6), (0, 2, 5, 7))
    return counts, {group: p.four_photon_law(group, counts) for group in groups}


def test_ring_multiplication_conjugation_and_norm_match_independent_quadratic_field():
    fixtures = ((-3, 2), (0, 0), (1, 0), (0, 1), (2, -4), (3, 5))
    for a in fixtures:
        r, s = embed(a)
        assert embed(p.conjugate(a)) == (r, -s)
        assert p.norm(a) == r*r+3*s*s
        for b in fixtures:
            assert embed(p.ring_mul(a, b)) == reference_mul(embed(a), embed(b))


def test_six_unit_roots_cycle_and_norm_vanishes_only_at_zero():
    value = (1, 0)
    for expected in p.XI_POWERS:
        assert value == expected and p.norm(value) == 1
        value = p.ring_mul(value, (0, 1))
    assert value == (1, 0) and p.ring_mul((0, 1), (0, 1)) == (-1, 1)
    for a in range(-4, 5):
        for b in range(-4, 5):
            assert p.norm((a, b)) >= 0
            assert (p.norm((a, b)) == 0) == (a == b == 0)


def test_exact_interferometer_entries_and_unnormalized_gram_are_independent():
    columns = p.columns_at_pi3()
    for source in range(8):
        for row in range(8):
            assert embed(columns[source][row]) == reference_entry(row, source)
    for a in range(8):
        for b in range(8):
            values = [reference_mul((embed(columns[a][i])[0], -embed(columns[a][i])[1]),
                                    embed(columns[b][i])) for i in range(8)]
            assert (sum(v[0] for v in values), sum(v[1] for v in values)) == ((8, 0) if a == b else (0, 0))


def test_two_group_fock_laws_have_exact_mass_and_bunched_output_factorial(two_group_laws):
    counts, laws = two_group_laws; index = {n: i for i, n in enumerate(counts)}
    for coefficients, probabilities in laws.values():
        assert len(coefficients) == 330 and sum(probabilities) == 8**4 and min(probabilities) >= 0
        for row in range(8):
            n = tuple(4 if i == row else 0 for i in range(8))
            assert probabilities[index[n]] == math.factorial(4)


def test_selected_four_photon_coefficients_match_direct_permutation_reference(two_group_laws):
    counts, laws = two_group_laws; index = {n: i for i, n in enumerate(counts)}
    examples = [tuple(4 if i == row else 0 for i in range(8)) for row in range(8)]
    examples += [(2, 2, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 0, 0, 0, 0),
                 (0, 1, 0, 1, 0, 1, 0, 1), (1, 0, 2, 0, 0, 1, 0, 0)]
    for group, (coefficients, probabilities) in laws.items():
        for n in examples:
            r, s = independent_coefficient(group, n)
            assert embed(coefficients[index[n]]) == (r, s)
            assert probabilities[index[n]] == math.prod(math.factorial(x) for x in n)*(r*r+3*s*s)


def test_repeated_noninteger_or_wrong_number_of_input_ports_are_rejected():
    for group in ((0, 0, 1, 2), (0, 1, 2), (0, 1, 2, 8), (0., 1, 2, 3)):
        with pytest.raises(ValueError): p.four_photon_law(group)


def test_probability_convolution_has_no_extra_final_fock_factor():
    # Species1 certainly has four photons in mode0; species2 chooses mode0/1 equiprobably.
    counts8 = tuple(p.exact.compositions(8, 8)); lookup = {n: i for i, n in enumerate(counts8)}
    a, b = (4, 0, 0, 0, 0, 0, 0, 0), (0, 4, 0, 0, 0, 0, 0, 0)
    mapping = tuple(tuple(lookup[tuple(x+y for x, y in zip(n, m))] for m in (a, b)) for n in (a, b))
    law = p.probability_convolution((p.DEN4, 0), (p.DEN4//2, p.DEN4//2), mapping, len(counts8))
    assert len(law) == 6435 and sum(law) == p.DEN8
    assert law[lookup[(8, 0, 0, 0, 0, 0, 0, 0)]] == p.DEN8//2
    assert law[lookup[(4, 4, 0, 0, 0, 0, 0, 0)]] == p.DEN8//2
    assert sum(value != 0 for value in law) == 2


def test_known_tie_pushforward_gives_balanced_means_with_denominator420():
    n = (4, 4, 0, 0, 0, 0, 0, 0)
    ties = p.exact.tie_scaled_rows([n]); assert len(ties[0]) == 15
    rank, numerator = p.exact._push_scalar([p.DEN8], ties)
    vector = tuple(Q(x, p.previous.KERNEL_DEN) for x in numerator)
    assert sum(rank) == p.previous.KERNEL_DEN and p.previous.validate_incident(vector)
    assert vector[p.previous.EDGES.index((0, 1))] == 0
    assert vector[p.previous.EDGES.index((0, 2))] == Q(2, 3)
    assert vector[p.previous.EDGES.index((2, 3))] == Q(8, 15)


def test_append_retains_all_original_and_duplicate_new_vertices():
    old = ((Q(4, 7),)*28,)*71
    new = {"labels": [{}]*35, "crossing_numerators": [(4*p.previous.KERNEL_DEN//7,)*28]*35}
    combined = p.append_library(old, new)
    assert len(combined) == 106 and combined[:71] == old and len(set(combined)) == 1


def test_append_rejects_missing_or_nonphysical_new_control():
    old = ((Q(4, 7),)*28,)*71
    for change in ("missing", "float", "incident"):
        rows = [[4*p.previous.KERNEL_DEN//7]*28 for _ in range(35)]
        if change == "missing": rows.pop()
        if change == "float": rows[0][0] = .5
        if change == "incident": rows[0][0] += 1
        with pytest.raises((TypeError, ValueError, ArithmeticError)):
            p.append_library(old, {"labels": [{}]*35, "crossing_numerators": rows})


def test_checkpoint_verifies_same_target_library_and_original_signed_graph_relation():
    checkpoint, library, target = toy_checkpoint()
    w, graph, scale = p.verify_checkpoint(checkpoint, library, target)
    assert w == graph == (Q(1),)+(Q(0),)*27 and scale == 1


def test_checkpoint_changed_target_library_or_float_physical_data_is_rejected():
    for change in ("target", "library", "graph", "float"):
        checkpoint, library, target = toy_checkpoint()
        if change == "target": checkpoint["target_exact"][0] = {"numerator": 0, "denominator": 1}
        if change == "library": checkpoint["library_exact"][0][0] = {"numerator": 0, "denominator": 1}
        if change == "graph": checkpoint["nonnegative_graph_witness"]["weight_sum"] = {"numerator": 2, "denominator": 1}
        if change == "float": checkpoint["target_exact"][0] = .5
        with pytest.raises((TypeError, ArithmeticError)):
            p.verify_checkpoint(checkpoint, library, target)


def test_fixed_old_graph_diagnostic_does_not_replace_graph_when_a_new_control_wins():
    checkpoint, library, target = toy_checkpoint()
    w, graph, scale = p.verify_checkpoint(checkpoint, library, target)
    before = w, graph, target
    diagnostic = p.fixed_graph_diagnostic(w, graph, scale, target, [balanced(Q(-2, 100))]+[library[0]]*34)
    assert diagnostic["status"] == "OLD_GRAPH_BEATEN_BY_NEW_CONTROL"
    assert diagnostic["minimum_normalized_margin"] == Q(-1, 100)
    assert diagnostic["new_controls_strictly_better_than_fixed_B_on_old_graph"] == 1
    assert (w, graph, target) == before


def test_expanded106_classification_is_separate_from_endpoint71_and_handles_contradiction():
    assert p.classify106(True, False, True, True) == "EXACT_POINT_EXPANDED106_MEMBERSHIP_CERTIFIED"
    assert p.classify106(False, True, True, True) == "EXACT_POINT_EXPANDED106_SEPARATION_CERTIFIED"
    assert p.classify106(True, True, False, False) == "INCONSISTENCY_EXACT_PRIMAL_DUAL_EXPANDED106"
    assert p.classify106(False, False, True, True) == "INCONCLUSIVE_AT_FIXED_X_EXPANDED106"


def test_mocked_membership_calls_both_providers_and_never_constructs_new_graph(monkeypatch):
    calls = []
    def primal(*args): calls.append("primal"); return mock_proposal(weights=[1.]+[0.]*105)
    def dual(*args): calls.append("dual"); return mock_proposal(signed=[0.]*28)
    monkeypatch.setattr(p.previous.lp_provider, "convex_fit", primal)
    monkeypatch.setattr(p.previous, "dual_proposal", dual)
    result = p.solve106(((Q(4, 7),)*28,)*106, (Q(4, 7),)*28)
    assert result["status"] == "EXACT_POINT_EXPANDED106_MEMBERSHIP_CERTIFIED"
    assert result["primal_exact"]["weights"] == [Q(1)]+[Q(0)]*105
    assert calls == ["primal", "dual"] and result["LP_provider_calls"] == 2
    assert "nonnegative_graph_witness" not in result


def test_mocked_strict_dual_uses106_scope_and_timeout_keeps_candidate_inconclusive(monkeypatch):
    monkeypatch.setattr(p.previous.lp_provider, "convex_fit", lambda *a: {"verification": {"verified": False}})
    for solved in (True, False):
        monkeypatch.setattr(p.previous, "dual_proposal", lambda *a: mock_proposal(signed=[1.]+[0.]*27, solved=solved))
        result = p.solve106(((Q(4, 7),)*28,)*106, balanced(Q(-1, 100)))
        assert result["dual_exact"]["verified"] and len(result["dual_exact"]["all_vertex_margins"]) == 106
        assert result["status"] == ("EXACT_POINT_EXPANDED106_SEPARATION_CERTIFIED" if solved else "INCONCLUSIVE_AT_FIXED_X_EXPANDED106")
        assert "nonnegative_graph_witness" not in result


def test_frozen_spec_rejects_other_point_population_or_extra_calls():
    p.validate_spec(p.frozen_spec())
    for key, value in (("x_numerator", 3), ("all_vertices", 105), ("maximum_LP_calls", 3), ("maximum_cpu_seconds", 21)):
        spec = p.frozen_spec(); spec[key] = value
        with pytest.raises(ValueError): p.validate_spec(spec)


def test_checkpoint_loader_hashes_gzip_and_ignores_floats_only_in_historical_proposals(tmp_path):
    checkpoint, library, target = toy_checkpoint()
    checkpoint["historical_proposal"] = {"floating_value": .1}
    path = tmp_path/"checkpoint.json.gz"
    path.write_bytes(gzip.compress(json.dumps(checkpoint).encode(), mtime=0))
    loaded = p.read_checkpoint(path, expected_sha=p.previous.sha256(path))
    assert p.verify_checkpoint(loaded, library, target)[2] == 1
    with pytest.raises(ValueError): p.read_checkpoint(path, expected_sha="0"*64)
