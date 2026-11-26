# P136 — source-support component obstruction for the rational reflection

2026-11-26. ROOT supplied the conjecture; this is a manual reconstruction, not a novelty claim.
No P134-generated graph, matrix, implementation, outcome or raw record was inspected.
No factory, import, AST, script, RNG, native computation or experiment occurred.
The fixed9441-row P134 population and its separate execution gates remain unchanged.

**Verdict: proved as written for the common spatial-count observation specified here.**
The result is an exact mode-block factorization, not a matched-clock or general optimizer impossibility theorem.

## 1. Exact hypothesis and block decomposition

Let F in Q(i)^(r-by-k), r>=1,k>=2, with P133's
`H=F†F`, `Q=(I+H)^(-1)`, `T=2FQ`, `D=(I-H)Q`,
`U=[[I-2FQF†,T],[T†,-D]]`.
Prepare known CF input in the LAST k modes, with all r other inputs vacuum.
The output alphabet is the spatial PNR vector on all r+k modes, with internal species labels ignored.
No assumption about signs, rank, transmission magnitude, or graph optimality is needed.

Construct the BIPARTITE support graph with receiver-row vertices j and source-column vertices a,
joining j to a iff the actual entry F_ja is nonzero. No floating threshold is substituted for this test.
Let its components containing sources have source sets A_1,...,A_c and receiver sets J_1,...,J_c.
Every A_l is nonempty; an isolated zero source column is a legitimate singleton component, possibly J_l empty.
An isolated zero receiver row contains NO source and must not be counted toward c.

After permuting row/source indices, F has blocks F[J_l,A_l] and zero cross blocks.
Therefore H,Q,D are block diagonal on the A_l, and T[J_l,A_m]=0 for l!=m,
with zero unused receiver rows. Also FQF† is block diagonal on the J_l.
Consequently U is block diagonal on the PHYSICAL mode groups

    M_l = receiver modes J_l union dump/input modes {r+a:a in A_l},

plus an identity on unused zero-F receiver rows. The latter start and stay in vacuum.
All permutations in this proof are analytical relabelings; both arms retain the same original output labels/decoder.
This argument uses the actual spatial support of F, not merely the Gram support.

## 2. Equality with a proper species law

Assume c>=2, and assign one orthogonal internal species to each source set A_l,
with photons indistinguishable inside each A_l. This is a proper source partition pi_*.
Gamma(U) factorizes over the mutually orthogonal spatial mode groups M_l.
For an output count vector n, both arms have probability0 unless each group has total |A_l|.
Otherwise the normalized Fock probability factorizes into the product of the local A_l bosonic probabilities.
No particle from A_l can reach another group; the same product holds after giving different groups orthogonal species labels.
Hence, INCLUDING resolved spatial dump counts and collisions,

    P_B(n;U) = P_(pi_*)(n;U)  for every spatial PNR n.   (1)

Equivalently, every nonzero assignment amplitude has the same source-component color at each output slot,
so the species bucket formula retains ALL nonzero B cross terms.
There is no CF denominator, loss independence assumption, or rare-sector conditioning.
Any identical classical count kernel, random-tie decoder, hold rule, score or terminal h preserves equality.
This includes common portwise thinning when it acts as a kernel on these counts.
It does NOT identify species-resolved label records, or cover an arbitrary subsequent coherent cross-group mode mixer.
For example, a later beam splitter can make two initially separate single-photon blocks interfere.
Unmodeled coherent device leakage also requires a separate error model, not an exact block claim.

## 3. Entire P133 graph family and the grid consequence

Fix the graph, S0, receiver pool, DISTINCT prototypes, d and W of P133.
For 0<=beta<=1/2, kappa>0, nonnegative weights and w_jj=0,

    F_ja != 0 iff j=p_a or w_(j,p_a)>0.                (2)

Indeed the prototype entry is real and >1/2, while every other entry is exactly i*kappa*w/W.
Thus the source-support partition is independent of beta and positive kappa.
If it has c>=2 source components, the SAME pi_* proves (1) throughout that parameter family.
At kappa=0, F is a diagonal-scaled prototype injection. Its finer singleton blocks make all species laws identical;
in particular the same coarser pi_* still duplicates B. No endpoint exception invalidates the grid comparison.

For any common finite grid and common utility, pointwise I_(pi_*)(theta)=I_B(theta), hence

    max_(proper pi) max_theta I_pi(theta) >= max_theta I_B(theta). (3)

This applies separately to each fixed residual context, with that context's own pi_*.
It therefore forbids a STRICT proper-profile grid win under the hypothesis, without using C* or inspecting the utility values.
It does not compare physical species-preparation time or arbitrary changing-policy total costs.

For k4, take any receiver-CF Y and amplitudes A_sigma,A_rho of P134.
If both are nonzero, sigma composed rho^(-1) preserves every A_l.
A single four-cycle cannot leave EVERY block of a nontrivial source partition setwise invariant.
Each single-four-cycle product A_sigma*conj(A_rho) is therefore zero individually, and C4(Y)=J4=0.
The component blocks contain at most three photons; this is an exact reduction to smaller blocks, not a measured runtime claim.
For general k a component may still be large, so no universal efficient-simulation conclusion is imported.

## 4. Necessary cautions and the next premise

Gram zeros alone are insufficient: F=[[1,i],[i,1]] has H=2I but shared receiver rows.
P133 gives T=(2/3)F; receiver coincidence is B0 versus D32/81, disproving a false Gram-only singleton certificate.
Conversely receiver-only isolated vertices do not trigger (3) when all sources lie in one component.
Even connectivity of the ordinary induced receiver graph is not the criterion:
a path p1-u-v-p2 with two nonprototype intermediate vertices uses an edge u-v absent from the bipartite F support.
The precise criterion is connectivity between SOURCE vertices in that support graph.

This may diagnose a sparse receiver pool even inside a connected ambient graph; no claim is made about the actual named P134 graphs.
Source connectivity is necessary to escape this screen, not sufficient for nonzero C4 or a useful sign.
A FUTURE optimum-blind policy could choose the first public-mark-ordered pool/prototypes satisfying this structural predicate,
charge every structural search and fallback, expose the same rule/features to controls, and retain failures when no pool qualifies.
Such a policy changes the prospective selection contract and needs a new card; it must not repair or replace the fixed P134 contexts.
The existing first screen still runs only under its original freeze/review/binding/authority, preserving all outcomes.

## 5. Supplied full-matrix robustness certificate

If U0 has these blocks and ||U-U0||op<=delta on the same unitary input/output spaces,
tensor-power telescoping gives ||U^tensorK-U0^tensorK||op<=K*delta, for both B and the fixed component-species input.
Pure-state trace distance is <=vector distance; internal trace and count measurement contract it.
Triangle through the exactly equal U0 laws gives TV(P_B(U),P_pi_*(U))<=min(1,2K*delta).
The same proof holds for full occupied isometries including dump outputs. Common count kernels preserve it; [0,h_max] utility error is <=h_max times this bound.
delta must certify that FULL unitary/isometry, including any later coherent cross-mixing: not entry thresholds, signal means, Gram zeros or a signal-only transfer. Rare conditional CF normalization has no such uniform bound.
