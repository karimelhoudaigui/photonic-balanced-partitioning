"""P90a prospective source-bound nonflat DEV screen; import runs no experiment.

Only main constructs scientific dependencies or production random streams.
Compact cuts/masks exist before paid clocks; audit dictionaries are later.
"""
from __future__ import annotations

import argparse
from array import array
from contextlib import contextmanager
from dataclasses import dataclass, fields, is_dataclass
from fractions import Fraction
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import numbers
import os
from pathlib import Path
import platform
import sys
import time


SPEC_SHA256 = "87dda967c662b0507c364d216f2c1a937d6a83e8616b536b7a0330bd90be0e7f"
PERSISTENT_PYTHON = "/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python"
P43_SHA256 = "b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777"
P50_SHA256 = "6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86"
FAST_MODES = ("FAST_RANDOM", "FAST_SPECTRAL")
STAGES = ("initialization", "initial_scan", "descent_scan", "anneal_setup",
          "anneal", "uniform_restart", "perturb_best")
MAX_WORK, MAX_TRACE = 1000000, 40000
MAX_BYTES, RESERVE, MAX_OBJECT = 32*1024*1024, 1024*1024, 4*1024*1024
STREAMS = ("B_ER.jsonl", "B_RR.jsonl", "paid_ledger.jsonl", "controls.jsonl")


class AuditFailure(RuntimeError):
    def __init__(self, message, payload=None):
        super().__init__(message)
        self.payload = {} if payload is None else payload


class ResourceFailure(AuditFailure):
    pass


class SystemClock:
    def now(self):
        return time.process_time(), time.perf_counter()


def strict_int(value, label, minimum=None):
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise AuditFailure("integer required: "+label, {"observed_repr": repr(value)})
    value = int(value)
    if minimum is not None and value < minimum:
        raise AuditFailure("integer below minimum: "+label, {"value": value})
    return value


def finite(value, label, nonnegative=True):
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise AuditFailure("real scalar required: "+label, {"observed_repr": repr(value)})
    value = float(value)
    if not math.isfinite(value) or (nonnegative and value < 0):
        raise AuditFailure("invalid finite scalar: "+label, {"observed_repr": repr(value)})
    return value


def numeric_cap(value, expected, label):
    if type(value) not in (int, float) or not math.isfinite(value) or value != expected:
        raise AuditFailure("exact numeric cap required: "+label, {"observed_repr": repr(value), "expected": expected})
    return float(value)


def checked_rank(rank, n):
    if len(rank) != n or any(isinstance(v, bool) or not isinstance(v, numbers.Integral) for v in rank):
        raise AuditFailure("invalid priority rank")
    values = [int(v) for v in rank]
    if sorted(values) != list(range(n)):
        raise AuditFailure("priority is not a permutation")
    return values


def checked_mask(mask, n):
    mask = strict_int(mask, "mask", 0)
    if n < 2 or n % 2 or mask >= 1 << n or mask.bit_count() != n//2:
        raise AuditFailure("mask padding/cardinality", {"mask": mask, "n": n})
    return mask


def mask_from_subset(vertices, n):
    values = list(vertices)
    mask = 0
    for value in values:
        vertex = strict_int(value, "vertex", 0)
        if vertex >= n or mask & (1 << vertex):
            raise AuditFailure("invalid/duplicate vertex")
        mask |= 1 << vertex
    return checked_mask(mask, n)


def mask_vertices(mask, n):
    mask = checked_mask(mask, n)
    return [v for v in range(n) if mask & (1 << v)]


def canonical_mask(mask, n, rank):
    mask, rank = checked_mask(mask, n), checked_rank(rank, n)
    return mask if mask & (1 << rank.index(0)) else ((1 << n)-1) ^ mask


