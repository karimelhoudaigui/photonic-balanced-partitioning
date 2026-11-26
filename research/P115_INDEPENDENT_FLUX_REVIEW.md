# P115 independent uniform-flux reduction review

2026-11-26. Non-author MANUAL adversarial proof review.
Source read FULL: `research/P115_UNIFORM_FLUX_REDUCTION.md`, 154 lines,
commit `21cbfc252d565b677d47472557670580c44a55f2`.
SHA256 `261ba1b0b501efb7e2006868870b0e1fe95e9a1f0b932013a45e2e1918085abf`.
Review parent: `d65e4e7afc5b9bc25f9b2223387b9444873fdce9`.

**PROVED AS WRITTEN for the reduction and its CONDITIONAL sign transfer.**
No blocking gauge, spectral, normalization, labeling or endpoint gap found.
P115 does not itself prove positivity. The strict-sign consequence below
uses separately identified P114 polynomials; it is not a result obtained
from the P107 rectangular certificate or its grid. No calculation was run.

## 1. Gauge and flux reconstructed at the same labels

Expanding a|z_j-exp(i theta_j)z_(j+1)|^2 gives L_jj=2a and
L_(j,j+1)=-a exp(i theta_j), with four distinct cycle edges. For
D_jj=exp(i chi_j), the transformed phase is theta_j-chi_j+chi_(j+1).
The stated recursion gives psi on the first three edges. Its closing-edge
value is sum_j theta_j-3psi=psi modulo 2pi because 4psi=Phi modulo 2pi.
Thus the phase convention, including the 3-to-0 edge, is correct.
The canonical phase is Phi_0/4 in [-pi/4,pi/4]; flux itself is Phi_0,
not psi. Different lifts are gauge-equivalent, not different selected data.

For phi=|psi|, reflection j->-j reverses the phase. A diagonal gauge cannot
generically reverse a nonzero flux; the source does not make that mistake.
More strongly, L(-phi)=conj(L(phi)) gives a direct SAME-LABEL comparison.
Real spectral functions imply T(-phi)=conj(T(phi)), E(-phi)=conj(E(phi)),
and U(-phi)=conj(U(phi)). Every fixed-Fock-input amplitude is conjugated,
with unchanged real occupation-factorial normalization. Full eight-port
probabilities therefore agree at each identical output occupation. D's
intensities agree too. This removes the sign without silently transporting
a decoder or graph vertex. It is not true for arbitrary coherent inputs.

For the initial diagonal gauge, T'=D^dagger T D and E'=D^dagger E D,
so U'=diag(D^dagger,D^dagger) U diag(D,D). The occupied four input ports
give a global phase, vacuum phases are immaterial, and each output Fock
occupation acquires only a phase. Hence all loss/collision/threshold records
and either frozen decoder retain their same-label law. If reflection itself
were used instead, labels/priorities would need transport as the source says.

## 2. Fourier order, scale and product relation

For F_jq=exp(-i pi j q/2)/2, its next cyclic component is
exp(-i pi q/2) times the current one. Direct application of L(phi) gives
lambda_q=2a[1-cos(phi-pi q/2)]. With c=cos(phi)>=s=sin(phi)>=0,
the FOURIER order is 2a(1-c,1-s,1+c,1+s), whereas increasing eigenvalue
order is q=0,1,3,2. In particular the ground is lambda_0 and width is 4ac.
No Fourier columns are secretly sorted before assigning x,xy,y.

With Lambda=max(1,4ac), the ground-shifted H spectrum is exactly
(0,2a(c-s),4ac,2a(c+s))/Lambda. It lies in [0,1], and the q=1 and q=3
gaps add to the q=2 gap. Exponentiating -beta H/2 therefore gives
F diag(1,x,xy,y) F^dagger with x=exp[-beta a(c-s)/Lambda] and
y=exp[-beta a(c+s)/Lambda]. This checks the otherwise essential factor 2a.
For finite beta>=0,a>0, 0<y<=x<=1. A square sign theorem suffices for
this image; no claim that one fixed flux sweeps the whole square is needed.

