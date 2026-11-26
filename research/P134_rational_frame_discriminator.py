"""P134 CODE ONLY: exact rational-frame physics qualification, no import-time science."""
import argparse
import hashlib
import importlib
from importlib import metadata
from fractions import Fraction as F
from itertools import combinations, permutations
import json
from math import comb, factorial
import os
from pathlib import Path
import resource
import sys
import traceback

CAP, RESERVE, CPU = 16777216, 1048576, 120
OUT = "research/P134_rational_frame_main/run_001/data"
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
STATIC = ("AGENTS.md", "pyproject.toml", "requirements-research-lock.txt",
          "research/P134_rational_frame_discriminator.py", "research/P134_POPULATION.md", "research/P134_contract_TEMPLATE.json",
          "research/P133_RATIONAL_RECEIVER_REFLECTION.md", "research/P134_FIRST_DISCRIMINATOR_DESIGN.md",
          "reports/P133_P134_ROOT_DESIGN_CHECKPOINT.md")
PINS = {"research/P133_RATIONAL_RECEIVER_REFLECTION.md": "56720652d4dbf7c2053ff5599fcfa1bbb1f88e632a3256ee8b9ece5c9735c98d",
        "research/P134_FIRST_DISCRIMINATOR_DESIGN.md": "318244b4cf840efd137671469e1c519fac09321779905276a7125d9ecbc23541",
        "reports/P133_P134_ROOT_DESIGN_CHECKPOINT.md": "540ec8c38e04e925daf94a8932a42c768bc8c115542ee558011efbacf96e9728"}
ROLES = ("python_binary", "pyvenv_cfg", "random_py", "random_native", "nx_metadata", "nx_init", "nx_random_graphs", "nx_graph", "nx_decorators", "nx_misc", "nx_backends")
PROFILE_NAMES = ("0000", "0001", "0010", "0011", "0012", "0100", "0101", "0102", "0110", "0111", "0112", "0120", "0121", "0122", "0123")
EXPECTED = {"provenance": 1, "graph_context": 2, "candidate_cost": 30, "matrix_context": 18,
            "subpermanent_check": 3780, "gram_permanent_check": 270, "cf_comparison": 4050,
            "profile_totals": 270, "four_cycle": 270, "full_pnr": 715, "full_pnr_totals": 1,
            "hand_completion": 2, "grid_envelope": 30, "graph_decision": 2}


def require(test, message):
    if not test:
        raise ValueError(message)


class C:
    """Gaussian rational. No Python complex or scientific binary float arithmetic."""
    __slots__ = ("re", "im")
    def __init__(self, re=0, im=0): self.re, self.im = F(re), F(im)
    def __add__(self, other):
        other = scalar(other); return C(self.re+other.re, self.im+other.im)
    __radd__ = __add__
    def __neg__(self): return C(-self.re, -self.im)
    def __sub__(self, other): return self+-scalar(other)
    def __rsub__(self, other): return scalar(other)+-self
    def __mul__(self, other):
        other = scalar(other)
        return C(self.re*other.re-self.im*other.im, self.re*other.im+self.im*other.re)
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = scalar(other); denominator = other.abs2()
        require(denominator != 0, "zero Gaussian-rational divisor")
        return C((self.re*other.re+self.im*other.im)/denominator,
                 (self.im*other.re-self.re*other.im)/denominator)
    def __eq__(self, other):
        other = scalar(other); return self.re == other.re and self.im == other.im
    def __bool__(self): return bool(self.re or self.im)
    def conjugate(self): return C(self.re, -self.im)
    def abs2(self): return self.re*self.re+self.im*self.im


def scalar(value): return value if isinstance(value, C) else C(value)
def eye(n): return [[C(int(i == j)) for j in range(n)] for i in range(n)]
def dagger(a): return [[a[i][j].conjugate() for i in range(len(a))] for j in range(len(a[0]))]
def block(a, rows, columns): return [[a[i][j] for j in columns] for i in rows]
def matmul(a, b):
    require(a and b and len(a[0]) == len(b), "matrix-product dimensions")
    return [[sum((x*b[l][j] for l, x in enumerate(row)), C()) for j in range(len(b[0]))] for row in a]
def difference(a, b):
    require(len(a) == len(b) and all(len(x) == len(y) for x, y in zip(a, b)), "matrix-difference shape")
    return [[x-y for x, y in zip(row, other)] for row, other in zip(a, b)]
