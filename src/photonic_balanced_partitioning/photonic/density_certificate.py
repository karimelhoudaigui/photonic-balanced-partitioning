"""Sufficient spatial certificate; no claim of hardness when a bound is loose.

Distinct singly occupied inputs, passive lossless optics and complete outcomes.
The new density implication is a derived research candidate pending independent
review and novelty checking. The spatial Gram/cycle certificate is separately
proved in theory/near_collisionless_bound.md.
"""
import math
import numpy as np


def cycle_envelope(sigma):
    """Infinite-cycle upper envelope; return the trivial bound outside its range."""
    if not math.isfinite(sigma) or sigma < 0:
        raise ValueError('Expected finite nonnegative sigma')
    if sigma >= 1:
        return 1.
    return min(1.,float(.5*np.expm1(-sigma-np.log1p(-sigma))))


def density_certificate(frame):
    """Return sufficient bounds from a finite complex Stiefel frame V[m,k].

    M is expected unordered collision pairs, not collision probability. The
    minimum density c is over all rows with positive intensity, without dropping
    small positive values. Zero rows carry no probability in either sampler.
    Roundoff corrections of at most 1e-10 are recorded rather than hidden.
    """
    v=np.asarray(frame,dtype=complex)
    if v.ndim!=2 or not 1<=v.shape[1]<=v.shape[0] or not np.isfinite(v).all():
        raise ValueError('Expected finite frame with 1<=k<=m')
    if not np.allclose(v.conj().T@v,np.eye(v.shape[1]),atol=1e-10,rtol=0):
        raise ValueError('Occupied columns must be orthonormal')
    q=abs(v)**2;intensities=q.sum(axis=1)
    raw_m=float(np.sum(intensities**2-np.sum(q*q,axis=1)))
    raw_delta=float(np.sum(intensities-np.max(q,axis=1)))
    if min(raw_m,raw_delta)<-1e-10:raise ArithmeticError('Negative physical certificate quantity')
    pairs=max(0.,raw_m);delta=max(0.,raw_delta)
    c=float(np.min(intensities[intensities>0]))
    density_ratio=pairs/c
    if delta>density_ratio+1e-9:raise ArithmeticError('Density implication violated beyond roundoff')
    refined_ratio=(pairs/(c+math.sqrt(c*c-2*pairs))
                   if pairs<c*c/2 else density_ratio)
    if delta>refined_ratio+1e-9:raise ArithmeticError('Refined density implication violated beyond roundoff')
    gram=np.sqrt(q).T@np.sqrt(q);off=gram.copy();np.fill_diagonal(off,0.)
    sigma=float(np.linalg.norm(off,'fro'))
    support_sigma=2*math.sqrt(delta)+delta
    if sigma>support_sigma+1e-9:raise ArithmeticError('Support/Gram bound violated beyond roundoff')
    return dict(m=v.shape[0],k=v.shape[1],minimum_positive_intensity=c,
        expected_collision_pairs=pairs,expected_collision_pairs_raw=raw_m,
        dominant_support_leakage=delta,dominant_support_leakage_raw=raw_delta,
        density_ratio=density_ratio,spatial_gram_sigma=sigma,
        refined_density_leakage_upper=refined_ratio,
        support_sigma_upper=support_sigma,
        direct_gram_tv_bound=cycle_envelope(sigma),
        support_cycle_tv_bound=cycle_envelope(support_sigma),
        density_cycle_tv_bound=cycle_envelope(2*math.sqrt(density_ratio)+density_ratio),
        refined_density_cycle_tv_bound=cycle_envelope(2*math.sqrt(refined_ratio)+refined_ratio),
        support_state_tv_bound=min(1.,math.sqrt(2*delta)+delta),
        zero_intensity_rows=int(np.sum(intensities==0)),
        non_claim='Sufficient absolute-TV certificate only; not a success ratio, sampler speedup or hardness test.')
