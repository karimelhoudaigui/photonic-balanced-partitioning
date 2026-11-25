"""Posthoc stdlib exact checker; no production import or physical reconstruction."""
import argparse, gzip, hashlib, itertools, json, math, sys, time
from fractions import Fraction as F
from pathlib import Path
if not __debug__: raise RuntimeError("assertion-enabled Python is required")

ROOT = Path(__file__).resolve().parents[1]
EDGES = tuple(itertools.combinations(range(8), 2)); DEN = 420 * 8**8
PINS = {
    "experiments/P53_exact_phase/run_001/data/exact_source.json.gz": "2a593abba088327ccb8b54f5f14bab6f8edcf5fc42128de6c31f394bf454d7a0",
    "experiments/P53_exact_phase/run_001/data/exact_library.json.gz": "cb210de13928e365b8983c2a17b882623a346975b522293fd549b6980871963b",
    "experiments/P53b_fixed_point/run_001/data/certificate.json.gz": "bd9874399ffed241b045f09a5a4f155d7d60263e7314a55e1bfd2358c9022dbe"}

def q(z):
    if type(z) is int: return F(z)
    assert type(z) is dict and set(z) == {"numerator", "denominator"}
    a, b = z["numerator"], z["denominator"]
    assert type(a) is int and type(b) is int and b > 0 and math.gcd(a, b) == 1
    return F(a, b)

def vec(z): return tuple(q(x) for x in z)
def dot(a, b):
    assert len(a) == len(b)
    return sum((x*y for x, y in zip(a, b)), F(0))
def incident(v, total):
    return len(v) == 28 and sum(v) == total and all(sum(v[e] for e, edge in enumerate(EDGES) if i in edge) == total/4 for i in range(8))
def primal_ok(V, b, lam):
    return len(lam) == len(V) and min(lam) >= 0 and sum(lam) == 1 and all(sum(lam[i]*V[i][j] for i in range(len(V))) == b[j] for j in range(28))
def dual_ok(V, b, w):
    margins = tuple(dot(w, v)-dot(w, b) for v in V)
    return sum(map(abs, w)) <= 1 and min(margins) > 0, margins
def gate(p): return p.get("solver_fit_solved") is True and p.get("solver_status") == 0 and p.get("solver_success") is True

def load(path, pin):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == pin
    with gzip.open(path, "rb") as stream: payload = stream.read(16*1024**2+1)
    assert len(payload) <= 16*1024**2
    return json.loads(payload)