def inverse(a, state):
    n = len(a); require(1 <= n <= 4 and all(len(row) == n for row in a), "inverse size")
    identity = eye(n); work = [list(row)+identity[i] for i, row in enumerate(a)]
    state["inverse_state"] = {"input": a, "augmented_work": work}
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        require(pivot is not None, "singular exact inverse")
        work[j], work[pivot] = work[pivot], work[j]
        diagonal = work[j][j]; work[j] = [x/diagonal for x in work[j]]
        for i in range(n):
            if i != j:
                multiple = work[i][j]
                work[i] = [x-multiple*y for x, y in zip(work[i], work[j])]
    answer = [row[n:] for row in work]
    state["inverse_state"]["answer"] = answer
    require(matmul(a, answer) == identity and matmul(answer, a) == identity, "two-sided inverse")
    return answer


def permanent_dp(a):
    n = len(a); require(n <= 4 and all(len(row) == n for row in a), "DP permanent shape")
    table = {0: C(1)}
    for row in a:
        following = {}
        for mask, value in table.items():
            for j, entry in enumerate(row):
                if not mask & (1 << j):
                    target = mask | (1 << j)
                    following[target] = following.get(target, C())+value*entry
        table = following
    return table[(1 << n)-1]


def permanent_ryser(a):
    n = len(a); require(n <= 4 and all(len(row) == n for row in a), "Ryser permanent shape")
    if n == 0: return C(1)
    answer = C()
    for selected in range(1, 1 << n):
        term = C(1)
        for i in range(n):
            row_sum = C()
            for j in range(n):
                if selected & (1 << j): row_sum = row_sum+a[i][j]
            term = term*row_sum
        answer = answer+((-1)**(n-selected.bit_count()))*term
    return answer


def occupations(total, modes):
    if modes == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in occupations(total-first, modes-1): yield (first,)+rest


def sha(path):
    with path.open("rb") as stream: return hashlib.file_digest(stream, "sha256").hexdigest()
def load(path): return json.loads(path.read_text(encoding="ascii"), parse_float=F)
def hex_digest(value): return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)
def local_file(root, name):
    p = Path(name)
    require(p.parts and not p.is_absolute() and p.as_posix() == name and all(x not in (".", "..") for x in p.parts), "canonical local input")
    cursor = root
    for part in p.parts:
        cursor /= part; require(not cursor.is_symlink(), "symlinked local input")
    require(cursor.is_file(), "nonregular/missing local input")
    return cursor
def external_file(name):
    p = Path(name)
    require(p.is_absolute() and p.resolve() == p and p.is_file(), "canonical regular external input")
    return p
def inspect_descriptor(row, path, state=None):
    observed = {"path": row["path"], "expected_sha256": row["sha256"], "observed_sha256": sha(path),
                "expected_bytes": row["bytes"], "observed_bytes": path.stat().st_size}
    if state is not None: state["input_check"] = observed
    require(type(row["bytes"]) is int and hex_digest(row["sha256"]) and
            observed["expected_sha256"] == observed["observed_sha256"] and observed["expected_bytes"] == observed["observed_bytes"], "bound hash/byte mismatch: "+row["path"])
    return observed
def authorize(root, name):
    b = load(local_file(root, name))
    require(b["binding_state"] == "ROOT_AUTHORIZED" and b["run_authorized"] is True, "separate ROOT authority")
    rows = b["artifacts"]; table = {row["path"]: row for row in rows}
    require(len(table) == len(rows) and name not in table and set(STATIC) <= set(table), "static binding closure")
    require(all((p.startswith("research/") or p.startswith("reports/")) and p.endswith((".md", ".json")) for p in set(table)-set(STATIC)), "only extra frozen review metadata")
    require(len(b["execution_artifacts"]) == len(table)+1 and set(b["execution_artifacts"]) == set(table)|{name}, "binding self-input closure")
    before = [inspect_descriptor(row, local_file(root, row["path"])) for row in rows]
    require(all(table[p]["sha256"] == value for p, value in PINS.items()), "original design/checkpoint bytes")
    require(sha(Path(__file__)) == b["source_sha256"] == table[STATIC[3]]["sha256"], "source binding")
    ext = b["external_artifacts"]; roles = {row["role"]: row for row in ext}
    require(len(ext) == len(roles) and set(roles) == set(ROLES) and len({row["path"] for row in ext}) == len(ext), "exact external roles")
    external_before = [inspect_descriptor(row, external_file(row["path"])) for row in ext]
    require(external_file(roles["python_binary"]["path"]) == Path(sys.executable).resolve(), "actual interpreter")
    require(external_file(roles["pyvenv_cfg"]["path"]) == (Path(sys.prefix)/"pyvenv.cfg").resolve(), "actual persistent venv")
    require(external_file(roles["nx_init"]["path"]).name == "__init__.py" and external_file(roles["nx_init"]["path"]).parent.name == "networkx", "NetworkX package root")
    return b, roles, {"project": before, "external": external_before}


