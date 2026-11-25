"""Small deterministic checks for the NEW decoder and graph feature contract.

These tests are declared before the first P45-B numerical execution.
"""
import itertools
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"research"))
from P45_encoding_full_fock_probe import decode, encode, generator, prepare


def test_full_fock_bijection_includes_collisions():
    for k in (1, 2, 3, 4):
        order = list(range(2*k-1, -1, -1))
        seen = set()
        for subset in itertools.combinations(range(2*k), k):
            n = encode(subset, order)
            assert decode(n, order) == list(subset)
            assert int(n.sum()) == k
            seen.add(tuple(n))
        assert len(seen) == len(list(itertools.combinations(range(2*k), k)))
        assert tuple([k]+[0]*k) in seen


def test_frontend_credits_every_hop_and_preserves_source_anchor(tmp_path):
    a = np.array([[0,3,1,2],[3,0,4,0],[1,4,0,2],[2,0,2,0]], dtype=float)
    with (tmp_path/"raw.jsonl").open("x") as stream:
        context = prepare(a, "deterministic_fixture", {"anchor_uniform_draws":4}, stream)
    import json
    rows = [json.loads(line) for line in (tmp_path/"raw.jsonl").read_text().splitlines()]
    assert context["common_scores"] == 8 == len(rows)
    assert context["front_cut"] == min(row["cut"] for row in rows)
    assert decode(context["source"], context["order"]) == context["anchor"]
    assert encode(context["front_subset"], context["order"]).sum() == 2
    for kappa in (0., np.pi/2):
        h, norm = generator(context, kappa)
        assert norm > 0
        np.testing.assert_allclose(h, h.conj().T, atol=1e-14)
        np.testing.assert_allclose(np.linalg.norm(h, 2), 1., atol=1e-14)


def test_hop_features_are_covariant_when_order_is_transported(tmp_path):
    a = np.array([[0,3,1,2],[3,0,4,0],[1,4,0,2],[2,0,2,0]], dtype=float)
    with (tmp_path/"raw.jsonl").open("x") as stream:
        context = prepare(a, "transport_fixture", {"anchor_uniform_draws":4}, stream)
    permutation = np.array([2,0,3,1])
    inverse = np.argsort(permutation)
    order = inverse[context["order"]].tolist()
    relabeled = a[np.ix_(permutation, permutation)]
    from P43_global_gain_probe import cut
    source = np.asarray(context["source"])
    for j in range(2):
        for i in range(3):
            if i == j:
                continue
            n = source.copy()
            n[i] += 1
            n[j] -= 1
            assert cut(a, decode(n, context["order"])) == cut(relabeled, decode(n, order))
