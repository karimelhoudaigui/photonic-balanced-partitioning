# P136 — Independent source-component obstruction review

2026-11-26. Manual non-author audit, parent 2cee874b19f684dfdadacde779af6ceafed51be0.
FULL 109-line research/P136_SUPPORT_COMPONENT_OBSTRUCTION.md read at
b80a4655d204722c649be8e2a3110d27d92edc9a; SHA256
e6f1dfd4d9c006006de6c59ad7368650b7c07ca136401567b3a5e554a366b106.
No P134 raw/output, graph or matrix was inspected. No import/AST, mathematical
program, numerical/symbolic evaluation, RNG, native/QPU or manuscript work.

**ACCEPT the exact spatial-count theorem and the supplied FULL-norm bound.**
I reconstruct the proof below; this is not acceptance of the author's verdict
as evidence, a literature priority claim or a universal optimization no-go.

## 1. The load-bearing physical block step

Let A_l be source sets and J_l receiver sets of the actual bipartite support
components of F. Different components share neither source nor receiver modes.
After analytical row/column permutations, F is a rectangular block sum.
F^dagger F is therefore a source-block sum. Since I+F^dagger F is positive
definite on the full source space, its inverse Q has the SAME source blocks;
this needs no full-column rank. T=2FQ, D=(I-F^dagger F)Q and FQF^dagger then
have exactly the claimed zero CROSS blocks, though entries inside can cancel.

In particular it is the explicit FULL rational reflection U, not only T or
its Gram, that becomes block diagonal on J_l union dump modes r+A_l.
Zero receiver rows give separate identity modes, initially and finally vacuum.
A zero SOURCE column instead contributes its own nonempty A_l, empty J_l,
Q=1,D=1 and one deterministically reflected dump photon. It counts as a
source component. Counting an empty-input receiver isolate would be a false veto.
This also handles all-zero F, rectangular r<k and rank-deficient F.
The same fixed original mode labels and observation apply to both arms;
the proof's analytical permutations do not relabel the graph decoder.

For output n of total k, a nonzero amplitude requires sum_(j in M_l)n_j=|A_l|.
With this condition, the repeated-row occupied amplitude matrix is itself
block diagonal after matching its row slots to these groups. Its permanent
factors as product_l per(B_l); its output factorial product n_j! factors on
the SAME spatial groups. Thus the NORMALIZED B probability is the product
of local normalized Fock probabilities, without an extra binomial factor.
Giving different groups orthogonal internal tags leaves those same local
interferences intact. No nonzero route crosses groups, so ignoring tags yields
the identical product. Both arms give zero on count vectors violating a group
total. This proves equality for every full spatial PNR record, including
collisions and resolved dump counts, without conditioning or tracing a
coherent cross-group mixer into a purported classical count kernel.

## 2. Parameter-uniform proper control and four-cycle zero

For the P133 compiler, W>max|d_j|, 0<=beta<=1/2 and w_jj=0 imply each prototype
diagonal is real >1/2. At every kappa>0, each other entry is nonzero exactly
when its prototype edge has positive weight. No real/imaginary cancellation
or beta-dependent support change occurs. Hence ONE fixed source-component
partition pi_* works for the whole positive-kappa family of a fixed residual.
At kappa=0 each source has its own prototype/dump spatial block. Coarsening
these singleton species to the same pi_* still leaves B's spatial law intact.

If there are at least two source components, pi_* is proper and belongs to
the complete proper-partition controls. Its pointwise utility equals B under
any common classical kernel/score; consequently its own grid maximum equals
B's grid maximum. The maximum over all proper profiles cannot be smaller.
Different residuals may have different pi_*; the claim needs no single
global profile or information about cuts, C* or the selected best grid point.
It does not compare unequal species-preparation costs or changing policies.

For k=4, suppose A_sigma and A_rho are both nonzero for the same receiver-CF
slots. For each slot j, sigma(j) and rho(j) must belong to that row's source
component. Thus sigma o rho^-1 preserves every A_l setwise. A single
four-cycle has one orbit on all four source labels, so it cannot preserve
a nontrivial partition. Every specified four-cycle cross-product is ZERO
individually, not merely canceled by summing orientations or receiver sets.
Therefore C4(Y)=J4=0. With k=4 all component blocks have at most three photons;
with general k one block may be arbitrarily large. No general efficient
simulation statement follows from the mere existence of another component.

The Gram-only shortcut is false. For F=[[1,i],[i,1]], H=2I despite shared
receiver support. T=(2/3)F gives B coincidence amplitude (4/9)(1+i^2)=0,
whereas D coincidence is 2*(4/9)^2=32/81. This directly rejects a singleton
certificate inferred solely from diagonal H. Ambient graph connectivity is
also irrelevant unless it induces the needed bipartite source connections.

## 3. Robustness and exact limits of the inference

For unitaries U,U0 with ||U-U0||op<=delta, telescoping the K=k tensor factors
gives norm distance <=K*delta; each other tensor factor has norm one.
The same inequality holds for occupied ISOMETRIES on the common source/output
spaces. Include internal tags by tensoring the one-particle maps with their
identity: the norm is unchanged. Restricting to normalized bosonic symmetric
inputs adds no factorial or combinatorial amplification. For each arm,
pure-state trace distance is <=vector distance, so counting contracts it
to TV<=K*delta. Triangle through P_B(U0)=P_pi_*(U0) gives
TV(P_B(U),P_pi_*(U))<=min(1,2K*delta). The source's constant is valid.
Common count kernels contract TV, and h in [0,h_max] gives mean error
<=h_max times that bound. This does not assign a favorable utility sign.

FULL means including resolved dump modes and any subsequent coherent mixing.
As a manual caution, two singleton sources may have zero signal transfer in
both instruments, yet a later balanced beam splitter between their dump
modes gives B coincidence 0 and D coincidence 1/2. Thus zero signal-matrix
difference does not certify the asserted full-PNR equality. This example
concerns an additional coherent mixer, not a contradiction to the reflection
theorem or to a separately specified canonical-environment signal bound.
Rare conditioning is also excluded: raw laws with common mass 1-epsilon on
failure and epsilon on different accepted records have raw TV epsilon but
conditional TV 1. Neither a small raw bound nor a positive support threshold
licenses an accepted-sector conclusion without its own probability bound.

Verdict scope: a proved structural veto for disconnected SOURCE support of
this modeled static family, with a supplied full-operator robustness bound.
Connected support is only necessary to evade this veto, not sufficient for
nonzero four-cycles, a favorable cut sign or an optimizer benefit. Any policy
that searches for connected pools must pay/share that search and keep failures
under a NEW prospective card; it cannot replace the frozen P134 contexts.
No named P134 outcome, practical runtime, hardware result or universal
impossibility was inferred. Only this review was written; source remains frozen.
