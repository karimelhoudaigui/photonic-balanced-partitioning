"""P37 exact source selection; Haar counting only, not full Fock simulation."""
import argparse
from fractions import Fraction as F
from functools import lru_cache
import json
import math
from pathlib import Path
import time

MODES = (8, 10, 12, 16, 24, 32, 48, 64)
ROOT_MODES = MODES + (128,)
LAMBDAS = tuple(F(i, 4) for i in (1, 3, 5, 7, 9, 11, 13, 15))
ETAS = (F(1, 4), F(1, 2), F(3, 4), F(9, 10), F(99, 100), F(1))


def encode(value):
    if isinstance(value, F):
        return {'numerator': str(value.numerator), 'denominator': str(value.denominator)}
    raise TypeError(type(value).__name__)


@lru_cache(None)
def h(m, photons):
    k = m // 2
    return (F(math.comb(m, k) * math.comb(photons-1, k-1),
              math.comb(m+photons-1, photons)) if photons >= k else F(0))


def mixture(m, photons, eta):
    return sum((math.comb(photons, l) * eta**l * (1-eta)**(photons-l) * h(m, l)
                for l in range(m//2, photons+1)), F(0))


def coefficient(m, photons, eta):
    k = m // 2
    return F(math.comb(m, k), math.comb(m+photons-1, photons)) * eta**k * sum(
        (math.comb(k+j-1, j) * math.comb(m+photons-k-j-1, photons-k-j)
         * (1-eta)**(photons-k-j) for j in range(photons-k+1)), F(0))


def bernstein(m, source, per_photon):
    n = source-1 if per_photon else source
    def value(l):
        return h(m, l) / l if per_photon and l else h(m, l)
    coefficients = [math.comb(n, r) * (value(r+2)-value(r+1) if per_photon
                                      else value(r+1)-value(r)) for r in range(n+1)]
    common = math.lcm(*(v.denominator for v in coefficients))
    integers = [int(v * common) for v in coefficients]
    signs = [int(v > 0)-int(v < 0) for v in integers if v]
    assert signs[0] == 1 and signs[-1] == -1
    assert sum(a != b for a, b in zip(signs, signs[1:])) == 1
    return integers, common


def polynomial_value(coefficients, eta):
    # Integer homogeneous Horner: sign equals the Bernstein expectation.
    a, b = eta.numerator, eta.denominator - eta.numerator
    q = coefficients[-1]
    power = 1
    for c in reversed(coefficients[:-1]):
        power *= b
        q = a*q + c*power
    return q


def transition(m, source, per_photon):
    coefficients, common = bernstein(m, source, per_photon)
    low, high = F(0), F(1)
    for _ in range(40):
        middle = (low+high)/2
        v = polynomial_value(coefficients, middle)
        if v > 0:
            low = middle
        elif v < 0:
            high = middle
        else:
            low = high = middle
            break
    def difference(eta):
        a, b = mixture(m, source+1, eta), mixture(m, source, eta)
        return a/(source+1)-b/source if per_photon else a-b
    dl, dh = difference(low), difference(high)
    assert 0 < low <= high < 1 and dl >= 0 >= dh
    assert (dl == 0) == (polynomial_value(coefficients, low) == 0)
    assert (dh == 0) == (polynomial_value(coefficients, high) == 0)
    return {'m': m, 'source': source, 'criterion': 'per_photon' if per_photon else 'per_attempt',
            'eta_low': low, 'eta_high': high, 'difference_low': dl, 'difference_high': dh,
            'scaled_loss_low': m*(1-high), 'scaled_loss_high': m*(1-low),
            'homogeneous_integer_coefficients': [str(c) for c in coefficients],
            'coefficient_denominator': str(common), 'bisections': 40}


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    grid, transitions = [], []
    progress = (output/'progress.jsonl').open('x')
    comparisons = 0
    for m in MODES:
        for eta in ETAS + tuple(1-lam/m for lam in LAMBDAS):
            values = []
            for n in range(m//2, m+1):
                probability = mixture(m, n, eta)
                assert probability == coefficient(m, n, eta)
                assert 0 < probability <= 1
                values.append({'source': n, 'probability': probability,
                               'per_photon': probability/n, 'waiting_photons_iid_haar': n/probability})
                comparisons += 1
            best_attempt = max(r['probability'] for r in values)
            best_photon = max(r['per_photon'] for r in values)
            maxima_a = [r['source'] for r in values if r['probability'] == best_attempt]
            maxima_b = [r['source'] for r in values if r['per_photon'] == best_photon]
            if eta < 1:
                assert set(maxima_a) <= {m-1, m}
                assert set(maxima_b) <= {m-3, m-2, m-1, m}
                predicted_a = [m] if values[-1]['probability'] > values[-2]['probability'] else [m-1]
                if values[-1]['probability'] == values[-2]['probability']:
                    predicted_a = [m-1, m]
                predicted_b = [m-3]
                for j in range(m-3, m):
                    diff = values[j+1-m//2]['per_photon']-values[j-m//2]['per_photon']
                    if diff > 0:
                        predicted_b = [j+1]
                    elif diff == 0:
                        predicted_b.append(j+1)
                    else:
                        break
                assert maxima_a == predicted_a and maxima_b == predicted_b
            else:
                assert maxima_a == [m-2, m-1] and maxima_b == [m-3]
            record = {'m': m, 'eta': eta, 'values': values,
                      'per_attempt_maximizers': maxima_a, 'per_photon_maximizers': maxima_b}
            grid.append(record)
            progress.write(json.dumps({'event': 'grid', **record}, default=encode)+'\n')
            progress.flush()
    for m in ROOT_MODES:
        current = [transition(m, m-1, False)] + [transition(m, j, True) for j in range(m-3, m)]
        # Per-photon roots strictly decrease with source count.
        assert all(b['eta_high'] < a['eta_low'] for a, b in zip(current[1:-1], current[2:]))
        transitions.extend(current)
        for record in current:
            progress.write(json.dumps({'event': 'transition', **record}, default=encode)+'\n')
        progress.flush()
    progress.close()
    summary = {'status': 'EXACT_FINITE_ASSERTIONS_PASS', 'grid_cells': len(grid),
               'source_probabilities_crosschecked': comparisons, 'transition_brackets': len(transitions),
               'bisection_steps': 40, 'physical_shots': 0, 'full_fock_circuits': 0,
               'runtime_seconds': time.monotonic()-start,
               'non_claims': ['No theorem follows from finite grid alone', 'No graph quality or optimization advantage',
                              'No novelty certificate', 'No fixed-device waiting-time inference']}
    assert len(grid) == 112 and comparisons == 1610 and len(transitions) == 36
    raw = {'summary': summary, 'grid': grid, 'transitions': transitions}
    (output/'raw.json').write_text(json.dumps(raw, default=encode, separators=(',', ':'))+'\n')
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    run(parser.parse_args().output)