def mask_hex(mask, n):
    return checked_mask(mask, n).to_bytes((n+7)//8, "little").hex()


def read_mask_hex(text, n):
    if type(text) is not str or len(text) != 2*((n+7)//8):
        raise AuditFailure("packed-mask length/type")
    try:
        raw = bytes.fromhex(text)
    except ValueError as error:
        raise AuditFailure("packed-mask hex", {"observed_repr": repr(text)}) from error
    return checked_mask(int.from_bytes(raw, "little"), n)


def validate_graph(graph):
    n = len(graph)
    if n < 2 or n % 2 or any(len(row) != n for row in graph):
        raise AuditFailure("even square graph required")
    out = [[strict_int(value, "weight", 0) for value in row] for row in graph]
    if any(out[i][i] != 0 for i in range(n)) or any(out[i][j] != out[j][i] for i in range(n) for j in range(n)):
        raise AuditFailure("graph diagonal/symmetry")
    if max(max(row) for row in out) > (2**63-1)//(4*n*n):
        raise AuditFailure("graph exact-int64 overflow guard")
    return out


def scalar_cut(graph, mask):
    n, mask = len(graph), checked_mask(mask, len(graph))
    return sum(int(graph[i][j]) for i in range(n) if mask & (1 << i)
               for j in range(n) if not mask & (1 << j))


@dataclass(frozen=True)
class Candidate:
    mask: int
    cut: int
    sequence: int


@dataclass(frozen=True)
class CutBatch:
    n: int
    source_mask: int
    base_cut: int
    inside: tuple
    outside: tuple
    cuts: array
    masks: array

    @property
    def count(self):
        return len(self.cuts)

    def best_index(self):
        return min(range(self.count), key=self.cuts.__getitem__)


def exact_swap_batch(graph, mask, rank, base_cut, degree=None):
    n = len(graph)
    rank = checked_rank(rank, n)
    mask = canonical_mask(mask, n, rank)
    base_cut = strict_int(base_cut, "base cut", 0)
    inside = tuple(sorted(mask_vertices(mask, n), key=rank.__getitem__))
    outside = tuple(sorted((v for v in range(n) if not mask & (1 << v)), key=rank.__getitem__))
    degree = [sum(row) for row in graph] if degree is None else degree
    ell = [int(degree[v])-2*sum(int(graph[v][u]) for u in inside) for v in range(n)]
    cuts, masks = array("q"), array("I")
    if cuts.itemsize != 8 or masks.itemsize != 4 or n > 32:
        raise AuditFailure("compact exact array representation unavailable")
    pivot, full = 1 << rank.index(0), (1 << n)-1
    for removed in inside:
        for added in outside:
            delta = ell[added]-ell[removed]+2*int(graph[removed][added])
            candidate = mask ^ (1 << removed) ^ (1 << added)
            candidate = candidate if candidate & pivot else full ^ candidate
            cuts.append(base_cut+delta)
            masks.append(candidate)
    return CutBatch(n, mask, base_cut, inside, outside, cuts, masks)


def m_matrix(batch):
    k = batch.n//2
    if batch.count != k*k or len(batch.masks) != k*k:
        raise AuditFailure("incomplete compiler batch")
    return [[int(batch.cuts[i*k+a])-batch.base_cut for i in range(k)] for a in range(k)]


@dataclass(frozen=True)
class Compiled:
    source_order: tuple
    target_order: tuple
    M: object
    H: object
    eigenvalues: object
    d: float
    V: object
    v_gram_error: float
    nonflat_max: float
    ipr_sum: float


@dataclass(frozen=True)
class Routed:
    W: object
    w_gram_error: float
    frame_gram_error: float


def gram_error(matrix):
    k = len(matrix)
    if k == 0 or any(len(row) != k for row in matrix):
        raise AuditFailure("square unitary dimensions")
    if any(not math.isfinite(complex(z).real) or not math.isfinite(complex(z).imag) for row in matrix for z in row):
        raise AuditFailure("nonfinite unitary")
    return max(abs(sum(complex(matrix[a][i]).conjugate()*matrix[a][j] for a in range(k))-int(i == j)) for i in range(k) for j in range(k))


def compile_feature(batch, np_module, expm):
    np = np_module
    m = np.asarray(m_matrix(batch), dtype=np.int64)
    h = (m+m.T)/2+1j*(m-m.T)/2
    if not np.array_equal(h, h.conjugate().T):
        raise AuditFailure("compiler H is not Hermitian")
    eigenvalues = np.linalg.eigvalsh(h)
    if not np.all(np.isfinite(eigenvalues)):
        raise AuditFailure("nonfinite Hermitian spectrum", {"M": m, "H": h, "eigenvalues": eigenvalues})
    d = max(1.0, float(np.max(np.abs(eigenvalues))))
    v = expm(-1j*h/d)
    try:
        error = gram_error(v)
    except AuditFailure as error:
        raise AuditFailure("V Gram guard", {"M": m, "H": h, "eigenvalues": eigenvalues,
            "d": d, "V": v, "error_repr": repr(error)}) from error
    if error > 3e-12:
        raise AuditFailure("V Gram guard", {"absolute_error": error, "M": m, "H": h,
            "eigenvalues": eigenvalues, "d": d, "V": v})
    k = len(v)
    nonflat = max(abs(abs(complex(z))**2-1/k) for row in v for z in row)
    ipr = sum(abs(complex(z))**4 for row in v for z in row)
    return Compiled(batch.inside, batch.outside, m, h, eigenvalues, d, v, error, nonflat, ipr)


def transport_feature(compiled, source_ports, target_ports):
    source_ports = tuple(strict_int(v, "source port label", 0) for v in source_ports)
    target_ports = tuple(strict_int(v, "target port label", 0) for v in target_ports)
    if sorted(source_ports) != sorted(compiled.source_order) or sorted(target_ports) != sorted(compiled.target_order):
        raise AuditFailure("transported source/target labels disagree")
    si = {v: i for i, v in enumerate(compiled.source_order)}
    ti = {v: a for a, v in enumerate(compiled.target_order)}
    w = [[complex(compiled.V[ti[a]][si[i]]) for i in source_ports] for a in target_ports]
    try:
        error = gram_error(w)
    except AuditFailure as error:
        raise AuditFailure("W Gram guard", {"source_ports": source_ports,
            "target_ports": target_ports, "W": w, "error_repr": repr(error)}) from error
    k = len(w)
    frame = max(abs(0.5*int(i == j)+0.5*sum(w[a][i].conjugate()*w[a][j] for a in range(k))-int(i == j)) for i in range(k) for j in range(k))
    if max(error, frame) > 3e-12:
        raise AuditFailure("transport/frame Gram guard", {"W_error": error, "frame_error": frame,
            "source_ports": source_ports, "target_ports": target_ports, "W": w})
    return Routed(w, error, frame)


@dataclass(frozen=True)
class Decoded:
    mask: int
    kept_counts: tuple
    receiver_counts: tuple
    full_counts: tuple
    vertex_counts: tuple
    removed_vertices: tuple
    r: int
    h: int
    fill: tuple
    repair_used: bool


def repair_counts(source_ports, target_ports, removed_ports, y, choose):
    source_ports = tuple(strict_int(v, "source port label", 0) for v in source_ports)
    target_ports = tuple(strict_int(v, "target port label", 0) for v in target_ports)
    k = len(source_ports)
    if len(target_ports) != k or sorted(source_ports+target_ports) != list(range(2*k)):
        raise AuditFailure("source/target ports are not a partition")
    removed = tuple(strict_int(v, "removed port", 0) for v in removed_ports)
    if len(set(removed)) != len(removed) or any(v >= k for v in removed):
        raise AuditFailure("duplicate/out-of-range removed ports")
    y = tuple(strict_int(value, "receiver count", 0) for value in y)
    if len(y) != k or sum(y) != len(removed):
        raise AuditFailure("receiver dimension/photon sum", {"observed_counts": y, "r": len(removed)})
    support = tuple(target_ports[a] for a in range(k) if y[a])
    available = tuple(sorted(set(target_ports)-set(support)))
    need = len(removed)-len(support)
    used = 0 < need < len(available)
    fill = tuple(choose(list(available), need)) if used else available if need else ()
    if len(fill) != need or len(set(fill)) != need or not set(fill) <= set(available):
        raise AuditFailure("invalid uniform completion")
    kept = tuple(int(i not in removed) for i in range(k))
    vertices = [0]*(2*k)
    for i, value in enumerate(kept):
        vertices[source_ports[i]] = value
    for a, value in enumerate(y):
        vertices[target_ports[a]] = value
    selected = [source_ports[i] for i in range(k) if i not in removed]+list(support)+list(fill)
    mask = mask_from_subset(selected, 2*k)
    return Decoded(mask, kept, y, kept+y, tuple(vertices), tuple(source_ports[i] for i in removed),
                   len(removed), len(support), fill, used)


@dataclass(frozen=True)
class Endpoint:
    mask: int
    cut: int
    scans: int
    local_optimum: bool


def bounded_descent(book, mask, value, max_scans):
    mask = canonical_mask(mask, len(book.graph), book.rank)
    value = strict_int(value, "endpoint cut", 0)
    scans, local = 0, False
    for _ in range(strict_int(max_scans, "scan cap", 0)):
        batch = book.batch(mask, value, "quench" if max_scans == 1 else "warmstart")
        index = batch.best_index()
        scans += 1
        if batch.cuts[index] >= value:
            local = True
            break
        mask, value = int(batch.masks[index]), int(batch.cuts[index])
    return Endpoint(mask, value, scans, local)


def serial(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if is_dataclass(value):
        return {field.name: serial(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, complex):
        return {"real": serial(value.real), "imag": serial(value.imag)}
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return value
    if isinstance(value, numbers.Integral):
        return int(value)
    if isinstance(value, numbers.Real):
        value = float(value)
        return value if math.isfinite(value) else {"nonfinite_repr": repr(value)}
    if isinstance(value, dict):
        return {str(key): serial(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, array)):
        return [serial(item) for item in value]
    if isinstance(value, bytes):
        return value.hex()
    if hasattr(value, "tolist"):
        return serial(value.tolist())
    return {"unsupported_repr": repr(value)[:4096]}


def encoded(value):
    return (json.dumps(serial(value), ensure_ascii=True, separators=(",", ":"), allow_nan=False)+"\n").encode("ascii")


class EvidenceWriter:
    def __init__(self, output, max_bytes=MAX_BYTES, reserve=RESERVE):
        self.output = Path(output)
        self.max_bytes, self.reserve = int(max_bytes), int(reserve)
        if not 0 < self.reserve < self.max_bytes:
            raise ValueError("invalid evidence reserve")
        self.output.mkdir(parents=True, exist_ok=False)
        self.streams = {name: (self.output/name).open("xb") for name in STREAMS}
        self.bytes_written = 0
        self.io_cpu = self.io_wall = 0.0
        self.finish_attempted = False

    def room(self, size, final=False):
        if size > MAX_OBJECT:
            raise ResourceFailure("single scientific JSON/line cap", {"next_bytes": size})
        limit = self.max_bytes if final else self.max_bytes-self.reserve
        if self.bytes_written+size > limit:
            raise ResourceFailure("scientific evidence byte cap", {
                "written_bytes": self.bytes_written, "next_bytes": size, "limit": limit})

    def append(self, name, record):
        name = name if name.endswith(".jsonl") else name+".jsonl"
        begin = SystemClock().now()
        data = encoded(record)
        self.room(len(data))
        self.streams[name].write(data)
        self.streams[name].flush()
        self.bytes_written += len(data)
        end = SystemClock().now()
        self.io_cpu += end[0]-begin[0]
        self.io_wall += end[1]-begin[1]

    def single(self, name, record, final=False):
        name = name if name.endswith(".json") else name+".json"
        if name not in ("metadata.json", "graphs.json", "summary.json", "failure.json"):
            raise ValueError("unknown single evidence file")
        begin = SystemClock().now()
        data = encoded(record)
        self.room(len(data), final)
        with (self.output/name).open("xb") as stream:
            stream.write(data)
            stream.flush()
        self.bytes_written += len(data)
        end = SystemClock().now()
        self.io_cpu += end[0]-begin[0]
        self.io_wall += end[1]-begin[1]

    def finish(self, summary, failure):
        if self.finish_attempted:
            raise AuditFailure("scientific finalization already attempted; no retry")
        self.finish_attempted = True
        records = {"summary.json": summary, "failure.json": failure}
        for name in ("metadata.json", "graphs.json"):
            if not (self.output/name).exists():
                records[name] = {"status": "NOT_RUN", "reason": "first failure"}
        required = sum(len(encoded(record)) for record in records.values())
        if self.bytes_written+required > self.max_bytes or any(len(encoded(record)) > MAX_OBJECT for record in records.values()):
            records["summary.json"] = {"status": "INCONCLUSIVE_RESOURCE_FAILURE", "positive_accepted": False,
                "completed_B_attempts": summary.get("completed_B_attempts"), "reason": "final reserve/object cap"}
            records["failure.json"] = {"status": "FIRST_FAILURE", "exception_repr": str(failure.get("exception_repr", "final reserve/object cap"))[:8192],
                "earlier_status": failure.get("status"), "reason": "final reserve/object cap"}
        total = sum(len(encoded(record)) for record in records.values())
        if self.bytes_written+total > self.max_bytes:
            records["summary.json"] = {"status": "INCONCLUSIVE_RESOURCE_FAILURE", "positive_accepted": False}
            records["failure.json"] = {"status": "FIRST_FAILURE", "reason": "final reserve exhausted"}
        for name, record in records.items():
            self.single(name, record, final=True)
        return records["summary.json"]

    def close(self):
        for stream in self.streams.values():
            stream.close()


class MemoryWriter:
    def __init__(self):
        self.records = {name: [] for name in STREAMS}
        self.singles = {}

    def append(self, name, record):
        name = name if name.endswith(".jsonl") else name+".jsonl"
        self.records[name].append(serial(record))

    def single(self, name, record, final=False):
        name = name if name.endswith(".json") else name+".json"
        if name in self.singles:
            raise AuditFailure("duplicate single result")
        self.singles[name] = serial(record)

    def finish(self, summary, failure):
        self.singles["summary.json"], self.singles["failure.json"] = serial(summary), serial(failure)
        return summary


@dataclass(frozen=True)
class ScalarEvent:
    n: int
    mask: int
    cut: int
    sequence: int
    phase: str
    owner_span: str

    def to_record(self):
        return {"type": "scalar_score", "sequence": self.sequence, "phase": self.phase,
                "owner_span": self.owner_span, "mask_u32": self.mask,
                "mask_hex": mask_hex(self.mask, self.n), "cut": self.cut}


@dataclass(frozen=True)
class BatchEvent:
    batch: CutBatch
    score_start: int
    phase: str
    owner_span: str
    best_index: int

    def to_record(self):
        return {"type": "scored_batch", "id": self.owner_span+"/scores/"+str(self.score_start),
            "phase": self.phase, "owner_span": self.owner_span, "score_start": self.score_start,
            "count": self.batch.count, "source_mask_u32": self.batch.source_mask,
            "base_cut": self.batch.base_cut, "inside": self.batch.inside, "outside": self.batch.outside,
            "cuts": self.batch.cuts, "masks_u32": self.batch.masks, "best_index": self.best_index,
            "best_cut": self.batch.cuts[self.best_index], "best_mask_u32": self.batch.masks[self.best_index],
            "order": "i-major/a-minor"}


class ScoreBook:
    def __init__(self, graph, rank, deps, stream):
        self.graph, self.rank, self.deps, self.stream = graph, checked_rank(rank, len(graph)), deps, stream
        self.degree = tuple(sum(row) for row in graph)
        self.count, self.pending, self.owner_span = 0, [], None
        self.global_best = self.chain_best = self.compiler_best = None
        self.global_best_phase = self.chain_best_phase = None
        self.chain = None

    def start_chain(self, chain):
        self.chain, self.chain_best, self.chain_best_phase = chain, None, None

    def credit(self, candidate, phase):
        if self.global_best is None or candidate.cut < self.global_best.cut:
            self.global_best, self.global_best_phase = candidate, phase
        if self.chain_best is None or candidate.cut < self.chain_best.cut:
            self.chain_best, self.chain_best_phase = candidate, phase
        if phase == "compiler_M" and (self.compiler_best is None or candidate.cut < self.compiler_best.cut):
            self.compiler_best = candidate

    def scalar(self, mask, phase):
        mask = canonical_mask(mask, len(self.graph), self.rank)
        value = strict_int(self.deps.cut(self.graph, mask), "cut", 0)
        candidate = Candidate(mask, value, self.count)
        self.credit(candidate, phase)
        self.pending.append(ScalarEvent(len(self.graph), mask, value, self.count, phase, self.owner_span))
        self.count += 1
        return value

    def batch(self, mask, base_cut, phase):
        n, k = len(self.graph), len(self.graph)//2
        mask = canonical_mask(mask, n, self.rank)
        batch = self.deps.swap_batch(self.graph, mask, self.rank, base_cut, self.degree)
        if (batch.n != n or batch.source_mask != mask or batch.base_cut != base_cut
                or batch.count != k*k or len(batch.masks) != k*k
                or not isinstance(batch.cuts, array) or batch.cuts.typecode != "q"
                or not isinstance(batch.masks, array) or batch.masks.typecode != "I"):
            raise AuditFailure("incomplete/wrong compact score batch")
        pivot = 1 << self.rank.index(0)
        if any(cut < 0 or mask >= 1 << n or mask.bit_count() != k or not mask & pivot
               for cut, mask in zip(batch.cuts, batch.masks)):
            raise AuditFailure("invalid materialized batch cut/mask")
        index = batch.best_index()
        candidate = Candidate(int(batch.masks[index]), int(batch.cuts[index]), self.count+index)
        self.credit(candidate, phase)
        self.pending.append(BatchEvent(batch, self.count, phase, self.owner_span, index))
        self.count += batch.count
        return batch

    def flush(self, writer):
        while self.pending:
            writer.append(self.stream, self.pending[0].to_record())
            self.pending.pop(0)


def duration_difference(outer_record, reported_record, event_id):
    if (outer_record.get("kind") != "OBSERVED_SPAN" or not outer_record.get("id") or not outer_record.get("case")
            or reported_record.get("kind") != "REPORTED_DURATION" or reported_record.get("paid") is not False
            or not reported_record.get("id") or reported_record.get("case") != outer_record.get("case")
            or any(reported_record.get(key) is not None for key in ("cpu_seconds", "start_cpu", "end_cpu", "start_wall", "end_wall"))):
        raise AuditFailure("invalid typed factory duration operands")
    outer = finite(outer_record["wall_seconds"], "factory outer WALL")
    reported = finite(reported_record["wall_seconds"], "factory reported WALL")
    if reported > outer:
        raise AuditFailure("factory reported duration exceeds observed outer", {"outer": outer, "reported": reported})
    return {"id": event_id, "case": outer_record["case"], "kind": "DURATION_DIFF", "paid": True,
        "label": "factory_prefix_plus_return_residual", "wall_seconds": outer-reported, "cpu_seconds": None,
        "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
        "outer_ref": outer_record["id"], "reported_ref": reported_record["id"],
        "formula": "factory_outer_wall - helper_reported_setup_wall"}


def call_boundary_difference(outer_cpu, outer_wall, adapter_cpu, adapter_wall, helper_cpu, helper_wall):
    oc, ow, ac, aw, hc, hw = [finite(value, "call-boundary duration") for value in
        (outer_cpu, outer_wall, adapter_cpu, adapter_wall, helper_cpu, helper_wall)]
    dc, dw = oc-ac-hc, ow-aw-hw
    if dc < 0 or dw < 0:
        raise AuditFailure("negative conservative call difference", {"delta_cpu": dc, "delta_wall": dw})
    return {"kind": "CONSERVATIVE_DURATION_DIFF", "cpu_seconds": dc, "wall_seconds": dw,
        "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
        "formula": "observed_outer - direct_adapter - helper_reported_compute",
        "scope": "conservative entry plus return charge, not an observed prefix interval"}


class Ledger:
    def __init__(self, case, clock, writer):
        self.case, self.clock, self.writer = case, clock, writer
        self.count, self.records, self.pending, self.last = 0, [], [], None

    def identifier(self):
        self.count += 1
        return self.case+"/"+str(self.count)

    @contextmanager
    def span(self, label, paid=False, **context):
        record = {"id": self.identifier(), "case": self.case, "kind": "OBSERVED_SPAN",
                  "label": label, "paid": bool(paid), "context": context}
        start = self.clock.now()
        try:
            yield record["id"]
        finally:
            end = self.clock.now()
            record.update(start_cpu=start[0], start_wall=start[1], end_cpu=end[0], end_wall=end[1],
                          cpu_seconds=finite(end[0]-start[0], "span CPU"), wall_seconds=finite(end[1]-start[1], "span WALL"))
            self.records.append(record)
            self.pending.append(record)
            self.last = record

    def factory_report(self, outer, setup_wall):
        report = {"id": self.identifier(), "case": self.case, "kind": "REPORTED_DURATION", "paid": False,
            "label": "P43_backend_setup_reported", "wall_seconds": finite(setup_wall, "setup WALL"),
            "cpu_seconds": None, "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
            "helper_source_path": "research/P43_global_gain_probe.py", "helper_source_sha256": P43_SHA256,
            "outer_ref": outer["id"]}
        self.records.append(report)
        self.pending.append(report)
        difference = duration_difference(outer, report, self.identifier())
        self.records.append(difference)
        self.pending.append(difference)
        return report, difference

    def flush(self):
        while self.pending:
            self.writer.append("paid_ledger", self.pending[0])
            self.pending.pop(0)

    def grant(self):
        return sum(record["wall_seconds"] for record in self.records if record["paid"])


def select_dual_trace(trace, adapter_cpu, adapter_wall, grant, n):
    ac, aw, grant = finite(adapter_cpu, "adapter CPU"), finite(adapter_wall, "adapter WALL"), finite(grant, "grant")
    keys = ("cpu_seconds", "wall_seconds", "best_cut", "best_subset_packbits_little", "proposal_count", "stage")
    if any(key not in trace for key in keys):
        raise AuditFailure("missing trace columns")
    count = len(trace["cpu_seconds"])
    if count > MAX_TRACE or any(len(trace[key]) != count for key in keys):
        raise ResourceFailure("trace count/column guard", {"count": count})
    previous, previous_cut, selected = (-1.0, -1.0, -1), None, None
    for j in range(count):
        cpu, wall = finite(trace["cpu_seconds"][j], "checkpoint CPU"), finite(trace["wall_seconds"][j], "checkpoint WALL")
        cut, work = strict_int(trace["best_cut"][j], "checkpoint cut", 0), strict_int(trace["proposal_count"][j], "checkpoint work", 0)
        raw = list(trace["best_subset_packbits_little"][j])
        values = [strict_int(value, "packed byte", 0) for value in raw]
        if any(value > 255 for value in values):
            raise AuditFailure("packed byte exceeds255")
        packed = bytes(values)
        if len(packed) != (n+7)//8:
            raise AuditFailure("packed trace mask length")
        mask = checked_mask(int.from_bytes(packed, "little"), n)
        if work > MAX_WORK or cpu < previous[0] or wall < previous[1] or work < previous[2] or (previous_cut is not None and cut > previous_cut):
            raise AuditFailure("nonmonotone/overguard trace")
        if trace["stage"][j] not in STAGES:
            raise AuditFailure("unknown immutable P50 checkpoint stage")
        previous, previous_cut = (cpu, wall, work), cut
        if ac+cpu <= grant and aw+wall <= grant:
            selected = {"index": j, "cut": cut, "mask_hex": packed.hex(),
                "cpu_seconds": cpu, "wall_seconds": wall, "total_cpu": ac+cpu, "total_wall": aw+wall,
                "provenance": "archived_preclock_RAM_prefix"}
    return selected


def role(spec, case_id, arm, name, chain=-1, step=-1, index=0):
    return ("P90a", spec["root_seed"], case_id, arm, chain, step, name, index)


def seed_from_role(value, native=False):
    digest = hashlib.sha256(json.dumps(list(value), ensure_ascii=True, separators=(",", ":")).encode("ascii")).digest()
    return 1+int.from_bytes(digest[:4], "little") % (2**32-1) if native else int.from_bytes(digest[:8], "little")


def seed_integrity(spec):
    records, seen = [], {False: set(), True: set()}
    for case in spec["cases"]:
        cid = case["id"]
        pairs = [(role(spec, cid, "GEN", "weights"), False), (role(spec, cid, "B", "priority"), False)]
        for chain in range(spec["chains"]):
            pairs.append((role(spec, cid, "B", "reset_start", chain), False))
            for step in range(spec["steps"]):
                for name in ("portS", "portT", "split", "repair"):
                    pairs.append((role(spec, cid, "B", name, chain, step), False))
                pairs.append((role(spec, cid, "B", "native", chain, step), True))
        pairs.extend((role(spec, cid, mode, "control"), False) for mode in FAST_MODES)
        for value, native in pairs:
            seed = seed_from_role(value, native)
            if seed in seen[native]:
                raise AuditFailure("production role-seed collision", {"role": value, "native": native})
            seen[native].add(seed)
            records.append({"role": value, "native": native, "seed": seed})
    return records


def candidate_record(candidate, n):
    if candidate is None:
        return None
    return {"mask_u32": candidate.mask, "mask_hex": mask_hex(candidate.mask, n),
            "cut": candidate.cut, "sequence": candidate.sequence}


def endpoint_record(mask, value, n):
    return {"mask_u32": mask, "mask_hex": mask_hex(mask, n), "cut": value}


def run_b_case(raw_graph, case, spec, deps, writer, progress):
    cid, n, k = case["id"], spec["n"], spec["K"]
    stream = "B_"+cid[:2]
    ledger = Ledger(cid, deps.clock, writer)
    progress.update(case=cid, chain=None, step=None, pending=None, active_ledger=ledger)
    start = deps.clock.now()
    with ledger.span("case_private_setup", paid=True) as span:
        graph = validate_graph(raw_graph)
        if len(graph) != n or n != 2*k:
            raise AuditFailure("registered graph dimension mismatch")
        order = deps.permutation(role(spec, cid, "B", "priority"), list(range(n)))
        if sorted(order) != list(range(n)):
            raise AuditFailure("priority order is not a permutation")
        rank = [order.index(vertex) for vertex in range(n)]
        book = ScoreBook(graph, rank, deps, stream)
        book.owner_span = span
        progress["active_book"] = book
        total_weight = sum(sum(row) for row in graph)//2
    writer.append(stream, {"type": "case_start", "case": cid, "priority_rank": rank,
        "total_edge_weight": total_weight, "case_start_clocks": start})
    ledger.flush()
    requested = completed = raw_sum = q_sum = accepted_count = 0
    histogram, chains = [0]*(k+1), []
    for chain in range(spec["chains"]):
        deps.guard()
        progress.update(chain=chain, step=None)
        with ledger.span("reset_start_warmstart", paid=True, chain=chain) as span:
            book.owner_span = span
            book.start_chain(chain)
            subset = deps.permutation(role(spec, cid, "B", "reset_start", chain), list(range(n)))[:k]
            reset_mask = canonical_mask(mask_from_subset(subset, n), n, rank)
            reset_cut = book.scalar(reset_mask, "reset")
            warm = bounded_descent(book, reset_mask, reset_cut, spec["warmstart_scans"])
            current_mask, current_cut = warm.mask, warm.cut
            endpoint_mask, endpoint_cut = current_mask, current_cut
        book.flush(writer)
        writer.append(stream, {"type": "reset", "chain": chain, "reset_mask_u32": reset_mask,
            "reset_cut": reset_cut, "warmstart": warm, "own_scored_best": candidate_record(book.chain_best, n)})
        ledger.flush()
        for step in range(spec["steps"]):
            deps.guard()
            progress.update(chain=chain, step=step)
            with ledger.span("compile_all_M_transport_split", paid=True, chain=chain, step=step) as span:
                book.owner_span = span
                compiler_batch = book.batch(current_mask, current_cut, "compiler_M")
                progress["pending"] = ("compiler_M", cid, chain, step, compiler_batch)
                # The labeled V exists before ANY physical mark or split draw.
                compiled = deps.compile_matrix(compiler_batch)
                progress["pending"] = ("compiled", cid, chain, step, compiled)
                source_ports = tuple(deps.permutation(role(spec, cid, "B", "portS", chain, step), list(compiler_batch.inside)))
                target_ports = tuple(deps.permutation(role(spec, cid, "B", "portT", chain, step), list(compiler_batch.outside)))
                progress["pending"] = ("ports", cid, chain, step, compiled, source_ports, target_ports)
                routed = deps.transport(compiled, source_ports, target_ports)
                progress["pending"] = ("routed", cid, chain, step, compiled, source_ports, target_ports, routed)
                coins = tuple(strict_int(value, "split coin", 0) for value in deps.split_draws(role(spec, cid, "B", "split", chain, step), k))
                progress["pending"] = ("split", cid, chain, step, compiled, source_ports, target_ports, routed, coins)
                if len(coins) != k or any(value not in (0, 1) for value in coins):
                    raise AuditFailure("invalid balanced split coins")
                removed = tuple(i for i, value in enumerate(coins) if value == 0)
                native_role = role(spec, cid, "B", "native", chain, step)
                native_seed = deps.native_seed(native_role)
                repair_role = role(spec, cid, "B", "repair", chain, step)
                repair_seed = deps.control_seed(repair_role)
                before_mask, before_cut = current_mask, current_cut
                requested += 1
                progress["requested"] += 1
                progress["pending"] = (cid, chain, step, source_ports, target_ports, removed, native_seed)
            book.flush(writer)
            request = {"type": "attempt_request", "case": cid, "chain": chain, "step": step,
                "current_before": endpoint_record(before_mask, before_cut, n),
                "compiler": compiled, "routed": routed, "source_ports": source_ports,
                "target_ports": target_ports, "split_coins": coins, "removed_ports": removed,
                "native_role": native_role, "native_seed": native_seed, "repair_role": repair_role,
                "repair_seed": repair_seed, "full_source_photons": k}
            writer.append(stream, request)
            ledger.flush()
            progress["pending"] = request
            if removed:
                with ledger.span("factory_total", paid=False, chain=chain, step=step):
                    sampler, setup_wall = deps.make_sampler(routed.W, removed, native_seed)
                outer = ledger.last
                reported, difference = ledger.factory_report(outer, setup_wall)
                writer.append(stream, {"type": "factory_report", "chain": chain, "step": step,
                    "outer_ref": outer["id"], "reported_ref": reported["id"],
                    "duration_difference_ref": difference["id"], "backend_setup_wall": setup_wall})
                ledger.flush()
                with ledger.span("serial_native_sample", paid=False, chain=chain, step=step):
                    y, fallback = sampler()
                ledger.flush()
            else:
                y, fallback = (0,)*k, False
                writer.append(stream, {"type": "native_not_called", "chain": chain, "step": step, "reason": "r=0"})
            observation = {"type": "native_observation", "chain": chain, "step": step,
                           "receiver_counts": serial(y), "fallback": serial(fallback)}
            writer.append(stream, observation)
            progress["pending"] = {"request": request, "observation": observation}
            if fallback:
                raise AuditFailure("native fallback forbidden", observation)
            with ledger.span("decode_raw_Q_accept_bests", paid=True, chain=chain, step=step) as span:
                book.owner_span = span
                decoded = repair_counts(source_ports, target_ports, removed, y,
                    lambda available, count: deps.permutation(repair_role, available)[:count])
                proposal_mask = canonical_mask(decoded.mask, n, rank)
                raw_cut = book.scalar(proposal_mask, "raw_proposal")
                quenched = bounded_descent(book, proposal_mask, raw_cut, spec["quench_scans"])
                accepted = quenched.cut < current_cut
                if accepted:
                    current_mask, current_cut = quenched.mask, quenched.cut
                if quenched.cut < endpoint_cut:
                    endpoint_mask, endpoint_cut = quenched.mask, quenched.cut
                raw_sum += raw_cut
                q_sum += quenched.cut
                accepted_count += int(accepted)
                histogram[len(removed)] += 1
                completed += 1
                progress["completed"] += 1
                scored_best, global_best = book.chain_best, book.global_best
            book.flush(writer)
            writer.append(stream, {"type": "attempt_outcome", "chain": chain, "step": step,
                "decoded": decoded, "raw_cut": raw_cut, "quench": quenched, "accepted": accepted,
                "current_after": endpoint_record(current_mask, current_cut, n),
                "endpoint_best": endpoint_record(endpoint_mask, endpoint_cut, n),
                "own_scored_best": candidate_record(scored_best, n),
                "all_paid_best": candidate_record(global_best, n)})
            ledger.flush()
            progress["pending"] = None
        with ledger.span("own_chain_finalization", paid=True, chain=chain):
            chain_snapshot = (chain, warm.cut, book.chain_best, book.chain_best_phase,
                              endpoint_mask, endpoint_cut, current_mask, current_cut)
        chains.append({"chain": chain_snapshot[0], "warmstart_cut": chain_snapshot[1],
            "own_scored_best": candidate_record(chain_snapshot[2], n), "own_scored_best_phase": chain_snapshot[3],
            "endpoint_best": endpoint_record(chain_snapshot[4], chain_snapshot[5], n),
            "current": endpoint_record(chain_snapshot[6], chain_snapshot[7], n)})
        ledger.flush()
    with ledger.span("case_algorithm_finalization", paid=True):
        raw_mean = Fraction(raw_sum, completed)
        q_mean = Fraction(q_sum, completed)
        raw_normalized = Fraction(raw_sum, completed*total_weight) if total_weight else Fraction(0)
        q_normalized = Fraction(q_sum, completed*total_weight) if total_weight else Fraction(0)
        conditional_photons = sum(r*count for r, count in enumerate(histogram))
        final_best, compiler_best = book.global_best, book.compiler_best
    grant = ledger.grant()
    result = {"case": cid, "requested": requested, "completed": completed,
        "full_source_photons": k*completed, "conditional_receiver_photons": conditional_photons,
        "r_histogram": histogram, "chains": chains, "accepted_steps": accepted_count,
        "raw_mean_cut": raw_mean, "q_mean_cut": q_mean,
        "raw_mean_normalized": raw_normalized, "q_mean_normalized": q_normalized,
        "all_paid_best": candidate_record(final_best, n), "all_paid_best_phase": book.global_best_phase,
        "compiler_only_best": candidate_record(compiler_best, n), "scored_candidates": book.count,
        "grant_wall_seconds": grant, "paid_component_ids": [r["id"] for r in ledger.records if r["paid"]],
        "case_start_clocks": start, "case_end_clocks": deps.clock.now()}
    ledger.flush()
    writer.append(stream, {"type": "case_result", **result})
    writer.append(stream, {"type": "native_readback", "case": cid, "readback": deps.native_readback()})
    return result


def run_fast_control(raw_graph, case, mode, grant, spec, deps, writer):
    start = deps.clock.now()
    graph = [list(row) for row in raw_graph]
    seed_role = role(spec, case["id"], mode, "control")
    seed = deps.control_seed(seed_role)
    initialization = "random" if mode == "FAST_RANDOM" else "spectral"
    boundary = deps.clock.now()
    ac, aw = boundary[0]-start[0], boundary[1]-start[1]
    budget = max(0.0, grant-ac)
    result = deps.fast_solver(graph, seed, initialization, budget, MAX_WORK)
    end = deps.clock.now()
    outer_cpu, outer_wall = end[0]-start[0], end[1]-start[1]
    # Preserve the returned operands and complete cached trace before validating
    # any timing difference.  These exports do not create a candidate or score.
    prefix = case["id"]+"/"+mode
    reported = {"id": prefix+"/reported_compute", "case": case["id"], "mode": mode,
        "kind": "REPORTED_DURATION", "paid": False, "label": "P50_compute_reported",
        "cpu_seconds": result.get("compute_cpu_seconds"), "wall_seconds": result.get("compute_wall_seconds"),
        "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
        "helper_source_path": "research/P50_fast_from_scratch.py", "helper_source_sha256": P50_SHA256}
    observed_outer = {"id": prefix+"/outer", "kind": "OBSERVED_SPAN", "start_cpu": start[0],
        "start_wall": start[1], "end_cpu": end[0], "end_wall": end[1], "cpu_seconds": outer_cpu, "wall_seconds": outer_wall}
    observed_adapter = {"id": prefix+"/adapter", "kind": "OBSERVED_SPAN", "start_cpu": start[0],
        "start_wall": start[1], "end_cpu": boundary[0], "end_wall": boundary[1], "cpu_seconds": ac, "wall_seconds": aw}
    compact = {key: value for key, value in result.items() if key not in
        ("trace", "best_subset", "overall_completed_best_subset", "initial_subset")}
    writer.append("controls", {"type": "control_return_observation", "case": case["id"], "mode": mode,
        "grant": grant, "observed_outer": observed_outer, "observed_direct_adapter": observed_adapter,
        "reported_compute_duration": reported, "returned_scalar_metadata": compact})
    trace = result["trace"]
    packed_rows = []
    for row in trace.get("best_subset_packbits_little", ()):
        try:
            packed_rows.append(bytes(row).hex())
        except Exception as error:
            packed_rows.append({"invalid_packed_row": serial(row), "error_repr": repr(error)})
    stage_codes = [STAGES.index(stage) if stage in STAGES else {"unknown_stage": serial(stage)}
                   for stage in trace.get("stage", ())]
    writer.append("controls", {"type": "control_trace", "case": case["id"], "mode": mode,
        "cpu_seconds": trace.get("cpu_seconds"), "wall_seconds": trace.get("wall_seconds"), "best_cut": trace.get("best_cut"),
        "mask_hex": packed_rows, "proposal_count": trace.get("proposal_count"), "stage_code": stage_codes})
    difference = call_boundary_difference(outer_cpu, outer_wall, ac, aw,
        result["compute_cpu_seconds"], result["compute_wall_seconds"])
    difference.update(outer_ref=prefix+"/outer", direct_adapter_ref=prefix+"/adapter", reported_ref=reported["id"])
    cc, cw = ac+difference["cpu_seconds"], aw+difference["wall_seconds"]
    direct = select_dual_trace(trace, ac, aw, grant, len(graph))
    selected = select_dual_trace(trace, cc, cw, grant, len(graph))
    first = next((j for j, stage in enumerate(trace["stage"]) if stage == "initial_scan"), None)
    first_timely = first is not None and cc+trace["cpu_seconds"][first] <= grant and cw+trace["wall_seconds"][first] <= grant
    early_guard = bool(result["early_cap_inconclusive"])
    adequate = selected is not None and first_timely and not early_guard
    header = {"type": "control_header", "case": case["id"], "mode": mode, "grant": grant,
        "seed_role": seed_role, "seed": seed, "adapter_cpu": ac, "adapter_wall": aw, "solver_cpu_budget": budget,
        "observed_outer": observed_outer, "observed_direct_adapter": observed_adapter,
        "reported_compute_duration": reported, "call_boundary_difference": difference}
    writer.append("controls", header)
    if selected is not None:
        deps.verify_candidate(graph, read_mask_hex(selected["mask_hex"], len(graph)), selected["cut"])
    outcome = {"case": case["id"], "mode": mode, "grant": grant, "normal_return": True,
        "adapter_cpu": ac, "adapter_wall": aw, "selected": selected, "direct_selected": direct,
        "call_boundary_difference": difference, "first_scan_index": first,
        "first_scan_dual_timely": first_timely, "first_scan_cpu": None if first is None else cc+trace["cpu_seconds"][first],
        "first_scan_wall": None if first is None else cw+trace["wall_seconds"][first],
        "early_guard": early_guard, "adequate": adequate, "result": compact}
    writer.append("controls", {"type": "control_result", **outcome})
    return outcome


def classify_panel(B_cases, controls, case_ids):
    if len(case_ids) != 2 or set(B_cases) != set(case_ids):
        raise AuditFailure("classification requires both registered B cases")
    for cid in case_ids:
        row = B_cases[cid]
        if (strict_int(row["requested"], "requested", 0) != 48 or strict_int(row["completed"], "completed", 0) != 48
                or strict_int(row["full_source_photons"], "photons", 0) != 576):
            raise AuditFailure("classification requires complete B population")
    expected = [(mode, cid) for mode in FAST_MODES for cid in case_ids]
    if ([(row.get("mode"), row.get("case")) for row in controls] != expected
            or any(row.get("normal_return") is not True or row.get("adequate") is not True or row.get("selected") is None for row in controls)):
        return "INCONCLUSIVE_BASELINE_ELIGIBILITY"
    return "FOLLOWUP_REQUIRED" if all(strict_int(B_cases[row["case"]]["all_paid_best"]["cut"], "B cut", 0)
        < strict_int(row["selected"]["cut"], "control cut", 0) for row in controls) else "NO_POSITIVE_SIGNAL"


def run_workflow(spec, deps, writer):
    B_cases, controls, graphs = {}, [], {}
    progress = {"requested": 0, "completed": 0, "case": None, "chain": None, "step": None, "pending": None}
    population = [{"case": case["id"], "mode": mode, "status": "NOT_RUN", "outcome": None}
                  for mode in FAST_MODES for case in spec["cases"]]
    summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False, "B_cases": B_cases,
        "controls": controls, "control_population": population,
        "mandatory_followups": {name: {"status": "NOT_RUN", "outcome": None, "reason": "separate contract/ROOT authorization required"}
            for name in ("D_REOPT", "SPECIES_LE3", "EXACT_LOW_R", "INTENSITY_ROUTING", "BUNCH_REPAIR", "COMPILER_ONLY",
                         "HIGH_ORDER_FEASIBLE_FRONTIER", "PROJECTION_DPP", "RELABEL_FRESH_SEEDS", "HELDOUT", "REPLICATION")}}
    failure = {"status": "NO_FAILURE"}
    try:
        writer.single("metadata", {"spec": spec, "provenance": deps.native_readback(),
            "stage_dictionary": STAGES, "scope": "ideal zero-optics first gate; no matched hardware/CPU positive claim"})
        for case in spec["cases"]:
            deps.guard()
            start = deps.clock.now()
            graphs[case["id"]] = deps.generate_graph(case)
            end = deps.clock.now()
            writer.append("paid_ledger", {"id": "GEN/"+case["id"], "case": case["id"], "kind": "OBSERVED_SPAN",
                "label": "synthetic_problem_input_generation", "paid": False, "start_cpu": start[0], "start_wall": start[1],
                "end_cpu": end[0], "end_wall": end[1], "cpu_seconds": end[0]-start[0], "wall_seconds": end[1]-start[1]})
        writer.single("graphs", {"cases": graphs, "recipes": spec["cases"]})
        for case in spec["cases"]:
            B_cases[case["id"]] = run_b_case(graphs[case["id"]], case, spec, deps, writer, progress)
            progress.pop("active_ledger", None)
            progress.pop("active_book", None)
        if progress["completed"] != 96:
            raise AuditFailure("registered96 B population incomplete")
        for mode in FAST_MODES:
            for case in spec["cases"]:
                deps.guard()
                progress.update(case=case["id"], chain=None, step=None, pending=("control", mode, case["id"]))
                entry = next(row for row in population if row["mode"] == mode and row["case"] == case["id"])
                entry["status"] = "REQUESTED"
                outcome = run_fast_control(graphs[case["id"]], case, mode, B_cases[case["id"]]["grant_wall_seconds"], spec, deps, writer)
                controls.append(outcome)
                entry.update(status="COMPLETE", outcome={"selected": outcome["selected"], "adequate": outcome["adequate"]})
        summary["status"] = classify_panel(B_cases, controls, [case["id"] for case in spec["cases"]])
        summary.update(requested_B_attempts=progress["requested"], completed_B_attempts=progress["completed"],
            modeled_full_source_photons=spec["K"]*progress["requested"], modeled_completed_source_photons=spec["K"]*progress["completed"],
            native_final_readback=deps.native_readback(), workflow_before_final_evidence_clocks=deps.clock.now(),
            serialization_io_before_final={"cpu_seconds": getattr(writer, "io_cpu", None), "wall_seconds": getattr(writer, "io_wall", None),
                "scope": "completed serialized writes; final summary/failure excluded"})
        if hasattr(deps, "start"):
            end = summary["workflow_before_final_evidence_clocks"]
            summary["whole_run_before_final_evidence"] = {"cpu_seconds": end[0]-deps.start[0], "wall_seconds": end[1]-deps.start[1]}
        deps.guard()
    except Exception as error:
        ledger, book = progress.pop("active_ledger", None), progress.pop("active_book", None)
        try:
            if book is not None:
                book.flush(writer)
            if ledger is not None:
                ledger.flush()
        except Exception as flush_error:
            progress["flush_exception_repr"] = repr(flush_error)
        summary.update(status="INCONCLUSIVE_RESOURCE_FAILURE" if isinstance(error, ResourceFailure) else "INCONCLUSIVE_FIRST_FAILURE",
            requested_B_attempts=progress["requested"], completed_B_attempts=progress["completed"],
            modeled_full_source_photons=spec["K"]*progress["requested"], modeled_completed_source_photons=spec["K"]*progress["completed"])
        failure = {"status": "FIRST_FAILURE", "exception_type": type(error).__name__, "exception_repr": repr(error),
            "payload": getattr(error, "payload", None), "progress": progress, "remaining": "NOT_RUN; no retry"}
    finally:
        summary = writer.finish(summary, failure)
    return summary


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_spec(spec):
    for field, expected in (("n", 24), ("K", 12), ("chains", 3), ("steps", 16), ("root_seed", 90026001),
            ("exponent_scale", 1), ("warmstart_scans", 2), ("quench_scans", 1), ("FAST_work_guard", MAX_WORK), ("FAST_trace_cap", MAX_TRACE)):
        if strict_int(spec[field], "spec/"+field, 0) != expected:
            raise AuditFailure("frozen spec integer mismatch", {"field": field})
    expected_cases = [
        {"id": "ER9002401", "generator": "gnp_random_graph", "n": 24, "edge_probability": 0.4, "seed": 9002401},
        {"id": "RR9002402", "generator": "random_regular_graph", "n": 24, "degree": 4, "seed": 9002402}]
    if spec["cases"] != expected_cases or spec["FAST_modes"] != list(FAST_MODES) or spec["trace_stage_dictionary"] != list(STAGES):
        raise AuditFailure("frozen cases/modes/stages mismatch")
    if spec["split_probability"] != [1, 2] or spec["positive_accepted"] is not False or spec["flatness_is_main_guard"] is not False:
        raise AuditFailure("frozen split/scope mismatch")
    for field, expected in (("CPU_seconds", 60), ("threads", 1), ("native_threads", 1), ("workers", 1),
            ("failed_retries", 0), ("scientific_bytes", MAX_BYTES), ("reserved_final_bytes", RESERVE),
            ("single_JSON_or_line_bytes", MAX_OBJECT), ("log_bytes", 4194304), ("logical_bytes_PLAN", 268435456)):
        if strict_int(spec["limits"][field], "spec/limits/"+field, 0) != expected:
            raise AuditFailure("frozen limit mismatch", {"field": field})
    numeric_cap(spec["limits"]["wall_seconds"], 90, "spec/WALL")
    numeric_cap(spec["guard_absolute"], 3e-12, "spec/absolute guard")
    numeric_cap(spec["guard_relative"], 0, "spec/relative guard")
    if len(spec["execution_artifacts"]) != 18 or len(set(spec["execution_artifacts"])) != 18 or len(spec["external_artifacts"]) != 18:
        raise AuditFailure("frozen input/pin population mismatch")


def project_input(root, relative):
    relative_path = Path(relative)
    if relative_path.is_absolute() or not relative_path.parts or any(part in (".", "..") for part in relative_path.parts):
        raise AuditFailure("unsafe project input", {"path": relative})
    current = root
    for part in relative_path.parts:
        current = current/part
        if current.is_symlink():
            raise AuditFailure("symlink project input", {"path": relative})
    if not current.is_file() or not current.resolve().is_relative_to(root.resolve()):
        raise AuditFailure("missing/outside project input", {"path": relative})
    return current


def checked_inputs(root, spec):
    validate_spec(spec)
    immutable, closure, external, software = [], [], [], {}
    for expected in spec["immutable_inputs"]:
        actual = file_sha256(project_input(root, expected["path"]))
        record = {**expected, "actual_sha256": actual}
        immutable.append(record)
        if actual != expected["sha256"]:
            raise AuditFailure("immutable input mismatch", record)
    for relative in spec["execution_artifacts"]:
        closure.append({"path": relative, "sha256": file_sha256(project_input(root, relative))})
    for expected in spec["external_artifacts"]:
        actual = file_sha256(expected["path"])
        record = {**expected, "actual_sha256": actual}
        external.append(record)
        if actual != expected["sha256"]:
            raise AuditFailure("external critical pin mismatch", record)
    for name, expected in spec["software"].items():
        actual = platform.python_version() if name == "Python" else importlib.metadata.version(name)
        software[name] = actual
        if actual != expected:
            raise AuditFailure("software version mismatch", {"name": name, "actual": actual, "expected": expected})
    actual_interpreter = {"path": str(Path(sys.executable).resolve()), "sha256": file_sha256(Path(sys.executable).resolve())}
    interpreter_pin = next(row for row in spec["external_artifacts"] if row["role"] == "physical_interpreter")
    if actual_interpreter["sha256"] != interpreter_pin["sha256"]:
        raise AuditFailure("actual interpreter hash mismatch", actual_interpreter)
    return {"immutable_inputs": immutable, "project_input_hashes": closure, "external_inputs": external,
        "software": software, "interpreter": sys.executable, "resolved_interpreter": str(Path(sys.executable).resolve()),
        "actual_interpreter": actual_interpreter,
        "external_binding": "preimport source-enforced hashes; external paths are not runner --inputs"}


def load_helper(path, name):
    descriptor = importlib.util.spec_from_file_location(name, path)
    if descriptor is None or descriptor.loader is None:
        raise AuditFailure("cannot locate frozen helper", {"path": str(path)})
    module = importlib.util.module_from_spec(descriptor)
    sys.modules[name] = module
    descriptor.loader.exec_module(module)
    return module


class NativeDependencies:
    """Only authorized main constructs this; fixture hooks never do."""
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
        from scipy.linalg import expm
        self.np, self.nx, self.expm = np, nx, expm
        self.p43 = load_helper(root/"research/P43_global_gain_probe.py", "_p90a_immutable_p43")
        self.p50 = load_helper(root/"research/P50_fast_from_scratch.py", "_p90a_immutable_p50")
        loaded = {}
        for pin_role, module_name in (
                ("serial_sampling_backend", "perceval.backends._clifford2017"),
                ("deterministic_qualification_backend", "perceval.backends._naive"),
                ("backend_circuit_input_convention", "perceval.backends._abstract_backends"),
                ("native_seed_bridge", "perceval.utils._random"),
                ("seed_bridge_export", "perceval.utils"), ("native_extension", "exqalibur.exqalibur"),
                ("eigvalsh_python", "numpy.linalg._linalg"), ("eigvalsh_native", "numpy.linalg._umath_linalg"),
                ("PCG64_native", "numpy.random._pcg64"), ("array_native", "numpy._core._multiarray_umath"),
                ("expm_python", "scipy.linalg._matfuncs"), ("expm_native", "scipy.linalg._matfuncs_expm")):
            module = importlib.import_module(module_name)
            path = Path(module.__file__).resolve()
            observed = {"module": module_name, "path": str(path), "sha256": file_sha256(path)}
            loaded[pin_role] = observed
            expected = next(row for row in spec["external_artifacts"] if row["role"] == pin_role)
            if observed["sha256"] != expected["sha256"]:
                raise AuditFailure("actually loaded critical module hash mismatch", observed)
        self.provenance["actually_loaded_critical_modules"] = loaded
        # Integrity metadata only: each actually used role is rederived and paid.
        self.provenance["role_seeds"] = seed_integrity(spec)
        self.native_readback()

    def guard(self):
        now = self.clock.now()
        cpu, wall = now[0]-self.start[0], now[1]-self.start[1]
        if cpu > self.spec["limits"]["CPU_seconds"] or wall > self.spec["limits"]["wall_seconds"]:
            raise ResourceFailure("registered global allowance exhausted", {"cpu_seconds": cpu, "wall_seconds": wall})

    def native_readback(self):
        value = self.xq.Config.compute_max_thread_count
        value = value() if callable(value) else value
        if value != 1:
            raise AuditFailure("native thread readback mismatch", {"observed_repr": repr(value)})
        environment = {name: os.environ.get(name) for name in self.spec["thread_environment"]}
        if any(item != "1" for item in environment.values()):
            raise AuditFailure("current thread environment readback mismatch", {"environment_threads": environment})
        return {"native_threads": int(value), "environment_threads": environment, "provenance": self.provenance}

    def control_seed(self, value):
        return seed_from_role(value)

    def rng(self, value):
        return self.np.random.Generator(self.np.random.PCG64(self.control_seed(value)))

    def native_seed(self, value):
        return seed_from_role(value, native=True)

    def permutation(self, value, values):
        return [int(item) for item in self.rng(value).permutation(values)]

    def split_draws(self, value, count):
        return [int(item) for item in self.rng(value).integers(0, 2, size=count)]

    def cut(self, graph, mask):
        return scalar_cut(graph, mask)

    def swap_batch(self, graph, mask, rank, base_cut, degree):
        return exact_swap_batch(graph, mask, rank, base_cut, degree)

    def compile_matrix(self, batch):
        return compile_feature(batch, self.np, self.expm)

    def transport(self, compiled, source_ports, target_ports):
        return transport_feature(compiled, source_ports, target_ports)

    def make_sampler(self, W, sorted_removed_ports, native_seed):
        return self.p43.make_optical_sampler(self.np.asarray(W, dtype=self.np.complex128),
                                            list(sorted_removed_ports), "bosonic", native_seed)

    def fast_solver(self, graph, seed, initialization, cpu_budget_seconds, max_proposals):
        return self.p50.solve_from_raw(graph, seed=seed, initialization=initialization,
            cpu_budget_seconds=cpu_budget_seconds, max_proposals=max_proposals)

    def verify_candidate(self, graph, mask, value):
        if scalar_cut(graph, mask) != value:
            raise AuditFailure("selected preexisting control mask/cut mismatch")

    def generate_graph(self, case):
        if case["generator"] == "gnp_random_graph":
            topology = self.nx.gnp_random_graph(case["n"], case["edge_probability"], seed=case["seed"])
        elif case["generator"] == "random_regular_graph":
            topology = self.nx.random_regular_graph(case["degree"], case["n"], seed=case["seed"])
        else:
            raise AuditFailure("unregistered graph generator")
        edges = sorted((min(int(u), int(v)), max(int(u), int(v))) for u, v in topology.edges())
        weights = self.rng(role(self.spec, case["id"], "GEN", "weights")).integers(1, 6, size=len(edges))
        graph = [[0]*case["n"] for _ in range(case["n"])]
        for (u, v), value in zip(edges, weights):
            graph[u][v] = graph[v][u] = int(value)
        return graph


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    root, start, writer = Path(__file__).resolve().parents[1], SystemClock().now(), None
    try:
        if Path(sys.executable).absolute() != Path(PERSISTENT_PYTHON):
            raise AuditFailure("main requires frozen persistent interpreter", {"actual": sys.executable})
        if args.spec.absolute() != root/"research/P90a_execution_spec.json" or file_sha256(args.spec) != SPEC_SHA256:
            raise AuditFailure("only exact frozen literal spec is authorized")
        spec = json.loads(args.spec.read_text(encoding="ascii"))
        validate_spec(spec)
        if args.output.absolute() != root/spec["main_output"]:
            raise AuditFailure("only exact frozen scientific output is authorized")
        writer = EvidenceWriter(args.output, spec["limits"]["scientific_bytes"], spec["limits"]["reserved_final_bytes"])
        for name in spec["thread_environment"]:
            os.environ[name] = "1"
        if any(os.environ.get(name) != "1" for name in spec["thread_environment"]):
            raise AuditFailure("thread environment readback mismatch")
        provenance = checked_inputs(root, spec)
        provenance["environment_threads"] = {name: os.environ[name] for name in spec["thread_environment"]}
        import_start = SystemClock().now()
        deps = NativeDependencies(root, spec, provenance, start)
        import_end = deps.clock.now()
        provenance["excluded_import_configuration_span"] = {"start_cpu": import_start[0], "start_wall": import_start[1],
            "end_cpu": import_end[0], "end_wall": import_end[1], "cpu_seconds": import_end[0]-import_start[0],
            "wall_seconds": import_end[1]-import_start[1]}
        summary = run_workflow(spec, deps, writer)
        return int(summary["status"] in ("INCONCLUSIVE_FIRST_FAILURE", "INCONCLUSIVE_RESOURCE_FAILURE"))
    except Exception as error:
        if writer is not None and not writer.finish_attempted:
            writer.finish({"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False,
                "B_cases": None, "controls": None, "population_status": "NOT_RUN"},
                {"status": "FIRST_FAILURE", "exception_type": type(error).__name__, "exception_repr": repr(error),
                 "payload": getattr(error, "payload", None)})
        else:
            sys.stderr.write(json.dumps({"status": "INCONCLUSIVE_FIRST_FAILURE", "exception_repr": repr(error)})+"\n")
        return 1
    finally:
        if writer is not None:
            writer.close()


if __name__ == "__main__":
    raise SystemExit(main())