def software_after_authority(roles):
    """Called only after every project/external hash and authority check."""
    distribution = metadata.distribution("networkx")
    require(distribution.version == "3.6.1" and (Path(distribution._path)/"METADATA").resolve() == Path(roles["nx_metadata"]["path"]), "actual pinned NetworkX metadata before import")
    require(Path(distribution.locate_file("networkx/__init__.py")).resolve() == Path(roles["nx_init"]["path"]), "declared package root before import")
    import random
    import networkx as nx
    modules = {"random_py": random, "random_native": importlib.import_module("_random"), "nx_init": nx,
               "nx_random_graphs": importlib.import_module("networkx.generators.random_graphs"),
               "nx_graph": importlib.import_module("networkx.classes.graph"),
               "nx_decorators": importlib.import_module("networkx.utils.decorators"),
               "nx_misc": importlib.import_module("networkx.utils.misc"),
               "nx_backends": importlib.import_module("networkx.utils.backends")}
    require(nx.__version__ == metadata.version("networkx") == "3.6.1", "pinned NetworkX")
    require(all(not getattr(nx.config.backend_priority, key) for key in ("algos", "generators", "classes")), "default core NetworkX backend priorities only")
    for role, module in modules.items():
        require(Path(module.__file__).resolve() == Path(roles[role]["path"]), "actual loaded module path")
    require((Path(distribution._path)/"METADATA").resolve() == Path(roles["nx_metadata"]["path"]), "actual NetworkX metadata")
    return random, nx


def encode(value):
    if isinstance(value, C): return [str(value.re), str(value.im)]
    if isinstance(value, F): return str(value)
    raise TypeError(type(value).__name__)
class Evidence:
    def __init__(self, path):
        require(path.parent.is_dir() and not path.parent.is_symlink() and not path.parent.parent.is_symlink() and not path.exists() and not path.is_symlink(), "fresh exclusive data child")
        path.mkdir(); self.path, self.bytes, self.rows = path, 0, 0
        self.counts = {key: 0 for key in EXPECTED}; self.stream = (path/"records.jsonl").open("x", encoding="ascii")
    def emit(self, row):
        require(row["kind"] in self.counts, "registered record kind")
        text = json.dumps(row, default=encode, sort_keys=True, allow_nan=False, separators=(",", ":"))+"\n"
        size = len(text.encode("ascii")); require(self.bytes+size <= CAP-RESERVE, "15MiB record cap/final reserve")
        self.stream.write(text); self.stream.flush()
        self.bytes += size; self.rows += 1; self.counts[row["kind"]] += 1
    def finish(self, summary, failure):
        self.stream.close()
        payloads = [json.dumps(x, default=encode, sort_keys=True, allow_nan=False)+"\n" for x in (summary, failure)]
        size = sum(len(x.encode("ascii")) for x in payloads)
        require(size <= RESERVE and self.bytes+size <= CAP, "combined final/science cap")
        for name, payload in zip(("summary.json", "failure.json"), payloads):
            with (self.path/name).open("x", encoding="ascii") as stream: stream.write(payload)


