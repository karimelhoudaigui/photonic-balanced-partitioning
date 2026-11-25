"""Post-run author consistency check; no physics/model sampling or numpy imports.

The first recorded check used the equivalent standard-library heredoc in the
execution session. This file preserves its checks for later reproduction.
Use a fresh --output; this is not independent physical replication.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--run", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
s = json.loads((args.run/"data/summary.json").read_text())
selection = json.loads((args.run/"data/selection.json").read_text())
contexts = s["contexts"]
groups, common, maps = collections.defaultdict(list), collections.defaultdict(list), {}
collisions, count = collections.Counter(), 0


def decode(n, order):
    pos, out = 0, []
    for j, c in enumerate(n):
        assert isinstance(c, int) and c >= 0
        out.extend(order[pos:pos+c])
        pos += c+(j < len(n)-1)
    assert pos == len(order)
    return sorted(out)


for line in (args.run/"data/raw.jsonl").read_text().splitlines():
    r = json.loads(line)
    count += 1
    case = r["case"]
    c = contexts[case]
    a = c["adjacency"]
    nv, k = len(a), len(a)//2
    if r["stage"] == "relabel_map":
        maps[case, r["probe"]] = r
        continue
    subset, order = r["subset"], c["order"]
    original = subset
    if r["stage"] == "fresh_dev":
        transform = maps[case, r["probe"]]
        order = transform["order"]
        original = sorted(transform["permutation_new_to_original"][v] for v in subset)
    assert len(subset) == k and len(set(subset)) == k and all(0 <= v < nv for v in subset)
    if "occupation" in r:
        assert sum(r["occupation"]) == k and len(r["occupation"]) == k+1
        assert decode(r["occupation"], order) == subset
        if r.get("model") == "bosonic":
            collisions[r["stage"]] += int(max(r["occupation"]) > 1)
    chosen = set(original)
    value = sum(a[i][j] for i in chosen for j in range(nv) if j not in chosen)
    assert value == r["cut"]
    if r["stage"].startswith("common_"):
        common[case].append(value)
    else:
        groups[case, r["model"]].append(r)
        if "gain_below_common_front" in r:
            assert r["gain_below_common_front"] == max(0, c["front_cut"]-value)
for case, c in contexts.items():
    assert len(common[case]) == 4+(len(c["adjacency"])//2)**2
    assert min(common[case]) == c["front_cut"]
for (case, model), records in groups.items():
    assert len(records) == 200
    best = min([contexts[case]["front_cut"]]+[r["cut"] for r in records])
    assert best == s["best_all_stages_including_common_front"][case][model]
for model, index in selection["selected_theta_independently"].items():
    gains, means = [], []
    for j in range(6):
        gain = mean = 0.
        for case, c in contexts.items():
            rr = [r for r in groups[case, model] if r["stage"] == "development" and r["theta_index"] == j]
            assert len(rr) == 12
            gain += sum(r["gain_below_common_front"] for r in rr)/12/max(1, c["front_cut"])
            mean += sum(r["cut"] for r in rr)/12/max(1, c["front_cut"])
        gains.append(gain)
        means.append(mean)
    assert index == min(range(6), key=lambda j:(-gains[j], means[j], j))
    assert max(abs(x-y) for x, y in zip(gains, selection["sum_normalized_mean_gains"][model])) < 1e-12
out = {"scope":"author standard-library raw consistency check; not independent physical replication",
       "raw_records":count, "scored_records":count-len(maps), "case_model_groups":len(groups),
       "each_group_new_scores":200, "bosonic_draws":sum(len(v) for (c,m),v in groups.items() if m=="bosonic"),
       "bosonic_collisions_by_stage":dict(collisions),
       "all_decoders_costs_fronts_counts_and_selections_match":True,
       "raw_sha256":hashlib.sha256((args.run/"data/raw.jsonl").read_bytes()).hexdigest(),
       "selected":s["selected"]}
with args.output.open("x") as f:
    json.dump(out, f, indent=2)
    f.write("\n")
print(json.dumps(out, sort_keys=True))
