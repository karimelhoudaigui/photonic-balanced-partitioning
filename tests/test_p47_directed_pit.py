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
SPEC = importlib.util.spec_from_file_location("p47_probe", ROOT/"research/P47_directed_pit_probe.py")
p47 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p47)


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
    context = p47.build_network(a, inside, outside, delta, 1, p)
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
            actual = p47.marginal_pmf(abs(u[i,inside])**2, bosonic)
            assert actual == pytest.approx(expected, abs=2e-12)
    # Orthogonal species of sizes2+1 use independent distributions, not a
    # single generic-Gram formula or the production all-one-species shortcut.
    b2, b1 = bosonic_distribution(u, inside[:2]), bosonic_distribution(u, inside[2:])
    for i in range(6):
        expected = np.zeros(4)
        for counts2, mass2 in b2.items():
            for counts1, mass1 in b1.items():
                expected[counts2[i]+counts1[i]] += mass2*mass1
        actual = np.convolve(p47.marginal_pmf(abs(u[i,inside[:2]])**2, True),
                             p47.marginal_pmf(abs(u[i,inside[2:]])**2, True))
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
    old_cut = p47.base.cut(a, inside)
    for i, old in enumerate(inside):
        for j, new in enumerate(outside):
            assert delta[i,j] == p47.base.cut(a,(set(inside)-{old})|{new})-old_cut
    j = np.eye(3)-np.ones((3,3))/3
    assert j@delta@j == pytest.approx(2*j@a[np.ix_(inside,outside)]@j, abs=1e-12)
    perm = np.asarray([3,0,5,1,4,2])
    relabeled = np.zeros_like(a); relabeled[np.ix_(perm,perm)] = a
    carried = p47.build_network(relabeled, perm[inside].tolist(), perm[outside].tolist(), delta,1,.25)
    assert carried["u"][np.ix_(perm,perm)] == pytest.approx(context["u"], abs=3e-12)
    assert carried["cov"][np.ix_(perm,perm)] == pytest.approx(context["cov"], abs=3e-12)


def test_gaussian_pit_uses_variance_of_the_actual_factor():
    _,_,context = example_context()
    effective = np.einsum("ij,ij->i",context["factor"],context["factor"])
    assert context["variance"] == pytest.approx(effective, abs=1e-15)
    assert context["target_variance"] == pytest.approx(np.diag(context["cov"]), abs=1e-15)
    assert context["Gaussian_factor_covariance_residual"] < 1e-12
    seed = 470081
    draw = p47.make_field(context,context["inside"],"gaussian_Bcov",seed,{})
    field,counts,extra = draw()
    raw = np.asarray(extra["gaussian_raw"])
    expected = p47.ndtr(raw/np.sqrt(effective))-.5
    assert counts is None
    assert field == pytest.approx(expected, abs=1e-15)


def test_randomized_pit_intervals_and_uniform_moments():
    pmf = np.asarray([[.2,.3,.5],[1.,0.,0.]])
    assert p47.pit([1,0], pmf, np.asarray([.4,.7])) == pytest.approx([.32,.7])
    left = 0.; first = second = 0.
    for mass in pmf[0]:
        first += mass*(left+mass/2)
        second += mass*(left**2+left*mass+mass**2/3)
        left += mass
    assert first == pytest.approx(.5)
    assert second == pytest.approx(1/3)
    with pytest.raises(ValueError):
        p47.pit([.5,0],pmf,np.asarray([.2,.3]))
    with pytest.raises(ValueError):
        p47.pit([1,0],pmf,np.asarray([.2,1.]))


def test_conditional_phase_global_calibration_and_old_pattern():
    _, _, context = example_context(.5)
    draw = p47.conditional_phase_sampler(context, 470077)
    for _ in range(12):
        counts = draw()
        assert counts.sum() == 3
        assert all(counts[i] in (0,1) for i in context["inside"])
        assert counts[context["outside"]].sum() == 3-counts[context["inside"]].sum()
    table, record = p47.calibrate_phase(context,470078,64,.001)
    assert record["calibration_is_global_unconditional_A"] is True
    assert record["joint_copula_error_certified"] is False
    assert np.asarray(record["histogram"]).sum(axis=1).tolist() == [64]*6
    for i in context["inside"]:
        assert table[i].tolist() == [.5,.5,0.,0.]
    assert table.sum(axis=1) == pytest.approx(np.ones(6))
    assert record["per_new_mode_TV_union_Hoeffding_radius"] > record["per_new_mode_DKW_radius"]


