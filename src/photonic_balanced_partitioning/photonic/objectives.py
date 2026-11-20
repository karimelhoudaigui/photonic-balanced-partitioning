"""Collision-aware statistics, objectives, and shot uncertainty.

Probabilities are per ideal physical attempt (before collision rejection).
Intervals describe independent binomial sampling of a *fixed* circuit, not
uncertainty from variational training or hardware losses.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import NormalDist
from typing import Sequence
import math
import numpy as np


@dataclass(frozen=True)
class DistributionMetrics:
    p_cf: float
    p_success: float
    p_opt_given_cf: float
    conditional_energy: float
    unconditional_cf_energy: float
    expected_shots: float


def _distribution(probabilities: Sequence[float]) -> np.ndarray:
    p = np.asarray(probabilities, dtype=float)
    if p.ndim != 1 or not np.all(np.isfinite(p)) or np.any(p < -1e-14):
        raise ValueError("probabilities must be a finite nonnegative vector")
    p = np.maximum(p, 0.0)
    if not np.isclose(p.sum(), 1.0, atol=1e-9, rtol=1e-9):
        raise ValueError("probabilities must sum to one; do not silently renormalize")
    return p


def cut_energies(occupations: Sequence[Sequence[int]], edges) -> np.ndarray:
    x = np.asarray(occupations)
    if x.ndim != 2:
        raise ValueError("occupations must be a matrix")
    result = np.zeros(len(x), dtype=float)
    for i, j, weight in edges:
        result += float(weight) * (x[:, i] != x[:, j])
    return result


def distribution_metrics(probabilities, occupations, edges, optimal_energy=None) -> DistributionMetrics:
    """Evaluate a normalized full Fock distribution; undefined conditionals are NaN.

    If optimal_energy is omitted the balanced classical optimum is enumerated
    from the collision-free support rows. This is an exact oracle diagnostic,
    not a hardware-accessible training objective.
    """
    p = _distribution(probabilities)
    states = np.asarray(occupations)
    if states.ndim != 2 or len(states) != len(p):
        raise ValueError("occupations and probabilities must have the same length")
    cf = np.all((states == 0) | (states == 1), axis=1)
    if not np.all(np.sum(states, axis=1) == np.sum(states[0])):
        raise ValueError("fixed-particle metrics require one total photon number")
    costs = cut_energies(states[cf], edges)
    p_cf = float(np.sum(p[cf]))
    energy = float(np.dot(p[cf], costs))
    if optimal_energy is None:
        optimal_energy = float(np.min(costs)) if len(costs) else math.inf
    optimal = np.isclose(costs, optimal_energy, atol=1e-10, rtol=0)
    p_success = float(np.sum(p[cf][optimal]))
    return DistributionMetrics(
        p_cf=p_cf,
        p_success=p_success,
        p_opt_given_cf=p_success / p_cf if p_cf > 1e-14 else math.nan,
        conditional_energy=energy / p_cf if p_cf > 1e-14 else math.inf,
        unconditional_cf_energy=energy,
        expected_shots=1.0 / p_success if p_success > 0 else math.inf,
    )


def objective_value(metrics: DistributionMetrics, name="conditional_energy", *, mu=1.0,
                    gamma=1.0, epsilon=1e-12) -> float:
    """Minimization losses; success/factorized require an optimum oracle.

    The log barrier has the sign E_CF - gamma*log(P_CF + epsilon).
    CVaR needs the distribution and is provided by conditional_cvar().
    """
    if mu < 0 or gamma < 0 or epsilon <= 0:
        raise ValueError("mu/gamma must be nonnegative and epsilon positive")
    if name in ("conditional", "conditional_energy"):
        return metrics.conditional_energy
    if name in ("success", "physical_success"):
        return -metrics.p_success
    if name == "factorized":
        return -metrics.p_cf * metrics.p_opt_given_cf if metrics.p_cf > 1e-14 else 0.0
    if name in ("collision_aware", "collision_aware_energy"):
        return metrics.conditional_energy + mu * (1.0 - metrics.p_cf)
    if name in ("log_barrier", "barrier"):
        return metrics.conditional_energy - gamma * math.log(metrics.p_cf + epsilon)
    if name in ("p_cf", "collision_free"):
        return -metrics.p_cf
    if name in ("p_opt_given_cf", "conditional_success"):
        return -metrics.p_opt_given_cf if metrics.p_cf > 1e-14 else math.inf
    raise ValueError(f"unknown objective {name!r}")


def weighted_lower_cvar(energies, probabilities=None, alpha=0.1) -> float:
    """Mean of lowest alpha probability mass; splits an atom at the quantile.

    Input weights may be unnormalized (e.g. collision-free probabilities).
    Empty/no-mass distributions return +inf, so rejection cannot improve loss.
    """
    if not np.isfinite(alpha) or not 0 < alpha <= 1:
        raise ValueError("alpha must lie in (0, 1]")
    values = np.asarray(energies, dtype=float)
    if values.ndim != 1 or not np.all(np.isfinite(values)):
        raise ValueError("energies must be a finite vector")
    if len(values) == 0:
        return math.inf
    p = np.ones(len(values), dtype=float) if probabilities is None else np.asarray(probabilities, dtype=float)
    if p.shape != values.shape or np.any(p < 0) or not np.all(np.isfinite(p)):
        raise ValueError("weights must be finite, nonnegative, and match energies")
    if p.sum() <= 1e-14:
        return math.inf
    order = np.argsort(values, kind="stable")
    weights = p[order] / p.sum()
    previous = np.cumsum(weights) - weights
    consumed = np.minimum(weights, np.maximum(alpha - previous, 0.0))
    return float(np.dot(values[order], consumed) / alpha)


def conditional_cvar(probabilities, occupations, edges, alpha=0.1) -> float:
    p = _distribution(probabilities)
    states = np.asarray(occupations)
    if states.ndim != 2 or len(states) != len(p):
        raise ValueError("occupations and probabilities must have the same length")
    cf = np.all((states == 0) | (states == 1), axis=1)
    return weighted_lower_cvar(cut_energies(states[cf], edges), p[cf], alpha)


def wilson_interval(successes: int, shots: int, confidence=0.95) -> tuple[float, float]:
    """Wilson score interval for an independent binomial success count."""
    if not isinstance(shots, (int, np.integer)) or shots <= 0:
        raise ValueError("shots must be a positive integer")
    if not isinstance(successes, (int, np.integer)) or not 0 <= successes <= shots:
        raise ValueError("successes must be an integer between zero and shots")
    if not 0 < confidence < 1:
        raise ValueError("confidence must lie in (0, 1)")
    z = NormalDist().inv_cdf(0.5 + confidence / 2)
    phat = successes / shots
    denominator = 1 + z*z/shots
    center = (phat + z*z/(2*shots)) / denominator
    half = z * math.sqrt(phat*(1-phat)/shots + z*z/(4*shots*shots)) / denominator
    # Endpoint clipping avoids an artificial finite upper shot bound at s=0.
    return (0.0 if successes == 0 else max(0.0, center-half),
            1.0 if successes == shots else min(1.0, center+half))


def expected_shots_interval(successes: int, shots: int, confidence=0.95) -> tuple[float, float]:
    lo, hi = wilson_interval(successes, shots, confidence)
    return (1.0 / hi, 1.0 / lo if lo > 0 else math.inf)
