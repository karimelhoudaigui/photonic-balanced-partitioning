"""Exact low-order Fock moments for a collision-penalized occupation cost.

Input frame V has one orthonormal column per distinct single-photon input.
No amplitudes, permanent, device, optimum oracle, or sampling are needed for
these moments. The same-frame bosonic mean cost is never below its independent
(distinguishable) counterpart for nonnegative graph weights and mu>=0.
This statement does not order success probabilities, conditional costs, or tails.
"""
from __future__ import annotations
from dataclasses import dataclass
from numbers import Integral
import numpy as np

MODELS=('bosonic','distinguishable')


@dataclass(frozen=True)
class OccupationMoments:
    """First moments, raw E[n_i n_j] (diagonal E[n_i^2]), and mean pair count."""
    mean: np.ndarray
    second: np.ndarray
    collision_pairs: float


@dataclass(frozen=True)
class OccupationGap:
    """Nonnegative same-frame bosonic-minus-distinguishable mean contributions."""
    graph: float
    collision: float

    @property
    def total(self):return self.graph+self.collision


def _frame(V):
    v=np.asarray(V,dtype=complex)
    if v.ndim!=2 or v.shape[0]<1 or v.shape[1]>v.shape[0] or not np.all(np.isfinite(v)):
        raise ValueError('V must be a finite m-by-k frame with 0<=k<=m')
    if not np.allclose(v.conj().T@v,np.eye(v.shape[1]),atol=1e-9,rtol=0):
        raise ValueError('Occupied columns must be orthonormal; no implicit renormalization')
    return v


def _parameters(m,edges,mu):
    if not np.isfinite(mu) or mu<0:
        raise ValueError('mu must be finite and nonnegative')
    result=[]
    for edge in edges:
        if len(edge)!=3:raise ValueError('Expected (vertex,vertex,nonnegative weight) triples')
        i,j,w=edge
        if (not isinstance(i,Integral) or not isinstance(j,Integral) or not 0<=i<m or not 0<=j<m
                or not np.isfinite(w) or w<0):
            raise ValueError('Edges require valid indices and finite nonnegative weights')
        result.append((int(i),int(j),float(w)))
    return result,float(mu)


def _model(model):
    if model not in MODELS:raise ValueError('model must be bosonic or distinguishable')


def occupation_cost(occupation,edges,mu):
    """H(n)=sum w_ij(n_i-n_j)^2 + mu*sum_i n_i(n_i-1)/2.

    The cost accepts integer Fock occupations, not threshold bits after decoding.
    For a total of k photons, mu>sum(weights) is a sufficient condition for
    every ground state to be collision-free; this function does not require it.
    """
    values=tuple(occupation)
    if not values or any(not isinstance(x,Integral) or x<0 for x in values):
        raise ValueError('Occupation must contain nonnegative integers')
    weighted,mu=_parameters(len(values),edges,mu)
    graph=sum(w*(values[i]-values[j])**2 for i,j,w in weighted)
    collisions=sum(x*(x-1)//2 for x in values)
    return float(graph+mu*collisions)


def occupation_moments(V,model='bosonic'):
    """Return exact ideal moments in O(m^2*k+mk^2) work, O(m^2) storage.

    The orthonormality check costs O(m*k^2). For sparse training use
    occupation_expectation, which avoids forming all m-by-m correlations.
    """
    v=_frame(V);_model(model)
    q=abs(v)**2;a=q.sum(axis=1);b=np.sum(q*q,axis=1)
    independent_overlap=q@q.T
    if model=='bosonic':
        projector=v@v.conj().T
        second=np.outer(a,a)+abs(projector)**2-2*independent_overlap
        np.fill_diagonal(second,a+2*(a*a-b))
        collisions=float(np.sum(a*a-b))
    else:
        second=np.outer(a,a)-independent_overlap
        np.fill_diagonal(second,a+(a*a-b))
        collisions=float(.5*np.sum(a*a-b))
    return OccupationMoments(a,np.asarray(second,dtype=float),collisions)


def occupation_expectation(V,edges,mu,model='bosonic'):
    """Exact mean H, O((m+|E|)*k) after O(m*k^2) frame validation.

    V is an occupied-column FRAME, not only its projector V V^dagger: mixing
    occupied columns can change the input Fock state and the fourth moments.
    No C* enters the calculation and collisions are not postselected away.
    """
    v=_frame(V);_model(model);weighted,mu=_parameters(len(v),edges,mu)
    q=abs(v)**2;a=q.sum(axis=1);b=np.sum(q*q,axis=1)
    factorial=a*a-b
    factor=2. if model=='bosonic' else 1.
    diagonal=a+factor*factorial
    result=mu*factor/2*float(factorial.sum())
    for i,j,w in weighted:
        if i==j:continue
        overlap=float(q[i]@q[j])
        if model=='bosonic':
            projector_ij=np.dot(v[i],v[j].conj())
            cross=a[i]*a[j]+abs(projector_ij)**2-2*overlap
        else:cross=a[i]*a[j]-overlap
        result+=w*(diagonal[i]+diagonal[j]-2*cross)
    return float(result)


def occupation_statistics_gap(V,edges,mu):
    """Positive-square expression for E_b[H]-E_d[H], O(k^2*(m+|E|)).

    Useful for auditing equality and cancellation, not a faster training path.
    For mu>0 the total is zero iff occupied columns have pairwise disjoint
    output supports (vacuum/one-photon cases are vacuous).
    """
    v=_frame(V);weighted,mu=_parameters(len(v),edges,mu)
    graph=collision=0.
    for a in range(v.shape[1]):
        for b in range(a+1,v.shape[1]):
            z=v[:,a]*v[:,b].conj()
            graph+=2*sum(w*abs(z[i]-z[j])**2 for i,j,w in weighted)
            collision+=mu*float(np.sum(abs(z)**2))
    return OccupationGap(float(graph),float(collision))
