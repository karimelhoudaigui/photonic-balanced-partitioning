"""CODE-ONLY P64 deterministic N18 point probabilities versus local Naive.

Fourteen prospective points, no random draw/graph/optimizer/QPU. The F6
cross-check is independent of production imports and precedes their loading.
Native18 construction occurs only in explicitly authorized main, never tests.
"""
from __future__ import annotations

import argparse
import cmath
from fractions import Fraction
import hashlib
import importlib.metadata
import inspect
import json
import math
import os
from pathlib import Path
import time

import P64_independent_F6_pair_source as independent_source

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_SOURCE_TABLE = "research/P64_qualification/run_001/data/source_table.json"
PRIMARY_SOURCE_SHA256 = "e02157b2990fa1eadef2d27cefe4f4817f6ff92a205ff67763d2365728492a75"
PRIMARY_MANIFEST = "research/P64_qualification/run_001/manifest.json"
PRIMARY_MANIFEST_SHA256 = "28e0bbcfcead8f1d84aa5a79b494464c246ab3b6f851e386777953c4b8a5fe01"
P64_SOURCE_SHA256 = "af2b016b9ce5dd71919a8745d21c7e7f363a1588a089f697770a29d5b9353543"
ABSOLUTE_TOLERANCE, RELATIVE_TOLERANCE, MATRIX_TOLERANCE = 1e-12, 1e-7, 5e-12
THREAD_VARIABLES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")


class RetainedFailure(RuntimeError):
    def __init__(self, message, evidence=None):
        super().__init__(message)
        self.evidence = {} if evidence is None else evidence


def occupations_frozen():
    z = (0, 0, 0)
    patterns = (
        ("all18_port0", ((18, 0, 0), z, z, z, z, z)),
        ("CF_forbidden", ((1, 1, 1),)*6),
        ("M666000", ((2, 2, 2), (2, 2, 2), (2, 2, 2), z, z, z)),
        ("M444222_left_rotations", ((2, 1, 1), (1, 1, 2), (1, 2, 1),
                                     (1, 1, 0), (1, 0, 1), (0, 1, 1))),
        ("M822222_left_cycle", ((3, 3, 2), (1, 1, 0), (1, 0, 1),
                                (0, 1, 1), (1, 1, 0), (1, 0, 1))),
        ("M660006", ((2, 2, 2), (2, 2, 2), z, z, z, (2, 2, 2))),
        ("all18_port12_flat_anchor", ((0, 0, 18), z, z, z, z, z)),
    )
    return [{"id": label, "triples": [list(x) for x in triples],
             "counts": [triples[i][a] for a in range(3) for i in range(6)]}
            for label, triples in patterns]


def expected_spec():
    zero = [["0"]*6 for _ in range(3)]
    phases = [["0"]*6,
              ["0", "1/11", "2/11", "3/11", "4/11", "5/11"],
              ["0", "6/11", "7/11", "8/11", "9/11", "10/11"]]
    return {"phase": "P64_NAIVE18_FIXED_POINT_CHECK", "N": 18, "d": 6,
            "phase_arrays": [{"id": "theta_zero", "exact": zero}, {"id": "theta_ten_rationals", "exact": phases}],
            "occupations": occupations_frozen(), "point_order": "phase_major_then_occupation_order",
            "rotation_convention": "LEFT; after(3,3,2), colors1..5 use (i-1)%3 on(1,1,0)",
            "points": 14, "source": [1]*18, "output_port_order": "a*6+i",
            "absolute_tolerance": ABSOLUTE_TOLERANCE, "relative_tolerance": RELATIVE_TOLERANCE,
            "comparison": "abs_error<=absolute_tolerance+relative_tolerance*max(p64,pNaive)",
            "matrix_tolerance": MATRIX_TOLERANCE, "guard_mass_tolerance": 2e-10,
            "independent_F6_products": 1728, "primary_source_table": PRIMARY_SOURCE_TABLE,
            "primary_source_sha256": PRIMARY_SOURCE_SHA256, "primary_manifest": PRIMARY_MANIFEST,
            "primary_manifest_sha256": PRIMARY_MANIFEST_SHA256, "P64_source_sha256": P64_SOURCE_SHA256,
            "flat_anchor_probability": "18!/18^18", "native_random_draws": 0,
            "graphs": 0, "optimum_used": False, "maximum_cpu_seconds": 60,
            "maximum_wall_seconds": 90, "maximum_threads": 1,
            "maximum_log_bytes": 33554432, "maximum_scientific_output_bytes": 33554432,
            "planned_logical_workspace_bytes": 268435456, "failed_retries": 0}


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_safe(value):
    """Tag invalid nonfinite evidence; never alter computational probabilities."""
    if isinstance(value, float) and not math.isfinite(value):
        return {"nonfinite_binary64": repr(value)}
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_safe(item) for item in value]
    return value


