"""Audit the frozen P41/R1 calculation, without repeating its campaign."""
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "research/P41_adaptive_runs/run001"


@pytest.fixture(scope="module")
def evidence():
    frames = json.loads((RUN / "data/frames.json").read_text())
    rows = [json.loads(line) for line in (RUN / "data/raw.jsonl").read_text().splitlines()]
    return {f["id"]: f for f in frames}, rows


def test_population_is_the_registered_cartesian_product(evidence):
    frames, rows = evidence
    assert len(frames) == 8 and len(rows) == 72
    expected = {(m, seed, phase) for m in (8, 10)
                for seed in (2026112401, 2026112402) for phase in (0., math.pi/3)}
    assert {(f["m"], f["seed"], f["phi"]) for f in frames.values()} == expected
    times = {0., -.04, -.02, -.01, -.005, .005, .01, .02, .04}
    assert {(row["frame"], row["t"]) for row in rows} == set(itertools.product(frames, times))


def test_complete_laws_and_independent_fock_reference(evidence):
    frames, rows = evidence
    for frame in frames.values():
        states = list(map(tuple, frame["fock_states"]))
        m, k = frame["m"], frame["k"]
        assert len(states) == len(set(states)) == math.comb(m+k-1, k)
        assert all(len(s) == m and sum(s) == k and min(s) >= 0 for s in states)
        assert any(max(s) > 1 for s in states)
    for row in rows:
        size = len(frames[row["frame"]]["fock_states"])
        laws = [np.asarray(row[name]) for name in
                ("full_bosonic_ryser", "full_bosonic_fock_reference", "full_distinguishable")]
        assert all(law.shape == (size,) and min(law) >= 0 and abs(sum(law)-1) < 1e-10 for law in laws)
        assert np.max(abs(laws[0]-laws[1])) < 1e-10


def test_positive_proxy_and_tv_bound_from_saved_laws(evidence):
    frames, rows = evidence
    for row in rows:
        frame = frames[row["frame"]]
        anchor = tuple(frame["selected"])
        repaired = {anchor: 0.}
        # Recompute independently from the full archived physical probabilities.
        for state, probability in zip(frame["fock_states"], row["full_bosonic_fock_reference"]):
            selected = tuple(i for i, n in enumerate(state) if n) if max(state) <= 1 else anchor
            repaired[selected] = repaired.get(selected, 0.) + probability
        proxy = {tuple(record["selected"]): record["probability"] for record in row["proxy"]}
        assert min(proxy.values()) >= 0 and sum(proxy.values()) == pytest.approx(1, abs=1e-13)
        measured = sum(abs(repaired.get(s, 0.)-proxy.get(s, 0.)) for s in repaired.keys() | proxy.keys())/2
        t, k = abs(row["t"]), frame["k"]
        bound = math.exp(2*k*t)*(2*k*t)**4/48 + 9*k*t**4/4
        assert bound < 1
        assert measured == pytest.approx(row["tv_repaired_boson_proxy"], abs=1e-13)
        assert measured <= bound+1e-12


def test_hand_triangle_exchange_sign_from_two_photon_amplitudes():
    h = np.zeros((4, 4), complex)
    h[0,1] = h[1,0] = h[1,2] = h[2,1] = 1
    h[2,0], h[0,2] = 1j, -1j
    coefficients = (np.eye(4, dtype=complex), -1j*h, -(h@h)/2)
    def routing_coefficients(rows, columns):
        return [sum(coefficients[j][rows[0],columns[0]]*
                    coefficients[d-j][rows[1],columns[1]]
                    for j in range(d+1)) for d in range(3)]
    def probability_cubic(amplitude):
        return float(2*np.real(np.conj(amplitude[1])*amplitude[2]))
    for rows, expected in (((1, 2), -2.), ((0, 2), 2.)):
        direct = routing_coefficients(rows, (0, 1))
        swapped = routing_coefficients(rows, (1, 0))
        bosonic = probability_cubic(np.asarray(direct)+np.asarray(swapped))
        labelled = probability_cubic(direct)+probability_cubic(swapped)
        assert bosonic-labelled == expected


def test_record_hashes_target_the_committed_inputs_and_outputs():
    manifest = json.loads((RUN / "manifest.json").read_text())
    assert manifest["schema_version"] == 2 and manifest["run"]["status"] == "completed"
    for item in manifest["input_artifacts"]:
        assert hashlib.sha256((ROOT/item["path"]).read_bytes()).hexdigest() == item["sha256"]
        assert item["sha256"] == item["sha256_after"]
    for item in manifest["outputs"]:
        assert hashlib.sha256((ROOT/item["path"]).read_bytes()).hexdigest() == item["sha256"]
