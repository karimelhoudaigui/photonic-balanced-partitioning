"""P141 CODE ONLY; derived from frozen P134 c443389, not independent replication.

No graph, registration, matrix or RNG is evaluated at import time. Separate
ROOT authority, complete hashes and environment checks precede random/NetworkX.
"""
import argparse
import hashlib
import importlib
from fractions import Fraction as F
from itertools import combinations, permutations
import json
from math import factorial, lcm
import os
from pathlib import Path
import resource
import shutil
import sys
import traceback

CAP, RESERVE, CPU = 50331648, 1048576, 180
OUT = "research/P141_finite_magnetic_main/run_001/data"
BINDING = "research/P141_execution_binding.json"
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
STATIC = ("AGENTS.md", "pyproject.toml", "requirements-research-lock.txt",
          "research/P141_finite_magnetic_screen.py", "research/P141_POPULATION.md", "research/P141_contract_TEMPLATE.json",
          "research/P133_RATIONAL_RECEIVER_REFLECTION.md", "research/P134_rational_frame_discriminator.py",
          "research/P138_INCUMBENT_MAGNETIC_RECEIVER_ROUTE.md", "research/P141_FINITE_MAGNETIC_SCREEN_CARD.md",
          "research/P141_INDEPENDENT_CARD_REVIEW.md", "reports/P141_ROOT_CODE_ONLY_AUTHORIZATION.md")
PINS = {"research/P133_RATIONAL_RECEIVER_REFLECTION.md": "56720652d4dbf7c2053ff5599fcfa1bbb1f88e632a3256ee8b9ece5c9735c98d",
        "research/P134_rational_frame_discriminator.py": "0f9dce56cecac9d7701953577adce1d5bf0c6cc2807083eca45c3ba47f1856f3",
        "research/P138_INCUMBENT_MAGNETIC_RECEIVER_ROUTE.md": "b40d8491906aa772e0662b22dcc97d60d1439df06b8ec1bd8b79fcd43acc7460",
        "research/P141_FINITE_MAGNETIC_SCREEN_CARD.md": "4daa33822164d1298202b5a15e0dd86a5ec68abc626606f5a292fa62936033cd",
        "research/P141_INDEPENDENT_CARD_REVIEW.md": "1a1750d4b26d48c6c4464a51cd8982158e88c181c04d483e471ef5846bf3957d",
        "reports/P141_ROOT_CODE_ONLY_AUTHORIZATION.md": "82a57ccb6062c3a0b280c6fa858ff5d0c4a4325af27364d996b93330faca8274"}