def save_json(path, value):
    with Path(path).open("x", encoding="utf8") as stream:
        json.dump(json_safe(value), stream, allow_nan=False, indent=2)
        stream.write("\n")


def emit(stream, value):
    stream.write(json.dumps(json_safe(value), allow_nan=False)+"\n")
    stream.flush()


def timed(call):
    wall, cpu = time.perf_counter(), time.process_time()
    result = call()
    return result, {"wall_seconds": time.perf_counter()-wall, "cpu_seconds": time.process_time()-cpu}


def matrix_record(matrix):
    return {"real": [[z.real for z in row] for row in matrix],
            "imag": [[z.imag for z in row] for row in matrix]}


def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def dense_reference_matrix(theta):
    """Independent full dense factorization, no P64 coefficient/cache helper."""
    source = [[0j]*18 for _ in range(18)]
    mix = [[0j]*18 for _ in range(18)]
    phases = [[0j]*18 for _ in range(18)]
    final = [[complex(i == j) for j in range(18)] for i in range(18)]
    for b in range(3):
        for i in range(6):
            phases[6*b+i][6*b+i] = cmath.exp(1j*theta[b][i])
            for j in range(6):
                source[6*b+i][6*b+j] = cmath.exp(2j*math.pi*i*j/6)/math.sqrt(6)
    for a in range(3):
        for b in range(3):
            for i in range(6):
                mix[6*a+i][6*b+i] = cmath.exp(2j*math.pi*a*b/3)/math.sqrt(3)
    final[0][0], final[0][6] = 3/5, -4/5
    final[6][0], final[6][6] = 4/5, 3/5
    return matmul(final, matmul(mix, matmul(phases, source)))


def scalar_architecture_matrix(theta):
    """Separate scalar entry formula used only for architecture diagnostics."""
    result = [[cmath.exp(2j*math.pi*(a*b/3+i*j/6)+1j*theta[b][i])/math.sqrt(18)
               for b in range(3) for j in range(6)] for a in range(3) for i in range(6)]
    first, second = result[0][:], result[6][:]
    result[0] = [(3*x-4*y)/5 for x, y in zip(first, second)]
    result[6] = [(4*x+3*y)/5 for x, y in zip(first, second)]
    return result


def matrix_diagnostics(dense, scalar):
    def adjoint(matrix):
        return [[matrix[j][i].conjugate() for j in range(18)] for i in range(18)]
    def gram_defect(matrix):
        gram = matmul(adjoint(matrix), matrix)
        return max(abs(gram[i][j]-int(i == j)) for i in range(18) for j in range(18))
    q = [[1/18]*18 for _ in range(18)]
    q[0], q[6] = [1/450]*6+[37/450]*12, [49/450]*6+[13/450]*12
    result = {"between_matrices_max": max(abs(dense[i][j]-scalar[i][j]) for i in range(18) for j in range(18)),
              "dense_column_gram_max": gram_defect(dense), "scalar_column_gram_max": gram_defect(scalar),
              "dense_row_gram_max": gram_defect(adjoint(dense)), "scalar_row_gram_max": gram_defect(adjoint(scalar)),
              "qfixed_max": max(abs(abs(matrix[i][j])**2-q[i][j]) for matrix in (dense, scalar)
                                for i in range(18) for j in range(18))}
    return result


def validate_counts(counts, d):
    if len(counts) != 3*d or any(type(n) is not int or n < 0 for n in counts) or sum(counts) != 3*d:
        raise ValueError("Complete exact nonnegative count vector of3d photons required")
    return tuple(counts)


