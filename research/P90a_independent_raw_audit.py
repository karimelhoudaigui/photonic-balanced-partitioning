"""Independent P90a sealed-record auditor. Import performs no replay or RNG work.

Scientific dependencies are constructed only behind a verified POST-SEAL token.
No producer, P43/P50, SciPy exponential or optical backend is imported.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import sys
import time
import xml.etree.ElementTree as ET

CASES = ("ER9002401", "RR9002402")
FAST = ("FAST_RANDOM", "FAST_SPECTRAL")
STAGES = ("initialization", "initial_scan", "descent_scan", "anneal_setup",
          "anneal", "uniform_restart", "perturb_best")
FILES = ("metadata.json", "graphs.json", "B_ER.jsonl", "B_RR.jsonl",
         "paid_ledger.jsonl", "controls.jsonl", "summary.json", "failure.json")
FOLLOWUPS = ("D_REOPT", "SPECIES_LE3", "EXACT_LOW_R", "INTENSITY_ROUTING",
             "BUNCH_REPAIR", "COMPILER_ONLY", "HIGH_ORDER_FEASIBLE_FRONTIER",
             "PROJECTION_DPP", "RELABEL_FRESH_SEEDS", "HELDOUT", "REPLICATION")
FREEZE = "82d7b63d35f2f0495df6ed9c0d86999b649c44ff"
EXPECTED_PRODUCER_COMMIT = "b2f9af31af86c83d8aef8841891c4d37832c69e5"
P43_SHA = "b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777"
P50_SHA = "6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86"
PRIMARY_PINS = {
    "research/P90_SOURCE_AWARE_NONFLAT_DESIGN.md": "b3c0b04c486f3368a0cbbc7e2030d8225d015f182cbfb00e0a9b63e0a0b2f173",
    "research/P90_SOURCE_AWARE_NONFLAT_EXACT_REVIEW.md": "ad2a473b7b37da806b7e327e07ca6273278dbbffd0f6cf5d271a99865589f4d5",
    "research/P90_BOUNDED_PRIMARY_LITERATURE_CHECK.md": "fa1c2be4a2b148450653207befe4cd4647dfef10f1147b0d1b03ce978a94e831",
    "research/P90a_DEV_VETO_CONTRACT.md": "dfdcabfd93cf1a1e0d06fb370ad295123c1726247857820acab9f5d08d04c660",
    "research/P90a_INDEPENDENT_CARD_REVIEW.md": "2372e0c2d8709ac722959166cc91767e059379d348949b27a4e3b20a8ef9e58e",
    "research/P90a_IMPLEMENTATION_API.md": "8c153fc538dd8b789239e25f814126e2e37c9a422778bed1bbd45b60a9645ca5",
    "research/P90a_source_bound_nonflat_veto.py": "95fa65c6c04a0d48bb29c5d38b4bb1cac1cfdc22170191ee49a280f2995098e1",
    "tests/test_p90a_source_bound_nonflat_veto.py": "9fba751e5bc2970e77e63a1d45a751c4a3e788f64b2f718fb7b26d8fee6dc9ec",
    "research/P90a_execution_spec.json": "87dda967c662b0507c364d216f2c1a937d6a83e8616b536b7a0330bd90be0e7f",
    "research/P90a_preflight_contract.json": "16e8ee28db9a26215fb22a12df8dcb3941ac957bc2c76ce1606ee1e0d3bfdfd7",
    "research/P90a_execution_contract.json": "0ed33b3d86e25eaa2e946506c52dcc510c89b633eabb61d68da7ed4e2d58b707",
    "research/P90a_IMPLEMENTATION_POPULATION.md": "54e69aad02836d0e3f6c48de9b3cbbabd3f66117a20b9e3391ae92a0455b1e9f",
    "research/P43_global_gain_probe.py": P43_SHA,
    "research/P50_fast_from_scratch.py": P50_SHA,
    "research/P50_FAST_FROM_RAW_API_CARD.md": "3a73269e3a98f853a2a7d0695f77e9efa06f65ad0914daf932ea1715c162ad91"}
PRIMARY_INPUTS = ("AGENTS.md", "pyproject.toml", "requirements-research-lock.txt", *PRIMARY_PINS)
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
RAW_BYTES, LINE_BYTES, OUTPUT_BYTES = 33554432, 4194304, 524288
MAX_B_ROWS, MAX_LEDGER_ROWS, MAX_CONTROL_ROWS = 2000, 2000, 20
MAX_TRACE, MAX_WORK = 40000, 1000000
TAYLOR_DEGREE, MATRIX_TOL, SPECTRUM_TOL, GUARD_TOL = 40, 3e-11, 2e-9, 3e-12
QUALIFICATION_ITEMS = 29
_POST_SEAL = object()


class AuditIssue(Exception):
    def __init__(self, category, location, message, detail=None):
        super().__init__(message)
        self.category, self.location, self.detail = category, location, detail


class PrefixEnd(Exception):
    """An explicitly failed producer may end at this retained event prefix."""


def insist(condition, location, message, detail=None, category="MISMATCH"):
    if not condition:
        raise AuditIssue(category, location, message, detail)


def integer(value, location, minimum=None):
    insist(type(value) is int, location, "strict integer required", repr(value), "MALFORMED")
    insist(minimum is None or value >= minimum, location, "integer below minimum", value, "MALFORMED")
    return value


def number(value, location, nonnegative=True):
    insist(type(value) in (int, float) and math.isfinite(value), location,
           "finite numeric scalar required", repr(value), "MALFORMED")
    insist(not nonnegative or value >= 0, location, "negative scalar", value, "MALFORMED")
    return float(value)


def same(actual, expected, location):
    if type(expected) in (list, tuple):
        insist(type(actual) is type(expected) and len(actual) == len(expected), location,
               "sequence type/length mismatch", category="MALFORMED")
        for i, (a, e) in enumerate(zip(actual, expected)):
            same(a, e, location+"/"+str(i))
        return
    if type(expected) is dict:
        insist(type(actual) is dict and set(actual) == set(expected), location,
               "object keys mismatch", category="SCHEMA")
        for key, e in expected.items():
            same(actual[key], e, location+"/"+key)
        return
    if type(expected) in (int, bool):
        insist(type(actual) is type(expected), location, "scalar type mismatch", repr(actual), "MALFORMED")
    insist(actual == expected, location, "record disagrees", {"actual": actual, "expected": expected})


def exact_numeric(value, expected, location):
    same(number(value, location), float(expected), location)


def near(value, expected, location, tolerance=MATRIX_TOL):
    insist(abs(value-expected) <= tolerance, location, "frozen absolute tolerance exceeded",
           {"actual": repr(value), "expected": repr(expected), "abs_tolerance": tolerance})


def zvalue(value, location):
    insist(type(value) is dict and set(value) == {"real", "imag"}, location,
           "complex pair required", category="MALFORMED")
    return complex(number(value["real"], location, False), number(value["imag"], location, False))


def graph_checked(graph):
    n = len(graph)
    insist(2 <= n <= 24 and n % 2 == 0 and all(type(row) is list and len(row) == n for row in graph),
           "graph", "bounded even square adjacency", category="MALFORMED")
    for i in range(n):
        for j in range(n):
            integer(graph[i][j], "graph/weight", 0)
            same(graph[i][j], graph[j][i], "graph/symmetry")
        same(graph[i][i], 0, "graph/diagonal")
    return graph


def mask_checked(mask, n):
    integer(mask, "mask", 0)
    insist(mask < 1 << n and mask.bit_count() == n//2, "mask", "padding/cardinality", category="MALFORMED")
    return mask


def membership(values, n):
    same(len(values), n//2, "subset/size")
    mask = 0
    for v in values:
        integer(v, "subset/vertex", 0)
        insist(v < n and not mask & (1 << v), "subset", "duplicate/outside vertex", category="MALFORMED")
        mask |= 1 << v
    return mask_checked(mask, n)


def vertices(mask, n):
    return [v for v in range(n) if mask & (1 << v)]


def mask_hex(mask, n):
    return mask_checked(mask, n).to_bytes((n+7)//8, "little").hex()


def mask_read(text, n):
    insist(type(text) is str and len(text) == 2*((n+7)//8), "mask", "packed length", category="MALFORMED")
    try:
        raw = bytes.fromhex(text)
    except ValueError as error:
        raise AuditIssue("MALFORMED", "mask", "hex encoding") from error
    same(raw.hex(), text, "mask/canonical-hex")
    return mask_checked(int.from_bytes(raw, "little"), n)


def rank_checked(rank, n):
    insist(type(rank) is list and all(type(v) is int for v in rank) and sorted(rank) == list(range(n)),
           "priority", "rank permutation", category="MALFORMED")
    return rank


def orient(mask, rank):
    mask_checked(mask, len(rank))
    return mask if mask & (1 << rank.index(0)) else mask ^ ((1 << len(rank))-1)


def integer_cut(graph, mask):
    """Complete independent unordered-edge sum, never producer deltas."""
    mask_checked(mask, len(graph))
    return sum(graph[a][b] for a in range(len(graph)) for b in range(a+1, len(graph))
               if bool(mask & (1 << a)) != bool(mask & (1 << b)))


def swap_data(graph, mask, rank):
    inside = sorted(vertices(mask, len(graph)), key=rank.__getitem__)
    outside = sorted((v for v in range(len(graph)) if not mask & (1 << v)), key=rank.__getitem__)
    masks = [orient(mask ^ (1 << a) ^ (1 << b), rank) for a in inside for b in outside]
    return inside, outside, masks, [integer_cut(graph, m) for m in masks]


def matrix_read(raw, k, location):
    insist(type(raw) is list and len(raw) == k and all(type(row) is list and len(row) == k for row in raw),
           location, "square matrix dimension", category="MALFORMED")
    return [[zvalue(z, location) for z in row] for row in raw]


def matmul(a, b):
    k = len(a)
    return [[sum((a[i][q]*b[q][j] for q in range(k)), 0j) for j in range(k)] for i in range(k)]


def taylor40(h, d):
    """Scalar-complex recurrence; no primary/SciPy expm or eigenvector oracle."""
    k = len(h)
    number(d, "Taylor/d")
    insist(d >= 1 and k <= 12, "Taylor", "normalizer/dimension", category="MALFORMED")
    a = [[-1j*z/d for z in row] for row in h]
    insist(sum(abs(z)**2 for row in a for z in row) <= 16, "Taylor", "Frobenius guard >4")
    term = [[complex(i == j) for j in range(k)] for i in range(k)]
    result = [row[:] for row in term]
    for degree in range(1, TAYLOR_DEGREE+1):
        term = [[z/degree for z in row] for row in matmul(term, a)]
        result = [[result[i][j]+term[i][j] for j in range(k)] for i in range(k)]
    return result


def gram_error(w):
    k = len(w)
    return max(abs(sum(w[a][i].conjugate()*w[a][j] for a in range(k))-int(i == j))
               for i in range(k) for j in range(k))


def compiler_check(graph, mask, rank, recorded, routed, source, target, eigenvalues):
    inside, outside, _, cuts = swap_data(graph, mask, rank)
    k, base = len(inside), integer_cut(graph, mask)
    m = [[cuts[i*k+a]-base for i in range(k)] for a in range(k)]
    h = [[complex(Fraction(m[a][i]+m[i][a], 2), Fraction(m[a][i]-m[i][a], 2))
          for i in range(k)] for a in range(k)]
    same(recorded["source_order"], inside, "compiler/source-order")
    same(recorded["target_order"], outside, "compiler/target-order")
    same(recorded["M"], m, "compiler/full-transposed-M")
    actual_h = matrix_read(recorded["H"], k, "compiler/H")
    same(actual_h, h, "compiler/exact-H")
    ev = [number(x, "compiler/eigenvalue", False) for x in recorded["eigenvalues"]]
    expected_ev = list(eigenvalues(h))
    same(len(ev), k, "compiler/spectrum-size")
    same(len(expected_ev), k, "compiler/independent-spectrum-size")
    for actual, expected in zip(ev, expected_ev):
        near(actual, number(expected, "eigh/eigenvalue", False), "compiler/eigh", SPECTRUM_TOL)
    d = number(recorded["d"], "compiler/d")
    near(d, max(1.0, max(abs(x) for x in expected_ev)), "compiler/independent-d", SPECTRUM_TOL)
    v = matrix_read(recorded["V"], k, "compiler/V")
    expected_v = taylor40(h, d)
    for a in range(k):
        for i in range(k):
            near(v[a][i], expected_v[a][i], "compiler/Taylor-V")
    verr = gram_error(v)
    insist(verr <= GUARD_TOL, "compiler", "V Gram guard")
    near(number(recorded["v_gram_error"], "V/recorded-guard"), verr, "V/guard", GUARD_TOL)
    near(number(recorded["nonflat_max"], "V/nonflat"), max(abs(abs(z)**2-1/k) for row in v for z in row), "V/nonflat")
    near(number(recorded["ipr_sum"], "V/IPR"), sum(abs(z)**4 for row in v for z in row), "V/IPR")
    same(sorted(source), sorted(inside), "ports/source-permutation")
    same(sorted(target), sorted(outside), "ports/target-permutation")
    expected_w = [[v[outside.index(a)][inside.index(i)] for i in source] for a in target]
    w = matrix_read(routed["W"], k, "compiler/W")
    same(w, expected_w, "compiler/exact-rounded-transport")
    werr = gram_error(w)
    frame = max(abs(0.5*int(i == j)+0.5*sum(w[a][i].conjugate()*w[a][j] for a in range(k))-int(i == j))
                for i in range(k) for j in range(k))
    insist(max(werr, frame) <= GUARD_TOL, "compiler", "transport/frame guard")
    near(number(routed["w_gram_error"], "W/guard"), werr, "W/recorded-guard", GUARD_TOL)
    near(number(routed["frame_gram_error"], "frame/guard"), frame, "frame/recorded-guard", GUARD_TOL)


def decoded_check(source, target, removed, y, recorded, choose):
    k = len(source)
    same(sorted(source+target), list(range(2*k)), "ports/partition")
    insist(removed == sorted(set(removed)) and all(type(v) is int and 0 <= v < k for v in removed),
           "removed", "sorted distinct input ports", category="MALFORMED")
    insist(type(y) is list and len(y) == k and all(type(v) is int and v >= 0 for v in y),
           "counts", "full nonnegative integer receiver vector", category="MALFORMED")
    same(sum(y), len(removed), "counts/receiver-sum")
    support = [target[a] for a, value in enumerate(y) if value]
    available, need = sorted(set(target)-set(support)), len(removed)-len(support)
    used = 0 < need < len(available)
    fill = choose(available, need) if used else available if need else []
    same(recorded["fill"], fill, "decoder/uniform-fill")
    same(recorded["repair_used"], used, "decoder/repair-used")
    kept = [int(i not in removed) for i in range(k)]
    full, mapped = kept+y, [0]*(2*k)
    for port, count in enumerate(full):
        mapped[(source+target)[port]] = count
    selected = [source[i] for i in range(k) if i not in removed]+support+fill
    mask = membership(selected, 2*k)
    for key, expected in (("kept_counts", kept), ("receiver_counts", y), ("full_counts", full),
                          ("vertex_counts", mapped), ("removed_vertices", [source[i] for i in removed]),
                          ("r", len(removed)), ("h", len(support)), ("mask", mask)):
        same(recorded[key], expected, "decoder/"+key)
    same(sum(full), k, "counts/full-injected-photons")
    return mask


def observed_span(row):
    same(row["kind"], "OBSERVED_SPAN", "clock/kind")
    for domain in ("cpu", "wall"):
        start = number(row["start_"+domain], "clock/start")
        end = number(row["end_"+domain], "clock/end")
        insist(end >= start, "clock", "reversed endpoints", category="MALFORMED")
        same(number(row[domain+"_seconds"], "clock/duration"), end-start, "clock/exact-endpoint-duration")


def ledger_checked(rows):
    paid_labels = {"case_private_setup", "reset_start_warmstart", "compile_all_M_transport_split",
                   "decode_raw_Q_accept_bests", "own_chain_finalization", "case_algorithm_finalization"}
    free_labels = {"synthetic_problem_input_generation", "factory_total", "serial_native_sample"}
    by_id, spans, order, paid, previous = {}, {}, {c: [] for c in CASES}, {c: [] for c in CASES}, {}
    for row in rows:
        identity, case = row["id"], row["case"]
        insist(type(identity) is str and identity not in by_id and case in CASES,
               "ledger", "unique ID/registered case", category="MALFORMED")
        by_id[identity] = row
        if row["kind"] == "OBSERVED_SPAN":
            observed_span(row)
            label = row["label"]
            insist(label in paid_labels | free_labels, "ledger", "unknown clock label", label, "SCHEMA")
            same(row["paid"], label in paid_labels, "ledger/payment-scope")
            context = row.get("context", {})
            key = (case, label, context.get("chain"), context.get("step"))
            insist(key not in spans, "ledger", "duplicate algorithmic span", key)
            spans[key] = row
            if case in previous:
                insist(row["start_cpu"] >= previous[case][0] and row["start_wall"] >= previous[case][1],
                       "ledger", "observed spans overlap/reverse")
            previous[case] = row["end_cpu"], row["end_wall"]
        elif row["kind"] == "REPORTED_DURATION":
            same(row["paid"], False, "factory/reported-unpaid")
            same(row["label"], "P43_backend_setup_reported", "factory/report-label")
            same(row["helper_source_path"], "research/P43_global_gain_probe.py", "factory/helper-path")
            same(row["helper_source_sha256"], P43_SHA, "factory/helper-pin")
            for key in ("cpu_seconds", "start_cpu", "end_cpu", "start_wall", "end_wall"):
                same(row[key], None, "factory/unknown-"+key)
            number(row["wall_seconds"], "factory/reported-WALL")
            outer = by_id.get(row["outer_ref"])
            insist(outer is not None and outer["label"] == "factory_total" and outer["case"] == case,
                   "factory", "reported duration links prior same-case outer")
        elif row["kind"] == "DURATION_DIFF":
            same(row["paid"], True, "factory/residual-paid")
            same(row["label"], "factory_prefix_plus_return_residual", "factory/residual-label")
            outer, report = by_id.get(row["outer_ref"]), by_id.get(row["reported_ref"])
            insist(outer is not None and report is not None and report["kind"] == "REPORTED_DURATION"
                   and report["outer_ref"] == outer["id"] and outer["case"] == report["case"] == case,
                   "factory", "typed residual operand references")
            for key in ("cpu_seconds", "start_cpu", "end_cpu", "start_wall", "end_wall"):
                same(row[key], None, "factory/derived-unknown-"+key)
            same(row["formula"], "factory_outer_wall - helper_reported_setup_wall", "factory/formula")
            difference = outer["wall_seconds"]-report["wall_seconds"]
            insist(difference >= 0, "factory", "negative un-clipped duration difference")
            same(number(row["wall_seconds"], "factory/residual"), difference, "factory/residual-value")
        else:
            raise AuditIssue("SCHEMA", "ledger", "unknown typed clock kind", row["kind"])
        order[case].append(identity)
        if row["paid"]:
            paid[case].append(identity)
    residual_operands = [r["outer_ref"] for r in by_id.values() if r["kind"] == "DURATION_DIFF"]
    same(len(set(residual_operands)), len(residual_operands), "factory/no-double-payment")
    return {"by_id": by_id, "spans": spans, "paid": paid,
            "grants": {c: sum(by_id[i]["wall_seconds"] for i in paid[c]) for c in CASES}}


def candidate(mask, value, sequence, n):
    return {"mask_u32": mask, "mask_hex": mask_hex(mask, n), "cut": value, "sequence": sequence}


def endpoint(mask, graph):
    return {"mask_u32": mask, "mask_hex": mask_hex(mask, len(graph)), "cut": integer_cut(graph, mask)}


class ScoreAudit:
    def __init__(self, graph, rank, ledger, case):
        self.graph, self.rank, self.ledger, self.case = graph, rank, ledger, case
        self.sequence = 0
        self.best = self.chain_best = self.compiler_best = None
        self.best_phase = self.chain_phase = None
        self.used_owners = set()

    def credit(self, mask, value, phase):
        c = candidate(mask, value, self.sequence, len(self.graph))
        if self.best is None or value < self.best["cut"]:
            self.best, self.best_phase = c, phase
        if self.chain_best is None or value < self.chain_best["cut"]:
            self.chain_best, self.chain_phase = c, phase
        if phase == "compiler_M" and (self.compiler_best is None or value < self.compiler_best["cut"]):
            self.compiler_best = c
        self.sequence += 1

    def owner(self, row, phase, chain, step):
        label = {"reset": "reset_start_warmstart", "warmstart": "reset_start_warmstart",
                 "compiler_M": "compile_all_M_transport_split", "raw_proposal": "decode_raw_Q_accept_bests",
                 "quench": "decode_raw_Q_accept_bests"}[phase]
        span = self.ledger["spans"].get((self.case, label, chain, step))
        insist(span is not None and span["paid"] is True, "scores", "missing disjoint paid owner", category="SCHEMA")
        same(row["owner_span"], span["id"], "scores/owner")
        same(row["phase"], phase, "scores/phase")
        self.used_owners.add(span["id"])

    def scalar(self, row, mask, phase, chain, step):
        same(row["type"], "scalar_score", "scores/scalar-type")
        self.owner(row, phase, chain, step)
        same(row["sequence"], self.sequence, "scores/sequence")
        same(integer(row["mask_u32"], "scores/mask"), mask, "scores/scalar-mask")
        same(mask_read(row["mask_hex"], len(self.graph)), mask, "scores/scalar-hex")
        value = integer_cut(self.graph, mask)
        same(integer(row["cut"], "scores/cut", 0), value, "scores/scalar-full-cut")
        self.credit(mask, value, phase)
        return value

    def batch(self, row, mask, phase, chain, step):
        same(row["type"], "scored_batch", "scores/batch-type")
        self.owner(row, phase, chain, step)
        same(row["score_start"], self.sequence, "scores/batch-sequence")
        same(row["id"], row["owner_span"]+"/scores/"+str(self.sequence), "scores/batch-id")
        inside, outside, masks, cuts = swap_data(self.graph, mask, self.rank)
        same(integer(row["source_mask_u32"], "batch/mask"), mask, "batch/source")
        same(integer(row["base_cut"], "batch/base", 0), integer_cut(self.graph, mask), "batch/base")
        same(row["inside"], inside, "batch/inside-rank-order")
        same(row["outside"], outside, "batch/outside-rank-order")
        same(row["order"], "i-major/a-minor", "batch/order")
        same(row["count"], len(masks), "batch/all-neighbors")
        same(len(row["cuts"]), len(cuts), "batch/cuts-length")
        same(len(row["masks_u32"]), len(masks), "batch/masks-length")
        for i, (m, c) in enumerate(zip(masks, cuts)):
            same(integer(row["masks_u32"][i], "batch/mask"), m, "batch/exact-neighbor")
            same(integer(row["cuts"][i], "batch/cut", 0), c, "batch/full-crosssum")
            self.credit(m, c, phase)
        best = min(range(len(cuts)), key=lambda i: (cuts[i], i))
        same(row["best_index"], best, "batch/first-min")
        same(row["best_cut"], cuts[best], "batch/best-cut")
        same(row["best_mask_u32"], masks[best], "batch/best-mask")
        return masks[best], cuts[best]


class Cursor:
    """One record resident; only a marked failed producer may end early."""
    def __init__(self, rows, partial=False):
        self.rows, self.partial, self.cached = iter(rows), partial, None

    def peek(self):
        if self.cached is None:
            self.cached = next(self.rows, None)
        return self.cached

    def take(self, kind):
        row = self.peek()
        if row is None:
            if self.partial:
                raise PrefixEnd(kind)
            raise AuditIssue("SCHEMA", kind, "missing required record")
        same(row.get("type"), kind, "stream/event-order")
        self.cached = None
        return row


def descent_records(cursor, book, mask, phase, chain, step, scans):
    current, value, completed, local = mask, integer_cut(book.graph, mask), 0, False
    for _ in range(scans):
        m, c = book.batch(cursor.take("scored_batch"), current, phase, chain, step)
        completed += 1
        if c >= value:
            local = True
            break
        current, value = m, c
    return {"mask": current, "cut": value, "scans": completed, "local_optimum": local}


def check_readback(row):
    same(row["native_threads"], 1, "producer/native-readback")
    same(row["environment_threads"], {key: "1" for key in THREADS}, "producer/thread-environment")


def case_audit(case, graph, rows, ledger, replay, eigenvalues, require_complete=True, chains=3, steps=16):
    n, k = len(graph), len(graph)//2
    cursor = Cursor(rows, not require_complete)
    start = cursor.take("case_start")
    same(start["case"], case, "B/case")
    priority = replay.permutation(case, "B", "priority", list(range(n)))
    rank = rank_checked(start["priority_rank"], n)
    same(rank, [priority.index(v) for v in range(n)], "B/priority-replay")
    total = sum(graph[a][b] for a in range(n) for b in range(a+1, n))
    same(start["total_edge_weight"], total, "B/total-weight")
    book = ScoreAudit(graph, rank, ledger, case)
    requests = completed = accepted_count = raw_sum = q_sum = 0
    histogram, chain_results = [0]*(k+1), []
    pending = None
    expected_spans = {(case, "case_private_setup", None, None), (case, "case_algorithm_finalization", None, None)}
    factory_ids = set()
    try:
        for chain in range(chains):
            expected_spans.update({(case, "reset_start_warmstart", chain, None), (case, "own_chain_finalization", chain, None)})
            book.chain_best = book.chain_phase = None
            reset_order = replay.permutation(case, "B", "reset_start", list(range(n)), chain)
            reset_mask = orient(membership(reset_order[:k], n), rank)
            book.scalar(cursor.take("scalar_score"), reset_mask, "reset", chain, None)
            warm = descent_records(cursor, book, reset_mask, "warmstart", chain, None, 2)
            reset = cursor.take("reset")
            same(reset["chain"], chain, "reset/chain")
            same(reset["reset_mask_u32"], reset_mask, "reset/fresh-start")
            same(reset["reset_cut"], integer_cut(graph, reset_mask), "reset/cut")
            same(reset["warmstart"], warm, "reset/warmstart")
            same(reset["own_scored_best"], book.chain_best, "reset/own-scored-best")
            current = endpoint_best = warm["mask"]
            for step in range(steps):
                expected_spans.update({(case, "compile_all_M_transport_split", chain, step),
                                       (case, "decode_raw_Q_accept_bests", chain, step)})
                pending = {"chain": chain, "step": step, "phase": "compiler"}
                book.batch(cursor.take("scored_batch"), current, "compiler_M", chain, step)
                request = cursor.take("attempt_request")
                for key, value in (("case", case), ("chain", chain), ("step", step), ("full_source_photons", k)):
                    same(request[key], value, "request/"+key)
                same(request["current_before"], endpoint(current, graph), "request/current-not-compiler-best")
                inside = sorted(vertices(current, n), key=rank.__getitem__)
                outside = sorted(vertices(current ^ ((1 << n)-1), n), key=rank.__getitem__)
                source = replay.permutation(case, "B", "portS", inside, chain, step)
                target = replay.permutation(case, "B", "portT", outside, chain, step)
                same(request["source_ports"], source, "request/source-port-replay")
                same(request["target_ports"], target, "request/target-port-replay")
                compiler_check(graph, current, rank, request["compiler"], request["routed"], source, target, eigenvalues)
                coins = replay.split_coins(case, chain, step, k)
                same(request["split_coins"], coins, "request/all-split-coins")
                insist(len(coins) == k and all(type(x) is int and x in (0, 1) for x in coins), "split", "individual unbiased binary coins")
                removed = [i for i, coin in enumerate(coins) if coin == 0]
                same(request["removed_ports"], removed, "request/removed-ports")
                for name, native in (("native", True), ("repair", False)):
                    r = replay.role(case, "B", name, chain, step)
                    same(request[name+"_role"], r, "request/"+name+"-role")
                    same(request[name+"_seed"], replay.seed(r, native), "request/"+name+"-seed")
                requests += 1
                pending["phase"] = "observation"
                if removed:
                    expected_spans.update({(case, "factory_total", chain, step), (case, "serial_native_sample", chain, step)})
                    factory = cursor.take("factory_report")
                    same((factory["chain"], factory["step"]), (chain, step), "factory/position")
                    outer = ledger["spans"].get((case, "factory_total", chain, step))
                    sample = ledger["spans"].get((case, "serial_native_sample", chain, step))
                    insist(outer is not None and sample is not None, "factory", "missing observed outer/sample spans")
                    report = ledger["by_id"].get(factory["reported_ref"])
                    diff = ledger["by_id"].get(factory["duration_difference_ref"])
                    insist(report is not None and diff is not None, "factory", "missing typed report/residual")
                    same(factory["outer_ref"], outer["id"], "factory/outer-link")
                    same(diff["outer_ref"], outer["id"], "factory/diff-outer")
                    same(diff["reported_ref"], report["id"], "factory/diff-report")
                    same(factory["backend_setup_wall"], report["wall_seconds"], "factory/reported-value")
                    factory_ids.update((report["id"], diff["id"]))
                else:
                    omitted = cursor.take("native_not_called")
                    same((omitted["chain"], omitted["step"], omitted["reason"]), (chain, step, "r=0"), "vacuum/native-omitted")
                    insist((case, "factory_total", chain, step) not in ledger["spans"]
                           and (case, "serial_native_sample", chain, step) not in ledger["spans"], "vacuum", "fabricated native work")
                observation = cursor.take("native_observation")
                same((observation["chain"], observation["step"]), (chain, step), "observation/position")
                same(observation["fallback"], False, "observation/no-fallback")
                # Read score events only after the full observation has survived its guards.
                pending["phase"] = "decode"
                next_row = cursor.peek()
                if next_row is None and cursor.partial:
                    raise PrefixEnd("decode")
                y = observation["receiver_counts"]
                # The stored decoder is emitted after its raw/Q score records.
                raw_record = cursor.take("scalar_score")
                raw_mask = mask_checked(raw_record["mask_u32"], n)
                raw_cut = book.scalar(raw_record, raw_mask, "raw_proposal", chain, step)
                quenched = descent_records(cursor, book, raw_mask, "quench", chain, step, 1)
                outcome = cursor.take("attempt_outcome")
                same((outcome["chain"], outcome["step"]), (chain, step), "outcome/position")
                decoded = decoded_check(source, target, removed, y, outcome["decoded"],
                    lambda available, count: replay.permutation(case, "B", "repair", available, chain, step)[:count])
                same(raw_mask, orient(decoded, rank), "outcome/proposal-source-labels")
                same(outcome["raw_cut"], raw_cut, "outcome/raw-cut")
                same(outcome["quench"], quenched, "outcome/Q-best-including-input")
                accepted = quenched["cut"] < integer_cut(graph, current)
                same(outcome["accepted"], accepted, "outcome/strict-accept")
                if accepted:
                    current = quenched["mask"]
                if quenched["cut"] < integer_cut(graph, endpoint_best):
                    endpoint_best = quenched["mask"]
                same(outcome["current_after"], endpoint(current, graph), "outcome/current")
                same(outcome["endpoint_best"], endpoint(endpoint_best, graph), "outcome/endpoint-not-allscored")
                same(outcome["own_scored_best"], book.chain_best, "outcome/own-scored-best")
                same(outcome["all_paid_best"], book.best, "outcome/all-batches-credit")
                raw_sum += raw_cut
                q_sum += quenched["cut"]
                accepted_count += int(accepted)
                histogram[len(removed)] += 1
                completed += 1
                pending = None
            chain_results.append({"chain": chain, "warmstart_cut": warm["cut"], "own_scored_best": book.chain_best,
                "own_scored_best_phase": book.chain_phase, "endpoint_best": endpoint(endpoint_best, graph),
                "current": endpoint(current, graph)})
            insist((case, "own_chain_finalization", chain, None) in ledger["spans"], "B", "missing paid chain finalization")
        result = cursor.take("case_result")
        expected = {"case": case, "requested": requests, "completed": completed,
            "full_source_photons": k*completed, "conditional_receiver_photons": sum(i*c for i, c in enumerate(histogram)),
            "r_histogram": histogram, "chains": chain_results, "accepted_steps": accepted_count,
            "all_paid_best": book.best, "all_paid_best_phase": book.best_phase, "compiler_only_best": book.compiler_best,
            "scored_candidates": book.sequence, "grant_wall_seconds": ledger["grants"][case],
            "paid_component_ids": ledger["paid"][case]}
        for key, value in expected.items():
            same(result[key], value, "case-result/"+key)
        for key, value in (("raw_mean_cut", Fraction(raw_sum, completed)), ("q_mean_cut", Fraction(q_sum, completed)),
                           ("raw_mean_normalized", Fraction(raw_sum, completed*total) if total else Fraction(0)),
                           ("q_mean_normalized", Fraction(q_sum, completed*total) if total else Fraction(0))):
            same(result[key], {"numerator": value.numerator, "denominator": value.denominator}, "case-result/"+key)
        same(result["case_start_clocks"], start["case_start_clocks"], "case-result/start-clocks")
        for a, b in zip(result["case_start_clocks"], result["case_end_clocks"]):
            insist(number(b, "case/end") >= number(a, "case/start"), "case", "reversed whole-case clocks")
        same(completed, chains*steps, "case-result/complete-population")
        same({key for key in ledger["spans"] if key[0] == case and key[1] != "synthetic_problem_input_generation"},
             expected_spans, "case-result/exact-clock-population")
        same({r["id"] for r in ledger["by_id"].values() if r["case"] == case and r["kind"] != "OBSERVED_SPAN"},
             factory_ids, "case-result/all-factory-operands-consumed")
        insist((case, "case_private_setup", None, None) in ledger["spans"] and
               (case, "case_algorithm_finalization", None, None) in ledger["spans"], "B", "missing paid setup/finalization")
        for i, domain in enumerate(("cpu", "wall")):
            insist(start["case_start_clocks"][i] <= ledger["spans"][(case, "case_private_setup", None, None)]["start_"+domain]
                   and result["case_end_clocks"][i] >= ledger["spans"][(case, "case_algorithm_finalization", None, None)]["end_"+domain],
                   "case", "paid spans outside whole-case clocks")
        insist(ledger["grants"][case] <= result["case_end_clocks"][1]-start["case_start_clocks"][1],
               "case", "grant exceeds full case WALL")
        readback = cursor.take("native_readback")
        same(readback["case"], case, "case/readback")
        check_readback(readback["readback"])
        same(cursor.peek(), None, "case/unregistered-trailing-record")
        return {"complete": True, "requested": requests, "completed": completed, "r_histogram": histogram,
                "all_paid_best": book.best, "scored_candidates": book.sequence, "grant": ledger["grants"][case],
                "primary_case_result": {key: value for key, value in result.items() if key != "type"}}
    except PrefixEnd:
        return {"complete": False, "requested": requests, "completed": completed, "r_histogram": histogram,
                "all_paid_best": book.best, "scored_candidates": book.sequence, "pending": pending}


def duration_gap(outer, adapter, reported):
    values = [number(v, "control/call-gap") for v in (*outer, *adapter, *reported)]
    cpu, wall = values[0]-values[2]-values[4], values[1]-values[3]-values[5]
    insist(cpu >= 0 and wall >= 0, "control/call-gap", "negative un-clipped residual")
    return cpu, wall


def trace_check(trace, graph, adapter, gap, grant, result):
    columns = ("cpu_seconds", "wall_seconds", "best_cut", "mask_hex", "proposal_count", "stage_code")
    insist(all(type(trace.get(key)) is list for key in columns), "trace", "six complete column arrays", category="SCHEMA")
    count = len(trace["cpu_seconds"])
    insist(count <= MAX_TRACE and all(len(trace[key]) == count for key in columns), "trace", "column length/export cap", category="MALFORMED")
    final_work = integer(result["proposal_count"], "trace/returned-work", 0)
    insist(final_work <= MAX_WORK and count <= final_work//32+4, "trace", "static work/checkpoint bound")
    ac, aw, g = number(adapter[0], "adapter/CPU"), number(adapter[1], "adapter/WALL"), number(grant, "grant")
    cc, cw = ac+gap[0], aw+gap[1]
    previous, previous_cut = (-1.0, -1.0, -1), None
    direct = selected = first = None
    first_cpu = first_wall = None
    for i in range(count):
        if i % 1000 == 0:
            resource_guard()
        cpu, wall = number(trace["cpu_seconds"][i], "trace/CPU"), number(trace["wall_seconds"][i], "trace/WALL")
        value, work = integer(trace["best_cut"][i], "trace/cut", 0), integer(trace["proposal_count"][i], "trace/work", 0)
        stage = integer(trace["stage_code"][i], "trace/stage-code", 0)
        insist(stage < len(STAGES) and cpu >= previous[0] and wall >= previous[1] and previous[2] <= work <= final_work,
               "trace", "chronology/work/stage", category="MALFORMED")
        insist(previous_cut is None or value <= previous_cut, "trace", "best cut increases")
        mask = mask_read(trace["mask_hex"][i], len(graph))
        same(value, integer_cut(graph, mask), "trace/every-retained-mask-cut")
        previous, previous_cut = (cpu, wall, work), value
        if first is None and STAGES[stage] == "initial_scan":
            first, first_cpu, first_wall = i, cc+cpu, cw+wall
        for corrected in (False, True):
            off_cpu, off_wall = (cc, cw) if corrected else (ac, aw)
            if off_cpu+cpu <= g and off_wall+wall <= g:
                witness = {"index": i, "cut": value, "mask_hex": trace["mask_hex"][i],
                    "cpu_seconds": cpu, "wall_seconds": wall, "total_cpu": off_cpu+cpu,
                    "total_wall": off_wall+wall, "provenance": "archived_preclock_RAM_prefix"}
                if corrected:
                    selected = witness
                else:
                    direct = witness
    if count:
        insist(previous[0] <= number(result["compute_cpu_seconds"], "helper/CPU")
               and previous[1] <= number(result["compute_wall_seconds"], "helper/WALL"), "trace", "checkpoint after reported computation")
    first_timely = first is not None and first_cpu <= g and first_wall <= g
    return selected, direct, first, first_cpu, first_wall, first_timely, count


def control_audit(cursor, graph, case, mode, grant, replay):
    raw = cursor.take("control_return_observation")
    trace = cursor.take("control_trace")
    header = cursor.take("control_header")
    outcome = cursor.take("control_result")
    for record in (raw, trace, header, outcome):
        same((record["case"], record["mode"]), (case, mode), "control/fixed-order")
    for record in (raw, header, outcome):
        same(number(record["grant"], "control/grant"), grant, "control/whole-own-grant")
    outer, adapter, reported = header["observed_outer"], header["observed_direct_adapter"], header["reported_compute_duration"]
    for key in ("observed_outer", "observed_direct_adapter", "reported_compute_duration"):
        same(header[key], raw[key], "control/returned-operands-before-validation")
    observed_span(outer)
    observed_span(adapter)
    prefix = case+"/"+mode
    same(outer["id"], prefix+"/outer", "control/outer-ID")
    same(adapter["id"], prefix+"/adapter", "control/adapter-ID")
    for domain in ("cpu", "wall"):
        same(adapter["start_"+domain], outer["start_"+domain], "control/shared-outer-start")
        insist(adapter["end_"+domain] <= outer["end_"+domain], "control", "adapter exceeds outer")
    same(reported["kind"], "REPORTED_DURATION", "control/reported-kind")
    same(reported["label"], "P50_compute_reported", "control/reported-label")
    same(reported["id"], prefix+"/reported_compute", "control/reported-ID")
    same((reported["case"], reported["mode"], reported["paid"]), (case, mode, False), "control/report-scope")
    same(reported["helper_source_path"], "research/P50_fast_from_scratch.py", "control/helper-path")
    same(reported["helper_source_sha256"], P50_SHA, "control/helper-pin")
    for key in ("start_cpu", "end_cpu", "start_wall", "end_wall"):
        same(reported[key], None, "control/reported-unknown-endpoint")
    ac, aw = adapter["cpu_seconds"], adapter["wall_seconds"]
    same(header["adapter_cpu"], ac, "control/direct-CPU")
    same(header["adapter_wall"], aw, "control/direct-WALL")
    same(header["solver_cpu_budget"], max(0.0, grant-ac), "control/helper-CPU-allowance")
    seed_role = replay.role(case, mode, "control")
    same(header["seed_role"], seed_role, "control/independent-role")
    same(header["seed"], replay.seed(seed_role), "control/independent-seed")
    result = outcome["result"]
    same(result, raw["returned_scalar_metadata"], "control/raw-return-lineage")
    for domain in ("cpu", "wall"):
        same(reported[domain+"_seconds"], result["compute_"+domain+"_seconds"], "control/reported-duration-lineage")
    gap = duration_gap((outer["cpu_seconds"], outer["wall_seconds"]), (ac, aw),
                       (reported["cpu_seconds"], reported["wall_seconds"]))
    difference = {"kind": "CONSERVATIVE_DURATION_DIFF", "cpu_seconds": gap[0], "wall_seconds": gap[1],
        "start_cpu": None, "end_cpu": None, "start_wall": None, "end_wall": None,
        "formula": "observed_outer - direct_adapter - helper_reported_compute",
        "scope": "conservative entry plus return charge, not an observed prefix interval",
        "outer_ref": outer["id"], "direct_adapter_ref": adapter["id"], "reported_ref": reported["id"]}
    same(header["call_boundary_difference"], difference, "control/typed-dual-call-gap")
    selected, direct, first, fc, fw, timely, count = trace_check(trace, graph, (ac, aw), gap, grant, result)
    early = result["early_cap_inconclusive"]
    insist(type(early) is bool, "control", "early-guard flag type", category="MALFORMED")
    same(integer(result["max_proposals"], "control/work-guard"), MAX_WORK, "control/work-guard")
    same(result["free_incumbent_used"], False, "control/no-B-incumbent")
    adequate = selected is not None and timely and not early
    expected = {"case": case, "mode": mode, "grant": grant, "normal_return": True,
        "adapter_cpu": ac, "adapter_wall": aw, "selected": selected, "direct_selected": direct,
        "call_boundary_difference": difference, "first_scan_index": first,
        "first_scan_dual_timely": timely, "first_scan_cpu": fc, "first_scan_wall": fw,
        "early_guard": early, "adequate": adequate, "result": result}
    same({key: value for key, value in outcome.items() if key != "type"}, expected, "control/outcome")
    return {"case": case, "mode": mode, "checkpoints": count, "selected": selected,
            "adequate": adequate, "early_guard": early, "normal_return": True, "primary_control_result": expected}


def classify(cases, controls):
    if any(not cases.get(cid, {}).get("complete", False) for cid in CASES):
        return "INCONCLUSIVE_BASELINE_ELIGIBILITY"
    expected = [(mode, case) for mode in FAST for case in CASES]
    if [(row["mode"], row["case"]) for row in controls] != expected or any(
            row.get("normal_return") is not True or row.get("adequate") is not True or row.get("selected") is None for row in controls):
        return "INCONCLUSIVE_BASELINE_ELIGIBILITY"
    return "FOLLOWUP_REQUIRED" if all(cases[row["case"]]["all_paid_best"]["cut"] < row["selected"]["cut"]
                                       for row in controls) else "NO_POSITIVE_SIGNAL"


_RUN_START = None


def resource_guard():
    if _RUN_START is not None:
        insist(time.process_time()-_RUN_START[0] <= 30 and time.perf_counter()-_RUN_START[1] <= 60,
               "auditor", "registered CPU/WALL budget exhausted", category="RESOURCE")


def pairs_checked(pairs):
    result = {}
    for key, value in pairs:
        insist(key not in result, "JSON", "duplicate object key", key, "MALFORMED")
        result[key] = value
    return result


def parse_json(raw):
    insist(len(raw) <= LINE_BYTES, "JSON", "single object/line byte cap", category="RESOURCE")
    try:
        return json.loads(raw, object_pairs_hook=pairs_checked,
            parse_constant=lambda token: (_ for _ in ()).throw(AuditIssue("MALFORMED", "JSON", "nonfinite token", token)))
    except (ValueError, UnicodeError) as error:
        raise AuditIssue("MALFORMED", "JSON", "invalid JSON", repr(error)) from error


def read_json(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(LINE_BYTES+1)
    return parse_json(raw)


def json_rows(path, limit):
    with Path(path).open("rb") as stream:
        index = 0
        while True:
            raw = stream.readline(LINE_BYTES+1)
            if not raw:
                return
            index += 1
            insist(index <= limit, "JSONL", "record count guard", category="RESOURCE")
            insist(raw.endswith(b"\n"), "JSONL", "unterminated/truncated line", category="MALFORMED")
            resource_guard()
            record = parse_json(raw)
            insist(type(record) is dict, "JSONL", "object record required", category="MALFORMED")
            yield record


def project_file(root, relative):
    insist(type(relative) is str, "path", "relative string required", category="MALFORMED")
    path = Path(relative)
    insist(not path.is_absolute() and path.parts and all(p not in (".", "..") for p in path.parts),
           "path", "unsafe project-relative path", relative, "MALFORMED")
    current = root
    for part in path.parts:
        current /= part
        insist(not current.is_symlink(), "path", "symlink forbidden", relative, "MALFORMED")
    insist(current.is_file() and current.resolve().is_relative_to(root.resolve()), "path", "missing/outside regular file", relative, "SCHEMA")
    return current


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            digest.update(block)
    return digest.hexdigest()


class MainReplay:
    def __init__(self, token):
        insist(token is _POST_SEAL, "replay", "postseal closure token required", category="AUTHORIZATION")
        for key in THREADS:
            same(os.environ.get(key), "1", "auditor/thread-environment")
        import numpy as np
        import networkx as nx
        same(np.__version__, "2.4.6", "auditor/NumPy")
        same(nx.__version__, "3.6.1", "auditor/NetworkX")
        self.np, self.nx = np, nx

    def role(self, case, arm, name, chain=-1, step=-1):
        return ["P90a", 90026001, case, arm, chain, step, name, 0]

    def seed(self, value, native=False):
        data = json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("ascii")
        digest = hashlib.sha256(data).digest()
        return 1+int.from_bytes(digest[:4], "little") % (2**32-1) if native else int.from_bytes(digest[:8], "little")

    def rng(self, value):
        return self.np.random.Generator(self.np.random.PCG64(self.seed(value)))

    def permutation(self, case, arm, name, values, chain=-1, step=-1):
        return [int(x) for x in self.rng(self.role(case, arm, name, chain, step)).permutation(values)]

    def split_coins(self, case, chain, step, k):
        return [int(x) for x in self.rng(self.role(case, "B", "split", chain, step)).integers(0, 2, size=k)]

    def eigenvalues(self, h):
        values, _ = self.np.linalg.eigh(self.np.asarray(h, dtype=self.np.complex128))
        return [float(x) for x in values]

    def role_records(self):
        records, seen = [], {False: set(), True: set()}
        for case in CASES:
            pairs = [(self.role(case, "GEN", "weights"), False), (self.role(case, "B", "priority"), False)]
            for chain in range(3):
                pairs.append((self.role(case, "B", "reset_start", chain), False))
                for step in range(16):
                    pairs.extend((self.role(case, "B", name, chain, step), False) for name in ("portS", "portT", "split", "repair"))
                    pairs.append((self.role(case, "B", "native", chain, step), True))
            pairs.extend((self.role(case, mode, "control"), False) for mode in FAST)
            for role, native in pairs:
                seed = self.seed(role, native)
                insist(seed not in seen[native], "roles", "seed collision; no rehash")
                seen[native].add(seed)
                records.append({"role": role, "native": native, "seed": seed})
        return records

    def graph(self, case):
        topology = self.nx.gnp_random_graph(24, 0.4, seed=9002401) if case == CASES[0] else self.nx.random_regular_graph(4, 24, seed=9002402)
        edges = sorted((min(int(a), int(b)), max(int(a), int(b))) for a, b in topology.edges())
        weights = self.rng(self.role(case, "GEN", "weights")).integers(1, 6, size=len(edges))
        graph = [[0]*24 for _ in range(24)]
        for (a, b), weight in zip(edges, weights):
            graph[a][b] = graph[b][a] = int(weight)
        return graph


def producer_limits_checked(run):
    exact_numeric(run["timeout_seconds"], 90, "producer/wall-cap")
    same(run["max_output_bytes"], 4194304, "producer/log-cap")
    same(run["resource_limits"]["cpu_seconds"], 60, "producer/CPU-cap")
    same(run["resource_limits"]["max_threads"], 1, "producer/thread-cap")


def manifest_checked(manifest, contract, artifacts, run_kind):
    same(manifest["schema_version"], 2, run_kind+"/manifest-schema")
    same(manifest["command"], contract["planned_command"], run_kind+"/exact-argv")
    same(manifest["execution_artifacts"], contract["execution_artifacts"], run_kind+"/input-argv")
    records = manifest["input_artifacts"]
    same([r["path"] for r in records], contract["execution_artifacts"], run_kind+"/observed-inputs")
    for row in records:
        insist(row["path"] in artifacts, run_kind, "input missing from sealed closure", row["path"], "SCHEMA")
        same(row["sha256"], artifacts[row["path"]]["sha256"], run_kind+"/input-hash")
        same(row["sha256_after"], row["sha256"], run_kind+"/unchanged-input")
    same(manifest["declared_results"], contract["declared_results"], run_kind+"/result-population")
    parent = contract.get("runner_output_directory", contract.get("runner_binding", {}).get("output_parent"))
    same(manifest["output_directory"], parent, run_kind+"/output-parent")
    for relative in manifest["declared_results"]:
        insist(Path(relative).is_relative_to(Path(parent)) and Path(relative) != Path(parent),
               run_kind, "result must be strict child of runner parent", relative, "SCHEMA")
    for row in manifest["outputs"]:
        insist(row["kind"] in ("result", "log"), run_kind, "unknown manifest output kind", category="SCHEMA")
        insist(row["path"] in artifacts, run_kind, "output/log missing from opaque closure", row["path"], "SCHEMA")
        same(row["sha256"], artifacts[row["path"]]["sha256"], run_kind+"/output-hash")
    same(sorted(row["path"] for row in manifest["outputs"]),
         sorted(manifest["declared_results"]+[parent+"/stdout.txt", parent+"/stderr.txt"]), run_kind+"/all-output-hashes")
    run = manifest["run"]
    if run["exit_status"] is not None:
        integer(run["exit_status"], run_kind+"/exit-code")
    number(run["runtime_seconds"], run_kind+"/runtime")
    same(run["invalid_results"], [], run_kind+"/invalid-results")
    checks = {row["check"]: row["passed"] for row in manifest["checks"]}
    same(checks.get("input hashes unchanged"), True, run_kind+"/input-check")
    same(checks.get("declared result files are present and regular"), True, run_kind+"/result-check")
    same(checks.get("process exited successfully within enforced limits"),
         run["status"] == "completed" and run["exit_status"] == 0, run_kind+"/exit-check")
    return run


def qualified_checked(root, relative, contract, artifacts, count, cpu, wall):
    manifest = read_json(project_file(root, relative))
    run = manifest_checked(manifest, contract, artifacts, "qualification")
    same(run["status"], "completed", "qualification/completed")
    same(run["exit_status"], 0, "qualification/exit")
    same(run["missing_results"], [], "qualification/missing")
    exact_numeric(run["timeout_seconds"], wall, "qualification/WALL")
    same(run["resource_limits"]["cpu_seconds"], cpu, "qualification/CPU")
    same(run["resource_limits"]["max_threads"], 1, "qualification/threads")
    same(run["max_output_bytes"], 4194304, "qualification/logs")
    same(len(manifest["declared_results"]), 1, "qualification/one-JUnit")
    xml_path = project_file(root, manifest["declared_results"][0])
    insist(xml_path.stat().st_size <= RAW_BYTES, "qualification", "JUnit bound", category="RESOURCE")
    try:
        xml = ET.parse(xml_path).getroot()
    except ET.ParseError as error:
        raise AuditIssue("MALFORMED", "qualification/JUnit", "invalid XML", repr(error)) from error
    cases = xml.findall(".//testcase")
    same(len(cases), count, "qualification/exact-population")
    ids = [(x.get("classname"), x.get("name")) for x in cases]
    same(len(set(ids)), count, "qualification/no-duplicate-node")
    insist(not xml.findall(".//failure") and not xml.findall(".//error") and not xml.findall(".//skipped"),
           "qualification", "failed/error/skipped item")
    return manifest


def verify_closure(root, binding):
    same(binding["binding_state"], "SEALED_POST_B_RAW_AUTHORIZED", "binding/state")
    same(binding["b_raw_sealed"], True, "binding/B-seal")
    same(binding["audit_authorized"], True, "binding/authorization")
    same(binding["producer_source_freeze"], FREEZE, "binding/producer-freeze")
    same(binding["producer_execution_commit"], EXPECTED_PRODUCER_COMMIT, "binding/predata-main-execution-commit")
    same(binding["checker_source_sha256"], file_hash(Path(__file__)), "binding/checker-source")
    artifacts = {}
    for row in binding["artifacts"]:
        path = row["path"]
        insist(path not in artifacts, "binding", "duplicate artifact", path, "MALFORMED")
        actual = project_file(root, path)
        same(integer(row["bytes"], "binding/bytes", 0), actual.stat().st_size, "binding/byte-count")
        same(row["sha256"], file_hash(actual), "binding/current-file-hash")
        artifacts[path] = row
    for path, digest in PRIMARY_PINS.items():
        insist(path in artifacts, "binding", "required frozen artifact absent", path, "SCHEMA")
        same(artifacts[path]["sha256"], digest, "binding/exact-primary-freeze")
    primary_contract = read_json(project_file(root, "research/P90a_execution_contract.json"))
    primary_spec = read_json(project_file(root, "research/P90a_execution_spec.json"))
    same(primary_contract["execution_artifacts"], list(PRIMARY_INPUTS), "binding/18-primary-inputs")
    same(primary_spec["execution_artifacts"], list(PRIMARY_INPUTS), "binding/spec-inputs")
    producer = read_json(project_file(root, binding["producer_manifest"]))
    insist(binding["producer_manifest"] in artifacts, "binding", "producer manifest not hashed", category="SCHEMA")
    same(producer["repository"]["commit"], binding["producer_execution_commit"], "binding/execution-commit")
    run = manifest_checked(producer, primary_contract, artifacts, "producer")
    producer_limits_checked(run)
    expected_results = ["experiments/P90a_dev_veto/run_001/data/"+name for name in FILES]
    same(producer["declared_results"], expected_results, "binding/eight-primary-results")
    same(binding["dataset_directory"], "experiments/P90a_dev_veto/run_001/data", "binding/dataset-directory")
    for path in expected_results:
        insist(path in artifacts, "binding", "missing raw artifact", path, "SCHEMA")
    insist(sum(artifacts[path]["bytes"] for path in expected_results) <= RAW_BYTES, "raw", "32MiB total", category="RESOURCE")
    same(run["missing_results"], [], "producer/missing-results")
    for key in ("producer_qualification_manifest", "checker_qualification_manifest"):
        insist(binding[key] in artifacts, "binding", "qualification manifest not hashed", category="SCHEMA")
    producer_qual = qualified_checked(root, binding["producer_qualification_manifest"],
        read_json(project_file(root, "research/P90a_preflight_contract.json")), artifacts, 283, 60, 90)
    same(producer_qual["repository"]["commit"], FREEZE, "qualification/producer-source-freeze-commit")
    own_spec = read_json(project_file(root, "research/P90a_independent_audit_spec.json"))
    own_qual = read_json(project_file(root, "research/P90a_independent_audit_preflight_contract.json"))
    same(own_spec["qualification_items"], QUALIFICATION_ITEMS, "checker/frozen-qualification-population")
    for path in own_qual["execution_artifacts"]:
        insist(path in artifacts, "binding", "checker qualification input not hashed", path, "SCHEMA")
    qualified_checked(root, binding["checker_qualification_manifest"], own_qual, artifacts,
                      QUALIFICATION_ITEMS, 30, 60)
    return producer, primary_spec, artifacts, _POST_SEAL


def failure_state_checked(run, summary, failure):
    status = summary["status"]
    same(summary["positive_accepted"], False, "primary/no-positive")
    insist(status in ("NO_POSITIVE_SIGNAL", "FOLLOWUP_REQUIRED", "INCONCLUSIVE_BASELINE_ELIGIBILITY",
                      "INCONCLUSIVE_FIRST_FAILURE", "INCONCLUSIVE_RESOURCE_FAILURE"), "primary", "unknown status")
    normal = run["status"] == "completed" and run["exit_status"] == 0
    failed = status in ("INCONCLUSIVE_FIRST_FAILURE", "INCONCLUSIVE_RESOURCE_FAILURE")
    insist(normal or failed, "producer", "runner failure not explained by first-failure status")
    if failed:
        same(failure["status"], "FIRST_FAILURE", "primary/first-failure-provenance")
    else:
        same(failure, {"status": "NO_FAILURE"}, "primary/no-failure")
        insist(normal, "producer", "complete scientific claim requires completed runner")
    return failed


def audit_dataset(root, binding):
    producer, spec, artifacts, token = verify_closure(root, binding)
    dataset = root/binding["dataset_directory"]
    summary, failure = read_json(dataset/"summary.json"), read_json(dataset/"failure.json")
    status = summary["status"]
    failed = failure_state_checked(producer["run"], summary, failure)
    metadata, graphs_record = read_json(dataset/"metadata.json"), read_json(dataset/"graphs.json")
    if metadata.get("status") == "NOT_RUN" or graphs_record.get("status") == "NOT_RUN":
        insist(failed, "prefix", "missing startup requires explicit first failure")
        return {"status": "FINITE_PREFIX_AUDIT_INCONCLUSIVE", "primary_status": status,
                "reason": "startup did not complete; no scientific replay", "positive_accepted": False}
    same(metadata["spec"], spec, "metadata/frozen-spec")
    same(metadata["stage_dictionary"], list(STAGES), "metadata/stages")
    check_readback(metadata["provenance"])
    provenance = metadata["provenance"]["provenance"]
    for record in provenance["project_input_hashes"]:
        insist(record["path"] in artifacts, "metadata", "unbound project input")
        same(record["sha256"], artifacts[record["path"]]["sha256"], "metadata/source-input-pin")
    same([r["path"] for r in provenance["project_input_hashes"]], list(PRIMARY_INPUTS), "metadata/full-input-closure")
    same(provenance["software"], spec["software"], "metadata/software")
    for record, expected in zip(provenance["external_inputs"], spec["external_artifacts"]):
        same({key: record[key] for key in expected}, expected, "metadata/external-pin")
        same(record["actual_sha256"], expected["sha256"], "metadata/external-actual-hash")
    same(len(provenance["external_inputs"]), 18, "metadata/external-population")
    actual_loaded = provenance["actually_loaded_critical_modules"]
    same(set(actual_loaded), {"serial_sampling_backend", "deterministic_qualification_backend",
         "backend_circuit_input_convention", "native_seed_bridge", "seed_bridge_export", "native_extension",
         "eigvalsh_python", "eigvalsh_native", "PCG64_native", "array_native", "expm_python", "expm_native"},
         "metadata/full-loaded-module-population")
    for pin in spec["external_artifacts"]:
        if pin["role"] in actual_loaded:
            same(actual_loaded[pin["role"]]["sha256"], pin["sha256"], "metadata/loaded-module-pin")
    same(provenance["actual_interpreter"]["sha256"], next(r["sha256"] for r in spec["external_artifacts"]
         if r["role"] == "physical_interpreter"), "metadata/interpreter-pin")
    replay = MainReplay(token)
    same(provenance["role_seeds"], replay.role_records(), "metadata/all-role-seed-integrity")
    same(graphs_record["recipes"], spec["cases"], "graphs/recipes")
    graphs = graphs_record["cases"]
    same(set(graphs), set(CASES), "graphs/two-cases")
    for case in CASES:
        same(graph_checked(graphs[case]), replay.graph(case), "graphs/independent-replay")
    ledger = ledger_checked(json_rows(dataset/"paid_ledger.jsonl", MAX_LEDGER_ROWS))
    for case in CASES:
        insist((case, "synthetic_problem_input_generation", None, None) in ledger["spans"], "ledger", "missing separately excluded GEN span")
    cases = {}
    for case, name in zip(CASES, ("B_ER.jsonl", "B_RR.jsonl")):
        records = json_rows(dataset/name, MAX_B_ROWS)
        probe = Cursor(records, partial=failed)
        if probe.peek() is None:
            insist(failed, case, "empty required B stream", category="SCHEMA")
            cases[case] = {"complete": False, "requested": 0, "completed": 0}
        else:
            def retained():
                yield probe.cached
                probe.cached = None
                yield from probe.rows
            cases[case] = case_audit(case, graphs[case], retained(), ledger, replay, replay.eigenvalues, not failed)
    controls, cursor = [], Cursor(json_rows(dataset/"controls.jsonl", MAX_CONTROL_ROWS), partial=failed)
    try:
        for mode in FAST:
            for case in CASES:
                if not cases[case]["complete"]:
                    insist(failed, case, "control before complete B population")
                    raise PrefixEnd("B")
                controls.append(control_audit(cursor, graphs[case], case, mode, ledger["grants"][case], replay))
        same(cursor.peek(), None, "controls/no-extra-call")
    except PrefixEnd:
        insist(failed, "controls", "unexpected incomplete panel")
    requested, completed = sum(c["requested"] for c in cases.values()), sum(c["completed"] for c in cases.values())
    same(summary["requested_B_attempts"], requested, "summary/requested-population")
    same(summary["completed_B_attempts"], completed, "summary/completed-population")
    same(summary["modeled_full_source_photons"], 12*requested, "summary/injected-photons")
    same(summary["modeled_completed_source_photons"], 12*completed, "summary/completed-photons")
    if not failed:
        same(completed, 96, "summary/complete96")
        same(status, classify(cases, controls), "summary/fixed-panel-decision")
        same(summary["B_cases"], {cid: cases[cid]["primary_case_result"] for cid in CASES}, "summary/case-lineage")
        same(summary["controls"], [c["primary_control_result"] for c in controls], "summary/control-lineage")
        expected_population = [{"case": c["case"], "mode": c["mode"], "status": "COMPLETE",
            "outcome": {"selected": c["selected"], "adequate": c["adequate"]}} for c in controls]
        same(summary["control_population"], expected_population, "summary/four-control-population")
        check_readback(summary["native_final_readback"])
    else:
        insist(type(failure.get("exception_repr")) is str and type(failure.get("exception_type")) is str,
               "failure", "first exception identity required", category="SCHEMA")
        population = summary.get("control_population", [])
        same(len(population), 4, "prefix/declared-control-slots")
        for i, row in enumerate(population):
            same((row["mode"], row["case"]), [(m, c) for m in FAST for c in CASES][i], "prefix/fixed-control-order")
            insist(row["status"] in ("NOT_RUN", "REQUESTED", "COMPLETE"), "prefix", "invalid control population state")
    same(summary["mandatory_followups"], {name: {"status": "NOT_RUN", "outcome": None,
         "reason": "separate contract/ROOT authorization required"} for name in FOLLOWUPS}, "summary/unrun-followups")
    for row in cases.values():
        row.pop("primary_case_result", None)
    for row in controls:
        row.pop("primary_control_result", None)
    return {"status": "FINITE_PREFIX_AUDIT_INCONCLUSIVE" if failed else "FINITE_RECORDED_DATA_AUDIT_PASSED",
        "primary_status": status, "producer_status": producer["run"]["status"], "B_cases": cases,
        "controls": controls, "positive_accepted": False, "optimizer_replays": 0, "native_calls": 0,
        "scope": {"Born_law_certified": False, "TV_certified": False, "physical_replication": False,
            "interval_certificate": False, "compiler_timing": "source-bound before R; no independent endpoints",
            "factory_CPU_split": None, "clocks": "stored arithmetic, not authentic timing certification"}}


def main(argv=None):
    global _RUN_START
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    output = Path(args.output)
    insist(not output.is_absolute() and output.parts and ".." not in output.parts, "output", "safe project-relative directory", category="MALFORMED")
    current = root
    for part in output.parts:
        current /= part
        insist(not current.is_symlink(), "output", "symlink forbidden", category="MALFORMED")
    current.mkdir(parents=True, exist_ok=False)
    _RUN_START = time.process_time(), time.perf_counter()
    result, failure, code = {}, None, 1
    try:
        for name in THREADS:
            same(os.environ.get(name), "1", "auditor/preimport-thread-readback")
        binding = read_json(project_file(root, args.binding))
        same(binding["audit_output_directory"], args.output, "binding/output")
        result = audit_dataset(root, binding)
        code = 0
    except AuditIssue as error:
        failure = {"category": error.category, "location": error.location,
                   "message": str(error), "detail_repr": repr(error.detail)[:4096]}
        result = {"status": "AUDIT_RESOURCE_INCONCLUSIVE" if error.category == "RESOURCE" else "AUDIT_"+error.category,
                  "positive_accepted": False}
    except (KeyError, TypeError, IndexError) as error:
        failure = {"category": "SCHEMA", "location": "auditor/record-shape", "exception_repr": repr(error)[:4096]}
        result = {"status": "AUDIT_SCHEMA", "positive_accepted": False}
    except Exception as error:
        failure = {"category": "UNEXPECTED", "location": "auditor", "exception_repr": repr(error)[:4096]}
        result = {"status": "AUDIT_UNEXPECTED_FAILURE", "positive_accepted": False}
    finally:
        result["source_sha256"] = file_hash(Path(__file__))
        payloads = [(json.dumps(item, ensure_ascii=True, separators=(",", ":"), allow_nan=False)+"\n").encode("ascii")
                    for item in (result, failure)]
        insist(sum(map(len, payloads)) <= OUTPUT_BYTES, "audit-output", "512KiB guard", category="RESOURCE")
        for name, payload in zip(("audit_summary.json", "audit_failure.json"), payloads):
            with (current/name).open("xb") as stream:
                stream.write(payload)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
