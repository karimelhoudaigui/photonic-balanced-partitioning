# P134 — independent prospective design/math review

Reviewed 2026-11-26: complete128-line card, commit `c9cbb7580597664f052c0f343b853dafd44c6096`,
`research/P134_FIRST_DISCRIMINATOR_DESIGN.md`, SHA256
`318244b4cf840efd137671469e1c519fac09321779905276a7125d9ecbc23541`.
Also read the complete ROOT decision `9ef2b3d05e13ab5b99ed0b05c46c6c0388b53541`,
`reports/P133_P134_ROOT_DESIGN_CHECKPOINT.md`, SHA256
`540ec8c38e04e925daf94a8932a42c768bc8c115542ee558011efbacf96e9728`.
Both current files matched their frozen Git identities. Reviewer did not author the card.
No moving implementation or P130/P131 scientific payload was inspected; no graph draw, import, AST, script, numerical worker, RNG or native call occurred.

**Primary verdict: conditional on the future implementation satisfying this exact card and ROOT override.**
The mathematical controls, hand cases and nominal counters are consistent; no material design error was found.
This is a static design pass, not qualification of an implementation or evidence of a useful optimizer signal.

## 1. Graph/data flow and exact candidate costs

Two topology seeds, two weight seeds and two mark seeds specify six separate prospective MT streams.
Canonical sorted min/max edges make weight assignment independent of incidental edge-iterator ordering.
The named NetworkX/Python versions, calls, weight range and permutations must be pinned in the later source/binding.
There is no connectivity/opportunity filter, replacement, retry, planted cut, or held-out claim.
This fixes a two-context DEV screen, not a representative-performance guarantee or proof of stochastic independence of seeds.

S has12 vertices, R has4, S0 has8, and every Y is a four-subset of the six receivers in S^c.
Thus S0 union Y is balanced, disjointness is automatic, and each proposal is a four-swap from S.
The residual identity from P132/P133 remains exact, with d_j including edges outside the receiver pool.
The34 whole-edge calls are17 per graph: current S, baseline S0, and15 lifted candidates.
The30 incremental evaluations are one per candidate, not additional graph selections.
C(S0) is an IMBALANCED algebraic baseline; it must never be credited as an eligible feasible candidate.
The15 lifted candidates and the known prototype are all credited to controls; the prototype is already one of the15.
Receiver/column/mark index maps must be explicit in the frozen source, including the last-four occupied input columns.
No minimum or argmin may enter compiler construction merely because the frontier has been scored.

At kappa=0, F is a diagonal-scaled prototype injection, so T has one receiver per occupied source.
There can be no same-signal-mode collision and no other CF target; every species profile has the same raw law.
At beta=kappa=0, T is the exact injection and the prototype event has probability1.
These endpoints are useful nulls and credited classical candidates, not interference gains.

## 2. Species convolution, buckets, and all-signal masses

For a fixed source partition, different species inhabit orthogonal internal Fock spaces.
For CF Y, each allocation of output vertices Y_A to a species block A is mutually exclusive in the unobserved colors.
Within one allocation its amplitude factorizes into `prod_A per(T[Y_A,A])`.
Squaring and summing allocations proves (1), with NO species factorial, output factorial or success denominator.
Every input block is itself CF and every receiver vertex is occupied only once in this observable.

Equivalently, assignments in one source-color-sequence bucket differ only by permutations inside the blocks.
The bucket amplitude factors as that same product of block permanents; distinct buckets add incoherently.
This proves the independent bucket comparison and distinguishes it from coherent color erasure.
The listed restricted-growth strings are exactly all15 partitions; 0000 is B and0123 is D.
Each of the14 proper profiles needs its own grid maximum, rather than a same-setting-only comparison.

For one block A, restricting all its photons to signal modes gives norm squared `per((T†T)[A,A])`.
Tensor factorization across orthogonal species therefore gives `prod_A per(G[A,A])`.
It is not a product of independent column survival probabilities except for the fully distinct profile or special Gram matrices.
Subtracting CF mass leaves only ALL-SIGNAL collisions; its complement is the dump mass.
A record with any dump photon and also a receiver collision belongs to dump, not both bins.
The three disjoint bins sum to one without observing or approximating individual dump patterns.

