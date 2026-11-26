"""Post-seal scalar audit; no producer import, native call, RNG or optimizer."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / 'research/P96_column_loss_main/run_001'
OUT = ROOT / 'reports/P96_validation_review/recorded_audit_run001/data'


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def permanent(matrix):
    k = len(matrix)
    values = [0j] * (1 << k)
    values[0] = 1 + 0j
    for mask in range((1 << k) - 1):
        row = mask.bit_count()
        for j in range(k):
            if not (mask >> j) & 1:
                values[mask | (1 << j)] += values[mask] * matrix[row][j]
    return values[-1]


def main():
    assert permanent([]) == 1 and permanent([[1, 1], [1, 1]]) == 2
    assert permanent([[0, 1], [1, 0]]) == 1 and permanent([[1j, 0], [0, 1]]) == 1j
    manifest = json.loads((RAW / 'manifest.json').read_text())
    summary = json.loads((RAW / 'data/summary.json').read_text())
    assert manifest['run']['status'] == 'completed' and manifest['run']['exit_status'] == 0
    assert len(manifest['input_artifacts']) == 35
    assert all(a['sha256'] == a['sha256_after'] == sha(ROOT / a['path']) for a in manifest['input_artifacts'])
    assert summary['status'] == 'FINITE_VALIDATION_PASS' and summary['positive_accepted'] is False
    rows = [json.loads(line) for line in (RAW / 'data/records.jsonl').read_text().splitlines()]
    kinds = Counter(r['kind'] for r in rows)
    exact, starts, audits, setups, native, marginals = (defaultdict(list) for _ in range(6))
    banks = {'exact_raw': exact, 'exact_case_start': starts, 'exact_audit': audits,
             'native_setup': setups, 'native_raw': native, 'native_marginal': marginals}
    for row in rows:
        if row['kind'] in banks:
            banks[row['kind']][row['case']].append(row)
    expected = ['V0', 'U1', 'H2', 'D3', 'R3a', 'R3b', 'S3', 'B4', 'D4', 'Z4', 'R4', 'C3', 'X4']
    assert list(starts) == expected and kinds['exact_raw'] == 167
    results = {}
    for name in expected:
        t = [[F(x) for x in r] for r in starts[name][0]['T']]
        m, k = len(t), len(t[0])
        p = {tuple(r['signal']): F(r['p']) for r in exact[name]}
        q = {tuple(r['signal']): F(r['q']) for r in exact[name]}
        states = {n for n in product(range(k + 1), repeat=m) if sum(n) <= k}
        assert len(p) == len(exact[name]) == math.comb(m + k, k) and set(p) == states
        assert sum(p.values()) == 1 and all(v >= 0 for v in p.values())
        lam = [sum((t[j][i] ** 2 for i in range(k)), F(0)) for j in range(m)]
        g = [[sum(((t[j][a] * t[l][b] + t[j][b] * t[l][a]) ** 2
                   for a, b in combinations(range(k), 2)), F(0)) for l in range(m)] for j in range(m)]
        for j in range(m):
            assert sum(p[n] * n[j] for n in p) == lam[j]
            for l in range(m):
                assert sum(p[n] * n[j] * (n[l] - (j == l)) for n in p) == g[j][l]
        if name == 'X4':
            assert q[(1,)] == F(-1, 2) and audits[name][0]['status'] == 'EXPECTED_OUTSIDE_DOMAIN'
            continue
        assert sum(q.values()) == 1 and all(v >= 0 for v in q.values())
        for j in range(m):
            assert sum(q[n] * n[j] for n in q) == lam[j]
            for l in range(m):
                assert sum(q[n] * n[j] * (n[l] - (j == l)) for n in q) == g[j][l]
        tv = sum(abs(p[n] - q[n]) for n in p) / 2
        tail = sum(p[n] * (sum(n) - 1) ** 2 for n in p if sum(n) >= 3)
        c = [sum(t[j][i] ** 2 for j in range(m)) for i in range(k)]
        e3 = sum((math.prod(c[i] for i in ids) for ids in combinations(range(k), 3)), F(0))
        assert tv == tail <= 24 * e3 <= 4 * sum(c) ** 3
        assert tv == F(audits[name][0]['tv'])
        results[name] = {'bins': len(p), 'tv': str(tv), 'bound24': str(24 * e3)}
    assert set(native) == {'V0', 'U1', 'H2', 'R3a', 'B4'}
    max_amp, max_prob, max_marginal, max_gram = 0.0, 0.0, 0.0, 0.0
    for name, samples in native.items():
        setup = setups[name][0]
        u, inp = setup['U'], setup['input']
        k, dim, m = sum(inp), len(inp), len(starts[name][0]['T'])
        t = starts[name][0]['T']
        assert all(abs(u[i][j] - float(F(t[i][j]))) <= 1e-14 for i in range(m) for j in range(k))
        for i in range(dim):
            for j in range(dim):
                max_gram = max(max_gram, abs(sum(u[a][i] * u[a][j] for a in range(dim)) - (i == j)),
                               abs(sum(u[i][a] * u[j][a] for a in range(dim)) - (i == j)))
        columns = [j for j, count in enumerate(inp) for _ in range(count)]
        seen = {tuple(r['counts']) for r in samples}
        assert len(seen) == len(samples) == math.comb(dim + k - 1, k)
        assert seen == {n for n in product(range(k + 1), repeat=dim) if sum(n) == k}
        aggregates = defaultdict(float)
        for r in samples:
            out = [j for j, count in enumerate(r['counts']) for _ in range(count)]
            matrix = [[u[i][j] for j in columns] for i in out]
            norm = math.sqrt(math.prod(math.factorial(v) for v in r['counts'] + inp))
            amp = permanent(matrix) / norm
            observed = complex(*r['amplitude'])
            max_amp = max(max_amp, abs(amp - observed))
            max_prob = max(max_prob, abs(abs(amp) ** 2 - r['probability']))
            for key in ('threads_before', 'threads_after'):
                assert r[key]['native'] == 1 and set(r[key]['environment'].values()) == {'1'}
            aggregates[tuple(r['signal'])] += abs(amp) ** 2
        for r in marginals[name]:
            max_marginal = max(max_marginal, abs(aggregates[tuple(r['signal'])] - float(F(r['expected_exact']))))
        assert abs(sum(aggregates.values()) - 1) <= 1e-11
    assert kinds['native_raw'] == kinds['native_attempt'] == 159 and kinds['native_marginal'] == 28
    assert max(max_amp, max_prob, max_marginal, max_gram) <= 1e-11
    result = {'status': 'RECORDED_SCALAR_AUDIT_PASS', 'rows': len(rows), 'kind_counts': dict(kinds),
              'exact_cases': results, 'exact_bins_including_outside': 167, 'native_points': 159,
              'native_marginal_bins': 28, 'max_amplitude_DP_error': max_amp,
              'max_probability_DP_error': max_prob, 'max_unconditional_marginal_error': max_marginal,
              'max_unitarity_Gram_error': max_gram,
              'native_calls': 0, 'optimizer_replays': 0, 'independent_physical_replication': False,
              'scope': 'Postseal independent scalar/Fraction/pair-expansion/subset-DP recorded arithmetic; no source import or native replay'}
    OUT.mkdir(exist_ok=False)
    (OUT / 'inspection.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
