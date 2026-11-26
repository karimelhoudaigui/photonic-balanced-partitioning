"""Read sealed P90a tiny qualification; integer DP independent of test permutations."""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def multiply(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def amplitude_reference(family, removed, counts):
    phases = ((1, 0), (0, 1), (-1, 0), (0, -1))
    if family == "HOM":
        matrix, denominators = (((1, 0), (1, 0)), ((1, 0), (-1, 0))), (2, 2)
    elif family == "flat":
        matrix = tuple(tuple(phases[(a*j) % 4] for j in range(4)) for a in range(4))
        denominators = (4, 4, 4, 4)
    elif family == "toy":
        matrix = (((1, 0), (1, 0), (0, 0), (0, 0)),
                  ((1, 0), (-1, 0), (0, 0), (0, 0)),
                  ((0, 0), (0, 0), (1, 0), (0, 0)),
                  ((0, 0), (0, 0), (0, 0), (1, 0)))
        denominators = (2, 2, 1, 1)
    else:
        raise AssertionError("unknown family")
    assert len(counts) == len(matrix) and sum(counts) == len(removed) <= 4
    rows = [a for a, number in enumerate(counts) for _ in range(number)]
    # Subset DP, with the current row inferred from the number of used columns.
    # This does not enumerate permutations or import the fixture oracle.
    table = {0: (1, 0)}
    for used in range(1 << len(removed)):
        if used not in table or used.bit_count() == len(removed):
            continue
        row = rows[used.bit_count()]
        for j, source in enumerate(removed):
            if not used & (1 << j):
                target = used | (1 << j)
                table[target] = add(table.get(target, (0, 0)),
                                    multiply(table[used], matrix[row][source]))
    numerator = table[(1 << len(removed))-1]
    denominator = math.prod(denominators[j] for j in removed)
    denominator *= math.prod(math.factorial(number) for number in counts)
    probability = Fraction(numerator[0]**2+numerator[1]**2, denominator)
    return complex(*numerator)/math.sqrt(denominator), probability


def occupations(modes, photons):
    if modes == 1:
        yield (photons,)
    else:
        for count in range(photons+1):
            for tail in occupations(modes-1, photons-count):
                yield (count,)+tail


def planned_keys():
    keys = [("HOM", (0, 1), counts) for counts in occupations(2, 2)]
    keys += [("flat", pair, counts) for pair in combinations(range(4), 2)
             for counts in occupations(4, 2)]
    keys += [("toy", source, counts) for r in range(1, 5)
             for source in combinations(range(4), r) for counts in occupations(4, r)]
    return keys


def inspect(root, raw_seal):
    run = root/"research/P90a_dev_veto_preflight/run_001"
    manifest = json.loads((run/"manifest.json").read_text())
    contract = json.loads((root/"research/P90a_preflight_contract.json").read_text())
    spec = json.loads((root/"research/P90a_execution_spec.json").read_text())
    assert manifest["repository"] == {"commit": "82d7b63d35f2f0495df6ed9c0d86999b649c44ff", "dirty": False}
    assert manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0
    assert not manifest["run"]["missing_results"] and not manifest["run"]["invalid_results"]
    assert all(row["passed"] for row in manifest["checks"])
    assert manifest["execution_artifacts"] == contract["execution_artifacts"]
    assert manifest["command"] == contract["planned_command"]
    assert len(manifest["input_artifacts"]) == 18
    for row in manifest["input_artifacts"]:
        assert sha(root/row["path"]) == row["sha256"] == row["sha256_after"]
    paths = [row["path"] for row in manifest["outputs"]]+[str((run/"manifest.json").relative_to(root))]
    for path in paths:
        archived = subprocess.check_output(["git", "-C", str(root), "show", raw_seal+":"+path])
        assert archived == (root/path).read_bytes()
    for row in manifest["outputs"]:
        assert sha(root/row["path"]) == row["sha256"]
    for row in spec["external_artifacts"]:
        assert sha(row["path"]) == row["sha256"]
    xml = ET.parse(run/"junit.xml")
    cases = xml.findall(".//testcase")
    assert len(cases) == 283
    assert not any(xml.findall(".//"+tag) for tag in ("failure", "error", "skipped"))
    population = (root/"research/P90a_IMPLEMENTATION_POPULATION.md").read_text()
    declared = re.findall(r"^tests/test_p90a_source_bound_nonflat_veto.py::([^\n]+)$", population, re.M)
    assert [row.attrib["name"] for row in cases] == declared
    observations, probability_errors, amplitude_errors, zero_count, native_zero_count = [], [], [], 0, 0
    first_provenance = None
    for case in cases:
        props = {p.attrib["name"]: p.attrib["value"] for p in case.findall("./properties/property")}
        if "p90a_native_observation" not in props:
            continue
        row = json.loads(props["p90a_native_observation"])
        expected_amplitude, expected = amplitude_reference(row["family"], row["removed"], row["counts"])
        assert Fraction(row["expected_probability_exact"]) == expected
        amplitude = complex(*row["amplitude"])
        assert all(math.isfinite(v) for v in (amplitude.real, amplitude.imag, row["probability"]))
        assert row["error_repr"] is None and row["native_calls_planned"] == 1
        assert abs(complex(*row["expected_amplitude"])-expected_amplitude) <= 2e-12
        assert row["probability"] == abs(amplitude)**2
        probability_errors.append(abs(row["probability"]-float(expected)))
        amplitude_errors.append(abs(amplitude-expected_amplitude))
        assert probability_errors[-1] <= 2e-12 and amplitude_errors[-1] <= 2e-12
        assert row["abs_tolerance"] == 2e-12 and row["relative_tolerance"] == 0
        assert row["native_configured"] == row["native_after_imports"] == row["native_after"] == 1
        assert set(row["environment_after"].values()) == {"1"}
        assert row["provenance"]["versions"] == {key: value for key, value in spec["software"].items()
                                                   if key not in ("Python", "networkx")}
        assert row["provenance"]["spec_sha256"] == sha(root/"research/P90a_execution_spec.json")
        provenance = row["provenance"]
        if first_provenance is None:
            first_provenance = provenance
            pins = {item["role"]: item for item in spec["external_artifacts"]}
            assert provenance["python"]["sha256"] == pins["physical_interpreter"]["sha256"]
            for group, name, role in (
                ("critical_python", "naive", "deterministic_qualification_backend"),
                ("critical_python", "abstract", "backend_circuit_input_convention"),
                ("critical_python", "linalg", "eigvalsh_python"),
                ("critical_python", "matfuncs", "expm_python"),
                ("actual_native", "exqalibur", "native_extension"),
                ("actual_native", "linalg", "eigvalsh_native"),
                ("actual_native", "array", "array_native"),
                ("actual_native", "expm", "expm_native")):
                identity = provenance[group][name]
                assert identity["sha256"] == pins[role]["sha256"] == sha(identity["path"])
        else:
            assert provenance == first_provenance
        observations.append((row["family"], tuple(row["removed"]), tuple(row["counts"])))
        zero_count += expected == 0
        native_zero_count += row["probability"] == 0
    assert observations == planned_keys() and len(observations) == 254
    teardown = xml.findall(".//testsuite/properties/property[@name='p90a_native_teardown_readback']")
    assert len(teardown) == 1
    final = json.loads(teardown[0].attrib["value"])
    assert final["native_readback"] == {"value": 1, "error_repr": None}
    assert set(final["environment"].values()) == {"1"} and final["setup_error_repr"] is None
    return {"status": "PASS", "inspector_sha256": sha(__file__), "raw_seal_commit": raw_seal,
        "manifest_sha256": sha(run/"manifest.json"), "JUnit_sha256": sha(run/"junit.xml"),
        "passed_items": 283, "independently_recomputed_amplitudes_and_probabilities": 254,
        "zero_reference_points": zero_count, "literal_native_zero_points": native_zero_count,
        "max_absolute_amplitude_error": max(amplitude_errors),
        "max_absolute_probability_error": max(probability_errors),
        "input_hashes_checked": 18, "external_pins_checked": 18, "native_configuration": 1,
        "scope": "Sealed tiny deterministic records only; no scientific imports, native calls, RNG, DEV graph, main, TV or optimizer/hardware validation"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--raw-seal", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args.root.resolve(), args.raw_seal)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps(result, allow_nan=False))
