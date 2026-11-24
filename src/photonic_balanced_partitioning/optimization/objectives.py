"""Optimum-blind losses; success probabilities belong to retrospective evaluation.

The caller supplies costs of observed or explicitly enumerated outcomes and
must charge their computation. Exact distribution access is not a free QPU
oracle. No optimal cost, optimal partition or optimal-state mask is accepted.
"""
import math
import numpy as np


def training_loss(probabilities, costs, feasible, objective='collision_aware', *,
                  mu=1., gamma=1., alpha=.25, rejection_cost=None):
    allowed={'conditional_energy','collision_aware','log_barrier','cvar','expected_with_rejection'}
    if objective not in allowed:
        raise ValueError('Only optimum-blind training objectives are accepted; success objectives are oracle diagnostics')
    p=np.asarray(probabilities,dtype=float);c=np.asarray(costs,dtype=float);mask=np.asarray(feasible)
    if p.ndim!=1 or not len(p) or c.shape!=p.shape or mask.shape!=p.shape:
        raise ValueError('Probabilities, costs and feasible mask must be nonempty matching vectors')
    if not np.all(np.isfinite(p)) or np.any(p<0) or not np.isclose(p.sum(),1,atol=1e-10,rtol=0):
        raise ValueError('Retain a normalized nonnegative distribution including rejected outcomes')
    if not np.all(np.isfinite(c)) or not np.all(np.isin(mask,[False,True])):
        raise ValueError('Costs must be finite and feasibility must be a Boolean mask')
    if any(not np.isfinite(x) or x<0 for x in (mu,gamma)):
        raise ValueError('Penalty coefficients must be finite and nonnegative')
    mask=mask.astype(bool);pf=float(p[mask].sum())
    if objective=='expected_with_rejection':
        if rejection_cost is None or not np.isfinite(rejection_cost):
            raise ValueError('An explicit finite rejection cost is required')
        if rejection_cost < (float(c[mask].max()) if mask.any() else 0.):
            raise ValueError('Rejection cost must dominate feasible costs of the supplied outcome space')
        return float(p[mask]@c[mask]+(1-pf)*rejection_cost)
    if pf==0:return math.inf
    mean=float(p[mask]@c[mask]/pf)
    if objective=='conditional_energy':return mean
    if objective=='collision_aware':return mean+mu*(1-pf)
    if objective=='log_barrier':return mean-gamma*math.log(pf)
    from ..photonic.objectives import weighted_lower_cvar
    return weighted_lower_cvar(c[mask],p[mask],alpha)
