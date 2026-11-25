# P66 independent review of the author's exact frozen proof

25-Nov-2026. **Primary verdict: proved as written.** This verdict covers the
restricted ideal warm-start theorem, connected extension and exact graph-only
equivariance corollary in the exact artifacts identified below. It does not
establish a positive optimizer, an all-graphs obstruction, a typical-start
result, hardware performance or novelty.

## 1. Exact audit target and provenance

Author commit: `2bcf84b82781cdf2bf8379e61fa5e9071aa25bbc`, branch
`research/p66-dark-barrier`.

| Artifact | SHA256 | Coverage |
|---|---|---|
| `theory/P66_bright_dark_barrier_obstruction.md` | `73b16001bbfb5400c1261e7e48d69751d44ff8e034cc00e38cb8c017d1545c70` | All 392 lines, sections 1--11 |
| `research/P66_BRIGHT_DARK_ROUTE_NOTE.md` | `8cebb12c4e364c8f2cd267e24a28bd268dfcad78f32b4034a79af55f7b336259` | Entire route note |

The reviewer's independent core/connected derivation was frozen BEFORE
reading these author artifacts, at commit
`eae1ddabb215c9dfda05ea9bdcc286a6698ba0ad`, file
`theory/P66_independent_bright_dark_audit.md`, SHA256
`7cb9a101155df7b1e9c5c7a219c3877e74b6246195952356801d86cb6cb973a9`.
The separate exact-covariance derivation was also frozen before this read:
`research/P67_exact_covariance_symmetry_obstruction.md`, SHA256
`63f891ca6b03790024bbade59d275e8f115dfccc1fa17c9632aa7ca878c25cf8`.
The coordinator preserved that exact file centrally after this worktree's
Git index became unavailable. No author's P66 proof or verdict was read
before the independent derivations. The reviewer did receive the same
candidate formulas and suggested arguments from the coordinator, so this
is independent rederivation of critical steps, not independent discovery.

No scientific code, import, graph generation, matrix computation, random
experiment, source qualification test, external theorem lookup or QPU call
was executed for this review. File reads, line numbering and SHA256 reads
established the exact target. The author's child-review assertion is not a
dependency of this verdict; its separate report was not read or relied on.

## 2. Normalized claim and dependency reconstruction

The quantified family has N=4L,K=2L,L>=2; four equal cliques of weight M>0;
two matched clique pairs of weight h>0; and M(L-1)>Lh. A prescribed current
whole-clique state lies in the four-state set B. Each fresh source is the
normalized CF Fock state for that current subset. Collision attempts are
paid self-loops; no CF conditioning is applied. The accepted source is
updated by the stated zero-temperature or finite-temperature rule.

Allowed one-particle matrices preserve both specified dark subspaces. The
author proves this for scalar spectral functions, Cayley transforms and,
separately, deterministic exact graph-only equivariant maps. A history
controller can select among allowed matrices, with the property imposed on
each realized matrix, not merely on its distribution.

The proof chain is:

    balanced clique gap
      -> exactly two improving CF targets
    separate dark-subspace preservation
      -> commuting Fock number projectors
    source support + exact source projector norm
    target support + factorial moments + target projector tail
      -> two-sided amplitude bound
      -> uniform conditional direct-improvement hazard
      -> first-exit trajectory bound.

All these leaves are proved in the author's text. The asymptotic envelope
uses elementary factorial integral inequalities. No external load-bearing
result or numerical certificate remains unverified.

## 3. Critical obligations and exact locators

