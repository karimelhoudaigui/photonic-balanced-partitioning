# Audit: near-collisionless bounds versus distinguishable sampling

Date: 2026-11-20. Initial program base:
`847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`.
Repository HEAD observed while writing this continuation:
`5ce1dc127a95c092a433f6b5a4ea6ed7b8865f38`.
Owner: theory/literature agent. Write scope: this report and
`theory/near_collisionless_bound.md` only. The latter contains the exact
claims and proofs; earlier theory files were left unchanged.

Primary mathematical verdict: **proved as written** for N1–N4, under the
explicit distinct-input-mode, passive, lossless, full-Fock hypotheses.
Review provenance: same-agent derivation and adversarial self-review.
Independent coordinator reconstruction and experiment cross-check are separate
obligations; this report does not claim they have occurred.

## Scientific outcome

The conjectured permanent bound is valid, including the factor one half:
`TV(p,d)<=min(1,(Per(B)-1)/2)`. A cycle expansion reduces it to an efficiently
computable bound using `S=||B-I||_F^2` and derangement coefficients. Collision
probability alone yields a dimension-dependent certificate via
`S<=m*binom(k,2)*(1-P_CF)`.

The attempted dimension-uniform interpretation is **REJECTED**, even at
balanced density. Explicit circuits with `m=2k`, even `k`, have
`1-P_CF=2/(k+2)->0` and `TV(p,d)=1/2`. This is a negative result about
approximation by independent photons, not a classical hardness result.

## Dependency graph and obligation checks

| Obligation | Decisive check | Status |
|---|---|---|
| Complete bosonic probability | Input factorials one; output factor `prod t_i!` retained | passed |
| Complete distinguishable probability | Incoherent routing sum divided by the same output multiplicity | passed |
| Occupation-to-ordered-list conversion | Each `t` has `k!/t!` lists; summand is symmetric | passed |
| Relative permutation count | `tau o sigma^{-1}` has exactly `k!` representations | passed |
| TV convention | Half L1, range [0,1], including collisions | passed |
| Cycle expansion | Permutations are vertex-disjoint simple cycles; exponential permits extra repetitions/overlaps, all positive | passed |
| Trace bound | `A` symmetric; closed-walk trace nonnegative; `ell_l<=ell_2` | passed |
| Infinite formal series | Only coefficients through degree k used; no convergence assumption needed for polynomial | passed |
| Closed form | Analytic infinite sum used only when S<1 | passed |
| Derangement recurrence | `!0=1`, `!1=0`, `!r=(r-1)(!(r-1)+!(r-2))` | passed |
| Collision reduction | Cauchy–Schwarz plus `E M<=binom(k,2)delta`; no dilute approximation | passed |
| Quantifiers | Fixed-size continuity distinguished from size-uniform claims | passed |
| Balanced counterexample | Active block dimension `k+2`, two active photons, `k-2` deterministic spectators | passed |
| Unitary existence | The active columns are orthonormal; complete a basis, then block-diagonal identity on spectators | passed |
| Physical success inference | An absolute fixed-event discrepancy bound; no waiting-time ratio or optimizer comparison inferred | passed |
| Novelty | Only a bounded source search; close prior permanent/triangle technique found | OPEN |

## Executed supplementary checks

Finite assertion: `Per(I+A)-1<=H_k(||A||_F^2)` up to numerical tolerance for
72 fixed-seed real symmetric nonnegative zero-diagonal matrices, and exact
normalization/TV/collision formulas for the two-photon counterexample at
15 even active dimensions `L=2,4,...,30`. The matrices in the first check need
not be physical Gram matrices, which tests the more general algebraic lemma.
This is not exhaustive coverage of all matrices or unitaries.

Command: `python3` with the complete code below. Environment: system Python
3.9.6, Python standard library only. Seed: 20261120. Exit: 0. Raw stdout:

