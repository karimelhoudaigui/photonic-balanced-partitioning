# P135 — prospective ideal phase-multinomial CF/hold control

2026-11-26; ROOT suggested this P129 corollary. Manual algebra only, before inspecting P134 scientific outcomes.
No P134 population/code change, new graph/parameter evaluation, import, script, RNG, native call or run.
The9441-row first screen is unchanged. Any implementation/evaluation here is a separate follow-up,
only after P134 passes its proper-group first screen and after a frozen contract/review/ROOT authority.
No novelty, optimizer advantage or source-preparation equivalence is claimed.

Let T in Q(i)^(r-by-k) be a contraction, k>=1, G=T†T, and M>k a power of two.
P129's IDEAL Q draws independent uniform Mth roots z_a, then k categorical trials
with receiver probabilities `|(Tz)_j|²/k` and residual loss probability.
For a CF receiver k-set Y, conditional probability is

    Q(Y|z) = k!/k^k * |product_(j in Y) sum_a T_ja z_a|².

Expand `product_(j in Y) sum_a T_ja z_a = sum_(|b|=k) c_b(Y) z^b`, with `b!=product_a b_a!`.
Independent finite twirling kills cross terms for distinct b,b', since each exponent difference has modulus <=k<M.
Consequently

    Q_CF(Y) = k!/k^k * sum_(|b|=k) |c_b(Y)|².          (1)

This contains no CF/survival denominator or output factorial because Y is distinct.
There are b! labelings of the repeated columns for each monomial assignment, so
`per(T[Y,columns repeated b])=b! c_b(Y)`.
Combining this with the Fock divisor b! and P129 mixture weight `k!/(k^k b!)`
independently gives (1); dropping either divisor would be wrong.

The same phase-twirled source mixture gives its ALL-SIGNAL mass

    Q_all = sum_(|b|=k) [k!/(k^k (b!)²)] per(G[b,b]),  (2)

where BOTH Gram indices repeat according to b. The normalized Fock all-signal
norm is `per(G[b,b])/b!`, establishing the second divisor in (2).
Then `Q_collision=Q_all-sum_Y Q_CF(Y)` and `Q_dump=1-Q_all`.
These are disjoint nonnegative physical-surrogate masses, including all collisions/losses.
A collision with a dump photon is in dump, not in all-signal collision.
Their sum is1; none is the B or D mass in general.

For k4, the coefficient table has only `binom(7,4)=35` entries per Y.
Multiply four linear forms by a degree-indexed coefficient DP, or enumerate the4^4 labeled choices;
no4096-context phase enumeration, target FPRAS, or optimization oracle is needed for (1).
Equation(2) needs only35 repeated-index size-four Gram permanents.
All setup, inversion, coefficient arithmetic, probability formation, sampling, decoder and scores remain paid.
For receiver pool r6 this provides all15 CF probabilities and the hold probability by subtraction,
not the complete resolved ten-mode Fock law.

Boundary hands: k1 reduces to the ordinary one-particle law; T=0 gives dump1.
For the k4 prototype injection, the sole nonzero CF polynomial is `z1 z2 z3 z4`:
`Q_CF(prototype)=4!/4^4=3/32`, while both original CF B and D give1.
Here G=I gives Q_all=1, hence Q_collision=29/32 and dump0.
Thus Q is NOT a universally dominating same-T proposal; the known deterministic prototype remains a credited classical control.
The ideal Q mean is still exactly the original CF mean. This separately derived eta=1 endpoint has exact TV29/32; P129's strict header is unchanged.
The k=0 vacuum case is separate; no k^k expression is required there.

A future utility comparison uses `I_Q=sum_Y h_Y Q_CF(Y)` with the same raw CF/hold decoder.
Q needs its own permitted parameter optimization and paid information/setup, not a same-setting handicap.
It is a shared-phase CLASSICAL correlation control, not a proper fixed-species partition of the original CF inputs.
Positive C4 or a proper-group grid win alone does not exclude this control or an exact-law classical mirror.
An ideal-Q evaluation is distinct from the rounded finite-bit sampler; if its TV discrepancy is <=epsilon,
any raw utility in [0,h_max] differs by at most h_max*epsilon, without rare conditioning.
The P131 API admits r6/k4 but its deployment on a new matrix still needs the separate binding/gate.
These identities are proved here as a P129 notation-level consequence; priority is not assessed.
