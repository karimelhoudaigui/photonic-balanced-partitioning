"""Posthoc P58 permanent-engine replication; scientific imports only in main."""
import argparse
import cmath
from fractions import Fraction as F
import gzip
import hashlib
import importlib.metadata
import inspect
import itertools
import json
import math
import os
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT/'experiments/P58_same_phase_species/run_001'
QUALIFICATION = ROOT/'research/P58_naive_qualification/run_001'
PINS = {
    'data/source_laws.json.gz': '0efca069e2770942e15a9dbb2f583220043c9df5eaad6539dab353576f61c5fc',
    'data/tie_scalars.json.gz': '52bb72479eeead11f00f855ac1ba4c31732d59381c0539ad0cb69be2c5c61660',
    'data/summary.json': '7f82c318ec591e232d9c765ce82618635876fcc09170f1e815602491ce29f1fe',
    'manifest.json': 'f03c242c81cf31a5a767a9e6cab5ac2c93a7c7466c8c45934277f0ffb80eb8a4',
}
AMP_TOL, MATRIX_TOL = 5e-10, 5e-12
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')


def require(ok, message):
    if not ok: raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n')


def fresh(path):
    path = Path(path).absolute()
    require(not path.exists() and '..' not in path.parts and path.is_relative_to(ROOT), 'fresh project output required')
    require(not path.is_relative_to(REFERENCE), 'historical reference immutable')
    parent = path
    while parent != ROOT:
        require(not parent.is_symlink(), 'symlink output ancestor')
        parent = parent.parent
    return path


def unitary():
    """Scalar trig plus crossed bit characters, original Walsh port order."""
    rows = []
    for out in range(8):
        rail, color = divmod(out, 4)
        row = []
        for inp in range(8):
            source_rail, port = divmod(inp, 4)
            parity = ((color & 1)*(port >> 1)+(color >> 1)*(port & 1)+rail*source_rail) % 2
            phase = source_rail*color*math.pi/3
            row.append((-1 if parity else 1)*complex(math.cos(phase), math.sin(phase))/math.sqrt(8))
        rows.append(row)
    return rows


def occupations(photons):
    for slots in itertools.combinations_with_replacement(range(8), photons):
        n = [0]*8
        for i in slots: n[i] += 1
        yield tuple(n)


def key16(counts):
    require(all(type(x) is int and 0 <= x <= 8 for x in counts), 'base16 digit')
    return sum(x << (4*i) for i, x in enumerate(counts))


def read9(key):
    n = []
    for _ in range(8): key, digit = divmod(key, 9); n.append(digit)
    require(key == 0, 'archive key overflow')
    return tuple(n)


def tie_scalar(n):
    """Uniform top4 via boundary hypergeometric inclusion, no subset iterator."""
    threshold = sorted(n, reverse=True)[3]
    high = {i for i, x in enumerate(n) if x > threshold}
    boundary = {i for i, x in enumerate(n) if x == threshold}
    choose, size = 4-len(high), len(boundary)
    def single(i):
        return F(1) if i in high else F(choose, size) if i in boundary else F(0)
    def joint(i, j):
        if i in high: return single(j)
        if j in high: return single(i)
        if i in boundary and j in boundary: return F(choose*(choose-1), size*(size-1))
        return F(0)
    def crossing(i, j): return single(i)+single(j)-2*joint(i, j)
    scaled = 420*(crossing(0, 4)-crossing(1, 5))
    require(scaled.denominator == 1, 'integer hypergeometric tie scalar')
    return scaled.numerator


def stdlib_guards():
    checks = [tie_scalar((0,)*8) == 0, tie_scalar((2,2,2,2,0,0,0,0)) == 0,
              tie_scalar((3,2,1,1,1,0,0,0)) == -280,
              key16((2,0,0,0,0,0,0,7))+key16((6,0,0,0,0,0,0,1)) == key16((8,0,0,0,0,0,0,8)),
              sum(math.comb(8, r)*math.comb(r+7, 7) for r in range(1,9)) == 157183]
    try: fresh(ROOT)
    except ValueError: checks.append(True)
    else: checks.append(False)
    require(all(checks), 'stdlib guard failure')
    return len(checks)


def configure_native(xq):
    before = int(xq.Config.compute_max_thread_count)
    xq.Config.compute_max_thread_count = 1
    after = int(xq.Config.compute_max_thread_count)
    require(after == 1, 'official native maximum not one')
    return {'interface': 'exqalibur.Config.compute_max_thread_count', 'before': before,
            'requested': 1, 'configured_before_work': after,
            'interpretation': 'documented native maximum only, not observed OS scheduling'}


