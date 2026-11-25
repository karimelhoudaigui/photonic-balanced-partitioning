"""Recorded P55 data audit; no production imports or physical resampling."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import gzip
import hashlib
import json
import math
from pathlib import Path
import random

MODELS = ('bosonic', 'distinguishable', 'species4', 'continuous_phase',
          'independent_B_marginals', 'inclusion_walk')
CASES = ('n20_ER_5502001', 'n20_RR_5502002')
CODE = 'f5563a868e6464e39a669d1fdecfb213374d203d0bf91fea64b7de6d69d422d7'
SPEC = '8b99380f8a79130b508800839c7022264e48d35345c3ef8e89d6846e1f12eba0'


def need(ok, label):
    if not ok:
        raise ValueError(label)


def seed(*parts):
    return int.from_bytes(hashlib.sha256('/'.join(map(str, parts)).encode()).digest()[:4], 'little')


def same(a, b, label):
    need(a == b, label)


def near(a, b, label):
    need(math.isfinite(a) and math.isfinite(b) and abs(a-b) <= 1e-8, label)


def gate(veto, required, eligible, clear):
    if veto: return 'DEV_REJECTED_FIXED_FAST'
    if required: return 'DEV_REJECTED_REQUIRED_CONTROL_MEAN'
    if not eligible: return 'INCONCLUSIVE_FAST_ELIGIBILITY'
    return 'FOLLOW_UP_ONLY' if clear else 'INCONCLUSIVE_MIXED_DEV'


def cut(a, subset):
    need(len(subset) == len(a)//2 and len(set(subset)) == len(subset)
         and all(type(i) is int and 0 <= i < len(a) for i in subset), 'balanced subset')
    chosen = set(subset)
    return sum(a[i][j] for i in chosen for j in range(len(a)) if j not in chosen)


def coefficients_and_rank(counts, subset):
    """Sparse prefix GF and inverse rank, independently of dense unranking."""
    k, total = len(counts)//2, sum(counts)
    tables = [{(0, 0): 1}]
    for value in counts:
        p = tables[-1]; q = dict(p)
        for (chosen, photons), ways in p.items():
            if chosen < k:
                pair = (chosen+1, photons+value)
                q[pair] = q.get(pair, 0) + ways
        tables.append(q)
    available = {s: w for (h, s), w in tables[-1].items() if h == k}
    imbalance = min(abs(2*s-total) for s in available)
    targets = sorted(s for s in available if abs(2*s-total) == imbalance)
    ways = sum(available[s] for s in targets)
    photons = sum(counts[i] for i in subset)
    need(photons in targets, 'neutral minimizer')
    rank = sum(available[s] for s in targets if s < photons)
    chosen = k
    for i in reversed(range(len(counts))):
        if i in subset:
            rank += tables[i].get((chosen, photons), 0)
            chosen -= 1; photons -= counts[i]
    same((chosen, photons), (0, 0), 'inverse rank terminal')
    return imbalance, targets, [available[s] for s in targets], ways, rank


def guards():
    from itertools import combinations
    for counts in ((0, 0, 0, 0), (2, 0, 1, 1), (3, 0, 0, 0), (4, 4, 4, 4)):
        subsets = list(combinations(range(4), 2))
        best = min(abs(2*sum(counts[i] for i in s)-sum(counts)) for s in subsets)
        good = [s for s in subsets if abs(2*sum(counts[i] for i in s)-sum(counts)) == best]
        ranks = [coefficients_and_rank(counts, s)[-1] for s in good]
        same(sorted(ranks), list(range(len(good))), 'synthetic inverse bijection')
    same(cut([[0, 3], [3, 0]], [0]), 3, 'synthetic cut')
    try:
        same(cut([[0, 3], [3, 0]], [0]), 4, 'intentional cut corruption')
    except ValueError:
        pass
    else:
        raise ValueError('corruption guard did not reject')
    for flags, status in (((True, True, False, False), 'DEV_REJECTED_FIXED_FAST'),
                          ((False, True, False, False), 'DEV_REJECTED_REQUIRED_CONTROL_MEAN'),
                          ((False, False, False, False), 'INCONCLUSIVE_FAST_ELIGIBILITY'),
                          ((False, False, True, False), 'INCONCLUSIVE_MIXED_DEV'),
                          ((False, False, True, True), 'FOLLOW_UP_ONLY')):
        same(gate(*flags), status, 'synthetic verdict hierarchy')
    return 11


def recipe(case):
    # Only fixed graph reconstruction uses these libraries; no optical helper.
    import networkx as nx
    import numpy as np
    same(nx.__version__, '3.6.1', 'pinned graph version')
    same(np.__version__, '2.4.6', 'pinned PCG64 version')
    master = 5502001 if case == CASES[0] else 5502002
    graph = (nx.gnp_random_graph(20, 4/19, seed=master) if master == 5502001
             else nx.random_regular_graph(4, 20, seed=master))
    rng = np.random.default_rng(seed(master, 'weights'))
    a = [[0]*20 for _ in range(20)]
    for i, j in sorted(graph.edges()):
        a[i][j] = a[j][i] = int(rng.integers(1, 6))
    return a


def batchkey(row):
    return tuple(row[x] for x in ('case', 'model', 'policy', 'stage', 'trial'))


def policies(model):
    n = 6 if model in ('distinguishable', 'species4', 'inclusion_walk') else 3
    return range(n), 4 if n == 6 else 8


def audit(folder, pins):
    for name, digest in pins.items():
        need(not Path(name).is_absolute() and '..' not in Path(name).parts, 'contained pinned input')
        same(hashlib.sha256((folder/name).read_bytes()).hexdigest(), digest, 'closed input hash '+name)
    def load(name):
        need(name in pins, 'unpinned input '+name)
        raw = (folder/name).read_bytes()
        same(hashlib.sha256(raw).hexdigest(), pins[name], 'input hash '+name)
        return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)
    rawname = 'raw.jsonl.gz'
    raw = (folder/rawname).read_bytes()
    same(hashlib.sha256(raw).hexdigest(), pins[rawname], 'raw hash')
    rows = [json.loads(line) for line in gzip.decompress(raw).splitlines()]
    summary = load('summary.json'); failure = load('failure.json')['failure']
    same(summary['raw_sha256'], pins[rawname], 'summary raw hash')
    same(summary['code_sha256'], CODE, 'primary source pin')
    same(summary['spec_sha256'], SPEC, 'spec pin')
    same(summary['actual_QPU_calls'], 0, 'no actual QPU calls')
    same(summary['actual_QPU_photons'], 0, 'no actual QPU photons')
    same(summary['positive_accepted'], False, 'no positive acceptance')
    same(summary['failure'] if failure else None, failure, 'failure agreement')
    graphs, contexts, shots, rngs, online = {}, {}, defaultdict(list), {}, {}
    fresh_seen = failure_seen = False
    for row in rows:
        kind = row['record_type']
        need(not failure_seen, 'raw records after first_failure')
        if kind == 'supplied_graph':
            case, a = row['case']['id'], row['adjacency']
            need(case in CASES and case not in graphs, 'case recipe/duplicate')
            same(row['case'], {'id': case, 'm': 20, 'k': 10, 'r': 20,
                              'family': 'ER' if case == CASES[0] else 'RR',
                              'seed': 5502001 if case == CASES[0] else 5502002}, 'fixed case source')
            same(a, recipe(case), 'replayed fixed graph')
            need(all(type(x) is int and 0 <= x <= 5 for line in a for x in line), 'integer weights')
            graphs[case] = a
        elif kind == 'shot':
            case, model, policy, stage, trial = key = batchkey(row)
            need(case in graphs and model in MODELS and stage in ('training', 'evaluation'), 'shot tag')
            need(not fresh_seen or stage == 'evaluation', 'training after fresh')
            fresh_seen |= stage == 'evaluation'
            n = row['counts']; subset = row['subset']
            need(len(n) == 20 and all(type(x) is int and 0 <= x <= 20 for x in n), 'integer counts')
            if model != 'independent_B_marginals': same(sum(n), 20, 'physical full count')
            expected_seed = seed(552000 if stage == 'training' else 553000, case, model, policy, trial)
            roles = {'observation': seed(expected_seed, 'observation'), 'neutral_rank': seed(expected_seed, 'neutral_rank')}
            if model == 'continuous_phase':
                roles.update(phase_coefficients=seed(roles['observation'], 'coherent_coefficients'),
                             phase_multinomial=seed(roles['observation'], 'coherent_multinomial'))
            same(row['seed'], expected_seed, 'batch seed'); same(row['seed_roles'], roles, 'role seeds')
            same(row['shot'], len(shots[key]), 'shot order/duplicate')
            value = cut(graphs[case], subset); same(row['cut'], value, 'cut recomputation')
            imbalance, targets, target_ways, ways, rank = coefficients_and_rank(n, subset)
            for field, expected in (('total_count', sum(n)), ('minimum_imbalance', imbalance), ('target_sums', targets),
                                    ('target_ways', target_ways), ('ways', ways), ('uniform_rank', rank),
                                    ('DP_cells', 21*11*(sum(n)+1)), ('collision', any(x > 1 for x in n)),
                                    ('defect_mass_twice', sum(abs(x-1) for x in n))):
                same(row[field], expected, 'shot '+field)
            need(0 <= rank < ways, 'rank range')
            if key not in rngs: rngs[key] = random.Random(roles['neutral_rank'])
            same(rank, rngs[key].randrange(ways), 'private sequential rank RNG')
            shots[key].append(row)
            old = online.get((case, model))
            if old is None or value < old['cut']: online[case, model] = {'cut': value, 'subset': subset}
        else:
            need(kind in ('failed_shot', 'first_failure'), 'unknown record kind')
            need(failure is not None, 'failure record without failure')
            if kind == 'failed_shot':
                same(row['completed_cuts'], [s['cut'] for s in shots[batchkey(row)]], 'retained failed-batch prefix')
            else:
                same({k: v for k, v in row.items() if k != 'record_type'}, failure, 'raw first failure')
                failure_seen = True
    same(failure_seen, failure is not None, 'failure record presence')
    same(summary['completed_shots'], sum(map(len, shots.values())), 'all completed shots')
    complete_batches = set()
    for batch in summary['primary_batches']:
        key = batchkey(batch); need(key not in complete_batches, 'duplicate complete batch'); complete_batches.add(key)
        events = shots[key]; cuts = [e['cut'] for e in events]
        need(bool(events), 'empty complete batch')
        same(batch['seed'], events[0]['seed'], 'batch master metadata')
        same(batch['seed_roles'], events[0]['seed_roles'], 'batch role metadata')
        same(batch['proposals'], len(events), 'batch population'); same(batch['cuts'], cuts, 'all batch cuts')
        same(batch['sum_cuts'], sum(cuts), 'batch sum')
        den = max(1, sum(graphs[key[0]][i][j] for i in range(20) for j in range(i+1, 20)))
        same(batch['weight_denominator'], den, 'weight denominator')
        same(F(batch['exact_mean_normalized_cut']), F(sum(cuts), len(cuts)*den), 'batch mean')
        winner = min(events, key=lambda e: e['cut'])
        same((batch['best_cut'], batch['best_subset']), (winner['cut'], winner['subset']), 'batch best')
        if key[1] in ('bosonic', 'species4'):
            b, t, c = batch['backend'], batch['setup'], batch['classical_setup']
            need(b['cpu_seconds'] is None and c['cpu_seconds'] is None, 'CPU split unavailable')
            same(b['CPU_split_available'], False, 'backend CPU unknown')
            same(c['CPU_split_available'], False, 'classical CPU unknown')
            same(b['backend_wall_source'], 'immutable_factory_reported_backend_seconds', 'backend clock scope')
            need(b['wall_seconds'] <= b['factory_total']['wall_seconds']+1e-8, 'factory nested clock')
            need(b['factory_total']['cpu_seconds'] >= 0, 'factory total CPU retained')
            near(c['wall_seconds'], max(0., t['wall_seconds']-b['wall_seconds']), 'paid factory prefix')
    for case in graphs:
        path = 'context_'+case+'.json.gz'
        if path in pins:
            contexts[case] = load(path)
            same(contexts[case]['case']['id'], case, 'context case')
            for model, arm in contexts[case]['arms'].items():
                same(arm['a'], graphs[case], 'context graph')
                same(arm['classical_preparation'], summary['classical_preparation'][case][model], 'owned preparation clock')
                if model == 'species4':
                    # Permutations use the pinned fixed graph-independent PCG64 generator.
                    import numpy as np
                    for g in (0, 1):
                        expected = np.random.default_rng(seed(551010+g, case)).permutation(20).tolist()
                        same(arm['groupings'][str(g)], expected, 'species grouping')
    for case, models in summary['paid_best_cached_online'].items():
        for model, value in models.items(): same(value, online.get((case, model)), 'online paid cache')
    report = {'successful_shots': sum(map(len, shots.values())), 'complete_batches': len(complete_batches),
              'partial_batches': [list(k) for k in shots if k not in complete_batches], 'failure_preserved': failure is not None}
    if failure is not None:
        same(summary['status'], 'INCONCLUSIVE_FIRST_FAILURE', 'failed main status')
        same(summary['positive_accepted'], False, 'no positive')
        report['verdict'] = 'VALIDATED_RECORDED_PREFIX_ONLY'
        return report
    need(set(graphs) == set(CASES) and len(complete_batches) == 96 and report['successful_shots'] == 480, 'full population')
    same(set(contexts), set(CASES), 'complete context closure')
    for key in ('requested', 'configured_before_work', 'readback_after_work'):
        same(summary['native_threads'][key], 1, 'native API '+key)
    same(summary['B_setup_CPU_split_available'], False, 'no fictional CPU split')
    same(summary['B_factory_prefix_WALL_is_charged'], True, 'paid prefix declaration')
    selection = load('selection.json'); selected, losses = {}, {}
    same(selection['selection_compute'], summary['selection_compute'], 'selection clock consistency')
    for model in MODELS:
        ids, draws = policies(model); loss = {}
        for policy in ids:
            means = []
            for case in CASES:
                keys = [(case, model, policy, 'training', trial) for trial in range(draws//4)]
                need(all(len(shots[k]) == 4 for k in keys), 'training grid population')
                den = max(1, sum(graphs[case][i][j] for i in range(20) for j in range(i+1, 20)))
                means.append(F(sum(s['cut'] for k in keys for s in shots[k]), draws*den))
            loss[policy] = sum(means, F(0))/2
        selected[model] = min(loss, key=lambda k: (loss[k], k)); losses[model] = loss
        same({int(k): F(v) for k, v in selection['losses'][model].items()}, loss, 'training Fraction losses')
        same({int(k): F(v) for k, v in summary['training_losses'][model].items()}, loss, 'summary losses')
        for case in CASES:
            for trial in (0, 1): need(len(shots[(case, model, selected[model], 'evaluation', trial)]) == 8, 'fresh population')
    same(selection['selected'], selected, 'selection'); same(summary['selected_policies'], selected, 'summary selection')
    same(selection['frozen_before_fresh'], True, 'recorded selection declaration')
    means, best, counts = {}, {}, {}
    for model in MODELS:
        means[model], best[model], counts[model] = {}, {}, {}
        for case in CASES:
            train = [s['cut'] for k in shots if k[:2] == (case, model) and k[3] == 'training' for s in shots[k]]
            fresh = [s['cut'] for k in shots if k[:2] == (case, model) and k[3] == 'evaluation' for s in shots[k]]
            den = max(1, sum(graphs[case][i][j] for i in range(20) for j in range(i+1, 20)))
            means[model][case] = F(sum(fresh), 16*den)
            best[model][case] = {'training': min(train), 'fresh': min(fresh), 'paid_total': min(train+fresh)}
            counts[model][case] = {'training': len(train), 'evaluation': len(fresh)}
            same(F(summary['fresh_evaluation_means'][model][case]), means[model][case], 'fresh mean')
        means[model]['equal_graph_mean'] = sum(means[model].values(), F(0))/2
        same(F(summary['fresh_evaluation_means'][model]['equal_graph_mean']), means[model]['equal_graph_mean'], 'global mean')
    same(summary['private_paid_incumbents'], best, 'paid incumbents'); same(summary['proposal_counts'], counts, 'population counts')
    fast = summary['FAST_comparisons']; same(len(fast), 4, 'FAST count')
    same({(f['case'], f['mode']) for f in fast}, {(c, m) for c in CASES for m in ('random', 'spectral')}, 'FAST labels')
    for row in fast:
        case, mode, r = row['case'], row['mode'], row['result']
        batches = [b for b in summary['primary_batches'] if b['case'] == case and b['model'] == 'bosonic']
        budget = summary['classical_preparation'][case]['bosonic']['wall_seconds'] + summary['selection_compute']['bosonic']['wall_seconds']/2
        budget += sum(b[key]['wall_seconds'] for b in batches for key in ('classical_setup', 'postprocessing', 'aggregation'))
        near(row['total_CPU_allowance'], budget, 'B-only allowance')
        near(row['solver_CPU_allowance'], max(0., budget-row['adapter']['cpu_seconds']), 'adapter CPU paid')
        near(r['cpu_budget_seconds'], row['solver_CPU_allowance'], 'solver budget')
        same(row['optical_or_other_model_seconds_granted'], 0., 'no foreign funding')
        same(row['serialization_seconds_granted'], 0., 'no IO funding')
        same(row['seed'], seed(554000, case, mode), 'FAST seed')
        same(r['seed'], row['seed'], 'solver seed'); same(r['initialization'], mode, 'fixed FAST mode')
        same(r['max_proposals'], 100000000, 'fixed FAST cap')
        need(0 <= r['proposal_count'] <= 100000000, 'FAST proposal bound')
        trace = r['trace']; length = len(trace['cpu_seconds'])
        need(all(len(v) == length for v in trace.values()), 'FAST trace lengths')
        need(all(x >= 0 and math.isfinite(x) for x in trace['cpu_seconds']), 'FAST finite clocks')
        same(trace['cpu_seconds'], sorted(trace['cpu_seconds']), 'FAST CPU monotonic')
        same(trace['best_cut'], sorted(trace['best_cut'], reverse=True), 'FAST best monotonic')
        for i, packed in enumerate(trace['best_subset_packbits_little']):
            subset = [j for j in range(20) if packed[j//8] & (1 << (j % 8))]
            same(cut(graphs[case], subset), trace['best_cut'][i], 'FAST trace feasible score')
        eligible = [i for i, t in enumerate(trace['cpu_seconds']) if t <= r['cpu_budget_seconds']]
        idx = eligible[-1] if eligible else None
        same(r['eligible_checkpoint_index'], idx, 'latest eligible checkpoint')
        same(r['has_eligible_result'], idx is not None, 'nullable FAST prefix')
        if idx is not None:
            same(cut(graphs[case], r['best_subset']), r['best_cut'], 'FAST feasible cut')
            same(r['eligible_checkpoint_cpu_seconds'], trace['cpu_seconds'][idx], 'snapshot clock')
            same(r['best_cut'], trace['best_cut'][idx], 'snapshot cut')
            same(r['best_subset'], [j for j in range(20) if trace['best_subset_packbits_little'][idx][j//8] & (1 << (j % 8))], 'cached snapshot subset')
        else:
            same((r['best_cut'], r['best_subset']), (None, None), 'no late best credited')
        scans = [i for i, stage in enumerate(trace['stage']) if stage in ('initial_scan', 'descent_scan')]
        timely = bool(scans and trace['cpu_seconds'][scans[0]] <= r['cpu_budget_seconds'])
        same(r['first_scan_completed_before_deadline'], timely, 'first scan deadline')
        lastcpu = trace['cpu_seconds'][-1] if length else r['validation_cpu_seconds']
        early = (r['guard_blocked_full_scan'] or r['stop_reason'] == 'max_proposals') and lastcpu < r['cpu_budget_seconds']
        same(r['early_cap_inconclusive'], early, 'early guard status')
        same(r['early_wall_inconclusive'], False, 'helper has no wall gate')
        same(r['comparison_acceptance_eligible'], idx is not None and not early, 'helper prefix eligibility')
        same(r['best_snapshot_cached_online'], True, 'declared online cache')
        veto_ok = idx is not None and r['best_cut'] is not None
        strong = veto_ok and r['comparison_acceptance_eligible'] and not r['early_cap_inconclusive'] and not r['early_wall_inconclusive'] and r['first_scan_completed_before_deadline']
        same(row['prefix_eligible_for_veto'], veto_ok, 'veto prefix'); same(row['comparison_acceptance_eligible'], strong, 'strong FAST gate')
        same(row['eligible_best_cut'], r['best_cut'], 'credited FAST best')
    veto = [m for m in ('random', 'spectral') if all(next(f for f in fast if (f['case'], f['mode']) == (c, m))['prefix_eligible_for_veto'] and next(f for f in fast if (f['case'], f['mode']) == (c, m))['eligible_best_cut'] <= best['bosonic'][c]['paid_total'] for c in CASES)]
    notbeaten = [m for m in MODELS[1:] if means['bosonic']['equal_graph_mean'] >= means[m]['equal_graph_mean']]
    required = [m for m in ('distinguishable', 'inclusion_walk') if m in notbeaten]
    eligible = all(f['comparison_acceptance_eligible'] for f in fast)
    clear = eligible and all(best['bosonic'][f['case']]['paid_total'] < f['eligible_best_cut'] for f in fast)
    clear &= all(means['bosonic'][c] < means[m][c] for c in CASES for m in MODELS[1:])
    status = gate(veto, required, eligible, clear)
    for field, expected in (('status', status), ('positive_accepted', False), ('fixed_FAST_veto_algorithms', veto),
                            ('required_control_mean_vetoes', required), ('controls_not_beaten_in_global_fresh_mean', notbeaten),
                            ('FAST_all_eligible', eligible), ('actual_QPU_calls', 0), ('actual_QPU_photons', 0),
                            ('heldout_opened', False), ('optimum_used', False), ('simulated_B_attempts', 80),
                            ('simulated_B_injected_photons', 1600)):
        same(summary[field], expected, 'summary '+field)
    report.update(verdict='RECORDED_COMPLETE_DATA_CHECKED', recomputed_main_status=status, B_paid_incumbents=best['bosonic'])
    return report


def main():
    p = argparse.ArgumentParser(); p.add_argument('--input', type=Path, required=True)
    p.add_argument('--pins', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); args.output.mkdir(parents=True, exist_ok=False)
    report = {'actual_QPU_calls': 0, 'new_physical_draws': 0, 'production_imported': False}
    try:
        report['synthetic_guards'] = guards()
        pins = json.loads(args.pins.read_text())
        report.update(audit(args.input, pins), status='PASS', input_hashes=pins)
    except Exception as error:
        report.update(status='FAIL', error=repr(error))
    (args.output/'check.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'status': report['status'], 'verdict': report.get('verdict')}))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