def verify(s, c, e):
    assert s["kernel_denominator"] == c["denominator"] == DEN
    powers = tuple(vec(r) for r in s["crossing_power"])
    assert len(powers) == 28 and all(len(r) == 7 for r in powers)
    for j in range(7): assert incident(tuple(r[j] for r in powers), F(16 if j == 0 else 0))
    raw = c["crossing_numerators"]
    assert len(raw) == 71 and all(len(r) == 28 and all(type(x) is int and 0 <= x <= DEN for x in r) for r in raw)
    V = tuple(tuple(F(x, DEN) for x in r) for r in raw)
    b = tuple(sum((coefficient * F(1, 4)**j for j, coefficient in enumerate(r)), F(0)) for r in powers)
    assert incident(b, F(16)) and all(0 <= x <= 1 for x in b) and all(incident(v, F(16)) for v in V)
    labels = [{"kind": "b4", "theta": phase, "groups": [list(g), [i for i in range(8) if i not in g]]} for phase in ("0", "pi/2") for g in itertools.combinations(range(8), 4) if 0 in g] + [{"kind": "uniform70"}]
    assert V[-1] == (F(4, 7),)*28 and c["labels"] == e["library_labels"] == labels
    assert q(e["x"]) == F(1, 4) and vec(e["target_exact"]) == b and tuple(vec(r) for r in e["library_exact"]) == V
    for name, path in zip(("source_artifact", "library_artifact"), list(PINS)[:2]): assert e[name] == {"path": path, "sha256": PINS[path]}
    pe, de = e["primal_exact"], e["dual_exact"]
    pv = primal_ok(V, b, vec(pe.get("weights", []))); coords = e["dual_proposal"].get("signed_float_coordinates")
    dv = False; gap = None
    if coords is not None:
        assert len(coords) == 28 and all(type(x) in (float, int) and math.isfinite(x) for x in coords)
        binary = tuple(F.from_float(float(x)) for x in coords); norm = sum(map(abs, binary)); divisor = max(F(1), norm)
        w = tuple(x/divisor for x in binary); dv, margins = dual_ok(V, b, w); gap = min(margins)
        for key, values in (("binary_signed_coordinates", binary), ("signed_weights", w), ("all_vertex_margins", margins)): assert vec(de[key]) == values
        for key, value in (("binary_L1", norm), ("exact_rescaling_divisor", divisor), ("exact_L1", sum(map(abs, w))), ("level", min(dot(w, v) for v in V)), ("target_mean", dot(w, b)), ("strict_margin", gap)): assert q(de[key]) == value
        assert de["all_strict_inequalities"] is (min(margins) > 0)
    assert pe["verified"] is pv and de["verified"] is dv and not (pv and dv)
    pg, dg = gate(e["primal_proposal"]), gate(e["dual_proposal"])
    assert e["primal_solver_gate"] is pg and e["dual_solver_gate"] is dg
    expected = "EXACT_POINT_MEMBERSHIP_CERTIFIED" if pv and pg else "EXACT_POINT_ENDPOINT71_SEPARATION_CERTIFIED" if dv and dg else "INCONCLUSIVE_AT_FIXED_X"
    assert e["status"] == expected and e["LP_provider_calls"] == e["native_LP_calls_upper_bound"] == 2
    g = e["nonnegative_graph_witness"]
    if dv:
        shift = max(F(0), -min(w)); a = tuple(x+shift for x in w); total = sum(a)
        assert min(a) >= 0 and total > 0 and tuple(map(tuple, g["edges_lexicographic"])) == EDGES
        normalized = tuple(x/total for x in a); gm = tuple(dot(a, v)-dot(a, b) for v in V)
        assert min(gm) == gap > 0 and min(dot(normalized, v)-dot(normalized, b) for v in V) == gap/total
        for key, values in (("weights_nonnegative", a), ("weights_normalized_sum_one", normalized), ("all_graph_margins", gm)): assert vec(g[key]) == values
        for key, value in (("uniform_edge_shift", shift), ("weight_sum", total), ("strict_mean_gap", gap), ("normalized_strict_mean_gap", gap/total)): assert q(g[key]) == value
        assert g["label"] == "POSTHOC_ADVERSARIAL_GRAPH_WITNESS_ENDPOINT71_ONLY" and g["not_DEV_heldout_or_fully_reoptimized_b4"] is True
    else: assert g is None
    return {"checker": "PASS", "production_status": expected, "primal_exact": pv, "dual_exact": dv, "strict_gap": None if gap is None else str(gap), "vertices_checked": 71, "coordinates_checked": 28}

def corruption_guards():
    r = (F(4, 7),)*28; V = (r,)*71; b = list(r)
    for edge, sign in (((0, 1), -1), ((2, 3), -1), ((0, 2), 1), ((1, 3), 1)): b[EDGES.index(edge)] += sign*F(1, 100)
    w = (F(1),)+(F(0),)*27
    assert primal_ok(V, r, (F(1),)+(F(0),)*70) and not primal_ok(V, r, (F(2),)+(F(0),)*70)
    assert dual_ok(V, b, w)[0] and not dual_ok(V[:-1]+(tuple(b),), b, w)[0]
    assert not dual_ok(V, b, tuple(2*x for x in w))[0] and not dual_ok(V, b, (F(0),)*28)[0]

def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--output", type=Path, required=True); a = p.parse_args()
    if a.output.exists(): raise FileExistsError("checker output must be fresh")
    started_cpu, started_wall = time.process_time(), time.monotonic(); corruption_guards()
    result = verify(*(load(ROOT/path, pin) for path, pin in PINS.items()))
    result.update({"inputs": PINS, "python": sys.version, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "method": "direct sum powers at1/4; no production import", "posthoc_not_blind": True, "CPU_seconds": time.process_time()-started_cpu, "wall_seconds": time.monotonic()-started_wall})
    text = json.dumps(result, indent=2, allow_nan=False)+"\n"; assert len(text.encode()) < 1024**2
    a.output.parent.mkdir(parents=True, exist_ok=True); a.output.write_text(text); print(text)

if __name__ == "__main__": main()