| Obligation | Verdict | Author locator and decisive check |
|---|---|---|
| Balanced cost landscape | Passed | Section 2, lines 60--77: one partial clique is incompatible with balance; each of at least two contributes at least M(L-1) |
| Cayley/scalar spectral class | Passed | Section 3, lines 86--108: adjacency and J-I preserve both orthogonal dark subspaces; Hermiticity makes Cayley unitary |
| Degenerate spectral caveat | Passed | Lines 105--108 correctly exclude arbitrary unitaries merely commuting with H; degenerate cross-block dark mixing need not preserve the projectors |
| Passive Fock lift | Passed | Lines 110--126 use dGamma(projector), distinguish one-attempt conservation from measurement/repreparation along a trajectory |
| Source projector norm | Passed | Section 4, lines 130--143: normalized CF input and sqrt(L!) overlap give exactly L!/(2L)^L |
| Target factorial moments | Passed | Section 5, lines 152--168: m! ordered annihilations per hole set, orthogonal residual states, and the correct single m! cancellation |
| Target tail | Passed | Lines 174--184: valid s in (0,1), correct optimizer, minimum with one |
| Two-support amplitude projection | Passed | Section 6, lines 188--206 explicitly supplies BOTH support identities and exchanged projector for the second target |
| Adaptive zero-temperature bound | Passed | Section 7, lines 210--226: uniform conditional bound on every still-bad history, with no independent-shot assumption |
| Finite-temperature adaptation | Passed | Lines 228--249: accepted uphill exits use the gap, random beta uses unconditional expectations with the survival indicator |
| Exponential constant | Passed | Section 8, lines 253--274: correct upper/lower bounds on the explicit bound constant r_L, and necessary exponential attempt scaling |
| Connected extension | Passed | Section 9, lines 282--309: exact cross-cut expression, positive good cost, preserved gap, rank-one cross adjacency, reciprocal beta scaling |
| Classical certificate | Passed | Lines 311--317: M>h>w identifies heavy cliques; the six whole-clique unions include the only better targets and dominate all partial states |
| Exact-equivariance corollary | Passed | Section 10, lines 327--359: independent transitive subgroups, their average projectors, and separate pathwise invariance |
| Limits and actual P65 schedule | Passed | Section 11, lines 364--392: prescribed warmstart, W and N/W correct, fixed-j beta*g need not grow, no actual P65 no-go claim |
| Route-note calibration | Passed | Its formulas and restrictions agree with the exact proof; no extra scientific conclusion is introduced |

The tuple/projector dimensions are consistent throughout: each one-particle
dark space has dimension 2L-1, the total photon number is 2L, the source has
L photons in each block, and the target has all 2L in one block. Distinct
complementary subsets are correctly counted as separate Fock events.

## 4. Checks against plausible overstatements

The projection bound would be false as a general consequence of Pi commuting
with Gamma(U). The author does not make that inference: lines 188--195 use
Q_A|source>=|source> and Q_B|target>=|target>. This agrees with the reviewer's
independent two-projector derivation.

The lower bound on r_L in section 8 is a lower bound on the explicit upper-
bound CONSTANT, not on any actual transition probability. The author uses
it to identify the exponential scale of that constant. The necessary raw-
attempt lower scaling for constant success follows from the upper hazard
bound, with no achievability or tightness claim. No measured wall-time
conclusion is smuggled in.

The connected extension has positive target cost 4wL^2. It remains a
structured family with an elementary classical solver. Removing graph
disconnection does not make it a hard benchmark, and the text says this.

The equivariance corollary is graph-only and exact for each realization.
Its exclusion of covariance in law, current-subset arguments and additional
modes is explicit. The separate P68 current-dependent proposed extension
uses rank-two bright spaces and a different constant; it cannot be silently
inserted into this rank-one corollary or treated as covered by this audit.

The theorem neither bounds the probability of reaching B from a uniform
start nor proves trapping for P65's actual normalized anneal. The first-
exit inequality may be vacuous at finite temperature. These limitations
are load-bearing and are preserved in the route note.

## 5. Remaining gap and disposition

No mathematical correction is required for the exact scoped claim audited.
No inference of novelty, typical-instance optimization difficulty, quantum
advantage, positive held-out replication or QPU readiness is supported.
Those remain separate unresolved scientific requirements.

This review is file-only and has no executable changes. No tests were run,
in accordance with the static-only instruction. A future exact small-case
implementation check would require a prospective computation contract; it
would not replace the proof or widen its scope. No change to paper/ or raw
experimental data was made.
