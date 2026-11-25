# P65 uniform collision-average proposition: focused proof audit

2026-11-25. **Primary verdict: proved as written.** A small uniform average
of ideal bosonic collision probabilities over ALL K-subsets implies the
stated monomial approximation, complete-output absolute TV bound and, for
symmetric U, symmetric classical permutation replacement. The conditional
history-by-history trajectory extension has the stated scope. It supplies
neither a relative-gap obstruction nor a matched-cost algorithmic conclusion.

Exact audited commit: `43dd87345790af2b07bbe83c784f84f63bfd2704`.
Artifact: `theory/P65_collision_counted_photonic_markov_kernel.md`, SHA256
`3ffb2be9e19b6d9acb49b6d376a7cbe1fc294940a24ee50313b840b3bf522271`.
The target is section4, lines182--275, Proposition(9)--(12) and its lift,
symmetrization and trajectory paragraphs. Sections1--2 supply source/kernel/
incumbent conventions only. Equation(8), other mechanisms and portfolio routes
are outside this review. No supervisor verdict on this proof was consulted.

## Normalized claim and dependency graph

For a finite N-mode unitary U and integer 2<=K<=N, let Omega_K consist of all
K-subsets of inputs. For the normalized lossless bosonic state |1_S>, let
p_col(S) include EVERY output occupation with at least one collision. Assume
the uniform average over Omega_K is at most epsilon. Its satisfaction already
implies epsilon>=0. The proposition locally quantifies K beyond the earlier
balanced specialization K=N/2; its all-K-subset proof makes that scope explicit.

There exists a unitary monomial V with squared Frobenius error at most
N(N-1)epsilon. Every normalized K-boson input has complete PNR output TV at
most delta=min(1,K sqrt(N(N-1)epsilon)). TV uses the half-L1 convention.
If U=U^T, the equal RANDOM mixture of V and V^T gives a symmetric proposal
on oriented K-subsets, with the same absolute error after the common collision
decoder and common Metropolis rule. This is a probabilistic mixture of two
channels, not the matrix (V+V^T)/2.

Dependencies, all internal elementary arguments:

1. Bosonic factorial-moment expansion -> exact unordered-pair expectation.
2. Uniform subset inclusion probability and collision bound -> q deficit.
3. Positive-support matching and finite subtraction -> stochastic decomposition.
4. Weighted assignment and entry phases -> monomial Frobenius error.
5. Tensor telescoping, bosonic restriction, trace/measurement contraction -> TV.
6. Transpose symmetry and inverse subset permutations -> symmetric replacement.
7. Shared conditional-history coupling -> trajectory and common score events.

There is no load-bearing numerical computation, external theorem citation,
unverified library convention or circular dependency. The decomposition normally
associated with doubly stochastic matrices is proved in the supplied text.

## Obligation matrix

| Obligation | Finding |
| --- | --- |
| Bosonic pair normalization | Passed: the coefficient is2 for UNORDERED pairs; distinguishable normalization would differ |
| Average over every K-subset | Passed: each fixed unordered input pair is included with probability K(K-1)/(N(N-1)) |
| Cancellation giving(12) | Passed only in the stated K>=2 domain; there is no missing factor of two |
| Positive-support perfect matching | Passed: the alternating-path reachable-set contradiction has the correct row/column masses |
| Finite convex decomposition | Passed: minimum subtraction and rescaling preserve row/column sums and strictly decrease support |
| Assignment, phases and Frobenius norm | Passed: one supported permutation has inner product at least ||q||_F^2; aligned phases give the stated constant |
| Every K-boson input | Passed: the operator bound is uniform; pure inputs give the trace bound and convexity includes mixed inputs |
| Symmetric classical replacement | Passed: transpose is a Frobenius isometry and induces the inverse subset permutation; averaging preserves TV |
| Shared Metropolis processing | Passed: common stochastic processing contracts TV; the fixed symmetric replacement satisfies detailed balance |
| Adaptive histories and T delta | Passed under the explicitly fresh/classically controlled, same-history hypothesis; it does not establish stationary Gibbs balance for an adaptive selector |
| Paid-best events and expectations | Passed for the common scored trajectory/initial incumbent, by coupling proposals and scores before acceptance |
| Costs, visited averages and relative gaps | Correctly limited: none is replaced by an unproved free-construction, empirical-average or relative-error assertion |