def registered():
    paths = tuple(permutations(range(4))); cycles = []
    for p in paths:
        seen, index = set(), 0
        while index not in seen: seen.add(index); index = p[index]
        if len(seen) == 4 and index == 0: cycles.append(p)
    require(len(paths) == 24 and len(cycles) == 6 and len(set(PROFILE_NAMES)) == 15, "permutation/profile population")
    profiles = {}
    for name in PROFILE_NAMES:
        colors = tuple(map(int, name))
        require(colors[0] == 0 and all(colors[j] <= 1+max(colors[:j]) for j in range(1, 4)), "restricted-growth profile")
        profiles[name] = tuple(tuple(i for i, color in enumerate(colors) if color == c) for c in range(max(colors)+1))
        if name != "0000":
            require(all(any(colors[t[i]] != colors[i] for i in range(4)) for t in cycles), "four-cycles absent in every proper profile")
    grid = tuple((F(beta), F(kappa)) for beta in ("0", "1/2") for kappa in ("0", "1/2", "1", "2"))
    return paths, tuple(cycles), profiles, grid, tuple(combinations(range(6), 4))


def edge_cut(weights, selected, state):
    state["edge_cut_calls"] += 1; selected = set(selected)
    return sum(weights[i][j] for i in range(24) for j in range(i+1, 24) if (i in selected) != (j in selected))
def graph_context(index, random, nx, writer, state):
    topology_seed, weight_seed, mark_seed = 1341001+index, 1342001+index, 1343001+index
    name = ("ER" if index == 0 else "RR")+str(topology_seed)
    state.update(phase="registered graph factory", case=name)
    graph = nx.gnp_random_graph(24, 0.4, seed=topology_seed, backend="networkx") if index == 0 else nx.random_regular_graph(4, 24, seed=topology_seed, backend="networkx")
    require(type(graph) is nx.Graph and set(graph) == set(range(24)) and not graph.is_directed() and not list(nx.selfloop_edges(graph)), "literal topology model")
    if index == 1: require(all(graph.degree(v) == 4 for v in range(24)), "RR degree")
    weight_rng, mark_rng = random.Random(weight_seed), random.Random(mark_seed)
    weights = [[0]*24 for unused in range(24)]; edges = []
    for i, j in sorted((min(i, j), max(i, j)) for i, j in graph.edges()):
        value = weight_rng.randint(1, 5); weights[i][j] = weights[j][i] = value; edges.append((i, j, value))
    marks = list(range(24)); mark_rng.shuffle(marks)
    source = tuple(marks[:12]); removed = tuple(source[:4]); outside = tuple(marks[12:])
    pool = tuple(outside[:6]); prototypes = pool[:4]; base = tuple(i for i in source if i not in removed)
    require(len(base) == 8 and len(set(base)|set(pool)) == 14, "disjoint imbalanced helper/pool")
    d = [sum(weights[j][h] for h in range(24) if h not in base and h != j)-sum(weights[j][h] for h in base) for j in pool]
    scale = 1+max(map(abs, d))+sum(weights[i][j] for a, i in enumerate(pool) for j in pool[a+1:])
    current, baseline = edge_cut(weights, source, state), edge_cut(weights, base, state)
    ctx = {"id": name, "weights": weights, "marks": marks, "S": source, "R": removed, "S0": base,
           "B": pool, "prototypes": prototypes, "d": d, "W": scale, "current_cost": current, "baseline_cost": baseline}
    writer.emit({"kind": "graph_context", "case": name, "family": "gnp_random_graph(24,0.4)" if index == 0 else "random_regular_graph(4,24)",
                 "seeds": {"topology": topology_seed, "weights": weight_seed, "marks": mark_seed}, "factory_backend": "networkx", "weighted_edges": edges,
                 "marks": marks, "S": source, "R": removed, "S0": base, "S0_feasible_candidate": False,
                 "B": pool, "prototypes": prototypes, "d": d, "W": scale, "current_cost": current, "baseline_helper_cost": baseline})
    scores = {}
    for y in combinations(range(6), 4):
        lifted = tuple(sorted(set(base)|{pool[j] for j in y})); require(len(lifted) == 12, "balanced lifted candidate")
        incremental = baseline+sum(d[j] for j in y)-2*sum(weights[pool[j]][pool[h]] for j, h in combinations(y, 2))
        whole = edge_cut(weights, lifted, state); state["incremental_cost_calls"] += 1
        utility = max(0, current-whole); scores[y] = {"cost": whole, "h": utility}
        writer.emit({"kind": "candidate_cost", "case": name, "Y": y, "vertices": [pool[j] for j in y], "lifted": lifted,
                     "incremental_cost": incremental, "whole_cut": whole, "current_cost": current, "h": utility,
                     "match": incremental == whole, "prototype": y == (0, 1, 2, 3), "credit_all_controls": True})
        require(incremental == whole, "independent whole-cut/formula comparison")
    ctx["scores"] = scores
    return ctx


