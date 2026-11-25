"""Prospective P66 finite diagnostic. Import performs no scientific work.

No production helper import, random draw, sampler, optimizer or full Fock law.
All scientific execution is deferred until the separately authorized bounded run.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import importlib.metadata
from itertools import combinations
import json
import math
from pathlib import Path
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[1]
PERSISTENT_PYTHON = Path("/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python")
MAX_SCIENTIFIC_BYTES = 28 * 1024 * 1024
MAX_RECORD_BYTES = 27 * 1024 * 1024
ABS_TOL, REL_TOL = 1e-12, 1e-7


class C:
    """Exact complex rational, never coerced through binary64 arithmetic."""
    __slots__ = ("r", "i")

    def __init__(self, r=0, i=0):
        if isinstance(r, C):
            self.r, self.i = r.r, r.i
        else:
            self.r, self.i = F(r), F(i)

    def __add__(self, other):
        other = C(other)
        return C(self.r + other.r, self.i + other.i)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.r, -self.i)

    def __sub__(self, other):
        return self + (-C(other))

    def __rsub__(self, other):
        return C(other) - self

    def __mul__(self, other):
        other = C(other)
        return C(self.r * other.r - self.i * other.i,
                 self.r * other.i + self.i * other.r)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = C(other)
        denominator = other.norm2()
        if not denominator:
            raise ZeroDivisionError("exact complex division by zero")
        return C((self.r * other.r + self.i * other.i) / denominator,
                 (self.i * other.r - self.r * other.i) / denominator)

    def __rtruediv__(self, other):
        return C(other) / self

    def __eq__(self, other):
        if not isinstance(other, (C, int, F)):
            return False
        other = C(other)
        return self.r == other.r and self.i == other.i

    def __bool__(self):
        return bool(self.r or self.i)

    def conjugate(self):
        return C(self.r, -self.i)

    def norm2(self):
        return self.r * self.r + self.i * self.i

    def floating(self):
        return complex(float(self.r), float(self.i))


def identity(n):
    return [[C(int(i == j)) for j in range(n)] for i in range(n)]


def multiply(a, b):
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("matrix dimensions")
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), C())
             for j in range(len(b[0]))] for i in range(len(a))]


def adjoint(a):
    return [[C(a[j][i]).conjugate() for j in range(len(a))]
            for i in range(len(a[0]))]


def inverse(a):
    """Gauss--Jordan over Q(i); first nonzero pivot, maximum dimension 12."""
    n = len(a)
    if not 1 <= n <= 12 or any(len(row) != n for row in a):
        raise ValueError("inverse dimension guard")
    unit = identity(n)
    rows = [[C(x) for x in a[i]] + unit[i] for i in range(n)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if rows[r][col]), None)
        if pivot is None:
            raise ArithmeticError("singular rational matrix")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [x / scale for x in rows[col]]
        for r in range(n):
            if r != col and rows[r][col]:
                scale = rows[r][col]
                rows[r] = [x - scale * y for x, y in zip(rows[r], rows[col])]
    return [row[n:] for row in rows]


def permanent(a):
    """Ryser inclusion--exclusion with Gray-code column updates; n <= 6."""
    n = len(a)
    if n > 6 or any(len(row) != n for row in a):
        raise ValueError("permanent dimension guard")
    if n == 0:
        return F(1)
    rowsums, previous, total = [0] * n, 0, 0
    for index in range(1, 1 << n):
        gray = index ^ (index >> 1)
        changed = gray ^ previous
        col = changed.bit_length() - 1
        direction = 1 if gray & changed else -1
        product = 1
        for row in range(n):
            rowsums[row] = rowsums[row] + direction * a[row][col]
            product = product * rowsums[row]
        total = total + (product if (n - gray.bit_count()) % 2 == 0 else -product)
        previous = gray
    return total


def fock_probability(u, source_counts, target_counts):
    """Both normalized Fock factorials; only tiny collided fixtures use them."""
    if (len(source_counts) != len(u) or len(target_counts) != len(u)
            or any(type(x) is not int or x < 0 for x in source_counts + target_counts)
            or sum(source_counts) != sum(target_counts)):
        raise ValueError("invalid normalized Fock occupations")
    columns = [i for i, count in enumerate(source_counts) for _ in range(count)]
    rows = [i for i, count in enumerate(target_counts) for _ in range(count)]
    value = C(permanent([[u[i][j] for j in columns] for i in rows])).norm2()
    normalization = math.prod(math.factorial(x) for x in source_counts + target_counts)
    return value / normalization


def graph(l, w):
    """Literal four cliques, two fixed matchings, optional uniform cross block."""
    if l not in (2, 3) or w not in (F(0), F(1, 2 * l)):
        raise ValueError("frozen graph domain")
    n, d = 4 * l, 2 * l
    a = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if i // l == j // l:
                weight = F(3)
            elif (i < d) != (j < d):
                weight = w
            elif j - i == l:
                weight = F(1)
            else:
                weight = F(0)
            a[i][j] = a[j][i] = weight
    return a


def cut(a, selected):
    selected = frozenset(selected)
    return sum((a[i][j] for i in selected for j in range(len(a))
                if j not in selected), F(0))


def source_targets(l):
    cliques = [tuple(range(i * l, (i + 1) * l)) for i in range(4)]
    bad = [cliques[a] + cliques[b] for a in (0, 1) for b in (2, 3)]
    good = [cliques[0] + cliques[1], cliques[2] + cliques[3]]
    return bad, good


def cayley(a, t, lam):
    n = len(a)
    degree = max(sum(row, F(0)) for row in a)
    denominator = degree + lam * (n - 1)
    if denominator <= 0:
        raise ValueError("nonpositive weighted normalization")
    h = [[(a[i][j] + (lam if i != j else 0)) / denominator
          for j in range(n)] for i in range(n)]
    minus = [[C(int(i == j), -t * h[i][j]) for j in range(n)] for i in range(n)]
    plus = [[C(int(i == j), t * h[i][j]) for j in range(n)] for i in range(n)]
    inv = inverse(minus)
    return multiply(plus, inv), h, denominator, minus, inv


def dark_projector(n, block):
    d, selected = len(block), frozenset(block)
    return [[C(F(int(i == j)) - F(1, d)) if i in selected and j in selected
             else C() for j in range(n)] for i in range(n)]


def bright_pgf(modes, occupied):
    """Coefficient vector of sum_m (occupied)_m/modes^m * (z-1)^m."""
    if not 1 <= occupied <= modes <= 16:
        raise ValueError("bright PGF domain")
    coefficients = [F(0)] * (occupied + 1)
    falling = 1
    for m in range(occupied + 1):
        if m:
            falling *= occupied - m + 1
        moment = F(falling, modes ** m)
        for k in range(m + 1):
            coefficients[k] += moment * math.comb(m, k) * (-1) ** (m - k)
    return coefficients


def bounds(l):
    a = F(math.factorial(l), (2 * l) ** l)
    b = min(F(1), F(l + 1, 2) * F(l + 1, 2 * l) ** l)
    return a, b, min(F(1), 2 * a * b), min(F(1), F(2, (2 * l) ** l))


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, C):
        return [str(value.r), str(value.i)]
    if isinstance(value, Path):
        return str(value)
    raise TypeError(type(value).__name__)


def json_bytes(value):
    return (json.dumps(value, default=encode, allow_nan=False, sort_keys=True) + "\n").encode()


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def native_api():
    """Local point-amplitude backend only; no source, seed or sampler created."""
    # main() enforces the experiment's contracted interpreter. Keep this
    # loader usable by portable native-physics tests; package/thread guards
    # and observed interpreter provenance still apply below.
    versions = {name: importlib.metadata.version(name) for name in
                ("numpy", "scipy", "perceval-quandela", "exqalibur")}
    if versions != {"numpy": "2.4.6", "scipy": "1.17.1",
                    "perceval-quandela": "1.3.0", "exqalibur": "1.4.2"}:
        raise RuntimeError("pinned numerical package versions differ")
    import exqalibur as xq
    xq.Config.compute_max_thread_count = 1
    native_readback(xq)
    import perceval as pcvl
    from perceval.backends import NaiveBackend
    native_readback(xq)
    files = {}
    for name, module in sorted(sys.modules.copy().items()):
        path = getattr(module, "__file__", None)
        if path and "/pasqal/.venv/" in str(Path(path).resolve()) and Path(path).is_file():
            files[name] = {"path": str(Path(path).resolve()), "sha256": digest(path)}
    metadata = {"versions": versions, "threads": native_readback(xq),
                "interpreter": str(Path(sys.executable).resolve()),
                "interpreter_sha256": digest(sys.executable), "loaded_module_files": files}
    return (pcvl, xq, NaiveBackend), metadata


def persistent_interpreter():
    if (Path(sys.executable).resolve() != PERSISTENT_PYTHON.resolve()
            or Path(sys.prefix).resolve() != PERSISTENT_PYTHON.parent.parent.resolve()
            or sys.version_info[:3] != (3, 11, 15)):
        raise RuntimeError("use the contracted persistent Python 3.11.15 virtual environment")


def native_readback(xq):
    observed = int(xq.Config.compute_max_thread_count)
    if observed != 1:
        raise RuntimeError("native thread readback is not one")
    return observed


def native_backend(u, api):
    pcvl, xq, backend_type = api
    native_readback(xq)
    matrix = [[C(x).floating() for x in row] for row in u]
    backend = backend_type()
    backend.set_circuit(pcvl.Circuit(len(u)).add(0, pcvl.Unitary(pcvl.Matrix(matrix))))
    return backend


def native_point(backend, source, target, api):
    pcvl, xq, _ = api
    native_readback(xq)
    backend.set_input_state(pcvl.BasicState(source))
    amplitude = complex(backend.prob_amplitude(pcvl.BasicState(target)))
    probability = abs(amplitude) ** 2
    if not all(math.isfinite(x) for x in (amplitude.real, amplitude.imag, probability)):
        raise ArithmeticError(f"nonfinite native point: amplitude={amplitude!r}, probability={probability!r}")
    native_readback(xq)
    return amplitude, probability


class FirstFailure(AssertionError):
    pass


class Ledger:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=False)
        self.stream = (self.output / "records.jsonl").open("xb")
        self.bytes = self.checks = 0
        self.counts = {key: 0 for key in ("matrices", "cuts", "bosonic_points",
                                        "distinguishable_points", "unions", "pgfs", "native_points")}
        self.context = {}

    def emit(self, kind, **record):
        payload = json_bytes({"kind": kind, **record})
        if self.bytes + len(payload) > MAX_RECORD_BYTES:
            raise RuntimeError("prospective scientific record byte cap")
        self.stream.write(payload)
        self.stream.flush()
        self.bytes += len(payload)

    def require(self, condition, label):
        self.checks += 1
        if not condition:
            raise FirstFailure(label)


def exact_population(ledger):
    native_cases = []
    for l in (2, 3):
        n, d = 4 * l, 2 * l
        bad, good = source_targets(l)
        a_bound, b_bound, boson_bound, distinguishable_bound = bounds(l)
        for w in (F(0), F(1, d)):
            family = "disconnected" if w == 0 else "connected"
            ledger.context = {"stage": "landscape", "L": l, "family": family}
            adjacency = graph(l, w)
            degree = F(3 * (l - 1) + 1) + d * w
            ledger.require(all(sum(row, F(0)) == degree for row in adjacency), "regular weighted degree")
            good_cost, bad_cost = 4 * w * l * l, 2 * l + 2 * w * l * l
            gap = 2 * 3 * (l - 1) - 2 * l
            ledger.require(good_cost < bad_cost and gap > 0, "strict landscape constants")
            for selected in combinations(range(n), d):
                value = cut(adjacency, selected)
                role = "good" if selected in good else "bad" if selected in bad else "partial"
                ledger.emit("cut", L=l, family=family, selected=selected, cost=value, role=role)
                ledger.counts["cuts"] += 1
                expected = good_cost if role == "good" else bad_cost
                ledger.require(value == expected if role != "partial" else value >= bad_cost + gap,
                               "exhaustive balanced cost landscape")
            for t in (F(0), F(1, 4), F(1), F(2)):
                for lam in (F(0), F(1, 4)):
                    ledger.context = {"stage": "matrix", "L": l, "family": family, "t": t, "lambda": lam}
                    u, h, denominator, minus, inv = cayley(adjacency, t, lam)
                    unit = identity(n)
                    flags = {"left_inverse": multiply(minus, inv) == unit,
                             "right_inverse": multiply(inv, minus) == unit,
                             "unitary": multiply(adjoint(u), u) == unit,
                             "symmetric": u == [list(row) for row in zip(*u)]}
                    for label, block in zip(("A", "B"), good):
                        projector = dark_projector(n, block)
                        flags["dark_" + label] = multiply(u, projector) == multiply(projector, u)
                    for label, rows, cols in (("AB", good[0], good[1]), ("BA", good[1], good[0])):
                        z = u[rows[0]][cols[0]]
                        flags["uniform_cross_" + label] = all(u[i][j] == z for i in rows for j in cols)
                    ledger.emit("matrix", **ledger.context, adjacency=adjacency, H=h, D=denominator,
                                U=u, exact_checks=flags,
                                cross_rank_AB=int(bool(u[0][d])), cross_rank_BA=int(bool(u[d][0])))
                    ledger.counts["matrices"] += 1
                    for label, passed in flags.items():
                        ledger.require(passed, label)
                    ledger.require(denominator == degree + lam * (n - 1), "weighted background normalization")
                    native_rows = []
                    for source in bad:
                        b_total, d_total = F(0), F(0)
                        for target in good:
                            ledger.context = {"stage": "exact_probability", "L": l, "family": family,
                                              "t": t, "lambda": lam, "source": source, "target": target}
                            block = [[u[i][j] for j in source] for i in target]
                            amplitude = C(permanent(block))
                            probability = amplitude.norm2()
                            distinguishable = permanent([[entry.norm2() for entry in row] for row in block])
                            ledger.emit("probability", L=l, family=family, t=t, lambda_value=lam,
                                        source=source, target=target, amplitude=amplitude,
                                        bosonic=probability, distinguishable=distinguishable,
                                        bosonic_point_bound=a_bound * b_bound,
                                        distinguishable_point_bound=F(1, d ** l))
                            ledger.counts["bosonic_points"] += 1
                            ledger.counts["distinguishable_points"] += 1
                            ledger.require(0 <= probability <= a_bound * b_bound, "bosonic point bound")
                            ledger.require(0 <= distinguishable <= F(1, d ** l), "distinguishable point bound")
                            b_total += probability
                            d_total += distinguishable
                            if t == 1 and lam == F(1, 4):
                                native_rows.append((source, target, probability))
                        ledger.emit("union", L=l, family=family, t=t, lambda_value=lam,
                                    source=source, bosonic=b_total, bosonic_bound=boson_bound,
                                    distinguishable=d_total, distinguishable_bound=distinguishable_bound)
                        ledger.counts["unions"] += 1
                        ledger.require(b_total <= boson_bound, "raw bosonic two-target union")
                        ledger.require(d_total <= distinguishable_bound, "raw distinguishable two-target union")
                    if native_rows:
                        native_cases.append((l, family, u, native_rows))
    for l in range(2, 9):
        ledger.context = {"stage": "PGF", "L": l}
        a_bound, b_bound, _, _ = bounds(l)
        target = bright_pgf(2 * l, 2 * l)
        source = bright_pgf(2 * l, l)
        tail = sum(target[l:], F(0))
        ledger.emit("bright_pgf", L=l, target_probabilities=target, source_probabilities=source,
                    target_tail=tail, target_tail_bound=b_bound, source_all_bright=source[-1],
                    source_all_bright_expected=a_bound)
        ledger.counts["pgfs"] += 1
        ledger.require(all(p >= 0 for p in target + source), "PGF coefficient nonnegativity")
        ledger.require(sum(target, F(0)) == sum(source, F(0)) == 1, "PGF mass one")
        ledger.require(sum((i * p for i, p in enumerate(target)), F(0)) == 1, "target bright mean one")
        ledger.require(tail <= b_bound, "exact bright tail")
        ledger.require(source[-1] == a_bound, "source all-bright normalization")
    return native_cases


def native_population(ledger, cases):
    ledger.context = {"stage": "native_import"}
    started = time.perf_counter()
    api, metadata = native_api()
    ledger.emit("native_runtime", metadata=metadata, import_wall_seconds=time.perf_counter() - started)
    for l, family, u, rows in cases:
        ledger.context = {"stage": "native_points", "L": l, "family": family}
        started = time.perf_counter()
        backend = native_backend(u, api)
        ledger.emit("native_setup", L=l, family=family,
                    setup_wall_seconds=time.perf_counter() - started)
        for source, target, exact in rows:
            source_counts = [int(i in source) for i in range(4 * l)]
            target_counts = [int(i in target) for i in range(4 * l)]
            ledger.context = {"stage": "native_point", "L": l, "family": family,
                              "source": source_counts, "target": target_counts}
            started = time.perf_counter()
            amplitude, observed = native_point(backend, source_counts, target_counts, api)
            reference = float(exact)
            absolute = abs(observed - reference)
            scale = max(observed, reference)
            relative = absolute / scale if scale else 0.0
            tolerance = ABS_TOL + REL_TOL * scale
            ledger.emit("native_point", L=l, family=family, t=F(1), lambda_value=F(1, 4),
                        source=source_counts, target=target_counts, exact=exact,
                        native_amplitude=[amplitude.real, amplitude.imag], native_probability=observed,
                        exact_zero=exact == 0, native_zero=observed == 0,
                        exact_positive_tiny=exact > 0 and reference <= ABS_TOL, absolute_error=absolute,
                        relative_error=relative, mixed_tolerance=tolerance,
                        tolerance_dominance="absolute" if ABS_TOL >= REL_TOL * scale else "relative",
                        query_wall_seconds=time.perf_counter() - started)
            ledger.counts["native_points"] += 1
            ledger.require(absolute <= tolerance, "fixed native point mixed tolerance")
    ledger.context = {"stage": "native_final_readback"}
    ledger.require(native_readback(api[1]) == 1, "native final threads")
    for item in metadata["loaded_module_files"].values():
        ledger.context = {"stage": "native_input_rehash", "path": item["path"]}
        ledger.require(digest(item["path"]) == item["sha256"], "native module input unchanged")


def run(output):
    wall, cpu = time.perf_counter(), time.process_time()
    ledger = Ledger(output)
    failure = None
    status = "INCONCLUSIVE_FIRST_FAILURE"
    try:
        cases = exact_population(ledger)
        native_population(ledger, cases)
        expected = {"matrices": 32, "cuts": 1988, "bosonic_points": 256,
                    "distinguishable_points": 256, "unions": 128, "pgfs": 7, "native_points": 32}
        ledger.require(ledger.counts == expected, "complete prospective coverage")
        status = "PASS_FINITE_ASSERTION"
    except Exception as error:
        failure = {"context": ledger.context, "type": type(error).__name__, "message": str(error),
                   "traceback": traceback.format_exc(limit=8), "retry_permitted": False}
    finally:
        ledger.stream.close()
    summary = {"status": status, "counts": ledger.counts, "checks": ledger.checks,
               "body_wall_seconds": time.perf_counter() - wall,
               "body_cpu_seconds": time.process_time() - cpu,
               "source_sha256": digest(__file__), "records_sha256": digest(ledger.output / "records.jsonl"),
               "native_random_draws": 0, "QPU_calls": 0, "optimizer_steps": 0,
               "full_Fock_laws": 0, "universal_proof_certified": False,
               "native_comparison_is_tolerance_conditional": True, "first_failure": failure}
    for name, value in (("failure.json", {"first_failure": failure}), ("summary.json", summary)):
        payload = json_bytes(value)
        if ledger.bytes + len(payload) > MAX_SCIENTIFIC_BYTES:
            raise RuntimeError("scientific total byte cap")
        with (ledger.output / name).open("xb") as handle:
            handle.write(payload)
        ledger.bytes += len(payload)
    return 0 if status == "PASS_FINITE_ASSERTION" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT) or output == ROOT:
        raise ValueError("output must be a fresh directory inside this worktree")
    persistent_interpreter()
    return run(output)


if __name__ == "__main__":
    raise SystemExit(main())
