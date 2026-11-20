# Theory audit and independent finite check

Base Git checkpoint: `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`.
Reviewed 2026-11-20. Reviewer: theory/literature agent, same-agent adversarial
self-review of its own proof text. A separate coordinator reconstruction is
still required before claiming independent review.

Supplementary independent review completed later in this cycle: the
objectives/baselines agent reconstructed the twirl, conditional Haar symmetry,
Stirling coefficient, pair-moment factor four, disjoint-support factorization
and permutation counterexample from the source proof at SHA256
`0daedc5400a211d8fd41eb76764283ca0c0e68c426a965d5f52af6ba64041b87`.
No missing hypothesis was found. The coordinator separately checked the
conditional expectation argument and the two-pair annihilation/creation terms.
This supplements, rather than changes, the author self-review recorded above;
novelty remains outside this correctness verdict.

Primary verdict: **proved as written** for T-Haar, T-Scaling, T-Haar-Metrics,
T-Pairs and T-Pareto under the exact hypotheses in `theory/proven_results.md`.
This verdict neither authenticates novelty nor evaluates algorithm performance.

## Dependency graph and obligations

| Claim | Leaves | Checks | Result |
|---|---|---|---|
| T-Haar | Haar invariance; occupation torus characters; connected photon-transfer graph; trace normalization | Commutant argument reproduced without assuming Haar randomness in the full Fock space; k=0 and k=m included; externally matched Arkhipov–Kuperberg Prop1/Cor2 | passed |
| T-Scaling | T-Haar factorial ratio; Stirling expansion | Extra factor 3/2 retained; inverse-power correction checked; sparse-density approximation explicitly excluded | passed |
| T-Haar-Metrics | T-Haar; output permutation transitivity; almost-sure positive CF | Conditional ratio proof uses symmetry directly; covariance zero does not imply independence | passed |
| T-Pairs | Fock annihilation relations; nonnegative pair count | Factor four checked by two-photon HOM and brute permanents; k>=2 denominator restriction; k=0,1 separate | passed |
| Disjoint-support characterization | T-Pairs; nonnegative q products | Both directions; full probability factorization; multiple photons per occupied input excluded | passed |
| T-Pareto | Permutation unitary; nonempty target set | Gives (1,1) constructively for any known target; does not solve discovery task | passed |
| Two-disjoint-target restriction | Disjoint column supports; Cartesian product support | Any nondeterministic column creates two outcomes differing by one vertex; k=1 excluded | passed |
| Novelty | Exact literature overlap and broader coverage | Haar and QAOA overlaps verified; postselection/ObliQ extraction incomplete | OPEN; not a mathematical proof gap |
| Quantitative near-collisionless simulation | Needed stability bound | Not derived; pair-overlap bound alone is insufficient | not addressed / OPEN |

## Independent computation contract

Assertion tested: the pair-moment identity and probability bounds hold within
floating error for the enumerated ideal Fock distributions, and explicitly
constructed disjoint-support circuits give identical bosonic/distinguishable
probabilities. This is an orthogonal implementation check using direct
permutation sums, independent of the repository's Ryser implementation. It
is not exhaustive in U and does not prove the universal statement.

Inputs: 25 complex-Gaussian-QR Haar matrices for each (m,k) in
(2,2), (4,2), (6,3), (8,4); seed 20261120; all weak output occupations in each
case. Four exact-structure disjoint-support circuits checked as well. The
m=2,k=2 case uses identity for the disjoint check; the others use independent
occupied-to-vacant rotations. No raw probabilities are renormalized. Tolerance
for interpretation: 1e-12 in these well-conditioned small cases.

Execution: completed, exit 0. Python 3.9.6, NumPy 1.26.4.
No QPU, loss model or optimization. Raw stdout:

```json
{
  "seed": 20261120,
  "haar_cases": 100,
  "max_normalization_error": 2.220446049250313e-15,
  "max_pair_moment_error": 1.9984014443252818e-15,
  "max_bound_violation": 2.220446049250313e-16,
  "max_disjoint_distribution_error": 2.220446049250313e-16,
  "numpy": "1.26.4"
}
```