def build_frame(ctx, beta, kappa):
    pool, p, weights, d, scale = ctx["B"], ctx["prototypes"], ctx["weights"], ctx["d"], ctx["W"]
    return [[C(F(int(j == p[a]))*(1-beta*F(d[row], scale)), kappa*F(weights[j][p[a]], scale)) for a in range(4)] for row, j in enumerate(pool)]
def hand_frame(name):
    f = [[C(int(i == j)) for j in range(4)] for i in range(6)]
    if name == "H_HOM":
        f[0][1] = C(0, 1); f[1][0] = C(0, 1)
    return f
def construct(f, state):
    state["matrix_operands"] = {"F": f}
    identity = eye(4); h = matmul(dagger(f), f); state["matrix_operands"]["H"] = h
    q = inverse([[identity[i][j]+h[i][j] for j in range(4)] for i in range(4)], state)
    t = [[2*x for x in row] for row in matmul(f, q)]; d = matmul(difference(identity, h), q)
    v = [list(row) for row in f]+[[-x for x in row] for row in identity]
    projection = matmul(matmul(v, q), dagger(v)); u = difference(eye(10), [[2*x for x in row] for row in projection])
    g, dump_gram = matmul(dagger(t), t), matmul(dagger(d), d)
    state["matrix_operands"].update(Q=q, T=t, D=d, U=u, G=g, dump_Gram=dump_gram)
    checks = {"Hermitian": u == dagger(u), "unitarity": matmul(dagger(u), u) == eye(10),
              "occupied_columns": block(u, range(6), range(6, 10)) == t and block(u, range(6, 10), range(6, 10)) == [[-x for x in row] for row in d],
              "occupied_Gram": [[g[i][j]+dump_gram[i][j] for j in range(4)] for i in range(4)] == identity}
    return h, q, t, d, u, g, checks


def convolution(y, groups, cache):
    """Disjoint output-set allocation among independent species, no path buckets."""
    def assign(index, remaining):
        if index == len(groups): return F(int(not remaining))
        source = groups[index]; total = F(0)
        for received in combinations(remaining, len(source)):
            rest = tuple(j for j in remaining if j not in received)
            total += cache[received, source].abs2()*assign(index+1, rest)
        return total
    return assign(0, y)
def path_buckets(amplitudes, profile, paths):
    """Independent labeled-path/color expansion, not group-convolution calls."""
    bins = {}
    for p in paths:
        key = tuple(profile[p[j]] for j in range(4))
        bins[key] = bins.get(key, C())+amplitudes[p]
    return sum((value.abs2() for value in bins.values()), F(0))
def cycle_coefficients(amplitudes, paths, cycles):
    values = []
    for tau in cycles:
        coefficient = C()
        for rho in paths:
            sigma = tuple(tau[rho[j]] for j in range(4))
            coefficient = coefficient+amplitudes[sigma]*amplitudes[rho].conjugate()
        values.append(coefficient)
    return values, sum(values, C())


