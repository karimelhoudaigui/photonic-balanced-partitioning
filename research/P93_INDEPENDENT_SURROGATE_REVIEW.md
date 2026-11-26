# P93 — independent exact-source surrogate review

Date: 2026-11-26. **Primary verdict: proved as written.**

For the exact lossless source and shared normalization stated in P93,
the rank-two initializer decomposition and conditional raw-observation
stability bound follow. This does not assert that the residual is small,
that the surrogate can be sampled efficiently, or that optimization is
obstructed. No correction to the reviewed source is requested.

## Exact target and independence

Reviewed ALL 159 lines of theory/P93_LOW_RANK_INITIALIZER_SURROGATE.md
at commit 4b13a641462c4e23986a018589d0c5a3e94f38aa; file SHA256:
73d7ea2de810be90736e99843369f2d0a059e07d82d6779f8054f16a38a19fd4.
The committed blob and current source have that same hash.

The coordinate/source conventions were checked against the frozen
research/P90a_DEV_VETO_CONTRACT.md at 14d8dbdd, SHA256:
dfdcabfd93cf1a1e0d06fb370ad295123c1726247857820acab9f5d08d04c660.
That is a definition dependency, not experimental evidence. Its target-
row/source-column convention, paired rank orders, shared p=1/2 splitter,
occupied frame [I;iW]/sqrt(2), pre-R compilation and full counts agree.
No other P93 review or P90 implementation/result was consulted.

This is a separate non-author manual correctness audit, using ROOT's
specified checklist. It is not a before-author reconstruction or an
independent discovery claim. The author's printed verdict is not a
premise. Review skills: mathbox:proof-audit and final proofread-math.

## Claim and dependency chain

Fix K>=1, a real graph block B and real paired vectors u,v. Use exact
Hermitian H=H0+E, original d=max(1,||H||op), and compare exp(-iH/d)
with exp(-iH0/d). Given a common conditional certificate delta for their
operator-norm distance, the raw observation laws obey

    TV(P_raw,Q_raw) <= E[min(1,r delta)] <= min(1,K delta/2),
    r ~ Bin(K,1/2).

For at most T measured/reset attempts with the SAME observation-driven
policy and conditional certificates delta_h, the transcript bound is
min(1, sum_j E_P[min(1,K delta_(h_j)/2)]).
The dependencies are: fixed-coordinate algebra -> Hermitian norm bound
and rank -> shared-d Duhamel estimate -> symmetric tensor lift -> pure-
state/measurement estimate -> common-R mixture -> common kernels and
first-mismatch coupling. All are finite-dimensional internal arguments;
no external theorem citation or load-bearing computation is required.

| Obligation | Source lines | Result |
|---|---|---|
| Signs, transpose pairing, Hermiticity, residual norm | 10–35 | Passed |
| Shared d and Duhamel orientation | 39–58 | Passed |
| Rank of V0-I, not physical crossrank | 60–62,145–148 | Passed |
| Normalized CF branch source and common R law | 66–77 | Passed |
| Bosonic tensor lift and trace/TV constants | 79–100 | Passed |
| Joint R/count mixture, vacuum and source charge | 102–112 | Passed |
| Same postprocessing and conditional transcript coupling | 116–138 | Passed |
| Small residual, efficient sampler, performance or hardware | 142–159 | Not established; explicitly unclaimed |

## Decisive algebra and probability checks

Writing z=(u-v)+i(u+v), the real part of H0 is
[(u-v)1^T+1(u-v)^T]/2 and its imaginary contribution is
i[(u+v)1^T-1(u+v)^T]/2. These reproduce the u1^T-1v^T
contribution to H exactly. The remaining part is
(B+B^T)+i(B-B^T)=(1+i)B+(1-i)B^T.
Its adjoint equals itself because B is real; no symmetry of B is needed.
The triangle bound is 2sqrt(2)||B||op, with no missing factor of two.

For F(s)=exp[-i(1-s)H/d]exp[-isH0/d], F'(s) is
i exp[-i(1-s)H/d](E/d)exp[-isH0/d]. Since F(0)=V and
F(1)=V0, integration gives the source's MINUS-i formula for V-V0.
Both factors are unitary even when H and H0 do not commute. Replacing d
by a separate surrogate normalizer would invalidate that step; P93
explicitly retains d. Rank(V0-I)<=rank(H0)<=2 follows from its kernel,
including rank-zero/one degeneracies and possible exponential aliasing.

The physical source expands as 2^(-K/2) times the product over inputs i
of [a_i^dagger+i sum_a W_ai b_a^dagger]. Choosing transferred inputs R
leaves distinct kept occupations, so different R branches are orthogonal.
Within a branch the receiver columns are orthonormal: the product of
their creation operators is a NORMALIZED r-photon CF input transported
by W. Thus each R has probability exactly 2^(-K), not a permanent-
weighted branch probability. Measuring all kept counts identifies R.

The unitary identification between normalized occupation states and
Sym^r(C^K) includes their usual factorial normalization. Gamma_r(W) is
therefore W tensor ... tensor W restricted to that subspace, not an
independent-photon replacement. Tensor telescoping costs r delta;
there is no r! factor. If c=<psi,phi>, then
(2-2Re c)-(1-|c|^2)=|1-c|^2>=0. Trace distance and PNR contraction give
TV<=min(1,r delta). At r=0 both branches are the same vacuum.

Because the joint alphabet retains R, summing its disjoint probabilities
gives the stated TV equality. Omitting R would instead give an upper
bound, which would remain safe. Common pre-R marks can be conditioned
on and then averaged; if certificates depend on those marks they must
be included in that conditioning/conditional expectation. No accepted-
sector renormalization occurs. E[r]=K/2 reduces the error bound, not the
K-photon injected cost of an attempt. K=1 and delta=0 are consistent;
the separately stated K=0 vacuum case is also consistent.

At each matching history use the same next-input/coin law and a maximal
coupling of its two observation kernels. The mismatch contribution is
bounded by E[1_matching epsilon_h]<=E_P epsilon_h since the first
marginal remains P. After a mismatch no favorable coupling is assumed.
Common observation-based stopping can be padded. This does NOT couple
unequal runtime policies, private matrix-driven decisions, persistent
coherent memory or transcripts containing deterministic V/V0 tags.

## Boundaries and disposition

Rank(V0-I)<=2 is in the paired receiving coordinates. Independent row/
column port permutations need not preserve rank(W0-I). More decisively,
the physical source-to-receiver block iW0/sqrt(2) has rank K. Consequently
this is not a rank-two application of P69 to the kept/receiver partition.
It neither eliminates bosonic collisions nor supplies a classical sampler.

No actual residual, graph or probability was evaluated. Its envelope may
equal one; no favorable graph or numerical rounding behavior is inferred.
The strongest safe result is exactly the conditional mathematical bound
above. There is no remaining implication needed for that stated result;
any practical small-error or sampling claim would require new evidence
and separate authorization. No such followup is initiated here.

Validation was limited to reading, file/committed-blob SHA256 and Git/text
checks. No imports, AST parsing, tests, role hashes, RNG, graph generation,
matrix/probability program, native call, experiment, B-data access, P90
change, manuscript or QPU action occurred. Only this new review is written.