def exact_color_mass(source, totals):
    """Integer/Fraction reachability check before any conditional division."""
    numerator = 0
    for first in source.support:
        for second in source.support:
            third = source.lookup.get(tuple(m-a-b for m, a, b in zip(totals, first.occupation, second.occupation)))
            if third is not None:
                numerator += first.weight*second.weight*third.weight
    return Fraction(numerator, source.denominator**3)


def structured_probability(sampler, theta, counts):
    counts = validate_counts(counts, sampler.d)
    totals = tuple(sum(counts[a*sampler.d+i] for a in range(3)) for i in range(sampler.d))
    exact_mass = exact_color_mass(sampler.source, totals)
    receipt = {"color_totals": totals, "exact_color_mass": str(exact_mass), "path": [],
               "zero_is_exact_color_mass": exact_mass == 0}
    if exact_mass == 0:
        return 0.0, receipt  # No conditional_state/project call and no division.
    state, returned_mass = sampler.conditional_state(totals, theta)
    if returned_mass != exact_mass:
        raise RetainedFailure("P64 exact M law disagrees with wrapper", receipt)
    conditional_probability = 1.0
    for color in range(sampler.d):
        outputs, probabilities, suffixes, groups = sampler.local_distribution(state, color)
        raw_mass = math.fsum(probabilities)
        if not math.isfinite(raw_mass) or abs(raw_mass-1) > 2e-10:
            raise RetainedFailure("Conditional mass guard", {**receipt, "raw_mass": raw_mass})
        target = tuple(counts[a*sampler.d+color] for a in range(3))
        selected = outputs.index(target)
        weight = probabilities[selected]
        normalized = weight/raw_mass
        receipt["path"].append({"color": color, "target": target, "width": len(state),
                                "raw_mass": raw_mass, "raw_selected_mass": weight, "normalized_selected_mass": normalized})
        if weight == 0:
            receipt["zero_origin"] = "rounded_local_Born_mass_not_exact_source_zero"
            return 0.0, receipt
        conditional_probability *= normalized
        if conditional_probability == 0 or not math.isfinite(conditional_probability):
            raise RetainedFailure("Conditional product underflow/nonfinite", receipt)
        state = sampler.project(outputs, probabilities, suffixes, groups, selected, color)
    value = float(exact_mass)*conditional_probability
    if not math.isfinite(value) or not 0 <= value <= 1+2e-10:
        raise RetainedFailure("Invalid final structured probability", receipt)
    return value, receipt


def comparison(p64, p_naive):
    if any(not math.isfinite(p) or not 0 <= p <= 1+2e-10 for p in (p64, p_naive)):
        raise RetainedFailure("Invalid engine probability", {"P64": p64, "Naive": p_naive})
    scale = max(p64, p_naive)
    error = abs(p64-p_naive)
    relative = error/scale if scale else 0.0
    return {"absolute_error": error, "relative_error": relative,
            "allowed_error": ABSOLUTE_TOLERANCE+RELATIVE_TOLERANCE*scale,
            "absolute_term_dominates": ABSOLUTE_TOLERANCE >= RELATIVE_TOLERANCE*scale,
            "relative_precision_certified": False, "global_TV_certified": False,
            "within_frozen_tolerance": error <= ABSOLUTE_TOLERANCE+RELATIVE_TOLERANCE*scale}


def native_readback(xq):
    value = int(xq.Config.compute_max_thread_count)
    if value != 1:
        raise RetainedFailure("Native maximum-thread readback", {"observed": value})
    return value


def load_naive_api():
    for variable in THREAD_VARIABLES:
        os.environ[variable] = "1"
    import exqalibur as xq
    before = int(xq.Config.compute_max_thread_count)
    xq.Config.compute_max_thread_count = 1
    import numpy as np
    from perceval.backends import NaiveBackend
    from perceval.components import Unitary
    from perceval.utils import FockState
    versions = {name: importlib.metadata.version(name) for name in ("numpy", "perceval-quandela", "exqalibur")}
    if versions != {"numpy": "2.4.6", "perceval-quandela": "1.3.0", "exqalibur": "1.4.2"}:
        raise RetainedFailure("Pinned native software versions differ", versions)
    metadata = {"maximum_threads_before": before, "maximum_threads_configured": native_readback(xq),
                "environment_threads": {key: os.environ[key] for key in THREAD_VARIABLES},
                "versions": versions,
                "Naive_backend_file": {"path": inspect.getfile(NaiveBackend), "sha256": file_hash(inspect.getfile(NaiveBackend))},
                "backend": "local_NaiveBackend.prob_amplitude_exqalibur.permanent_cx_no_mask_iterator_sample_or_remote"}
    return (np, xq, NaiveBackend, Unitary, FockState), metadata