def evaluate_context(name, f, graph, beta, kappa, writer, state, paths, cycles, profiles, targets):
    state.update(phase="matrix context", context=name); h, q, t, d, u, g, checks = construct(f, state)
    writer.emit({"kind": "matrix_context", "context": name, "case": graph["id"] if graph else None, "beta": beta, "kappa": kappa,
                 "F": f, "H": h, "Q": q, "T": t, "D": d, "U": u, "G": g, "input": [6, 7, 8, 9],
                 "checks": checks, "permutation_order": paths, "four_cycles": cycles})
    require(all(checks.values()), "exact full reflection/occupied-column invariants")
    state.pop("matrix_operands", None); state.pop("inverse_state", None)
    cache, gram = {}, {}
    for size in range(5):
        for source in combinations(range(4), size):
            for received in combinations(range(6), size):
                state.update(phase="DP/Ryser subpermanents", source=source, received=received)
                sub = block(t, received, source); dp, ryser = permanent_dp(sub), permanent_ryser(sub)
                writer.emit({"kind": "subpermanent_check", "context": name, "source": source, "received": received, "DP": dp, "Ryser": ryser, "match": dp == ryser})
                require(dp == ryser, "independent subpermanent disagreement"); cache[received, source] = dp
            if size:
                state.update(phase="DP/Ryser Gram permanents", source=source)
                dp, ryser = permanent_dp(block(g, source, source)), permanent_ryser(block(g, source, source))
                writer.emit({"kind": "gram_permanent_check", "context": name, "source": source, "DP": dp, "Ryser": ryser, "match": dp == ryser})
                require(dp == ryser and dp.im == 0 and dp.re >= 0, "real nonnegative principal Gram permanent")
                gram[source] = dp.re
    require(len(cache) == 210 and len(gram) == 15, "complete subset caches")
    totals = {profile: {"cf": F(0), "I": F(0), "hazard": F(0)} for profile in profiles}; j4 = F(0); c4_values = {}; b_probabilities = {}
    for y in targets:
        state.update(phase="CF path/cycle/profiles", Y=y)
        amplitudes = {}
        for p in paths:
            term = C(1)
            for row, column in zip(y, p): term = term*t[row][column]
            amplitudes[p] = term
        cycle_values, c4_gaussian = cycle_coefficients(amplitudes, paths, cycles); c4 = c4_gaussian.re; c4_values[y] = c4
        utility = graph["scores"][y]["h"] if graph else None
        writer.emit({"kind": "four_cycle", "context": name, "Y": y, "path_amplitudes": [amplitudes[p] for p in paths],
                     "cycle_coefficients": cycle_values, "C4_Gaussian": c4_gaussian, "real_check": c4_gaussian.im == 0,
                     "C4": c4, "h": utility, "utility_contribution": utility*c4 if graph else None})
        require(c4_gaussian.im == 0, "real signed four-cycle sum")
        if graph: j4 += utility*c4
        if not graph: require(c4 == 0, "hand has no connected four-cycle")
        for profile, groups in profiles.items():
            p_conv = convolution(y, groups, cache); p_bucket = path_buckets(amplitudes, profile, paths)
            expected_hand = None
            if not graph:
                expected_hand = F(int(y == (0, 1, 2, 3))) if name == "H_ID" else (F(32, 81) if profile[0] != profile[1] and y == (0, 1, 2, 3) else F(0))
            match = p_conv == p_bucket and (expected_hand is None or p_conv == expected_hand)
            writer.emit({"kind": "cf_comparison", "context": name, "profile": profile, "Y": y, "convolution": p_conv,
                         "path_bucket": p_bucket, "expected_hand": expected_hand, "match": match, "h": utility})
            require(match and p_conv >= 0, "CF profile/independent path comparison")
            totals[profile]["cf"] += p_conv
            if graph:
                totals[profile]["I"] += utility*p_conv
                if utility > 0: totals[profile]["hazard"] += p_conv
            if profile == "0000": b_probabilities[y] = p_conv
    for profile, groups in profiles.items():
        state.update(phase="profile normalization", profile=profile)
        all_signal = F(1)
        for group in groups: all_signal *= gram[group]
        cf = totals[profile]["cf"]; collision, dump = all_signal-cf, 1-all_signal
        writer.emit({"kind": "profile_totals", "context": name, "profile": profile, "all_signal": all_signal, "CF": cf,
                     "SIGNAL_COLLISION": collision, "DUMP": dump, "total": cf+collision+dump,
                     "I": totals[profile]["I"] if graph else None, "hazard": totals[profile]["hazard"] if graph else None,
                     "J4": j4 if graph and profile == "0000" else (F(0) if graph else None)})
        require(min(cf, collision, dump) >= 0 and cf+collision+dump == 1, "raw CF/collision/dump normalization")
        totals[profile].update(all_signal=all_signal, collision=collision, dump=dump)
        if not graph:
            expected_signal = F(1) if name == "H_ID" else F(64, 81)
            require(all_signal == expected_signal and dump == 1-expected_signal, "hand signal/dump masses")
        elif kappa == 0:
            require(all(b_probabilities[y] == 0 for y in targets if y != (0, 1, 2, 3)) and collision == 0 and cf == totals["0000"]["cf"], "known prototype-only endpoint in all groups")
    result = {"context": name, "beta": beta, "kappa": kappa, "profiles": totals, "J4": j4, "b_cf": b_probabilities, "U": u}
    if not graph:
        writer.emit({"kind": "hand_completion", "context": name, "passed": True, "profiles": list(profiles), "four_cycles_zero": True})
    return result