The product xy=exp[-2beta ac/Lambda] equals exp(-beta/2) for beta>0
precisely when Lambda=4ac. If 4ac<1, Lambda=1 and that shortcut is false.
At a=1/2,phi=pi/6, Lambda=sqrt(3) and
(c+s)/(c-s)=(sqrt(3)+1)/(sqrt(3)-1)=2+sqrt(3), reproducing P101.
Its original three forward phases 4pi/3 and closing phase -4pi/3 give
flux 8pi/3 modulo 2pi, canonical phi=pi/6, consistently with this example.

## 3. Degeneracies and limits

At beta=0 the transfer is I. At phi=0,a>0 the ground is simple although
the middle excited pair is degenerate. For fixed a>0,phi<pi/4 the gap is
2a(c-s)/Lambda>0, so the canonical strong limit is F_0F_0^dagger=J/4.
At phi=pi/4 the ground is instead q=0,1; x=1,
y=exp[-sqrt(2)beta a/Lambda], and the strong limit is
F diag(1,1,0,0) F^dagger. The rank-one surrogate does not cover it.
Taking strong filtering before versus after the flux endpoint produces
different projectors, explaining the noncommuting limits. An arbitrarily
small positive gap does not guarantee a uniformly accurate rank-one approximation
at fixed finite strength. At a=0, Lambda=1, L=H=0 and T=I for every beta;
all four ground vectors
remain. Flux has no edge observable meaning, and no bright-mode limit is
available. Ground subtraction is an ideal compiler definition, not a way
to recover external physical attenuation.

## 4. Graph costs and conditional signed transfer

For 0<a<=1 the graph has cycle weights 1-a and diagonal weights 1.
An adjacent-side partition crosses two cycle edges and both diagonals,
costing 4-2a; an opposite-side partition crosses four cycle edges,
costing 4-4a. Thus at EVERY balanced output partition, same labels,
C_a=2a C_(1/2)+(4-8a). A normalized B-minus-D raw expectation cancels
the additive constant, giving delta_a=2a delta_(1/2)(x,y).
All outputs, including vacuum fallback, are feasible balanced partitions;
neither conditioning nor removal of lower sectors enters this cancellation.
The factor is positive for a>0. For a=0 every cut costs 4 and delta=0.
At a=1 the graph is two disjoint unit diagonals; no connectedness premise
is claimed there. For a>1 the optical reduction still holds but some graph
weights are negative, outside the stated nonnegative-graph scope.

P114's explicit-polynomial proof was independently checked in f52bef0;
ROOT reports its physical identification by independent P113 COMPARE_PASS
at original seal `ac82cd0d1dc8a1a21ec5475180e821d881c6f78a`.
Accepting that separate evidence dependency,
P114's strict positivity implies delta_a>0 for every 0<a<=1, finite
beta>0 and flux: y<1 while y>0, so neither exceptional corner is reached.
At beta=0 delta=0; for fixed phi<pi/4 its strong-filter limit is also zero.
No bound separated from zero over all permitted strengths/weights/fluxes
is claimed.
This is a conditional same-setting D mean comparison, not equality of laws
or evidence that the registered Bernstein algorithm established its sign.

## Scope and disposition

Accept the elementary spectral/gauge reduction and conditional cost transfer.
Gauge-invariant count laws do NOT transport P101's real-spin energy bridge:
that bridge used its specific cos(theta) convention. Nonnegative eigenvalues
also do not imply entrywise nonnegative amplitudes. Nonuniform cycle weights,
different inputs, decoders, adaptive policies, extra hardware losses/noise and
other graph encodings require new arguments. P117's binary-cost independent-
attempt corollary is a separate dependency, not a conclusion proved in P115.
No measured-wall-time, QPU readiness, universal no-go, novelty or optimizer
success follows. Frozen P113/P114 remain unchanged. Only manual algebra,
text reads, hashes and Git metadata were used; no scientific program ran.
