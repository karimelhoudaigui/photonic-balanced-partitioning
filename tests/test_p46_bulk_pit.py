"""Independent finite physical checks, not development graph outcomes."""
import importlib.util
import io
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"research"))
SPEC = importlib.util.spec_from_file_location("p46_probe", ROOT/"research/P46_bulk_pit_probe.py")
p46 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p46)


def permanent_explicit(matrix):
    return sum((np.prod([matrix[i, j] for i, j in enumerate(order)])
                for order in itertools.permutations(range(len(matrix)))), 0j)


def bosonic_distribution(u, source):
    """Standalone normalized Fock formula, factorial collision denominators."""
    m, k = len(u), len(source)
    result = {}
    for slots in itertools.combinations_with_replacement(range(m), k):
        counts = tuple(slots.count(i) for i in range(m))
        amplitude = permanent_explicit(u[np.ix_(slots, source)])
        result[counts] = abs(amplitude)**2/math.prod(math.factorial(x) for x in counts)
    return result


def labeled_distribution(u, source):
    result = {}
    for slots in itertools.product(range(len(u)), repeat=len(source)):
        counts = tuple(slots.count(i) for i in range(len(u)))
        probability = math.prod(abs(u[slots[j], source[j]])**2 for j in range(len(source)))
        result[counts] = result.get(counts, 0.)+probability
    return result


def example_context(p=.25):
    a = np.asarray([[0,3,0,2,4,0],[3,0,1,0,3,2],[0,1,0,2,1,4],
                    [2,0,2,0,4,1],[4,3,1,4,0,2],[0,2,4,1,2,0]], dtype=float)
    inside, outside = [2,0,4], [5,1,3]
    ell = a.sum(axis=1)-2*a[:, inside].sum(axis=1)
    delta = np.asarray([[ell[j]-ell[i]+2*a[i,j] for j in outside] for i in inside])
    context = p46.build_network(a, inside, outside, delta, .25, p)
    return a, delta, context


@pytest.mark.parametrize("transfer_p", [.25,.5])
def test_hollow_fock_and_labeled_marginals_against_enumeration(transfer_p):
    _, _, context = example_context(transfer_p)
    u, inside, outside = context["u"], context["inside"], context["outside"]
    b = bosonic_distribution(u, inside)
    d = labeled_distribution(u, inside)
    assert sum(b.values()) == pytest.approx(1., abs=2e-12)
    assert sum(d.values()) == pytest.approx(1., abs=2e-12)
    for law, bosonic in ((b, True),(d,False)):
        transfers = np.zeros(4)
        for counts, probability in law.items():
            transfers[sum(counts[i] for i in outside)] += probability
            if probability > 1e-20:
                assert all(counts[i] in (0,1) for i in inside)
        assert transfers == pytest.approx([math.comb(3,r)*transfer_p**r*(1-transfer_p)**(3-r)
                                          for r in range(4)], abs=2e-12)
        for i in range(6):
            expected = [sum(value for counts, value in law.items() if counts[i] == r) for r in range(4)]
            actual = p46.marginal_pmf(abs(u[i,inside])**2, bosonic)
            assert actual == pytest.approx(expected, abs=2e-12)
    # Orthogonal species of sizes2+1 use independent distributions, not a
    # single generic-Gram formula or the production all-one-species shortcut.
    b2, b1 = bosonic_distribution(u, inside[:2]), bosonic_distribution(u, inside[2:])
    for i in range(6):
        expected = np.zeros(4)
        for counts2, mass2 in b2.items():
            for counts1, mass1 in b1.items():
                expected[counts2[i]+counts1[i]] += mass2*mass1
        actual = np.convolve(p46.marginal_pmf(abs(u[i,inside[:2]])**2, True),
                             p46.marginal_pmf(abs(u[i,inside[2:]])**2, True))
        assert actual == pytest.approx(expected, abs=2e-12)
    mean = np.zeros(6); second = np.zeros((6,6))
    for counts, probability in b.items():
        mean += probability*np.asarray(counts)
        second += probability*np.outer(counts, counts)
    assert context["mu"] == pytest.approx(mean, abs=2e-12)
    assert context["cov"] == pytest.approx(second-np.outer(mean,mean), abs=3e-12)
    assert context["polar_singular_min"] >= .75-1e-12
    assert context["unitary_residual"] < 3e-12