```text
symmetric_nonnegative_zero_diagonal_cases 72 max_positive_violation 2.7755575615628914e-17
two_photon_counterexamples_L2_to30 15 exact_rational_checks_PASS
```

The `2.78e-17` residual is below the `1e-12` floating tolerance and comes
from cancellation in the k=2 equality. Counterexample checks use exact rational
arithmetic. Outcome: **finite assertions verified in the stated range**;
universal claims rest on the proofs, not these samples. No full-distribution
simulator, QPU or noise model was used by this supplementary command.

```python
import itertools, math, random
from fractions import Fraction
rng=random.Random(20261120)
max_violation=0.0
cases=0
for k in range(2,8):
 for repetition in range(12):
  A=[[0.0]*k for _ in range(k)]
  for a in range(k):
   for b in range(a): A[a][b]=A[b][a]=rng.random()/max(1,k-1)
  B=[[A[a][b]+(a==b) for b in range(k)] for a in range(k)]
  per=sum(math.prod(B[a][p[a]] for a in range(k)) for p in itertools.permutations(range(k)))
  S=sum(x*x for row in A for x in row)
  H=0.0
  der=[1,0]
  for r in range(2,k+1):
   der.append((r-1)*(der[-1]+der[-2]))
   H+=der[-1]/math.factorial(r)*S**(r/2)
  max_violation=max(max_violation, per-1-H)
  cases+=1
print('symmetric_nonnegative_zero_diagonal_cases',cases,'max_positive_violation',max_violation)
for L in range(2,32,2):
 dcol=Fraction(1,L*L); pcol=2*dcol
 same=L*(L-2)//4; opposite=L*L//4
 psum=L*pcol+same*4*dcol
 dsum=L*dcol+(same+opposite)*2*dcol
 tv=(L*abs(pcol-dcol)+same*2*dcol+opposite*2*dcol)/2
 assert psum==dsum==1 and tv==Fraction(1,2) and L*pcol==Fraction(2,L)
print('two_photon_counterexamples_L2_to30',15,'exact_rational_checks_PASS')
```

This report preserves the exact command input and stdout. No v2 run manifest
was created for this supplementary calculation. Full independent physical
distribution checks are being handled by the coordinating experiment route.

## Source authentication and novelty boundary

Primary source read: Malte C. Tichy, *Sampling of partially distinguishable
bosons and the relation to the multidimensional permanent*,
[arXiv:1410.7687v3](https://arxiv.org/html/1410.7687v3), 2015-02-18,
published [PRA 91, 022316](https://doi.org/10.1103/PhysRevA.91.022316).
Authentication: arXiv version history and publisher title/metadata matched.
Extraction: Sec. IV.2 Eq. (55) and Sec. IV.4, including its unhalved L1
convention. Application verdict: **partial or adjacent result only**. Its
internal-state Gram matrix is not our spatial absolute-overlap matrix; the
new proof does not rely on substituting one for the other. No fetched text
was retained; exact URLs and version identify the source.

Bounded discovery queries covered boson sampling / total variation /
permanent / overlaps, spatial overlap, absolute values, and permanent /
derangements / Frobenius norm. These searches do not settle novelty. The
cycle bound and balanced spectator construction may be elementary corollaries
of existing work. No “apparently new” label is assigned.

## Research decision and next discriminator

KEEP the overlap certificate as a diagnostic: if it is small, substantial
fixed-circuit success enrichment from indistinguishability is impossible.
REJECT collision rate alone as a size-uniform proxy for interference.
FOLLOW-UP: evaluate exact TV, N1 and N2 on the actually optimized meshes;
then compare the same U and separately reoptimized distinguishable circuits
under matched budgets. A vacuous upper bound must be recorded as inconclusive,
not as evidence that interference matters.

Mathematical proofreading: both new files reviewed for notation, quantifier
scope, factorials and display integration. No further edits or unresolved
typographical mathematical-token changes were needed. Independent novelty
and proof review remain separate from this self-review.
