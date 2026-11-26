# P137 — independent exact-source review of the general-K addendum

Reviewed 2026-11-26; all83 lines of `research/P137_GENERAL_K_ADDENDUM.md`,
commit `da18f7366be56acc6528f521879430345ecb8336`, independently hashed SHA256
`966f42008f228dd4bf574ba2acb92a155d59c36a1c18b469cda02c742b60ab96`.
The original130-line source remains unchanged. Its separate independent review was frozen BEFORE this addendum was read:
`1e942caae5735921c1b7feb3a49e19dd9460f4bd`,112 lines, SHA256
`f1b4c46c4968a8536fa6288269a7eac020e2824949bf2b845f89637059d568d1`.
ROOT supplied the candidate; reviewer is not the source author and read no separate author verdict.
No import/AST/program, numerical matrix evaluation, graph draw, RNG, native call, P134 source/outcome/raw read or paper change occurred.

**Primary verdict: proved as written.**
The photon-count extension, constants and K=1 equality exception are valid under the source's dense-floor, current-prototype and admitted-control hypotheses.
No practical precision/runtime or general optimizer conclusion is thereby established.

## 1. Reused estimates remain valid for every finite K

Let K>=2, c=ceil(sqrt(K)), q=c². Then q>=K and c>=2.
The original contraction identity and dump bound do not use K<=4.
Nor do the normalized outside-row bounds: at x<=1 the entries of M_x,M_0 have modulus<=1,
their entry error is<=3x/2, and inside limit rows force their own columns.
For Y!=R put s=|Y\R| and L=per(|H[Y\R,R\Y]|²)>=s!*d^(2s).
The leading complex permanent bound is still s!*L, not K!*L.
Product telescoping through K entries and K! assignments is valid at every K.
Thus, exactly as in the original independent reconstruction,

    p_B(Y;kappa)/kappa^(2s) <= s!*L+3K(K!)²*kappa,
    p_D(Y;c*kappa)/kappa^(2s) >= c^(2s)*(L-3K*K!*c*kappa).

Subtracting gives `(c^(2s)-s!)*L - 3K*K!*(c^(2s+1)+K!)*kappa`.
The extra factor c in the D error is necessary and is present.
No factorial or source-subset factor is missing; there is no survival normalization or dimension-m summation.

## 2. The monotone factorial gap

Set delta_s=q^s-s!, for integer1<=s<=K. For1<=s<=K-1,

    delta_(s+1)-delta_s=(q-1)q^s-s*s!.

Because q>=K, each factor in s! is<=q, so s!<=q^s; also q-1>=s.
Consequently

    delta_(s+1)-delta_s >=(q-1-s)q^s >=0.

This proves delta_s>=delta_1=q-1>=3. Strict monotonicity is not needed.
With d<=1 and L>=s!*d^(2s), the leading term is>=3*d^(2K).
Since c>=2 and s<=K, its error coefficient is at most `3K*K!*(c^(2K+1)+K!)`.
For

    kappa0=d^(2K)/(2K*K!*(c^(2K+1)+K!)),

the source's strict kappa<kappa0 makes the error<(3/2)d^(2K).
This proves the stated raw probability gap, with its `(3/2)d^(2K)kappa^(2s)` margin.
As in the original, the calculation actually gives a strict inequality before that margin.

## 3. Noncircular range check and boundary cases

Independently of any entrywise remainder assumption,

    c*kappa0 = c*d^(2K)/(2K*K!*(c^(2K+1)+K!))
              <1/(2K*K!*c^(2K)) <1.

Here d<=1 and the positive additional K! term give the first strict inequality.
Hence both kappa and c*kappa lie in the x<=1 range used above; there is no bootstrap gap.
For K2,K3,K4, c=2, so c^(2K+1)=2*4^K exactly.
The original denominators272,4824,102912 and original window are unchanged.

For K=1 the prescribed c=1 compares the SAME setting.
One-photon indistinguishable and distinguishable spatial count laws are identical, including dump/hold;
delta_1=0 and no strict conclusion is valid, even with a positive coupling floor.
The addendum excludes this case from its strict theorem and correctly records equality.
K=0 is not part of its statement.
Without the dense floor, an H supported on one outside diagonal has HE=0 and T_x=E.
Every off-prototype target then has zero probability in both arms; this correctly defeats strictness, not the stated theorem.

## 4. Scope and remaining decisions

The off-R inequalities hold simultaneously, so every common h>=0 with h(R)=0 has the claimed raw expectation/positive-threshold order.
Strictness requires an alternative with positive utility; all collision and dump records remain paid holds.
If the incumbent is not R, the missing R contribution can change the conclusion.
The D family must admit c*kappa, with the same source/receiver/decoder contract; a finite grid need not contain it.
Rational H,kappa and integer c preserve rational F,T,U, but do not certify compiled hardware errors or supply a finite-bit implementation.
The small-d/factorial window is not uniform in K,d and is not a measured crossover or resource claim.
Different setup, synthesis, physical losses, internal tags, detectors, precision and clocks remain unmatched.
Adaptive chains, sparse matrices, all strengths, arbitrary initial states, global graph performance and quantum advantage remain outside this proof.
No P134 outcome was consulted or inferred; the original and this addendum are separate preserved sources.
