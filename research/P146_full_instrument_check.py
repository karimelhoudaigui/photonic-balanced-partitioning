"""P146 bounded qualification: complete mediator instrument, not an optimizer.

Exact Q(i) arithmetic for the optical dilation, D control and weighted purge.
Floating arithmetic only for a dyadic angle identity and local Perceval audit.
All 36 bosonic outputs, including zero records and environment labels, retained.
"""
from __future__ import annotations

import argparse
import cmath
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import traceback


@dataclass(frozen=True)
class G:
    re: F = F(0)
    im: F = F(0)

    def __add__(self, other):
        other = as_g(other)
        return G(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, other):
        return self + -as_g(other)

    def __mul__(self, other):
        other = as_g(other)
        return G(self.re*other.re-self.im*other.im,
                 self.re*other.im+self.im*other.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_g(other)
        num = self * other.conj()
        return G(num.re/other.norm(), num.im/other.norm())

    def conj(self):
        return G(self.re, -self.im)

    def norm(self):
        return self.re*self.re + self.im*self.im

    def __complex__(self):
        return complex(float(self.re), float(self.im))


def as_g(x):
    return x if isinstance(x, G) else G(F(x))


I = G(F(0), F(1))
ONE = G(F(1))
ZERO = G()
PHASES = (ONE, I, G(F(3, 5), F(4, 5)))
# s is survival AMPLITUDE; eta=s^2 is per-photon survival PROBABILITY.
LOSS_AMPLITUDES = ((F(1), F(0)), (F(399, 401), F(40, 401)),
                   (F(112, 113), F(15, 113)))
LOGICAL = tuple(product((0, 1), repeat=2))
CONTEXT = {}


def serial(x):
    if isinstance(x, F):
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, G):
        return {"re": serial(x.re), "im": serial(x.im)}
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def h4(z):
    return [[as_g(x)/2 for x in row] for row in
            ((1, 1, 1, 1), (1, z, -1, -z),
             (1, -1, 1, -1), (1, -z, -1, z))]


def dilation(z, s, loss):
    h = h4(z)
    return [[s*h[r][c] if r < 4 and c < 4 else
             -loss*h[r][c-4] if r < 4 else
             as_g(loss*int(r-4 == c)) if c < 4 else
             as_g(s*int(r == c)) for c in range(8)] for r in range(8)]


def occupations(modes):
    for j in range(modes):
        for k in range(j, modes):
            yield tuple(int(r == j)+int(r == k) for r in range(modes))


def boson_branches(v):
    for n in occupations(8):
        rows = [r for r, count in enumerate(n) for _ in range(count)]
        j, k = rows
        amps = []
        for x, y in LOGICAL:
            a, b = 2*x, 1+2*y
            amps.append(v[j][a]*v[k][b] + v[j][b]*v[k][a])
        yield {"n": n, "divisor": 2 if j == k else 1, "amplitudes": amps}


def determinant(a):
    n = len(a)
    out = ZERO
    for p in permutations(range(n)):
        sign = (-1)**sum(p[j] > p[k] for j in range(n) for k in range(j+1, n))
        term = as_g(sign)
        for j in range(n):
            term *= a[j][p[j]]
        out += term
    return out


def ppt_minors(rho):
    pt = [[rho[2*x+v][2*u+y] for u, v in LOGICAL] for x, y in LOGICAL]
    return [determinant([[pt[j][k] for k in ids] for j in ids])
            for size in range(1, 5) for ids in combinations(range(4), size)]


