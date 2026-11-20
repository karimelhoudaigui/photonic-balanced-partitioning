"""Full binary penalty baselines.

This module does not implement the ObliQ optical dynamics. The historical
``PenaltyObliq`` name is retained only as a warning-emitting compatibility
alias. Comparisons must label this model ``classical_product_bernoulli``.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import math
import warnings
import numpy as np
from scipy.special import expit, logsumexp
from scipy.optimize import minimize
from .objectives import cut_energies


@dataclass(frozen=True)
class PenaltyObliqResult:
    occupation_numbers: tuple[int, ...]
    is_valid: bool
    is_balanced: bool
    energy: float
    partition: tuple[int, ...]
    penalty: float
    total: float


class PenaltyProductBernoulli:
    """Independent-bit sampler over {0,1}^n, trained on penalized expectation.

    ``params`` are n real logits, not a photonic unitary. All 2**n outcomes,
    including empty/full/unbalanced strings, retain support for finite logits.
    Enumeration is exponential; this is a small-instance reference baseline.
    """
    model_name = "classical_product_bernoulli"

    def __init__(self, n: int, k: int | None = None, lam: float = 10.0):
        if not isinstance(n, (int, np.integer)) or n <= 0:
            raise ValueError("n must be a positive integer")
        self.n = int(n)
        self.k = n//2 if k is None else k
        if not isinstance(self.k, (int, np.integer)) or not 0 <= self.k <= n:
            raise ValueError("k must be an integer between zero and n")
        if not np.isfinite(lam) or lam < 0:
            raise ValueError("lambda must be finite and nonnegative")
        self.lam = float(lam)
        self.bitstrings = np.array(list(product((0, 1), repeat=n)), dtype=int)
        self.feasible = self.bitstrings.sum(axis=1) == self.k

    def _partition(self, partition):
        values = tuple(partition)
        if len(set(values)) != len(values) or any(not isinstance(i, (int, np.integer)) or i < 0 or i >= self.n for i in values):
            raise ValueError("partition must contain distinct vertex indices")
        return values

    def compute_penalty(self, partition) -> float:
        return self.lam * (len(self._partition(partition))-self.k)**2

    def compute_total_energy(self, partition, edges) -> float:
        part = set(self._partition(partition))
        cut = sum(float(w) for i,j,w in edges if (i in part) != (j in part))
        return cut + self.compute_penalty(tuple(part))

    def cut_energies(self, edges) -> np.ndarray:
        return cut_energies(self.bitstrings, edges)

    def energies(self, edges) -> np.ndarray:
        return self.cut_energies(edges) + self.lam * (self.bitstrings.sum(axis=1)-self.k)**2

    def probabilities(self, params) -> np.ndarray:
        params = np.asarray(params, dtype=float)
        if params.shape != (self.n,) or not np.all(np.isfinite(params)):
            raise ValueError("params must be n finite logits, not a photonic matrix")
        # Stable log probabilities, avoiding products that underflow for small
        # reference instances; finite saturation is documented and keeps support.
        q = np.clip(expit(params), 1e-12, 1-1e-12)
        logp = self.bitstrings @ np.log(q) + (1-self.bitstrings) @ np.log1p(-q)
        return np.exp(logp-logsumexp(logp))

    def expected_energy(self, params, edges) -> float:
        return float(np.dot(self.probabilities(params), self.energies(edges)))

    def metrics(self, params, edges, optimal_energy=None) -> dict:
        p = self.probabilities(params)
        cut = self.cut_energies(edges)
        if optimal_energy is None:
            optimal_energy = float(np.min(cut[self.feasible]))
        optimal = self.feasible & np.isclose(cut, optimal_energy, atol=1e-10, rtol=0)
        ps = float(p[optimal].sum())
        pf = float(p[self.feasible].sum())
        return {"p_feasible":pf, "p_success":ps,
                "p_opt_given_feasible":ps/pf if pf else math.nan,
                "conditional_energy":float(np.dot(p[self.feasible],cut[self.feasible])/pf) if pf else math.inf,
                "penalized_energy":float(np.dot(p,self.energies(edges))),
                "expected_shots":1/ps if ps else math.inf,
                "model":self.model_name}

    def qubo_coefficients(self, edges) -> dict:
        """Return QUBO in offset + sum h_i x_i + sum_{i<j} J_ij x_i x_j convention.

        Cancellation at lambda=w_ij can remove a coupling; density is measured,
        never presumed dense solely from the penalty term.
        """
        linear = np.full(self.n, self.lam*(1-2*self.k), dtype=float)
        pair = np.full((self.n,self.n), 2*self.lam, dtype=float)
        pair = np.triu(pair,1)
        for i,j,w in edges:
            if i == j:
                continue
            if not 0 <= i < self.n or not 0 <= j < self.n or not np.isfinite(w):
                raise ValueError("invalid weighted edge")
            i,j = min(i,j),max(i,j)
            linear[i] += w
            linear[j] += w
            pair[i,j] -= 2*w
        nonzero = np.concatenate((linear[np.abs(linear)>1e-12],pair[np.abs(pair)>1e-12]))
        absolute = np.abs(nonzero)
        possible = self.n*(self.n-1)//2
        return {"offset":self.lam*self.k**2, "linear":linear,
                "quadratic":pair,
                "coupling_count":int(np.count_nonzero(np.abs(pair)>1e-12)),
                "coupling_density":float(np.count_nonzero(np.abs(pair)>1e-12)/possible) if possible else 0.0,
                "coefficient_min":float(nonzero.min()) if len(nonzero) else 0.0,
                "coefficient_max":float(nonzero.max()) if len(nonzero) else 0.0,
                "coefficient_abs_range":float(absolute.max()/absolute.min()) if len(absolute) else 0.0,
                "obliq_circuit_depth":None}

    def gibbs_probabilities(self, edges, beta=1.0) -> np.ndarray:
        """Exact enumerated Gibbs diagnostic, not an efficient sampler claim."""
        if not np.isfinite(beta) or beta < 0:
            raise ValueError("beta must be finite and nonnegative")
        logp = -beta*self.energies(edges)
        return np.exp(logp-logsumexp(logp))

    def sample(self, params, num_shots: int, edges, seed=None) -> list[PenaltyObliqResult]:
        if not isinstance(num_shots, (int,np.integer)) or num_shots < 0:
            raise ValueError("num_shots must be a nonnegative integer")
        rng = np.random.default_rng(seed)
        p = self.probabilities(params)
        costs, total = self.cut_energies(edges),self.energies(edges)
        draws = rng.choice(len(p),size=num_shots,p=p)
        results = []
        for index in draws:
            x = self.bitstrings[index]
            part = tuple(np.flatnonzero(x).tolist())
            valid = bool(self.feasible[index])
            results.append(PenaltyObliqResult(tuple(x.tolist()),valid,valid,
                float(costs[index]),part,self.compute_penalty(part),float(total[index])))
        return results

    def optimize(self, edges, num_iterations=100, seed=None, *, initial_params=None,
                 method="COBYLA", shots_per_evaluation=0) -> dict:
        """Budget-capped training (at most num_iterations objective calls).

        Nonzero shots_per_evaluation uses full binary multinomial shots in every
        objective call, charging all infeasible outcomes. Reporting diagnostics
        are exact and are not used to pick parameters.
        """
        if not isinstance(num_iterations,(int,np.integer)) or num_iterations < 1:
            raise ValueError("num_iterations must be a positive evaluation budget")
        if not isinstance(shots_per_evaluation,(int,np.integer)) or shots_per_evaluation < 0:
            raise ValueError("shots_per_evaluation must be nonnegative integer")
        rng = np.random.default_rng(seed)
        initial = rng.normal(0,0.25,self.n) if initial_params is None else np.asarray(initial_params,dtype=float)
        self.probabilities(initial)
        costs = self.energies(edges)
        trace, parameters = [], []
        best_value, best_params = math.inf, initial.copy()
        class BudgetReached(Exception):
            pass
        def fun(theta):
            nonlocal best_value,best_params
            if len(trace) >= num_iterations:
                raise BudgetReached
            p = self.probabilities(theta)
            value = (float(np.dot(rng.multinomial(shots_per_evaluation,p),costs)/shots_per_evaluation)
                     if shots_per_evaluation else float(np.dot(p,costs)))
            trace.append(value)
            parameters.append(np.asarray(theta).copy())
            if value < best_value:
                best_value,best_params = value,np.asarray(theta).copy()
            return value
        if method == "random":
            fun(initial)
            for _ in range(num_iterations-1):
                fun(rng.normal(0,2,self.n))
        else:
            if method not in ("COBYLA","Nelder-Mead"):
                raise ValueError("supported methods: COBYLA, Nelder-Mead, random")
            options = {"maxiter":num_iterations} if method == "COBYLA" else {"maxfev":num_iterations,"maxiter":num_iterations}
            try:
                minimize(fun,initial,method=method,options=options)
            except BudgetReached:
                pass
            # If optimizer converges early, retain actual count rather than
            # falsely charging the unused budget.
        return {"best_params":best_params,"best_energy":best_value,
                "energies":trace,"parameter_trace":parameters,
                "iterations":len(trace),"n_evaluations":len(trace),
                "n_shots":len(trace)*shots_per_evaluation,
                "training_mode":"shots" if shots_per_evaluation else "exact_distribution",
                "metrics":self.metrics(best_params,edges),"model":self.model_name,
                "method":method}


class PenaltyObliq(PenaltyProductBernoulli):
    """Deprecated historical name; this is a classical penalty sampler."""
    def __init__(self,*args,**kwargs):
        warnings.warn("PenaltyObliq never implemented genuine ObliQ dynamics; use PenaltyProductBernoulli (classical_product_bernoulli)",DeprecationWarning,stacklevel=2)
        super().__init__(*args,**kwargs)