@pytest.mark.parametrize("m,k,expected", [(26,13,100),(34,17,173)])
def test_shared_decoder_score_units(m,k,expected):
    a = np.zeros((m,m))
    result = p47.adaptive.complete(a,np.linspace(-.5,.5,m),k,1,list(range(m)),(k+1)//2)
    assert len(result["subset"]) == k
    assert result["score_units"] == expected
    assert sum(step["candidate_marginals"] for step in result["completion"])+1 == expected


def test_matching_keeps_all_actual_queries_and_feasibility():
    a,delta,context = example_context()
    output = io.StringIO()
    cref = p47.base.cut(a,context["inside"])
    result = p47.block_matching(a,context["inside"],context["inside"],context["outside"],
                                delta,cref,470079,8,output,{"case":"test"})
    rows = [json.loads(line) for line in output.getvalue().splitlines()]
    assert len(rows) == result["candidate_scores"] == 8
    assert result["best_cut"] == min([cref]+[row["cut"] for row in rows])
    for row in rows:
        assert len(row["subset"]) == len(set(row["subset"])) == 3
        assert row["cut"] == p47.base.cut(a,row["subset"])


def test_immutable_clifford_sampler_accepts_bulk_unitary():
    _,_,context = example_context(.5)
    sample,_ = p47.base.make_optical_sampler(context["u"],context["inside"],"bosonic",470080)
    counts,rejected = sample()
    assert not rejected
    assert counts.sum() == 3
    assert all(counts[i] in (0,1) for i in context["inside"])


@pytest.mark.parametrize("k", [13,17])
def test_prime_directed_step_descends_actual_routing_proxy(k):
    p = .5
    inside,outside = list(range(k)),list(range(k,2*k))
    x,y = np.zeros(k),np.zeros(k)
    x[:2]=[1,-1]; y[1:3]=[1,-1]
    delta = np.outer(x,y)+2
    a = np.zeros((2*k,2*k))
    guided = p47.build_network(a,inside,outside,delta,1,p)
    blind = p47.build_network(a,inside,outside,delta,0,p)
    routing = abs(guided["u"][np.ix_(outside,inside)].T)**2/p
    routing_blind = abs(blind["u"][np.ix_(outside,inside)].T)**2/p
    actual_change = float(np.sum(delta*(routing-routing_blind)))
    assert actual_change < -1e-10
    assert actual_change == pytest.approx(guided["centered_delta_norm"]*(
        guided["normalized_proxy_after"]-guided["normalized_proxy_before"]),abs=1e-12)
    assert guided["normalized_proxy_after"]-guided["normalized_proxy_before"] <= guided["finite_proxy_decrease_bound"]+1e-12
    assert guided["proxy_tangent_frobenius_squared"] > 0
    assert guided["proxy_tangent_frobenius_squared"] >= math.sin(math.pi/k)**2/k-1e-12
    assert blind["W_minus_F_frobenius_squared"] < 1e-24


def test_composite_stall_and_zero_signal_are_preserved():
    k=4
    a = np.zeros((8,8))
    for block in (range(4),range(4,8)):
        for i in block:
            for j in block:
                if i != j:
                    a[i,j]=17/16
    v=np.asarray([1,-1,1,-1])
    a[:4,4:]=1+np.outer(v,v)/8
    a[4:,:4]=a[:4,4:].T
    inside,outside=list(range(4)),list(range(4,8))
    ell=a.sum(axis=1)-2*a[:,inside].sum(axis=1)
    delta=np.asarray([[ell[j]-ell[i]+2*a[i,j] for j in outside] for i in inside])
    context=p47.build_network(a,inside,outside,delta,1,.5)
    def rational_fixture_cut(subset):
        return sum(a[i,j] for i in subset for j in range(8) if j not in subset)
    assert rational_fixture_cut(inside)==16
    assert rational_fixture_cut([0,2,4,6])==15.5
    assert delta.min()==.125
    assert context["centered_delta_norm"] > .9
    assert context["W_minus_F_frobenius_squared"] < 1e-24
    assert context["proxy_tangent_frobenius_squared"] < 1e-24
    zero=p47.build_network(np.zeros((6,6)),list(range(3)),list(range(3,6)),np.ones((3,3)),1,.25)
    assert zero["guide_epsilon"]==0
    assert zero["W_minus_F_frobenius_squared"] < 1e-24
