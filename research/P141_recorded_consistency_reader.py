"""CODE ONLY: post-seal/outcomes-known recorded consistency, by primary author.
Not independent physics/optimizer replication. No producer, matrix evaluation,
factory, RNG, permanent, native, QPU or new parameter point. ROOT authorizes
execution separately; a required CLI flag does not itself supply that authority.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from math import factorial
from pathlib import Path
import resource
import traceback

ROOT = Path("/Users/karimelhoudaigui/Desktop/pasqal")
BASE = "research/P141_finite_magnetic_main/run_001"
ORIGIN = "737321d98f3b979b29e0fb82c622f3f81662938b"
RAW = (("manifest.json", "acfb116e8f93a382aa582f2ebfd5955b891c1868bdd40037a6b5b4a3966189b7", "2081b4cccc5e410ba1c5fc0bc944ee2a57cd4c97"),
       ("stdout.txt", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"),
       ("stderr.txt", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"),
       ("data/records.jsonl", "faf9d55fd28d7b5442763e3dbcb4ed54edf4a006ec9516eb665df2541329933c", "e31de02a572b5349307ad9aad656b018211540c4"),
       ("data/summary.json", "b0244e358baf777f7a51fc5f602a8e59f5261854122fb8e93f1d1fc90432b93e", "fa0ebdeed596f760a400f6583eee1b0b9d0737e0"),
       ("data/failure.json", "38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed", "19765bd501b636fce433540d9e6735f51d66151d"))
EXPECTED = dict(provenance=1, graph_context=2, field_check=16, candidate_cost=140, generator_context=8, matrix_context=36,
                subpermanent_check=17820, gram_permanent_check=540, cf_comparison=37800, profile_totals=540,
                selected_four_cycle=140, full_pnr=1365, full_pnr_totals=1, hand_completion=2, grid_envelope=30, graph_decision=2)
KEYS = {"provenance": (), "graph_context": ("case",), "field_check": ("case", "vertex"), "candidate_cost": ("case", "Y"),
        "generator_context": ("case", "alpha", "rho"), "matrix_context": ("context",), "subpermanent_check": ("context", "source", "received"),
        "gram_permanent_check": ("context", "source"), "cf_comparison": ("context", "profile", "Y"), "profile_totals": ("context", "profile"),
        "selected_four_cycle": ("context", "Y"), "full_pnr": ("context", "occupation"), "full_pnr_totals": ("context",),
        "hand_completion": ("context",), "grid_envelope": ("case", "profile"), "graph_decision": ("case",)}
PROFILES = ("0000", "0001", "0010", "0011", "0012", "0100", "0101", "0102", "0110", "0111", "0112", "0120", "0121", "0122", "0123")


def need(value, message):
    if not value: raise ValueError(message)
def load(path): return json.loads(path.read_text(encoding="ascii"), parse_float=F)
def digest(path):
    need(path.is_file() and path.resolve() == path, "regular canonical input")
    size = path.stat().st_size; h, g = hashlib.sha256(), hashlib.sha1(b"blob "+str(size).encode()+b"\0")
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""): h.update(chunk); g.update(chunk)
    return {"sha256": h.hexdigest(), "git_blob_sha1": g.hexdigest(), "bytes": size}
def raw_hashes():
    answer = {name: digest(ROOT/BASE/name) for name, unused, other in RAW}
    for name, sha, blob in RAW: need(answer[name]["sha256"] == sha and answer[name]["git_blob_sha1"] == blob, "sealed raw bytes/blob changed")
    return answer
def number(value, signs):
    need(isinstance(value, str) and str(int(value)) == value, "canonical signed decimal numerator")
    n = int(value); signs["negative" if n < 0 else "zero" if n == 0 else "positive"] += 1; return n
def pair(value, signs):
    need(isinstance(value, list) and len(value) == 2, "Gaussian numerator pair"); return tuple(number(x, signs) for x in value)
def shape(a, n, m, signs, fractions=False):
    need(len(a) == n and all(len(row) == m for row in a), "recorded matrix shape")
    for row in a:
        for x in row:
            if fractions: need(len(x) == 2 and all(str(F(v)) == v for v in x), "own Gaussian-rational domain")
            else: pair(x, signs)
def cut(graph, vertices):
    vertices = set(vertices); return sum(w for i, j, w in graph["weighted_edges"] if (i in vertices) != (j in vertices))


def audit(report):
    before = raw_hashes(); report["raw_before"] = before
    manifest = load(ROOT/BASE/"manifest.json"); summary = load(ROOT/BASE/"data/summary.json")
    need(manifest["schema_version"] == 2 and manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0, "completed v2 run")
    need(load(ROOT/BASE/"data/failure.json") is None and summary["status"] == "EXACT_GRID_ENGINE_PASS" and not summary["FAILED_TASK"] and not summary["NOT_RUN"], "complete primary engine")
    counts, signs, seen = Counter(), Counter(), set(); graphs, scores, mats, acc, totals, bcf, qbins, envelopes, decisions, j4 = {}, {}, {}, defaultdict(lambda: [0, 0, 0]), {}, {}, defaultdict(lambda: [0, 0, 0]), {}, {}, defaultdict(int)
    pnr, pnr_seen, provenance = Counter(), set(), None; target = set(combinations(range(8), 4))
    cases = ("ER1411001", "RR1411002"); contexts = {c+"/g"+str(i) for c in cases for i in range(17)}|{"H_ID", "H_HOM"}
    with (ROOT/BASE/"data/records.jsonl").open(encoding="ascii") as stream:
        for line_number, line in enumerate(stream, 1):
            report["last_row"] = line_number; row = json.loads(line, parse_float=F); kind = row["kind"]; need(kind in EXPECTED, "registered kind")
            key = (kind,)+tuple(tuple(row[k]) if isinstance(row[k], list) else row[k] for k in KEYS[kind]); need(key not in seen, "duplicate semantic row"); seen.add(key); counts[kind] += 1
            context = row.get("context"); power = row.get("power"); d8 = mats[context]["D"]**8 if context in mats else None
            if kind == "provenance":
                provenance = row; need(line_number == 1 and tuple(row["profiles"]) == PROFILES and set(map(tuple, row["targets"])) == target and row["grid"] == [[0, "1", "0"]]+[[a, r, k] for a in (0, 1) for r in ("1", "i") for k in ("1/2", "1", "2", "4")], "literal provenance/domain")
            elif kind == "graph_context":
                graphs[row["case"]] = row; need(row["case"] in cases and len(set(row["S"])) == 12 and len(set(row["S0"])) == 8 and cut(row, row["S"]) == row["current_cost"] and cut(row, row["S0"]) == row["baseline_helper_cost"], "recorded current/helper cut")
            elif kind == "field_check":
                g = graphs[row["case"]]; need(row["delta"] == 0 and row["helper_cut"] == cut(g, g["S0"]+[row["vertex"]]) and row["edge_sum_field"]-row["delta"] == row["helper_cut"]-row["baseline_helper_cut"], "field first-minus-delta reconstruction")
            elif kind == "candidate_cost":
                g = graphs[row["case"]]; y = tuple(row["Y"]); need(y in target and set(row["lifted"]) == set(g["S0"])|{g["B_pool"][j] for j in y}, "recorded lift")
                need(row["delta"] == 0 and row["formula"]-row["delta"] == row["whole_cut"] == cut(g, row["lifted"]) and row["h"] == max(0, g["current_cost"]-row["whole_cut"]), "140 recorded costs against edges")
                scores[row["case"], y] = row["h"]
            elif kind == "generator_context":
                need(row["case"] in cases and row["alpha"] in (0, 1) and row["rho"] in ("1", "i"), "generator domain")
                for name in ("L", "H"): shape(row[name], 8, 8, signs, True)
                shape(row["source_H2"], 4, 4, signs, True); need(all(v is True for v in row["checks"].values()), "recorded generator certificate flags only")
            elif kind == "matrix_context":
                denominator = number(row["D_scale"], signs); need(0 < denominator < 2**124 and context in contexts and context not in mats and row["input"] == [8, 9, 10, 11], "common T/U scale")
                mats[context] = {"D": denominator, "case": row["case"], "alpha": row["alpha"], "rho": row["rho"], "kappa": row["kappa"]}
                if row["case"] is not None: need(context.startswith(row["case"]+"/g") and [row["alpha"], row["rho"], row["kappa"]] == provenance["grid"][int(context.split("/g")[1])], "context/grid parameters")
                for name, n, m in (("T_num", 8, 4), ("dump_num", 4, 4), ("U_num", 12, 12), ("G_num", 4, 4), ("dump_Gram_num", 4, 4)): shape(row[name], n, m, signs)
                for name, n, m in (("F_own_fractions", 8, 4), ("frame_Gram_own_fractions", 4, 4), ("Q_own_fractions", 4, 4)): shape(row[name], n, m, signs, True)
                need(all(v is True for v in row["checks"].values()), "recorded matrix flags only; not new unitarity test")
            elif kind in ("subpermanent_check", "gram_permanent_check"):
                n = len(row["source"]); need(context in mats and power == (n if kind == "subpermanent_check" else 2*n), "amplitude/Gram power")
                need(tuple(row["source"]) in set(combinations(range(4), n)) and (kind == "subpermanent_check" and tuple(row["received"]) in set(combinations(range(8), n)) or kind == "gram_permanent_check" and n > 0), "complete subset domains")
                first, delta = pair(row["num"], signs), pair(row["delta"], signs); second = tuple(a-b for a, b in zip(first, delta)); need(first == second, "DP/Ryser two-operand reconstruction")
            elif kind == "cf_comparison":
                y, profile = tuple(row["Y"]), row["profile"]; need(y in target and profile in PROFILES and power == 8, "CF domain")
                first, delta = number(row["num"], signs), number(row["delta"], signs); second = first-delta; need(first == second and first >= 0, "convolution/bucket operands")
                h = row["h"] or 0; need(row["h"] is None if mats[context]["case"] is None else h == scores[mats[context]["case"], y], "recorded utility")
                a = acc[context, profile]; a[0] += first; a[1] += h*first; a[2] += first if h > 0 else 0
                q = sum(j >= 4 for j in y); z = qbins[context, profile, q]; z[0] += first; z[1] += h*first; z[2] += first if h > 0 else 0
                if profile == "0000": bcf[context, y] = first
                if row["expected_hand_num"] is not None:
                    expected = F(int(y == (0, 1, 2, 3))) if context == "H_ID" else F(32, 81)*int(profile[0] != profile[1] and y == (0, 1, 2, 3)); need(first == number(row["expected_hand_num"], signs) == expected*d8, "hand CF")
                if context.endswith("/g0"): need(first == (d8 if y == (0, 1, 2, 3) else 0), "all-profile incumbent null")
            elif kind == "profile_totals":
                need(power == 8 and context in mats and row["profile"] in PROFILES, "totals power/profile"); values = [number(row[k], signs) for k in ("CF_num", "all_signal_num", "SIGNAL_COLLISION_num", "DUMP_num")]
                cf, signal, collision, dump = values; a = acc[context, row["profile"]]; need(min(values) >= 0 and cf+collision == signal and signal+dump == d8 and number(row["total_num"], signs) == d8 and a[0] == cf, "540 raw mass totals")
                if row["I_num"] is not None: need([number(row[k], signs) for k in ("I_num", "hazard_num")] == a[1:], "raw I/hazard sums")
                else: need(mats[context]["case"] is None and row["hazard_num"] is None and a[1:] == [0, 0], "hands-only absent utility")
                totals[context, row["profile"]] = {k: F(v, d8) for k, v in zip(("cf", "signal", "collision", "dump", "I", "hazard"), values+a[1:])}
            elif kind == "full_pnr":
                n = tuple(row["occupation"]); need(context == "ER1411001/g14" and len(n) == 12 and min(n) >= 0 and sum(n) == 4, "full-PNR domain")
                amplitude = pair(row["amplitude_num"], signs); numerator = number(row["p_num"], signs); divisor = 1
                for count in n: divisor *= factorial(count)
                need(numerator == sum(x*x for x in amplitude) and divisor == row["occupation_factorial"] and row["amplitude_power"] == 4 and row["probability_power"] == 8, "PNR square/factorial")
                label = "DUMP" if any(n[8:]) else "CF" if max(n[:8]) <= 1 else "SIGNAL_COLLISION"; need(label == row["classification"], "ANY-dump precedence")
                p = F(numerator, d8*divisor); pnr[label] += p; pnr_seen.add(n)
                if label == "CF":
                    expected, delta = number(row["expected_CF_num"], signs), number(row["CF_delta_num"], signs); need(expected == bcf[context, tuple(j for j in range(8) if n[j])] and p*d8-delta == expected and delta == 0, "PNR first-minus-delta CF operands")
                else: need(row["expected_CF_num"] is None and row["CF_delta_num"] is None, "non-CF has no favorable comparator")
            elif kind == "full_pnr_totals":
                need(power == 8 and row["bins"] == len(pnr_seen) == 1365 and sum(pnr.values()) == F(row["total"]) == 1, "complete1365 normalization")
                for label, field in (("CF", "cf"), ("SIGNAL_COLLISION", "collision"), ("DUMP", "dump")):
                    first, delta = number(row["mass_num"][label], signs), number(row["delta"][label], signs); need(F(first, d8) == pnr[label] and F(first-delta, d8) == totals[context, "0000"][field] and delta == 0, "PNR coarse reconstruction")
            elif kind == "selected_four_cycle":
                need(power == 8 and tuple(row["Y"]) in target, "C4 domain"); parts = [pair(v, signs) for v in row["six_coefficients_num"]]; total = pair(row["total_num"], signs)
                need(len(parts) == 6 and tuple(map(sum, zip(*parts))) == total and total[1] == 0 and row["h"] == scores[mats[context]["case"], tuple(row["Y"])], "signed six-cycle sum")
                value = number(row["weighted_real_num"], signs); need(value == row["h"]*total[0], "signed C4 weighting"); j4[context] += value
            elif kind == "grid_envelope": envelopes[row["case"], row["profile"]] = row
            elif kind == "graph_decision": decisions[row["case"]] = row
            elif kind == "hand_completion": need(row["passed"] is True and tuple(row["profiles"]) == PROFILES, "recorded hand completion")
    need(dict(counts) == EXPECTED == summary["counts"] and len(seen) == summary["records"] == report["last_row"] == 58443, "all kinds/counts/unique keys")
    need(len(mats) == 36 and len(totals) == 540 and len(envelopes) == 30, "complete context/profile table"); contrasts, exploratory = {}, []
    for case in ("ER1411001", "RR1411002"):
        best = {}
        for profile in PROFILES:
            values = [totals[case+"/g"+str(i), profile]["I"] for i in range(17)]; index = max(range(17), key=values.__getitem__); row = envelopes[case, profile]; context = case+"/g"+str(index)
            need(list(map(F, row["all_I"])) == values and row["grid_index"] == index and F(row["I"]) == values[index] and F(row["hazard"]) == totals[context, profile]["hazard"], "30 normalized maxima/first ties")
            need([row["alpha"], row["rho"], row["kappa"]] == provenance["grid"][index] and row["null_selected"] == (index == 0) and row["kappa_at_registered_max"] == (F(row["kappa"]) == 4), "selected grid metadata")
            best[profile] = row
        proper = max(PROFILES[1:], key=lambda p: F(best[p]["I"])); decision = decisions[case]; b = best["0000"]
        need(decision["B"] == {k: b[k] for k in decision["B"]} and decision["proper_best"] == {k: best[proper][k] for k in decision["proper_best"]} and decision["proper_profile"] == proper and F(decision["proper_envelope"]) == F(best[proper]["I"]) and decision["strict_grid"] == (F(b["I"]) > F(best[proper]["I"])), "recomputed proper-envelope decision")
        selected = case+"/g"+str(b["grid_index"]); need(selected in j4 and F(decision["selected_J4"]) == F(j4[selected], mats[selected]["D"]**8), "selected signed J4")
        need(decision["frontier_h"] == max(h for (c, y), h in scores.items() if c == case) and decision["current_R_h"] == scores[case, (0, 1, 2, 3)] == 0 and decision["optimizer_advantage"] is False, "credited frontier/current null")
        contrasts[case] = {"B": b, "D": best["0123"], "proper_profile": proper, "proper": best[proper], "B_minus_D": F(b["I"])-F(best["0123"]["I"]), "B_minus_proper": F(b["I"])-F(best[proper]["I"]), "credited_frontier_h": decision["frontier_h"], "selected_J4": F(decision["selected_J4"]), "strict_grid": decision["strict_grid"]}
        for profile in dict.fromkeys(("0000", "0123", proper)):
            context = case+"/g"+str(best[profile]["grid_index"]); exploratory.append({"case": case, "profile": profile, "context": context, "post_outcome_exploratory": True,
                "raw_totals": totals[context, profile], "q_domain": "Raw signal-CF only; collision/dump hold R, excluded from these q bins without renormalization",
                "by_q": [{"q": q, **{k: F(v, mats[context]["D"]**8) for k, v in zip(("CF", "I", "hazard"), qbins[context, profile, q])}, "h_positive_candidates": sum(h > 0 and sum(j >= 4 for j in y) == q for (c, y), h in scores.items() if c == case)} for q in range(5)]})
    need({c: d for c, d in decisions.items()} == {d["case"]: d for d in summary["decisions"]} and summary["signal_status"] == ("FOLLOWUP" if all(d["strict_grid"] for d in decisions.values()) else "NO_SIGNAL"), "summary decision consistency")
    need(summary["cost_ledger"] == dict(edge_cut_calls=160, field_checks=16, incremental_cost_calls=140, two_hop_pair_sums=56, two_hop_products=1344) and summary["optimizer_advantage"] is False and summary["positive_accepted"] is False, "recorded ledger/non-claims")
    need(len(j4) == 2 and len(summary["completed"]) == len(set(summary["completed"])) == 45 and set(summary["completed"]) == set(summary["task_plan"]) and summary["record_bytes"] == before["data/records.jsonl"]["bytes"], "C4/task/byte completion")
    need(provenance["before"] == summary["after"], "recorded project/external before-after unchanged"); inputs = manifest["input_artifacts"]; need(len(inputs) == len({r["path"] for r in inputs}) == 17, "17 manifest inputs")
    need(set(manifest["execution_artifacts"]) == {r["path"] for r in inputs} == {r["path"] for r in summary["after"]["project"]}|{provenance["binding"]}, "primary closure")
    need({r["path"]: r["sha256"] for r in manifest["outputs"]} == {BASE+"/"+n: h for n, h, b in RAW if n != "manifest.json"}, "five manifest result/log hashes")
    for r in inputs: need(r["sha256"] == r["sha256_after"] == digest(ROOT/r["path"])["sha256"], "current primary input hash")
    for group, count in (("project", 16), ("external", 11)):
        rows = summary["after"][group]; need(len(rows) == len({r["path"] for r in rows}) == count, "descriptor count")
        for r in rows:
            actual = digest(Path(r["path"]) if group == "external" else ROOT/r["path"]); need(r["expected_sha256"] == r["observed_sha256"] == actual["sha256"] and r["expected_bytes"] == r["observed_bytes"] == actual["bytes"], "current descriptor hash/size")
    binding = load(ROOT/provenance["binding"]); need(digest(ROOT/provenance["binding"])["sha256"] == provenance["binding_sha256"] and binding["source_sha256"] == provenance["source_sha256"], "binding/source linkage")
    need({r["path"] for r in binding["external_artifacts"]} == {r["path"] for r in summary["after"]["external"]} and len({r["role"] for r in binding["external_artifacts"]}) == 11, "eleven external role links")
    need(raw_hashes() == before, "raw inputs unchanged after reading")
    report.update(status="RECORDED_CONSISTENCY_PASS", primary_signal_status=summary["signal_status"], counts=dict(counts), signed_integer_components=dict(signs), normalized_contrasts=contrasts, exploratory_replacement_breakdown=exploratory, raw_after=before, manifest_inputs=inputs, external_pin_observations=summary["after"]["external"],
                  limitations="No new unitary, permanent, matrix certificate, graph draw, native point, independent physics/optimizer replication or causal inference; producer authored by this reader's author.")


def main():
    resource.setrlimit(resource.RLIMIT_CPU, (20, 20)); resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))
    p = argparse.ArgumentParser(); p.add_argument("--root-authorized-recorded-read", action="store_true", required=True); p.parse_args()
    output = ROOT/"reports/P141_validation_review/recorded_consistency.json"; need(not output.exists() and not output.is_symlink() and output.parent.is_dir() and output.parent.resolve() == output.parent, "fresh processed output")
    report = {"provenance": "POST_SEAL_OUTCOMES_KNOWN_RECORDED_CONSISTENCY_PRIMARY_AUTHOR", "raw_origin_commit": ORIGIN, "independent_physical_replication": False, "independent_optimizer_replication": False, "optimizer_advantage": False}
    try: audit(report)
    except Exception: report.update(status="RECORDED_CONSISTENCY_FAIL", traceback=traceback.format_exc())
    payload = json.dumps(report, default=str, sort_keys=True, allow_nan=False, indent=2)+"\n"; need(len(payload.encode("ascii")) <= 1048576, "1MiB processed output cap")
    with output.open("x", encoding="ascii") as stream: stream.write(payload)
    if report["status"] != "RECORDED_CONSISTENCY_PASS": raise SystemExit(1)


if __name__ == "__main__": main()
