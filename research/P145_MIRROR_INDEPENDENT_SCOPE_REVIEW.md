# P145 — independent scope review of the finite-kernel mirror

26-Nov-2026. **Primary verdict: correct only after the source/conditional-history
restrictions below for the general mirror wording.** The B-only exact mirror and
the analytic fixture identities pass; no computational or practical advantage is inferred.

FULL 236-line source read at `6c5a63b2f0f70fe18774c7ebe7f0e4b75091ae99`:
`research/P145_TRIAD_LNS_ANALYSIS.md`, SHA256
`0092b6031449ad2fec82c509c2b4d43c6b1d795c9c3163a35dfabf79216a0b75`.
Non-author manual reconstruction; the ROOT verdict was not used as proof.
The separate126-line fixture review was frozen BEFORE this source was opened:
`6e1a761514760783d6a86e5dff32982610da56c0`, SHA256
`e7fc46a4725a3e401e6438f842f9c01f1a2af68e6589386228c4ab4edde062f5`.
That review and all producer files remain unchanged. No run payload was opened.

## 1. Residual, moment and fixture claims — passed

Expanding each crossing edge gives its outside-only constant plus
`w_ij*(1-2*x_j)*z_i`; internal edges give the degree-linear and quadratic terms.
Thus Eq.(1) is exact when C_out includes the all-zero-block boundary cost.
Block complementation changes only `sum_i h_i*(1-2*z_i)`. Constant h and
sum z=3 make this zero. A two-replacement target complements a one-swap target;
the three-replacement target complements the incumbent. A block one-swap minimum
is therefore best among all20 candidates in this CONSTANT-field case.
This does not follow from global complement symmetry when outside bits stay fixed.

In the same-setting permutation expansion, D keeps identity, each pair adds its
one transposition, and B adds all six permutations. Their inclusion/exclusion
leaves the two conjugate three-cycle terms, including every output factorial.
Normal ordering for occupation degree<=2 uses at most two source labels, so
the same subtraction annihilates every such polynomial. The stated invalid/hold
and acceptance-cutoff ledger follows from `g_+=g+(-g)_+` without conditioning.
This is not an identity between separately optimized utilities.

The twelve-vertex trap, Fourier law, I3=4w*p^3, restricted maxima and classical
gain9w agree with my preceding independent derivation. The adjacency-plus-diagonal
compiler leaves R and Q invariant because its block off-diagonal entries vanish;
no CF output can change the selected set. This proves zero gain for THAT compiler.
The dense Fourier mixer is a different family, not a correction to that argument.
Both its restricted contrast and its defeat by a monomial D route are valid.
The P139/P143 applications retain their admitted-retuning, null and common-utility
premises; they are local windows, not complete adaptive-search or clock orderings.

## 2. Exact21-category mirror — passed for B; missing source type identified

For THREE fully INDISTINGUISHABLE CF photons, a known physical6x3 signal
contraction T gives `p_Y=abs(per(T[Y,:]))^2` for each of the20 distinct Y.
The remaining mass `1-sum_Y p_Y` exactly combines every collision/loss/invalid
record when the controller observes only Y or the common hold atom.
Each permanent uses six products. No graph score is needed to form these
weights; evaluate only the sampled candidate, matching the optical scoring rule.

“Fresh prescribed3-CF-photon source” ALONE does not specify this law: CF is
spatial occupancy, not internal indistinguishability. A Gaussian-rational
counterexample uses the2x2 unitary with diagonal a=(1+i)/2 and off-diagonal
b=(1-i)/2, plus an untouched third source and three vacuum output rows.
For the three distinct occupied outputs, the B probability is
`abs(a^2+b^2)^2=0`, while D gives `abs(a)^4+abs(b)^4=1/2`.
The same T therefore does not determine the five source laws via that one formula.
Restrict §4's permanent formula explicitly to B, or supply the internal/species
law and its appropriate finite expansion. The latter is an additional extension,
not something silently proved by the B formula. This does not refute the B mirror.

For explicitly encoded Gaussian-rational T, all21 weights are rational and a
common denominator gives integer categorical weights. An unbiased-bit sampler
is exact without a guaranteed deterministic finite number of rejection draws.
The note correctly leaves a strict time cap separate. For transcendental exp(-itH),
certified compilation/probability error is still a named gap; no exact-real oracle
or finite-bit approximation theorem has been established by the21-weight formula.

## 3. Adaptive transcript and cost quantifiers

Copy the SAME observation-based classical policy, parameter/block choices and
policy randomness, then match its kernel conditional on EACH common history.
Induction gives equality of finite call-indexed transcripts, including scores,
accept/reject and histories, with no surviving quantum memory between calls.
This is stronger than agreement of aggregate histograms at selected settings.
It is not equality of wall-clock trajectories or policies driven by unequal timing.

For approximate kernels require `TV(P_l(.|h),Q_l(.|h))<=epsilon_l` for EVERY
admissible common history h (or a justified bound along the coupled common prefix).
Maximal coupling until the first mismatch then gives transcript TV at horizon L
at most `min(1,sum_(l<=L) epsilon_l)`. Average histogram error alone is insufficient.
If detailed invalid records influence the policy,21 categories no longer suffice;
match the full lossless56-bin law or the specified loss/detector observation law.
Independent loss coins are not a generally valid shortcut for correlated optical loss.

The mirror is a distinct CLASSICAL control, not the D arm or a proof of D's
retuned dominance. Source compilation, matrix arithmetic, fair bits, scores and
precision costs remain paid. A fixed-size arithmetic mirror does not establish
equal latency, a practical no-go or performance for growing coherent memory.
The P33 paragraph remains conditional on the previously reviewed density theorem
and its stated full-column/density/collision-pair premises; no new P33 proof is claimed.
No source edit, import/AST, programmatic math, RNG, raw-data read, test, native,
runner or QPU call occurred. Only this separate scope review was written.