def check_exact_optics(records, checks):
    for z, (s, loss) in product(PHASES, LOSS_AMPLITUDES):
        assert s*s+loss*loss == 1
        v = dilation(z, s, loss)
        records.append({"kind": "optics_input", "z": z, "s": s, "loss": loss, "V": v})
        for c, d in product(range(8), repeat=2):
            gram = sum((v[r][c].conj()*v[r][d] for r in range(8)), ZERO)
            CONTEXT.update(stage="Gram", z=z, s=s, columns=[c, d], actual=gram)
            assert gram == as_g(c == d)
        branches = list(boson_branches(v))
        totals = [[F(0) for _ in LOGICAL] for _ in range(3)]
        h = h4(z)
        for branch in branches:
            n, div, amps = branch["n"], branch["divisor"], branch["amplitudes"]
            records.append({"kind": "boson", "z": z, "s": s, **branch})
            CONTEXT.clear()
            CONTEXT.update(stage="boson", z=z, s=s, branch=branch)
            detected = sum(n[:4])
            for xy, amp in enumerate(amps):
                totals[detected][xy] += amp.norm()/div
            if detected == 2:
                ports = [j for j, count in enumerate(n[:4]) for _ in range(count)]
                j, k = ports
                for xy, (x, y) in enumerate(LOGICAL):
                    if j == k:
                        expected = 2*h[j][2*x]*h[j][1+2*y]
                    elif (j, k) in ((0, 2), (1, 3)):
                        expected = ZERO
                    else:
                        even, odd = (j, k) if j % 2 == 0 else (k, j)
                        bj = (ONE, z, -ONE, -z)[even]
                        bk = (ONE, z, -ONE, -z)[odd]
                        expected = (bj*(-1)**x + bk*(-1)**y)/4
                    assert amps[xy] == s*s*expected
                if z == I and any(a.norm() for a in amps):
                    assert all(a.norm()/div == s**4/F(8) for a in amps)
                if z == ONE and j != k and any(a.norm() for a in amps):
                    assert sum(a.norm() != 0 for a in amps) == 2
            elif detected == 1:
                port = next(j for j in range(4) if n[j])
                env = next(j-4 for j in range(4, 8) if n[j])
                for xy, (x, y) in enumerate(LOGICAL):
                    expected = s*loss*(h[port][1+2*y]*int(env == 2*x)
                                      + h[port][2*x]*int(env == 1+2*y))
                    assert amps[xy] == expected
            else:
                for xy, (x, y) in enumerate(LOGICAL):
                    expected = as_g(loss*loss*int(n[4+2*x] == n[5+2*y] == 1))
                    assert amps[xy] == expected
        eta = s*s
        CONTEXT.update(stage="loss_masses", totals=totals, eta=eta)
        assert totals == [[(1-eta)**2]*4, [2*eta*(1-eta)]*4, [eta*eta]*4]
        # Distinguishable labels are traced, never coherently erased at detection.
        coarse = {}
        for j, k in product(range(8), repeat=2):
            amps = [v[j][2*x]*v[k][1+2*y] for x, y in LOGICAL]
            records.append({"kind": "D_label_resolved", "z": z, "s": s,
                            "ordered_outputs": [j, k], "amplitudes": amps})
            CONTEXT.update(stage="D_factorization", outputs=[j, k], amplitudes=amps)
            assert amps[0]*amps[3] == amps[1]*amps[2]
            n = tuple(int(r == j)+int(r == k) for r in range(8))
            obs = n[:4]
            rho = coarse.setdefault(obs, [[ZERO]*4 for _ in range(4)])
            for a, b in product(range(4), repeat=2):
                rho[a][b] += amps[a]*amps[b].conj()/4
        dmass = ZERO
        for obs, rho in coarse.items():
            minors = ppt_minors(rho)
            CONTEXT.update(stage="D_PPT", observed=obs, rho=rho, minors=minors)
            assert all(x.im == 0 and x.re >= 0 for x in minors)
            dmass += sum((rho[j][j] for j in range(4)), ZERO)
        assert dmass == ONE
        checks.append({"kind": "optics", "z": z, "s": s, "eta": eta,
                       "boson_fine_branches": len(branches),
                       "observed_records": len(coarse), "D_fine_branches": 64,
                       "loss_masses": totals, "D_PPT_all_principal_minors": True})
    # B entanglement is a resource witness, not an optimization score.
    b = next(b for b in boson_branches(dilation(I, F(1), F(0)))
             if b["n"][:4] == (1, 1, 0, 0))
    amps, div = b["amplitudes"], b["divisor"]
    mass = sum(a.norm() for a in amps)/(4*div)
    rho = [[a*b.conj()/(4*div*mass) for b in amps] for a in amps]
    det_pt = ppt_minors(rho)[-1]
    CONTEXT.clear()
    CONTEXT.update(stage="B_CZ_witness", rho=rho, det_pt=det_pt)
    assert det_pt == G(-F(1, 16))
    checks.append({"kind": "B_CZ_resource_witness", "branch_probability": mass,
                   "normalized_partial_transpose_determinant": det_pt})


def phase_value(bitstring, edges):
    out = ONE
    for u, v, phase in edges:
        out *= phase if bitstring[u] == bitstring[v] else phase.conj()
    return out


