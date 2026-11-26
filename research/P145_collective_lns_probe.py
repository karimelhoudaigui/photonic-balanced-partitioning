"""P145 CODE ONLY library; no DEV driver or execution authority.

Authoring base afbbddb9; ROOT design context 2fdf942. No scientific import,
fixture, graph, grid or RNG is evaluated at import. A separate frozen contract,
review and ROOT authority must precede qualification or a DEV invocation.
The three-in/six-mode boundary-field encoding is already in P142: no novelty
or optimizer advantage is claimed. Exact-law enumeration is a mandatory cheap
classical mirror; all costs used by validation must be credited to controls.
Optics below is floating exhaustive Fock enumeration, NOT an exact/interval
sign proof. Raw collisions/losses are never conditioned away or renormalized.
Graph generation, paid one-swap certificate, block selection, KL and run limits
belong to the separately reviewed ROOT driver, not this import-safe kernel.
"""
from itertools import combinations, permutations
from math import expm1, factorial, fsum, isfinite, log1p, sqrt
import os

TOL = 5e-11
ARMS = {"B": (0, 0, 0), "pair12": (0, 0, 1), "pair13": (0, 1, 0), "pair23": (0, 1, 1), "D": (0, 1, 2)}
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")


def require(condition, message):
    if not condition: raise ValueError(message)


def unitary_from_features(a, h, alpha, beta, t):
    """exp[-it(alpha*A + beta*diag(h))]; eigenvectors never initialize a cut."""
    require(all(isfinite(float(v)) for v in (alpha, beta, t)), "finite parameters")
    require(len(a) == len(h) == 6 and all(len(row) == 6 for row in a), "six-mode feature dimensions")
    require(all(isfinite(float(v)) for row in a for v in row) and all(isfinite(float(v)) for v in h) and
            all(a[i][j] == a[j][i] for i in range(6) for j in range(6)), "finite real symmetric graph features")
    require(all(os.environ.get(name) == "1" for name in THREADS), "contract must set all six thread variables before process startup")
    if float(t) == 0: return tuple(tuple(complex(i == j) for j in range(6)) for i in range(6))
    import numpy as np
    require(np.__version__ == "2.4.6", "pinned NumPy")
    generator = float(alpha)*np.array(a, dtype=float)+float(beta)*np.diag(np.array(h, dtype=float))
    eigenvalues, vectors = np.linalg.eigh(generator)
    result = (vectors*np.exp(-1j*float(t)*eigenvalues))@vectors.conj().T
    return tuple(tuple(complex(v) for v in row) for row in result)


def occupations(total, modes):
    if modes == 1: yield (total,)
    else:
        for first in range(total+1):
            for rest in occupations(total-first, modes-1): yield (first,)+rest


def permanent_dp(matrix):
    n = len(matrix); require(n <= 3 and all(len(row) == n for row in matrix), "permanent size0..3")
    values = {0: 1+0j}
    for row in matrix:
        following = {}
        for mask, value in values.items():
            for j, entry in enumerate(row):
                if not mask & (1 << j): following[mask | (1 << j)] = following.get(mask | (1 << j), 0j)+value*entry
        values = following
    return values[(1 << n)-1]


def _matrix(u):
    u = tuple(tuple(complex(z) for z in row) for row in u); m = len(u)
    require(1 <= m <= 6 and all(len(row) == m for row in u) and all(isfinite(z.real) and isfinite(z.imag) for row in u for z in row), "finite square unitary, <=6modes")
    residual = max(abs(sum(u[r][i].conjugate()*u[r][j] for r in range(m))-int(i == j)) for i in range(m) for j in range(m))
    require(residual <= TOL, "nonunitary input, no probability renormalization"); return u


def _canonical(tags):
    labels = {}; return tuple(labels.setdefault(x, len(labels)) for x in tags)


