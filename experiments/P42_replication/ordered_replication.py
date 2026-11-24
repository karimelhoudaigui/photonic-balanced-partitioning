"""P42 independent first-quantized finite check; no project or primary imports."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, permutations, product
import json
import math
import os
from pathlib import Path
import platform
import resource
import time

import numpy as np

TOL = 1e-10
MAX_ARRAY = 64 * 1024**2
MAX_OUTPUT = 32 * 1024**2


def checked(a):
    if a.nbytes > MAX_ARRAY:
        raise MemoryError("A single array exceeds64MiB")
    return a


def sha(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def complex_rows(a):
    return {"real": a.real.tolist(), "imag": a.imag.tolist()}


def histogram(word, m):
    return tuple(word.count(i) for i in range(m))


def internal_vectors(n, kind):
    if not n:
        return np.empty((0, 1), dtype=complex)
    if kind == "equal":
        return np.ones((n, 1), dtype=complex)
    if kind == "orthogonal":
        return np.eye(n, dtype=complex)
    if kind != "partial_complex" or n < 2:
        raise ValueError("Undeclared internal-state family")
    rows = np.eye(n, dtype=complex)
    for j in range(n):
        rows[j, (j + 1) % n] += (j + 1) / (n + 2) * np.exp(1j * math.pi * (j + 1) / (n + 1))
        rows[j] /= np.linalg.norm(rows[j])
    return rows


def symmetrized_source(s, internal):
    """Normalize the actual sum of N! ordered tensor-product amplitudes."""
    m, n = len(s), sum(s)
    d = internal.shape[1]
    if n == 0:
        return np.ones((), dtype=complex), 1.
    modes = [i for i, count in enumerate(s) for _ in range(count)]
    one_particle = []
    for j, mode in enumerate(modes):
        factor = np.zeros((m, d), dtype=complex)
        factor[mode] = internal[j]
        one_particle.append(factor.reshape(m * d))
    state = checked(np.zeros((m * d,) * n, dtype=complex))
    for order in permutations(range(n)):
        term = np.ones((), dtype=complex)
        for j in order:
            term = checked(np.multiply.outer(term, one_particle[j]))
        state += term
    norm_before = float(np.linalg.norm(state.reshape(-1)))
    state /= norm_before
    return state.reshape((m, d) * n), norm_before


def spatial_reduction(state, m, d, n, r):
    """Keep r spatial factors; trace EVERY internal and N-r lost factors."""
    if n == 0:
        return np.ones((1, 1), dtype=complex)
    keep = [2 * j for j in range(r)]
    environment = [j for j in range(2 * n) if j not in keep]
    amplitude = checked(np.ascontiguousarray(state.transpose(keep + environment)).reshape(m**r, -1))
    return checked(amplitude @ amplitude.conj().T)


def tensor_power(u, r):
    result = np.ones((1, 1), dtype=complex)
    for _ in range(r):
        result = checked(np.kron(result, u))
    return result


def stirling(n, k):
    table = [[0] * (k + 1) for _ in range(n + 1)]
    table[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            table[i][j] = j * table[i-1][j] + table[i-1][j-1]
    return table[n][k]


def write_json(path, value):
    with path.open("x") as out:
        json.dump(value, out, indent=2, allow_nan=False)
        out.write("\n")


def run(cases_path, output):
    started = time.monotonic()
    cpu_started = time.process_time()
    spec = json.loads(cases_path.read_text())
    if any(os.environ.get(v) != "1" for v in spec["thread_variables"]):
        raise ValueError("Runner must set every declared numerical thread variable to1")
    if not output.is_dir() or any(output.iterdir()):
        # The runner owns manifest/stdout/stderr; these can already exist.
        allowed = {"stdout.txt", "stderr.txt"}
        if not output.is_dir() or any(p.name not in allowed for p in output.iterdir()):
            raise FileExistsError("A fresh runner output directory is required")
    unitaries = {}
    for seed in spec["seeds"]:
        rng = np.random.Generator(np.random.PCG64(seed))
        for m in spec["random_unitary_dimensions"]:
            z = rng.standard_normal((m, m)) + 1j * rng.standard_normal((m, m))
            q, r = np.linalg.qr(z)
            phases = np.diag(r) / np.abs(np.diag(r))
            unitaries[(m, f"qr_{seed}")] = q * phases.conj()[None, :]
    for m in (2, 3, 4):
        unitaries[(m, "identity")] = np.eye(m, dtype=complex)
        h = np.eye(m, dtype=complex)
        h[:2, :2] = np.array([[1, 1j], [1j, 1]]) / math.sqrt(2)
        unitaries[(m, "balanced_first_two")] = h
    diagnostics = []
    errors = defaultdict(float)
    minimum_margins = {"ordered": 1., "identical": 1.}
    witness = None
    joint_max_bytes = 0
    with (output / "laws.jsonl").open("x") as raw:
        for case in spec["cases"]:
            s, kind, u_name = tuple(case["occupation"]), case["internal"], case["unitary"]
            m, n = len(s), sum(s)
            internal = internal_vectors(n, kind)
            d = internal.shape[1]
            state, source_norm = symmetrized_source(s, internal)
            joint_max_bytes = max(joint_max_bytes, state.nbytes)
            u = unitaries[(m, u_name)]
            errors["unitarity"] = max(errors["unitarity"], float(np.max(abs(u.conj().T @ u - np.eye(m)))))
            errors["source_normalization"] = max(errors["source_normalization"], abs(float(np.vdot(state, state).real) - 1))
            if n > 1:
                swapped = state.reshape((m*d,)*n).swapaxes(0, 1)
                errors["bosonic_symmetry"] = max(errors["bosonic_symmetry"], float(np.max(abs(swapped-state.reshape((m*d,)*n)))))
            modes = [i for i, count in enumerate(s) for _ in range(count)]
            sectors = []
            for r in range(n + 1):
                rho = spatial_reduction(state, m, d, n, r)
                words = list(product(range(m), repeat=r))
                occupations = [histogram(word, m) for word in words]
                groups = defaultdict(list)
                for index, t in enumerate(occupations):
                    groups[t].append(index)
                diag = np.diag(rho).real
                block_traces = {t: float(np.sum(diag[indices])) for t, indices in groups.items() if all(t[i] <= s[i] for i in range(m))}
                expected_counts = Counter(histogram(tuple(modes[j] for j in subset), m) for subset in combinations(range(n), r))
                for t, count in expected_counts.items():
                    closed_count = math.prod(math.comb(s[i], t[i]) for i in range(m))
                    if count != closed_count:
                        raise AssertionError("Indexed-loss enumeration disagrees with binomial multiplicity")
                    errors["block_trace"] = max(errors["block_trace"], abs(block_traces[t] - count/math.comb(n, r)))
                mask = np.array([[a != b for b in occupations] for a in occupations])
                errors["off_occupation_block"] = max(errors["off_occupation_block"], float(np.max(abs(rho[mask]), initial=0)))
                errors["density_trace"] = max(errors["density_trace"], abs(float(np.trace(rho).real)-1))
                errors["density_hermiticity"] = max(errors["density_hermiticity"], float(np.max(abs(rho-rho.conj().T))))
                errors["density_negative_eigenvalue"] = max(errors["density_negative_eigenvalue"], max(0., -float(np.linalg.eigvalsh(rho)[0])))
                symmetric_mass = 0.
                for indices in groups.values():
                    symmetric_mass += float(np.sum(rho[np.ix_(indices, indices)]).real) / len(indices)
                if kind == "equal":
                    errors["identical_symmetric_mass"] = max(errors["identical_symmetric_mass"], abs(symmetric_mass - 1))
                ur = tensor_power(u, r)
                transformed = checked(ur @ rho @ ur.conj().T)
                outgoing = defaultdict(float)
                for t, probability in zip(occupations, np.diag(transformed).real):
                    outgoing[t] += float(probability)
                errors["output_trace"] = max(errors["output_trace"], abs(math.fsum(outgoing.values()) - 1))
                errors["negative_probability"] = max(errors["negative_probability"], max(0., -min(outgoing.values())))
                ranks = {}
                for k in range(m + 1):
                    for support in combinations(range(m), k):
                        accepted = [j for j, word in enumerate(words) if set(word) == set(support)]
                        ordered_rank = len(accepted)
                        symmetric_rank = len({occupations[j] for j in accepted})
                        expected_ordered = math.factorial(k) * stirling(r, k)
                        expected_symmetric = (math.comb(r-1, k-1) if 1 <= k <= r else int(k == r == 0))
                        if (ordered_rank, symmetric_rank) != (expected_ordered, expected_symmetric):
                            raise AssertionError("Enumerated output rank disagrees with formula")
                        ranks[support] = (ordered_rank, symmetric_rank)
                sectors.append({"r": r, "rho_sha256": sha(rho), "rho_eigenvalues": np.linalg.eigvalsh(rho).tolist(),
                    "block_traces": block_traces, "outgoing": dict(outgoing), "ranks": ranks,
                    "symmetric_mass": symmetric_mass, "loss_subset_counts": expected_counts})
            gram = internal.conj() @ internal.T
            diagnostics.append({"case_id": case["id"], "occupation": s, "internal": kind,
                "internal_vectors": complex_rows(internal), "internal_gram": complex_rows(gram),
                "internal_dimension": d, "unitary_name": u_name, "unitary": complex_rows(u),
                "source_norm_before": source_norm, "source_sha256": sha(state), "source_array_bytes": state.nbytes,
                "sectors": [{"r": sec["r"], "density_sha256": sec["rho_sha256"],
                    "density_eigenvalues": sec["rho_eigenvalues"], "symmetric_mass": sec["symmetric_mass"],
                    "input_blocks": [{"t": t, "trace_conditional": mass, "loss_subset_count": sec["loss_subset_counts"][t]} for t, mass in sorted(sec["block_traces"].items())]} for sec in sectors]})
            for eta in spec["etas"]:
                survivor_weights = Counter()
                for keep in product((0, 1), repeat=n):
                    survivor_weights[sum(keep)] += math.prod(eta if flag else 1-eta for flag in keep)
                full_law = defaultdict(float)
                for sec in sectors:
                    r = sec["r"]
                    errors["sector_binomial"] = max(errors["sector_binomial"], abs(survivor_weights[r] - math.comb(n, r)*eta**r*(1-eta)**(n-r)))
                    for t, probability in sec["outgoing"].items():
                        full_law[t] += survivor_weights[r] * probability
                errors["loss_law_normalization"] = max(errors["loss_law_normalization"], abs(math.fsum(full_law.values()) - 1))
                errors["all_photons_detected"] = max(errors["all_photons_detected"], abs(math.fsum(p for t, p in full_law.items() if sum(t) == n) - eta**n))
                support_rows = []
                for k in range(m + 1):
                    for support in combinations(range(m), k):
                        for encoding in ("threshold", "pnr_exact_k"):
                            probability = math.fsum(p for t, p in full_law.items() if tuple(i for i, count in enumerate(t) if count) == support and (encoding == "threshold" or sum(t) == k))
                            caps = {"ordered": 0., "identical": 0.}
                            for sec in sectors:
                                if encoding == "pnr_exact_k" and sec["r"] != k:
                                    continue
                                masses = sorted(sec["block_traces"].values(), reverse=True)
                                ordered_rank, symmetric_rank = sec["ranks"][support]
                                caps["ordered"] += survivor_weights[sec["r"]] * math.fsum(masses[:ordered_rank])
                                caps["identical"] += survivor_weights[sec["r"]] * math.fsum(masses[:symmetric_rank])
                            margin = caps["ordered"] - probability
                            minimum_margins["ordered"] = min(minimum_margins["ordered"], margin)
                            if kind == "equal":
                                minimum_margins["identical"] = min(minimum_margins["identical"], caps["identical"] - probability)
                            support_rows.append({"support": support, "encoding": encoding, "probability": probability,
                                "ordered_block_trace_cap": caps["ordered"],
                                "identical_block_trace_cap": caps["identical"] if kind == "equal" else None})
                if n == 2 and s == (1, 1) and u_name == "balanced_first_two":
                    cf = full_law[(1, 1)]
                    expected = eta**2 * (1-abs(gram[0, 1])**2)/2
                    errors["hom_overlap"] = max(errors["hom_overlap"], abs(cf-expected))
                if s == (4, 0, 0, 0) and u_name == "balanced_first_two" and kind == "equal" and eta == .1:
                    actual = math.fsum(p for t, p in full_law.items() if t[0] and t[1] and not t[2] and not t[3])
                    prediction = 1-2*(1-eta/2)**4+(1-eta)**4
                    errors["bunched_witness_formula"] = abs(actual-prediction)
                    witness = {"case_id": case["id"], "eta": eta, "two_click_probability": actual,
                        "prediction": prediction, "invalid_distinct_input_cap": .01,
                        "distinct_input_scope_refuted": actual > .01 + TOL}
                raw.write(json.dumps({"case_id": case["id"], "eta": eta, "occupation": s,
                    "internal": kind, "law": [{"occupation": t, "probability": p} for t, p in sorted(full_law.items())],
                    "support_checks": support_rows}, allow_nan=False) + "\n")
    write_json(output / "states_and_sectors.json", diagnostics)
    passed = all(e < TOL for e in errors.values()) and all(margin >= -TOL for margin in minimum_margins.values()) and witness is not None and witness["distinct_input_scope_refuted"]
    report = {"result": "FINITE_CHECK_PASS" if passed else "FINITE_CHECK_FAIL", "case_count": len(diagnostics),
        "eta_count": len(spec["etas"]), "full_law_count": len(diagnostics)*len(spec["etas"]),
        "maximum_errors": dict(errors), "minimum_cap_margins": minimum_margins,
        "bunched_scope_falsifier": witness, "tolerance": TOL, "largest_joint_source_array_bytes": joint_max_bytes,
        "cpu_seconds_child": time.process_time()-cpu_started, "wall_seconds_child": time.monotonic()-started,
        "max_rss_platform_units": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "software": {"python": platform.python_version(), "numpy": np.__version__},
        "numerical_semantics": "FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED", "primary_code_or_raw_read": False,
        "non_claims": ["Not a universal proof", "No advantage or hardware inference", "No novelty claim", "No general validation of partial-distinguishability shortcuts"]}
    write_json(output / "summary.json", report)
    if sum(p.stat().st_size for p in output.iterdir() if p.is_file()) > MAX_OUTPUT:
        raise RuntimeError("Output exceeds32MiB")
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.cases, args.output))