ROLES = ("python_binary", "pyvenv_cfg", "random_py", "random_native", "nx_metadata", "nx_init", "nx_random_graphs", "nx_graph", "nx_decorators", "nx_misc", "nx_backends")
PROFILE_NAMES = ("0000", "0001", "0010", "0011", "0012", "0100", "0101", "0102", "0110", "0111", "0112", "0120", "0121", "0122", "0123")
EXPECTED = {"provenance": 1, "graph_context": 2, "field_check": 16, "candidate_cost": 140,
            "generator_context": 8, "matrix_context": 36, "subpermanent_check": 17820,
            "gram_permanent_check": 540, "cf_comparison": 37800, "profile_totals": 540,
            "selected_four_cycle": 140, "full_pnr": 1365, "full_pnr_totals": 1,
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
    require(name == BINDING, "registered active-binding path")
    binding_path = local_file(root, name); binding_sha = sha(binding_path); b = load(binding_path)
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
    require(sha(binding_path) == binding_sha, "binding changed during authorization")
    return b, roles, {"project": before, "external": external_before}, binding_sha


def software_after_authority(roles):
    """Called only after every project/external hash and authority check."""
    from importlib import metadata
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
        size = len(text.encode("ascii")); require(self.bytes+size <= CAP-RESERVE, "47MiB record cap/final reserve")
        self.stream.write(text); self.stream.flush()
        self.bytes += size; self.rows += 1; self.counts[row["kind"]] += 1
    def finish(self, summary, failure):
        self.stream.close()
        payloads = [json.dumps(x, default=encode, sort_keys=True, allow_nan=False)+"\n" for x in (summary, failure)]
        size = sum(len(x.encode("ascii")) for x in payloads)
        require(size <= RESERVE and self.bytes+size <= CAP, "combined final/science cap")
        for name, payload in zip(("summary.json", "failure.json"), payloads):
            with (self.path/name).open("x", encoding="ascii") as stream: stream.write(payload)


def integer_text(value):
    value = F(value); require(value.denominator == 1, "noninteger in declared numerator domain")
    return str(value.numerator)
def complex_integer(value): return [integer_text(value.re), integer_text(value.im)]
def integer_matrix(a): return [[complex_integer(x) for x in row] for row in a]
def scale_matrix(a, factor): return [[x*factor for x in row] for row in a]
def common_denominator(*matrices):
    answer = 1
    for a in matrices:
        for row in a:
            for x in row: answer = lcm(answer, x.re.denominator, x.im.denominator)
    return answer
def source_support(f):
    """Actual F bipartite components, including unused receiver rows separately."""
    unseen, components = set(range(4)), []
    while unseen:
        sources, received = {min(unseen)}, set()
        while True:
            rows = {j for j in range(8) if any(f[j][a] for a in sources)}
            following = {a for a in range(4) if any(f[j][a] for j in rows)}
            if following == sources and rows == received: break
            sources, received = following, rows
        require(sources, "unsupported source column")
        unseen -= sources; components.append({"sources": sorted(sources), "receivers": sorted(received)})
    return {"source_components": components, "vacuum_receiver_isolates": [j for j in range(8) if not any(f[j])],
            "proper_component_profile_exists": len(components) > 1}


def registered():
    paths = tuple(permutations(range(4))); cycles = []
    for p in paths:
        seen, index = set(), 0
        while index not in seen: seen.add(index); index = p[index]
        if len(seen) == 4 and index == 0: cycles.append(p)
    require(len(paths) == 24 and len(cycles) == 6 and len(set(PROFILE_NAMES)) == 15, "path/profile population")
    profiles = {}
    for name in PROFILE_NAMES:
        colors = tuple(map(int, name))
        require(colors[0] == 0 and all(colors[j] <= 1+max(colors[:j]) for j in range(1, 4)), "restricted-growth profile")
        profiles[name] = tuple(tuple(i for i, color in enumerate(colors) if color == c) for c in range(max(colors)+1))
        if name != "0000": require(all(any(colors[t[i]] != colors[i] for i in range(4)) for t in cycles), "proper profile/four-cycle")
    grid = ((0, "1", F(0)),)+tuple((alpha, rho, F(k)) for alpha in (0, 1) for rho in ("1", "i") for k in ("1/2", "1", "2", "4"))
    return paths, tuple(cycles), profiles, grid, tuple(combinations(range(8), 4))


def edge_cut(weights, selected, state):
    state["edge_cut_calls"] += 1; selected = set(selected)
    return sum(weights[i][j] for i in range(24) for j in range(i+1, 24) if (i in selected) != (j in selected))
def graph_context(index, random, nx, writer, state):
    seeds = (1411001+index, 1412001+index, 1413001+index)
    name = ("ER" if index == 0 else "RR")+str(seeds[0]); state.update(phase="registered graph factory", case=name)
    graph = nx.gnp_random_graph(24, 0.4, seed=seeds[0], backend="networkx") if index == 0 else nx.random_regular_graph(4, 24, seed=seeds[0], backend="networkx")
    state["factory_snapshot"] = {"nodes": list(graph), "edges": list(graph.edges())}
    require(type(graph) is nx.Graph and set(graph) == set(range(24)) and not graph.is_directed() and not list(nx.selfloop_edges(graph)), "literal topology")
    if index == 1: require(all(graph.degree(v) == 4 for v in range(24)), "RR degree")
    weight_rng, mark_rng = random.Random(seeds[1]), random.Random(seeds[2])
    weights = [[0]*24 for unused in range(24)]; edges = []
    for i, j in sorted((min(i, j), max(i, j)) for i, j in graph.edges()):
        value = weight_rng.randint(1, 5); weights[i][j] = weights[j][i] = value; edges.append((i, j, value))
    marks = list(range(24)); mark_rng.shuffle(marks); ranks = {v: j for j, v in enumerate(marks)}
    source, removed = tuple(marks[:12]), tuple(marks[:4]); base = tuple(marks[4:12]); pool = removed+tuple(marks[12:16])
    require(len(set(base)|set(pool)) == 16 and len(base) == len(pool) == 8, "disjoint helper/receiver pool")
    current, baseline = edge_cut(weights, source, state), edge_cut(weights, base, state)
    writer.emit({"kind": "graph_context", "case": name, "seeds": seeds, "factory_backend": "networkx", "weighted_edges": edges,
                 "marks": marks, "S": source, "R": removed, "S0": base, "S0_feasible_candidate": False,
                 "B_pool": pool, "prototypes": removed, "current_cost": current, "baseline_helper_cost": baseline})
    state.pop("factory_snapshot", None); fields = []
    for j in pool:
        value = sum(weights[j][v] for v in range(24) if v not in base and v != j)-sum(weights[j][v] for v in base)
        helper = edge_cut(weights, base+(j,), state); state["field_checks"] += 1
        writer.emit({"kind": "field_check", "case": name, "vertex": j, "S0_plus_j_feasible": False,
                     "edge_sum_field": value, "helper_cut": helper, "baseline_helper_cut": baseline, "delta": value-(helper-baseline)})
        require(value == helper-baseline and abs(value) <= 75, "independent field identity/bound"); fields.append(value)
    twohop = [[0]*8 for unused in range(8)]
    for j, h in combinations(range(8), 2):
        value = sum(weights[pool[j]][v]*weights[v][pool[h]] for v in range(24))
        twohop[j][h] = twohop[h][j] = value
        state["two_hop_pair_sums"] += 1; state["two_hop_products"] += 24
    generators = {}
    for alpha in (0, 1):
        b = [[weights[pool[j]][pool[h]]+alpha*twohop[j][h] if j != h else 0 for h in range(8)] for j in range(8)]
        row_bounds = [abs(fields[j])+sum(b[j]) for j in range(8)]; nu = max(1, *row_bounds)
        omega = [[(ranks[pool[h]] > ranks[pool[j]])-(ranks[pool[h]] < ranks[pool[j]]) for h in range(8)] for j in range(8)]
        for rho in ("1", "i"):
            ell = [[C(fields[j]) if j == h else C(b[j][h])*(C(1) if rho == "1" else C(0, omega[j][h])) for h in range(8)] for j in range(8)]
            hamiltonian = [[x/nu for x in row] for row in ell]; selected = block(hamiltonian, range(8), range(4))
            a = matmul(dagger(selected), selected)
            checks = {"Hermitian": ell == dagger(ell), "row_norm_certificate": all(x <= nu for x in row_bounds),
                      "integer_bounds": nu <= 3960 and max(map(max, twohop)) <= 550 and max(map(max, b)) <= 555}
            writer.emit({"kind": "generator_context", "case": name, "alpha": alpha, "rho": rho, "d": fields, "two_hop": twohop,
                         "b": b, "Omega": omega, "L": ell, "nu": nu, "row_bounds": row_bounds, "H": hamiltonian,
                         "source_H2": a, "checks": checks, "uses_scores_or_optimum": False})
            require(all(checks.values()), "exact magnetic-generator certificate")
            generators[alpha, rho] = {"H": hamiltonian, "A": a, "nu": nu}
    scores = {}
    for y in combinations(range(8), 4):
        lifted = tuple(sorted(set(base)|{pool[j] for j in y})); require(len(lifted) == 12, "balanced candidate")
        formula = baseline+sum(fields[j] for j in y)-2*sum(weights[pool[j]][pool[h]] for j, h in combinations(y, 2))
        whole = edge_cut(weights, lifted, state); state["incremental_cost_calls"] += 1
        utility = max(0, current-whole); scores[y] = {"cost": whole, "h": utility}
        writer.emit({"kind": "candidate_cost", "case": name, "Y": y, "lifted": lifted, "whole_cut": whole, "formula": formula,
                     "delta": formula-whole, "current_cost": current, "h": utility, "current_R": y == (0, 1, 2, 3), "credit_all_controls": True})
        require(formula == whole and (y != (0, 1, 2, 3) or whole == current and utility == 0), "cost identity/current null")
    return {"id": name, "scores": scores, "generators": generators, "current_cost": current}


def build_frame(generator, kappa):
    return [[C(int(j == a))+C(0, kappa)*generator["H"][j][a] for a in range(4)] for j in range(8)]
def hand_frame(name):
    f = [[C(int(i == j)) for j in range(4)] for i in range(8)]
    if name == "H_HOM": f[0][1], f[1][0] = C(0, 1), C(0, 1)
    return f
def construct(f, state):
    state["matrix_operands"] = {"F": f}; identity = eye(4); gram = matmul(dagger(f), f)
    state["matrix_operands"]["frame_Gram"] = gram
    q = inverse([[identity[i][j]+gram[i][j] for j in range(4)] for i in range(4)], state)
    t = scale_matrix(matmul(f, q), 2); dump = matmul(difference(identity, gram), q)
    v = [list(row) for row in f]+[[-x for x in row] for row in identity]
    u = difference(eye(12), scale_matrix(matmul(matmul(v, q), dagger(v)), 2))
    state["matrix_operands"].update(Q=q, T=t, D_dump=dump, U=u)
    denominator = common_denominator(t, u); tn, un, dn = (scale_matrix(x, denominator) for x in (t, u, dump))
    gn, dumpgn = matmul(dagger(tn), tn), matmul(dagger(dn), dn)
    checks = {"Hermitian": un == dagger(un), "unitarity": matmul(dagger(un), un) == scale_matrix(eye(12), denominator**2),
              "occupied_columns": block(un, range(8), range(8, 12)) == tn and block(un, range(8, 12), range(8, 12)) == scale_matrix(dn, -1),
              "occupied_Gram": [[gn[i][j]+dumpgn[i][j] for j in range(4)] for i in range(4)] == scale_matrix(identity, denominator**2),
              "D_bound": denominator < 2**124}
    return gram, q, tn, dn, un, gn, dumpgn, denominator, checks


def convolution(y, groups, cache):
    """Gaussian-integer numerator; disjoint species subset allocation."""
    def assign(index, remaining):
        if index == len(groups): return F(int(not remaining))
        source = groups[index]; total = F(0)
        for received in combinations(remaining, len(source)):
            rest = tuple(j for j in remaining if j not in received)
            total += cache[received, source].abs2()*assign(index+1, rest)
        return total
    return assign(0, y)
def path_buckets(amplitudes, profile, paths):
    """Independent 24-path color expansion; never calls species convolution."""
    bins = {}
    for p in paths:
        key = tuple(profile[p[j]] for j in range(4)); bins[key] = bins.get(key, C())+amplitudes[p]
    return sum((value.abs2() for value in bins.values()), F(0))
def path_amplitudes(tn, y, paths):
    amplitudes = {}
    for p in paths:
        term = C(1)
        for row, column in zip(y, p): term = term*tn[row][column]
        amplitudes[p] = term
    return amplitudes
def cycle_coefficients(amplitudes, paths, cycles):
    values = []
    for tau in cycles:
        coefficient = C()
        for rho in paths:
            sigma = tuple(tau[rho[j]] for j in range(4))
            coefficient = coefficient+amplitudes[sigma]*amplitudes[rho].conjugate()
        values.append(coefficient)
    return values, sum(values, C())


def evaluate_context(name, f, graph, alpha, rho, kappa, writer, state, paths, profiles, targets):
    state.update(phase="matrix context", case=graph["id"] if graph else None, context=name)
    fg, q, tn, dn, un, gn, dumpgn, denominator, checks = construct(f, state); d8 = denominator**8
    if graph:
        a = graph["generators"][alpha, rho]["A"]
        checks["frame_Gram_identity"] = fg == [[C(int(i == j))+kappa*kappa*a[i][j] for j in range(4)] for i in range(4)]
    writer.emit({"kind": "matrix_context", "context": name, "case": graph["id"] if graph else None,
                 "alpha": alpha, "rho": rho, "kappa": kappa, "shared_null": kappa == 0 if graph else False,
                 "F_own_fractions": f, "frame_Gram_own_fractions": fg, "Q_own_fractions": q,
                 "D_scale": str(denominator), "T_num": integer_matrix(tn), "dump_num": integer_matrix(dn),
                 "U_num": integer_matrix(un), "G_num": integer_matrix(gn), "dump_Gram_num": integer_matrix(dumpgn),
                 "source_support": source_support(f), "input": [8, 9, 10, 11], "checks": checks})
    require(all(checks.values()), "exact reflection/Gram/denominator certificates")
    state.pop("matrix_operands", None); state.pop("inverse_state", None)
    cache, gram = {}, {}
    for size in range(5):
        for source in combinations(range(4), size):
            for received in combinations(range(8), size):
                state.update(phase="DP/Ryser subpermanents", source=source, received=received)
                dp, ryser = permanent_dp(block(tn, received, source)), permanent_ryser(block(tn, received, source))
                state["comparison"] = {"first": dp, "second": ryser, "D_scale": str(denominator), "power": size}
                writer.emit({"kind": "subpermanent_check", "context": name, "source": source, "received": received,
                             "power": size, "num": complex_integer(dp), "delta": complex_integer(dp-ryser)})
                require(dp == ryser, "independent subpermanent disagreement"); cache[received, source] = dp
            if size:
                dp, ryser = permanent_dp(block(gn, source, source)), permanent_ryser(block(gn, source, source))
                state.update(phase="DP/Ryser Gram permanents", comparison={"first": dp, "second": ryser, "power": 2*size})
                writer.emit({"kind": "gram_permanent_check", "context": name, "source": source,
                             "power": 2*size, "num": complex_integer(dp), "delta": complex_integer(dp-ryser)})
                require(dp == ryser and dp.im == 0 and dp.re >= 0, "real nonnegative Gram permanent"); gram[source] = dp.re
    require(len(cache) == 495 and len(gram) == 15, "complete subset caches")
    totals = {profile: {"cf": F(0), "I": F(0), "hazard": F(0)} for profile in profiles}; b_cf = {}
    for y in targets:
        state.update(phase="CF profile comparisons", Y=y); amplitudes = path_amplitudes(tn, y, paths)
        utility = graph["scores"][y]["h"] if graph else None
        for profile, groups in profiles.items():
            first, second = convolution(y, groups, cache), path_buckets(amplitudes, profile, paths)
            expected_hand = None
            if not graph:
                expected_hand = F(int(y == (0, 1, 2, 3))) if name == "H_ID" else (F(32, 81) if profile[0] != profile[1] and y == (0, 1, 2, 3) else F(0))
            state["comparison"] = {"first": first, "second": second, "D_scale": str(denominator), "power": 8, "expected_hand": expected_hand}
            writer.emit({"kind": "cf_comparison", "context": name, "profile": profile, "Y": y, "power": 8,
                         "num": integer_text(first), "delta": integer_text(first-second),
                         "expected_hand_num": integer_text(expected_hand*d8) if expected_hand is not None else None, "h": utility})
            require(first == second and first >= 0 and (expected_hand is None or first == expected_hand*d8), "independent CF/profile/hand comparison")
            if graph and kappa == 0: require(first == (d8 if y == (0, 1, 2, 3) else 0), "all profiles current-only null")
            totals[profile]["cf"] += first
            if graph:
                totals[profile]["I"] += utility*first
                if utility > 0: totals[profile]["hazard"] += first
            if profile == "0000": b_cf[y] = first/d8
    for profile, groups in profiles.items():
        state.update(phase="profile normalization", profile=profile); signal = F(1)
        for group in groups: signal *= gram[group]
        cf = totals[profile]["cf"]; collision, dump = signal-cf, d8-signal
        row = {"kind": "profile_totals", "context": name, "profile": profile, "power": 8,
               "all_signal_num": integer_text(signal), "CF_num": integer_text(cf), "SIGNAL_COLLISION_num": integer_text(collision),
               "DUMP_num": integer_text(dump), "total_num": integer_text(cf+collision+dump),
               "I_num": integer_text(totals[profile]["I"]) if graph else None,
               "hazard_num": integer_text(totals[profile]["hazard"]) if graph else None}
        state["profile_operands"] = row; writer.emit(row)
        require(min(cf, collision, dump) >= 0 and cf+collision+dump == d8, "raw coarse normalization")
        if not graph: require(signal == (F(1) if name == "H_ID" else F(64, 81))*d8, "hand signal/dump law")
        elif kappa == 0: require(cf == d8 and collision == dump == totals[profile]["I"] == 0, "lossless zero-utility null")
        totals[profile].update(all_signal=signal, collision=collision, dump=dump)
        totals[profile] = {key: value/d8 for key, value in totals[profile].items()}
    if not graph: writer.emit({"kind": "hand_completion", "context": name, "passed": True, "profiles": list(profiles)})
    return {"context": name, "alpha": alpha, "rho": rho, "kappa": kappa, "D_scale": denominator,
            "T_num": tn, "U_num": un, "profiles": totals, "b_cf": b_cf}


def full_normalization(result, writer, state):
    state["phase"] = "full1365 physical PNR"; un, d8 = result["U_num"], result["D_scale"]**8
    masses = {"CF": F(0), "SIGNAL_COLLISION": F(0), "DUMP": F(0)}; visited = 0
    for n in occupations(4, 12):
        state["occupation"] = n; rows = [j for j, count in enumerate(n) for unused in range(count)]
        amplitude = permanent_dp(block(un, rows, range(8, 12))); divisor = 1
        for count in n: divisor *= factorial(count)
        probability = amplitude.abs2()/(d8*divisor)
        if any(n[8:]): label, y = "DUMP", None
        elif all(count <= 1 for count in n[:8]): label, y = "CF", tuple(j for j, count in enumerate(n[:8]) if count)
        else: label, y = "SIGNAL_COLLISION", None
        expected_cf = result["b_cf"][y] if label == "CF" else None
        state["comparison"] = {"first": probability, "second": expected_cf, "amplitude_num": amplitude, "occupation_factorial": divisor}
        writer.emit({"kind": "full_pnr", "context": result["context"], "occupation": n, "amplitude_power": 4,
                     "amplitude_num": complex_integer(amplitude), "p_num": integer_text(amplitude.abs2()), "probability_power": 8,
                     "occupation_factorial": divisor, "classification": label,
                     "expected_CF_num": integer_text(expected_cf*d8) if expected_cf is not None else None,
                     "CF_delta_num": integer_text((probability-expected_cf)*d8) if expected_cf is not None else None})
        require(probability >= 0 and (expected_cf is None or probability == expected_cf), "full-U/receiver CF identity")
        masses[label] += probability; visited += 1
    expected = result["profiles"]["0000"]; reference = {"CF": expected["cf"], "SIGNAL_COLLISION": expected["collision"], "DUMP": expected["dump"]}
    writer.emit({"kind": "full_pnr_totals", "context": result["context"], "bins": visited, "power": 8,
                 "mass_num": {key: integer_text(value*d8) for key, value in masses.items()},
                 "delta": {key: integer_text((value-reference[key])*d8) for key, value in masses.items()}, "total": sum(masses.values())})
    require(visited == 1365 and sum(masses.values()) == 1 and masses == reference, "complete full-PNR/coarse identity")


def envelopes(graph, runs, profiles, writer, state):
    state.update(phase="independent grid envelopes", case=graph["id"]); best = {}
    for profile in profiles:
        index = max(range(len(runs)), key=lambda i: runs[i]["profiles"][profile]["I"])
        run, outcome = runs[index], runs[index]["profiles"][profile]
        best[profile] = {"grid_index": index, "alpha": run["alpha"], "rho": run["rho"], "kappa": run["kappa"],
                         "null_selected": run["kappa"] == 0, "kappa_at_registered_max": run["kappa"] == 4,
                         "I": outcome["I"], "hazard": outcome["hazard"]}
        writer.emit({"kind": "grid_envelope", "case": graph["id"], "profile": profile,
                     "all_I": [r["profiles"][profile]["I"] for r in runs], **best[profile]})
    proper_name = max((p for p in profiles if p != "0000"), key=lambda p: best[p]["I"])
    proper, b = best[proper_name]["I"], best["0000"]
    frontier = max(row["h"] for row in graph["scores"].values()); current_h = graph["scores"][(0, 1, 2, 3)]["h"]
    require(current_h == 0 and all(0 <= value["I"] <= frontier and 0 <= value["hazard"] <= 1 for value in best.values()), "credited full frontier/current null")
    return {"case": graph["id"], "B": b, "proper_profile": proper_name, "proper_best": best[proper_name],
            "proper_envelope": proper, "strict_grid": b["I"] > proper, "frontier_h": frontier, "current_R_h": current_h,
            "no_improving_candidate": frontier == 0, "frontier_fully_credited": True, "optimizer_advantage": False}


def selected_cycles(graph, result, paths, cycles, targets, writer, state):
    state.update(phase="registered best-B auxiliary four cycles", context=result["context"]); weighted = F(0); d8 = result["D_scale"]**8
    for y in targets:
        values, total = cycle_coefficients(path_amplitudes(result["T_num"], y, paths), paths, cycles); utility = graph["scores"][y]["h"]
        state["cycle_operands"] = {"coefficients_num": values, "total_num": total, "h": utility, "Y": y}
        writer.emit({"kind": "selected_four_cycle", "context": result["context"], "Y": y, "power": 8,
                     "six_coefficients_num": [complex_integer(value) for value in values], "total_num": complex_integer(total),
                     "h": utility, "weighted_real_num": integer_text(utility*total.re)})
        require(total.im == 0, "real signed four-cycle sum"); weighted += utility*total.re
    return weighted/d8


def main():
    resource.setrlimit(resource.RLIMIT_FSIZE, (CAP, CAP)); resource.setrlimit(resource.RLIMIT_CPU, (CPU, CPU))
    parser = argparse.ArgumentParser(); parser.add_argument("--binding", required=True); args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15) and sys.dont_write_bytecode and
            os.environ.get("PYTHONDONTWRITEBYTECODE") == "1" and all(os.environ.get(key) == "1" for key in THREADS), "CPython/-B/thread profile")
    binding, roles, before, binding_sha = authorize(root, args.binding)
    require(not any(row["path"].startswith(str(Path(OUT).parent)+"/") for row in binding["artifacts"]), "inputs outside fresh run parent")
    writer = Evidence(root/OUT)
    state = {"phase": "authorized setup", "edge_cut_calls": 0, "incremental_cost_calls": 0, "field_checks": 0, "two_hop_pair_sums": 0, "two_hop_products": 0}
    failure, decisions, completed, attempted, after = None, [], [], [], None
    plan = ["setup", "graphs/features/costs", "H_ID", "H_HOM"]
    for prefix in ("ER1411001", "RR1411002"):
        for i in range(17):
            plan.append(prefix+"/g"+str(i))
            if prefix == "ER1411001" and i == 14: plan.append("full1365")
    plan += ["envelopes/ER1411001", "envelopes/RR1411002", "selected-C4/ER1411001", "selected-C4/RR1411002", "final_population", "final_integrity"]
    def start(task):
        require(task in plan and task not in attempted, "unique registered task"); state["task"] = task; attempted.append(task)
    try:
        start("setup"); free = shutil.disk_usage(root).free
        require(free > CAP+4194304+1048576, "science/log/metadata free-space allowance")
        random, nx = software_after_authority(roles); paths, cycles, profiles, grid, targets = registered()
        writer.emit({"kind": "provenance", "source_sha256": binding["source_sha256"], "binding": args.binding, "binding_sha256": binding_sha,
                     "source_origin": "DERIVED_P134_c443389_NOT_INDEPENDENT_REPLICATION", "before": before,
                     "Python": sys.version, "networkx": nx.__version__, "environment": {key: os.environ.get(key) for key in THREADS},
                     "factory_backend": "networkx", "backend_priorities": {key: list(getattr(nx.config.backend_priority, key)) for key in ("algos", "generators", "classes")},
                     "profiles": PROFILE_NAMES, "grid": grid, "permutation_order": paths, "four_cycles": cycles, "targets": targets,
                     "CPU": CPU, "wall_ROOT": 240, "science_cap": CAP, "record_cap": CAP-RESERVE, "final_reserve": RESERVE,
                     "disk_free_bytes_before": free, "photon_RNG_draws": 0, "native_calls": 0, "optimizer_advantage": False})
        completed.append("setup"); start("graphs/features/costs")
        graphs = [graph_context(i, random, nx, writer, state) for i in range(2)]; completed.append("graphs/features/costs")
        for name in ("H_ID", "H_HOM"):
            start(name); evaluate_context(name, hand_frame(name), None, None, None, None, writer, state, paths, profiles, targets); completed.append(name)
        runs_by_case = {}
        for graph in graphs:
            runs = []
            for index, (alpha, rho, kappa) in enumerate(grid):
                name = graph["id"]+"/g"+str(index); start(name)
                result = evaluate_context(name, build_frame(graph["generators"][alpha, rho], kappa), graph, alpha, rho, kappa, writer, state, paths, profiles, targets)
                runs.append(result); completed.append(name)
                if graph["id"] == "ER1411001" and index == 14:
                    start("full1365"); full_normalization(result, writer, state); completed.append("full1365")
                result.pop("U_num")
            runs_by_case[graph["id"]] = runs
        for graph in graphs:
            task = "envelopes/"+graph["id"]; start(task)
            decisions.append(envelopes(graph, runs_by_case[graph["id"]], profiles, writer, state)); completed.append(task)
        for graph, decision in zip(graphs, decisions):
            task = "selected-C4/"+graph["id"]; start(task); selected = runs_by_case[graph["id"]][decision["B"]["grid_index"]]
            decision["selected_J4"] = selected_cycles(graph, selected, paths, cycles, targets, writer, state)
            writer.emit({"kind": "graph_decision", **decision}); completed.append(task)
        start("final_population")
        require(writer.counts == EXPECTED and writer.rows == 58443 and state["edge_cut_calls"] == 160 and state["incremental_cost_calls"] == 140 and
                state["field_checks"] == 16 and state["two_hop_pair_sums"] == 56 and state["two_hop_products"] == 1344 and len(completed) == 43, "fixed population/cost ledger")
        completed.append("final_population"); start("final_integrity"); state["phase"] = "final input integrity"
        after = {"project": [inspect_descriptor(row, local_file(root, row["path"]), state) for row in binding["artifacts"]],
                 "external": [inspect_descriptor(row, external_file(row["path"]), state) for row in binding["external_artifacts"]]}
        require(sha(local_file(root, args.binding)) == binding_sha, "active binding changed")
        completed.append("final_integrity"); require(len(plan) == len(completed) == 45 and set(completed) == set(plan), "all tasks complete")
    except Exception as exc:
        failure = {"state": state, "exception": repr(exc), "traceback": traceback.format_exc()}
    signal = "NOT_ACCEPTED_ENGINE_FAILURE" if failure else ("FOLLOWUP" if all(d["strict_grid"] for d in decisions) else "NO_SIGNAL")
    writer.finish({"status": "INCONCLUSIVE_FIRST_FAILURE" if failure else "EXACT_GRID_ENGINE_PASS", "signal_status": signal,
                   "counts": writer.counts, "records": writer.rows, "record_bytes": writer.bytes,
                   "cost_ledger": {key: state[key] for key in ("edge_cut_calls", "incremental_cost_calls", "field_checks", "two_hop_pair_sums", "two_hop_products")},
                   "completed": completed, "task_plan": plan, "FAILED_TASK": [t for t in attempted if t not in completed], "NOT_RUN": [t for t in plan if t not in attempted],
                   "decisions": decisions, "after": after, "registered_graph_MT_streams": 6, "photon_RNG_draws": 0, "native_calls": 0, "FPRAS_calls": 0,
                   "positive_accepted": False, "optimizer_advantage": False, "practical_speed_advantage": False, "sampler_claim": False}, failure)
    if failure: raise SystemExit(1)


if __name__ == "__main__": main()
