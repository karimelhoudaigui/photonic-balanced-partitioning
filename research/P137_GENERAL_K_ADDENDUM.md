# P137 — General-K weak-reflection addendum

2026-11-26. ROOT proposed this continuation; manual derivation reconstructed
independently. Parent c24a5b8ddd7c381d4f9060f3696a69c00ba4e290.
PROOF CANDIDATE pending ROOT/non-author review, no novelty claim. The original
130-line P137 source is unchanged. No import/AST, code, symbolic/numerical
execution, graph/matrix evaluation, RNG, raw preview, native/QPU or paper work.

## Hypotheses and candidate statement

Use the same P137 instrument and observation: K CF source photons, m>=K+1,
current receiver set R of size K, embedding E, H=H^dagger with ||H||op<=1,
and supplied |H_ja|>=d>0 for every j outside R and a in R. Thus d<=1.
Let K be ANY integer>=2 and choose the INTEGER c=ceil(sqrt(K)). Set

    c^2>=K, c>=2,
    kappa0(K,d)=d^(2K)/[2*K*K!*(c^(2K+1)+K!)].        (1)

For EVERY receiver-CF K-set Y!=R, s=|Y\R|, and 0<kappa<kappa0, claim

    p_D(Y;c*kappa)-p_B(Y;kappa)
      >= (3/2)*d^(2K)*kappa^(2s)>0.                  (2)

Missing outside sets when m-K<s need no special case. This extends the
photon-count scope, not the class of physical instruments or observations.

## Uniform proof, including the factorial gap

The P137 contraction identity, scaled-row bounds and elementary permanent
product telescoping do not require K<=4. For x<=1 they give, with
L=per(|H[Y\R,R\Y]|^2)>=s!*d^(2s),

    p_B(Y;kappa)/kappa^(2s)<=s!*L+3*K*(K!)^2*kappa,
    p_D(Y;c*kappa)/kappa^(2s)
                      >=c^(2s)*(L-3*K*K!*c*kappa).

The second line applies the same entrywise probability-permanent bound at
x=c*kappa, with outside row factors (c*kappa)^(2s). Therefore

    (p_D(Y;c*kappa)-p_B(Y;kappa))/kappa^(2s)
      >=(c^(2s)-s!)*L-3*K*K!*(c^(2s+1)+K!)*kappa.     (3)

To check the load-bearing gap, write q=c^2 and delta_s=q^s-s!.
For 1<=s<=K-1, q-1>=s and s!<=q^s, so

    delta_(s+1)-delta_s=(q-1)*q^s-s*s!
                       >=(q-1-s)*q^s>=0.

Thus every delta_s>=delta_1=q-1>=3. Since d<=1 and s<=K,
(c^(2s)-s!)*L>=3*d^(2K). The error term in (3) is bounded by
3*K*K!*(c^(2K+1)+K!)*kappa<3*d^(2K)/2 under (1), proving (2).
The required x<=1 premise is not circular:

    c*kappa0 < 1/[2*K*K!*c^(2K)] <1.

Here the first strict inequality follows by d<=1 and the positive K! term
in the denominator. For K=2,3,4, c=2 and (1) reproduces the original window
exactly, with denominators 272,4824,102912. No original constant was changed.

## Consequences and exclusions

For every common utility h(R)=0,h(Y)>=0 and all non-CF records held at R,
the raw D expectation at c*kappa dominates B at kappa, strictly when any
alternative utility is positive. This holds simultaneously for these h,
without C*, an optimal-state mask or prior knowledge of an improving set.
Both attempts inject K photons; modeled dump/collision events remain paid.
The comparator's admitted parameter family must contain c*kappa, not merely
the same setting or a grid which omits it. Adaptive policies and measured
setup/wall/precision/loss/tag-preparation costs are not matched by this bound.

K=1 with the prescribed c=1 is an equality exception: indistinguishable and
distinguishable one-photon laws coincide at every common setting. There is
no strict margin delta_1 and the proof does not extend (2) to that case.
Without the dense floor, H supported only on an outside diagonal again
gives T_x=E and zero alternative probabilities, refuting strict domination.
No sparse, all-strength, d-independent or global optimizer no-go is proved.

For Gaussian-rational H and rational kappa, integer c preserves rational
parameters and hence rational F/T/U. This does not implement compilation,
certify its cost, prove a finite-bit sampler or claim asymptotic speedup.
The factorial/small-d window may be extremely restrictive; no practical or
hardware interpretation follows without a separate resource/precision study.
Only this addendum was written; existing proofs, source and data are intact.
