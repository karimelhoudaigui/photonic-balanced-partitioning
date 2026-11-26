"""P110 fixed-point 330-amplitude replication; authoring/import is not execution authority."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import importlib
import importlib.metadata
import json
import math
import os
import resource
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
PYTHON = "/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python"
SPEC = "research/P110_native_filter_replication_contract_TEMPLATE.json"
BINDING = "research/P110_native_filter_execution_binding.json"
OUTPUT = "experiments/P110_native_filter_main/run_001/data"
CAP, RESERVE = 8388608, 65536
ABS_TOL, REL_TOL = 2e-12, 1e-10
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
VERSIONS = {"numpy": "2.4.6", "perceval-quandela": "1.3.0", "exqalibur": "1.4.2"}
STATIC = ("AGENTS.md", "pyproject.toml", "requirements-research-lock.txt",
          "research/P110_P107_NATIVE_REPLICATION_CARD.md",
          "research/P110_native_filter_replication.py", SPEC)
FROZEN = {
    "research/P110_P107_NATIVE_REPLICATION_CARD.md": "e97d7e7fc8a1a34441042bc5b32595c0e464ffa91c053e7760e8007ca38a6f7c",
    "research/P101_FINITE_FILTER_ALL_OUTPUT_CARD.md": "65e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c",
    "research/P107_symbolic_filter_validation.py": "4e0973ebfe8a250dbf012719087dcb0b7390932acd3ddab4e7055b3808cb2bbc",
    "research/P107_SYMBOLIC_FILTER_POPULATION.md": "051d24038066d7cac3ef34f6f835703793c0d7e93b085cf20fa03d99ac14636b",
    "research/P107_symbolic_filter_contract_TEMPLATE.json": "d150e2042c5f8a02b09baab4da8426fd92348eb66525a2d7bf1a90ddb734e8ed"}
RAW_ROLES = ("manifest", "stdout", "stderr", "records", "summary", "failure")
PRODUCER_SEAL = "99f2d98d93f13c7fc088218bfb06ff39af4c40e9"
PRODUCER_RAW = {
    "manifest": "research/P107_symbolic_filter_main/run_001/manifest.json",
    "stdout": "research/P107_symbolic_filter_main/run_001/stdout.txt",
    "stderr": "research/P107_symbolic_filter_main/run_001/stderr.txt",
    "records": "research/P107_symbolic_filter_main/run_001/data/records.jsonl",
    "summary": "research/P107_symbolic_filter_main/run_001/data/summary.json",
    "failure": "research/P107_symbolic_filter_main/run_001/data/failure.json"}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def clean(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, complex):
        return [clean(value.real), clean(value.imag)]
    if isinstance(value, float) and not math.isfinite(value):
        return {"nonfinite_float_repr": repr(value)}
    if isinstance(value, dict):
        return {str(key): clean(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [clean(item) for item in value]
    return value


def unique_object(pairs):
    answer = {}
    for key, value in pairs:
        require(key not in answer, "duplicate JSON member: " + repr(key))
        answer[key] = value
    return answer


def bad_constant(value):
    raise ValueError("nonstandard JSON numeric constant: " + value)


def loads(text):
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=bad_constant)


def digest(path, algorithm="sha256", git_blob=False):
    result = hashlib.new(algorithm)
    if git_blob:
        result.update(("blob " + str(path.stat().st_size) + "\0").encode("ascii"))
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            result.update(block)
    return result.hexdigest()


def safe(relative):
    path = Path(relative)
    require(isinstance(relative, str) and path.as_posix() == relative
            and not path.is_absolute() and path.parts
            and all(part not in (".", "..") for part in path.parts), "canonical relative input")
    actual = ROOT
    for part in path.parts:
        actual /= part
        require(not actual.is_symlink(), "input symlink: " + relative)
    require(actual.is_file(), "regular input: " + relative)
    return actual


class Evidence:
    def __init__(self):
        directory = ROOT / OUTPUT
        require(directory.parent.is_dir() and not directory.exists(), "fresh runner child")
        actual = ROOT
        for part in Path(OUTPUT).parts:
            actual /= part
            require(not actual.is_symlink(), "output symlink")
        directory.mkdir()
        self.directory, self.used, self.rows = directory, 0, 0
        self.handle = (directory / "records.jsonl").open("x", encoding="ascii")

    @staticmethod
    def payload(value):
        return json.dumps(clean(value), ensure_ascii=True, sort_keys=True,
                          separators=(",", ":"), allow_nan=False) + "\n"

    def emit(self, row):
        text = self.payload(row)
        size = len(text.encode("ascii"))
        require(self.used + size <= CAP - RESERVE, "combined scientific-output reserve")
        self.handle.write(text)
        self.handle.flush()
        self.used += size
        self.rows += 1

    def finish(self, summary, failure):
        self.handle.close()
        values = [self.payload(summary), self.payload(failure)]
        require(self.used + sum(len(text.encode("ascii")) for text in values) <= CAP,
                "combined scientific-output cap")
        for name, text in zip(("summary.json", "failure.json"), values):
            with (self.directory / name).open("x", encoding="ascii") as handle:
                handle.write(text)


def occupations(total, modes):
    """Independent stars-and-bars indexing, in ascending lexicographic order."""
    for bars in combinations(range(total + modes - 1), modes - 1):
        boundaries = (-1,) + bars + (total + modes - 1,)
        yield tuple(boundaries[j + 1] - boundaries[j] - 1 for j in range(modes))


def signal_states():
    return [state for total in range(5) for state in occupations(total, 4)]


def dagger(matrix):
    return [[matrix[j][i].conjugate() for j in range(len(matrix))]
            for i in range(len(matrix[0]))]


def product(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), 0j)
             for j in range(len(right[0]))] for i in range(len(left))]


def identity(size):
    return [[complex(i == j) for j in range(size)] for i in range(size)]


def within(observed, expected):
    return math.isfinite(abs(observed)) and abs(observed - expected) <= ABS_TOL + REL_TOL * abs(expected)


def independent_dilation(writer):
    phases = (1 + 0j, -1j, -1 + 0j, 1j)
    fourier = [[phases[(j * r) % 4] / 2 for r in range(4)] for j in range(4)]
    values = (1.0, 0.5, 0.125, 0.25)
    writer.emit({"kind": "construction_operands", "F": fourier, "d": values,
                 "e_squared_exact": ["0", "3/4", "63/64", "15/16"]})
    roots = (0.0, math.sqrt(3) / 2, math.sqrt(63) / 8, math.sqrt(15) / 4)
    def lift(diagonal):
        return [[sum((fourier[j][r] * diagonal[r] * fourier[k][r].conjugate()
                      for r in range(4)), 0j) for k in range(4)] for j in range(4)]
    transfer, environment = lift(values), lift(roots)
    unitary = [transfer[j] + environment[j] for j in range(4)]
    unitary += [environment[j] + [-value for value in transfer[j]] for j in range(4)]
    writer.emit({"kind": "construction", "F": fourier, "d": values, "e": roots,
                 "T": transfer, "E": environment, "U": unitary,
                 "point_exact": ["1/2", "1/4"], "input": [1, 1, 1, 1, 0, 0, 0, 0]})
    t2, e2 = product(transfer, transfer), product(environment, environment)
    checks = [("T_Hermitian", transfer, dagger(transfer)),
              ("E_Hermitian", environment, dagger(environment)),
              ("T_colGram", product(dagger(transfer), transfer), lift(tuple(v * v for v in values))),
              ("T2_plus_E2", [[t2[i][j] + e2[i][j] for j in range(4)] for i in range(4)], identity(4)),
              ("TE_commutes", product(transfer, environment), product(environment, transfer)),
              ("U_colGram", product(dagger(unitary), unitary), identity(8)),
              ("U_rowGram", product(unitary, dagger(unitary)), identity(8))]
    failures = []
    for name, observed, expected in checks:
        differences = [[abs(observed[i][j] - expected[i][j]) for j in range(len(expected))]
                       for i in range(len(expected))]
        writer.emit({"kind": "matrix_check", "name": name, "observed": observed,
                     "expected": expected, "absolute_errors": differences})
        if not all(within(observed[i][j], expected[i][j]) for i in range(len(expected)) for j in range(len(expected))):
            failures.append(name)
    require(not failures, "matrix checks: " + repr(failures))
    return unitary


def authorize(relative, writer):
    require(relative == BINDING, "fixed future active binding path")
    binding = loads(safe(relative).read_text(encoding="utf-8"))
    writer.emit({"kind": "binding_observation", "binding": binding})
    require(binding["binding_state"] == "ROOT_AUTHORIZED" and binding["run_authorized"] is True,
            "separate ROOT execution authorization")
    require(binding["claim_id"] == "P110-P107-FIXED-POINT-NATIVE-REPLICATION", "claim identity")
    require(sys.version_info[:3] == (3, 11, 15) and Path(sys.executable).absolute() == Path(PYTHON),
            "persistent Python3.11.15 required only for main")
    artifacts = binding["artifacts"]
    names = [row["path"] for row in artifacts]
    require(len(names) == len(set(names)) and relative not in names
            and (set(STATIC) | set(FROZEN)) <= set(names), "complete unique frozen input closure")
    require(len(binding["execution_artifacts"]) == len(names) + 1
            and set(binding["execution_artifacts"]) == set(names) | {relative}, "exact runner self-input closure")
    observations = []
    for row in artifacts:
        path = safe(row["path"])
        observed = {"path": row["path"], "bytes": path.stat().st_size, "sha256": digest(path)}
        writer.emit({"kind": "input_observation", **observed})
        require(type(row["bytes"]) is int and row["bytes"] == observed["bytes"]
                and row["sha256"] == observed["sha256"], "bound input hash/size")
        if row["path"] in FROZEN:
            require(observed["sha256"] == FROZEN[row["path"]], "exact frozen theory/schema/card")
        observations.append(observed)
    require(binding["source_sha256"] == digest(Path(__file__)), "actual frozen P110 source")
    raw = binding["producer_raw"]
    require(len(raw) == 6 and {row["role"] for row in raw} == set(RAW_ROLES)
            and len({row["path"] for row in raw}) == 6
            and {row["path"] for row in raw} <= set(names)
            and {row["role"]: row["path"] for row in raw} == PRODUCER_RAW, "six opaque bound producer files")
    seal = binding["producer_seal_commit"]
    require(seal == PRODUCER_SEAL, "original raw seal commit communicated as opaque identity")
    descriptors = {row["path"]: row for row in artifacts}
    for row in raw:
        path = safe(row["path"])
        actual_blob = digest(path, "sha1", True)
        sealed_blob = subprocess.run(["git", "rev-parse", seal + ":" + row["path"]], cwd=ROOT,
                                     capture_output=True, text=True, check=True).stdout.strip()
        writer.emit({"kind": "producer_blob_observation", **row, "observed_git_blob": actual_blob,
                     "sealed_git_blob": sealed_blob, "seal_commit": seal})
        require(actual_blob == sealed_blob == row["git_blob_sha1"]
                and row["sha256"] == descriptors[row["path"]]["sha256"], "original-seal blob/hash binding")
    spec = loads(safe(SPEC).read_text(encoding="utf-8"))
    provenance = {"Python": sys.version, "executable": sys.executable, "inputs": observations,
                  "binding_sha256": digest(safe(relative)), "external_before": []}
    for pin in spec["external_artifacts"]:
        actual = digest(Path(pin["path"]))
        writer.emit({"kind": "external_pin_observation", **pin, "observed_sha256": actual})
        require(actual == pin["sha256"], "preimport external pin")
        provenance["external_before"].append(pin)
    versions = {name: importlib.metadata.version(name) for name in VERSIONS}
    writer.emit({"kind": "version_observation", "versions": versions})
    require(versions == VERSIONS, "pinned numerical/native versions")
    provenance["versions"] = versions
    require(digest(Path(sys.executable).resolve()) == next(pin["sha256"] for pin in spec["external_artifacts"]
                                                        if pin["role"] == "physical_interpreter"), "running interpreter hash")
    return binding, spec, provenance


def reference_law(binding, writer, state, guard):
    paths = {row["role"]: safe(row["path"]) for row in binding["producer_raw"]}
    manifest = loads(paths["manifest"].read_text(encoding="utf-8"))
    summary = loads(paths["summary"].read_text(encoding="utf-8"))
    failure = loads(paths["failure"].read_text(encoding="utf-8"))
    writer.emit({"kind": "producer_completion_observation", "manifest_run": manifest.get("run"),
                 "summary": summary, "failure": failure})
    require(type(manifest["schema_version"]) is int and manifest["schema_version"] == 2
            and manifest["claim_id"] == "P107-EXACT-P101-FINITE-FILTER-SQUARE-DISCRIMINATOR"
            and manifest["run"]["status"] == "completed"
            and type(manifest["run"]["exit_status"]) is int and manifest["run"]["exit_status"] == 0,
            "completed v2 P107 reference")
    source_inputs = manifest["input_artifacts"]
    require(len({row["path"] for row in source_inputs}) == len(source_inputs), "unique producer manifest inputs")
    observed_inputs = {row["path"]: row for row in source_inputs}
    for name, expected in FROZEN.items():
        if name.startswith("research/P101_") or name.startswith("research/P107_"):
            require(name in observed_inputs and observed_inputs[name]["sha256"] == expected
                    and observed_inputs[name]["sha256_after"] == expected, "producer actually bound frozen source/schema")
    observed_outputs = manifest["outputs"]
    require(len(observed_outputs) == 5 and len({row["path"] for row in observed_outputs}) == 5,
            "five unique producer result/log manifest outputs")
    output_hashes = {row["path"]: row["sha256"] for row in observed_outputs}
    raw_hashes = {row["path"]: row["sha256"] for row in binding["producer_raw"] if row["role"] != "manifest"}
    require(output_hashes == raw_hashes
            and set(manifest["declared_results"]) == {PRODUCER_RAW[role] for role in ("records", "summary", "failure")}
            and len(manifest["declared_results"]) == 3, "manifest outputs linked to all five sealed payload/log files")
    require(summary["ENGINE_PASS"] is True and type(summary["records"]) is int and summary["records"] == 9612
            and type(summary["counts"]["coefficients"]) is int and summary["counts"]["coefficients"] == 5670
            and summary["NOT_RUN"] == [] and summary["FAILED_TASK"] == [] and failure is None,
            "complete nominal producer reference")
    support = signal_states()
    require(len(support) == len(set(support)) == 70, "70 unique signal occupations")
    keys = [(n, (i, j)) for n in support for i in range(9) for j in range(9)]
    answer = {n: Fraction(0) for n in support}
    observed_count, total_rows = 0, 0
    with paths["records"].open(encoding="utf-8") as handle:
        for total_rows, line in enumerate(handle, 1):
            guard()
            state["reference_line"] = total_rows
            row = loads(line)
            if row.get("kind") != "coefficient":
                continue
            state["last_reference_coefficient"] = row
            require(observed_count < len(keys), "too many coefficients")
            n, powers = row["occupation"], row["powers"]
            require(isinstance(n, list) and len(n) == 4 and all(type(x) is int and x >= 0 for x in n)
                    and isinstance(powers, list) and len(powers) == 2 and all(type(x) is int for x in powers), "coefficient indexing types")
            key = tuple(n), tuple(powers)
            require(key == keys[observed_count] and type(row["denominator"]) is int
                    and row["denominator"] == 65536, "complete ordered coefficient schema")
            for label in ("B", "D", "B_minus_D", "B_moment"):
                pair = row[label]
                require(isinstance(pair, list) and len(pair) == 2 and all(type(value) is int for value in pair)
                        and pair[1] == 0, "real Gaussian integer coefficient: " + label)
            require(row["B_moment"] == row["B"] and row["B_minus_D"][0] == row["B"][0] - row["D"][0], "reference coefficient consistency")
            answer[tuple(n)] += Fraction(row["B"][0], 65536) * Fraction(1, 2) ** powers[0] * Fraction(1, 4) ** powers[1]
            observed_count += 1
    state.pop("last_reference_coefficient", None)
    require(total_rows == 9612 and observed_count == 5670, "whole producer record/coefficient population")
    for n in support:
        writer.emit({"kind": "reference_evaluation", "signal": n, "exact_B": answer[n],
                     "point": ["1/2", "1/4"]})
    require(all(value >= 0 for value in answer.values()) and sum(answer.values()) == 1, "physical exact reference law")
    state["reference_bins"] = 70
    return answer


def snapshot(xq):
    report = {"environment": {key: os.environ.get(key) for key in THREADS}}
    try:
        value = xq.Config.compute_max_thread_count
        report["native"] = value if type(value) in (int, float, str, bool) else None
        report["native_repr"] = repr(value)
        report["native_type"] = type(value).__name__
    except Exception as error:
        report["native"] = None
        report["readback_exception"] = repr(error)
    return report


def check_snapshot(report):
    require(type(report.get("native")) is int and report["native"] == 1
            and all(report["environment"].get(key) == "1" for key in THREADS), "actual native/environment thread readback")


def native_stack(spec, writer, state):
    import exqalibur as xq
    initial = state["native_before_configuration"] = snapshot(xq)
    writer.emit({"kind": "native_before_configuration", "readback": initial})
    require(type(initial["native"]) is int and initial["native"] >= 0
            and all(initial["environment"].get(key) == "1" for key in THREADS), "observable initial native/environment configuration")
    xq.Config.compute_max_thread_count = 1
    state["configuration_readback"] = snapshot(xq)
    writer.emit({"kind": "native_configured", "readback": state["configuration_readback"]})
    check_snapshot(state["configuration_readback"])
    import numpy as np
    import perceval as pcvl
    from perceval.backends import NaiveBackend
    loaded = {}
    for pin in spec["external_artifacts"]:
        if "module" in pin:
            actual = Path(importlib.import_module(pin["module"]).__file__).resolve()
            observation = {"module": pin["module"], "path": str(actual), "sha256": digest(actual)}
            loaded[pin["module"]] = observation
            writer.emit({"kind": "actually_loaded_pin", **observation})
            require(actual == Path(pin["path"]).resolve() and observation["sha256"] == pin["sha256"], "actual loaded critical identity")
    state["after_import_readback"] = snapshot(xq)
    writer.emit({"kind": "native_after_imports", "readback": state["after_import_readback"], "loaded": loaded})
    check_snapshot(state["after_import_readback"])
    return np, pcvl, NaiveBackend, xq


def replicate(unitary, reference, stack, writer, state, guard):
    np, pcvl, backend_type, xq = stack
    backend = backend_type()
    backend.set_circuit(pcvl.Circuit(8).add(0, pcvl.Unitary(pcvl.Matrix(np.array(unitary, dtype=complex)))))
    backend.set_input_state(pcvl.BasicState([1, 1, 1, 1, 0, 0, 0, 0]))
    full_states = list(occupations(4, 8))
    require(len(full_states) == len(set(full_states)) == 330
            and all(len(n) == 8 and sum(n) == 4 for n in full_states), "330 unique full-PNR outputs")
    probabilities, contributions = [], {n: [] for n in reference}
    groups = {n: [] for n in reference}
    state.update(native_calls_attempted=0, native_calls_returned=0, native_records=0)
    for index, counts in enumerate(full_states):
        guard()
        state.update(native_index=index, counts=counts, last_native_return_repr=None,
                     last_amplitude=None, last_probability=None, last_native_after=None)
        before = snapshot(xq)
        writer.emit({"kind": "native_before", "index": index, "counts": counts, "readback": before})
        check_snapshot(before)
        error, amplitude, probability = None, None, None
        state["native_calls_attempted"] += 1
        try:
            raw = backend.prob_amplitude(pcvl.BasicState(list(counts)))
            state["last_native_return_repr"] = repr(raw)
            state["native_calls_returned"] += 1
            writer.emit({"kind": "native_return", "index": index, "counts": counts,
                         "amplitude_repr": state["last_native_return_repr"]})
            amplitude = complex(raw)
            state["last_amplitude"] = amplitude
            probability = abs(amplitude) ** 2
            state["last_probability"] = probability
        except Exception as exception:
            error = exception
            state["native_exception_repr"] = repr(exception)
        finally:
            state["last_native_after"] = snapshot(xq)
            writer.emit({"kind": "native_after", "index": index, "counts": counts,
                         "readback": state["last_native_after"],
                         "amplitude_repr": state["last_native_return_repr"]})
        writer.emit({"kind": "native_raw", "index": index, "counts": counts, "signal": counts[:4],
                     "loss": sum(counts[4:]), "amplitude": amplitude, "probability": probability,
                     "amplitude_repr": state["last_native_return_repr"],
                     "exception_repr": repr(error) if error is not None else None})
        if error is not None:
            raise RuntimeError("first native API/conversion failure") from error
        check_snapshot(state["last_native_after"])
        require(math.isfinite(amplitude.real) and math.isfinite(amplitude.imag)
                and math.isfinite(probability), "finite native amplitude/probability; diagnostics emitted")
        probabilities.append(probability)
        contributions[counts[:4]].append(probability)
        groups[counts[:4]].append(index)
        state["native_records"] += 1
    failures, maximum_error = [], 0.0
    for n, exact in reference.items():
        observed = math.fsum(contributions[n])
        expected = float(exact)
        error = abs(observed - expected)
        maximum_error = max(maximum_error, error)
        writer.emit({"kind": "marginal_comparison", "signal": n, "loss": 4 - sum(n),
                     "full_output_indices": groups[n], "observed": observed, "exact_reference": exact,
                     "reference_float": expected, "absolute_error": error,
                     "allowed_error": ABS_TOL + REL_TOL * abs(expected), "within_tolerance": within(observed, expected)})
        if not within(observed, expected):
            failures.append(n)
    total = math.fsum(probabilities)
    marginal_total = math.fsum(math.fsum(values) for values in contributions.values())
    writer.emit({"kind": "normalization_comparison", "native_total": total,
                 "marginal_total": marginal_total, "reference_total": sum(reference.values()),
                 "full_outputs": len(probabilities), "marginals": len(contributions), "failed_bins": failures})
    state.update(marginal_bins=len(contributions), maximum_absolute_error=maximum_error,
                 first_failed_bin=failures[0] if failures else None)
    require(not failures and within(total, 1.0) and within(marginal_total, 1.0), "all70 marginal and both mass checks")
    require(state["native_records"] == state["native_calls_attempted"] == state["native_calls_returned"] == 330,
            "complete fixed native call population")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", required=True)
    args = parser.parse_args(argv)
    started = time.process_time(), time.perf_counter()
    writer, failure = None, None
    state = {"phase": "PREIMPORT", "status": "NOT_RUN", "positive_accepted": False,
             "native_calls_attempted": 0, "native_calls_returned": 0,
             "native_records": 0, "reference_bins": None, "marginal_bins": None}
    try:
        resource.setrlimit(resource.RLIMIT_FSIZE, (CAP, CAP))
        resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
        for key in THREADS:
            os.environ[key] = "1"
        writer = Evidence()
        writer.emit({"kind": "preimport_profile", "environment": {key: os.environ.get(key) for key in THREADS},
                     "RLIMIT_FSIZE": resource.getrlimit(resource.RLIMIT_FSIZE), "RNG": False})
        def guard():
            require(time.process_time() - started[0] <= 60 and time.perf_counter() - started[1] <= 90, "CPU60/wall90")
        binding, spec, provenance = authorize(args.binding, writer)
        state["phase"] = "REFERENCE"
        reference = reference_law(binding, writer, state, guard)
        guard()
        state["phase"] = "CONSTRUCTION"
        unitary = independent_dilation(writer)
        state["phase"] = "NATIVE_SETUP"
        stack = native_stack(spec, writer, state)
        state["phase"] = "NATIVE_POPULATION"
        replicate(unitary, reference, stack, writer, state, guard)
        state["final_readback"] = snapshot(stack[3])
        writer.emit({"kind": "final_readback", "readback": state["final_readback"]})
        check_snapshot(state["final_readback"])
        for row in provenance["inputs"]:
            require(digest(safe(row["path"])) == row["sha256"], "unchanged project inputs")
        require(digest(safe(args.binding)) == provenance["binding_sha256"], "unchanged active binding")
        for pin in spec["external_artifacts"]:
            require(digest(Path(pin["path"])) == pin["sha256"], "unchanged external pins")
        guard()
        state.update(phase="COMPLETE", status="FINITE_NATIVE_REPLICATION_PASS")
    except Exception as exception:
        failure = {"exception": repr(exception), "traceback": traceback.format_exc(), "prefix": dict(state)}
        state["status"] = "INCONCLUSIVE_FIRST_FAILURE"
        if writer is None:
            sys.stderr.write(Evidence.payload(failure))
    finally:
        state["main_body_elapsed"] = {"cpu_seconds": time.process_time() - started[0],
                                      "wall_seconds": time.perf_counter() - started[1]}
        state["NOT_RUN_native_outputs"] = 330 - state["native_calls_attempted"]
        if writer is not None:
            state["scientific_records"] = writer.rows
            writer.finish(state, failure)
    return int(failure is not None)


if __name__ == "__main__":
    raise SystemExit(main())