## Independent reconstruction of the constants

Write b_a=sum_i U_ai a_i and

    Z = sum_a n_a(n_a-1)/2.

On |1_S>, a repeated occupied input label cannot annihilate two photons.
For each unordered pair i<j in S there are two annihilation orders and two
creation orders in b_a^dagger^2 b_a^2. Consequently

    E[n_a(n_a-1)|S] = 4 sum_(i<j in S) q_ai q_aj,
    E[Z|S] = 2 sum_(a,i<j in S) q_ai q_aj.

The factor1/2 in Z is essential; the displayed source coefficient2 is correct.
Since a collision-free outcome has Z=0 and any K-photon outcome has
Z<=K(K-1)/2, the uniform expectation is bounded above by
K(K-1)epsilon/2. Independently, pair inclusion and row normalization give

    E_uniform E[Z|S]
      = 2 K(K-1)/(N(N-1)) sum_(a,i<j) q_ai q_aj
      = K(K-1)/(N(N-1)) (N-sum_(a,i) q_ai^2).

Canceling K(K-1)>0 proves(12). No independence between different collision
events is used, and no conditioning on collision-free observations occurs.

For the decomposition, start at an unmatched row of a maximum support
matching. If no augmenting path exists, each reachable column is matched to
a reachable row, apart from that initial row. Every positive edge from the
reachable rows ends in the reachable columns. Row mass is therefore |R|,
while those columns can receive at most |C|; |R|=|C|+1 is impossible.
This proves a positive-support perfect matching without invoking an external
matching theorem. Subtract its smallest positive entry alpha. If alpha=1,
q is that permutation. Otherwise the residual divided by1-alpha is doubly
stochastic with strictly fewer positive entries. Finite support gives a finite
convex decomposition and weights summing to one.

From q=sum_l w_l P_l,

    ||q||_F^2 = sum_l w_l <q,P_l> <= max_l <q,P_l>.

Choose such a supported P and put unit-modulus entries of V on its support,
with U's phases. Then V is unitary and

    ||U-V||_F^2
      = ||U||_F^2+||V||_F^2-2 Re trace(U^dagger V)
      = 2N-2 sum_(P support) sqrt(q_ai)
      <= 2(N-<q,P>)
      <= 2(N-||q||_F^2)
      <= N(N-1)epsilon.

Here Re trace(...) denotes the ordinary real part of the trace; no normalized
trace is intended. The chosen matching is supported on positive q entries, so
its phase choices are defined. The sqrt(q)>=q inequality applies entrywise.

The K-fold tensor difference is a sum of K terms with exactly one factor
U-V and all other factors unitary. Therefore its operator norm is at most
K||U-V||_op<=K||U-V||_F. Both tensor powers preserve the symmetric subspace;
restriction cannot increase the norm. For normalized output vectors u,v,

    trace_distance(|u><u|,|v><v|)
      = sqrt(1-|<u,v>|^2) <= ||u-v||.

Convexity covers mixed input states as well. PNR measurement contracts trace
distance, and TV cannot exceed one. This gives exactly(11), without an extra
factor2 or an assumption of collision-free INPUT beyond the averaging premise.
The measurement step also follows directly in normalized Fock coordinates:
half the sum of `||u_n|^2-|v_n|^2|` is at most
`||u-v||_2 (||u||_2+||v||_2)/2 = ||u-v||_2`, by Cauchy--Schwarz.

## Symmetry, histories and boundary cases

