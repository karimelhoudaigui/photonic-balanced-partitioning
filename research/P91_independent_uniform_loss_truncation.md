# P91 independent hand reconstruction: uniform-loss truncation

**Verdict: the candidate reduction and absolute-TV bound are valid under the
operator-norm hypothesis and known collision-free source stated below.**
Replacing that hypothesis by a mean efficiency is invalid. This note was
derived before reading any P91 author file, review or output. It is static hand
mathematics: no code/import/AST/test, seed, RNG, graph, numerical execution,
native backend, experiment, QPU or manuscript was used or changed.

## Exact channel and source assumptions

Let T:C^m→C^n be the one-particle transmission matrix of a passive channel with
vacuum environments and ideal PNR observation of the n retained outputs.
Assume a supplied, pointwise certificate `||T||op²≤eta`, with0<eta<1. The input
is the known normalized Fock state |S>, with k distinct singly occupied input
modes S⊆{1,...,m}; all other inputs are vacuum. No inaccessible entangled source
or retained quantum memory between attempts is supplied to the simulator.
Let s≥0 be an integer. All statements concern the entire observed raw PNR law,
including vacuum, every loss sector and all collisions, rather than a heralded
or collision-free conditional law. TV means `sup_A |P(A)-Q(A)| = (1/2)||P-Q||1`.

Put T'=T/sqrt(eta), a contraction. Passive vacuum channels compose by multiplying
their one-particle matrices, hence

    Phi_T = Phi_T' o uniformLoss_eta.                    (1)

One direct noise check is instructive. Uniform loss first gives
`a1=sqrt(eta)a+sqrt(1-eta)e`; the next channel gives
`b=T'a1+Lf`, with vacuum e,f and `LL†=I-T'T'†`. The resulting transmission is T
and the total vacuum-noise covariance is
`(1-eta)T'T'†+I-T'T'†=I-TT†`. A vacuum-mode isometry identifies this combined
linear noise with the canonical square root of that matrix. Hence the complete
channels agree even on Fock inputs; this is not merely moment matching, a
replacement by distinguishable photons or a thermal-noise approximation.

Uniform attenuation of the occupied input modes has joint system/environment
state `sum_R eta^(|R|/2)(1-eta)^((k-|R|)/2)|R>|S\R>_env`.
The environment Fock patterns are orthogonal for distinct R, so tracing them
gives exactly

    rho_after = sum_(R subset S) eta^|R|(1-eta)^(k-|R|) |R><R|.  (2)

Therefore r=|R| is Bin(k,eta) and R given r is a uniform r-subset of S.
This labels occupied modes, not individual bosons. Conditional on R, the
remaining photons are still indistinguishable and may exhibit full r-photon
interference in T'. There is no inter-R coherence to approximate in this known
input case. The same simple uniform-subset description is not asserted for an
arbitrary unknown coherent superposition of Fock inputs.

## Small-particle exact simulation, and what exact means here

For completeness, a finite passive vacuum dilation exists explicitly. Put
`A=(I_n-T'T'†)^(1/2)`, `B=(I_m-T'†T')^(1/2)` and

    U = [[T', A], [B, -T'†]].                             (3)

This square (m+n)-mode matrix has row blocks n,m and column blocks m,n.
Its diagonal products are identities; its off-diagonal product vanishes since
`T'B=AT'`, verified on each singular vector. Thus U is unitary, and its first
m input modes followed by the first n observed output modes realize Phi_T'.
The remaining input modes are vacuum; the extra output modes are discarded.

Draw r and R from (2). When r≤s, enumerate the occupations z of m+n modes with
sum z=r. For source R the normalized probability is
`|per U[z,R]|² / product_j z_j!`; input factorials equal1. Unitarity of the
bosonic lift gives total mass1. Sample this law and retain only the first n
counts, thereby tracing the dilation outputs. This permits further losses in
T'; observed photon number is at most r and need not equal it. The r0 branch
is genuine vacuum. There is no full-k Fock enumeration or approximation of
the interference among the retained r photons.

Here “exact” is the **ideal-real probability/arithmetic oracle model**. The
dilation, square roots, complex permanents and random-real comparisons have
their mathematical values. There is no proved efficient exact Turing sampler,
finite-bit precision bound, numerical stability estimate or runtime benchmark
in this note. For fixed s the displayed enumeration has at most
`binom(m+n+s-1,s)` output occupations per retained sector and each permanent
can be evaluated with an s-particle finite algorithm. Its actual expense is
not zero; if s grows, this expression is not a generic polynomial bound.

## Whole-law truncation bound

Let q=Pr[Bin(k,eta)>s]. For r>s return an explicit FLAG, or a declared cheap
fallback whose output/flag provenance is retained. Couple the ideal simulator
with the true channel using the same latent r,R and the same exact conditional
count on r≤s. They can differ only on r>s. On the common observation space,
embedding the true law with no flags,

    TV(P_true,P_truncated) ≤ q.                           (4)