def _profile_law(u, source, tags, cache):
    tags = _canonical(tags); key = (u, source, tags)
    if key in cache: return cache[key]
    m = len(u); result = {(0,)*m: 1.0}
    for tag in dict.fromkeys(tags):
        inputs = tuple(source[j] for j, label in enumerate(tags) if label == tag); group = {}
        for n in occupations(len(inputs), m):
            rows = [j for j, count in enumerate(n) for unused in range(count)]
            amplitude = permanent_dp(tuple(tuple(u[j][a] for a in inputs) for j in rows)); divisor = 1
            for count in n: divisor *= factorial(count)
            group[n] = abs(amplitude)**2/divisor
        following = {}
        for left, p in result.items():
            for right, q in group.items():
                n = tuple(a+b for a, b in zip(left, right)); following[n] = following.get(n, 0.0)+p*q
        result = following
    cache[key] = result; return result


def fock_law(u, source, tags, transmission=1.0, cache=None):
    """All raw N<=K occupations, including zeros. Uniform input-mode loss.

    Each surviving source subset carries eta^l(1-eta)^(K-l); restricting its
    species labels preserves the full partial-distinguishability law. K3/m6
    returns84 bins even at eta1 (56 total3 bins and28 zero lower-sector bins).
    """
    u = _matrix(u); source, tags = tuple(source), tuple(tags); k, m = len(source), len(u); eta = float(transmission)
    require(k <= 3 and len(set(source)) == k and set(source) <= set(range(m)) and len(tags) == k and 0 <= eta <= 1 and isfinite(eta), "CF source/profile/transmission")
    result = {n: 0.0 for l in range(k+1) for n in occupations(l, m)}; cache = {} if cache is None else cache
    for l in range(k+1):
        weight = eta**l*(1-eta)**(k-l)
        if weight == 0: continue
        for survivors in combinations(range(k), l):
            law = _profile_law(u, tuple(source[j] for j in survivors), tuple(tags[j] for j in survivors), cache)
            for n, p in law.items(): result[n] += weight*p
    require(min(result.values()) >= 0 and abs(fsum(result.values())-1) <= TOL, "raw Fock mass; never condition/renormalize")
    return result


def direct_three_cycle(u, source, target):
    """Two oriented3cycles; structural identity exact, evaluation floating."""
    require(len(source) == 3 and len(target) == len(u) and all(type(n) is int and n >= 0 for n in target), "three-source cycle domain")
    if sum(target) != 3: return 0.0
    rows = [j for j, count in enumerate(target) for unused in range(count)]; paths = tuple(permutations(range(3))); amplitudes = {}
    for p in paths:
        value = 1+0j
        for j, row in enumerate(rows): value *= u[row][source[p[j]]]
        amplitudes[p] = value
    terms = [amplitudes[tuple(tau[r] for r in rho)]*amplitudes[rho].conjugate() for tau in ((1, 2, 0), (2, 0, 1)) for rho in paths]
    divisor = 1
    for count in target: divisor *= factorial(count)
    require(abs(fsum(z.imag for z in terms)) <= TOL, "three-cycle imaginary residual")
    return fsum(z.real for z in terms)/divisor


