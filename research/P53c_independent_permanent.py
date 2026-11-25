"""Complete posthoc K4 permanent/control replication, stdlib only, no LP."""
import argparse, gzip, hashlib, itertools, json, math, resource, sys, time
from fractions import Fraction as F
from pathlib import Path
if not __debug__: raise RuntimeError("assertion-enabled Python is required")

ROOT = Path(__file__).resolve().parents[1]
OLD = "experiments/P53b_fixed_point/run_001/data/certificate.json.gz"
NEW = "experiments/P53c_same_phase/run_001/data/certificate.json.gz"
PINS = {OLD: "bd9874399ffed241b045f09a5a4f155d7d60263e7314a55e1bfd2358c9022dbe",
        NEW: "408140f0a1a3865e374256d2a1e797961adcf6742cd8b1d234c2c7b4b2cbc065"}
EDGES = tuple(itertools.combinations(range(8), 2)); GROUPS = tuple(itertools.combinations(range(8), 4))
SPLITS = tuple(g for g in GROUPS if 0 in g); PERMS = tuple(itertools.permutations(range(4)))
DEN4, DEN8, KD = 8**4, 8**8, 420*8**8

def q(z):
    if type(z) is int: return F(z)
    assert type(z) is dict and set(z) == {"numerator", "denominator"}
    a, b = z["numerator"], z["denominator"]
    assert type(a) is int and type(b) is int and b > 0 and math.gcd(a, b) == 1
    return F(a, b)
def vector(z): return tuple(q(x) for x in z)
def dot(a, b):
    assert len(a) == len(b)
    return sum((x*y for x, y in zip(a, b)), F(0))
def encode(z):
    if isinstance(z, F): return {"numerator": z.numerator, "denominator": z.denominator}
    if isinstance(z, dict): return {k: encode(v) for k, v in z.items()}
    if isinstance(z, (list, tuple)): return [encode(x) for x in z]
    return z
def load(path, pin):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == pin
    with gzip.open(path, "rb") as stream: data = stream.read(16*1024**2+1)
    assert len(data) <= 16*1024**2
    return json.loads(data)

