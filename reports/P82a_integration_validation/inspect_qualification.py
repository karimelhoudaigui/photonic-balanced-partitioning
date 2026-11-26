"""Inspect sealed P82a qualification records; no scientific package imports."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])


def times(a, b):
    return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])


def independent_probability(row):
    if row["kind"] == "HOM":
        return F(0) if row["occupation"] == [1, 1] else F(1, 2)
    phase = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0))][row["phase_id"]]
    one, neg = (F(1), F(0)), (F(-1), F(0))
    minus_phase = (-phase[0], -phase[1])
    unscaled = [[one, one, one, one], [one, neg, phase, minus_phase],
                [one, one, neg, neg], [one, neg, minus_phase, phase]]
    selected = [j for j, count in enumerate(row["occupation"]) for _ in range(count)]
    assert len(selected) == 2
    a, b = row["source"]
    u, v = selected
    amp = plus(times(unscaled[u][a], unscaled[v][b]),
               times(unscaled[u][b], unscaled[v][a]))
    return (amp[0]**2 + amp[1]**2)/(16*math.prod(math.factorial(c) for c in row["occupation"]))


def inspect(root):
    run = root / "research/P82a_dev_veto_preflight/run_001"
    manifest = json.loads((run / "manifest.json").read_text())
    spec = json.loads((root / "research/P82a_execution_spec.json").read_text())
    contract = json.loads((root / "research/P82a_split_scatter_preflight_contract.json").read_text())
    assert manifest["repository"] == {"commit": "94f80b94f75317524c202ce9ef5bf932d78ddc5e", "dirty": False}
    assert manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0
    assert not manifest["run"]["missing_results"] and not manifest["run"]["invalid_results"]
    assert all(check["passed"] for check in manifest["checks"])
    assert manifest["execution_artifacts"] == contract["execution_artifacts"]
    assert len(manifest["input_artifacts"]) == 15
    for item in manifest["input_artifacts"]:
        assert sha(root / item["path"]) == item["sha256"] == item["sha256_after"]
    for item in manifest["outputs"]:
        assert sha(root / item["path"]) == item["sha256"]
    for item in spec["external_artifacts"]:
        assert sha(item["path"]) == item["sha256"]
    xml = ET.parse(run / "junit.xml")
    cases = xml.findall(".//testcase")
    assert len(cases) == 27
    assert not xml.findall(".//failure") and not xml.findall(".//error") and not xml.findall(".//skipped")
    declared = [part.split("::", 1)[1] for part in manifest["command"] if "::" in part]
    assert [case.attrib["name"] for case in cases] == declared
    native = next(case for case in cases if case.attrib["name"].startswith("test_native_183"))
    properties = {p.attrib["name"]: p.attrib["value"] for p in native.findall("./properties/property")}
    for name in ("planned", "attempted", "actual"):
        assert int(properties[f"P82a_native_{name}_queries"]) == 183
    assert json.loads(properties["P82a_native_errors"]) == []
    records = json.loads(properties["P82a_native_observations"])
    assert len(records) == 183 and [r["query"] for r in records] == list(range(183))
    keys = [(r["kind"], r["phase_id"], tuple(r["source"]), tuple(r["occupation"])) for r in records]
    assert len(set(keys)) == 183
    assert sum(r["kind"] == "HOM" for r in records) == 3
    assert [sum(r["kind"] == "r2" and r["phase_id"] == j for r in records) for j in range(3)] == [60]*3
    errors, zero_references, literal_zeros = [], 0, 0
    for row in records:
        expected = independent_probability(row)
        assert expected == F(row["expected_fraction"])
        amplitude = complex(row["amplitude_real"], row["amplitude_imag"])
        observed = row["probability"]
        assert all(math.isfinite(v) for v in (amplitude.real, amplitude.imag, observed))
        assert observed == abs(amplitude)**2
        errors.append(abs(observed - float(expected)))
        assert errors[-1] <= 2e-12
        zero_references += expected == 0
        literal_zeros += observed == 0
    threads = json.loads(properties["P82a_native_threads"])
    assert all(threads[name] == 1 for name in ("configured", "after_import", "after_queries"))
    assert all(set(threads[name].values()) == {"1"} for name in ("environment_configured", "environment_after_queries"))
    provenance_case = cases[0]
    provenance = json.loads(provenance_case.find("./properties/property[@name='P82a_external_provenance']").attrib["value"])
    assert not provenance["errors"] and all(row["match"] for row in provenance["critical_python_sources"])
    native_pin = next(item["sha256"] for item in spec["external_artifacts"] if item["role"] == "native_extension")
    assert provenance["native_extension"]["sha256"] == native_pin
    return {"status": "PASS", "inspector_sha256": sha(__file__), "raw_seal_commit": "8e6ba06645954a0113b8d473eaf4648c7dbf4221",
            "manifest_sha256": sha(run / "manifest.json"), "JUnit_sha256": sha(run / "junit.xml"),
            "passed_nodes": 27, "independently_recomputed_probabilities": 183,
            "max_absolute_probability_error": max(errors), "zero_reference_points": zero_references,
            "literal_native_zero_points": literal_zeros, "input_hashes_checked": 15,
            "external_pins_checked": len(spec["external_artifacts"]),
            "observed_native_configuration": 1, "runner_wall_seconds": manifest["run"]["runtime_seconds"],
            "scope": "Recorded deterministic qualification only; no new native calls, RNG, DEV data, optimizer or hardware validation"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = inspect(args.root)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps(result, allow_nan=False))