def same_circuit_scores(u, source, gains, transmission=1.0):
    """B/pair/D at ONE U. Do not apply this identity to independently selected maxima."""
    u = _matrix(u); require(len(u) == 6 and len(source) == 3, "P145 six-mode three-source domain")
    require(set(gains) == set(combinations(range(6), 3)) and all(v >= 0 and isfinite(float(v)) for v in gains.values()), "complete paid gain table")
    require(gains[tuple(sorted(source))] == 0, "current-source preparation is not an improvement")
    cache = {}; laws = {arm: fock_law(u, source, tags, transmission, cache) for arm, tags in ARMS.items()}
    score, hazard = {}, {}; direct = {}
    for arm, law in laws.items():
        score[arm] = fsum(p*float(gains[tuple(j for j, n in enumerate(out) if n)]) for out, p in law.items() if sum(out) == 3 and max(out) <= 1)
        hazard[arm] = fsum(p for out, p in law.items() if sum(out) == 3 and max(out) <= 1 and gains[tuple(j for j, n in enumerate(out) if n)] > 0)
    for out in laws["B"]:
        algebraic = laws["B"][out]-laws["pair12"][out]-laws["pair13"][out]-laws["pair23"][out]+2*laws["D"][out]
        direct[out] = float(transmission)**3*direct_three_cycle(u, source, out)
        require(abs(algebraic-direct[out]) <= TOL, "same-circuit irreducible3cycle identity")
    i3 = fsum(p*float(gains[tuple(j for j, n in enumerate(out) if n)]) for out, p in direct.items() if sum(out) == 3 and max(out) <= 1)
    bound = max(map(float, gains.values()), default=0); require(abs(i3-(score["B"]-score["pair12"]-score["pair13"]-score["pair23"]+2*score["D"])) <= TOL*(1+bound), "weighted3cycle identity")
    return {"laws": laws, "scores": score, "hazards": hazard, "same_circuit_I3_law": direct, "same_circuit_I3": i3,
            "I3_numeric_sign": "POSITIVE" if i3 > TOL*(1+bound) else "NEGATIVE" if i3 < -TOL*(1+bound) else "UNRESOLVED_NEAR_ZERO",
            "semantics": "FLOAT_EXHAUSTIVE_NOT_INTERVAL_OR_EXACT_SIGN_CERTIFICATE", "optimizer_advantage": False}


def validation_envelopes(evaluations):
    """Own first-tie grid maximum per arm; NO 'irreducible I3 of maxima'."""
    require(evaluations, "nonempty prospectively fixed grid")
    best = {arm: max(range(len(evaluations)), key=lambda i: evaluations[i]["scores"][arm]) for arm in ARMS}
    return {arm: {"grid_index": i, "score": evaluations[i]["scores"][arm], "hazard": evaluations[i]["hazards"][arm]} for arm, i in best.items()}


def feasible_mirror_kernel(law):
    """Classical20-CF-plus-FAIL law, needing ZERO cut queries. No postselection."""
    result = {y: law[tuple(int(j in y) for j in range(6))] for y in combinations(range(6), 3)}
    result["FAIL"] = fsum(p for n, p in law.items() if sum(n) != 3 or max(n) > 1)
    require(min(result.values()) >= 0 and abs(fsum(result.values())-1) <= TOL, "raw mirror probability mass")
    return result


def density_diagnostics(u, source, gain_bound):
    """P33 ideal-unitary FLOAT diagnostics only; never filter tiny positive rows.

    The same-U bounded gain error uses the ideal-law Phi estimate. A common
    uniform-loss/readout map contracts TV; this is not a retuned-arm bound.
    """
    u = _matrix(u); require(1 <= len(source) <= 3 and len(set(source)) == len(source) and set(source) <= set(range(len(u))) and gain_bound >= 0 and isfinite(float(gain_bound)), "diagnostic source/R domain")
    q = [[abs(row[a])**2 for a in source] for row in u]; intensities = [fsum(row) for row in q]
    c = min(x for x in intensities if x > 0); moment = 2*fsum(row[a]*row[b] for row in q for a, b in combinations(range(len(source)), 2))
    def phi(x):
        s = 2*sqrt(x)+x
        return 1.0 if s >= 1 else min(1.0, max(0.0, .5*expm1(-s-log1p(-s))))
    refined = moment/(c+sqrt(c*c-2*moment)) if moment < c*c/2 else None
    return {"c": c, "M": moment, "coarse_Phi": phi(moment/c), "refined_Phi": None if refined is None else phi(refined),
            "same_U_gain_bound_estimate": float(gain_bound)*phi(moment/c), "R_current_cut": gain_bound,
            "semantics": "FLOAT_DIAGNOSTIC_NOT_CERTIFICATE_NO_INTENSITY_CUTOFF", "not_a_retuned_envelope_bound": True}


if __name__ == "__main__":
    raise SystemExit("CODE ONLY library: no DEV contract/driver/authority in this file")
