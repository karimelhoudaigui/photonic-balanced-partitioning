"""P82a frozen prospective DEV screen. Importing this module runs no experiment.

Scientific dependencies are loaded only at an explicitly invoked CLI boundary.
The public scalar functions also support deterministic, scripted qualification.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from fractions import Fraction
import hashlib
import importlib.metadata
import importlib.util
import itertools
import json
import math
import numbers
import os
from pathlib import Path
import platform
import sys
import time


SPEC_SHA256 = "8598bd4220d1caadb20aed68601e92b4bba85db787bfe71b83efb6376151c838"
PERSISTENT_PYTHON = "/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python"
P43_SHA256 = "b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777"
P50_SHA256 = "6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86"
FAST_MODES = ("FAST_RANDOM", "FAST_SPECTRAL")
CUSTOM_MODES = ("RECIPIENT_FRONTIER", "PHASE_HYPERPLANE",
                "CONTINUED_DESCENT", "MULTISWAP")
N, K = 16, 8
MAX_BYTES, RESERVE = 32 * 1024 * 1024, 1024 * 1024
MAX_WORK, MAX_TRACE = 10000, 10001
ROOTS = (1 + 0j, 1j, -1 + 0j, -1j)
STREAM_NAMES = ("B_ER.jsonl", "B_RR.jsonl", "paid_ledger.jsonl", "controls.jsonl")
RESULT_NAMES = ("metadata.json", "graphs.json", *STREAM_NAMES,
                "summary.json", "failure.json")


class RetainedFailure(RuntimeError):
    def __init__(self, message, payload=None):
        super().__init__(message)
        self.evidence = {} if payload is None else payload
        self.payload = self.evidence


class ResourceFailure(RetainedFailure):
    pass


class SystemClock:
    def now(self):
        return time.process_time(), time.perf_counter()


def finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise RetainedFailure("nonfinite " + name, {"observed_repr": repr(value)})
    return value


def serial(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, complex):
        return {"real": serial(value.real), "imag": serial(value.imag)}
    if isinstance(value, float):
        return value if math.isfinite(value) else {"nonfinite_repr": repr(value)}
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, dict):
        return {str(key): serial(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    if hasattr(value, "tolist"):
        return serial(value.tolist())
    if hasattr(value, "item"):
        return serial(value.item())
    return {"unsupported_repr": repr(value)[:4096]}


def encoded(value):
    return (json.dumps(serial(value), ensure_ascii=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


class EvidenceWriter:
    """Exclusive append-only streams with a separate compact failure reserve."""
    def __init__(self, output, max_bytes=MAX_BYTES, reserve=RESERVE):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=False)
        self.max_bytes, self.reserve = int(max_bytes), int(reserve)
        if not 0 < self.reserve < self.max_bytes:
            raise ValueError("invalid output reserve")
        self.bytes = 0
        self.serialization_and_io_cpu = self.serialization_and_io_wall = 0.0
        self.streams = {}
        for name in STREAM_NAMES:
            self.streams[name] = (self.output / name).open("xb")

    def _room(self, size, final=False):
        limit = self.max_bytes if final else self.max_bytes - self.reserve
        if self.bytes + size > limit:
            raise RetainedFailure("scientific output cap", {
                "written_bytes": self.bytes, "next_bytes": size, "limit": limit})

    def append(self, name, record):
        begin = SystemClock().now()
        name = name if name.endswith(".jsonl") else name+".jsonl"
        data = encoded(record)
        self._room(len(data))
        stream = self.streams[name]
        stream.write(data)
        stream.flush()
        self.bytes += len(data)
        end = SystemClock().now()
        self.serialization_and_io_cpu += end[0]-begin[0]
        self.serialization_and_io_wall += end[1]-begin[1]

    def single(self, name, record, final=False):
        begin = SystemClock().now()
        name = name if name.endswith(".json") else name+".json"
        data = encoded(record)
        self._room(len(data), final)
        with (self.output / name).open("xb") as stream:
            stream.write(data)
            stream.flush()
        self.bytes += len(data)
        end = SystemClock().now()
        self.serialization_and_io_cpu += end[0]-begin[0]
        self.serialization_and_io_wall += end[1]-begin[1]

    def finish(self, summary, failure):
        """Pre-size both final objects before writing any scientific verdict."""
        records = {"summary.json": summary, "failure.json": failure}
        for name in ("metadata.json", "graphs.json"):
            if not (self.output / name).exists():
                records[name] = {"status": "NOT_RUN", "reason": "first_failure"}
        required = sum(len(encoded(row)) for row in records.values())
        if self.bytes + required > self.max_bytes:
            failure = {"stage": "final_output", "error": "final reserve exhausted",
                       "earlier_failure": serial(failure)}
            summary = {"status": "INCONCLUSIVE_FIRST_FAILURE",
                       "positive_accepted": False, "failure": failure["error"],
                       "completed_cases": summary.get("completed_cases", [])}
            records["summary.json"], records["failure.json"] = summary, failure
            required = sum(len(encoded(row)) for row in records.values())
            if self.bytes + required > self.max_bytes:
                records["failure.json"] = {"stage": "final_output",
                                          "error": "final reserve exhausted"}
                records["summary.json"] = {
                    "status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False}
        self._room(sum(len(encoded(row)) for row in records.values()), final=True)
        for name, row in records.items():
            self.single(name, row, final=True)
        return records["summary.json"]

    def close(self):
        for stream in self.streams.values():
            stream.close()


class MemoryWriter:
    """Scripted qualification sink; it does not create files or random streams."""
    def __init__(self):
        self.records = {name: [] for name in STREAM_NAMES}
        self.singles = {}

    def append(self, name, record):
        name = name if name.endswith(".jsonl") else name+".jsonl"
        self.records[name].append(serial(record))

    def single(self, name, record, final=False):
        name = name if name.endswith(".json") else name+".json"
        if name in self.singles:
            raise RetainedFailure("duplicate single result", {"name": name})
        self.singles[name] = serial(record)

    def finish(self, summary, failure):
        self.singles["summary.json"] = serial(summary)
        self.singles["failure.json"] = serial(failure)
        return summary


def profile(d, rho=Fraction(1), eta=Fraction(1, 2)):
    rho, eta = Fraction(rho), Fraction(eta)
    if d < 2 or rho <= 0 or not 0 <= eta < 1:
        raise RetainedFailure("invalid profile")
    odds = [rho * (1 + eta * Fraction(2*j-d-1, d-1))
            for j in range(1, d+1)]
    one = [item / (1 + item) for item in odds]
    return {"odds": odds, "probabilities": one + one, "rho": rho, "eta": eta}


def fourier(d):
    if d == 2:
        root = math.sqrt(0.5)
        return [[root + 0j, root + 0j], [root + 0j, -root + 0j]]
    if d == 4:
        return [[ROOTS[(r*j) % 4] / 2 for j in range(4)] for r in range(4)]
    raise RetainedFailure("only frozen d2/d4 Fourier populations are allowed")


def receiver_cache(d, rho=Fraction(1), eta=Fraction(1, 2)):
    out = profile(d, rho, eta)
    f = fourier(d)
    if Fraction(eta) == 0:
        a = [[complex(float(rho)) if r == s else 0j for s in range(d)]
             for r in range(d)]
    else:
        a = [[sum(f[r][j] * float(out["odds"][j]) * f[s][j].conjugate()
                  for j in range(d)) for s in range(d)] for r in range(d)]
    return {**out, "profile": out, "F": f, "A": a}


def compile_receiver(graph, source_order, target_order, phase_ids,
                     rho=Fraction(1), eta=Fraction(1, 2), sweeps=2, cache=None):
    k = len(source_order)
    if k % 2 or len(target_order) != k or len(phase_ids) != k // 2:
        raise RetainedFailure("compiler dimensions")
    d = k // 2
    cache = receiver_cache(d, rho, eta) if cache is None else cache
    f, a = cache["F"], cache["A"]
    analytic_zero = Fraction(eta) == 0
    phases = []
    for item in phase_ids:
        if not isinstance(item, numbers.Integral) or isinstance(item, bool) or not 0 <= item < 4:
            raise RetainedFailure("invalid initial phase ID")
        phases.append(ROOTS[int(item)])
    q = [[0 for _ in range(d)] for _ in range(d)]
    coupling = [[0.0 for _ in range(d)] for _ in range(d)]
    for r in range(d):
        for s in range(d):
            if r != s:
                q[r][s] = (int(graph[target_order[r]][target_order[s]])
                           + int(graph[target_order[d+r]][target_order[d+s]])
                           - int(graph[target_order[r]][target_order[d+s]])
                           - int(graph[target_order[d+r]][target_order[s]]))
                if not analytic_zero:
                    coupling[r][s] = q[r][s] * abs(a[r][s]) ** 2
    trace = []
    for sweep in range(int(sweeps)):
        for r in range(d):
            h = 0j if analytic_zero else sum(coupling[r][s] * phases[s]
                                             for s in range(d) if s != r)
            if not math.isfinite(h.real) or not math.isfinite(h.imag):
                raise RetainedFailure("nonfinite phase field", {"H_repr": repr(h)})
            before = phases[r]
            if h != 0j:
                angle = math.atan2(h.imag, h.real)
                phases[r] = complex(math.cos(angle), math.sin(angle))
            trace.append({"sweep": sweep, "coordinate": r, "H": h,
                          "before": before, "after": phases[r]})
    factor = math.sqrt(0.5)
    w = []
    for sign in (1, -1):
        for r in range(d):
            w.append([factor * f[r][j] for j in range(d)]
                     + [sign * factor * phases[r] * f[r][j] for j in range(d)])
    guards = validate_receiver(w, cache["probabilities"])
    return {"W": w, "J": coupling, "Q": q, "A": a, "phases": phases,
            "phase_trace": trace, "guards": guards, "analytic_uniform_null": analytic_zero}


def validate_receiver(w, probabilities, tolerance=3e-12):
    k = len(w)
    if k == 0 or len(probabilities) != k or any(len(row) != k for row in w):
        raise RetainedFailure("receiver/frame dimensions")
    for row in w:
        for value in row:
            if not math.isfinite(complex(value).real) or not math.isfinite(complex(value).imag):
                raise RetainedFailure("nonfinite receiver", {"value_repr": repr(value)})
    gram_error = max(abs(sum(complex(w[r][i]).conjugate()*w[r][j]
                             for r in range(k)) - int(i == j))
                     for i in range(k) for j in range(k))
    flat_error = max(abs(abs(value)**2 - 1/k) for row in w for value in row)
    p = [float(value) for value in probabilities]
    if any(not 0 < value < 1 or not math.isfinite(value) for value in p):
        raise RetainedFailure("invalid splitter probability")
    frame_error = max(abs((1-p[i])*int(i == j)
                          + math.sqrt(p[i]*p[j])*sum(
                              complex(w[r][i]).conjugate()*w[r][j] for r in range(k))
                          - int(i == j)) for i in range(k) for j in range(k))
    if max(gram_error, flat_error, frame_error) > tolerance:
        raise RetainedFailure("receiver/frame invariant failure", {
            "gram_error": gram_error, "flat_probability_error": flat_error,
            "occupied_frame_error": frame_error, "tolerance": tolerance})
    return {"gram_error": gram_error, "flat_probability_error": flat_error,
            "occupied_frame_error": frame_error}


def validated_graph(graph):
    n = len(graph)
    if n < 2 or n % 2 or any(len(row) != n for row in graph):
        raise RetainedFailure("invalid graph dimensions")
    out = []
    for row in graph:
        converted = []
        for item in row:
            if isinstance(item, bool) or not isinstance(item, numbers.Integral) or item < 0:
                raise RetainedFailure("graph weights must be nonnegative integers")
            converted.append(int(item))
        out.append(converted)
    if any(out[i][i] != 0 for i in range(n)) or any(
            out[i][j] != out[j][i] for i in range(n) for j in range(n)):
        raise RetainedFailure("graph symmetry/diagonal")
    if max(max(row) for row in out) > (2**63-1) // (4*n*n):
        raise RetainedFailure("graph integer overflow bound")
    return out


def checked_subset(subset, n):
    raw = list(subset)
    if any(isinstance(value, bool) or not isinstance(value, numbers.Integral) for value in raw):
        raise RetainedFailure("noninteger subset")
    values = tuple(int(value) for value in raw)
    if len(values) != n//2 or len(set(values)) != len(values) or not all(
            0 <= value < n for value in values):
        raise RetainedFailure("invalid feasible subset", {"subset": list(values)})
    return values


def canonical(subset, n, rank):
    values = checked_subset(subset, n)
    if len(rank) != n or sorted(int(value) for value in rank) != list(range(n)):
        raise RetainedFailure("invalid rank permutation")
    pivot = min(range(n), key=lambda vertex: rank[vertex])
    inside = set(values)
    return tuple(sorted(inside if pivot in inside else set(range(n))-inside))


def cut(graph, subset):
    inside = set(checked_subset(subset, len(graph)))
    return sum(int(graph[i][j]) for i in inside
               for j in range(len(graph)) if j not in inside)


def pack_mask(subset, n):
    data = bytearray((n+7)//8)
    for vertex in checked_subset(subset, n):
        data[vertex//8] |= 1 << (vertex % 8)
    return bytes(data)


def unpack_mask(data, n):
    data = bytes.fromhex(data) if isinstance(data, str) else bytes(data)
    if len(data) != (n+7)//8 or (n % 8 and data[-1] >> (n % 8)):
        raise RetainedFailure("invalid packed mask")
    return checked_subset([i for i in range(n) if data[i//8] & (1 << (i % 8))], n)


def all_swap_candidates(graph, subset, rank, base_cut):
    n = len(graph)
    current = canonical(subset, n, rank)
    chosen = set(current)
    inside = sorted(chosen, key=lambda value: rank[value])
    outside = sorted(set(range(n))-chosen, key=lambda value: rank[value])
    degree = [sum(map(int, row)) for row in graph]
    ell = [degree[v] - 2*sum(int(graph[v][u]) for u in chosen) for v in range(n)]
    rows = []
    for removed in inside:
        for added in outside:
            delta = ell[added] - ell[removed] + 2*int(graph[removed][added])
            candidate = canonical((chosen-{removed}) | {added}, n, rank)
            rows.append({"subset": candidate, "cut": int(base_cut)+delta,
                         "removed": removed, "added": added, "delta": delta})
    return rows


def bounded_descent(graph, subset, rank, max_scans, score, initial_cut=None):
    n = len(graph)
    current = canonical(subset, n, rank)
    value = int(score(current)) if initial_cut is None else int(initial_cut)
    scans, local = 0, False
    for _ in range(int(max_scans)):
        if hasattr(score, "scan"):
            rows = score.scan(current, rank, value)
        else:
            rows = []
            chosen = set(current)
            for removed in sorted(chosen, key=lambda v: rank[v]):
                for added in sorted(set(range(n))-chosen, key=lambda v: rank[v]):
                    candidate = canonical((chosen-{removed}) | {added}, n, rank)
                    rows.append({"subset": candidate, "cut": int(score(candidate)),
                                 "removed": removed, "added": added})
        if len(rows) != (n//2)**2:
            raise RetainedFailure("incomplete descent scan")
        best = min(rows, key=lambda row: (
            row["cut"], rank[row["removed"]], rank[row["added"]]))
        scans += 1
        if best["cut"] >= value:
            local = True
            break
        current = canonical(best["subset"], n, rank)
        value = int(best["cut"])
    return {"subset": current, "cut": value, "scans": scans, "local_optimum": local}


def decode_counts(source_order, target_order, removed_ports, y, chooser):
    source_order, target_order = list(source_order), list(target_order)
    k = len(source_order)
    if len(target_order) != k or sorted(source_order+target_order) != list(range(2*k)):
        raise RetainedFailure("port mapping is not a partition")
    if any(isinstance(value, bool) or not isinstance(value, numbers.Integral) for value in removed_ports):
        raise RetainedFailure("noninteger receiver input")
    removed = tuple(int(value) for value in removed_ports)
    if len(set(removed)) != len(removed) or any(not 0 <= value < k for value in removed):
        raise RetainedFailure("invalid receiver input ports")
    if len(y) != k or any(isinstance(value, bool) or not isinstance(value, numbers.Integral)
                          or value < 0 for value in y) or sum(y) != len(removed):
        raise RetainedFailure("invalid receiver counts", {
            "removed_ports": removed, "count_repr": repr(y)[:4096]})
    y = [int(value) for value in y]
    support = [target_order[j] for j, value in enumerate(y) if value]
    remaining = sorted(set(target_order)-set(support))
    need = len(removed)-len(support)
    used = 0 < need < len(remaining)
    repair = list(chooser(remaining, need)) if used else remaining if need else []
    if len(repair) != need or len(set(repair)) != need or not set(repair) <= set(remaining):
        raise RetainedFailure("invalid repair subset")
    kept = [int(i not in removed) for i in range(k)]
    full = kept+y
    vertex = [0]*(2*k)
    for j, value in enumerate(kept):
        vertex[source_order[j]] = value
    for j, value in enumerate(y):
        vertex[target_order[j]] = value
    subset = sorted([source_order[j] for j in range(k) if j not in removed]
                    + support + repair)
    checked_subset(subset, 2*k)
    return {"subset": tuple(subset), "full_counts": full, "vertex_counts": vertex,
            "R": [source_order[j] for j in removed], "r": len(removed),
            "h": len(support), "repair": repair, "repair_rng_used": used}


def duration_difference(outer_record, reported_record, event_id):
    if (outer_record.get("kind") != "OBSERVED_SPAN" or not outer_record.get("id")
            or not outer_record.get("case")
            or reported_record.get("kind") != "REPORTED_DURATION"
            or reported_record.get("paid") is not False or not reported_record.get("id")
            or reported_record.get("case") != outer_record.get("case")
            or any(reported_record.get(key) is not None for key in
                   ("cpu_seconds", "start_cpu", "end_cpu", "start_wall", "end_wall"))):
        raise RetainedFailure("invalid typed reported factory duration", {"reported": reported_record})
    outer = finite(outer_record["wall_seconds"], "factory outer WALL")
    reported = finite(reported_record["wall_seconds"], "factory reported WALL")
    if not 0 <= reported <= outer:
        raise RetainedFailure("invalid nested factory duration", {
            "outer": outer_record, "reported_wall": reported})
    return {"id": event_id, "kind": "DURATION_DIFF",
            "label": "factory_prefix_plus_return_residual",
            "wall_seconds": outer-reported, "cpu_seconds": None,
            "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
            "outer_ref": outer_record["id"], "reported_ref": reported_record["id"],
            "reported_setup_wall_seconds": reported,
            "formula": "factory_outer_wall - setup_reported_wall"}


def select_dual_checkpoint(trace, adapter_cpu, adapter_wall, grant, n):
    ac, aw, g = (finite(adapter_cpu, "adapter CPU"),
                 finite(adapter_wall, "adapter WALL"), finite(grant, "grant"))
    if min(ac, aw, g) < 0:
        raise RetainedFailure("negative adapter/grant")
    names = ("cpu_seconds", "wall_seconds", "best_cut",
             "best_subset_packbits_little", "stage", "proposal_count")
    if any(name not in trace for name in names):
        raise RetainedFailure("missing archived checkpoint fields")
    count = len(trace[names[0]])
    if count > MAX_TRACE or any(len(trace[name]) != count for name in names):
        raise RetainedFailure("invalid archived checkpoint lengths")
    previous = (-1.0, -1.0, -1)
    previous_cut = None
    selected = None
    for j in range(count):
        cpu = finite(trace["cpu_seconds"][j], "checkpoint CPU")
        wall = finite(trace["wall_seconds"][j], "checkpoint WALL")
        raw_work = trace["proposal_count"][j]
        if isinstance(raw_work, bool) or not isinstance(raw_work, numbers.Integral):
            raise RetainedFailure("noninteger checkpoint work")
        work = int(raw_work)
        value = trace["best_cut"][j]
        if isinstance(value, bool) or not isinstance(value, numbers.Integral) or value < 0:
            raise RetainedFailure("invalid archived cut")
        if previous_cut is not None and value > previous_cut:
            raise RetainedFailure("nonmonotone archived best cut")
        previous_cut = value
        raw_mask = list(trace["best_subset_packbits_little"][j])
        if any(isinstance(item, bool) or not isinstance(item, numbers.Integral)
               or not 0 <= item <= 255 for item in raw_mask):
            raise RetainedFailure("invalid archived mask byte")
        mask = bytes(raw_mask)
        if len(mask) != (n+7)//8 or (n % 8 and mask[-1] >> (n % 8)):
            raise RetainedFailure("invalid archived mask format")
        if sum(value.bit_count() for value in mask) != n//2:
            raise RetainedFailure("unbalanced archived mask")
        if cpu < 0 or wall < 0 or work < 0 or work > MAX_WORK:
            raise RetainedFailure("negative checkpoint")
        if cpu < previous[0] or wall < previous[1] or work < previous[2]:
            raise RetainedFailure("nonmonotone checkpoint clocks/work")
        previous = (cpu, wall, work)
        if ac+cpu <= g and aw+wall <= g:
            selected = {"index": j, "cut": int(value), "mask_hex": mask.hex(),
                        "cpu_seconds": cpu, "wall_seconds": wall,
                        "total_cpu": ac+cpu, "total_wall": aw+wall,
                        "provenance": "archived_preclock_RAM_prefix"}
    return selected


def call_boundary_difference(outer_cpu, outer_wall, adapter_cpu, adapter_wall,
                             helper_cpu, helper_wall):
    values = [finite(value, name) for value, name in zip(
        (outer_cpu, outer_wall, adapter_cpu, adapter_wall, helper_cpu, helper_wall),
        ("outer CPU", "outer WALL", "adapter CPU", "adapter WALL", "reported compute CPU", "reported compute WALL"))]
    if min(values) < 0:
        raise RetainedFailure("negative call-boundary duration")
    oc, ow, ac, aw, hc, hw = values
    dc, dw = oc-ac-hc, ow-aw-hw
    if dc < 0 or dw < 0:
        raise RetainedFailure("negative call-boundary duration difference", {"durations": values, "delta_cpu": dc, "delta_wall": dw})
    return {"kind": "CONSERVATIVE_DURATION_DIFF", "cpu_seconds": dc, "wall_seconds": dw,
            "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
            "formula": "observed_outer_total - observed_direct_adapter - helper_reported_compute",
            "scope": "entry plus return residual; conservative whole charge, not an observed prefix interval"}


def role(spec, case_id, arm, name, chain=-1, step=-1, index=0):
    return ("P82a", spec["root_seed"], case_id, arm, chain, step, name, index)


def seed_from_role(value, native=False):
    raw = json.dumps(list(value), separators=(",", ":"), ensure_ascii=True).encode("ascii")
    digest = hashlib.sha256(raw).digest()
    return 1+int.from_bytes(digest[:4], "little") % (2**32-1) if native else int.from_bytes(digest[:8], "little")


def role_table(spec):
    rows = []
    for case in spec["cases"]:
        cid = case["id"]
        rows.append((role(spec, cid, "GEN", "weights"), False))
        rows.append((role(spec, cid, "B", "priority"), False))
        for chain in range(spec["chains"]):
            rows.append((role(spec, cid, "B", "reset_start", chain), False))
            for step in range(spec["steps"]):
                for name in ("portS", "portT", "phase_init", "split", "repair"):
                    rows.append((role(spec, cid, "B", name, chain, step), False))
                rows.append((role(spec, cid, "B", "native", chain, step), True))
        for mode in FAST_MODES+CUSTOM_MODES:
            rows.append((role(spec, cid, mode, "control"), False))
    return rows


def seed_integrity(spec):
    seen = {False: set(), True: set()}
    rows = []
    for value, native in role_table(spec):
        seed = seed_from_role(value, native)
        if seed in seen[native]:
            raise RetainedFailure("role seed collision", {"role": value, "native": native, "seed": seed})
        seen[native].add(seed)
        rows.append({"role": value, "native": native, "seed": seed})
    return rows


class Ledger:
    def __init__(self, case_id, clock, writer):
        self.case_id, self.clock, self.writer = case_id, clock, writer
        self.records, self.pending = [], []
        self.counter = 0

    def identifier(self):
        self.counter += 1
        return self.case_id+"/"+str(self.counter)

    @contextmanager
    def span(self, label, paid=False, **context):
        event = {"id": self.identifier(), "case": self.case_id, "kind": "OBSERVED_SPAN",
                 "label": label, "paid": bool(paid), "context": context}
        start = self.clock.now()
        event["start_cpu"], event["start_wall"] = start
        try:
            yield event
        finally:
            end = self.clock.now()
            event.update(end_cpu=end[0], end_wall=end[1],
                         cpu_seconds=finite(end[0]-start[0], "span CPU"),
                         wall_seconds=finite(end[1]-start[1], "span WALL"))
            if event["cpu_seconds"] < 0 or event["wall_seconds"] < 0:
                raise RetainedFailure("negative observed span", event)
            self.records.append(event)
            self.pending.append(event)

    def factory_residual(self, outer, reported):
        reported_record = {"id": self.identifier(), "case": self.case_id,
            "kind": "REPORTED_DURATION", "paid": False, "label": "P43_backend_setup_reported",
            "wall_seconds": finite(reported, "factory reported WALL"), "cpu_seconds": None,
            "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
            "helper_source_path": "research/P43_global_gain_probe.py",
            "helper_source_sha256": P43_SHA256, "outer_ref": outer["id"]}
        self.records.append(reported_record)
        self.pending.append(reported_record)
        event = duration_difference(outer, reported_record, self.identifier())
        event.update(case=self.case_id, paid=True)
        self.records.append(event)
        self.pending.append(event)
        return event

    def flush(self):
        while self.pending:
            self.writer.append("paid_ledger", self.pending[0])
            self.pending.pop(0)

    def grant(self):
        return sum(event["wall_seconds"] for event in self.records if event["paid"])


class ScoreBoard:
    """Each batch materializes all costs/masks before its owning span ends."""
    def __init__(self, graph, rank, deps, stream):
        self.graph, self.rank, self.deps, self.stream = graph, rank, deps, stream
        self.best, self.pending, self.count, self.owner = None, [], 0, None

    def remember(self, subset, value, **extra):
        if isinstance(value, bool) or not isinstance(value, numbers.Integral) or value < 0:
            raise RetainedFailure("invalid exact score", {"cut_repr": repr(value)})
        subset = canonical(subset, len(self.graph), self.rank)
        record = {"type": "score", "sequence": self.count, "owner_span": self.owner,
                  "cut": int(value), "mask_hex": pack_mask(subset, len(self.graph)).hex(), **extra}
        self.count += 1
        self.pending.append(record)
        if self.best is None or int(value) < self.best["cut"]:
            self.best = {"cut": int(value), "subset": subset, "mask_hex": record["mask_hex"],
                         "score_sequence": record["sequence"]}
        return int(value)

    def __call__(self, subset):
        return self.remember(subset, self.deps.score(self.graph, subset), method="scalar_cut")

    def scan(self, subset, rank, base_cut):
        rows = self.deps.scan(self.graph, subset, rank, base_cut)
        if len(rows) != (len(self.graph)//2)**2:
            raise RetainedFailure("incomplete exact score batch")
        batch = self.count
        for index, row in enumerate(rows):
            self.remember(row["subset"], row["cut"], method="exact_swap_delta",
                          batch=batch, batch_index=index, removed=row["removed"], added=row["added"])
        return rows

    def flush(self, writer):
        while self.pending:
            writer.append(self.stream, self.pending[0])
            self.pending.pop(0)


def priority_rank(order, n):
    if sorted(order) != list(range(n)):
        raise RetainedFailure("invalid priority order")
    return [order.index(vertex) for vertex in range(n)]


def run_b_case(raw_graph, case, spec, deps, writer, progress):
    cid, stream = case["id"], "B_"+case["id"][:2]
    ledger = Ledger(cid, deps.clock, writer)
    progress["active_ledger"] = ledger
    progress.update(case=cid, chain=None, step=None, pending=None)
    case_start = deps.clock.now()
    with ledger.span("case_private_setup", paid=True) as event:
        graph = validated_graph(raw_graph)
        rank = priority_rank(deps.permutation(role(spec, cid, "B", "priority"), list(range(N))), N)
        cache = deps.cache_factory(K//2)
        board = ScoreBoard(graph, rank, deps, stream)
        progress["active_board"] = board
        board.owner = event["id"]
        total_weight = sum(sum(row) for row in graph)//2
    writer.append(stream, {"type": "case_start", "case": cid, "priority_rank": rank,
                           "cache": cache, "total_edge_weight": total_weight})
    ledger.flush()
    raw_cuts, q_cuts, chain_rows, hist = [], [], [], [0]*(K+1)
    requested = completed = 0
    for chain in range(spec["chains"]):
        deps.guard()
        progress.update(chain=chain, step=None)
        with ledger.span("reset_start_and_warmstart", paid=True, chain=chain) as event:
            board.owner = event["id"]
            start = canonical(deps.permutation(role(spec, cid, "B", "reset_start", chain), list(range(N)))[:K], N, rank)
            initial = board(start)
            warm = bounded_descent(graph, start, rank, 2, board, initial)
            current, current_cut = warm["subset"], warm["cut"]
            chain_best = {"subset": current, "cut": current_cut}
            warm_best = current_cut
        board.flush(writer)
        writer.append(stream, {"type": "reset", "chain": chain, "start": start,
                               "start_cut": initial, "warmstart": warm})
        ledger.flush()
        for step in range(spec["steps"]):
            deps.guard()
            progress.update(chain=chain, step=step)
            with ledger.span("attempt_setup_compile_split", paid=True, chain=chain, step=step) as event:
                board.owner = event["id"]
                source_order = deps.permutation(role(spec, cid, "B", "portS", chain, step), sorted(current))
                target_order = deps.permutation(role(spec, cid, "B", "portT", chain, step), sorted(set(range(N))-set(current)))
                phase_ids = deps.integers(role(spec, cid, "B", "phase_init", chain, step), 4, K//2)
                compiled = deps.compiler(graph, source_order, target_order, phase_ids, cache=cache)
                probabilities = cache["profile"]["probabilities"]
                split_role = role(spec, cid, "B", "split", chain, step)
                coins = deps.split_draws(split_role, [p.denominator for p in probabilities])
                if len(coins) != K or any(isinstance(c, bool) or not isinstance(c, numbers.Integral)
                        or not 0 <= c < probabilities[j].denominator for j, c in enumerate(coins)):
                    raise RetainedFailure("invalid split coins", {"coins": coins})
                removed = sorted(j for j, p in enumerate(probabilities) if coins[j] < p.numerator)
                native_role = role(spec, cid, "B", "native", chain, step)
                native_seed = deps.native_seed(native_role)
                repair_role = role(spec, cid, "B", "repair", chain, step)
                repair_seed = deps.control_seed(repair_role)
                before = {"subset": current, "cut": current_cut}
                pending = {"type": "attempt_request", "case": cid, "chain": chain, "step": step,
                           "source_order": source_order, "target_order": target_order,
                           "phase_ids": phase_ids, "compiler": compiled, "split_coins": coins,
                           "removed_ports": removed, "native_role": native_role, "native_seed": native_seed,
                           "repair_role": repair_role, "repair_seed": repair_seed, "current_before": before,
                           "full_source_photons": K}
                requested += 1
                progress["requested"] = progress.get("requested", 0)+1
                progress["pending"] = pending
            writer.append(stream, pending)
            ledger.flush()
            if removed:
                with ledger.span("factory_total", paid=False, chain=chain, step=step) as outer:
                    sampler, backend_setup = deps.make_sampler(compiled["W"], removed, native_seed)
                residual = ledger.factory_residual(outer, backend_setup)
                writer.append(stream, {"type": "factory_report", "chain": chain, "step": step,
                                       "outer_ref": outer["id"], "backend_setup_wall": backend_setup,
                                       "reported_ref": residual["reported_ref"],
                                       "duration_difference_ref": residual["id"]})
                ledger.flush()
                with ledger.span("serial_native_sample", paid=False, chain=chain, step=step):
                    y, fallback = sampler()
                ledger.flush()
                if fallback:
                    raise RetainedFailure("native fallback forbidden", {"counts": serial(y), "request": pending})
            else:
                y, fallback = [0]*K, False
                writer.append(stream, {"type": "native_not_called", "chain": chain, "step": step, "reason": "r=0"})
            # Retain even malformed observations before validation can fail.
            progress["pending"] = {"request": pending, "receiver_counts": serial(y), "fallback": serial(fallback)}
            writer.append(stream, {"type": "native_observation", "chain": chain, "step": step,
                                   "receiver_counts": serial(y), "fallback": serial(fallback)})
            with ledger.span("attempt_post_decode_score_quench_accept", paid=True, chain=chain, step=step) as event:
                board.owner = event["id"]
                decoded = decode_counts(source_order, target_order, removed, y,
                    lambda available, count: deps.permutation(repair_role, available)[:count])
                candidate = canonical(decoded["subset"], N, rank)
                raw_cut = board(candidate)
                quench = bounded_descent(graph, candidate, rank, 1, board, raw_cut)
                accepted = quench["cut"] < current_cut
                if accepted:
                    current, current_cut = quench["subset"], quench["cut"]
                if quench["cut"] < chain_best["cut"]:
                    chain_best = {"subset": quench["subset"], "cut": quench["cut"]}
                raw_cuts.append(raw_cut)
                q_cuts.append(quench["cut"])
                hist[len(removed)] += 1
                completed += 1
                outcome = {"type": "attempt_outcome", "chain": chain, "step": step,
                           "receiver_counts": list(y), "fallback": fallback, "decoded": decoded,
                           "raw_cut": raw_cut, "quench": quench, "accepted": accepted,
                           "current_after": {"subset": current, "cut": current_cut},
                           "chain_best": chain_best.copy(), "all_paid_best": board.best.copy()}
                progress.update(completed=progress.get("completed", 0)+1, pending=outcome)
            board.flush(writer)
            writer.append(stream, outcome)
            ledger.flush()
            progress["pending"] = None
        with ledger.span("own_chain_final", paid=True, chain=chain):
            chain_rows.append({"chain": chain, "warmstart_cut": warm_best, "best": chain_best.copy(),
                               "current": {"subset": current, "cut": current_cut},
                               "gain_from_warmstart": warm_best-chain_best["cut"]})
        ledger.flush()
    with ledger.span("case_algorithm_finalization", paid=True):
        denominator = len(raw_cuts)*total_weight
        result = {"case": cid, "requested": requested, "completed": completed,
                  "full_source_photons": K*completed, "r_histogram": hist, "chains": chain_rows,
                  "conditional_receiver_photons": sum(r*count for r, count in enumerate(hist)),
                  "all_paid_best": board.best.copy(), "scored_candidates": board.count,
                  "raw_mean_cut": Fraction(sum(raw_cuts), len(raw_cuts)),
                  "q_mean_cut": Fraction(sum(q_cuts), len(q_cuts)),
                  "raw_mean_normalized": Fraction(sum(raw_cuts), denominator) if denominator else Fraction(0),
                  "q_mean_normalized": Fraction(sum(q_cuts), denominator) if denominator else Fraction(0)}
    result["grant_wall_seconds"] = ledger.grant()
    result["paid_component_ids"] = [event["id"] for event in ledger.records if event["paid"]]
    result["case_start_clocks"], result["case_end_clocks"] = case_start, deps.clock.now()
    ledger.flush()
    writer.append(stream, {"type": "case_result", **result})
    deps.native_readback()
    return result


def run_fast_control(raw_graph, case, mode, grant, spec, deps, writer):
    start = deps.clock.now()
    adapter_graph = [list(row) for row in raw_graph]
    seed = deps.control_seed(role(spec, case["id"], mode, "control"))
    initialization = "random" if mode == "FAST_RANDOM" else "spectral"
    boundary = deps.clock.now()
    ac, aw = boundary[0]-start[0], boundary[1]-start[1]
    budget = max(0.0, grant-ac)
    # A zero allowance still makes the registered normal helper call; it cannot
    # silently stand in for one of the four required Tier1 returns.
    result = deps.fast_solver(adapter_graph, seed, initialization, budget, MAX_WORK)
    end = deps.clock.now()
    trace = result["trace"]
    outer_cpu, outer_wall = end[0]-start[0], end[1]-start[1]
    overhead = call_boundary_difference(outer_cpu, outer_wall, ac, aw,
        result["compute_cpu_seconds"], result["compute_wall_seconds"])
    reported_compute = {"id": case["id"]+"/"+mode+"/reported_compute",
        "case": case["id"], "mode": mode, "kind": "REPORTED_DURATION", "paid": False,
        "label": "P50_compute_reported", "cpu_seconds": result["compute_cpu_seconds"],
        "wall_seconds": result["compute_wall_seconds"], "start_cpu": None, "end_cpu": None,
        "start_wall": None, "end_wall": None,
        "helper_source_path": "research/P50_fast_from_scratch.py", "helper_source_sha256": P50_SHA256}
    overhead.update(outer_ref=case["id"]+"/"+mode+"/outer",
                    direct_adapter_ref=case["id"]+"/"+mode+"/adapter",
                    reported_ref=reported_compute["id"])
    charged_ac, charged_aw = ac+overhead["cpu_seconds"], aw+overhead["wall_seconds"]
    direct_selected = select_dual_checkpoint(trace, ac, aw, grant, len(raw_graph))
    selected = select_dual_checkpoint(trace, charged_ac, charged_aw, grant, len(raw_graph))
    stages = trace["stage"]
    if len(stages) != len(trace["cpu_seconds"]):
        raise RetainedFailure("FAST stage association mismatch")
    first = next((j for j, stage in enumerate(stages) if stage == "initial_scan"), None)
    first_timely = first is not None and charged_ac+finite(trace["cpu_seconds"][first], "first scan CPU") <= grant and charged_aw+finite(trace["wall_seconds"][first], "first scan WALL") <= grant
    early_guard = bool(result.get("early_cap_inconclusive", False))
    header = {"type": "control_header", "case": case["id"], "mode": mode, "grant": grant,
              "seed": seed, "seed_role": role(spec, case["id"], mode, "control"),
              "adapter_cpu": ac, "adapter_wall": aw, "solver_cpu_budget": budget,
              "call_boundary_difference": overhead, "witness_charged_adapter_cpu": charged_ac,
              "witness_charged_adapter_wall": charged_aw,
              "reported_compute_duration": reported_compute,
              "adapter_start": start, "solver_boundary": boundary,
              "call_end": end, "actual_total_cpu": end[0]-start[0], "actual_total_wall": end[1]-start[1],
              "observed_outer": {"id": overhead["outer_ref"], "kind": "OBSERVED_SPAN",
                  "start_cpu": start[0], "start_wall": start[1], "end_cpu": end[0], "end_wall": end[1],
                  "cpu_seconds": outer_cpu, "wall_seconds": outer_wall},
              "observed_direct_adapter": {"id": overhead["direct_adapter_ref"], "kind": "OBSERVED_SPAN",
                  "start_cpu": start[0], "start_wall": start[1], "end_cpu": boundary[0], "end_wall": boundary[1],
                  "cpu_seconds": ac, "wall_seconds": aw}}
    writer.append("controls", header)
    for j in range(len(stages)):
        writer.append("controls", {"type": "checkpoint", "case": case["id"], "mode": mode,
            "index": j, "stage": stages[j], "cpu_seconds": trace["cpu_seconds"][j],
            "wall_seconds": trace["wall_seconds"][j], "cut": trace["best_cut"][j],
            "mask_hex": bytes(trace["best_subset_packbits_little"][j]).hex(),
            "work": trace["proposal_count"][j],
            "direct_dual_timely": ac+trace["cpu_seconds"][j] <= grant and aw+trace["wall_seconds"][j] <= grant,
            "dual_timely": charged_ac+trace["cpu_seconds"][j] <= grant and charged_aw+trace["wall_seconds"][j] <= grant})
    if selected is not None:
        # Validation of the selected PREEXISTING mask cannot create a new winner.
        subset = unpack_mask(selected["mask_hex"], len(raw_graph))
        deps.verify_candidate(raw_graph, subset, selected["cut"])
    compact = {key: value for key, value in result.items() if key not in (
        "trace", "best_subset", "overall_completed_best_subset", "initial_subset")}
    outcome = {"case": case["id"], "mode": mode, "grant": grant, "adapter_cpu": ac,
               "adapter_wall": aw, "selected": selected, "first_scan_dual_timely": first_timely,
               "direct_selected": direct_selected, "call_boundary_difference": overhead,
               "early_guard": early_guard, "eligible": selected is not None and first_timely and not early_guard,
               "normal_return": True, "result": compact}
    writer.append("controls", {"type": "control_result", **outcome})
    return outcome


class ControlStop(Exception):
    pass


class TimedSearch:
    def __init__(self, raw_graph, case, mode, grant, ac, aw, spec, deps, boundary=None):
        self.deps, self.clock = deps, deps.clock
        self.start = deps.clock.now() if boundary is None else boundary
        self.mode, self.cid, self.grant, self.ac, self.aw = mode, case["id"], grant, ac, aw
        self.graph = validated_graph(raw_graph)
        self.rng = deps.control_rng(role(spec, self.cid, mode, "control"))
        self.rank = priority_rank(list(map(int, self.rng.permutation(N))), N)
        self.cache = None
        self.work, self.best, self.trace, self.scores = 0, None, [], []
        self.stop_reason, self.first_scan_timely = None, False

    def check(self, work):
        self.deps.guard()
        cpu, wall = self.clock.now()
        if self.ac+cpu-self.start[0] >= self.grant or self.aw+wall-self.start[1] >= self.grant:
            self.stop_reason = "deadline"
            raise ControlStop()
        if self.work+work > MAX_WORK:
            self.stop_reason = "work_guard"
            raise ControlStop()

    def remember(self, subset, value, **extra):
        if isinstance(value, bool) or not isinstance(value, numbers.Integral) or value < 0:
            raise RetainedFailure("invalid custom score")
        subset = canonical(subset, N, self.rank)
        mask = pack_mask(subset, N).hex()
        self.work += 1
        self.scores.append({"work": self.work, "cut": int(value), "mask_hex": mask, **extra})
        if self.best is None or value < self.best["cut"]:
            self.best = {"cut": int(value), "subset": subset, "mask_hex": mask}
        return int(value)

    def checkpoint(self, stage):
        # Both the mask AND integer cut already exist before reading either clock.
        cached = None if self.best is None else {"cut": self.best["cut"], "mask_hex": self.best["mask_hex"]}
        cpu, wall = self.clock.now()
        cpu, wall = cpu-self.start[0], wall-self.start[1]
        timely = self.ac+cpu <= self.grant and self.aw+wall <= self.grant
        self.trace.append({"stage": stage, "work": self.work, "cpu_seconds": cpu,
                           "wall_seconds": wall, "cached_best": cached, "dual_timely": timely})
        if stage == "initial_scan" and timely:
            self.first_scan_timely = True
        return timely

    def __call__(self, subset):
        self.check(1)
        value = self.remember(subset, self.deps.score(self.graph, subset), method="scalar_cut")
        self.checkpoint("score")
        return value

    def scan(self, subset, rank, value):
        self.check(K*K)
        rows = self.deps.scan(self.graph, subset, rank, value)
        if len(rows) != K*K:
            raise RetainedFailure("custom incomplete scan")
        batch = self.work
        for j, row in enumerate(rows):
            self.remember(row["subset"], row["cut"], method="exact_swap_delta", batch=batch,
                          batch_index=j, removed=row["removed"], added=row["added"])
        timely = self.checkpoint("descent_scan" if self.first_scan_timely else "initial_scan")
        if not timely:
            self.stop_reason = "deadline"
            raise ControlStop()
        return rows

    def fresh(self, scans):
        self.check(1)
        subset = canonical(list(map(int, self.rng.permutation(N)))[:K], N, self.rank)
        value = self(subset)
        if scans:
            q = bounded_descent(self.graph, subset, self.rank, scans, self, value)
            return q["subset"], q["cut"]
        return subset, value

    def quench(self, subset):
        subset = canonical(subset, N, self.rank)
        value = self(subset)
        q = bounded_descent(self.graph, subset, self.rank, 1, self, value)
        return q["subset"], q["cut"]


def run_custom_control(raw_graph, case, mode, grant, spec, deps, writer):
    start = deps.clock.now()
    adapter_graph = [list(row) for row in raw_graph]
    boundary = deps.clock.now()
    ac, aw = boundary[0]-start[0], boundary[1]-start[1]
    search = TimedSearch(adapter_graph, case, mode, grant, ac, aw, spec, deps, boundary)
    completed_units = 0
    unexpected = None
    try:
        current, value = search.fresh(0 if mode == "CONTINUED_DESCENT" else 2)
        while True:
            search.check(1)
            rng = search.rng
            if mode == "CONTINUED_DESCENT":
                q = bounded_descent(search.graph, current, search.rank, 1, search, value)
                if q["cut"] < value:
                    current, value = q["subset"], q["cut"]
                else:
                    current, value = search.fresh(0)
            elif mode == "MULTISWAP":
                radius = (2, 3, 4)[completed_units % 3]
                removed = set(map(int, rng.permutation(sorted(current))[:radius]))
                added = set(map(int, rng.permutation(sorted(set(range(N))-set(current)))[:radius]))
                proposal, proposal_cut = search.quench((set(current)-removed) | added)
                if proposal_cut < value:
                    current, value = proposal, proposal_cut
                if (completed_units+1) % 12 == 0:
                    current, value = search.fresh(2)
            elif mode == "RECIPIENT_FRONTIER":
                sports = list(map(int, rng.permutation(sorted(current))))
                target = sorted(set(range(N))-set(current), key=lambda v: search.rank[v])
                probabilities = profile(K//2)["probabilities"]
                removed = [sports[j] for j, p in enumerate(probabilities) if int(rng.integers(p.denominator)) < p.numerator]
                endpoint, endpoint_cut = current, value
                for receiving in itertools.combinations(target, len(removed)):
                    proposal, proposal_cut = search.quench((set(current)-set(removed)) | set(receiving))
                    if proposal_cut < endpoint_cut:
                        endpoint, endpoint_cut = proposal, proposal_cut
                current, value = endpoint, endpoint_cut
            elif mode == "PHASE_HYPERPLANE":
                sports = list(map(int, rng.permutation(sorted(current))))
                tports = list(map(int, rng.permutation(sorted(set(range(N))-set(current)))))
                phase_ids = list(map(int, rng.integers(0, 4, K//2)))
                if search.cache is None:
                    search.cache = deps.cache_factory(K//2)
                compiled = deps.compiler(search.graph, sports, tports, phase_ids, cache=search.cache)
                theta = float(rng.uniform(0.0, 2*math.pi))
                chosen = []
                for j, phase in enumerate(compiled["phases"]):
                    projection = (phase*complex(math.cos(theta), -math.sin(theta))).real
                    plus, minus = tports[j], tports[j+K//2]
                    chosen.append(plus if projection > 0 or (projection == 0 and search.rank[plus] < search.rank[minus]) else minus)
                removed = set(map(int, rng.permutation(sorted(current))[:K//2]))
                proposal, proposal_cut = search.quench((set(current)-removed) | set(chosen))
                if proposal_cut < value:
                    current, value = proposal, proposal_cut
            else:
                raise RetainedFailure("unknown custom mode", {"mode": mode})
            completed_units += 1
    except ControlStop:
        pass
    except Exception as error:
        unexpected = error
    selected = None
    for j, checkpoint in enumerate(search.trace):
        if checkpoint["dual_timely"] and checkpoint["cached_best"] is not None:
            selected = {"index": j, **checkpoint["cached_best"],
                        "cpu_seconds": checkpoint["cpu_seconds"], "wall_seconds": checkpoint["wall_seconds"],
                        "total_cpu": ac+checkpoint["cpu_seconds"], "total_wall": aw+checkpoint["wall_seconds"],
                        "provenance": "custom_online_preclock_RAM_prefix"}
    early_guard = search.stop_reason == "work_guard"
    result = {"case": case["id"], "mode": mode, "grant": grant, "adapter_cpu": ac,
              "adapter_wall": aw, "selected": selected, "first_scan_dual_timely": search.first_scan_timely,
              "eligible": selected is not None and search.first_scan_timely and not early_guard,
              "early_guard": early_guard, "normal_return": unexpected is None, "stop_reason": search.stop_reason,
              "work": search.work, "completed_policy_units": completed_units,
              "adapter_start": start, "solver_boundary": boundary, "solver_start": search.start,
              "call_end": deps.clock.now()}
    writer.append("controls", {"type": "control_header", "case": case["id"], "mode": mode,
                               "seed_role": role(spec, case["id"], mode, "control"),
                               "seed": deps.control_seed(role(spec, case["id"], mode, "control"))})
    for record in search.scores:
        writer.append("controls", {"type": "custom_score", "case": case["id"], "mode": mode, **record})
    for j, checkpoint in enumerate(search.trace):
        writer.append("controls", {"type": "checkpoint", "case": case["id"], "mode": mode, "index": j, **checkpoint})
    writer.append("controls", {"type": "control_result", **result})
    if unexpected is not None:
        if isinstance(unexpected, ResourceFailure):
            raise unexpected
        raise RetainedFailure("custom control first failure", {"case": case["id"], "mode": mode,
            "exception_repr": repr(unexpected), "payload": getattr(unexpected, "payload", None)}) from unexpected
    return result


def classify_panel(panel, b_cases, modes):
    for mode in modes:
        rows = [row for row in panel if row["mode"] == mode]
        if len(rows) == len(b_cases) and all(row.get("normal_return") and row.get("selected") is not None
                and row["selected"]["cut"] < b_cases[row["case"]]["all_paid_best"]["cut"] for row in rows
                ) and len({row["case"] for row in rows}) == len(b_cases):
            return mode
    return None


def run_workflow(spec, deps, writer):
    progress = {"requested": 0, "completed": 0, "case": None, "chain": None, "step": None, "pending": None}
    b_cases, tier1, tier2, graphs = {}, [], [], {}
    summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False,
               "B_cases": b_cases, "tier1": tier1, "tier2": tier2,
               "D_species": {"status": "NOT_RUN", "reason": "separate future authorization required"}}
    population = [{"case": case["id"], "mode": mode, "status": "NOT_RUN", "outcome": None}
                  for mode in FAST_MODES+CUSTOM_MODES for case in spec["cases"]]
    summary["control_population"] = population
    failure = {"status": "NO_FAILURE"}
    try:
        writer.single("metadata", {"spec": spec, "provenance": deps.native_readback(),
                                   "scope": "zero-optics favorable B veto proxy; no matched physical cost"})
        for case in spec["cases"]:
            deps.guard()
            begin = deps.clock.now()
            graphs[case["id"]] = deps.generate_graph(case)
            end = deps.clock.now()
            writer.append("paid_ledger", {"kind": "OBSERVED_SPAN", "paid": False, "label": "synthetic_input_generation",
                "case": case["id"], "start_cpu": begin[0], "start_wall": begin[1], "end_cpu": end[0], "end_wall": end[1],
                "cpu_seconds": end[0]-begin[0], "wall_seconds": end[1]-begin[1]})
        writer.single("graphs", {"cases": graphs, "recipes": spec["cases"]})
        for case in spec["cases"]:
            b_cases[case["id"]] = run_b_case(graphs[case["id"]], case, spec, deps, writer, progress)
            progress.pop("active_ledger", None)
            progress.pop("active_board", None)
        if progress["completed"] != 96:
            raise RetainedFailure("incomplete registered B population", progress["completed"])
        for mode in FAST_MODES:
            for case in spec["cases"]:
                deps.guard()
                progress.update(case=case["id"], pending={"mode": mode}, chain=None, step=None)
                population_row = next(row for row in population if row["case"] == case["id"] and row["mode"] == mode)
                population_row["status"] = "REQUESTED"
                tier1.append(run_fast_control(graphs[case["id"]], case, mode,
                    b_cases[case["id"]]["grant_wall_seconds"], spec, deps, writer))
                population_row.update(status="COMPLETE", outcome={"selected": tier1[-1]["selected"], "eligible": tier1[-1]["eligible"]})
        winner = classify_panel(tier1, b_cases, FAST_MODES)
        if winner:
            summary.update(status="DEV_REJECTED_FIXED_FAST", veto_mode=winner,
                           tier2_status={"status": "NOT_RUN", "reason": "fixed FAST veto"})
        elif any(not row["eligible"] for row in tier1):
            summary.update(status="INCONCLUSIVE_FAST_ELIGIBILITY",
                           tier2_status={"status": "NOT_RUN", "reason": "FAST eligibility incomplete"})
        else:
            for mode in CUSTOM_MODES:
                for case in spec["cases"]:
                    deps.guard()
                    progress.update(case=case["id"], pending={"mode": mode})
                    population_row = next(row for row in population if row["case"] == case["id"] and row["mode"] == mode)
                    population_row["status"] = "REQUESTED"
                    tier2.append(run_custom_control(graphs[case["id"]], case, mode,
                        b_cases[case["id"]]["grant_wall_seconds"], spec, deps, writer))
                    population_row.update(status="COMPLETE", outcome={"selected": tier2[-1]["selected"], "eligible": tier2[-1]["eligible"]})
            winner = classify_panel(tier2, b_cases, CUSTOM_MODES)
            summary.update(status="DEV_REJECTED_FIXED_CLASSICAL" if winner else
                           "INCONCLUSIVE_CONTROL_ELIGIBILITY" if any(not row["eligible"] for row in tier2)
                           else "STAGE1_REOPTIMIZED_D_SPECIES_REQUIRED", veto_mode=winner)
        summary["completed_B_attempts"] = progress["completed"]
        summary["requested_B_attempts"] = progress["requested"]
        summary["modeled_full_source_photons"] = K*progress["requested"]
        summary["modeled_completed_source_photons"] = K*progress["completed"]
        summary["native_final_readback"] = deps.native_readback()
        end = deps.clock.now()
        summary["workflow_before_final_evidence_clocks"] = end
        if hasattr(deps, "start"):
            summary["whole_run_before_final_evidence"] = {"cpu_seconds": end[0]-deps.start[0],
                                                        "wall_seconds": end[1]-deps.start[1]}
        summary["serialization_and_io_before_final_evidence"] = {
            "cpu_seconds": getattr(writer, "serialization_and_io_cpu", None),
            "wall_seconds": getattr(writer, "serialization_and_io_wall", None),
            "scope": "completed serialized writes only; final summary/failure write excluded"}
        deps.guard()
    except Exception as error:
        # Ordinary exceptions are first-failure evidence, never a hidden retry.
        ledger, board = progress.pop("active_ledger", None), progress.pop("active_board", None)
        try:
            if board is not None:
                board.flush(writer)
            if ledger is not None:
                ledger.flush()
        except Exception as flushing_error:
            progress["flush_error"] = repr(flushing_error)
        summary.update(status="INCONCLUSIVE_RESOURCE_FAILURE" if isinstance(error, ResourceFailure) else "INCONCLUSIVE_FIRST_FAILURE", completed_B_attempts=progress["completed"],
                       requested_B_attempts=progress["requested"], modeled_full_source_photons=K*progress["requested"],
                       modeled_completed_source_photons=K*progress["completed"],
                       tier2_status={"status": "NOT_RUN_OR_PARTIAL", "reason": "first failure"})
        failure = {"status": "FIRST_FAILURE", "exception_type": type(error).__name__,
                   "exception_repr": repr(error), "payload": getattr(error, "payload", None),
                   "progress": {key: value for key, value in progress.items() if not key.startswith("active_")},
                   "remaining": "NOT_RUN; no retry"}
    finally:
        summary = writer.finish(summary, failure)
    return summary


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def checked_inputs(root, spec):
    local = []
    for expected in spec["immutable_inputs"]:
        path = root/expected["path"]
        actual = file_sha256(path)
        local.append({**expected, "actual_sha256": actual})
        if actual != expected["sha256"]:
            raise RetainedFailure("immutable source mismatch", local[-1])
    closure = []
    for relative in spec["execution_artifacts"]:
        path = root/relative
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise RetainedFailure("invalid project input closure", {"path": relative})
        closure.append({"path": relative, "sha256": file_sha256(path)})
    external = []
    for expected in spec["external_artifacts"]:
        actual = file_sha256(expected["path"])
        external.append({**expected, "actual_sha256": actual})
        if actual != expected["sha256"]:
            raise RetainedFailure("external source mismatch", external[-1])
    software = {}
    for name, expected in spec["software"].items():
        actual = platform.python_version() if name == "Python" else importlib.metadata.version(name)
        software[name] = actual
        if actual != expected:
            raise RetainedFailure("software version mismatch", {"name": name, "expected": expected, "actual": actual})
    return {"immutable_inputs": local, "project_input_hashes": closure, "external_inputs": external,
            "software": software, "interpreter": sys.executable,
            "resolved_interpreter": str(Path(sys.executable).resolve()),
            "external_binding": "independent preimport SHA checks; external paths are not runner --inputs"}


def load_helper(path, name):
    module_spec = importlib.util.spec_from_file_location(name, path)
    if module_spec is None or module_spec.loader is None:
        raise RetainedFailure("cannot locate frozen helper", {"path": str(path)})
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[name] = module
    module_spec.loader.exec_module(module)
    return module


class NativeDependencies:
    """Created only by authorized main, after preimport environment/pin checks."""
    def __init__(self, root, spec, provenance, start):
        self.spec, self.provenance, self.start, self.clock = spec, provenance, start, SystemClock()
        import exqalibur as xq
        xq.Config.compute_max_thread_count = 1
        self.xq = xq
        self.native_readback()
        import perceval as pcvl
        self.pcvl = pcvl
        self.native_readback()
        import numpy as np
        import networkx as nx
        self.np, self.nx = np, nx
        self.p43 = load_helper(root/"research/P43_global_gain_probe.py", "_p82a_frozen_p43")
        self.p50 = load_helper(root/"research/P50_fast_from_scratch.py", "_p82a_frozen_p50")
        # This pregraph integrity pass is metadata. Every used role is derived
        # again inside its charged algorithm scope, rather than using this cache.
        self.provenance["role_seeds"] = seed_integrity(spec)
        self.native_readback()

    def guard(self):
        cpu, wall = self.clock.now()
        if cpu-self.start[0] > self.spec["limits"]["cpu_seconds"] or wall-self.start[1] > self.spec["limits"]["wall_seconds"]:
            raise ResourceFailure("registered process resource allowance exhausted", {
                "cpu_seconds": cpu-self.start[0], "wall_seconds": wall-self.start[1]})

    def native_readback(self):
        actual = self.xq.Config.compute_max_thread_count
        actual = actual() if callable(actual) else actual
        if actual != 1:
            raise RetainedFailure("native threads readback mismatch", {"observed_repr": repr(actual)})
        return {"native_threads": int(actual), "provenance": self.provenance}

    def control_seed(self, value):
        return seed_from_role(value)

    def control_rng(self, value):
        return self.np.random.Generator(self.np.random.PCG64(self.control_seed(value)))

    def permutation(self, value, values):
        return [int(item) for item in self.control_rng(value).permutation(values)]

    def integers(self, value, high, count):
        return [int(item) for item in self.control_rng(value).integers(0, high, size=count)]

    def split_draws(self, value, denominators):
        rng = self.control_rng(value)
        return [int(rng.integers(0, denominator)) for denominator in denominators]

    def native_seed(self, value):
        return seed_from_role(value, native=True)

    def cache_factory(self, d):
        return receiver_cache(d, Fraction(*self.spec["rho"]), Fraction(*self.spec["eta"]))

    def compiler(self, graph, sports, tports, phase_ids, cache=None):
        return compile_receiver(graph, sports, tports, phase_ids,
            Fraction(*self.spec["rho"]), Fraction(*self.spec["eta"]), self.spec["phase_sweeps"], cache)

    def score(self, graph, subset):
        return cut(graph, subset)

    def scan(self, graph, subset, rank, base_cut):
        return all_swap_candidates(graph, subset, rank, base_cut)

    def make_sampler(self, matrix, source, seed):
        return self.p43.make_optical_sampler(self.np.asarray(matrix, dtype=self.np.complex128),
                                           list(source), "bosonic", seed)

    def fast_solver(self, graph, seed, initialization, cpu_budget_seconds, max_proposals):
        return self.p50.solve_from_raw(graph, seed=seed, initialization=initialization,
            cpu_budget_seconds=cpu_budget_seconds, max_proposals=max_proposals)

    def verify_candidate(self, graph, subset, value):
        if cut(graph, subset) != value:
            raise RetainedFailure("selected archived cut/mask mismatch", {"cut": value, "subset": subset})

    def generate_graph(self, case):
        if case["generator"] == "gnp_random_graph":
            graph = self.nx.gnp_random_graph(case["n"], case["edge_probability"], seed=case["seed"])
        elif case["generator"] == "random_regular_graph":
            graph = self.nx.random_regular_graph(case["degree"], case["n"], seed=case["seed"])
        else:
            raise RetainedFailure("unknown frozen graph generator")
        edges = sorted((min(int(u), int(v)), max(int(u), int(v))) for u, v in graph.edges())
        rng = self.control_rng(role(self.spec, case["id"], "GEN", "weights"))
        weights = [int(item) for item in rng.integers(1, 6, size=len(edges))]
        adjacency = [[0]*case["n"] for _ in range(case["n"])]
        for (u, v), weight in zip(edges, weights):
            adjacency[u][v] = adjacency[v][u] = weight
        return adjacency


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    start = SystemClock().now()
    root = Path(__file__).resolve().parents[1]
    writer = None
    try:
        if Path(sys.executable).absolute() != Path(PERSISTENT_PYTHON):
            raise RetainedFailure("main requires frozen persistent interpreter", {"actual": sys.executable})
        if args.spec.absolute() != root/"research/P82a_execution_spec.json":
            raise RetainedFailure("only frozen spec path is authorized")
        if file_sha256(args.spec) != SPEC_SHA256:
            raise RetainedFailure("frozen spec byte hash mismatch")
        spec = json.loads(args.spec.read_text(encoding="ascii"))
        if args.output.absolute() != root/spec["main_output"]:
            raise RetainedFailure("only frozen output path is authorized")
        writer = EvidenceWriter(args.output, spec["limits"]["scientific_bytes"], spec["limits"]["reserved_final_bytes"])
        for name in spec["thread_environment"]:
            os.environ[name] = "1"
        if any(os.environ[name] != "1" for name in spec["thread_environment"]):
            raise RetainedFailure("environment thread readback mismatch")
        provenance = checked_inputs(root, spec)
        provenance["environment_threads"] = {name: os.environ[name] for name in spec["thread_environment"]}
        setup_start = SystemClock().now()
        deps = NativeDependencies(root, spec, provenance, start)
        setup_end = deps.clock.now()
        provenance["excluded_import_configuration_span"] = {
            "start_cpu": setup_start[0], "start_wall": setup_start[1],
            "end_cpu": setup_end[0], "end_wall": setup_end[1],
            "cpu_seconds": setup_end[0]-setup_start[0], "wall_seconds": setup_end[1]-setup_start[1]}
        summary = run_workflow(spec, deps, writer)
        return 0 if summary["status"] not in ("INCONCLUSIVE_FIRST_FAILURE", "INCONCLUSIVE_RESOURCE_FAILURE") else 1
    except Exception as error:
        if writer is not None:
            writer.finish({"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False,
                           "B_cases": None, "tier1": None, "tier2": None, "population_status": "NOT_RUN"},
                          {"status": "FIRST_FAILURE", "exception_type": type(error).__name__,
                           "exception_repr": repr(error), "payload": getattr(error, "payload", None)})
        else:
            sys.stderr.write(json.dumps({"status": "INCONCLUSIVE_FIRST_FAILURE", "exception_repr": repr(error)})+"\n")
        return 1
    finally:
        if writer is not None:
            writer.close()


if __name__ == "__main__":
    raise SystemExit(main())