def mul(a, b): return a[0]*b[0]-3*a[1]*b[1], a[0]*b[1]+a[1]*b[0]
def matrix():
    def entry(r, c):
        j, a = r % 4, c % 4
        sign = (-1)**((j//2)*(a % 2)+(j % 2)*(a//2)+(r//4)*(c//4))
        x, y = ((2, 0), (1, 1), (-1, 1), (-2, 0))[j if c >= 4 else 0]
        return sign*x, sign*y
    return tuple(tuple(entry(r, c) for c in range(8)) for r in range(8))
def permanent_num(mat, rows, group):
    a, b = 0, 0
    for permutation in PERMS:
        z = (1, 0)
        for row, j in zip(rows, permutation): z = mul(z, mat[row][group[j]])
        a += z[0]; b += z[1]
    return a, b
def probability_num(pair, occupation):
    factorial = math.prod(math.factorial(n) for n in occupation)
    value, remainder = divmod(pair[0]**2+3*pair[1]**2, 256*factorial)
    assert remainder == 0 and value >= 0
    return value
def count_space(total):
    slots = tuple(itertools.combinations_with_replacement(range(8), total))
    return slots, tuple(tuple(row.count(i) for i in range(8)) for row in slots)
def align(raw, expected):
    assert len(raw) == len(expected) and all(len(n) == 8 and all(type(x) is int for x in n) for n in raw)
    positions = {tuple(n): i for i, n in enumerate(raw)}
    assert len(positions) == len(expected) and set(positions) == set(expected)
    return tuple(positions[n] for n in expected)
def tie_function(n):
    scores = [sum(n[i] for i in subset) for subset in GROUPS]; best = max(scores)
    chosen = [subset for subset, score in zip(GROUPS, scores) if score == best]
    difference = sum(((0 in s) != (4 in s))-((1 in s) != (5 in s)) for s in chosen)
    value, remainder = divmod(420*difference, len(chosen))
    assert remainder == 0
    return value
def convolve(a, b, mapping, size):
    values = [0]*size
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: values[mapping[i][j]] += x*y
    assert min(values) >= 0 and sum(values) == DEN8
    return tuple(values)

def guards(mat):
    for a in range(8):
        for b in range(8):
            terms = [mul((mat[r][a][0], -mat[r][a][1]), mat[r][b]) for r in range(8)]
            assert (sum(x for x, y in terms), sum(y for x, y in terms)) == ((32, 0) if a == b else (0, 0))
    for rows, n, expected in (((0,)*4, (4,0,0,0,0,0,0,0), 24), ((0,0,1,1), (2,2,0,0,0,0,0,0), 16), ((0,1,2,3), (1,1,1,1,0,0,0,0), 64)):
        assert probability_num(permanent_num(mat, rows, (0,1,2,3)), n) == expected
    assert tie_function((1,)*8) == 0 and tie_function((2,1,1,1,0,1,1,1)) == 168

def reconstruct(old, new):
    b = vector(old["target_exact"]); w = vector(old["dual_exact"]["signed_weights"])
    expected_w = tuple(F(1,2) if e == (0,4) else F(-1,2) if e == (1,5) else F(0) for e in EDGES)
    assert w == expected_w and q(old["x"]) == q(new["x"]) == F(1,4) and sum(b) == 16
    V = tuple(vector(v) for v in old["library_exact"]); expanded = tuple(vector(v) for v in new["library_exact"])
    assert len(V) == 71 and len(expanded) == 106 and expanded[:71] == V and vector(new["target_exact"]) == b
    target = dot(w, b); old_gap = min(dot(w, v)-target for v in V)
    assert old_gap > 0 and all(len(v) == 28 and sum(v) == 16 for v in expanded)
    graph = vector(old["nonnegative_graph_witness"]["weights_normalized_sum_one"])
    scale = q(old["nonnegative_graph_witness"]["weight_sum"]); shift = q(old["nonnegative_graph_witness"]["uniform_edge_shift"])
    assert scale > 0 and min(graph) >= 0 and sum(graph) == 1 and graph == tuple((x+shift)/scale for x in w)
    assert vector(new["saved_P53b_signed_weights"]) == w and vector(new["saved_P53b_graph_normalized"]) == graph and new["P53b_checkpoint_sha256"] == PINS[OLD]
    raw = new["new_controls_raw"]; rows4, ns4 = count_space(4); _, ns8 = count_space(8)
    ix4, ix8 = align(raw["counts4"], ns4), align(raw["counts8"], ns8)
    assert tuple(map(tuple, raw["groups"])) == GROUPS and raw["group_denominator"] == DEN4 and raw["occupation_denominator"] == DEN8 and raw["kernel_denominator"] == KD
    labels = [{"kind":"b4", "theta":"pi/3", "groups":[list(g), [i for i in range(8) if i not in g]]} for g in SPLITS]
    assert raw["labels"] == labels and new["library_labels"] == old["library_labels"]+labels
    mat = matrix(); guards(mat); group_probs, group_permanents = [], []
    assert len(raw["group_probability_numerators"]) == len(raw["group_coefficients_xi"]) == 70
    assert all(len(row) == 330 for key in ("group_probability_numerators", "group_coefficients_xi") for row in raw[key])
    for gi, group in enumerate(GROUPS):
        probabilities, permanents = [], []
        for k, (rows, n) in enumerate(zip(rows4, ns4)):
            pair = permanent_num(mat, rows, group); value = probability_num(pair, n)
            coeff = raw["group_coefficients_xi"][gi][ix4[k]]; f = math.prod(math.factorial(x) for x in n)
            assert len(coeff) == 2 and all(type(x) is int for x in coeff)
            assert pair == (8*f*(2*coeff[0]+coeff[1]), 8*f*coeff[1]), (group, n, "coefficient mismatch")
            assert type(raw["group_probability_numerators"][gi][ix4[k]]) is int and value == raw["group_probability_numerators"][gi][ix4[k]], (group, n, "probability mismatch")
            probabilities.append(value); permanents.append(pair)
        assert sum(probabilities) == DEN4
        group_probs.append(tuple(probabilities)); group_permanents.append(tuple(permanents))
        print("checked group", group, flush=True)
    code = lambda n: sum(value*9**i for i, value in enumerate(n))
    index8 = {code(n): i for i, n in enumerate(ns8)}; codes4 = tuple(code(n) for n in ns4)
    mapping = tuple(tuple(index8[a+b] for b in codes4) for a in codes4)
    functional = tuple(tie_function(n) for n in ns8); group_index = {g: i for i, g in enumerate(GROUPS)}
    laws, means, gaps = [], [], []
    assert len(raw["occupation_numerators"]) == len(raw["crossing_numerators"]) == 35
    assert all(len(row) == 6435 for row in raw["occupation_numerators"])
    for j, g in enumerate(SPLITS):
        complement = tuple(i for i in range(8) if i not in g)
        values = convolve(group_probs[group_index[g]], group_probs[group_index[complement]], mapping, len(ns8))
        assert all(type(raw["occupation_numerators"][j][ix8[k]]) is int and x == raw["occupation_numerators"][j][ix8[k]] for k, x in enumerate(values)), (g, "convolution mismatch")
        mean = F(sum(x*a for x, a in zip(values, functional)), 2*KD)
        crossing = raw["crossing_numerators"][j]
        assert len(crossing) == 28 and all(type(x) is int for x in crossing)
        assert mean == F(crossing[EDGES.index((0,4))]-crossing[EDGES.index((1,5))], 2*KD) == dot(w, expanded[71+j])
        laws.append(values); means.append(mean); gaps.append(mean-target)
        print("checked split", g, flush=True)
    normalized = tuple(x/scale for x in gaps); diagnostic = new["fixed_old_graph_diagnostic"]
    assert tuple(gaps) == vector(diagnostic["signed_margins"]) and normalized == vector(diagnostic["normalized_graph_margins"])
    assert min(normalized) == q(diagnostic["minimum_normalized_margin"])
    assert diagnostic["new_controls_strictly_better_than_fixed_B_on_old_graph"] == sum(x < 0 for x in normalized)
    assert diagnostic["status"] == ("OLD_GRAPH_BEATEN_BY_NEW_CONTROL" if min(normalized) < 0 else "OLD_GRAPH_TIED_BY_NEW_CONTROL" if min(normalized) == 0 else "OLD_GRAPH_STRICT_GAP_RETAINS35")
    replica = {"unitary_entry_numerators_den2sqrt8_basis_1_i_sqrt3": mat, "groups": GROUPS, "counts4": ns4, "counts8": ns8, "permanent_numerators_den16_unscaled_sqrt8U": group_permanents, "group_probability_numerators_den4096": group_probs, "splits": SPLITS, "occupation_numerators_den8pow8": laws, "tie_functional_numerators_den840": functional, "signed_means": means, "signed_margins": gaps, "normalized_graph_margins": normalized}
    report = {"replication": "EXACT_COMPLETE_MATCH", "old_witness_separates106": min(gaps) > 0, "target_signed_mean": target, "old71_gap": old_gap, "minimum_new_signed_gap": min(gaps), "minimum_new_normalized_graph_gap": min(normalized), "production_permanent_calls": 70*330, "production_permanent_terms": 70*330*24, "toy_permanent_calls": 3, "Gram_Fock_tie_guards_passed": True, "new_groups": 70, "new_splits": 35, "all_occupations_per_split": 6435, "new_LP_dual_audited": False, "posthoc_not_blind": True, "physical8source_reconstructed": False}
    return replica, report

def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--output", type=Path, required=True); args = p.parse_args()
    output = args.output.resolve()
    if output.exists() or not output.is_relative_to(ROOT): raise ValueError("fresh project output required")
    cpu, wall = time.process_time(), time.monotonic()
    replica, report = reconstruct(*(load(ROOT/path, pin) for path, pin in PINS.items()))
    output.mkdir(parents=True)
    payload = (json.dumps(encode(replica), separators=(",",":"), allow_nan=False)+"\n").encode()
    assert len(payload) <= 4*1024**2-65536
    with (output/"replica.json.gz").open("xb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as stream: stream.write(payload)
    report.update({"inputs": PINS, "python": sys.version, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "CPU_seconds": time.process_time()-cpu, "wall_seconds": time.monotonic()-wall, "max_RSS_native_units": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, "RSS_unit": "bytes on Darwin; KiB on Linux", "replica_sha256": hashlib.sha256((output/"replica.json.gz").read_bytes()).hexdigest()})
    text = json.dumps(encode(report), indent=2, allow_nan=False)+"\n"; assert len(text.encode()) <= 65536
    (output/"report.json").write_text(text); assert sum(f.stat().st_size for f in output.iterdir()) <= 4*1024**2
    print(text)

if __name__ == "__main__": main()
