"""P41/R1 frozen finite discriminator, not an optimization benchmark.

Run only through the bounded computation-audit runner after committing the
contract and code. The parent coordinates the single numerical worker slot.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import expm
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq

SEEDS = (2026112401, 2026112402)
TIMES = (0., -.04, -.02, -.01, -.005, .005, .01, .02, .04)
TOLERANCE = 1e-10


def encode(z):
    return np.stack((np.asarray(z).real, np.asarray(z).imag), axis=-1).tolist()


def fock_basis(m, k):
    states = []
    for routing in itertools.combinations_with_replacement(range(m), k):
        state = [0] * m
        for i in routing:
            state[i] += 1
        states.append(tuple(state))
    return states


def bosonic_generator(h, states):
    """Independent second-quantized creation/annihilation construction."""
    index = {state: i for i, state in enumerate(states)}
    rows, cols, values = [], [], []
    for j, state in enumerate(states):
        for a, na in enumerate(state):
            if not na:
                continue
            for b in range(len(h)):
                if b == a:
                    value = h[a, a] * na
                    i = j
                else:
                    target = list(state)
                    target[a] -= 1
                    target[b] += 1
                    i = index[tuple(target)]
                    value = h[b, a] * math.sqrt(na * (state[b] + 1))
                if value:
                    rows.append(i); cols.append(j); values.append(value)
    return coo_matrix((values, (rows, cols)), shape=(len(states), len(states))).tocsr()


def labelled_probabilities(u, selected, states):
    """Labelled categorical routing DP; no permanent and no Fock amplitudes."""
    law = {(0,) * len(u): 1.}
    for a in selected:
        updated = {}
        for state, mass in law.items():
            for b in range(len(u)):
                target = list(state); target[b] += 1
                target = tuple(target)
                updated[target] = updated.get(target, 0.) + mass * abs(u[b, a])**2
        law = updated
    return np.asarray([law.get(state, 0.) for state in states])


def graph_frame(m, seed, phi):
    rng = np.random.default_rng(seed + m * 100)
    upper = .5 + rng.random((m, m))
    graph = np.triu(upper, 1)
    graph = graph + graph.T
    selected = tuple(sorted(rng.choice(m, m // 2, replace=False).tolist()))
    return graph, selected, graph_hamiltonian(graph, selected, phi)


def graph_hamiltonian(graph, selected, phi):
    x = np.zeros(len(graph)); x[list(selected)] = 1
    flip = (1 - 2*x) * (graph.sum(axis=1) - 2*graph@x)
    h = graph * np.exp(1j * phi * np.sign(flip[:, None] - flip[None, :]))
    h /= np.linalg.norm(h, 2)
    return h


def proxy(h, selected, t):
    occupied = list(selected)
    vacant = [b for b in range(len(h)) if b not in selected]
    a = h[np.ix_(vacant, occupied)]
    b = (h@h)[np.ix_(vacant, occupied)] / 2 + a @ h[np.ix_(occupied, occupied)]
    probabilities = t*t * abs(a - 1j*t*b)**2
    result = {tuple(selected): 1 - float(probabilities.sum())}
    for ib, vertex_b in enumerate(vacant):
        for ia, vertex_a in enumerate(occupied):
            target = tuple(sorted(set(selected) - {vertex_a} | {vertex_b}))
            result[target] = float(probabilities[ib, ia])
    return result


def cubic_exchange(h, selected):
    result = {}
    for a in selected:
        for b in range(len(h)):
            if b in selected:
                continue
            exchange = sum(h[b, i]*h[i, a] for i in selected if i != a)
            result[(a, b)] = float(2*np.imag(np.conj(h[b, a])*exchange))
    return result


def repaired(states, probabilities, selected):
    result = {tuple(selected): 0.}
    for state, p in zip(states, probabilities):
        target = tuple(i for i, number in enumerate(state) if number) if max(state) <= 1 else tuple(selected)
        result[target] = result.get(target, 0.) + float(p)
    return result


def tv(left, right):
    return sum(abs(left.get(s, 0.)-right.get(s, 0.)) for s in left.keys() | right.keys()) / 2


def cost(graph, selected):
    x = np.zeros(len(graph)); x[list(selected)] = 1
    return float(x@graph.sum(axis=1) - x@graph@x)


def gain(graph, initial, law):
    previous = cost(graph, initial)
    return sum(p * max(previous-cost(graph, target), 0.) for target, p in law.items())


def collision(states, probabilities):
    return float(sum(p for state, p in zip(states, probabilities) if max(state) > 1))


def triangle_control():
    h = np.zeros((4, 4), dtype=complex)
    h[0, 1] = h[1, 0] = h[1, 2] = h[2, 1] = 1
    h[2, 0], h[0, 2] = 1j, -1j
    actual = cubic_exchange(h, (0, 1))
    return {"coefficients": {f"{a}->{b}": value for (a, b), value in actual.items()},
            "expected_0_to_2": -2, "expected_1_to_2": 2,
            "pass": abs(actual[0, 2]+2) < TOLERANCE and abs(actual[1, 2]-2) < TOLERANCE}


def run(output):
    started = time.monotonic()
    output = Path(output)
    # The bounded runner owns this directory; data subdirectory remains fresh.
    data = output / "data"
    data.mkdir(parents=True, exist_ok=False)
    frames, cells, checks = [], [], []
    law_file = (data / "raw.jsonl").open("x")
    triangle = triangle_control()
    checks.append({"name": "hand_triangle_coefficients", "pass": triangle["pass"]})
    for m in (8, 10):
        k = m // 2
        states = fock_basis(m, k)
        solver = FixedPhotonObliq(m, k)
        solver_index = {state: i for i, state in enumerate(solver._enumerate_all_fock_states())}
        reindex = [solver_index[state] for state in states]
        state_index = {state: i for i, state in enumerate(states)}
        for seed in SEEDS:
            for phi in (0., math.pi/3):
                graph, selected, h = graph_frame(m, seed, phi)
                occupation = tuple(int(i in selected) for i in range(m))
                generator = bosonic_generator(h, states)
                initial = np.zeros(len(states), dtype=complex)
                initial[state_index[occupation]] = 1
                first = generator @ initial
                second = generator @ first
                cubic_b = np.imag(np.conj(first)*second)
                exchange = cubic_exchange(h, selected)
                h_squared = h@h
                cubic_errors = []
                for (a, b), predicted in exchange.items():
                    target = tuple(sorted(set(selected)-{a}|{b}))
                    target_state = tuple(int(i in target) for i in range(m))
                    cubic_d = float(np.imag(np.conj(h[b, a])*h_squared[b, a]))
                    cubic_errors.append(abs(cubic_b[state_index[target_state]]-cubic_d-predicted))
                fid = f"m{m}-s{seed}-phi{'0' if phi == 0 else 'pi3'}"
                frames.append({"id":fid,"m":m,"k":k,"seed":seed,"phi":phi,
                    "graph":graph.tolist(),"selected":selected,"h":encode(h),"fock_states":states,
                    "cubic_exchange":{f"{a}->{b}":value for (a,b),value in exchange.items()},
                    "cubic_coefficient_max_error":max(cubic_errors),
                    "cubic_exchange_sum":sum(exchange.values()),
                    "sparse_generator_hermitian_max_error":float(abs(generator-generator.conj().T).max()),
                    "fock_dimension":len(states),"nnz":generator.nnz})
                frame_laws = {}
                for t in TIMES:
                    u = expm(-1j*t*h)
                    psi_reference = expm_multiply(-1j*t*generator, initial)
                    psi_ryser = solver.output_state(u, input_occupation=occupation)[reindex]
                    full_b = abs(psi_ryser)**2
                    full_reference = abs(psi_reference)**2
                    full_d = labelled_probabilities(u, selected, states)
                    repaired_b = repaired(states, full_b, selected)
                    repaired_d = repaired(states, full_d, selected)
                    q = proxy(h, selected, t)
                    actual_tv = tv(repaired_b, q)
                    bound = math.exp(2*k*abs(t))*(2*k*abs(t))**4/48 + 9*k*t**4/4
                    pnorm_error = max(abs(full_b.sum()-1),abs(full_reference.sum()-1),abs(full_d.sum()-1))
                    err = float(max(abs(psi_reference-psi_ryser)))
                    cell = {"frame":fid,"t":t,"normalization_error":float(pnorm_error),
                            "fock_vs_ryser_amplitude_max_error":err,
                            "tv_repaired_boson_proxy":actual_tv,"tv_bound_unclipped":bound,
                            "tv_bound_clipped":min(1.,bound),"bound_informative":bound<1,
                            "tv_error_over_t4":actual_tv/(t**4) if t else None,
                            "proxy_min_mass":min(q.values()),"proxy_mass":sum(q.values()),
                            "collision_b":collision(states,full_b),"collision_d":collision(states,full_d),
                            "accepted_gain_b":gain(graph,selected,repaired_b),
                            "accepted_gain_d":gain(graph,selected,repaired_d),
                            "accepted_gain_classical_proxy":gain(graph,selected,q),
                            "cubic_coefficient_max_error":max(cubic_errors),
                            "pass":bool(pnorm_error<TOLERANCE and err<TOLERANCE and
                                max(cubic_errors)<TOLERANCE and min(q.values())>=0 and
                                abs(sum(q.values())-1)<TOLERANCE and actual_tv<=bound+TOLERANCE)}
                    cells.append(cell)
                    law_file.write(json.dumps(cell | {"full_bosonic_ryser":full_b.tolist(),
                        "full_bosonic_fock_reference":full_reference.tolist(),
                        "full_distinguishable":full_d.tolist(),
                        "proxy":[{"selected":s,"probability":p} for s,p in q.items()]})+"\n")
                    frame_laws[t] = (full_b,repaired_b,q)
                # H conjugation exactly reverses t; separate permanent reference.
                conjugate = solver.output_state(expm(-1j*.04*h.conj()),input_occupation=occupation)[reindex]
                conjugation_error = float(max(abs(abs(conjugate)**2-frame_laws[-.04][0])))
                perm = np.random.default_rng(seed+100000+m).permutation(m)
                inverse = np.argsort(perm)
                graph_p = graph[np.ix_(perm,perm)]
                selected_p = tuple(sorted(inverse[list(selected)].tolist()))
                h_p = graph_hamiltonian(graph_p,selected_p,phi)
                relabel_h_error = float(max(abs(h_p-h[np.ix_(perm,perm)]).flat))
                q_p = proxy(h_p,selected_p,.04)
                q_back = {tuple(sorted(perm[list(target)].tolist())):p for target,p in q_p.items()}
                relabel_proxy_tv = tv(q_back,frame_laws[.04][2])
                real_odd_error = tv(frame_laws[.04][1],frame_laws[-.04][1]) if phi == 0 else None
                checks.append({"name":fid,"conjugation_probability_error":conjugation_error,
                    "relabel_h_error":relabel_h_error,"relabel_proxy_tv":relabel_proxy_tv,
                    "real_time_reversal_tv":real_odd_error,
                    "pass":bool(conjugation_error<TOLERANCE and relabel_h_error<TOLERANCE
                                and relabel_proxy_tv<TOLERANCE
                                and (real_odd_error is None or real_odd_error<TOLERANCE))})
    law_file.close()
    (data/"frames.json").write_text(json.dumps(frames,indent=2)+"\n")
    summary = {"status":"PASS" if all(c["pass"] for c in cells+checks) else "FAIL",
        "assertion_tested":"See committed P41_adaptive_contract.json; local chiral proxy, not optimization advantage",
        "frame_count":len(frames),"cell_count":len(cells),"checks":checks,"triangle":triangle,
        "max_fock_ryser_amplitude_error":max(c["fock_vs_ryser_amplitude_max_error"] for c in cells),
        "max_cubic_coefficient_error":max(c["cubic_coefficient_max_error"] for c in cells),
        "max_proxy_tv_error":max(c["tv_repaired_boson_proxy"] for c in cells),
        "max_unclipped_bound":max(c["tv_bound_unclipped"] for c in cells),
        "all_bounds_informative":all(c["bound_informative"] for c in cells),
        "max_error_over_t4":max(c["tv_error_over_t4"] for c in cells if c["t"]),
        "failed_cells":[c for c in cells if not c["pass"]],
        "wall_seconds":time.monotonic()-started,"qpu_calls":0,"graph_training":False}
    (data/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary))
    return summary["status"] == "PASS"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    raise SystemExit(0 if run(args.output) else 1)
