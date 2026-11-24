"""Exact loss-spectrum certificates and bounded optical checks, not QPU data.

Only the CLI creates fresh result files. The calculator assumes identical
photons, fresh independent uniform loss and complete output-support detection.
Costs are explicit deterministic bounds, never inferred from provider shots.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json
import math
from pathlib import Path
import time

MAX_PHOTONS = 12
ETA_GRID = (Q(0), Q(1, 50), Q(1, 10), Q(1, 5), Q(1, 4), Q(1, 2), Q(1))


def natural(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def eta_exact(value):
    if type(value) not in (int, Q) or not 0 <= value <= 1:
        raise ValueError("eta must be an exact Fraction/integer in [0,1]")
    return Q(value)


def spectra(source):
    """Integer eigenvalue coefficients after loss of a product Fock source.

    For sector ell, each input remainder t<=source contributes eigenvalue
    prod binom(source_i,t_i)*eta**ell*(1-eta)**(N-ell).
    At N<=12 there are at most2**12 remainders, including bunched sources.
    """
    source = tuple(source)
    if not source or len(source) > 24:
        raise ValueError("Expected 1..24 source modes")
    for n in source:
        natural(n, "source occupation")
    total = sum(source)
    if total > MAX_PHOTONS:
        raise ValueError("Source exceeds the registered 12-photon calculation cap")
    sectors = defaultdict(Counter)
    for remaining in product(*(range(n+1) for n in source)):
        coefficient = math.prod(math.comb(n, r) for n, r in zip(source, remaining))
        sectors[sum(remaining)][coefficient] += 1
    assert all(sum(c*count for c, count in terms.items()) == math.comb(total, ell)
               for ell, terms in sectors.items())
    return total, dict(sectors)


def largest_sum(coefficients, rank):
    total = 0
    for coefficient, multiplicity in sorted(coefficients.items(), reverse=True):
        take = min(rank, multiplicity)
        total += take*coefficient
        rank -= take
        if not rank:
            break
    return total


def support_cap(source, eta, k, *, pnr_only=False, internal="identical"):
    """Ky Fan upper bound for one specified k-mode clicked support.

    Includes all ell>=k sectors for threshold; exact total=k for PNR-only.
    No photon bunching, sector, or loss event is silently normalized away.
    """
    eta = eta_exact(eta)
    natural(k, "support size", 1)
    if internal not in ("identical", "arbitrary"):
        raise ValueError("Internal-state model must be declared")
    total, sector_data = spectra(source)
    answer = Q(0)
    for ell, coefficients in sector_data.items():
        if ell < k or (pnr_only and ell != k):
            continue
        if internal == "identical":
            rank = 1 if pnr_only else math.comb(ell-1, k-1)
        else:
            rank = sum((-1)**j*math.comb(k,j)*(k-j)**ell for j in range(k+1))
        answer += largest_sum(coefficients, rank)*eta**ell*(1-eta)**(total-ell)
    assert 0 <= answer <= 1
    return answer


def budget_certificate(cap, k, n_quantum, n_classical):
    natural(k, "k", 2)
    natural(n_quantum, "quantum attempt ceiling")
    natural(n_classical, "guaranteed classical draws")
    if type(cap) not in (int, Q) or not 0 <= cap <= 1:
        raise ValueError("cap must be an exact probability upper bound")
    ratio = ((n_quantum+n_classical-1)//n_classical) if n_classical else None
    certified = n_quantum == 0 or (ratio is not None and ratio*math.comb(2*k, k)*cap <= 1)
    return {"certified_under_stated_model": bool(certified), "k": k,
            "n_quantum_upper": n_quantum, "n_classical_guaranteed": n_classical,
            "ceil_attempt_ratio": ratio, "support_cap": str(cap),
            "test_value": str(ratio*math.comb(2*k, k)*cap) if ratio is not None else None,
            "physical_device_parameters_verified": False, "qpu_gate_opened": False}


def partitions(n, maximum=None):
    if n == 0:
        yield ()
    else:
        for first in range(min(n, maximum or n), 0, -1):
            for rest in partitions(n-first, first):
                yield (first,)+rest


def exact_table():
    rows = []
    for k in range(2, 13):
        for total in range(k, 13):
            source = (1,)*total
            for eta in ETA_GRID:
                threshold = support_cap(source, eta, k)
                pnr = support_cap(source, eta, k, pnr_only=True)
                unknown_internal = support_cap(source, eta, k, internal="arbitrary")
                assert threshold <= unknown_internal
                assert pnr == eta**k*(1-eta)**(total-k)
                coefficients = sum(Q(min(math.comb(total, ell), math.comb(ell-1, k-1)))
                                   * eta**ell*(1-eta)**(total-ell)
                                   for ell in range(k, total+1))
                assert threshold == coefficients
                if eta < 1:
                    assert threshold <= (eta/(1-eta))**k
                if eta <= Q(1, 5):
                    assert math.comb(2*k, k)*threshold <= 1
                rows.append({"k": k, "N": total, "eta": str(eta),
                    "threshold_cap": str(threshold), "pnr_cap": str(pnr),
                    "arbitrary_internal_cap":str(unknown_internal),
                    "certificates": [budget_certificate(threshold, k, 1000*ratio, 1000)
                                     for ratio in (1, 1000, 1_000_000)]})
    return rows


def source_extension():
    rows = []
    for total in range(2, 13):
        for source in partitions(total):
            for k in range(2, min(total, 12)+1):
                eta = Q(1, 50)
                cap = support_cap(source, eta, k)
                unknown_internal = support_cap(source, eta, k, internal="arbitrary")
                survival = sum(Q(math.comb(total, ell))*eta**ell*(1-eta)**(total-ell)
                               for ell in range(k, total+1))
                assert cap <= survival
                assert cap <= unknown_internal <= survival
                if len(source) == 1:
                    assert cap == survival
                rows.append({"source": source, "k": k, "eta": str(eta),
                             "cap": str(cap), "survival_upper": str(survival),
                             "arbitrary_internal_cap":str(unknown_internal),
                             "certificate": budget_certificate(cap, k, 1000, 1000)})
    return rows


def optical_checks():
    """Compare a full Ryser law + loss with loss before the interferometer.

    This float64 validation is separate from the exact certificate table.
    No model/account client is imported, and all outcome sectors are retained.
    """
    import numpy as np
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
    from photonic_balanced_partitioning.noise import apply_independent_loss
    rows = []
    for m, source in ((4, (1,1,1,0)), (4, (2,1,0,0)), (6, (1,1,1,1,0,0)),
                      (4, (4,0,0,0))):
        total, sector_data = spectra(source)
        for seed in (2026112451, 2026112452):
            rng = np.random.default_rng(seed)
            raw = rng.normal(size=(m,m))+1j*rng.normal(size=(m,m))
            unitary, r = np.linalg.qr(raw)
            unitary = unitary@np.diag(np.diag(r)/abs(np.diag(r)))
            full = FixedPhotonObliq(m, total)
            states = full._enumerate_all_fock_states()
            law = dict(zip(states, abs(full.output_state(unitary, source))**2))
            for eta in (Q(1,50), Q(1,5), Q(1,2), Q(1)):
                after = apply_independent_loss(law, float(eta))
                before = defaultdict(float)
                for remaining in product(*(range(n+1) for n in source)):
                    ell = sum(remaining)
                    weight = math.prod(math.comb(n,t) for n,t in zip(source, remaining))
                    weight *= float(eta**ell*(1-eta)**(total-ell))
                    model = FixedPhotonObliq(m, ell)
                    for state, probability in zip(model._enumerate_all_fock_states(),
                                                  abs(model.output_state(unitary, remaining))**2):
                        before[state] += weight*float(probability)
                difference = max(abs(after.get(state,0)-before.get(state,0))
                                 for state in after.keys() | before.keys())
                assert difference < 1e-10
                for k in range(2, min(total, m)+1):
                    grouped = defaultdict(float)
                    for state, probability in after.items():
                        support = tuple(i for i,n in enumerate(state) if n)
                        if len(support) == k:
                            grouped[support] += probability
                    cap = support_cap(source, eta, k)
                    assert all(p <= float(cap)+1e-10 for p in grouped.values())
                    rows.append({"m":m, "source":source, "seed":seed, "k":k,
                        "eta":str(eta), "full_law_total":sum(after.values()),
                        "loss_commutation_max_error":difference,
                        "support_cap":str(cap), "support_probabilities":
                            [{"support":s, "probability":p} for s,p in sorted(grouped.items())]})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.process_time()
    table, general, physical = exact_table(), source_extension(), optical_checks()
    # A bunched source refutes extending the single-input spectrum unmodified.
    eta = Q(1,10)
    bunched = 1-2*(1-eta/2)**4+(1-eta)**4
    singles_bound = support_cap((1,1,1,1), eta, 2)
    assert bunched > singles_bound
    partial_eta = Q(1,100)
    partial_lower = Q(7,6)*partial_eta**4*(1-partial_eta)**4
    wrong_identical_envelope = (partial_eta/(1-partial_eta))**4
    assert partial_lower > wrong_identical_envelope
    output = {"certificate_table":table, "arbitrary_fock_sources":general,
              "optical_checks":physical, "source_assumption_counterexample":
              {"source": [4,0,0,0], "beam_splitter": "balanced into two modes",
               "eta":str(eta), "actual_two_clicks":str(bunched),
               "inapplicable_single_input_bound":str(singles_bound)},
              "internal_state_assumption_counterexample":
              {"source":"eight single inputs, two internal species in six-mode block plus two spectators",
               "eta":str(partial_eta), "physical_four_click_lower":str(partial_lower),
               "inapplicable_identical_envelope":str(wrong_identical_envelope),
               "ordered_rank_cap":str(support_cap((1,)*8,partial_eta,4,internal="arbitrary"))}}
    with (args.output/"raw.json").open("x") as stream:
        json.dump(output,stream,indent=2);stream.write("\n")
    summary = {"result":"REGISTERED_FINITE_ASSERTIONS_PASS", "exact_grid_rows":len(table),
               "arbitrary_source_rows":len(general), "optical_rows":len(physical),
               "cpu_seconds":time.process_time()-started, "qpu_calls":0,
               "actual_hardware_efficiency_inferred":False,
               "mathematical_scope":"Stated source/loss/rank and finite-cost model; no ideal universal no-go"}
    with (args.output/"summary.json").open("x") as stream:
        json.dump(summary,stream,indent=2);stream.write("\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