def check_purge(checks):
    # Five data qubits: cycle built, chord(0,2) missing; max target degree3.
    q = G(F(3, 5), F(4, 5))
    t = G(F(5, 13), F(12, 13))
    built = ((0, 1, q), (1, 2, t), (2, 3, q), (3, 4, t), (0, 4, q))
    kept = (1, 3, 4)
    cases = 0
    branches = [b for b in boson_branches(dilation(I, *LOSS_AMPLITUDES[1]))
                if sum(b["n"][:4]) < 2]
    # Loss in nativeCZ1 or nativeCZ2, after zero/one temporary wrong phase.
    for second_gate, previous_wrong, branch, measured in product(
            (False, True), (False, True), branches, product((0, 1), repeat=3)):
        ancilla_bit, bit_u, bit_v = measured
        a = branch["amplitudes"][2*ancilla_bit+(bit_v if second_gate else bit_u)]
        actual, expected = [], []
        for values in product((0, 1), repeat=3):
            bits = [bit_u, values[0], bit_v, values[1], values[2]]
            original = phase_value(bits, built)
            temp = phase_value(bits, ((0, 2, t.conj()),)) if previous_wrong else ONE
            cz = (-1)**(ancilla_bit*bit_u) if second_gate else 1
            actual.append(original*temp*cz*a*(F(3, 5) if ancilla_bit == 0 else F(4, 5)))
            # Induced graph PLUS explicitly retained known neighbor rotations.
            remain = phase_value(bits, tuple(e for e in built if e[0] in kept and e[1] in kept))
            neighbors = phase_value(bits, tuple(e for e in built if (e[0] in kept) != (e[1] in kept)))
            expected.append(remain*neighbors)
        CONTEXT.clear()
        CONTEXT.update(stage="purge", second_gate=second_gate,
                       previous_wrong=previous_wrong, branch=branch,
                       measured=measured, actual=actual, expected=expected)
        assert all(actual[j]*expected[0] == actual[0]*expected[j] for j in range(8))
        cases += 1
    # Negative control: H on the discarded center of CZ01 CZ02 creates parity.
    after_h_z0 = [1+(-1)**(x+y) for x, y in LOGICAL]
    assert after_h_z0 == [2, 0, 0, 2]
    checks.append({"kind": "weighted_purge", "fine_branch_and_Z_cases": cases,
                   "loss_branches_per_gate": len(branches),
                   "data_qubits": 5, "ancilla_qubits": 1,
                   "non_diagonal_counterexample": after_h_z0,
                   "non_claim": "Known offline resource only; no arbitrary-state repair"})


def check_phases_and_resources(checks):
    # Derive K from ancilla amplitudes and two diagonal CZs, using exact Q(i).
    c, s = F(3, 5), F(4, 5)
    for parity in (-1, 1):
        for ysign in (-1, 1):
            unnormalized_k = as_g(c) - I*ysign*s*parity
            CONTEXT.clear()
            CONTEXT.update(stage="phase_ancilla", parity=parity,
                           ysign=ysign, k=unnormalized_k)
            assert unnormalized_k.norm() == 1  # omitted common1/sqrt2
    for m in range(1, 9):
        theta = math.pi/(2**(m+1))
        errors = []
        for k in range(1, m+1):
            for final_sign in ((1, -1) if k == m else (1,)):
                angle = -(2**(k-1)-1)*theta + final_sign*2**(k-1)*theta
                if final_sign == -1:
                    angle += math.pi/2
                error = max(abs(cmath.exp(1j*parity*angle)-cmath.exp(1j*parity*theta))
                            for parity in (-1, 1))
                CONTEXT.update(stage="dyadic_sign", m=m, k=k,
                               final_sign=final_sign, angle=angle, error=error)
                assert math.isfinite(error) and error < 1e-12
                errors.append(error)
        checks.append({"kind": "dyadic_sign_compiler", "m": m,
                       "terminating_histories": len(errors), "errors": errors,
                       "two_CZ_per_stage": True})
    for (amp, _), cap, m in product(LOSS_AMPLITUDES, (4, 8), (1, 2, 4)):
        tau = amp**4
        p = tau/2
        # Independent finite native stopping distribution:success/loss/timeout.
        law = [(j, "success", p**j) for j in range(1, cap+1)]
        law += [(j, "loss", p**(j-1)*(1-tau)) for j in range(1, cap+1)]
        law += [(cap, "timeout", p**cap)]
        CONTEXT.clear()
        CONTEXT.update(stage="resource_law", amplitude=amp, cap=cap, m=m, law=law)
        assert sum(x[2] for x in law) == 1
        r = sum(prob for _, status, prob in law if status == "success")
        c = sum(j*prob for j, _, prob in law)
        assert r == tau/(2-tau)*(1-p**cap)
        assert c == (1-p**cap)/(1-p)
        a = r*r
        # Recursion directly over phase stages, contrasted to closed form.
        success, work = a, c*(1+r)
        for _ in range(m-1):
            success = a/2*(1+success)
            work = c*(1+r)+a/2*work
        q = a/2
        formula = sum((q**k for k in range(1, m)), F(0))+2*q**m
        work_formula = c*(1+r)*sum((q**j for j in range(m)), F(0))
        CONTEXT.update(stage="resource_recursion", success=success, formula=formula,
                       work=work, work_formula=work_formula)
        assert success == formula and work == work_formula
        delta = success-4*(1-success)  # max target degree3
        checks.append({"kind": "capped_resource", "survival_amplitude": amp,
                       "eta": amp*amp, "R": cap, "m": m, "success": success,
                       "expected_microattempts": work, "Delta": 3, "delta": delta,
                       "positive_drift": delta > 0,
                       "expected_photons_per_edge_upper_bound": 2*work/delta if delta > 0 else None})