def test_label_covariance_and_swap_orientation():
    a, delta, context = example_context()
    inside, outside = context["inside"], context["outside"]
    old_cut = p46.base.cut(a, inside)
    for i, old in enumerate(inside):
        for j, new in enumerate(outside):
            assert delta[i,j] == p46.base.cut(a,(set(inside)-{old})|{new})-old_cut
    j = np.eye(3)-np.ones((3,3))/3
    assert j@delta@j == pytest.approx(2*j@a[np.ix_(inside,outside)]@j, abs=1e-12)
    perm = np.asarray([3,0,5,1,4,2])
    relabeled = np.zeros_like(a); relabeled[np.ix_(perm,perm)] = a
    carried = p46.build_network(relabeled, perm[inside].tolist(), perm[outside].tolist(), delta,.25,.25)
    assert carried["u"][np.ix_(perm,perm)] == pytest.approx(context["u"], abs=3e-12)
    assert carried["cov"][np.ix_(perm,perm)] == pytest.approx(context["cov"], abs=3e-12)


def test_randomized_pit_intervals_and_uniform_moments():
    pmf = np.asarray([[.2,.3,.5],[1.,0.,0.]])
    assert p46.pit([1,0], pmf, np.asarray([.4,.7])) == pytest.approx([.32,.7])
    left = 0.; first = second = 0.
    for mass in pmf[0]:
        first += mass*(left+mass/2)
        second += mass*(left**2+left*mass+mass**2/3)
        left += mass
    assert first == pytest.approx(.5)
    assert second == pytest.approx(1/3)
    with pytest.raises(ValueError):
        p46.pit([.5,0],pmf,np.asarray([.2,.3]))
    with pytest.raises(ValueError):
        p46.pit([1,0],pmf,np.asarray([.2,1.]))


def test_conditional_phase_global_calibration_and_old_pattern():
    _, _, context = example_context(.5)
    draw = p46.conditional_phase_sampler(context, 460077)
    for _ in range(12):
        counts = draw()
        assert counts.sum() == 3
        assert all(counts[i] in (0,1) for i in context["inside"])
        assert counts[context["outside"]].sum() == 3-counts[context["inside"]].sum()
    table, record = p46.calibrate_phase(context,460078,64,.001)
    assert record["calibration_is_global_unconditional_A"] is True
    assert record["joint_copula_error_certified"] is False
    assert np.asarray(record["histogram"]).sum(axis=1).tolist() == [64]*6
    for i in context["inside"]:
        assert table[i].tolist() == [.5,.5,0.,0.]
    assert table.sum(axis=1) == pytest.approx(np.ones(6))
    assert record["per_new_mode_TV_union_Hoeffding_radius"] > record["per_new_mode_DKW_radius"]


@pytest.mark.parametrize("m,k,expected", [(24,12,94),(28,14,127)])
def test_shared_decoder_score_units(m,k,expected):
    a = np.zeros((m,m))
    result = p46.adaptive.complete(a,np.linspace(-.5,.5,m),k,1,list(range(m)),(k+1)//2)
    assert len(result["subset"]) == k
    assert result["score_units"] == expected
    assert sum(step["candidate_marginals"] for step in result["completion"])+1 == expected


def test_matching_keeps_all_actual_queries_and_feasibility():
    a,delta,context = example_context()
    output = io.StringIO()
    cref = p46.base.cut(a,context["inside"])
    result = p46.block_matching(a,context["inside"],context["inside"],context["outside"],
                                delta,cref,460079,8,output,{"case":"test"})
    rows = [json.loads(line) for line in output.getvalue().splitlines()]
    assert len(rows) == result["candidate_scores"] == 8
    assert result["best_cut"] == min([cref]+[row["cut"] for row in rows])
    for row in rows:
        assert len(row["subset"]) == len(set(row["subset"])) == 3
        assert row["cut"] == p46.base.cut(a,row["subset"])


def test_immutable_clifford_sampler_accepts_bulk_unitary():
    _,_,context = example_context(.5)
    sample,_ = p46.base.make_optical_sampler(context["u"],context["inside"],"bosonic",460080)
    counts,rejected = sample()
    assert not rejected
    assert counts.sum() == 3
    assert all(counts[i] in (0,1) for i in context["inside"])