def load_api():
    cache = os.environ.setdefault('MPLCONFIGDIR', '/Users/karimelhoudaigui/Desktop/pasqal/.local/mplconfig')
    Path(cache).mkdir(parents=True, exist_ok=True)
    import numpy as np
    import exqalibur as xq
    native = configure_native(xq)  # Before Perceval or any permanent call.
    from perceval.backends import NaiveBackend
    from perceval.components import Unitary
    from perceval.utils import FockState
    versions = {name: importlib.metadata.version(name) for name in ('numpy','perceval-quandela','exqalibur')}
    require(versions == {'numpy':'2.4.6','perceval-quandela':'1.3.0','exqalibur':'1.4.2'}, 'pinned scientific versions')
    backend_file = inspect.getfile(NaiveBackend)
    files = {'NaiveBackend':backend_file, 'Unitary':inspect.getfile(Unitary), 'exqalibur':xq.__file__}
    for name, module in tuple(sys.modules.items()):
        path = getattr(module, '__file__', None)
        if name.startswith('exqalibur') and path and path.endswith(('.so','.pyd')): files[name] = path
    meta = {'versions': versions, 'native': native, 'MPLCONFIGDIR': cache,
            'cache_note': 'persistent config only; no warm/cold performance claim',
            'thread_environment': {k: os.environ.get(k) for k in THREADS},
            'engine_files': {name:{'path':path,'sha256':sha(path)} for name,path in files.items()},
            'backend': 'local NaiveBackend.prob_amplitude -> exqalibur.permanent_cx; no pruning, mask, iterator or remote',
            'Config_doc': xq.Config.__doc__, 'permanent_doc': xq.permanent_cx.__doc__}
    return (np, xq, NaiveBackend, Unitary, FockState), meta


def backend_for(matrix, source, api):
    np, _, NaiveBackend, Unitary, FockState = api
    b = NaiveBackend(); b.set_circuit(Unitary(np.asarray(matrix, dtype=complex)))
    b.set_input_state(FockState(source))
    return b


def qualification(api):
    _, _, _, _, State = api
    hom = [[1/math.sqrt(2), 1j/math.sqrt(2)], [1j/math.sqrt(2), 1/math.sqrt(2)]]
    b = backend_for(hom, [1,1], api)
    values = [('HOM_CF', b.prob_amplitude(State([1,1])), 0j),
              ('HOM_bunch', b.prob_amplitude(State([2,0])), 1j/math.sqrt(2))]
    phi = .37
    u = [[.6, -.8*cmath.exp(1j*phi)], [.8*cmath.exp(-1j*phi), .6]]
    b = backend_for(u, [1,0], api)
    values.append(('partial_source_complex_orientation', b.prob_amplitude(State([0,1])), .8*cmath.exp(-1j*phi)))
    b.set_input_state(State([0,0])); values.append(('vacuum', b.prob_amplitude(State([0,0])), 1))
    own = unitary()
    residual = max(abs(sum(own[r][i].conjugate()*own[r][j] for r in range(8))-(i == j)) for i in range(8) for j in range(8))
    values.append(('eight_mode_Gram_only', residual, 0))
    checks = [{'name':name, 'observed':[float(complex(x).real),float(complex(x).imag)],
               'expected':[float(complex(y).real),float(complex(y).imag)],
               'absolute_error':float(abs(x-y)), 'pass':bool(abs(x-y) <= MATRIX_TOL)} for name,x,y in values]
    require(all(c['pass'] for c in checks), 'tiny qualification mismatch')
    return {'physics_checks':checks, 'P58_source_probabilities_evaluated':0, 'P58_reference_files_opened':False}


def check_reference():
    for name, digest in PINS.items():
        p = REFERENCE/name
        require(not p.is_symlink() and sha(p) == digest, 'historical reference pin '+name)


def check_qualification():
    manifest = json.loads((QUALIFICATION/'manifest.json').read_text())
    report_path = QUALIFICATION/'data/report.json'
    report = json.loads(report_path.read_text())
    require(manifest['schema_version'] == 2 and manifest['run']['status'] == 'completed'
            and manifest['run']['exit_status'] == 0, 'completed qualification required')
    require(report['status'] == 'PASS' and report['mode'] == 'qualify'
            and report['code_sha256'] == sha(__file__), 'same-source qualification required')
    require(report['P58_source_probabilities_evaluated'] == 0
            and not report['P58_reference_files_opened'], 'qualification scope')
    own = str(Path(__file__).relative_to(ROOT)); current = sha(__file__)
    inputs = {x['path']:x for x in manifest['input_artifacts']}
    require(inputs[own]['sha256'] == inputs[own]['sha256_after'] == current, 'qualification source closure')
    outputs = {x['path']:x['sha256'] for x in manifest['outputs']}
    require(outputs[str(report_path.relative_to(ROOT))] == sha(report_path), 'qualification report hash')
    return {'manifest_sha256':sha(QUALIFICATION/'manifest.json'), 'report_sha256':sha(report_path)}


