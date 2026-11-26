"""Eight prospective hand tests; NO import/collection/execution before review.
No DEV graph/seed is used. A skipped Perceval test leaves its validation gate
unmet. F3 is known interference physics, not graph optimization or novelty.
"""
import cmath
import importlib.util
from importlib import metadata
from itertools import combinations
import json
from math import comb, factorial, fsum, isfinite, pi, sqrt
from pathlib import Path
import sys
import pytest


@pytest.fixture(scope="module")
def probe():
    path = Path(__file__).resolve().parents[1]/"research/P145_collective_lns_probe.py"
    spec = importlib.util.spec_from_file_location("p145_hand_library", path)
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module
    spec.loader.exec_module(module); return module


def identity(n): return tuple(tuple(complex(i == j) for j in range(n)) for i in range(n))
def dft(n, modes=6):
    return tuple(tuple(cmath.exp(2j*pi*i*j/n)/sqrt(n) if i < n and j < n else complex(i == j) for j in range(modes)) for i in range(modes))
def zero_gains(): return {y: 0 for y in combinations(range(6), 3)}


def test_hom_factorials_distinguishability_and_vacuum(probe):
    u = ((1/sqrt(2), 1/sqrt(2)), (1/sqrt(2), -1/sqrt(2)))
    b = probe.fock_law(u, (0, 1), (0, 0)); d = probe.fock_law(u, (0, 1), (0, 1))
    assert probe.permanent_dp(()) == 1 and probe.permanent_dp(((1, 2), (3, 4))) == 10
    assert (b[(2, 0)], b[(1, 1)], b[(0, 2)]) == pytest.approx((.5, 0, .5))
    assert (d[(2, 0)], d[(1, 1)], d[(0, 2)]) == pytest.approx((.25, .5, .25))
    assert probe.fock_law(((1,),), (), ()) == {(0,): 1.0}


def test_all_profiles_uniform_loss_raw_sectors_and_zeros(probe):
    for tags in probe.ARMS.values():
        law = probe.fock_law(identity(6), (0, 1, 2), tags, .8)
        assert len(law) == 84 and fsum(law.values()) == pytest.approx(1)
        for k in range(4): assert fsum(p for n, p in law.items() if sum(n) == k) == pytest.approx(comb(3, k)*.8**k*.2**(3-k))
        assert law[(1, 1, 1, 0, 0, 0)] == pytest.approx(.8**3)
        assert probe.fock_law(identity(6), (0, 1, 2), tags, 0)[(0,)*6] == 1


def test_known_tritter_connected_cycles_do_not_imply_gain(probe):
    result = probe.same_circuit_scores(dft(3), (0, 1, 2), zero_gains()); n = (1, 1, 1, 0, 0, 0)
    expected = {"B": 1/3, "D": 2/9, "pair12": 1/9, "pair13": 1/9, "pair23": 1/9}
    for arm, p in expected.items(): assert result["laws"][arm][n] == pytest.approx(p)
    assert result["same_circuit_I3_law"][n] == pytest.approx(4/9)
    assert fsum(result["same_circuit_I3_law"].values()) == pytest.approx(0, abs=1e-12)
    assert min(result["same_circuit_I3_law"].values()) < 0
    assert result["same_circuit_I3"] == 0 and result["I3_numeric_sign"] == "UNRESOLVED_NEAR_ZERO"


def test_uniform_loss_preserves_only_eta_cubed_three_cycle(probe):
    ideal = probe.same_circuit_scores(dft(3), (0, 1, 2), zero_gains())
    lossy = probe.same_circuit_scores(dft(3), (0, 1, 2), zero_gains(), .8)
    for n, value in lossy["same_circuit_I3_law"].items():
        assert value == pytest.approx(.8**3*ideal["same_circuit_I3_law"][n], abs=1e-12)
        if sum(n) < 3: assert value == 0


def test_retuning_is_per_arm_first_tie_and_never_i3(probe):
    rows = [{"scores": dict(B=1, pair12=2, pair13=.5, pair23=.8, D=1), "hazards": dict.fromkeys(probe.ARMS, .1)},
            {"scores": dict(B=2, pair12=1, pair13=4, pair23=.8, D=1), "hazards": dict.fromkeys(probe.ARMS, .1)}]
    best = probe.validation_envelopes(rows)
    assert {a: r["grid_index"] for a, r in best.items()} == dict(B=1, pair12=0, pair13=1, pair23=0, D=0)
    assert all("same_circuit_I3" not in r for r in best.values())