def full_normalization(result, writer, state):
    state["phase"] = "full715 physical PNR"; u = result["U"]
    masses = {"CF": F(0), "SIGNAL_COLLISION": F(0), "DUMP": F(0)}; visited = 0
    for n in occupations(4, 10):
        state["occupation"] = n; rows = [j for j, count in enumerate(n) for unused in range(count)]
        amplitude = permanent_dp(block(u, rows, range(6, 10))); divisor = 1
        for count in n: divisor *= factorial(count)
        probability = amplitude.abs2()/divisor
        if any(n[6:]): label, y = "DUMP", None
        elif all(count <= 1 for count in n[:6]): label, y = "CF", tuple(j for j, count in enumerate(n[:6]) if count)
        else: label, y = "SIGNAL_COLLISION", None
        expected_cf = result["b_cf"][y] if label == "CF" else None
        writer.emit({"kind": "full_pnr", "context": result["context"], "occupation": n, "amplitude": amplitude,
                     "occupation_factorial": divisor, "p": probability, "classification": label, "expected_CF": expected_cf})
        require(probability >= 0 and (expected_cf is None or probability == expected_cf), "full-U/receiver CF identity")
        masses[label] += probability; visited += 1
    expected = result["profiles"]["0000"]
    match = (visited == 715 and sum(masses.values()) == 1 and masses["CF"] == expected["cf"] and
             masses["SIGNAL_COLLISION"] == expected["collision"] and masses["DUMP"] == expected["dump"])
    writer.emit({"kind": "full_pnr_totals", "context": result["context"], "bins": visited, "masses": masses, "total": sum(masses.values()), "match": match})
    require(match, "all715 full-PNR and disjoint coarse normalization")


def envelopes(graph, runs, profiles, writer, state):
    state.update(phase="independent grid envelopes", case=graph["id"]); best = {}
    for profile in profiles:
        index = max(range(len(runs)), key=lambda i: runs[i]["profiles"][profile]["I"])
        run, outcome = runs[index], runs[index]["profiles"][profile]
        best[profile] = {"grid_index": index, "I": outcome["I"], "hazard": outcome["hazard"], "J4": run["J4"] if profile == "0000" else F(0)}
        writer.emit({"kind": "grid_envelope", "case": graph["id"], "profile": profile,
                     "all_I": [r["profiles"][profile]["I"] for r in runs], "selected_grid_index": index,
                     "beta": run["beta"], "kappa": run["kappa"], **best[profile]})
    proper = max(best[p]["I"] for p in profiles if p != "0000"); b = best["0000"]
    frontier = max(row["h"] for row in graph["scores"].values()); prototype = graph["scores"][(0, 1, 2, 3)]["h"]
    require(all(value["I"] <= frontier and value["I"] >= prototype for value in best.values()), "credited frontier/prototype envelope")
    decision = {"case": graph["id"], "B": b, "proper_envelope": proper, "strict_grid": b["I"] > proper,
                "selected_J4_positive": b["J4"] > 0, "frontier_h": frontier, "prototype_h": prototype,
                "no_improving_candidate": frontier == 0, "frontier_fully_credited": True, "optimizer_advantage": False}
    writer.emit({"kind": "graph_decision", **decision}); return decision