## 3. Four-cycle coefficient and limits of its interpretation

Take sigma,rho as maps from ordered output slots to source indices.
The relative source permutation `sigma composed rho^(-1)` preserves species colors iff the assignments lie in one bucket.
A single four-cycle can preserve the partition only if all four source colors agree.
Consequently every such cross term is absent from EVERY proper partition at the same T.
There are `(4-1)!=6` four-cycles, with24 possible rho, hence144 ordered pairs.
Reversing sigma,rho conjugates the term and inverts the cycle, so the full sum is real.
There is no extra one-half factor; the ordered-pair sum already contains both conjugate contributions.
Double transpositions are not in this class; all signed contributions must be retained.

With loss/collision holds, h_Y is zero outside receiver-CF records, so J4 is exactly this class's raw utility contribution.
It is not the full B-minus-proper difference, a probability law, or a causal isolation experiment.
Other cycle classes and their retuning can alter the same utility.
A strict grid winner plus positive selected J4 therefore supports only the stated follow-up label, not unique-four-cycle causality.
First-grid tie breaking must also apply when another tied setting has a more favorable J4; no postselection of that sign is permitted.

## 4. Hands and the full-unitary cross-check

For F=[I4;0], H=I, T is the prototype injection and D=0.
Only one assignment contributes, giving CF1/collision0/dump0 and C4=0 in every profile.
In the second hand, the first two signal columns are `(2/3)[[1,i],[i,1]]` and the other two are deterministic spectators.
Their signal Gram is diag(8/9,8/9,1,1), hence all-signal mass64/81 and dump17/81 for every partition.
If sources1,2 share a block their receiver coincidence permanent cancels: CF0 and collision64/81.
Otherwise the two labeled paths give CF32/81 and collision32/81.
Only identity/transposition assignments survive the spectators, so C4=0. These are count-law hands, not utility examples.

Four photons in ten modes have `binom(13,4)=715` full occupations.
With the last four inputs CF, their probabilities have output divisor `prod_j n_j!` and no input factorial.
The fixed ER/beta1/2/kappa1 full-U check can therefore independently recover normalization and the three reduced B masses.
Its graph or spectrum becoming degenerate is not permission to replace the point.

## 5. Population and decision contract

There are18 matrix contexts,270 profile totals,4050 CF/profile rows and270 C4 rows.
Per context `sum_l binom(4,l)binom(6,l)=1+24+90+80+15=210`, including the empty permanent.
Thus3780 DP/Ryser minor rows are required; the15 nonempty principal Gram subsets give another270 rows.
The nominal row sum is

    18+270+4050+270+3780+270+2+30+715+1+2+30+2+1 = 9441.

The18 matrix-context rows are essential: all remaining categories alone sum9423.
Each matrix row must contain the archived F/H/Q/T/D/U rather than silently adding or omitting nominal rows.
Error diagnostics may add failure evidence but cannot create a nominal complete PASS.

Maximizing raw expected utility separately over the same eight settings is a valid grid-only comparison.
If either graph ties/loses to a proper profile, the stated NO_STRICT_GRID_SIGNAL follows; a zero-opportunity graph is retained and flagged.
Both strict graph wins with nonpositive selected J4 give the intermediate label; strict wins with positive J4 give FOLLOWUP ONLY.
The credited deterministic frontier has maximum utility at least every expected utility, so none of these labels is an optimizer win.
Continuous retuning, fresh contexts, practical full-cost controls and held-out replication remain open obligations.

ROOT's pre-data override is CPU120/wall180, preserving the card's proposed60/90 as history.
The future source/population/TEMPLATE must enforce that override, one worker, six thread env vars1, Python -B, science16MiB with1MiB final reserve, logs4MiB,
logical256MiB PLAN, zero retries/precision rescue/native photon draws, and fresh bound outputs with raw sealing before interpretation.
No timing calibration or prior outcome justified the override; a resource failure remains inconclusive.
This review authorizes no factory, code execution, new population, native follow-on, hardware access, paper change or positive claim.