def test_feature_exponential_and_p33_are_float_diagnostics(probe, monkeypatch):
    for name in probe.THREADS: monkeypatch.setenv(name, "1")
    a = [[0]*6 for unused in range(6)]; h = (1, -2, 3, -4, 5, -6)
    assert probe.unitary_from_features(a, h, 1, 1, 0) == identity(6)
    u = probe.unitary_from_features(a, h, 1, 1, .5)
    for i in range(6):
        for j in range(6): assert u[i][j] == pytest.approx(cmath.exp(-.5j*h[i]) if i == j else 0, abs=1e-12)
    tiny = [list(row) for row in identity(6)]; r = 1e-12; tiny[0][3], tiny[3][0] = -r, r
    diag = probe.density_diagnostics(tiny, (0, 1, 2), 10)
    assert 0 < diag["c"] < 1e-20 and diag["M"] == 0 and "NOT_CERTIFICATE" in diag["semantics"]
    with pytest.raises(ValueError, match="nonunitary"): probe.fock_law(((1, 1), (0, 1)), (0,), (0,))


def test_exact_law_mirror_keeps_loss_collision_fail(probe):
    law = probe.fock_law(dft(3), (0, 1, 2), probe.ARMS["B"], .8); kernel = probe.feasible_mirror_kernel(law)
    assert len(kernel) == 21 and fsum(kernel.values()) == pytest.approx(1)
    assert kernel[(0, 1, 2)] == pytest.approx(.8**3/3) and kernel["FAIL"] == pytest.approx(1-.8**3/3)


def test_independent_perceval_literal_dft6_all56(probe, record_property):
    try: versions = {name: metadata.version(name) for name in ("perceval-quandela", "exqalibur")}
    except metadata.PackageNotFoundError: pytest.skip("Perceval absent: native qualification gate NOT MET")
    assert versions == {"perceval-quandela": "1.3.0", "exqalibur": "1.4.2"}
    import exqalibur as xq
    xq.Config.compute_max_thread_count = 1
    import perceval as pcvl
    from perceval.backends import NaiveBackend
    u = dft(6); actual = probe.fock_law(u, (0, 1, 2), (0, 0, 0)); raw = []
    assert int(xq.Config.compute_max_thread_count) == 1
    backend = NaiveBackend(); backend.set_circuit(pcvl.Circuit(6).add(0, pcvl.Unitary(pcvl.Matrix([list(row) for row in u])))); backend.set_input_state(pcvl.BasicState([1, 1, 1, 0, 0, 0]))
    try:
        for n in probe.occupations(3, 6):
            assert int(xq.Config.compute_max_thread_count) == 1
            reference = complex(backend.prob_amplitude(pcvl.BasicState(n))); rows = [j for j, count in enumerate(n) for unused in range(count)]; divisor = 1
            for count in n: divisor *= factorial(count)
            amplitude = probe.permanent_dp(tuple(tuple(u[j][a] for a in (0, 1, 2)) for j in rows))/sqrt(divisor)
            values = {"ours": actual[n], "reference_real": reference.real, "reference_imag": reference.imag,
                      "amplitude_real": amplitude.real, "amplitude_imag": amplitude.imag,
                      "prob_error": abs(actual[n]-abs(reference)**2), "amp_error": abs(amplitude-reference)}
            finite = all(isfinite(value) for value in values.values())
            raw.append({"n": n, "finite": finite, **{key: value if isfinite(value) else repr(value) for key, value in values.items()}})
            assert finite, "Nonfinite native/model amplitude or error; offending point preserved in P145_native_raw"
            assert int(xq.Config.compute_max_thread_count) == 1
    finally:
        record_property("P145_native_raw", json.dumps(raw, allow_nan=False)); record_property("P145_native_points", len(raw)); record_property("P145_native_threads", int(xq.Config.compute_max_thread_count))
    assert len(raw) == 56 and all(r["finite"] for r in raw) and max(r["prob_error"] for r in raw) < 1e-10 and max(r["amp_error"] for r in raw) < 1e-10