For a distinct FLAG and no fallback substitution, equality holds: the simulator
replaces exactly the q bad-sector subprobability by q mass on FLAG. A registered
physical-output fallback can only reduce this upper bound; a simulated vacuum
fallback must not be represented as an actual observed vacuum draw.
Never delete flags and renormalize while claiming the same whole-raw law.

For 0≤s<k, `1_(r≥s+1)≤binom(r,s+1)` and the binomial factorial moment is
`E binom(r,s+1)=binom(k,s+1)eta^(s+1)`. Hence

    q ≤ min(1, binom(k,s+1) eta^(s+1)).                   (5)

For s≥k, q=0 and no truncation is needed. For s0, the bound is q≤k eta;
for T=0 the physical output is vacuum, and an explicit vacuum fallback can be
exact even when the auxiliary uniform-loss flag bound is loose. These are
absolute-distribution statements, not relative guarantees for rare events.

Any common classical decoder, scoring/quench kernel or randomized postprocess
contracts TV, provided its randomness and rule are the same and it receives
only the compared observations. The latent R is private simulator randomness:
it cannot be gifted to an optimizer if the physical observation does not reveal
it. Computational wall times and simulator-internal tags have no automatically
matching physical counterpart. A quench driven by actual runtime needs its own
timing comparison, rather than an appeal to (4).

## Adaptive classical observation histories

Consider at most J attempts, with no coherence between attempts. At a common
classical history h, both processes use the same source/channel/action policy,
including shared classical policy randomness. Each input must again have its
known CF description, and each chosen channel must satisfy its certified
norm bound at that history. Suppose the next compared observation kernels
satisfy TV(P_j(.|h),Q_j(.|h))≤epsilon_j(h), as above.

A sequential coupling until the first differing observation, or telescoping
hybrids, gives the safe uniform bound

    TV(full observation transcripts) ≤ min(1, sum_j sup_h epsilon_j(h)). (6)

More precisely the hybrid expansion can use
`sum_j E_(h drawn from the true prefix law) epsilon_j(h)`, when those pointwise
bounds are available. Observational stopping rules can be represented by an
absorbing STOP state under the fixed J cap. This does not compare wall-clock
trajectories, policies with hidden quantum memory, or two algorithms allotted
different numbers of attempts by their measured runtimes.

Rare conditioning cannot be added for free. Take distinct outcomes o,a,b, with
P(a)=epsilon, Q(b)=epsilon and P(o)=Q(o)=1-epsilon. Their raw TV is epsilon,
but conditioning on the rare event {a,b} gives TV1. A heralded conclusion
needs an appropriate success-probability/error analysis and all discarded
attempts paid, not merely the absolute bound (6).

## Conditional illustrations and the mean-efficiency obstruction

If eta=1/50 is genuinely an operator-norm upper bound, s3 and J96 give:

| Known k | One-attempt union bound | 96-attempt bound |
|---|---|---|
| 12 | `495/50^4 = 0.0000792` | `47520/50^4 = 0.0076032` |
| 8 | `70/50^4 = 0.0000112` | `6720/50^4 = 0.0010752` |

These are upper bounds from (5)/(6), not exact tails or measured efficiencies.
They require the pointwise norm certificate at every relevant adaptive history.

The supplied CEA public-description context—12 photons,24 fibres and a mean2%
figure—is not authenticated or converted into a calibration in this note.
Even interpreting “mean” favorably as `Tr(T†T)/24=0.02` does not imply the
required norm bound. One transmission eigenvalue0.48 and23 zeros has that mean
but `||T||op²=0.48`. Factoring at eta0.02 would make T' a noncontraction.

A stronger hand counterexample to a mean-based tail envelope uses four
orthogonal modes of intensity transmission `6 eta=0.12`, all other20 zero.
Their mean is eta0.02. A known CF12 source occupying these four and eight dark
modes has `Pr[N_out≥4]=(6 eta)^4=1296 eta^4`, exceeding the proposed
`binom(12,4)eta^4=495 eta^4`. Thus the binomial-tail inference itself cannot be
recovered from that mean. This refutes the mean substitution, not (1)–(6).

Every classical preparation description, norm certificate, dilation, random
draw, subset choice, occupation enumeration, permanent, repair, fallback,
decoder and actually scored/quench candidate must be charged in any later
comparison. All k physical source photons remain prepared/paid even when the
simulator retains only r. No equal-runtime, physical hardware capability,
quantum advantage or theorem-priority/novelty claim follows. The mathematical
reduction is complete in its stated oracle model; a finite-bit/resource
implementation and any application to real hardware remain separate obligations.