def backend_for(matrix, source, api):
    np, xq, Backend, Unitary, State = api
    native_readback(xq)
    backend = Backend()
    backend.set_circuit(Unitary(np.asarray(matrix, dtype=complex)))
    backend.set_input_state(State(list(source)))
    return backend


def naive_probability(backend, counts, api):
    amplitude = complex(backend.prob_amplitude(api[4](list(counts))))
    if not math.isfinite(amplitude.real) or not math.isfinite(amplitude.imag):
        raise RetainedFailure("Nonfinite Naive amplitude", {"real": repr(amplitude.real), "imag": repr(amplitude.imag)})
    return abs(amplitude)**2, {"real": amplitude.real, "imag": amplitude.imag}


def fresh_output(path):
    path = Path(path).absolute()
    if ".." in path.parts or not path.is_relative_to(ROOT) or path.exists():
        raise ValueError("New project-relative output required")
    for parent in (path, *path.parents):
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise ValueError("Symlink output ancestor")
    path.mkdir(parents=True, exist_ok=False)
    return path


def execute(spec, output):
    if spec != expected_spec():
        raise ValueError("Frozen N18 point specification changed")
    output = fresh_output(output)
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    records, failure, native, native_setups = [], None, {}, {}
    stage, current = "source_provenance", {}
    api = None
    def guard():
        if (time.perf_counter()-started_wall >= 90 or time.process_time()-started_cpu >= 60
                or sum(path.stat().st_size for path in output.iterdir() if path.is_file()) >= 33554432-1048576):
            raise RetainedFailure("Frozen resource/output guard")
    with (output/"points.jsonl").open("x", encoding="utf8") as stream:
        try:
            for relative, expected in ((PRIMARY_SOURCE_TABLE, PRIMARY_SOURCE_SHA256),
                                       (PRIMARY_MANIFEST, PRIMARY_MANIFEST_SHA256),
                                       ("research/P64_structured_sampler.py", P64_SOURCE_SHA256)):
                if file_hash(ROOT/relative) != expected:
                    raise RetainedFailure("Pinned input differs", {"path": relative})
            primary_table = json.loads((ROOT/PRIMARY_SOURCE_TABLE).read_text())
            independent, source_time = timed(independent_source.exact_source_table)
            source_comparison = independent_source.comparison(independent, primary_table)
            save_json(output/"independent_source.json", {"independent": independent,
                      "primary_comparison": source_comparison, "timing": source_time,
                      "primary_table_sha256": PRIMARY_SOURCE_SHA256})
            if not all(independent["checks"].values()) or not source_comparison["all_rows_equal"]:
                raise RetainedFailure("Independent exact F6 source disagreement", source_comparison)
            # Production import occurs only AFTER the independent source check.
            stage = "structured_setup"
            from P64_structured_sampler import StructuredSampler
            sampler, structured_setup = timed(lambda: StructuredSampler(6))
            stage = "native_imports"
            loaded, native_imports = timed(load_naive_api)
            api, native = loaded
            for phase in spec["phase_arrays"]:
                guard()
                stage = "matrix/"+phase["id"]
                current = {"phase": phase}
                theta = tuple(tuple(float(Fraction(v)) for v in row) for row in phase["exact"])
                dense, dense_time = timed(lambda: dense_reference_matrix(theta))
                scalar, scalar_time = timed(lambda: scalar_architecture_matrix(theta))
                diagnostics, diagnostics_time = timed(lambda: matrix_diagnostics(dense, scalar))
                save_json(output/f"matrices_{phase['id']}.json", {"phase": phase, "dense_reference": matrix_record(dense),
                          "scalar_architecture": matrix_record(scalar), "diagnostics": diagnostics,
                          "dense_timing": dense_time, "scalar_timing": scalar_time, "diagnostic_timing": diagnostics_time})
                if any(not math.isfinite(value) or value > MATRIX_TOLERANCE for value in diagnostics.values()):
                    raise RetainedFailure("Independent architecture matrix guard", diagnostics)
                backend, native_setup = timed(lambda: backend_for(dense, [1]*18, api))
                native_setups[phase["id"]] = native_setup
                for occupation in spec["occupations"]:
                    guard()
                    stage = phase["id"]+"/"+occupation["id"]
                    counts = tuple(occupation["counts"])
                    current = {"phase": phase, "occupation": occupation, "counts": counts}
                    structured, structured_time = timed(lambda: structured_probability(sampler, theta, counts))
                    p64, path = structured
                    current.update(P64_probability=p64, P64_path=path, P64_timing=structured_time)
                    naive, naive_time = timed(lambda: naive_probability(backend, counts, api))
                    p_naive, amplitude = naive
                    current.update(Naive_probability=p_naive, Naive_amplitude=amplitude, Naive_timing=naive_time)
                    errors = comparison(p64, p_naive)
                    record = {**current, "P64_probability": p64, "Naive_probability": p_naive,
                              "Naive_amplitude": amplitude, "P64_path": path, "errors": errors,
                              "P64_timing": structured_time, "Naive_timing": naive_time,
                              "native_setup_phase_id": phase["id"], "cache_entries_after_point": sampler.cache.entries}
                    if occupation["id"] == "all18_port12_flat_anchor":
                        anchor = Fraction(math.factorial(18), 18**18)
                        record["analytic_anchor"] = {"exact": str(anchor), "float": float(anchor),
                            "P64_errors": comparison(p64, float(anchor)), "Naive_errors": comparison(p_naive, float(anchor))}
                    # Both engines and all tolerances/times are durable BEFORE assertions.
                    emit(stream, record)
                    records.append(record)
                    if not errors["within_frozen_tolerance"]:
                        raise RetainedFailure("N18 engine point disagreement", {"stage": stage, "errors": errors})
                    if "analytic_anchor" in record and not all(record["analytic_anchor"][name]["within_frozen_tolerance"]
                                                               for name in ("P64_errors", "Naive_errors")):
                        raise RetainedFailure("Unmixed full-bunching factorial anchor disagreement", {"stage": stage})
            stage = "native_final_readback"
            native["maximum_threads_after"] = native_readback(api[1])
            summary = {"status": "FOURTEEN_FIXED_POINTS_WITHIN_FROZEN_TOLERANCE", "points": len(records),
                       "source_check": source_comparison, "structured_setup": structured_setup,
                       "native_imports": native_imports, "native": native}
        except Exception as error:
            failure = {"stage": stage, "error": repr(error), "evidence": getattr(error, "evidence", {}), "current": current}
            emit(stream, {"record_type": "first_failure", **failure})
            summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "points": len(records), "failure": failure, "native": native}
            if api is not None:
                try:
                    native["maximum_threads_after_failure"] = native_readback(api[1])
                except Exception as readback_error:
                    native["readback_failure"] = repr(readback_error)
    save_json(output/"failure.json", {"failure": failure})
    summary.update(positive_accepted=False, optimizer_tested=False, full_N18_law_verified=False,
                   global_TV_certified=False, native_random_draws=0, graphs=0, actual_QPU_calls=0,
                   max_absolute_error=max((row["errors"]["absolute_error"] for row in records), default=None),
                   max_relative_error=max((row["errors"]["relative_error"] for row in records), default=None),
                   absolute_dominated_points=sum(row["errors"]["absolute_term_dominates"] for row in records),
                   native_setup_by_phase=native_setups,
                   runtime_optimizer_claim=False, cpu_seconds=time.process_time()-started_cpu,
                   wall_seconds=time.perf_counter()-started_wall, source_sha256=file_hash(Path(__file__)),
                   points_sha256=file_hash(output/"points.jsonl"))
    save_json(output/"summary.json", summary)
    return summary, failure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary, failure = execute(json.loads(args.spec.read_text()), args.output)
    print(json.dumps({"status": summary["status"], "points": summary["points"], "positive_accepted": False}))
    return int(failure is not None)


if __name__ == "__main__":
    raise SystemExit(main())
