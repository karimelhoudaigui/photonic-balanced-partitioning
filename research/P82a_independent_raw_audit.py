"""Independent P82a recorded-data checker; import performs no audit/RNG work.

No producer module, optical backend or optimizer is imported. NumPy/NetworkX
are lazy dependencies of the separately authorized POST-SEAL replay only.
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


CASES = ("ER8201601", "RR8201602")
FAST = ("FAST_RANDOM", "FAST_SPECTRAL")
CUSTOM = ("RECIPIENT_FRONTIER", "PHASE_HYPERPLANE", "CONTINUED_DESCENT", "MULTISWAP")
FILES = ("metadata.json", "graphs.json", "B_ER.jsonl", "B_RR.jsonl",
         "paid_ledger.jsonl", "controls.jsonl", "summary.json", "failure.json")
SOURCE_FREEZE = "94f80b94f75317524c202ce9ef5bf932d78ddc5e"
PRIMARY_SOURCE_SHA = "7e1a0d037f5fe0a6af036c1b2a92e765981c93e8d473535984e6f07ea7acfbbc"
PRIMARY_SPEC_SHA = "8598bd4220d1caadb20aed68601e92b4bba85db787bfe71b83efb6376151c838"
PRIMARY_PINS = {
    "research/P82a_split_scatter_veto.py": PRIMARY_SOURCE_SHA,
    "research/P82a_execution_spec.json": PRIMARY_SPEC_SHA,
    "research/P82a_IMPLEMENTATION_POPULATION.md": "9080adee7e67189731cdbcbd297c0b419748337025135f85cf7406bee5c1a4ba",
    "tests/test_p82a_split_scatter_veto.py": "e70b74c2915632cf62677c80f40ebeea8e67c669116660096426101542794861",
    "research/P82a_split_scatter_preflight_contract.json": "209696de0b0170ff4099cdfd77b6acdaec3c4f78e04e86631047008c13517c0d",
    "research/P82a_split_scatter_execution_contract.json": "dca509b4fee65b652227fb395cfc982b4426a9c8ae0da05de75f825493cc5f20",
    "research/P82_HARDWARE_COMPATIBLE_ESCAPE_DESIGN.md": "c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723",
    "research/P82a_DEV_VETO_CONTRACT.md": "d5e994d970f278bb9c51fa8a806555dce4047e82c8342f676fe267b75dbe71b9",
    "research/P82a_PREEXEC_CLOCK_ADDENDUM.md": "1b548885d05fe6a42487c77b12ac00292ebd8bd379c4074e6ce3a49ceb93a8d4",
    "research/P82a_CLOCK_ADDENDUM_REVIEW.md": "edeba00f839368b0c9ca6ef5f7a01befaa1a98527808d906c008f93218d77271",
    "research/P43_global_gain_probe.py": "b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777",
    "research/P50_fast_from_scratch.py": "6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86"}
P43_SHA = "b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777"
P50_SHA = "6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86"
RAW_BYTES = 32 * 1024 * 1024
OBJECT_BYTES = 4 * 1024 * 1024
OUTPUT_BYTES = 512 * 1024
MAX_B_ROWS = 5000
MAX_LEDGER_ROWS = 2000
MAX_CONTROL_ROWS = 20005
TOL = 3e-12
_POST_SEAL = object()


class AuditIssue(Exception):
    def __init__(self, category, location, message, detail=None):
        super().__init__(message)
        self.category, self.location, self.detail = category, location, detail


def insist(condition, location, message, detail=None, category="MISMATCH"):
    if not condition:
        raise AuditIssue(category, location, message, detail)


def integer(value, location, minimum=None):
    insist(type(value) is int, location, "integer required", repr(value), "MALFORMED")
    insist(minimum is None or value >= minimum, location, "integer below minimum", value, "MALFORMED")
    return value


def number(value, location, nonnegative=True):
    insist(type(value) in (int, float) and math.isfinite(value), location,
           "finite scalar required", repr(value), "MALFORMED")
    insist(not nonnegative or value >= 0, location, "negative duration", value, "MALFORMED")
    return float(value)


def zvalue(value, location):
    insist(isinstance(value, dict) and set(value) == {"real", "imag"}, location,
           "serialized complex pair required", category="MALFORMED")
    return complex(number(value["real"], location, False), number(value["imag"], location, False))


def fraction(value, location):
    insist(isinstance(value, dict) and set(value) == {"numerator", "denominator"},
           location, "serialized Fraction required", category="MALFORMED")
    return Fraction(integer(value["numerator"], location), integer(value["denominator"], location, 1))


def same(actual, expected, location):
    if type(expected) in (int, bool):
        insist(type(actual) is type(expected), location, "scalar type mismatch", repr(actual), "MALFORMED")
    insist(actual == expected, location, "recorded value disagrees", {"actual": actual, "expected": expected})


def near(actual, expected, location, tolerance=TOL):
    insist(abs(actual - expected) <= tolerance, location, "fixed numerical residual exceeded",
           {"actual": repr(actual), "expected": repr(expected), "absolute_tolerance": tolerance})


def graph_checked(graph, n=None):
    n = len(graph) if n is None else n
    insist(n >= 2 and n % 2 == 0 and len(graph) == n, "graph", "even square graph required", category="MALFORMED")
    insist(all(isinstance(row, list) and len(row) == n for row in graph),
           "graph", "square graph required", category="MALFORMED")
    for i, row in enumerate(graph):
        for j, weight in enumerate(row):
            integer(weight, "graph", 0)
            same(weight, graph[j][i], "graph/symmetry")
        same(row[i], 0, "graph/diagonal")
    return graph


def membership(values, n, location="subset"):
    insist(isinstance(values, (list, tuple)) and len(values) == n // 2, location,
           "half-sized subset required", category="MALFORMED")
    mask = 0
    for vertex in values:
        integer(vertex, location, 0)
        insist(vertex < n and not mask & (1 << vertex), location,
               "invalid/duplicate vertex", vertex, "MALFORMED")
        mask |= 1 << vertex
    return mask


def vertices(mask, n):
    return [i for i in range(n) if mask & (1 << i)]


def mask_read(text, n, location="mask"):
    insist(type(text) is str and len(text) == 2 * ((n + 7) // 8), location,
           "packed little-bit mask length", category="MALFORMED")
    try:
        raw = bytes.fromhex(text)
    except ValueError as error:
        raise AuditIssue("MALFORMED", location, "invalid hex mask") from error
    mask = int.from_bytes(raw, "little")
    insist(mask < (1 << n) and mask.bit_count() == n // 2, location,
           "mask padding/cardinality", text, "MALFORMED")
    return mask


def mask_hex(mask, n):
    return mask.to_bytes((n + 7) // 8, "little").hex()


def rank_checked(rank, n):
    insist(isinstance(rank, list) and all(type(x) is int for x in rank)
           and sorted(rank) == list(range(n)), "rank", "rank permutation required", category="MALFORMED")
    return rank


def orient(mask, rank):
    n = len(rank)
    pivot = rank.index(0)
    return mask if mask & (1 << pivot) else mask ^ ((1 << n) - 1)


def integer_cut(graph, mask):
    """Independent unordered-edge full sum; no producer delta arithmetic."""
    return sum(graph[i][j] for i in range(len(graph)) for j in range(i + 1, len(graph))
               if bool(mask & (1 << i)) != bool(mask & (1 << j)))


def swap_list(graph, mask, rank):
    inside = sorted(vertices(mask, len(graph)), key=lambda x: rank[x])
    outside = sorted((i for i in range(len(graph)) if not mask & (1 << i)), key=lambda x: rank[x])
    return [(a, b, orient(mask ^ (1 << a) ^ (1 << b), rank)) for a in inside for b in outside]


def descent_check(graph, rank, records, start, max_scans, location):
    """Reconstruct scalar costs and mathematical best-one-swap choices."""
    n, cursor, current = len(graph), 0, orient(start, rank)
    insist(records, location, "missing initial scored input", category="SCHEMA")
    same(mask_read(records[0]["mask_hex"], n), current, location + "/input")
    same(records[0]["cut"], integer_cut(graph, current), location + "/input-cut")
    same(records[0]["method"], "scalar_cut", location + "/input-method")
    cursor += 1
    scans, local = 0, False
    for _ in range(max_scans):
        candidates = swap_list(graph, current, rank)
        insist(cursor + len(candidates) <= len(records), location, "incomplete complete-scan evidence", category="SCHEMA")
        batch = records[cursor]["sequence"]
        evaluated = []
        for offset, (removed, added, candidate) in enumerate(candidates):
            row = records[cursor + offset]
            same(row["method"], "exact_swap_delta", location + "/method")
            same(row["batch"], batch, location + "/batch")
            same(row["batch_index"], offset, location + "/batch-index")
            same((row["removed"], row["added"]), (removed, added), location + "/swap-order")
            same(mask_read(row["mask_hex"], n), candidate, location + "/neighbor")
            value = integer_cut(graph, candidate)
            same(row["cut"], value, location + "/neighbor-cut")
            evaluated.append((value, rank[removed], rank[added], candidate))
        cursor += len(candidates)
        scans += 1
        best = min(evaluated)
        if best[0] >= integer_cut(graph, current):
            local = True
            break
        current = best[3]
    same(cursor, len(records), location + "/unregistered-score")
    return {"subset": vertices(current, n), "cut": integer_cut(graph, current),
            "scans": scans, "local_optimum": local}


def f4_exact():
    """Literal positive-sign Fourier convention, rational complex pairs."""
    roots = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)),
             (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(-1)))
    return [[tuple(x / 2 for x in roots[(r * j) % 4]) for j in range(4)] for r in range(4)]


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def exact_features(graph, tports, odds):
    insist(len(tports) == 8 and len(odds) == 4, "features", "F4 population required", category="MALFORMED")
    f = f4_exact()
    a, q, j = [], [], []
    for r in range(4):
        ar, qr, jr = [], [], []
        for s in range(4):
            terms = [cmul(f[r][k], (f[s][k][0], -f[s][k][1])) for k in range(4)]
            entry = (sum((odds[k] * terms[k][0] for k in range(4)), Fraction(0)),
                     sum((odds[k] * terms[k][1] for k in range(4)), Fraction(0)))
            contrast = 0 if r == s else (graph[tports[r]][tports[s]] + graph[tports[r + 4]][tports[s + 4]]
                - graph[tports[r]][tports[s + 4]] - graph[tports[r + 4]][tports[s]])
            ar.append(entry)
            qr.append(contrast)
            jr.append(Fraction(0) if r == s else contrast * (entry[0] ** 2 + entry[1] ** 2))
        a.append(ar)
        q.append(qr)
        j.append(jr)
    return a, q, j


def phase_trace_check(j, ids, trace, sweeps=2, analytic_zero=False):
    """Use ARCHIVED rounded J/phasors, including the exact floating zero test."""
    roots = (1 + 0j, 1j, -1 + 0j, -1j)
    d = len(j)
    insist(len(ids) == d and all(type(x) is int and 0 <= x < 4 for x in ids),
           "phase_ids", "root IDs", category="MALFORMED")
    insist(len(trace) == sweeps * d, "phase_trace", "complete sequential sweep trace", category="SCHEMA")
    phases = [roots[x] for x in ids]
    for position, record in enumerate(trace):
        r = position % d
        same((record["sweep"], record["coordinate"]), (position // d, r), "phase_trace/order")
        before = zvalue(record["before"], "phase_trace/before")
        same(before, phases[r], "phase_trace/archived-before")
        observed = zvalue(record["H"], "phase_trace/H")
        expected = 0j if analytic_zero else sum(j[r][s] * phases[s] for s in range(d) if s != r)
        same(observed, expected, "phase_trace/actual-rounded-H")
        after = zvalue(record["after"], "phase_trace/after")
        if observed == 0j:
            same(after, before, "phase_trace/exact-zero-keeps-phase")
        else:
            angle = math.atan2(observed.imag, observed.real)
            near(after, complex(math.cos(angle), math.sin(angle)), "phase_trace/atan2")
        phases[r] = after
    return phases


def split_profile():
    return [Fraction(1, 3), Fraction(5, 11), Fraction(7, 13), Fraction(3, 5)] * 2


def compiler_check(graph, tports, ids, recorded, uniform_null=False):
    odds = [Fraction(1) for _ in range(4)] if uniform_null else [Fraction(1, 2), Fraction(5, 6), Fraction(7, 6), Fraction(3, 2)]
    a, q, exact_j = exact_features(graph, tports, odds)
    same(recorded["analytic_uniform_null"], uniform_null, "compiler/null-branch")
    same(recorded["Q"], q, "compiler/integer-Q")
    insist(len(recorded["A"]) == len(recorded["J"]) == 4
           and all(len(row) == 4 for row in recorded["A"] + recorded["J"]),
           "compiler/features", "four square rows", category="MALFORMED")
    j = []
    for r in range(4):
        row = []
        for s in range(4):
            near(zvalue(recorded["A"][r][s], "compiler/A"),
                 complex(float(a[r][s][0]), float(a[r][s][1])), "compiler/exact-A")
            value = number(recorded["J"][r][s], "compiler/J", False)
            if uniform_null:
                same(value, 0.0, "compiler/analytic-zero-J")
            else:
                near(value, float(exact_j[r][s]), "compiler/exact-J")
            row.append(value)
        j.append(row)
    phases = phase_trace_check(j, ids, recorded["phase_trace"], analytic_zero=uniform_null)
    insist(len(recorded["phases"]) == 4 and len(recorded["W"]) == 8,
           "compiler", "matrix dimensions", category="MALFORMED")
    for actual, expected in zip(recorded["phases"], phases):
        same(zvalue(actual, "compiler/phases"), expected, "compiler/phase-lineage")
    f = [[complex(float(x), float(y)) for x, y in row] for row in f4_exact()]
    expected_w = []
    for sign in (1, -1):
        for r in range(4):
            expected_w.append([math.sqrt(0.5) * x for x in f[r]]
                + [sign * math.sqrt(0.5) * phases[r] * x for x in f[r]])
    w = []
    for r, row in enumerate(recorded["W"]):
        insist(len(row) == 8, "compiler/W", "eight receiving columns", category="MALFORMED")
        w.append([zvalue(x, "compiler/W") for x in row])
        for actual, expected in zip(w[-1], expected_w[r]):
            near(actual, expected, "compiler/W-from-archived-phases")
    gram = max(abs(sum(w[r][i].conjugate() * w[r][j] for r in range(8)) - int(i == j)) for i in range(8) for j in range(8))
    flat = max(abs(abs(x) ** 2 - 1 / 8) for row in w for x in row)
    probabilities = [Fraction(1, 2)] * 8 if uniform_null else split_profile()
    frame = max(abs((1 - float(probabilities[i])) * int(i == j)
        + math.sqrt(float(probabilities[i]) * float(probabilities[j]))
        * sum(w[r][i].conjugate() * w[r][j] for r in range(8)) - int(i == j)) for i in range(8) for j in range(8))
    for name, value in (("gram_error", gram), ("flat_probability_error", flat), ("occupied_frame_error", frame)):
        insist(value <= TOL, "compiler/" + name, "runtime invariant exceeded")
        near(number(recorded["guards"][name], name), value, "compiler/recorded-guard")


def decoded_check(source, target, removed, y, recorded, fill):
    k = len(source)
    same(sorted(source + target), list(range(2 * k)), "ports/partition")
    insist(all(type(i) is int for i in removed) and removed == sorted(set(removed))
           and all(0 <= i < k for i in removed), "removed_ports", "sorted distinct input ports", category="MALFORMED")
    insist(len(y) == k and all(type(x) is int and x >= 0 for x in y),
           "counts", "nonnegative full counts", category="MALFORMED")
    same(sum(y), len(removed), "counts/receiving-total")
    support = [target[i] for i, count in enumerate(y) if count]
    available = sorted(set(target) - set(support))
    need = len(removed) - len(support)
    used = 0 < need < len(available)
    repair = fill(available, need) if used else available if need else []
    same(recorded["repair"], repair, "repair/seeded-fill")
    same(recorded["repair_rng_used"], used, "repair/usage")
    full = [int(i not in removed) for i in range(k)] + y
    mapped = [0] * (2 * k)
    for i, count in enumerate(full):
        mapped[(source + target)[i]] = count
    expected_subset = sorted([source[i] for i in range(k) if i not in removed] + support + repair)
    same(recorded["full_counts"], full, "counts/full-port-counts")
    same(recorded["vertex_counts"], mapped, "counts/vertex-mapping")
    same(sum(full), k, "counts/full-injected-total")
    same(recorded["subset"], expected_subset, "decoder/subset")
    same(recorded["R"], [source[i] for i in removed], "decoder/R-labels")
    same((recorded["r"], recorded["h"]), (len(removed), len(support)), "decoder/r-h")
    return membership(expected_subset, 2 * k)


def null_fill_identity(k, r, h):
    insist(type(k) is int and 0 <= h <= r <= k, "null", "binomial identity domain", category="MALFORMED")
    return Fraction(math.comb(r, h), math.comb(k, h) * math.comb(k - h, r - h))


def observed_span(row):
    same(row["kind"], "OBSERVED_SPAN", "span/kind")
    for domain in ("cpu", "wall"):
        start = number(row["start_" + domain], "span/start")
        end = number(row["end_" + domain], "span/end")
        insist(end >= start, "span", "clock reversed", category="MALFORMED")
        same(number(row[domain + "_seconds"], "span/duration"), end - start, "span/duration-endpoints")


def duration_gap(outer, adapter, reported):
    values = [number(x, "call_gap") for x in (outer[0], outer[1], adapter[0], adapter[1], reported[0], reported[1])]
    cpu, wall = values[0] - values[2] - values[4], values[1] - values[3] - values[5]
    insist(cpu >= 0 and wall >= 0, "call_gap", "negative un-clipped derived gap")
    return cpu, wall


def select_checkpoint(rows, adapter_cpu, adapter_wall, grant, graph, custom=False, scores=()):
    ac, aw, g = [number(x, "eligibility") for x in (adapter_cpu, adapter_wall, grant)]
    insist(len(rows) <= 10001, "checkpoints", "trace guard exceeded", category="MALFORMED")
    previous, previous_cut, chosen, first_scan = (-1.0, -1.0, -1), None, None, False
    score_best, score_cursor = None, 0
    for index, row in enumerate(rows):
        same(row["index"], index, "checkpoint/index")
        cpu, wall = number(row["cpu_seconds"], "checkpoint/cpu"), number(row["wall_seconds"], "checkpoint/wall")
        work = integer(row["work"], "checkpoint/work", 0)
        insist(work <= 10000 and cpu >= previous[0] and wall >= previous[1] and work >= previous[2],
               "checkpoints", "nonmonotone clocks/work or work guard", category="MALFORMED")
        previous = cpu, wall, work
        cached = row["cached_best"] if custom else {"cut": row["cut"], "mask_hex": row["mask_hex"]}
        if custom:
            while score_cursor < len(scores) and scores[score_cursor]["work"] <= work:
                item = scores[score_cursor]
                if score_best is None or item["cut"] < score_best["cut"]:
                    score_best = {"cut": item["cut"], "mask_hex": item["mask_hex"]}
                score_cursor += 1
            same(cached, score_best, "checkpoint/custom-preclock-best-lineage")
        if cached is not None:
            value = integer(cached["cut"], "checkpoint/cut", 0)
            mask = mask_read(cached["mask_hex"], len(graph))
            same(value, integer_cut(graph, mask), "checkpoint/independent-cut")
            insist(previous_cut is None or value <= previous_cut, "checkpoint", "best cut increased", category="MALFORMED")
            previous_cut = value
        timely = ac + cpu <= g and aw + wall <= g
        if row["stage"] == "initial_scan" and timely:
            first_scan = True
        if timely and cached is not None:
            chosen = {"index": index, "cut": cached["cut"], "mask_hex": cached["mask_hex"],
                      "cpu_seconds": cpu, "wall_seconds": wall, "total_cpu": ac + cpu, "total_wall": aw + wall,
                      "provenance": "custom_online_preclock_RAM_prefix" if custom else "archived_preclock_RAM_prefix"}
    return chosen, first_scan


def record_by_type(rows, kind):
    return [row for row in rows if row.get("type") == kind]


def one(rows, location):
    insist(len(rows) == 1, location, "one associated record required", len(rows), "SCHEMA")
    return rows[0]


def expect_state(record, mask, graph, location):
    same(membership(record["subset"], len(graph)), mask, location + "/mask")
    same(record["cut"], integer_cut(graph, mask), location + "/cut")


def case_audit(case, graph, rows, ledger, replay, require_complete):
    if not rows:
        insist(not require_complete, case, "missing complete B stream", category="SCHEMA")
        return {"complete": False, "completed": 0, "requested": 0, "r_histogram": [0] * 9}
    start = one(record_by_type(rows, "case_start"), case + "/case_start")
    allowed = {"case_start", "score", "reset", "attempt_request", "factory_report",
               "native_not_called", "native_observation", "attempt_outcome", "case_result"}
    insist(all(row.get("type") in allowed for row in rows), case, "unknown B record type", category="MALFORMED")
    same(start["case"], case, case + "/identity")
    rank = rank_checked(start["priority_rank"], 16)
    priority = replay.permutation(case, "B", "priority", list(range(16)))
    same(rank, [priority.index(i) for i in range(16)], case + "/priority-replay")
    total_weight = sum(graph[i][j] for i in range(16) for j in range(i + 1, 16))
    same(start["total_edge_weight"], total_weight, case + "/total_weight")
    cache = start["cache"]["profile"]
    same([fraction(x, "cache/probabilities") for x in cache["probabilities"]], split_profile(), case + "/profile")
    same([fraction(x, "cache/odds") for x in cache["odds"]],
         [Fraction(1, 2), Fraction(5, 6), Fraction(7, 6), Fraction(3, 2)], case + "/odds")
    same(fraction(cache["rho"], "cache/rho"), Fraction(1), case + "/rho")
    same(fraction(cache["eta"], "cache/eta"), Fraction(1, 2), case + "/eta")
    groups, best_at, best = {}, [], None
    score_rows = record_by_type(rows, "score")
    for sequence, score in enumerate(score_rows):
        same(score["sequence"], sequence, case + "/score-sequence")
        mask = mask_read(score["mask_hex"], 16)
        same(orient(mask, rank), mask, case + "/canonical-score")
        value = integer(score["cut"], case + "/score-cut", 0)
        same(value, integer_cut(graph, mask), case + "/independent-score")
        owner = score["owner_span"]
        insist(owner in ledger["by_id"] and ledger["by_id"][owner]["paid"],
               case + "/score-owner", "score must have a paid owner", owner, "SCHEMA")
        groups.setdefault(owner, []).append(score)
        if best is None or value < best["cut"]:
            best = {"cut": value, "subset": vertices(mask, 16),
                    "mask_hex": score["mask_hex"], "score_sequence": sequence}
        best_at.append(best)
    events = [row for row in rows if row.get("type") != "score"]
    positions = {}
    for pos, row in enumerate(events):
        kind = row.get("type")
        if kind in ("reset", "attempt_request", "native_observation", "attempt_outcome", "factory_report", "native_not_called"):
            key = kind, row["chain"], row.get("step")
            insist(key not in positions, case, "duplicate B event", key, "MALFORMED")
            positions[key] = pos
    requests = record_by_type(rows, "attempt_request")
    same([(r["chain"], r["step"]) for r in requests],
         [(i // 16, i % 16) for i in range(len(requests))], case + "/request-prefix")
    insist(len(requests) <= 48, case, "too many attempts", category="MALFORMED")
    outcomes = record_by_type(rows, "attempt_outcome")
    same([(r["chain"], r["step"]) for r in outcomes],
         [(i // 16, i % 16) for i in range(len(outcomes))], case + "/outcome-prefix")
    raw_cuts, q_cuts, hist, chain_results, consumed = [], [], [0] * 9, [], set()
    pending = None
    previous_outcome_position = -1
    for chain in range(3):
        reset_rows = [x for x in events if x.get("type") == "reset" and x["chain"] == chain]
        if not reset_rows:
            break
        reset = one(reset_rows, case + "/reset")
        insist(positions["reset", chain, None] > previous_outcome_position, case, "reset before preceding chain ended")
        owner = ledger["spans"].get(("reset_start_and_warmstart", chain, None))
        insist(owner is not None, case, "missing reset paid span", category="SCHEMA")
        scored = groups.get(owner["id"], [])
        consumed.add(owner["id"])
        reset_order = replay.permutation(case, "B", "reset_start", list(range(16)), chain)
        initial_mask = orient(membership(reset_order[:8], 16), rank)
        same(membership(reset["start"], 16), initial_mask, case + "/own-reset")
        same(reset["start_cut"], integer_cut(graph, initial_mask), case + "/reset-cut")
        warm = descent_check(graph, rank, scored, initial_mask, 2, case + "/warm")
        same(reset["warmstart"], warm, case + "/warm-result")
        current = membership(warm["subset"], 16)
        chain_best = {"subset": warm["subset"], "cut": warm["cut"]}
        chain_complete = True
        for step in range(16):
            key = "attempt_request", chain, step
            if key not in positions:
                chain_complete = False
                break
            request = events[positions[key]]
            insist(positions[key] > max(previous_outcome_position, positions["reset", chain, None]),
                   case, "request before reset/prior outcome")
            same(request["case"], case, case + "/request-case")
            same(request["full_source_photons"], 8, case + "/source-photons")
            expect_state(request["current_before"], current, graph, case + "/fresh-current")
            source = replay.permutation(case, "B", "portS", vertices(current, 16), chain, step)
            target = replay.permutation(case, "B", "portT", vertices(current ^ 65535, 16), chain, step)
            same(request["source_order"], source, case + "/source-order")
            same(request["target_order"], target, case + "/target-order")
            ids = replay.phase_ids(case, chain, step)
            same(request["phase_ids"], ids, case + "/phase-root-replay")
            compiler_check(graph, target, ids, request["compiler"])
            coins = replay.split_coins(case, chain, step)
            same(request["split_coins"], coins, case + "/split-replay")
            removed = [i for i, p in enumerate(split_profile()) if coins[i] < p.numerator]
            same(request["removed_ports"], removed, case + "/removed-ports")
            native_role = replay.role(case, "B", "native", chain, step)
            repair_role = replay.role(case, "B", "repair", chain, step)
            same(request["native_role"], native_role, case + "/native-role")
            same(request["repair_role"], repair_role, case + "/repair-role")
            same(request["native_seed"], replay.seed(native_role, True), case + "/native-seed")
            same(request["repair_seed"], replay.seed(repair_role), case + "/repair-seed")
            result_key = "attempt_outcome", chain, step
            if result_key not in positions:
                pending = {"chain": chain, "step": step, "request_retained": True}
                chain_complete = False
                break
            observed = events[positions["native_observation", chain, step]]
            outcome = events[positions[result_key]]
            previous_outcome_position = positions[result_key]
            insist(positions[key] < positions["native_observation", chain, step] < positions[result_key],
                   case, "request/observation/outcome order")
            same(observed["fallback"], False, case + "/fallback")
            same(outcome["fallback"], False, case + "/fallback")
            same(observed["receiver_counts"], outcome["receiver_counts"], case + "/count-lineage")
            if removed:
                factory = events[positions["factory_report", chain, step]]
                insist(("native_not_called", chain, step) not in positions, case, "spurious native-not-called")
                outer = ledger["spans"].get(("factory_total", chain, step))
                sample = ledger["spans"].get(("serial_native_sample", chain, step))
                insist(outer is not None and sample is not None, case, "missing native spans", category="SCHEMA")
                same(factory["outer_ref"], outer["id"], case + "/factory-ref")
                same(factory["reported_ref"], ledger["by_id"][factory["duration_difference_ref"]]["reported_ref"],
                     case + "/factory-reported-ref")
                same(factory["backend_setup_wall"],
                     ledger["by_id"][factory["duration_difference_ref"]]["reported_setup_wall_seconds"],
                     case + "/reported-setup-lineage")
            else:
                omitted = events[positions["native_not_called", chain, step]]
                same(omitted["reason"], "r=0", case + "/native-zero-branch")
                insist(("factory_report", chain, step) not in positions
                       and ("factory_total", chain, step) not in ledger["spans"]
                       and ("serial_native_sample", chain, step) not in ledger["spans"],
                       case, "r0 fabricated native work")
            candidate = decoded_check(source, target, removed, observed["receiver_counts"], outcome["decoded"],
                lambda available, count: replay.permutation(case, "B", "repair", available, chain, step)[:count])
            candidate = orient(candidate, rank)
            same(outcome["raw_cut"], integer_cut(graph, candidate), case + "/proposal-cut")
            span = ledger["spans"].get(("attempt_post_decode_score_quench_accept", chain, step))
            insist(span is not None, case, "missing paid quench span", category="SCHEMA")
            scored = groups.get(span["id"], [])
            consumed.add(span["id"])
            quench = descent_check(graph, rank, scored, candidate, 1, case + "/Q")
            same(outcome["quench"], quench, case + "/Q-best-not-last")
            accepted = quench["cut"] < integer_cut(graph, current)
            same(outcome["accepted"], accepted, case + "/strict-accept")
            if accepted:
                current = membership(quench["subset"], 16)
            expect_state(outcome["current_after"], current, graph, case + "/current-after")
            if quench["cut"] < chain_best["cut"]:
                chain_best = {"subset": quench["subset"], "cut": quench["cut"]}
            same(outcome["chain_best"], chain_best, case + "/own-chain-best")
            insist(scored, case, "missing actual paid scores")
            same(outcome["all_paid_best"], best_at[scored[-1]["sequence"]], case + "/all-neighbor-credit")
            hist[len(removed)] += 1
            raw_cuts.append(outcome["raw_cut"])
            q_cuts.append(quench["cut"])
        if chain_complete:
            chain_results.append({"chain": chain, "warmstart_cut": warm["cut"], "best": chain_best,
                                  "current": {"subset": vertices(current, 16), "cut": integer_cut(graph, current)},
                                  "gain_from_warmstart": warm["cut"] - chain_best["cut"]})
        else:
            break
    results = record_by_type(rows, "case_result")
    complete = len(results) == 1
    insist(not require_complete or complete, case, "missing full B case result", category="SCHEMA")
    if complete:
        same(len(raw_cuts), 48, case + "/complete-population")
        same(len(requests), 48, case + "/requested-population")
        same(set(groups), consumed, case + "/unowned-complete-score-batches")
        result = results[0]
        same(result["case"], case, case + "/result-case")
        same(len(events), 197, case + "/full-event-population")
        for key, expected in (("requested", 48), ("completed", 48), ("full_source_photons", 384),
                              ("scored_candidates", len(score_rows)), ("r_histogram", hist),
                              ("conditional_receiver_photons", sum(i * x for i, x in enumerate(hist))),
                              ("chains", chain_results), ("all_paid_best", best),
                              ("paid_component_ids", ledger["paid_ids"]), ("grant_wall_seconds", ledger["grant"])):
            same(result[key], expected, case + "/" + key)
        for key, expected in (("raw_mean_cut", Fraction(sum(raw_cuts), 48)),
                              ("q_mean_cut", Fraction(sum(q_cuts), 48)),
                              ("raw_mean_normalized", Fraction(sum(raw_cuts), 48 * total_weight) if total_weight else Fraction(0)),
                              ("q_mean_normalized", Fraction(sum(q_cuts), 48 * total_weight) if total_weight else Fraction(0))):
            same(fraction(result[key], key), expected, case + "/" + key)
    return {"complete": complete, "completed": len(raw_cuts), "requested": len(requests), "r_histogram": hist,
            "macro_r4": hist[4], "scored_candidates": len(score_rows), "all_paid_best": best,
            "grant": ledger["grant"], "pending": pending}


def reported_duration(row, helper_path, helper_sha, cpu_known):
    same(row["kind"], "REPORTED_DURATION", "reported/kind")
    same(row["paid"], False, "reported/paid")
    same(row["helper_source_path"], helper_path, "reported/helper")
    same(row["helper_source_sha256"], helper_sha, "reported/helper-sha")
    for name in ("start_cpu", "end_cpu", "start_wall", "end_wall"):
        same(row[name], None, "reported/unknown-endpoints")
    number(row["wall_seconds"], "reported/wall")
    if cpu_known:
        number(row["cpu_seconds"], "reported/cpu")
    else:
        same(row["cpu_seconds"], None, "reported/unknown-cpu")


def grant_audit(rows, case, complete):
    relevant = [row for row in rows if row.get("case") == case]
    by_id, spans, direct, excluded, residuals, paid = {}, {}, [], [], [], []
    for row in relevant:
        insist(type(row["paid"]) is bool, "ledger", "paid flag must be Boolean", category="MALFORMED")
        if "id" in row:
            insist(row["id"] not in by_id, "ledger", "duplicate event ID", row["id"], "MALFORMED")
            by_id[row["id"]] = row
        if row["kind"] == "OBSERVED_SPAN":
            observed_span(row)
            if row["label"] != "synthetic_input_generation":
                context = row.get("context", {})
                key = row["label"], context.get("chain"), context.get("step")
                insist(key not in spans, "ledger", "duplicate span owner", key, "MALFORMED")
                spans[key] = row
            if row["paid"]:
                direct.append(row)
            elif row["label"] in ("factory_total", "serial_native_sample"):
                excluded.append(row)
        elif row["kind"] == "REPORTED_DURATION":
            reported_duration(row, "research/P43_global_gain_probe.py", P43_SHA, False)
        elif row["kind"] == "DURATION_DIFF":
            same(row["paid"], True, "factory-residual/paid")
            for name in ("cpu_seconds", "start_cpu", "end_cpu", "start_wall", "end_wall"):
                same(row[name], None, "factory-residual/unknown")
            residuals.append(row)
        else:
            raise AuditIssue("MALFORMED", "ledger", "unknown event kind", row["kind"])
        if row["paid"]:
            insist("id" in row, "ledger", "paid record lacks ID", category="SCHEMA")
            paid.append(row)
    seen_outer, seen_report = set(), set()
    for row in residuals:
        outer, reported = by_id.get(row["outer_ref"]), by_id.get(row["reported_ref"])
        insist(outer is not None and reported is not None, "factory-residual", "dangling operands", category="SCHEMA")
        same(outer["kind"], "OBSERVED_SPAN", "factory-residual/outer")
        same(outer["label"], "factory_total", "factory-residual/outer")
        same(outer["paid"], False, "factory-residual/outer-not-paid")
        same(reported["outer_ref"], outer["id"], "factory-residual/reported-outer")
        insist(outer["id"] not in seen_outer and reported["id"] not in seen_report,
               "factory-residual", "operand charged twice")
        seen_outer.add(outer["id"])
        seen_report.add(reported["id"])
        reported_wall = number(reported["wall_seconds"], "factory/reported")
        insist(reported_wall <= outer["wall_seconds"], "factory", "negative factory residual")
        same(row["reported_setup_wall_seconds"], reported_wall, "factory/reported-copy")
        same(row["wall_seconds"], outer["wall_seconds"] - reported_wall, "factory/residual-formula")
        same(row["formula"], "factory_outer_wall - setup_reported_wall", "factory/formula")
    if complete:
        same(seen_outer, {x["id"] for x in excluded if x["label"] == "factory_total"}, "factory/all-operands")
        same(seen_report, {x["id"] for x in relevant if x["kind"] == "REPORTED_DURATION"}, "factory/reported-once")
    for domain in ("wall", "cpu"):
        ordered = sorted(direct, key=lambda x: x["start_" + domain])
        for left, right in zip(ordered, ordered[1:]):
            insist(left["end_" + domain] <= right["start_" + domain], "ledger", "paid spans overlap")
        for left in direct:
            for right in excluded:
                insist(min(left["end_" + domain], right["end_" + domain])
                       <= max(left["start_" + domain], right["start_" + domain]),
                       "ledger", "direct paid/native containing spans overlap")
    return {"by_id": by_id, "spans": spans, "paid_ids": [x["id"] for x in paid],
            "grant": sum(x["wall_seconds"] for x in paid),
            "known_direct_paid_cpu": sum(x["cpu_seconds"] for x in direct),
            "factory_cpu_allocation": None}


def control_audit(block, graph, grant, replay):
    header = one(record_by_type(block, "control_header"), "control/header")
    result = one(record_by_type(block, "control_result"), "control/result")
    insist(type(result["normal_return"]) is bool, "control", "normal-return flag required", category="MALFORMED")
    case, mode = header["case"], header["mode"]
    insist(all(row.get("type") in {"control_header", "control_result", "checkpoint", "custom_score"}
               for row in block), "control", "unknown control record type", category="MALFORMED")
    same((result["case"], result["mode"]), (case, mode), "control/identity")
    same(result["grant"], grant, "control/whole-B-grant")
    role = replay.role(case, mode, "control")
    same(header["seed_role"], role, "control/private-role")
    same(header["seed"], replay.seed(role), "control/private-seed")
    ac, aw = number(result["adapter_cpu"], "adapter/cpu"), number(result["adapter_wall"], "adapter/wall")
    for domain, offset in (("cpu", ac), ("wall", aw)):
        index = 0 if domain == "cpu" else 1
        same(offset, result["solver_boundary"][index] - result["adapter_start"][index],
             "control/adapter-endpoints") if mode in CUSTOM else None
    checkpoints = record_by_type(block, "checkpoint")
    for row in block:
        same((row["case"], row["mode"]), (case, mode), "control/row-owner")
    charged_c, charged_w = ac, aw
    custom = mode in CUSTOM
    scores = record_by_type(block, "custom_score")
    if custom:
        same(result["solver_start"], result["solver_boundary"], "custom/clock-origin")
        for index, row in enumerate(scores, 1):
            same(row["work"], index, "custom/actual-score-work")
            mask = mask_read(row["mask_hex"], len(graph))
            same(integer(row["cut"], "custom/cut", 0), integer_cut(graph, mask), "custom/independent-cut")
        same(result["work"], len(scores), "custom/total-work")
        same(result["early_guard"], result["stop_reason"] == "work_guard", "custom/guard")
    else:
        insist(mode in FAST, "control", "unknown fixed mode", mode, "MALFORMED")
        same(header["adapter_cpu"], ac, "FAST/adapter")
        same(header["adapter_wall"], aw, "FAST/adapter")
        observed_span(header["observed_outer"])
        observed_span(header["observed_direct_adapter"])
        outer = header["observed_outer"]
        adapter = header["observed_direct_adapter"]
        reported = header["reported_compute_duration"]
        reported_duration(reported, "research/P50_fast_from_scratch.py", P50_SHA, True)
        same(reported["case"], case, "FAST/reported-case")
        same(reported["mode"], mode, "FAST/reported-mode")
        same((adapter["cpu_seconds"], adapter["wall_seconds"]), (ac, aw), "FAST/adapter-operands")
        same((outer["start_cpu"], outer["start_wall"]), tuple(header["adapter_start"]), "FAST/outer-start")
        same((outer["end_cpu"], outer["end_wall"]), tuple(header["call_end"]), "FAST/outer-end")
        same((header["actual_total_cpu"], header["actual_total_wall"]),
             (outer["cpu_seconds"], outer["wall_seconds"]), "FAST/total-observations")
        same((adapter["end_cpu"], adapter["end_wall"]), tuple(header["solver_boundary"]), "FAST/direct-boundary")
        same(reported["cpu_seconds"], result["result"]["compute_cpu_seconds"], "FAST/reported-compute")
        same(reported["wall_seconds"], result["result"]["compute_wall_seconds"], "FAST/reported-compute")
        dc, dw = duration_gap((outer["cpu_seconds"], outer["wall_seconds"]), (ac, aw),
                              (reported["cpu_seconds"], reported["wall_seconds"]))
        gap = header["call_boundary_difference"]
        same(gap, result["call_boundary_difference"], "FAST/gap-copy")
        same(gap["kind"], "CONSERVATIVE_DURATION_DIFF", "FAST/gap-type")
        same((gap["cpu_seconds"], gap["wall_seconds"]), (dc, dw), "FAST/gap-values")
        for key in ("start_cpu", "end_cpu", "start_wall", "end_wall"):
            same(gap[key], None, "FAST/gap-endpoints-unknown")
        same((gap["outer_ref"], gap["direct_adapter_ref"], gap["reported_ref"]),
             (outer["id"], adapter["id"], reported["id"]), "FAST/gap-lineage")
        charged_c, charged_w = ac + dc, aw + dw
        same((header["witness_charged_adapter_cpu"], header["witness_charged_adapter_wall"]),
             (charged_c, charged_w), "FAST/conservative-whole-gap")
        same(header["solver_cpu_budget"], max(0.0, grant - ac), "FAST/helper-CPU-budget")
        direct, _ = select_checkpoint(checkpoints, ac, aw, grant, graph)
        same(result["direct_selected"], direct, "FAST/direct-diagnostic-only")
        same(result["early_guard"], bool(result["result"].get("early_cap_inconclusive", False)), "FAST/guard-preserved")
        insist(not scores, "FAST", "unregistered custom score stream")
    selected, first_scan = select_checkpoint(checkpoints, charged_c, charged_w, grant, graph, custom, scores)
    for row in checkpoints:
        timely = charged_c + row["cpu_seconds"] <= grant and charged_w + row["wall_seconds"] <= grant
        same(row["dual_timely"], timely, "checkpoint/binding-dual-clock")
        if not custom:
            same(row["direct_dual_timely"], ac + row["cpu_seconds"] <= grant and aw + row["wall_seconds"] <= grant,
                 "checkpoint/direct-diagnostic")
    same(result["selected"], selected, "control/latest-existing-prefix")
    same(result["first_scan_dual_timely"], first_scan, "control/initial-scan-dual-clock")
    eligible = selected is not None and first_scan and not result["early_guard"]
    same(result["eligible"], eligible, "control/nonveto-eligibility")
    return {"case": case, "mode": mode, "selected": selected, "eligible": eligible,
            "normal_return": result["normal_return"], "checkpoints": len(checkpoints),
            "actual_custom_scores": len(scores)}


def fixed_winner(results, b_cases, modes):
    for mode in modes:
        panel = {x["case"]: x for x in results if x["mode"] == mode}
        if set(panel) == set(CASES) and all(panel[c]["normal_return"] and panel[c]["selected"] is not None
                and panel[c]["selected"]["cut"] < b_cases[c]["all_paid_best"]["cut"] for c in CASES):
            return mode
    return None


def decision_audit(summary, controls, b_cases):
    same(summary["positive_accepted"], False, "decision/no-positive")
    expected_order = [(mode, case) for mode in FAST + CUSTOM for case in CASES]
    order = [(x["mode"], x["case"]) for x in controls]
    same(order, expected_order[:len(order)], "decision/fixed-call-order")
    insist(len(controls) >= 4 and all(x["normal_return"] for x in controls),
           "decision", "four normal Tier1 returns required", category="SCHEMA")
    fast, custom = controls[:4], controls[4:]
    winner = fixed_winner(fast, b_cases, FAST)
    if winner:
        status = "DEV_REJECTED_FIXED_FAST"
        same(len(custom), 0, "decision/Tier2-not-run-after-FAST-veto")
    elif any(not x["eligible"] for x in fast):
        status = "INCONCLUSIVE_FAST_ELIGIBILITY"
        same(len(custom), 0, "decision/Tier2-not-run-after-FAST-ineligible")
    else:
        same(len(custom), 8, "decision/full-Tier2-panel")
        winner = fixed_winner(custom, b_cases, CUSTOM)
        status = ("DEV_REJECTED_FIXED_CLASSICAL" if winner else
                  "INCONCLUSIVE_CONTROL_ELIGIBILITY" if any(not x["eligible"] for x in custom) else
                  "STAGE1_REOPTIMIZED_D_SPECIES_REQUIRED")
    same(summary["status"], status, "decision/status")
    if winner:
        same(summary["veto_mode"], winner, "decision/same-mode-both-anchors")
    population = summary["control_population"]
    same([(x["mode"], x["case"]) for x in population], expected_order, "decision/population")
    for index, row in enumerate(population):
        if index < len(controls):
            same(row["status"], "COMPLETE", "decision/completed-call")
            same(row["outcome"], {"selected": controls[index]["selected"], "eligible": controls[index]["eligible"]},
                 "decision/population-outcome")
        else:
            same(row["status"], "NOT_RUN", "decision/unrun-status")
            same(row["outcome"], None, "decision/no-fabricated-unrun-result")
    same(summary["D_species"]["status"], "NOT_RUN", "decision/optional-not-run")
    if not custom:
        same(summary["tier2_status"]["status"], "NOT_RUN", "decision/Tier2-reason")
        insist(bool(summary["tier2_status"].get("reason")), "decision", "missing NOT_RUN reason", category="SCHEMA")
    return status


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        insist(key not in result, "json", "duplicate JSON key", key, "MALFORMED")
        result[key] = value
    return result


def decode_json(raw, location):
    try:
        return json.loads(raw, object_pairs_hook=strict_object,
                          parse_float=lambda x: number(float(x), "json", False),
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    except (ValueError, UnicodeError) as error:
        raise AuditIssue("MALFORMED", location, "invalid/nonfinite JSON", repr(error)) from error


def load_json(path):
    insist(path.stat().st_size <= OBJECT_BYTES, str(path), "single JSON input guard", category="RESOURCE")
    return decode_json(path.read_text(encoding="ascii"), str(path))


def lines(path, maximum):
    count = 0
    with path.open("rb") as stream:
        for raw in stream:
            count += 1
            insist(count <= maximum and len(raw) <= OBJECT_BYTES, str(path), "record guard exceeded", category="RESOURCE")
            insist(raw.endswith(b"\n"), str(path), "unterminated JSONL prefix", category="PARTIAL")
            row = decode_json(raw, str(path) + ":" + str(count))
            insist(isinstance(row, dict), str(path), "record object required", category="MALFORMED")
            yield row


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def project_path(root, relative, directory=False):
    insist(type(relative) is str and relative and not Path(relative).is_absolute()
           and ".." not in Path(relative).parts, "path", "project-relative path required", relative, "PROVENANCE")
    path = root
    for part in Path(relative).parts:
        path = path / part
        insist(not path.is_symlink(), "path", "symlink forbidden", relative, "PROVENANCE")
    insist(path.resolve().is_relative_to(root.resolve()), "path", "path escaped project", relative, "PROVENANCE")
    if directory:
        insist(path.is_dir(), "path", "directory missing", relative, "PARTIAL")
    else:
        insist(path.is_file(), "path", "input file missing", relative, "PARTIAL")
    return path


def authorize_binding(binding):
    same(binding.get("schema"), "P82a.independent-recorded-audit-binding.v1", "binding/schema")
    insist(binding.get("binding_state") == "SEALED_POST_B_RAW_AUTHORIZED"
           and binding.get("b_raw_sealed") is True and binding.get("audit_authorized") is True,
           "binding", "unbound/unsealed/unauthorized audit main", category="AUTHORIZATION")
    same(binding["producer_source_freeze"], SOURCE_FREEZE, "binding/producer-freeze")
    same(binding["producer_source_sha256"], PRIMARY_SOURCE_SHA, "binding/producer-source")
    same(binding["producer_spec_sha256"], PRIMARY_SPEC_SHA, "binding/producer-spec")
    return _POST_SEAL


class MainReplay:
    """Only this POST-SEAL boundary imports numerical packages or creates RNGs."""
    def __init__(self, token):
        insist(token is _POST_SEAL, "replay", "post-seal authorization required", category="AUTHORIZATION")
        for name, expected in (("numpy", "2.4.6"), ("networkx", "3.6.1")):
            same(importlib.metadata.version(name), expected, "replay/version/" + name)
        import numpy
        import networkx
        self.np, self.nx = numpy, networkx

    @staticmethod
    def role(case, arm, name, chain=-1, step=-1):
        return ["P82a", 82026001, case, arm, chain, step, name, 0]

    @staticmethod
    def seed(role, native=False):
        value = hashlib.sha256(json.dumps(role, ensure_ascii=True, separators=(",", ":")).encode("ascii")).digest()
        return 1 + int.from_bytes(value[:4], "little") % (2**32 - 1) if native else int.from_bytes(value[:8], "little")

    def rng(self, role):
        return self.np.random.Generator(self.np.random.PCG64(self.seed(role)))

    def permutation(self, case, arm, name, values, chain=-1, step=-1):
        return [int(x) for x in self.rng(self.role(case, arm, name, chain, step)).permutation(values)]

    def phase_ids(self, case, chain, step):
        return [int(x) for x in self.rng(self.role(case, "B", "phase_init", chain, step)).integers(0, 4, size=4)]

    def split_coins(self, case, chain, step):
        rng = self.rng(self.role(case, "B", "split", chain, step))
        return [int(rng.integers(0, p.denominator)) for p in split_profile()]

    def graph(self, case):
        topology = (self.nx.gnp_random_graph(16, 0.4, seed=8201601) if case == CASES[0]
                    else self.nx.random_regular_graph(4, 16, seed=8201602))
        edges = sorted((min(int(u), int(v)), max(int(u), int(v))) for u, v in topology.edges())
        weights = self.rng(self.role(case, "GEN", "weights")).integers(1, 6, size=len(edges))
        graph = [[0] * 16 for _ in range(16)]
        for (u, v), weight in zip(edges, weights):
            graph[u][v] = graph[v][u] = int(weight)
        return graph

    def seed_table(self):
        expected, seen = [], {False: set(), True: set()}
        for case in CASES:
            roles = [(self.role(case, "GEN", "weights"), False), (self.role(case, "B", "priority"), False)]
            for chain in range(3):
                roles.append((self.role(case, "B", "reset_start", chain), False))
                for step in range(16):
                    roles.extend((self.role(case, "B", name, chain, step), False)
                                 for name in ("portS", "portT", "phase_init", "split", "repair"))
                    roles.append((self.role(case, "B", "native", chain, step), True))
            roles.extend((self.role(case, mode, "control"), False) for mode in FAST + CUSTOM)
            for role, native in roles:
                seed = self.seed(role, native)
                insist(seed not in seen[native], "role-seeds", "registered seed collision")
                seen[native].add(seed)
                expected.append({"role": role, "native": native, "seed": seed})
        return expected


def control_blocks(path):
    block = []
    for row in lines(path, 12 * MAX_CONTROL_ROWS):
        if row.get("type") == "control_header" and block:
            yield block
            block = []
        block.append(row)
        insist(len(block) <= MAX_CONTROL_ROWS, "controls", "single-control record guard", category="RESOURCE")
    if block:
        yield block


def producer_limits_checked(run):
    """Runner argparse serializes timeout as float; compare its EXACT value."""
    wall = number(run["timeout_seconds"], "manifest/wall-cap")
    same(wall, 90.0, "manifest/wall-cap")
    same(run["max_output_bytes"], 4194304, "manifest/log-cap")
    same(run["resource_limits"]["cpu_seconds"], 60, "manifest/CPU-cap")
    same(run["resource_limits"]["max_threads"], 1, "manifest/thread-cap")


def verify_closure(root, binding):
    paths, records_by_path, total_raw = {}, {}, 0
    for record in binding["artifacts"]:
        name = record["name"]
        insist(name not in paths, "binding", "duplicate artifact alias", name, "PROVENANCE")
        path = project_path(root, record["path"])
        same(path.stat().st_size, integer(record["bytes"], "binding/bytes", 0), "binding/input-size")
        same(digest(path), record["sha256"], "binding/input-hash")
        paths[name] = path
        insist(record["path"] not in records_by_path, "binding", "duplicate artifact path", record["path"], "PROVENANCE")
        records_by_path[record["path"]] = record
        if name in FILES:
            same(record["path"], binding["dataset_directory"].rstrip("/") + "/" + name, "binding/dataset-path")
            total_raw += path.stat().st_size
    insist(total_raw <= RAW_BYTES, "dataset", "scientific input exceeds fixed 32MiB guard", category="RESOURCE")
    insist("producer_manifest" in paths, "binding", "producer manifest required", category="PROVENANCE")
    for relative, expected in PRIMARY_PINS.items():
        insist(relative in records_by_path, "binding", "missing frozen primary artifact", relative, "PROVENANCE")
        same(records_by_path[relative]["sha256"], expected, "binding/primary-pin")
    manifest = load_json(paths["producer_manifest"])
    same(manifest["schema_version"], 2, "manifest/version")
    producer_limits_checked(manifest["run"])
    same(manifest["repository"]["commit"], binding["producer_execution_commit"], "manifest/commit")
    source_rows = {row["path"]: row for row in manifest["input_artifacts"]}
    for row in manifest["input_artifacts"]:
        insist(row["sha256"] == row["sha256_after"], "manifest", "producer input changed", row["path"], "PROVENANCE")
        insist(row["path"] in records_by_path, "binding", "producer input not locally bound", row["path"], "PROVENANCE")
        same(records_by_path[row["path"]]["sha256"], row["sha256"], "binding/producer-input")
    source = source_rows.get("research/P82a_split_scatter_veto.py")
    spec = source_rows.get("research/P82a_execution_spec.json")
    insist(source is not None and spec is not None, "manifest", "missing frozen source/spec inputs", category="PROVENANCE")
    same(source["sha256"], PRIMARY_SOURCE_SHA, "manifest/source-hash")
    same(spec["sha256"], PRIMARY_SPEC_SHA, "manifest/spec-hash")
    frozen_spec = load_json(root / "research/P82a_execution_spec.json")
    same(set(source_rows), set(frozen_spec["execution_artifacts"]), "manifest/exact-primary-closure")
    outputs = {row["path"]: row["sha256"] for row in manifest["outputs"] if row.get("kind") == "result"}
    for name in FILES:
        if name in paths:
            relative = paths[name].relative_to(root).as_posix()
            insist(relative in outputs, "manifest", "dataset file absent from result hashes", relative, "PROVENANCE")
            same(outputs[relative], digest(paths[name]), "manifest/result-hash")
    complete = manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0
    if complete:
        insist(all(name in paths for name in FILES), "dataset", "completed producer missing a scientific result", category="PROVENANCE")
        insist(not manifest["run"].get("missing_results") and not manifest["run"].get("invalid_results"),
               "manifest", "completed producer missing/invalid results", category="PROVENANCE")
    return paths, manifest, complete


def audit_dataset(root, binding, token):
    paths, manifest, complete = verify_closure(root, binding)
    if not all(name in paths for name in FILES):
        return {"status": "INCONCLUSIVE_PRIMARY_PREFIX", "producer_status": manifest["run"]["status"],
                "available_scientific_files": [name for name in FILES if name in paths]}
    summary, failure = load_json(paths["summary.json"]), load_json(paths["failure.json"])
    same(summary["positive_accepted"], False, "summary/no-positive")
    failed = summary["status"] in ("INCONCLUSIVE_FIRST_FAILURE", "INCONCLUSIVE_RESOURCE_FAILURE")
    if failed:
        same(failure["status"], "FIRST_FAILURE", "failure/retained")
        complete = False
    elif complete:
        same(failure["status"], "NO_FAILURE", "failure/success-null")
    metadata, graph_data = load_json(paths["metadata.json"]), load_json(paths["graphs.json"])
    if "cases" not in graph_data or "provenance" not in metadata:
        insist(not complete, "dataset", "complete producer lacks graph/metadata", category="SCHEMA")
        return {"status": "INCONCLUSIVE_PRIMARY_PREFIX", "producer_status": manifest["run"]["status"],
                "detail": "graph or native setup did not complete"}
    replay = MainReplay(token)
    actual_provenance = metadata["provenance"]
    same(actual_provenance["native_threads"], 1, "metadata/native-readback")
    provenance = actual_provenance["provenance"]
    same(metadata["spec"], load_json(root / "research/P82a_execution_spec.json"), "metadata/frozen-spec")
    same(provenance["software"], metadata["spec"]["software"], "metadata/software")
    same(provenance["environment_threads"], {name: "1" for name in metadata["spec"]["thread_environment"]},
         "metadata/thread-environment")
    same(provenance["role_seeds"], replay.seed_table(), "metadata/full-role-seed-table")
    same(metadata["spec"]["root_seed"], 82026001, "metadata/root-seed")
    same(metadata["spec"]["rho"], [1, 1], "metadata/rho")
    same(metadata["spec"]["eta"], [1, 2], "metadata/eta")
    same(metadata["spec"]["phase_sweeps"], 2, "metadata/sweeps")
    for item in provenance["immutable_inputs"]:
        same(item["actual_sha256"], item["sha256"], "metadata/immutable-input")
    same([{k: x[k] for k in ("path", "sha256")} for x in provenance["immutable_inputs"]],
         metadata["spec"]["immutable_inputs"], "metadata/immutable-population")
    same({x["path"]: x["sha256"] for x in provenance["project_input_hashes"]},
         {x["path"]: x["sha256"] for x in manifest["input_artifacts"]}, "metadata/project-closure")
    for item in provenance["external_inputs"]:
        same(item["actual_sha256"], item["sha256"], "metadata/external-input")
    same([{k: x[k] for k in ("role", "path", "sha256")} for x in provenance["external_inputs"]],
         metadata["spec"]["external_artifacts"], "metadata/external-population")
    ledger_rows = list(lines(paths["paid_ledger.jsonl"], MAX_LEDGER_ROWS))
    b_cases, graphs = {}, {}
    for case, stream in zip(CASES, ("B_ER.jsonl", "B_RR.jsonl")):
        graph = graph_checked(graph_data["cases"][case], 16)
        same(graph, replay.graph(case), case + "/registered-graph-and-weights")
        graphs[case] = graph
        ledger = grant_audit(ledger_rows, case, complete)
        b_cases[case] = case_audit(case, graph, list(lines(paths[stream], MAX_B_ROWS)), ledger, replay, complete)
    controls = []
    for block in control_blocks(paths["controls.jsonl"]):
        if not record_by_type(block, "control_result"):
            insist(not complete, "controls", "missing normal control result", category="SCHEMA")
            break
        case = block[0]["case"]
        insist(case in graphs, "controls", "unknown case", category="MALFORMED")
        controls.append(control_audit(block, graphs[case], b_cases[case]["grant"], replay))
    if complete:
        same(summary["completed_B_attempts"], 96, "summary/completed")
        same(summary["requested_B_attempts"], 96, "summary/requested")
        same(summary["modeled_full_source_photons"], 768, "summary/injected")
        same(summary["modeled_completed_source_photons"], 768, "summary/completed-photons")
        status = decision_audit(summary, controls, b_cases)
        for case in CASES:
            same(summary["B_cases"][case]["all_paid_best"], b_cases[case]["all_paid_best"], "summary/B-best")
        verdict = "FINITE_RECORDED_DATA_AUDIT_PASSED"
    else:
        status, verdict = summary["status"], "INCONCLUSIVE_PRIMARY_PREFIX"
    return {"status": verdict, "primary_status": status, "producer_status": manifest["run"]["status"],
            "B_cases": b_cases, "controls": controls,
            "scope": {"compiler_before_R": "source-pin plus independent mark-only reconstruction; no separate endpoints",
                      "custom_policies": "mask/cut/work/cache/clock audit; no policy replay",
                      "factory_cpu_split": None, "Born_law_certified": False,
                      "TV_certified": False, "physical_replication": False}}


def output_pair(directory, summary, failure):
    directory.mkdir(parents=True, exist_ok=False)
    payloads = [json.dumps(row, ensure_ascii=True, sort_keys=True, allow_nan=False,
                          separators=(",", ":")).encode("ascii") + b"\n" for row in (summary, failure)]
    insist(sum(map(len, payloads)) <= OUTPUT_BYTES, "audit-output", "fixed output cap", category="RESOURCE")
    for name, payload in zip(("audit_summary.json", "audit_failure.json"), payloads):
        with (directory / name).open("xb") as stream:
            stream.write(payload)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    binding = load_json(project_path(root, args.binding))
    token = authorize_binding(binding)  # BEFORE outputs, main seeds, numerical imports or raw paths.
    same(binding["checker_source_sha256"], digest(Path(__file__)), "binding/frozen-checker-bytes")
    output = root / args.output
    insist(not Path(args.output).is_absolute() and ".." not in Path(args.output).parts,
           "output", "project-relative fresh audit output required", category="PROVENANCE")
    insist(not output.exists() and output.parent.resolve().is_relative_to(root.resolve()),
           "output", "exclusive output escaped/is occupied", category="PROVENANCE")
    cursor = root
    for part in Path(args.output).parts:
        cursor = cursor / part
        insist(not cursor.is_symlink(), "output", "output symlink forbidden", category="PROVENANCE")
    for item in binding["artifacts"]:
        if item["name"] not in FILES:
            continue
        raw_parent = (root / item["path"]).parent
        insist(not output.resolve().is_relative_to(raw_parent.resolve()), "output",
               "audit output cannot be inside a sealed input directory", category="PROVENANCE")
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
        os.environ[key] = "1"
    failure = None
    try:
        result = audit_dataset(root, binding, token)
        code = 0
    except AuditIssue as error:
        result = {"status": "AUDIT_" + error.category, "location": error.location}
        failure = {"category": error.category, "location": error.location,
                   "message": str(error), "detail_repr": repr(error.detail)[:8192]}
        code = 1
    except (KeyError, TypeError, ValueError, IndexError, OSError) as error:
        result = {"status": "AUDIT_MALFORMED_INPUT"}
        failure = {"category": "MALFORMED", "message": repr(error)[:8192]}
        code = 1
    result.update(positive_accepted=False, source_sha256=digest(Path(__file__)),
                  stochastic_native_calls=0, optimizer_replays=0,
                  claim="recorded finite protocol only; no Born/TV/physical certificate")
    output_pair(output, result, failure)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
