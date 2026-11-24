"""P44 independent pure-state dilation check; imports only NumPy and stdlib."""
from __future__ import annotations

import argparse
from collections import defaultdict
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
ARRAY_CAP = 64 * 1024**2
OUTPUT_CAP = 32 * 1024**2
LARGEST_ARRAY = 0


def bounded(a):
    global LARGEST_ARRAY
    LARGEST_ARRAY = max(LARGEST_ARRAY, a.nbytes)
    if a.nbytes > ARRAY_CAP:
        raise MemoryError("Individual array exceeds64MiB")
    return a


def digest(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def encode(a):
    return {"real": a.real.tolist(), "imag": a.imag.tolist()}


def hist(word, m):
    return tuple(word.count(j) for j in range(m))


def permanent(a):
    if a.shape[0] != a.shape[1]:
        raise ValueError("Permanent requires square input")
    return sum((math.prod(a[j, p[j]] for j in range(len(p))) for p in permutations(range(a.shape[0]))), 0j)


def make_internal(n, kind):
    if kind == "equal":
        vectors = np.ones((n, 1), dtype=complex)
    elif kind == "orthogonal":
        vectors = np.eye(n, dtype=complex)
    elif kind == "partial_complex":
        vectors = np.eye(n, dtype=complex)
        for j in range(n):
            vectors[j, (j+1) % n] += (j+2)/(n+4) * np.exp(1j*math.pi*(j+1)/(n+2))
            vectors[j] /= np.linalg.norm(vectors[j])
    elif kind == "singlet":
        if n != 2:
            raise ValueError("Singlet requires two source modes")
        phi = np.zeros((2, 2), dtype=complex)
        phi[0, 1], phi[1, 0] = 1/math.sqrt(2), -1/math.sqrt(2)
        return phi, None
    elif kind == "cyclic_entangled":
        if n != 3:
            raise ValueError("Cyclic entangled fixture requires N3")
        phi = np.zeros((3, 3, 3), dtype=complex)
        phi[0, 1, 2] = 1/math.sqrt(3)
        phi[1, 2, 0] = 1j/math.sqrt(3)
        phi[2, 0, 1] = np.exp(1j*math.pi/5)/math.sqrt(3)
        return phi, None
    else:
        raise ValueError("Unknown declared internal state")
    phi = np.ones((), dtype=complex)
    for vector in vectors:
        phi = np.multiply.outer(phi, vector)
    return phi, vectors


def source_state(m, occupied, phi):
    n = len(occupied)
    d = phi.shape[0] if n else 1
    q = 2*m*d
    base = bounded(np.zeros((q,)*n, dtype=complex))
    for internal in product(range(d), repeat=n):
        base[tuple(occupied[j]*d+internal[j] for j in range(n))] = phi[internal]
    state = bounded(np.zeros_like(base))
    for order in permutations(range(n)):
        state += base.transpose(order)
    norm_before = float(np.linalg.norm(state.reshape(-1)))
    state /= norm_before
    return state, d, norm_before


def evolve(state, dilation, d, n):
    gate = bounded(np.kron(dilation, np.eye(d)))
    out = state
    for axis in range(n):
        out = bounded(np.moveaxis(np.tensordot(gate, out, axes=(1, axis)), 0, axis))
    return out


def trace_internal(state, spatial_modes, d, n):
    if not n:
        return np.ones((1, 1), dtype=complex)
    tensor = state.reshape((spatial_modes, d)*n)
    axes = list(range(0, 2*n, 2)) + list(range(1, 2*n, 2))
    amplitude = bounded(np.ascontiguousarray(tensor.transpose(axes)).reshape(spatial_modes**n, d**n))
    return bounded(amplitude @ amplitude.conj().T)


def qr_unitary(rng, m):
    z = rng.standard_normal((m, m)) + 1j*rng.standard_normal((m, m))
    q, r = np.linalg.qr(z)
    return q * (np.diag(r)/abs(np.diag(r))).conj()[None, :]


def repeated_counts(n, k):
    return sorted({hist(word, n) for word in product(range(n), repeat=k)})


def gram_moment(b, gram):
    k, n = b.shape
    total = 0j
    for chosen in combinations(range(n), k):
        for left in permutations(chosen):
            c_left = math.prod(b[j, left[j]] for j in range(k))
            for right in permutations(chosen):
                c_right = math.prod(b[j, right[j]] for j in range(k))
                total += c_left*c_right.conjugate()*math.prod(gram[right[j], left[j]] for j in range(k))
    return total


def write_json(path, obj):
    with path.open("x") as out:
        json.dump(obj, out, indent=2, allow_nan=False)
        out.write("\n")


def run(cases_path, outdir):
    start, cpu = time.monotonic(), time.process_time()
    spec = json.loads(cases_path.read_text())
    if any(os.environ.get(v) != "1" for v in spec["thread_variables"]):
        raise ValueError("All declared numerical thread variables must equal1")
    if not outdir.is_dir() or any(p.name not in {"stdout.txt", "stderr.txt"} for p in outdir.iterdir()):
        raise FileExistsError("Fresh runner output required")
    mixers = {}
    for seed in spec["seeds"]:
        rng = np.random.Generator(np.random.PCG64(seed))
        for m in spec["dimensions"]:
            mixers[(seed, m)] = qr_unitary(rng, m), qr_unitary(rng, m)
    errors, excesses = defaultdict(float), defaultdict(float)
    opaque_thermal_excess = -math.inf
    seen = []
    with (outdir/"full_laws.jsonl").open("x") as raw:
        for case in spec["cases"]:
            m, occupied = case["m"], case["occupied_inputs"]
            n, kind = len(occupied), case["internal"]
            if len(set(occupied)) != n or not 0 <= n <= m <= 3:
                raise ValueError("Frozen input is not a valid small CF source")
            left, right = mixers[(case["seed"], m)]
            profile = np.array(case["intensity_singular_values"], dtype=float)
            dmat, emat = np.diag(np.sqrt(profile)), np.diag(np.sqrt(1-profile))
            t = left @ dmat @ right.conj().T
            dilation = np.block([[t, -left @ emat], [emat @ right.conj().T, dmat]])
            errors["dilation_unitarity"] = max(errors["dilation_unitarity"], float(np.max(abs(dilation.conj().T@dilation-np.eye(2*m)))))
            eta_global = float(np.linalg.norm(t, ord=2)**2)
            t_occ = t[:, occupied]
            eta_occ = float(np.linalg.norm(t_occ, ord=2)**2) if n else 0.
            errors["singular_profile"] = max(errors["singular_profile"], abs(eta_global-float(max(profile))))
            phi, vectors = make_internal(n, kind)
            internal_purities = []
            for factor in range(n):
                matrix = np.moveaxis(phi, factor, 0).reshape(phi.shape[factor], -1)
                reduced = matrix @ matrix.conj().T
                purity = float(np.trace(reduced @ reduced).real)
                internal_purities.append(purity)
                expected = .5 if kind == "singlet" else (1/3 if kind == "cyclic_entangled" else 1.)
                errors["internal_single_factor_purity"] = max(errors["internal_single_factor_purity"], abs(purity-expected))
            source, d, norm_before = source_state(m, occupied, phi)
            errors["internal_normalization"] = max(errors["internal_normalization"], abs(float(np.vdot(phi, phi).real)-1))
            errors["source_normalization"] = max(errors["source_normalization"], abs(float(np.vdot(source, source).real)-1))
            errors["cf_symmetrization_norm"] = max(errors["cf_symmetrization_norm"], abs(norm_before**2-math.factorial(n)))
            output = evolve(source, dilation, d, n)
            errors["output_pure_norm"] = max(errors["output_pure_norm"], abs(float(np.vdot(output, output).real)-1))
            for j in range(n-1):
                errors["bosonic_symmetry"] = max(errors["bosonic_symmetry"], float(np.max(abs(output-output.swapaxes(j, j+1)))))
            rho = trace_internal(output, 2*m, d, n)
            errors["density_trace"] = max(errors["density_trace"], abs(float(np.trace(rho).real)-1))
            errors["density_hermiticity"] = max(errors["density_hermiticity"], float(np.max(abs(rho-rho.conj().T))))
            errors["density_negative_eigenvalue"] = max(errors["density_negative_eigenvalue"], max(0., -float(np.linalg.eigvalsh(rho)[0])))
            joint, system = defaultdict(float), defaultdict(float)
            for word, probability in zip(product(range(2*m), repeat=n), np.diag(rho).real):
                joint[hist(word, 2*m)] += float(probability)
            for occupation, probability in joint.items():
                if sum(occupation) != n:
                    raise AssertionError("Global photon number changed under unitary dilation")
                system[occupation[:m]] += probability
            sectors = [math.fsum(p for occ, p in system.items() if sum(occ) == r) for r in range(n+1)]
            errors["joint_law_normalization"] = max(errors["joint_law_normalization"], abs(math.fsum(joint.values())-1))
            errors["system_law_normalization"] = max(errors["system_law_normalization"], abs(math.fsum(system.values())-1))
            errors["detected_mean"] = max(errors["detected_mean"], abs(math.fsum(sum(occ)*p for occ,p in system.items())-float(np.trace(t_occ.conj().T@t_occ).real)))
            if np.max(profile)-np.min(profile) == 0:
                eta = float(profile[0])
                errors["uniform_control_sectors"] = max(errors["uniform_control_sectors"], max(abs(sectors[r]-math.comb(n,r)*eta**r*(1-eta)**(n-r)) for r in range(n+1)))
            gram = vectors.conj()@vectors.T if vectors is not None else None
            if gram is not None:
                predicted_no_loss = permanent((t_occ.conj().T@t_occ)*gram)
                errors["all_detected_product_internal"] = max(errors["all_detected_product_internal"], abs(sectors[n]-predicted_no_loss))
            if kind == "singlet":
                errors["all_detected_singlet"] = max(errors["all_detected_singlet"], abs(sectors[n]-np.linalg.det(t_occ.conj().T@t_occ)))
            checks = []
            for k in range(m+1):
                for support in combinations(range(m), k):
                    b = t_occ[list(support), :]
                    g = b@b.conj().T
                    thermal = permanent(g)
                    repeated = 0.
                    for counts in repeated_counts(n, k):
                        columns = [a for a,count in enumerate(counts) for _ in range(count)]
                        repeated += abs(permanent(b[:,columns]))**2/math.prod(math.factorial(count) for count in counts)
                    errors["permanent_cb_repeated"] = max(errors["permanent_cb_repeated"], abs(thermal-repeated))
                    errors["thermal_imaginary"] = max(errors["thermal_imaginary"], abs(thermal.imag))
                    moment = math.fsum(math.prod(occ[i] for i in support)*p for occ,p in system.items())
                    all_click = math.fsum(p for occ,p in system.items() if all(occ[i]>0 for i in support))
                    exact = math.fsum(p for occ,p in system.items() if tuple(i for i,v in enumerate(occ) if v) == support)
                    decoded = math.fsum(p for occ,p in system.items() if tuple(i for i,v in enumerate(occ) if v)[:k] == support and sum(v>0 for v in occ)>=k)
                    distinct_b = math.fsum(abs(permanent(b[:,chosen]))**2 for chosen in combinations(range(n),k))
                    classical = math.fsum(math.prod(abs(b[j,assignment[j]])**2 for j in range(k)) for assignment in permutations(range(n),k))
                    row_product = math.prod(float(np.sum(abs(b[j])**2)) for j in range(k))
                    cap = eta_occ**k if k else 1.
                    robust_route = math.factorial(k)*classical
                    excesses["event_vs_moment"] = max(excesses["event_vs_moment"], all_click-moment, exact-all_click, decoded-all_click)
                    excesses["thermal_vs_spectral"] = max(excesses["thermal_vs_spectral"], thermal.real-cap)
                    excesses["robust_routing"] = max(excesses["robust_routing"], moment-robust_route)
                    excesses["robust_spectral"] = max(excesses["robust_spectral"], moment-math.factorial(k)*cap)
                    excesses["classical_row_envelope"] = max(excesses["classical_row_envelope"], classical-row_product, row_product-cap)
                    if kind == "equal":
                        errors["identical_moment_identity"] = max(errors["identical_moment_identity"], abs(moment-distinct_b))
                        excesses["identical_thermal"] = max(excesses["identical_thermal"], moment-thermal.real)
                        excesses["identical_spectral"] = max(excesses["identical_spectral"], moment-cap)
                    else:
                        opaque_thermal_excess = max(opaque_thermal_excess, moment-thermal.real)
                    if gram is not None:
                        errors["product_gram_moment"] = max(errors["product_gram_moment"], abs(moment-gram_moment(b,gram)))
                    if kind == "orthogonal":
                        errors["distinguishable_moment"] = max(errors["distinguishable_moment"], abs(moment-classical))
                    if kind == "singlet" and k == 2:
                        errors["singlet_determinant"] = max(errors["singlet_determinant"], abs(moment-abs(np.linalg.det(b))**2))
                    checks.append({"support":support,"moment":moment,"all_click_probability":all_click,
                        "exact_support_probability":exact,"first_k_click_decoder_probability":decoded,
                        "eta_occupied_power_cap":cap,"permanental_envelope":thermal.real,
                        "repeated_column_sum":repeated,"distinct_column_bosonic_sum":distinct_b,
                        "distinguishable_injection_sum":classical,"routing_cauchy_cap":robust_route,
                        "row_product":row_product,"robust_spectral_cap":math.factorial(k)*cap})
            if kind == "singlet":
                errors["singlet_collision_probability"] = max(errors["singlet_collision_probability"], abs(math.fsum(p for occ,p in joint.items() if max(occ)>=2)))
            record={"case":case,"internal_dimension":d,"internal_tensor":encode(phi),
                "internal_single_factor_purities":internal_purities,
                "product_internal_gram":encode(gram) if gram is not None else None,
                "T":encode(t),"dilation":encode(dilation),"eta_global":eta_global,"eta_occupied":eta_occ,
                "input_mean_survival":float(np.trace(t_occ.conj().T@t_occ).real)/n if n else None,
                "source_sha256":digest(source),"output_tensor_sha256":digest(output),"spatial_density_sha256":digest(rho),
                "joint_system_environment_law":[{"occupation":occ,"probability":p} for occ,p in sorted(joint.items())],
                "system_law":[{"occupation":occ,"probability":p} for occ,p in sorted(system.items())],
                "detected_sector_weights":sectors,"support_checks":checks}
            raw.write(json.dumps(record,allow_nan=False)+"\n");raw.flush()
            seen.append(case["id"])
    passed=all(v<TOL for v in errors.values()) and all(v<TOL for v in excesses.values()) and len(seen)==len(spec["cases"])
    summary={"result":"FINITE_CHECK_PASS" if passed else "FINITE_CHECK_FAIL","cases":len(seen),"case_ids":seen,
        "maximum_errors":dict(errors),"maximum_positive_bound_excesses":dict(excesses),
        "opaque_thermal_excess_observed_not_a_required_bound":opaque_thermal_excess,
        "tolerance":TOL,"largest_array_bytes":LARGEST_ARRAY,"cpu_seconds_child":time.process_time()-cpu,
        "wall_seconds_child":time.monotonic()-start,"max_rss_platform_units":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "software":{"python":platform.python_version(),"numpy":np.__version__},
        "numerical_semantics":"FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED","primary_code_or_raw_read":False,
        "non_claims":["No universal proof from finite data","No thermal sampling algorithm used","No hardware, optimization or novelty inference"]}
    write_json(outdir/"summary.json",summary)
    if sum(p.stat().st_size for p in outdir.iterdir() if p.is_file())>OUTPUT_CAP:
        raise RuntimeError("Outputs exceed32MiB")
    print(json.dumps(summary,indent=2,allow_nan=False))
    return 0 if passed else 1


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    raise SystemExit(run(args.cases,args.output))
