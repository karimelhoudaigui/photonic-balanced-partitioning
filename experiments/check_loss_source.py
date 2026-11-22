"""Separate P37 arithmetic path: Polya urn + de Casteljau loss transform.

This is an Astra self-review, not an independent agent review.
"""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path
import time


def q(value):
    return F(int(value['numerator']), int(value['denominator']))


def haar_by_urn(m):
    # Dirichlet-multinomial(alpha_i=1) is uniform over weak compositions.
    # For l photons and c occupied modes, occupied weights sum to l+c.
    law = [F(1)] + [F(0)]*m
    target = [law[m//2]]
    for l in range(m):
        nxt = [F(0)]*(m+1)
        for c, mass in enumerate(law):
            nxt[c] += mass*F(l+c, m+l)
            if c < m:
                nxt[c+1] += mass*F(m-c, m+l)
        assert sum(nxt) == 1
        assert all(p >= 0 for p in nxt)
        law = nxt
        target.append(law[m//2])
    return target


def binomial_transform(values, eta):
    # Repeated affine averaging; no binomial coefficients or comb formula.
    current = list(values)
    result = [current[0]]
    while len(current) > 1:
        current = [(1-eta)*a + eta*b for a, b in zip(current, current[1:])]
        result.append(current[0])
    return result


def weighted_mean(values, n, eta):
    # The root endpoints are interior; recurrent probability weights.
    weight = (1-eta)**n
    result = weight*values[0]
    for l in range(n):
        weight *= F(n-l, l+1)*eta/(1-eta)
        result += weight*values[l+1]
    return result


def review(raw_path, output):
    output.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    raw = json.loads(raw_path.read_text())
    target = {m: haar_by_urn(m) for m in (8,10,12,16,24,32,48,64,128)}
    rows = 0
    seen = set()
    for cell in raw['grid']:
        m = cell['m']; eta = q(cell['eta'])
        assert (m, eta) not in seen
        seen.add((m, eta))
        probabilities = binomial_transform(target[m], eta)
        assert [r['source'] for r in cell['values']] == list(range(m//2, m+1))
        for row in cell['values']:
            n = row['source']; p = probabilities[n]
            assert p == q(row['probability'])
            assert p/n == q(row['per_photon'])
            assert n/p == q(row['waiting_photons_iid_haar'])
            rows += 1
        ma = max(probabilities[m//2:])
        mb = max(probabilities[n]/n for n in range(m//2, m+1))
        assert cell['per_attempt_maximizers'] == [n for n in range(m//2, m+1) if probabilities[n] == ma]
        assert cell['per_photon_maximizers'] == [n for n in range(m//2, m+1) if probabilities[n]/n == mb]
    expected = {(m, eta) for m in (8,10,12,16,24,32,48,64)
                for eta in (F(1,4),F(1,2),F(3,4),F(9,10),F(99,100),F(1))
                + tuple(1-F(i,4*m) for i in (1,3,5,7,9,11,13,15))}
    assert seen == expected
    checked = []
    for root in raw['transitions']:
        m = root['m']; n = root['source']; h = target[m]
        per_photon = root['criterion'] == 'per_photon'
        lo, hi = q(root['eta_low']), q(root['eta_high'])
        assert 0 < lo < hi < 1 and hi-lo == F(1, 2**40)
        differences = []
        for endpoint, label in ((lo,'low'),(hi,'high')):
            a = weighted_mean(h, n+1, endpoint)
            b = weighted_mean(h, n, endpoint)
            difference = a/(n+1)-b/n if per_photon else a-b
            assert difference == q(root['difference_'+label])
            differences.append(difference)
        assert differences[0] > 0 > differences[1]
        assert q(root['scaled_loss_low']) == m*(1-hi)
        assert q(root['scaled_loss_high']) == m*(1-lo)
        degree = n-1 if per_photon else n
        coefficients = [int(c) for c in root['homogeneous_integer_coefficients']]
        common = int(root['coefficient_denominator'])
        assert len(coefficients) == degree+1
        for r, c in enumerate(coefficients):
            difference = (h[r+2]/(r+2)-h[r+1]/(r+1) if per_photon else h[r+1]-h[r])
            assert F(c,common) == math.comb(degree,r)*difference
        checked.append({'m':m,'source':n,'criterion':root['criterion'],
                        'eta_midpoint_for_display':float((lo+hi)/2),
                        'scaled_loss_midpoint_for_display':float(m*(1-(lo+hi)/2))})
    assert rows == 1610 and len(checked) == 36
    for m in target:
        group = [r for r in raw['transitions'] if r['m']==m]
        assert [(r['criterion'],r['source']) for r in group] == [('per_attempt',m-1)] + [('per_photon',j) for j in range(m-3,m)]
        assert q(group[3]['eta_high']) < q(group[2]['eta_low']) < q(group[1]['eta_low'])
    progress = [json.loads(line) for line in (raw_path.parent/'progress.jsonl').read_text().splitlines()]
    assert progress == [{'event':'grid', **cell} for cell in raw['grid']] + [{'event':'transition', **r} for r in raw['transitions']]
    summary = {'status':'EXACT_FINITE_REVIEW_PASS', 'review_provenance':'ASTRA_SELF_REVIEW_SEPARATE_IMPLEMENTATION',
               'grid_cells':len(seen), 'all_source_values_checked':rows, 'root_sign_brackets_checked':len(checked),
               'orthogonal_invariant':'Polya urn normalized at every photon count; de Casteljau binomial transform',
               'new_full_fock_simulations':0,'physical_shots':0,'runtime_seconds':time.monotonic()-start,
               'limitations':['No fresh agent proof review','No novelty audit completed','No asymptotic proved by finite numbers']}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (output/'transition_display.json').write_text(json.dumps(checked,indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--raw',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    review(args.raw,args.output)
