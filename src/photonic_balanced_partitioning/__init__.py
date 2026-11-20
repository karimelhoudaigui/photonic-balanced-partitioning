"""Photonic Balanced Partitioning - Constraint-Preserving Photonic Quantum Optimization."""

__version__ = "0.1.0"

from .cli import main
from .problems.min_bisection import BalancedGraphPartitioning, solve_exact_min_bisection
from .photonic import FixedPhotonObliq, CollisionAwareSolver, PenaltyObliq, CVaRFixedPhoton

__all__ = [
    "main",
    "__version__",
    "BalancedGraphPartitioning",
    "solve_exact_min_bisection",
    "FixedPhotonObliq",
    "CollisionAwareSolver",
    "PenaltyObliq",
    "CVaRFixedPhoton",
]