When U=U^T,
`||U-V^T||_F=||U^T-V||_F=||U-V||_F`. Both replacement channels thus satisfy
the same uniform K-photon bound, and convexity retains delta for their mixture.
If V sends an input port i to sigma(i), its transpose sends i to sigma^-1(i).
For a Fock input S the proposal is

    Q_C(S,T) = (1[T=sigma(S)] + 1[T=sigma^-1(S)])/2.

This is symmetric even for cycles longer than two. Phases do not alter those
occupation probabilities. The common collision-rejection map and acceptance
coin cannot increase the error. For a fixed U and beta, the usual symmetric-
proposal Metropolis detailed-balance identity from section2 follows. Neither
irreducibility nor a nonzero spectral gap is supplied by this construction.

For an adaptive controller, couple the COMPLETE proposal/score/acceptance
record at each common history, rather than only the accepted chain state.
The same classically controlled policy then selects the same U_t on that
history. Hypothesis(9) must hold for that entire selected matrix, averaging
over ALL K-subsets, at every such history. It yields a uniform conditional
failure probability at most delta. T fresh attempts give a disagreement
probability at most min(1,T delta). After histories disagree, no shared-choice
assertion is needed. This argument does not claim that the history-dependent
combined kernel has a single stationary Gibbs law.

Coupling proposals before acceptance also retains rejected scored candidates,
so a common paid-best threshold event differs by at most that TV. For the
nonnegative weighted cut objective, its range lies in[0,W], where W is total
graph weight. The difference of expected best cuts is at most W times TV;
there is no additional factor2. This statement uses the common initial
incumbent and common score functional, not separately added frontend results
or a redefinition of the scored record.

- **K=1:** correctly excluded. Every one-photon experiment is collision-free,
  including a nonmonomial two-mode Hadamard. Thus epsilon=0 would not imply a
  monomial U; cancellation of K(K-1) would be invalid.
- **K=N:** valid. The uniform average has one input subset; pair inclusion is
  one. The argument still constrains U. The collision-rejected subset chain
  itself has one state, so its chain comparison is trivially exact.
- **epsilon=0:**(12) forces ||q||_F^2=N. Each row has mass one and squared
  mass at most one, so every row is concentrated at one entry; column sums
  make q a permutation. U itself is monomial and delta=0. A symmetric U then
  has involutive underlying permutation, consistently with the construction.
- **Loose errors:** delta<1 requires the source's stated epsilon threshold.
  A useful T-attempt bound requires the stronger T delta<1. Absolute TV
  closeness cannot control the relative error of a tiny or zero gap.

## Scope, provenance and remaining work

No mathematical gap remains in this focused statement. The strongest safe
conclusion is existence of a monomial approximation and an absolute common-
attempt trajectory bound under the uniform collision-average hypothesis.
The permutation is not a supplied free resource: matrix acquisition,
assignment, updating it under a controller, RNG, scoring and every actual
per-step construction remain paid. No equal-wall-time or fair-budget optimizer
dominance follows from the existence proof.

Applying the statement to a policy requires a valid bound(9) for every matrix
chosen at every matching history. A collision rate measured only along visited
states, at one favorable start, or after discarding outcomes does not supply
that hypothesis. Construction precision/cost and any physical experiment need
their own reviewed contract. No additional numerical check is required to
complete this purely analytic audit, and none is authorized by this report.

Provenance: independent same-team subagent reconstruction in a new isolated
worktree, with shared broad research context; not external replication. Skills:
`mathbox:proof-audit`, then `mathbox:proofread-math` on this report only. Proof
leaves were checked internally, without browsing or importing a decomposition
result. Read-only shell/Git/hash inspection and symbolic reasoning only: no
code execution, numerical matrix evaluation, graph, RNG, test, sampler or QPU
call. The author proof and its hash are unchanged. Only this report was added;
existing tests were not run in this explicitly static subtask. The positive
research objective remains OPEN.