def full_replication(api, output):
    _, _, _, _, State = api
    def read(name):
        raw = (REFERENCE/'data'/name).read_bytes()
        if name.endswith('.gz'): raw = gzip.decompress(raw)
        require(len(raw) <= 64*1024*1024, 'inflated input bound')
        return json.loads(raw)
    archive, old_ties, primary = read('source_laws.json.gz'), read('tie_scalars.json.gz'), read('summary.json')
    own, xi = unitary(), cmath.exp(1j*math.pi/3)
    alignment = max(abs(own[i][j]-(archive['matrix'][i][j][0]+archive['matrix'][i][j][1]*xi)/math.sqrt(8)) for i in range(8) for j in range(8))
    require(alignment <= MATRIX_TOL, 'independent matrix alignment')
    groups = {row['input_mask']:row for row in archive['laws']}
    require(len(groups) == len(archive['laws']) == 255 and set(groups) == set(range(1,256)), 'all255 source masks')
    b = backend_for(own, [0]*8, api)
    states = {r:[(n,key16(n),State(n),math.prod(math.factorial(x) for x in n)) for n in occupations(r)] for r in range(1,9)}
    laws, diagnostics, maximum, total = {}, [], 0., 0
    native_path = output/'native_amplitudes.jsonl.gz'
    with gzip.GzipFile(filename=str(native_path), mode='wb', mtime=0) as stream:
        stream.write((json.dumps({'record_type':'independent_matrix','theta':math.pi/3,
                                  'real':[[z.real for z in row] for row in own],
                                  'imag':[[z.imag for z in row] for row in own]},separators=(',',':'))+'\n').encode())
        for mask in range(1,256):
            group = [j for j in range(8) if mask & (1 << j)]; r = len(group)
            saved = groups[mask]
            require(saved['group'] == group and saved['denominator'] == 8**r, 'archive input ports/denominator')
            ref = {}
            for key, a, c, weight in saved['states']:
                n = read9(key); target = key16(n)
                require(sum(n) == r and target not in ref and all(type(v) is int for v in (a,c,weight)), 'archive occupation/types')
                factor = math.prod(math.factorial(x) for x in n)
                require(weight == (a*a+a*c+c*c)*factor, 'archive normalization weight')
                ref[target] = (a,c,weight)
            require(set(ref) == {k for _,k,_,_ in states[r]} and len(ref) == math.comb(r+7,7), 'complete multiset alignment')
            require(sum(v[2] for v in ref.values()) == 8**r, 'exact source mass')
            b.set_input_state(State([int(j in group) for j in range(8)]))
            amplitudes, probabilities, error, zero_error, zeros = [], [], 0., 0., 0
            for n, key, state, factor in states[r]:
                value = complex(b.prob_amplitude(state)); a,c,weight = ref[key]
                expected = (a+c*xi)*math.sqrt(factor)/(math.sqrt(8)**r)
                require(math.isfinite(value.real) and math.isfinite(value.imag), 'nonfinite native amplitude')
                error = max(error, abs(value-expected))
                if a == c == 0: zeros += 1; zero_error = max(zero_error, abs(value))
                probabilities.append(abs(value)**2)
                amplitudes.append([key,value.real,value.imag])
            mass = math.fsum(probabilities); total += len(amplitudes); maximum = max(maximum,error)
            diagnostic = {'input_mask':mask,'photons':r,'states':len(amplitudes),'native_mass':mass,
                          'max_abs_amplitude_error':error,'exact_zero_states':zeros,'max_zero_amplitude':zero_error}
            diagnostics.append(diagnostic)
            stream.write((json.dumps({'record_type':'source_group','input_mask':mask,'group':group,'base':16,
                                      'diagnostic':diagnostic,'amplitudes':amplitudes},separators=(',',':'),allow_nan=False)+'\n').encode())
            laws[mask] = {key:v[2] for key,v in ref.items()}
    require(total == 157183 and maximum <= AMP_TOL, 'native complete amplitude agreement')
    require(all(abs(d['native_mass']-1) <= AMP_TOL for d in diagnostics), 'all native source masses')
    ties = {key16(n):tie_scalar(n) for n in occupations(8)}
    reference_ties = {key16(read9(key)):value for key,value in old_ties['values']}
    require(len(ties) == len(reference_ties) == len(old_ties['values']) == 6435 and ties == reference_ties and old_ties['scale'] == 420, 'all hypergeometric tie scalars')
    denominator = 840*8**8
    target = F(sum(w*ties[k] for k,w in laws[255].items()), denominator)
    rational = lambda d:F(d['numerator'],d['denominator'])
    require(target == F(-767,327680) == rational(primary['B_mean']), 'full-B exact mean')
    controls = {}
    for row in primary['controls']:
        mask = sum(1 << j for j in row['input_group']); canonical = min(mask,255 ^ mask)
        require(canonical not in controls, 'duplicate unordered reference control'); controls[canonical] = row
    require(set(controls) == set(range(1,128)), 'all127 unordered control masks')
    results = []; pair_terms = 0
    for mask in range(1,128):
        left, right = laws[mask], laws[255 ^ mask]
        pair_terms += len(left)*len(right)
        numerator = sum(v*w*ties[k+h] for k,v in left.items() for h,w in right.items())
        mean = F(numerator,denominator); gap = mean-target; ref = controls[mask]
        require(mean == rational(ref['mean']) and gap == rational(ref['gap_above_B']), 'exact two-species mean')
        results.append({'left_mask':mask,'right_mask':255 ^ mask,'reference_group':ref['input_group'],
                        'mean':str(mean),'gap_above_B':str(gap)})
    minimum = min(F(r['gap_above_B']) for r in results)
    status = 'SAME_PHASE_ALL_BIPARTITIONS_SEPARATED' if minimum > 0 else 'STRONGER_SAME_PHASE_SPECIES_INTERPRETATION_REFUTED'
    require(minimum == rational(primary['minimum_gap']) and status == primary['status'], 'exact decision/minimum')
    require(pair_terms == 11083116, 'all convolution terms')
    save(output/'independent_ties_and_means.json', {'base':16,'tie_scale':420,'ties':sorted(ties.items()),'B_mean':str(target),'controls':results})
    return {'source_groups':255,'native_amplitudes':total,'max_abs_amplitude_error':maximum,
            'matrix_alignment_error':alignment,'source_diagnostics':diagnostics,'exact_tie_scalars':len(ties),
            'exact_control_means':127,'convolution_pairs':pair_terms,'minimum_gap':str(minimum),
            'reference_decision_recomputed':status,'reference_hashes':PINS,
            'interpretation':'finite numerical amplitude corroboration plus independent exact tie/convolution arithmetic; not an interval certificate or new physical sampling'}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--mode', choices=('qualify','full'), required=True)
    p.add_argument('--output', type=Path, required=True); args = p.parse_args()
    output = fresh(args.output); output.mkdir(parents=True, exist_ok=False)
    wall, cpu = time.perf_counter(), time.process_time()
    report = {'mode':args.mode,'posthoc_not_blind':True,'production_imported':False,
              'physical_draws':0,'actual_QPU_calls':0,'positive_optimizer_accepted':False,
              'genuine_order8_claimed':False,'code_sha256':sha(__file__)}
    api = meta = None
    try:
        report['stdlib_guards'] = stdlib_guards()
        if args.mode == 'full':
            report['qualification_gate'] = check_qualification()
            check_reference()
        api, meta = load_api(); report['provenance'] = meta
        report.update(qualification(api) if args.mode == 'qualify' else full_replication(api,output))
        after = int(api[1].Config.compute_max_thread_count)
        meta['native']['readback_after_work'] = after
        require(after == 1, 'native maximum after work')
        if args.mode == 'full': check_reference()
        report['status'] = 'PASS'
    except Exception as error:
        report.update(status='FAIL',error=repr(error))
        if api is not None:
            try: meta['native']['readback_after_failure'] = int(api[1].Config.compute_max_thread_count)
            except Exception as observation_error: meta['native']['failure_readback_unavailable'] = repr(observation_error)
    report.update(cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,
                  peak_rss_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  rss_unit='bytes' if sys.platform == 'darwin' else 'KiB_on_Linux_platform_dependent')
    save(output/'report.json',report)
    print(json.dumps({'status':report['status'],'mode':args.mode,'native_amplitudes':report.get('native_amplitudes',0)}))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