Outcome: **implementation and finite assertion verified in the stated range**
up to 1e-12 tolerance. Mathematical proofs above, rather than this finite check,
support the universal conclusions.

## Exact reproduction command

Save the following code as `/tmp/pasqal_theory_check.py` and run
`python3 /tmp/pasqal_theory_check.py` with NumPy 1.26.4. It is embedded here to
preserve the exact executed input; no package source edits are needed.

```python
import itertools, json, math
import numpy as np

def compositions(total, modes):
    if modes == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first, modes-1):
                yield (first,)+tail

def permanent(matrix):
    k=len(matrix)
    return sum(np.prod([matrix[i,p[i]] for i in range(k)]) for p in itertools.permutations(range(k)))

def distribution(U,k,bosonic=True):
    states=list(compositions(k,len(U)))
    p=[]
    for state in states:
        rows=np.repeat(np.arange(len(U)),state)
        A=U[rows,:k]
        den=math.prod(math.factorial(v) for v in state)
        p.append(abs(permanent(A))**2/den if bosonic else permanent(abs(A)**2).real/den)
    return states,np.array(p)

rng=np.random.default_rng(20261120)
max_norm=max_moment=max_bounds=max_disjoint=0.
cases=0
for m,k in [(2,2),(4,2),(6,3),(8,4)]:
    for _ in range(25):
        Z=rng.normal(size=(m,m))+1j*rng.normal(size=(m,m))
        U,R=np.linalg.qr(Z); U=U@np.diag(np.diag(R)/abs(np.diag(R)))
        states,p=distribution(U,k)
        Q=sum(sum(abs(U[i,a])**2*abs(U[i,b])**2 for a in range(k) for b in range(a+1,k)) for i in range(m))
        M=np.array([sum(t*(t-1)/2 for t in s) for s in states])
        eps=p[M>0].sum()
        max_norm=max(max_norm,abs(p.sum()-1))
        max_moment=max(max_moment,abs(p@M-2*Q))
        K=k*(k-1)/2
        max_bounds=max(max_bounds,max(0,2*Q/K-eps,eps-2*Q))
        cases+=1
    U=np.eye(m,dtype=complex)
    if 2*k<=m:
        for a in range(k):
            angle=0.23+0.17*a
            U[np.ix_([a,a+k],[a,a+k])]=[[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]]
    states,p=distribution(U,k)
    _,d=distribution(U,k,False)
    max_disjoint=max(max_disjoint,np.max(abs(p-d)),abs(sum(p[i] for i,s in enumerate(states) if max(s)<=1)-1))
print(json.dumps(dict(seed=20261120,haar_cases=cases,max_normalization_error=max_norm,max_pair_moment_error=max_moment,max_bound_violation=max_bounds,max_disjoint_distribution_error=max_disjoint,numpy=np.__version__),indent=2))
```

Executed script SHA256: `2d2aa2bf4452d6ef445f4ac85efc90d7067b44e948b960cee5cebd487698040b`.
The executed script was temporary; this report contains the complete retained
script and raw summary. Full per-state samples were not retained in this
independent check; the main Perceval validation owns that separate obligation.
No v2 runner manifest was generated for this small supplementary check, so
its provenance is this exact input plus stdout and explicit environment.

## Literature authentication and limits

Primary exact-source obligations used: Arkhipov–Kuperberg 1106.0849v1 Prop1,
Cor2 and published pp2–4; Hadfield 1709.03489v2 Appendix A.3.2; Martinez–Font-Segura
2602.09894v1 Sec3.6 Eq39. Their mode/particle notation is interchanged where
needed. The proofs in our notes are self-contained and do not import an
unverified theorem from ObliQ or recent trainability work. Primary papers were
read through web tools; no full-text source cache or retained-source hashes
were created, so these links and versions identify the external evidence.
Extraction depth for every record is in `research/literature_matrix.csv`.

Smallest remaining scientific gap: an optimum-blind, interference-dependent
benefit at matched physical attempt and classical search budgets. Neither the
exact Haar law nor a permutation preparing a known optimum closes it. Cheapest
next discriminator: evaluate and reoptimize distinguishable circuits and a
classical feasible swap sampler on the very same graph/seed/budget list.
