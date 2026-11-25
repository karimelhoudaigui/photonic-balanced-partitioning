"""Exact fixed-angle species falsifier; no production imports or sampling."""
import argparse
from fractions import Fraction
import gzip
import itertools
import json
import math
from pathlib import Path
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def multiply(x, y):
    a, b = x
    c, d = y
    return a*c-b*d, a*d+b*c+b*d


def conjugate(x):
    return x[0]+x[1], -x[1]


def norm(x):
    return x[0]**2+x[0]*x[1]+x[1]**2


def matrix():
    roots = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    signs = ((1, 1, 1, 1), (1, 1, -1, -1),
             (1, -1, 1, -1), (1, -1, -1, 1))
    rows = []
    for r in range(8):
        row = []
        for j in range(8):
            sign = signs[r % 4][j % 4] * (-1 if r >= 4 and j >= 4 else 1)
            value = roots[r % 4] if j >= 4 else roots[0]
            row.append(tuple(sign*x for x in value))
        rows.append(row)
    return rows


def gram_check(q):
    n = len(q)
    for i in range(n):
        for j in range(n):
            values = [multiply(conjugate(row[i]), row[j]) for row in q]
            require(tuple(map(sum, zip(*values))) == ((n, 0) if i == j else (0, 0)), 'exact Gram')


def unpack(key, n):
    counts = []
    for _ in range(n):
        key, digit = divmod(key, 9)
        counts.append(digit)
    require(key == 0, 'base9 overflow')
    return counts


def source(q, group):
    coefficients = {0: (1, 0)}
    for j in group:
        nxt = {}
        for key, value in coefficients.items():
            for r in range(len(q)):
                target = key+9**r
                added = multiply(value, q[r][j])
                old = nxt.get(target, (0, 0))
                nxt[target] = old[0]+added[0], old[1]+added[1]
        coefficients = nxt
    weights = {}
    for key, value in coefficients.items():
        counts = unpack(key, len(q))
        require(sum(counts) == len(group), 'fixed total')
        weights[key] = norm(value)*math.prod(math.factorial(x) for x in counts)
    require(sum(weights.values()) == len(q)**len(group), 'source exact mass')
    return coefficients, weights


def compositions(total, n):
    if n == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first, n-1):
                yield (first,)+tail


def tie_scalar(counts):
    best, ways, numerator = -1, 0, 0
    for subset in itertools.combinations(range(8), 4):
        value = sum(counts[i] for i in subset)
        signed = int((0 in subset) != (4 in subset))-int((1 in subset) != (5 in subset))
        if value > best:
            best, ways, numerator = value, 1, signed
        elif value == best:
            ways += 1
            numerator += signed
    scaled = Fraction(420*numerator, ways)
    require(scaled.denominator == 1 and abs(scaled) <= 420, 'integer tie scalar')
    return scaled.numerator


def synthetic_guards():
    roots = [(1, 0)]
    for _ in range(6):
        roots.append(multiply(roots[-1], (0, 1)))
    require(roots[6] == roots[0] and roots[2] == (-1, 1), 'ring roots')
    require(all(norm(multiply(x, y)) == norm(x)*norm(y) for x in roots for y in roots), 'norm multiplicativity')
    q = [[(1, 0), (1, 0)], [(1, 0), (-1, 0)]]
    gram_check(q)
    _, b = source(q, (0, 1))
    require(b == {2: 2, 10: 0, 18: 2}, 'two-photon HOM')
    _, p = source(q, (0,))
    _, s = source(q, (1,))
    d = {}
    for k, v in p.items():
        for h, w in s.items():
            d[k+h] = d.get(k+h, 0)+v*w
    require(d == {2: 1, 10: 2, 18: 1}, 'distinguishable convolution')
    require(tie_scalar((2, 2, 2, 2, 0, 0, 0, 0)) == 0, 'unique top subset')
    # Choose two of boundary vertices2,3,4: edge04 crosses in one of the
    # three maximizers and edge15 in all three, signed mean -2/3.
    require(tie_scalar((3, 2, 1, 1, 1, 0, 0, 0)) == -280, 'nontrivial uniform tie')
    require(unpack(2+7*9**7+6+9**7, 8) == [8, 0, 0, 0, 0, 0, 0, 8], 'base9 no carry')
    return 7


def rational(value):
    return {'numerator': value.numerator, 'denominator': value.denominator}


def save(path, obj):
    with gzip.GzipFile(filename=str(path), mode='wb', mtime=0) as stream:
        stream.write((json.dumps(obj, separators=(',', ':'), allow_nan=False)+'\n').encode())


def run(output):
    guard_count = synthetic_guards()
    q = matrix()
    gram_check(q)
    scalars = {sum(x*9**i for i, x in enumerate(n)): tie_scalar(n) for n in compositions(8, 8)}
    require(len(scalars) == 6435, 'complete output space')
    laws, archive = {}, []
    for size in range(1, 9):
        for group in itertools.combinations(range(8), size):
            mask = sum(1 << j for j in group)
            coefficients, weights = source(q, group)
            laws[mask] = weights
            archive.append({'input_mask': mask, 'group': group, 'denominator': 8**size,
                            'states': [[key, *coefficients[key], weights[key]] for key in sorted(weights)]})
    denominator = 840*8**8
    b_mean = Fraction(sum(v*scalars[key] for key, v in laws[255].items()), denominator)
    require(b_mean == Fraction(-767, 327680), 'independently reconstructed full-B mean')
    save(output/'source_laws.json.gz', {'basis': '1,xi;xi^2=xi-1', 'base': 9, 'matrix': q, 'laws': archive})
    save(output/'tie_scalars.json.gz', {'scale': 420, 'values': sorted(scalars.items())})
    controls = []
    for size in range(1, 5):
        for group in itertools.combinations(range(8), size):
            if size == 4 and 0 not in group:
                continue
            mask = sum(1 << j for j in group)
            left, right = laws[mask], laws[255 ^ mask]
            numerator = sum(v*w*scalars[k+h] for k, v in left.items() for h, w in right.items())
            mean = Fraction(numerator, denominator)
            controls.append({'input_group': group, 'mean': rational(mean), 'gap_above_B': rational(mean-b_mean)})
    require(len(controls) == 127, 'all unordered bipartitions')
    gaps = [Fraction(c['gap_above_B']['numerator'], c['gap_above_B']['denominator']) for c in controls]
    minimum = min(gaps)
    status = ('SAME_PHASE_ALL_BIPARTITIONS_SEPARATED' if minimum > 0
              else 'STRONGER_SAME_PHASE_SPECIES_INTERPRETATION_REFUTED')
    result = {'status': status, 'synthetic_guards': guard_count, 'controls': controls,
              'source_groups': len(laws), 'B_mean': rational(b_mean), 'minimum_gap': rational(minimum),
              'minimizers': [c['input_group'] for c, gap in zip(controls, gaps) if gap == minimum],
              'positive_optimizer_accepted': False, 'genuine_order8_witness_claimed': False,
              'new_graphs': 0, 'physical_draws': 0, 'actual_QPU_calls': 0}
    (output/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    try:
        result = run(args.output)
    except Exception as error:
        (args.output/'failure.json').write_text(json.dumps({'error': repr(error)})+'\n')
        raise
    print(json.dumps({'status': result['status'], 'wall_seconds': time.monotonic()-start}))


if __name__ == '__main__':
    main()
