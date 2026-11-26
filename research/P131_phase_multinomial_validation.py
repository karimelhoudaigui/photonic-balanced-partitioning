"""P131 deterministic exact qualification; no import-time experiment or RNG.

Only this CLI may read separately ROOT-bound old raw references. The inactive
TEMPLATE is never authority. No P96/P107/P110 production module is imported.
Scientific mismatches are recorded and accumulated; they do not skip later bins.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import comb, factorial, prod
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
PYTHON = "/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python"
OUTPUT = "research/P131_phase_multinomial_main/run_001/data"
BINDING = "research/P131_phase_multinomial_execution_binding.json"
CAP, FINAL_CAP, RESERVE = 8388608, 65536, 131072
CPU, WALL = 120, 180
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
STATIC = ("AGENTS.md", "pyproject.toml", "requirements-research-lock.txt",
          "research/P131_phase_multinomial.py", "research/P131_phase_multinomial_validation.py",
          "research/P131_PHASE_MULTINOMIAL_POPULATION.md", "research/P131_phase_multinomial_contract_TEMPLATE.json",
          "research/P129_FINITE_PHASE_MULTINOMIAL_REPLACEMENT.md",
          "research/P96_column_loss_validation.py", "research/P107_symbolic_filter_validation.py")
PINS = {"research/P129_FINITE_PHASE_MULTINOMIAL_REPLACEMENT.md":
        "515d2c2ac9b2e4763d17d591691ff8aa71e004fd77400b0d8364e2d5092870b8",
        "research/P96_column_loss_validation.py":
        "ee3592ef608b0b7ad19ba81babcdc369bf4da50e319f3f00baf868074d83c223",
        "research/P107_symbolic_filter_validation.py":
        "4e0973ebfe8a250dbf012719087dcb0b7390932acd3ddab4e7055b3808cb2bbc"}
SEALS = {"P96": "240c7e5518fbcd69d8f22bbe5e8ead3c1bbbc9c1",
         "P107": "99f2d98d93f13c7fc088218bfb06ff39af4c40e9"}
PREFIX = {"P96": "research/P96_column_loss_main/run_001",
          "P107": "research/P107_symbolic_filter_main/run_001"}
SUFFIX = {"manifest": "manifest.json", "stdout": "stdout.txt", "stderr": "stderr.txt",
          "records": "data/records.jsonl", "summary": "data/summary.json", "failure": "data/failure.json"}
CLAIMS = {"P96": "P96-COLUMN-BUDGET-TWO-PHOTON-SURROGATE-FINITE-VALIDATION",
          "P107": "P107-EXACT-P101-FINITE-FILTER-SQUARE-DISCRIMINATOR"}


def need(value, message):
    if not value:
        raise ValueError(message)


class C:
    """Independent Gaussian-rational oracle arithmetic, not control helpers."""
    __slots__ = ("r", "i")
    def __init__(self, real=0, imag=0):
        self.r, self.i = F(real), F(imag)
    def __add__(self, other):
        other = other if isinstance(other, C) else C(other)
        return C(self.r+other.r, self.i+other.i)
    __radd__ = __add__
    def __neg__(self):
        return C(-self.r, -self.i)
    def __sub__(self, other):
        return self + (-other if isinstance(other, C) else C(-other))
    def __mul__(self, other):
        other = other if isinstance(other, C) else C(other)
        return C(self.r*other.r-self.i*other.i, self.r*other.i+self.i*other.r)
    __rmul__ = __mul__
    def __truediv__(self, denominator):
        return C(self.r/denominator, self.i/denominator)
    def conjugate(self):
        return C(self.r, -self.i)
    def __bool__(self):
        return bool(self.r or self.i)
    def __eq__(self, other):
        other = other if isinstance(other, C) else C(other)
        return self.r == other.r and self.i == other.i


def clean(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, C):
        return [str(value.r), str(value.i)]
    if isinstance(value, (tuple, list)):
        return [clean(x) for x in value]
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    return value


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key: " + repr(key))
        result[key] = value
    return result


def loads(text):
    def reject(value):
        raise ValueError("nonstandard JSON number: " + value)
    return json.loads(text, object_pairs_hook=unique, parse_constant=reject)


def exact_fraction(value):
    need(type(value) in (int, str), "exact fraction encoding: " + repr(value))
    return F(value)


def exact_int(value):
    need(type(value) is int, "strict integer: " + repr(value))
    return value


def safe(relative):
    path = Path(relative)
    need(type(relative) is str and path.as_posix() == relative and path.parts
         and not path.is_absolute() and all(x not in (".", "..") for x in path.parts), "canonical relative file")
    actual = ROOT
    for part in path.parts:
        actual /= part
        need(not actual.is_symlink(), "input symlink: " + relative)
    need(actual.is_file(), "regular input: " + relative)
    return actual


def digest(path, blob=False):
    h = hashlib.sha1() if blob else hashlib.sha256()
    if blob:
        h.update(("blob " + str(path.stat().st_size) + "\0").encode("ascii"))
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            h.update(block)
    return h.hexdigest()


class Evidence:
    def __init__(self):
        directory = ROOT/OUTPUT
        need(directory.parent.is_dir() and not directory.exists(), "fresh runner child")
        current = ROOT
        for part in Path(OUTPUT).parts:
            current /= part
            need(not current.is_symlink(), "output symlink")
        directory.mkdir()
        self.directory, self.used, self.rows = directory, 0, 0
        self.handle = (directory/"records.jsonl").open("x", encoding="ascii")
    def payload(self, row):
        return json.dumps(clean(row), ensure_ascii=True, sort_keys=True,
                          separators=(",", ":"), allow_nan=False)+"\n"
    def emit(self, row):
        text = self.payload(row)
        need(self.used+len(text.encode("ascii")) <= CAP-RESERVE, "scientific output reserve")
        self.handle.write(text)
        self.handle.flush()
        self.used += len(text.encode("ascii"))
        self.rows += 1
    def finish(self, summary, failure):
        self.handle.close()
        payloads = [self.payload(value) for value in (summary, failure)]
        need(all(len(text.encode("ascii")) <= FINAL_CAP for text in payloads), "summary/failure64KiB cap")
        need(self.used+sum(len(text.encode("ascii")) for text in payloads) <= CAP, "combined science8MiB")
        for name, text in zip(("summary.json", "failure.json"), payloads):
            with (self.directory/name).open("x", encoding="ascii") as handle:
                handle.write(text)


def authorize(relative, writer):
    need(relative == BINDING, "fixed separate active binding")
    b = loads(safe(relative).read_text(encoding="utf-8"))
    writer.emit({"kind": "binding_observation", "binding": b})
    need(b["binding_state"] == "ROOT_AUTHORIZED" and b["run_authorized"] is True, "separate ROOT authority")
    need(b["planned_command"] == [PYTHON, "-B", "research/P131_phase_multinomial_validation.py", "--binding", BINDING], "frozen argv")
    limits = b["runner_binding"]
    need(type(limits["timeout"]) in (int, float) and limits["timeout"] == WALL
         and type(limits["max_cpu_seconds"]) is int and limits["max_cpu_seconds"] == CPU
         and type(limits["max_threads"]) is int and limits["max_threads"] == 1
         and type(limits["max_output_bytes"]) is int and limits["max_output_bytes"] == 4194304
         and limits["max_memory_bytes"] is None and limits["max_cores"] is None, "fixed runner caps; no float tolerance")
    names = [row["path"] for row in b["artifacts"]]
    raw_names = {PREFIX[group]+"/"+tail for group in PREFIX for tail in SUFFIX.values()}
    need(len(names) == len(set(names)) and set(STATIC)|raw_names <= set(names) and relative not in names,
         "complete unique code/reference closure")
    need(len(b["execution_artifacts"]) == len(names)+1
         and set(b["execution_artifacts"]) == set(names)|{relative}, "exact runner repeated inputs")
    for row in b["artifacts"]:
        path = safe(row["path"])
        observed = digest(path)
        writer.emit({"kind": "input_observation", "path": row["path"], "sha256": observed, "bytes": path.stat().st_size})
        need(type(row["bytes"]) is int and row["bytes"] == path.stat().st_size and observed == row["sha256"], "input size/hash")
        if row["path"] in PINS:
            need(observed == PINS[row["path"]], "immutable proof/schema source")
    required_sources = {"control": "research/P131_phase_multinomial.py",
                        "validator": "research/P131_phase_multinomial_validation.py"}
    need(set(b["source_sha256"]) == set(required_sources), "two frozen source identities")
    for role, path in required_sources.items():
        need(digest(safe(path)) == b["source_sha256"][role], "actually used source identity")
    need(Path(sys.executable).absolute() == Path(PYTHON) and sys.version_info[:3] == (3, 11, 15), "persistent Python3.11.15")
    need(sys.dont_write_bytecode and all(os.environ.get(k) == "1" for k in THREADS), "preprocess bytecode/thread environment")
    physical = Path(sys.executable).resolve()
    external = b["external_artifacts"]
    need(any(row["role"] == "physical_interpreter" and Path(row["path"]).resolve() == physical for row in external), "actual interpreter pin")
    for row in external:
        need(Path(row["path"]).is_file() and digest(Path(row["path"])) == row["sha256"], "external pin")
    need(set(b["references"]) == set(SEALS), "exact two sealed reference groups")
    for group, seal in SEALS.items():
        reference = b["references"][group]
        need(reference["original_seal_commit"] == seal, "original pre-reading seal")
        descriptors = reference["files"]
        need(len(descriptors) == 6 and {row["role"] for row in descriptors} == set(SUFFIX), "six unique reference files")
        for row in descriptors:
            expected = PREFIX[group]+"/"+SUFFIX[row["role"]]
            need(row["path"] == expected and row["path"] in names, "fixed reference path")
            path = safe(row["path"])
            sealed = subprocess.check_output(["git", "rev-parse", seal+":"+expected], cwd=ROOT, text=True).strip()
            observed = digest(path, blob=True)
            writer.emit({"kind": "reference_blob", "group": group, **row, "observed_git_blob": observed,
                         "sealed_git_blob": sealed, "observed_sha256": digest(path)})
            need(observed == sealed == row["git_blob_sha1"] and digest(path) == row["sha256"]
                 and type(row["bytes"]) is int and row["bytes"] == path.stat().st_size, "original reference blob/hash/size")
    return b


def occupations(total, modes):
    """Stars-and-bars ordering independent of recursive producer iterators."""
    if modes == 0:
        if total == 0:
            yield ()
        return
    for bars in combinations(range(total+modes-1), modes-1):
        boundaries = (-1,)+bars+(total+modes-1,)
        yield tuple(boundaries[j+1]-boundaries[j]-1 for j in range(modes))


def support(m, k):
    return tuple(n for total in range(k+1) for n in occupations(total, m))


def fixtures():
    return [("V0", [[]]), ("U1", [["1/2"]]),
            ("H2", [["1/4", "1/4"], ["1/4", "-1/4"]]),
            ("D3", [["1/4", 0, 0], [0, "1/4", 0], [0, 0, "1/4"]]),
            ("R3a", [["1/4"]*3]), ("R3b", [["1/8"]*3]),
            ("S3", [["1/8", "1/4", "-1/8"], ["1/4", 0, "1/8"]]),
            ("B4", [["1/4"]*4, ["1/4"]*4]),
            ("D4", [["1/4" if i == j else 0 for j in range(4)] for i in range(4)]),
            ("Z4", [[0]*4, [0]*4]), ("R4", [["1/4"]*4]),
            ("C3", [["1/2", 0, 0], [0, "1/2", 0]]), ("X4", [["1/2"]*4])]


def independent_matrix(rows):
    return [[C(*v) if isinstance(v, (tuple, list)) else C(v) for v in row] for row in rows]


def complex_cases():
    first = (C(F(15, 32)), C(F(7, 32), F(1, 16)), C(F(3, 32)), C(F(7, 32), F(-1, 16)))
    base = [[first[(j-i) % 4] for j in range(4)] for i in range(4)]
    return base, [[value/4 for value in row] for row in base]


def gram(t):
    k = len(t[0])
    return [[sum((row[i].conjugate()*row[j] for row in t), C()) for j in range(k)] for i in range(k)]


def entries(t):
    m, k = len(t), len(t[0])
    zero, g = (0,)*m, gram(t)
    answer = []
    for i in range(k):
        row = []
        for j in range(k):
            terms = {zero: C(int(i == j))-g[i][j]}
            for signal in range(m):
                n = tuple(int(a == signal) for a in range(m))
                terms[n] = t[signal][i].conjugate()*t[signal][j]
            row.append({n: c for n, c in terms.items() if c})
        answer.append(row)
    return answer


def polynomial_product(p, q):
    result = {}
    for a, x in p.items():
        for b, y in q.items():
            n = tuple(i+j for i, j in zip(a, b))
            result[n] = result.get(n, C())+x*y
    return {n: c for n, c in result.items() if c}


def repeated_pgf(table, occupation, modes):
    """per(M[a,a])/a!, with labeled-column subset DP, not phase contexts."""
    indices = [i for i, n in enumerate(occupation) for unused in range(n)]
    k, zero = len(indices), (0,)*modes
    dp = {0: {zero: C(1)}}
    for source in indices:
        next_dp = {}
        for mask, polynomial in dp.items():
            for column, target in enumerate(indices):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                target_polynomial = next_dp.setdefault(new_mask, {})
                for n, c in polynomial_product(polynomial, table[source][target]).items():
                    target_polynomial[n] = target_polynomial.get(n, C())+c
        dp = next_dp
    divisor = prod(factorial(n) for n in occupation)
    return {n: c/divisor for n, c in dp[(1 << k)-1].items() if c}


def tau(k, eta):
    if k == 0:
        return F(0)
    return sum((F(comb(k, l))*eta**l*(1-eta)**(k-l)
                *(1-F(factorial(k), factorial(k-l)*k**l)) for l in range(k+1)), F(0))


def tv(p, q):
    return sum((abs(p[n]-q[n]) for n in p), F(0))/2


def read_references(binding, writer):
    manifests = {}
    for group in SEALS:
        paths = {role: safe(PREFIX[group]+"/"+suffix) for role, suffix in SUFFIX.items()}
        manifest = loads(paths["manifest"].read_text(encoding="utf-8"))
        summary = loads(paths["summary"].read_text(encoding="utf-8"))
        failure = loads(paths["failure"].read_text(encoding="utf-8"))
        writer.emit({"kind": "reference_completion", "group": group, "run": manifest.get("run"),
                     "summary": summary, "failure": failure})
        need(type(manifest["schema_version"]) is int and manifest["schema_version"] == 2
             and manifest["claim_id"] == CLAIMS[group] and manifest["run"]["status"] == "completed"
             and type(manifest["run"]["exit_status"]) is int and manifest["run"]["exit_status"] == 0,
             "successful original reference runner")
        source_path = "research/P96_column_loss_validation.py" if group == "P96" else "research/P107_symbolic_filter_validation.py"
        input_rows = manifest["input_artifacts"]
        need(len({row["path"] for row in input_rows}) == len(input_rows), "unique producer input descriptors")
        source_rows = [row for row in input_rows if row["path"] == source_path]
        need(len(source_rows) == 1 and source_rows[0]["sha256"] == PINS[source_path]
             and source_rows[0]["sha256_after"] == PINS[source_path], "actually bound immutable producer source")
        if group == "P96":
            need(summary["status"] == "FINITE_VALIDATION_PASS" and failure == {"status": "NO_FAILURE"}, "P96 reference completion")
        else:
            need(summary["ENGINE_PASS"] is True and summary["NOT_RUN"] == [] and summary["FAILED_TASK"] == []
                 and failure is None, "P107 engine completion, independent of sign verdict")
        outputs = manifest["outputs"]
        sealed = {row["path"]: row for row in binding["references"][group]["files"] if row["role"] != "manifest"}
        need(len(outputs) == 5 and len({row["path"] for row in outputs}) == 5
             and {row["path"] for row in outputs} == set(sealed), "all five original payload/log outputs")
        need(all(row["sha256"] == sealed[row["path"]]["sha256"] for row in outputs), "manifest sealed output hashes")
        need(set(manifest["declared_results"]) == {PREFIX[group]+"/"+SUFFIX[r] for r in ("records", "summary", "failure")}
             and len(manifest["declared_results"]) == 3, "three original declared results")
        manifests[group] = paths
    p96, count = {}, 0
    for line in manifests["P96"]["records"].open(encoding="utf-8"):
        row = loads(line)
        if row.get("kind") != "exact_raw":
            continue
        name, n = row["case"], tuple(exact_int(v) for v in row["signal"])
        need(n not in p96.setdefault(name, {}), "duplicate P96 signal")
        p96[name][n] = exact_fraction(row["p"])
        count += 1
    need(count == 167 and set(p96) == {name for name, rows in fixtures()}, "all13 P96 cases/167 bins")
    base_support, coefficients = set(support(4, 4)), {}
    for line in manifests["P107"]["records"].open(encoding="utf-8"):
        row = loads(line)
        if row.get("kind") != "coefficient":
            continue
        n = tuple(exact_int(v) for v in row["occupation"])
        powers = tuple(exact_int(v) for v in row["powers"])
        need(n in base_support and len(powers) == 2 and all(0 <= v <= 8 for v in powers), "registered P107 coefficient")
        need(type(row["denominator"]) is int and row["denominator"] == 65536, "P107 common denominator")
        values = tuple(exact_int(v) for v in row["B"])
        moment = tuple(exact_int(v) for v in row["B_moment"])
        need(len(values) == len(moment) == 2 and values == moment and values[1] == 0, "independent exact P107 B numerator")
        key = n, powers
        need(key not in coefficients, "duplicate P107 coefficient")
        coefficients[key] = F(values[0], 65536)
    need(len(coefficients) == 5670 and all((n, (i, j)) in coefficients for n in base_support for i in range(9) for j in range(9)), "complete70x81 P107 coefficients")
    base = {n: sum((coefficients[(n, (i, j))]*F(1, 2)**i*F(1, 4)**j
                   for i in range(9) for j in range(9)), F(0)) for n in base_support}
    # Independent common signal thinning, intensity1/16, no Fock truncation.
    attenuation = {n: F(0) for n in base_support}
    for source, probability in base.items():
        for target in base_support:
            if all(a <= b for a, b in zip(target, source)):
                attenuation[target] += probability*prod(F(comb(b, a))*F(1, 16)**a*F(15, 16)**(b-a)
                                                        for a, b in zip(target, source))
    return p96 | {"G4": base, "G4atten": attenuation}


def run(writer, binding, state, guard):
    sys.path.insert(0, str(ROOT/"research"))
    import P131_phase_multinomial as control
    need(Path(control.__file__).resolve() == safe("research/P131_phase_multinomial.py"), "actual control module")
    state.update(checks=0, scientific_failures=0, contexts=0, bins=0, input_pgfs=0, hand_groups=0, completed=[])
    def check(ok, label, details):
        state["checks"] += 1
        if not ok:
            state["scientific_failures"] += 1
            writer.emit({"kind": "check_failure", "label": label, "details": details})
            state.setdefault("first_scientific_failure", {"row": writer.rows, "label": label})
    def literal_case(label, rows, tickets, expected):
        iterator, calls = iter(tickets), []
        def bits(width):
            value = next(iterator)
            calls.append([width, value])
            return value
        model = control.build_model(rows)
        observed, receipt = control.sample_counts(model, bits)
        sentinel = object()
        exhausted = next(iterator, sentinel) is sentinel
        writer.emit({"kind": "literal_boundary", "case": label, "observed": observed,
                     "expected": expected, "receipt": receipt, "fully_consumed": exhausted})
        check(observed == expected and exhausted and len(calls) == 2*model.k
              and [width for width, value in calls] == [model.phase_bits]*model.k+[model.categorical_bits]*model.k
              and receipt["bits"] == model.bit_count, "literal bit/CDF boundary", label)
        state["hand_groups"] += 1
    state["phase"] = "LITERAL_HANDS"
    literal_case("vacuum", [[]], [], (0,))
    for label, tickets, expected in (("unary-first", (0, 0), (1,)), ("unary-last-signal", (1, 511), (1,)),
                                     ("unary-first-loss", (0, 512), (0,)), ("unary-last-loss", (1, 2047), (0,))):
        literal_case(label, [["1/2"]], tickets, expected)
    literal_case("H2-first", [["1/4", "1/4"], ["1/4", "-1/4"]], (0, 0, 1023, 1024), (1, 0))
    literal_case("H2-second", [["1/4", "1/4"], ["1/4", "-1/4"]], (0, 2, 0, 8191), (0, 1))
    doubled = repeated_pgf(entries(independent_matrix([["1/2", 0]])), (2, 0), 1)
    writer.emit({"kind": "repeated_input_hand", "occupation": [2, 0], "law": [[n, c] for n, c in sorted(doubled.items())]})
    check(doubled == {(0,): C(F(9, 16)), (1,): C(F(3, 8)), (2,): C(F(1, 16))}, "double-input Fock factorial", doubled)
    state["hand_groups"] += 1
    for label, rows, exception in (("unsupported-K8", [[0]*8], control.UnsupportedScope),
                                   ("noncontraction", [[2]], ValueError), ("zero-pivot-offdiagonal", [[1, 1]], ValueError)):
        try:
            control.build_model(rows)
            observed, correct = "NO_REJECTION", False
        except Exception as error:
            observed, correct = repr(error), isinstance(error, exception)
        writer.emit({"kind": "literal_rejection", "case": label, "observed": observed, "bits_read": 0})
        check(correct, "explicit scope/contraction rejection", label)
        state["hand_groups"] += 1
    model = control.build_model([["1/2"]])
    try:
        control.sample_counts(model, lambda width: True)
        invalid_return = "NO_REJECTION"
    except ValueError as error:
        invalid_return = repr(error)
    writer.emit({"kind": "invalid_bit_return", "observed": invalid_return})
    check(invalid_return != "NO_REJECTION", "bool is not a fair-bit integer", invalid_return)
    state["hand_groups"] += 1
    check(state["hand_groups"] == 12, "complete twelve literal groups", state["hand_groups"])
    state["phase"] = "SEALED_REFERENCE_READ"
    references = read_references(binding, writer)
    cases = [(name, independent_matrix(rows)) for name, rows in fixtures()]
    base, attenuated = complex_cases()
    cases += [("G4", base), ("G4atten", attenuated)]
    for name, t in cases:
        guard()
        state.update(case=name, phase="CASE_SETUP", context=None, input_occupation=None)
        m, k = len(t), len(t[0])
        states, g = support(m, k), gram(t)
        if name in ("G4", "G4atten"):
            eta = F(1) if name == "G4" else F(1, 16)
        else:
            trace = sum((g[i][i].r for i in range(k)), F(0))
            need(all(v.i == 0 for row in g for v in row), "real P96 Gram for rational Gershgorin")
            row_bound = max((sum((abs(v.r) for v in row), F(0)) for row in g), default=F(0))
            eta = min(trace, row_bound)
        rows = [[(value.r, value.i) for value in row] for row in t]
        writer.emit({"kind": "case_operands", "case": name, "T": t, "gram": g, "eta": eta,
                     "strict_P129": eta < 1, "P96_original_trace_counterexample": name == "X4"})
        model = control.build_model(rows)
        pivots = control.contraction_certificate(model.t, eta)
        writer.emit({"kind": "case_profile", "case": name, "roots": model.roots, "root_proof": model.root_proof,
                     "eta_pivots": pivots, "D": model.denominator, "phase_bits": model.phase_bits,
                     "categorical_bits": model.categorical_bits, "bits_per_sample": model.bit_count})
        if name in ("G4", "G4atten"):
            roots = (C(1), C(0, -1), C(-1), C(0, 1))
            values = (F(1), F(1, 2), F(1, 8), F(1, 4))
            factor = F(1) if name == "G4" else F(1, 4)
            reconstructed = [[sum((roots[((i-j)*r) % 4]*values[r]*factor/4 for r in range(4)), C())
                              for j in range(4)] for i in range(4)]
            writer.emit({"kind": "complex_spectrum_identity", "case": name, "reconstructed": reconstructed,
                         "spectral_amplitudes": [v*factor for v in values]})
            check(t == reconstructed, "literal circulant/Fourier indexing", name)
            fourier_gram = [[sum((roots[(-r*i) % 4]*roots[(r*j) % 4]/4 for r in range(4)), C())
                             for j in range(4)] for i in range(4)]
            writer.emit({"kind": "fourier_gram", "case": name, "observed": fourier_gram, "eta": eta})
            check(fourier_gram == [[C(int(i == j)) for j in range(4)] for i in range(4)]
                  and max((v*factor)**2 for v in values) == eta, "exact spectral norm certificate", name)
        state["phase"] = "EXACT_IDEAL_PGF"
        table, ideal = entries(t), {n: C() for n in states}
        for a in occupations(k, k):
            guard()
            state["input_occupation"] = a
            pgf = repeated_pgf(table, a, m)
            mass = sum(pgf.values(), C())
            weight = F(factorial(k), k**k*prod(factorial(v) for v in a)) if k else F(1)
            writer.emit({"kind": "input_pgf", "case": name, "input_occupation": a, "mixture_weight": weight,
                         "mass": mass, "law": [[n, c] for n, c in sorted(pgf.items())]})
            check(mass == C(1) and all(c.i == 0 and c.r >= 0 for c in pgf.values()), "normalized repeated-input PGF", [name, a])
            for n, c in pgf.items():
                need(n in ideal, "oracle occupation outside registered support")
                ideal[n] = ideal[n]+c*weight
            state["input_pgfs"] += 1
        ideal_real = {n: value.r for n, value in ideal.items()}
        state["phase"] = "ALL_FINITE_CONTEXTS"
        accumulators = {n: 0 for n in states}
        terms = [(n, n+(k-sum(n),), factorial(k)//(factorial(k-sum(n))*prod(factorial(v) for v in n))) for n in states]
        contexts = 0
        for labels in product(range(len(model.roots)), repeat=k):
            guard()
            state["context"] = labels
            weights = control.context_weights(model, labels)
            writer.emit({"kind": "context", "case": name, "phase": labels, "weights": weights})
            check(len(weights) == m+1 and all(type(w) is int and w >= 0 for w in weights)
                  and sum(weights) == model.denominator, "complete exact context weights", [name, labels, weights])
            powers = [[w**exponent for exponent in range(k+1)] for w in weights]
            for n, exponents, coefficient in terms:
                accumulators[n] += coefficient*prod(powers[j][count] for j, count in enumerate(exponents))
            contexts += 1
            state["contexts"] += 1
        finite = {n: F(value, len(model.roots)**k*model.denominator**k) for n, value in accumulators.items()}
        reference = references[name]
        need(set(reference) == set(states), "complete bound reference support: " + name)
        for n in states:
            writer.emit({"kind": "output_bin", "case": name, "signal": n, "loss": k-sum(n),
                         "B_reference": reference[n], "Q_ideal": ideal[n], "Q_finite": finite[n]})
            check(ideal[n].i == 0 and ideal[n].r >= 0 and finite[n] >= 0 and reference[n] >= 0,
                  "real nonnegative full output bin", [name, n, ideal[n], finite[n], reference[n]])
            state["bins"] += 1
        error, bound = tv(ideal_real, finite), tau(k, eta)
        ideal_error, finite_error = tv(reference, ideal_real), tv(reference, finite)
        report = {"kind": "case_result", "case": name, "strict_P129": eta < 1, "eta": eta, "tau": bound,
                  "birthday_bound": min(F(1), F(k-1, 2)*eta**2) if k else F(0), "epsilon": control.EPSILON,
                  "TV_finite_ideal": error, "TV_B_ideal": ideal_error, "TV_B_finite": finite_error,
                  "masses": [sum(reference.values()), sum(ideal_real.values()), sum(finite.values())], "contexts": contexts}
        writer.emit(report)
        check(report["masses"] == [F(1)]*3, "three exact normalizations", report)
        check(error <= control.EPSILON, "finite-bit additive error", report)
        check(ideal_error <= bound and finite_error <= bound+control.EPSILON, "raw-loss TV bounds", report)
        check(bound <= report["birthday_bound"], "birthday bound including eta1 diagnostic", report)
        for j in range(m):
            target = sum((value.r*value.r+value.i*value.i for value in t[j]), F(0))
            means = [sum((law[n]*n[j] for n in states), F(0)) for law in (reference, ideal_real, finite)]
            writer.emit({"kind": "mean", "case": name, "signal_row": j, "expected": target, "B_ideal_finite": means})
            check(means[0] == means[1] == target and abs(means[2]-target) <= k*control.EPSILON,
                  "ideal means exact/finite means approximate", [name, j, means, target])
        state["completed"].append(name)
    check((len(state["completed"]), state["contexts"], state["bins"], state["input_pgfs"]) == (15, 29011, 307, 300),
          "complete predeclared population", state.copy())
    return references


def main(argv=None):
    resource.setrlimit(resource.RLIMIT_FSIZE, (CAP, CAP))
    resource.setrlimit(resource.RLIMIT_CPU, (CPU, CPU))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", required=True)
    args = parser.parse_args(argv)
    start = time.process_time(), time.perf_counter()
    writer, failure = None, None
    state = {"phase": "PROVENANCE", "positive_accepted": False, "native_calls": 0, "RNG_draws": 0,
             "random_bit_source": "NONE: exhaustive contexts and literal boundary vectors only"}
    try:
        writer = Evidence()
        state["active_binding_observed_sha256"] = digest(safe(args.binding))
        binding = authorize(args.binding, writer)
        writer.emit({"kind": "provenance", "Python": sys.version, "executable": sys.executable,
                     "environment": {key: os.environ.get(key) for key in THREADS}, "FSIZE": resource.getrlimit(resource.RLIMIT_FSIZE),
                     "CPU_limit": resource.getrlimit(resource.RLIMIT_CPU), "limits": {"CPU": CPU, "wall": WALL, "science": CAP, "summary": FINAL_CAP}})
        def guard():
            need(time.process_time()-start[0] <= CPU and time.perf_counter()-start[1] <= WALL, "fixed CPU/wall allowance")
        run(writer, binding, state, guard)
        for row in binding["artifacts"]:
            need(digest(safe(row["path"])) == row["sha256"], "input unchanged after exact qualification")
        for row in binding["external_artifacts"]:
            need(digest(Path(row["path"])) == row["sha256"], "external pin unchanged")
        need(digest(safe(args.binding)) == state["active_binding_observed_sha256"], "active binding unchanged")
        guard()
        state["phase"] = "COMPLETE"
        state["status"] = "FINITE_VALIDATION_PASS" if state["scientific_failures"] == 0 else "SCIENTIFIC_COMPARISON_FAILURE"
    except Exception as error:
        failure = {"type": type(error).__name__, "repr": repr(error), "traceback": traceback.format_exc(), "prefix": dict(state)}
        state["status"] = "INCONCLUSIVE_FIRST_FAILURE"
        if writer is None:
            sys.stderr.write(json.dumps(clean(failure), allow_nan=False)+"\n")
    finally:
        if writer is not None:
            state["runtime"] = {"cpu": time.process_time()-start[0], "wall": time.perf_counter()-start[1]}
            state["records"] = writer.rows
            names = [name for name, rows in fixtures()]+["G4", "G4atten"]
            state["NOT_RUN"] = [name for name in names if name not in state.get("completed", []) and name != state.get("case")]
            state["PARTIAL_CASE"] = state.get("case") if state.get("case") not in state.get("completed", []) else None
            writer.finish(state, failure or {"status": "NO_EXCEPTION", "scientific_failures": state.get("scientific_failures")})
    return int(failure is not None or state.get("scientific_failures", 1) != 0)


if __name__ == "__main__":
    raise SystemExit(main())