def check_native(records, checks):
    import exqalibur as xq
    xq.Config.compute_max_thread_count = 1
    import perceval as pcvl
    from perceval.backends import NaiveBackend
    for s, loss in LOSS_AMPLITUDES:
        v = dilation(I, s, loss)
        circuit = pcvl.Circuit(8).add(0, pcvl.Unitary(pcvl.Matrix(
            [[complex(x) for x in row] for row in v])))
        backend = NaiveBackend()
        backend.set_circuit(circuit)
        exact = list(boson_branches(v))
        for xy, (x, y) in enumerate(LOGICAL):
            incoming = [0]*8
            incoming[2*x] = incoming[1+2*y] = 1
            backend.set_input_state(pcvl.BasicState(incoming))
            for branch in exact:
                expected = complex(branch["amplitudes"][xy])/math.sqrt(branch["divisor"])
                actual = complex(backend.prob_amplitude(pcvl.BasicState(branch["n"])))
                error = abs(expected-actual)
                finite = all(math.isfinite(t) for t in (actual.real, actual.imag,
                             expected.real, expected.imag, error))
                # Preserve offending nonfinite point as strings BEFORE any assertion.
                records.append({"kind": "native", "s": s, "logical": [x, y],
                                "n": branch["n"], "expected": repr(expected),
                                "actual": repr(actual), "error": repr(error), "finite": finite})
                assert finite and error < 1e-12
                assert int(xq.Config.compute_max_thread_count) == 1
    checks.append({"kind": "Perceval_Naive", "native_amplitudes": 432,
                   "all_loss_environment_outputs_included": True, "threads": 1})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError("Assertions must remain enabled")
    root = Path(args.output)
    root.mkdir(parents=True, exist_ok=False)
    records, checks = [], []
    failure = None
    try:
        check_exact_optics(records, checks)
        check_purge(checks)
        check_phases_and_resources(checks)
        check_native(records, checks)
    except BaseException as exc:
        failure = {"type": type(exc).__name__, "message": str(exc),
                   "traceback": traceback.format_exc(), "context": dict(CONTEXT)}
        raise
    finally:
        outputs = {"records.json": records, "checks.json": checks, "failure.json": failure}
        encoded = {name: json.dumps(serial(value), indent=2, allow_nan=False)+"\n"
                   for name, value in outputs.items()}
        total = sum(len(x.encode()) for x in encoded.values())
        over = total > 3*1024*1024
        if over:
            # A failed, explicitly truncated receipt survives a serialization cap.
            previous = ({key: str(failure.get(key, ""))[:16384]
                         for key in ("type", "message", "traceback")} if failure else None)
            failure = {"type": "ScientificOutputLimit", "original_failure": previous,
                       "serialized_bytes": total, "record_count": len(records),
                       "check_count": len(checks), "raw_prefix_only": True}
            outputs = {"failure.json": failure,
                       "records.json": {"truncated": True, "prefix": records[:1]},
                       "checks.json": {"truncated": True, "prefix": checks[:1]}}
            encoded = {name: json.dumps(serial(value), indent=2, allow_nan=False)+"\n"
                       for name, value in outputs.items()}
        for name, value in encoded.items():
            (root/name).write_text(value)
        if over:
            raise RuntimeError("Scientific output cap exceeded; bounded failure prefix preserved")


if __name__ == "__main__":
    main()
