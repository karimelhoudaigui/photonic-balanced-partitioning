# P90a independent prospective-card review

26 November 2026. **Verdict: no material card-level blocker found; suitable
for separately authorized CODE ONLY implementation.** No implementation,
import, qualification, native query or main is authorized by this review.
The proposed optimization benefit remains unproved.

## Exact authority and reviewed population

Card: `research/P90a_DEV_VETO_CONTRACT.md`, all 180 lines, commit
`14d8dbdd875bac9d443b310d63abad31c660ccd0`, SHA-256
`dfdcabfd93cf1a1e0d06fb370ad295123c1726247857820acab9f5d08d04c660`.
Producer worktree: `.local/p65-independent-audit`.

For context, the complete P90 design (171 lines, c52afab, SHA
`b3c0b04c486f3368a0cbbc7e2030d8225d015f182cbfb00e0a9b63e0a0b2f173`)
and exact mathematical review (166 lines, 1412c9a, SHA
`ad2a473b7b37da806b7e327e07ca6273278dbbffd0f6cf5d271a99865589f4d5`)
were read. The immutable P50 implementation was reread completely as text,
SHA `6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86`.
P43's existing pin is `b0507d36`. The bounded literature note's hash
`fa1c2be4a2b148450653207befe4cd4647dfef10f1147b0d1b03ce978a94e831`
was checked, but its external sources were not reaudited or browsed here.
No novelty claim is admitted by this review.

## Physical model, causal compiler and P89 boundary

The real target-row/source-column array M is the transpose of an
inside-major swap-delta table. Removing s and adding t changes cost by
`ell_t-ell_s+2*w_st`, so every `C(S)+M[a,i]` is an actual feasible neighbor
cost. Rank-sorted source/target lists explicitly identify the common index
space used for the symmetric/skew decomposition. H is Hermitian,
`d=max(1,max(abs(eigvalsh(H))))` is positive and V is unitary in exact
arithmetic. Neither nonflatness nor a beneficial mean sign is guaranteed.

V is built before sigma/tau and before R. The latter orderings transport
coordinates only: W is V with corresponding row/column permutations.
The full occupied frame is physically valid, since

    U = diag(I,W) * [[I,iI],[iI,I]]/sqrt(2)

is a 2K-mode passive unitary whose first K columns are `[I;iW]/sqrt(2)`.
Thus kept-bank detection fixes the transferred input columns, giving raw
weight `2^-K * |per(W[y,R_ports])|^2 / product(y!)`. Summing the conditional
lossless Fock law gives marginal mass `2^-K` for each removed port set.
All r, vacuum transfer, collisions and photon costs are included.

Unlike the P89 source-blind receiver, the transported W retains the actual
labeled column correspondence. At fixed r, labeled R remains uniform,
while Y can depend on `V[:,R]`. This is not control of the marginal R and
does not make the classical one-photon routing contribution quantum.
There is no after-R compiler, optimum mask, known solution or C* input.

The prescribed numerical Gram/full-frame guard fails rather than repairs
a matrix. Null/monomial V values remain data. Public 12-photon/24-fibre
context is not an account, connectivity, PNR or loss certificate. The ideal
lossless decoder cannot fill hardware losses as though they were collisions.

## Candidate accounting and clock obligations

The card requires all 144 compiler costs and canonical masks, all warmstart
and Q neighbors, duplicates and rejected candidates to be materialized and
credited. Current, own-chain scored best, endpoint best and global all-paid
best are distinct. Compiler discoveries cannot be relabeled optical gains.

Compact arrays are legitimate only if actual integer cuts/masks and their
best-state updates exist before the owning end clock. Later audit dicts may
serialize these arrays; they cannot compute/select a missing best witness.
No per-candidate timestamps are invented. These are source-review obligations,
not facts established about future implementation by this card.

Paid B WALL spans and factory residuals are disjoint and typed. The P43
reported setup WALL has unknown CPU/endpoints; its paid residual links both
operands once. P50 direct/outer/reported records and separate CPU/WALL gaps
are retained, unclipped. Last chronological pre-clock masks qualify only under
both conservative inequalities. There is no equal-CPU, real-time API return
or matched optical-resource claim hidden in the zero-optics proxy.

## P50 guard and trace bound checked from the immutable source

At n24 the helper's epoch is 192 and its normal anneal chunks are 32.
Each complete descent checkpoint costs 144 work. Every cheap restart or
perturb checkpoint can be paired with its following first 144-scan, except
at termination. These disjoint two-checkpoint groups cost at least 145
work, exceeding two 32-work allocations. The initialization and one setup
checkpoint, and a possible terminal partial chunk/unpaired cheap checkpoint,
are covered conservatively by the card's additive four.

Consequently `trace_count<=floor(work/32)+4<=31,254` at the frozen one-million
work guard, below 40,000. The n24 divisible epoch matters: ordinary epochs
do not introduce repeated short chunks. Export is not a new checkpoint.
The guard and trace limits are prospective; no helper timing was measured.

The 64 MiB one-control workspace and 80-byte compact-record estimate remain
logical plans, not RSS/native-allocation certificates. Actual 32 MiB total
scientific capacity, final reserve and global CPU60/WALL90 limits must be
enforced. A cap failure is inconclusive, without rerun or outcome-based boost.

## Controls, decision and qualification

All four independent FAST calls receive their own whole G and private raw
setup/seed; no B incumbent, priority or matrix is donated. Inadequacy of any
required control forces inconclusive, including an early guard-limited call. This
is deliberately conservative, even when a partial record looks favorable.
Only complete adequate panels can reach NO_POSITIVE_SIGNAL on any failed
strict B inequality, or FOLLOWUP_REQUIRED if B strictly beats every named
mode on both anchors. The former is a necessary-gate failure, not a newly
pooled classical portfolio; the latter is not a positive result.

Independent D reoptimization, group/low-r/intensity/routing/repair controls,
full-feature classical search, relabeling, fresh seeds, held-outs and
replication remain mandatory later. None is automatically launched, and
`positive_accepted` is always false. No paper or QPU gate is passed here.

The qualification count is correct: 3 HOM, 6*10 flat two-photon outputs
and 191 nonempty toy points total 254; the toy count is
`4*4+6*10+4*20+35`. All 16 removed subsets include analytic vacuum, with
at most four receiving photons/modes per native point. At p=1/2 the
raw toy law gives `-1/96-1/64=-5/192` against D. The two-photon-group
control reproduces its entire block-factorized count/repair law, so its
advantage gate must fail. No selected-sector conditioning is allowed.

One nonblocking interpretation constraint should carry into the fixtures:
the flat uniform-R null is the sourced inclusion/mean cancellation, not an
unsupported equality of the joint (R,Y) law or of nonlinear quench histories.
The card's exact P90 dependencies delimit that null. The full 96-attempt
workflow qualification must keep compiler/scorer/factory/RNG/clocks mocked,
with no K12 native sample, DEV graph or production role digest.

## Disposition and provenance

Proceed only to a separately authorized, isolated implementation freeze.
Source/tests/literal spec/both v2 contracts/full pins and a prospective
independent checker require review before any import/collection/execution.
Runner results must be strict children of a fresh output parent. Actual
pre-clock arrays, typed ledgers and query population are the next checks.

This is a separate static reviewer, aware of the card's disclosed P82 guard
history; it is not a blind-outcome extension or discovery claim. Only text
reads, hashes, hand algebra and isolated report/Git operations were used.
No card/source edit, seed evaluation, graph, import, AST, test, RNG,
probability/native query, calibration, experiment, B-data interpretation,
QPU or manuscript action occurred. The positive research objective is open.