def main():
    resource.setrlimit(resource.RLIMIT_FSIZE, (CAP, CAP)); resource.setrlimit(resource.RLIMIT_CPU, (CPU, CPU))
    parser = argparse.ArgumentParser(); parser.add_argument("--binding", required=True); args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15) and all(os.environ.get(key) == "1" for key in THREADS), "CPython/thread profile")
    binding, roles, before = authorize(root, args.binding); binding_sha = sha(local_file(root, args.binding))
    writer = Evidence(root/OUT); state = {"phase": "authorized setup", "edge_cut_calls": 0, "incremental_cost_calls": 0}
    failure, decisions, completed, attempted, after = None, [], [], [], None
    plan = ["setup", "graphs/costs", "H_ID", "H_HOM"]
    for prefix in ("ER1341001", "RR1341002"):
        for i in range(8):
            plan.append(prefix+"/g"+str(i))
            if prefix == "ER1341001" and i == 6: plan.append("full715")
    plan += ["envelopes/ER1341001", "envelopes/RR1341002", "final_population", "final_integrity"]
    def start(task):
        require(task in plan and task not in attempted, "unique registered task")
        state["task"] = task; attempted.append(task)
    try:
        start("setup")
        random, nx = software_after_authority(roles)
        paths, cycles, profiles, grid, targets = registered()
        writer.emit({"kind": "provenance", "source_sha256": binding["source_sha256"], "binding": args.binding, "binding_sha256": binding_sha,
                     "before": before, "Python": sys.version, "networkx": nx.__version__, "environment": {key: os.environ.get(key) for key in THREADS},
                     "factory_backend": "networkx", "backend_priorities": {key: list(getattr(nx.config.backend_priority, key)) for key in ("algos", "generators", "classes")},
                     "profiles": PROFILE_NAMES, "grid": grid, "CPU": CPU, "wall_ROOT": 180, "science_cap": CAP, "record_cap": CAP-RESERVE,
                     "final_reserve": RESERVE, "photon_RNG_draws": 0, "native_calls": 0, "optimizer_advantage": False})
        completed.append("setup"); start("graphs/costs")
        graphs = [graph_context(i, random, nx, writer, state) for i in range(2)]; completed.append("graphs/costs")
        for name in ("H_ID", "H_HOM"):
            start(name)
            evaluate_context(name, hand_frame(name), None, None, None, writer, state, paths, cycles, profiles, targets); completed.append(name)
        runs_by_case = {}
        for graph in graphs:
            runs = []
            for index, (beta, kappa) in enumerate(grid):
                name = graph["id"]+"/g"+str(index)
                start(name)
                result = evaluate_context(name, build_frame(graph, beta, kappa), graph, beta, kappa, writer, state, paths, cycles, profiles, targets)
                runs.append(result); completed.append(name)
                if graph["id"] == "ER1341001" and beta == F(1, 2) and kappa == 1:
                    start("full715")
                    full_normalization(result, writer, state); completed.append("full715")
            runs_by_case[graph["id"]] = runs
        for graph in graphs:
            task = "envelopes/"+graph["id"]; start(task)
            decisions.append(envelopes(graph, runs_by_case[graph["id"]], profiles, writer, state)); completed.append(task)
        start("final_population")
        require(writer.counts == EXPECTED and writer.rows == 9441 and state["edge_cut_calls"] == 34 and state["incremental_cost_calls"] == 30 and len(completed) == 23, "complete fixed population/cost ledger")
        completed.append("final_population"); start("final_integrity")
        state["phase"] = "final input integrity"
        after = {"project": [inspect_descriptor(row, local_file(root, row["path"]), state) for row in binding["artifacts"]],
                 "external": [inspect_descriptor(row, external_file(row["path"]), state) for row in binding["external_artifacts"]]}
        require(sha(local_file(root, args.binding)) == binding_sha, "active binding changed")
        completed.append("final_integrity"); require(len(plan) == len(completed) == 25 and set(completed) == set(plan), "all registered tasks complete")
    except Exception as exc:
        failure = {"state": state, "exception": repr(exc), "traceback": traceback.format_exc()}
    if failure:
        signal = "NOT_ACCEPTED_ENGINE_FAILURE"
    elif not all(d["strict_grid"] for d in decisions): signal = "NO_STRICT_GRID_SIGNAL"
    elif not all(d["selected_J4_positive"] for d in decisions): signal = "GRID_SIGNAL_NOT_POSITIVE_4CYCLE"
    else: signal = "GRID_4CYCLE_FOLLOWUP_ONLY"
    writer.finish({"status": "INCONCLUSIVE_FIRST_FAILURE" if failure else "EXACT_GRID_ENGINE_PASS", "signal_status": signal,
                   "counts": writer.counts, "records": writer.rows, "edge_cut_calls": state["edge_cut_calls"], "incremental_cost_calls": state["incremental_cost_calls"],
                   "completed": completed, "task_plan": plan, "FAILED_TASK": [task for task in attempted if task not in completed],
                   "NOT_RUN": [task for task in plan if task not in attempted],
                   "decisions": decisions, "after": after, "registered_graph_MT_streams": 6, "photon_RNG_draws": 0, "native_calls": 0, "FPRAS_calls": 0,
                   "positive_accepted": False, "optimizer_advantage": False, "practical_speed_advantage": False, "sampler_claim": False}, failure)
    if failure: raise SystemExit(1)


if __name__ == "__main__": main()
