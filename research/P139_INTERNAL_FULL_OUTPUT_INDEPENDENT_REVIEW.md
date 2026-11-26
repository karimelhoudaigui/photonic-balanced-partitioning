# P139 — independent full-output/internal-state addendum review

2026-11-26; complete76-line source `research/P139_INTERNAL_FULL_OUTPUT_ADDENDUM.md`,
commit `58c333d4ac8881467bdd6dfb5d7bfb01c4020522`, independently hashed SHA256
`dbe6611d678e5dc65465ae9dfd8e72ab4e50d8e340adb922ae6444b4c48242ec`.
The original119 review was frozen BEFORE reading this addendum:
`7976536253c701c84107ca14660835284d9883fc`,96 lines, SHA256
`6b83830fb18bc660588f414622a2a9ea834dac90cf1660dd99282dc54bde3515`.
Reviewer is not the author; no separate author verdict, program/import/AST, numerical evaluation,
graph draw, RNG, native call, P134 raw/receipt/implementation or source edit was used.

**Primary verdict: proved as written.**
The common factorial bound, positive D valuations and fixed-kernel utility transfer are correct under the explicit stronger endpoint/instrument hypotheses.

## 1. Physical observation and the K! bound

Require known CF input, vacuum auxiliaries, finitely many FULL spatial output modes and an internal-blind spatial isometry W_x.
Species labels are not extra output data in this statement.
For repeated output rows, the same divisor n!=prod_j n_j! appears in BOTH arms.
For every normalized physical internal state, the permutation kernel has diagonal1 and modulus<=1.
Physicality supplies nonnegative normalized probabilities; those entry bounds alone do not make an arbitrary matrix J a physical kernel.
Pure-state permutation vectors, or a purification for mixed states, justify the modulus bound.

Triangle and Cauchy give exactly

    0<=p_J(n;x)<=sum_(sigma,tau)|a_sigma||a_tau|/n!
                =(sum_sigma |a_sigma|)²/n!
                <=K! sum_sigma |a_sigma|²/n!=K!*p_D(n;x).

No extra n!, input factor or second K! is missing. CF source factorials are1.
The upper bound uses only physical kernel magnitudes, so no analyticity or continuity of J(x) is needed.
It covers B, proper species, mixtures and the stated partial-internal families sharing the SAME spatial device.
An internal-state-dependent optical transfer/detector is not automatically described by this common W_x law.

## 2. Monomial endpoint and uniform analytic window

At W_0, every occupied column has one unit-modulus entry in a DISTINCT row.
A nonzero assignment at zero must use exactly that multiset of rows, once each; hence n must equal n0.
Thus EVERY path a_sigma(0) vanishes for n!=n0, including collisional patterns with repeated rows.
At n0 the unique allowed assignment has unit modulus, proving deterministic output for all admitted internal states.
Suppression of selected B events without this path-level endpoint property would not suffice.

For a nonzero D germ, analytic paths give `p_D(n;x)=a_n*x^(2v_n)*f_n(x)` with a_n>0,v_n>=1,f_n(0)=1.
The constant n! only rescales a_n. No leading cancellation occurs in the positive sum of squared paths.
With c=ceil(sqrt(K!+1)), the D ratio at c*x tends to c^(2v_n)>=c²>K!.
The original review's continuity enclosure and finite minimum therefore apply to every full output n!=n0.
The minimum must include zero-germ neighborhoods and rho/c; the addendum does so.
There are only binom(M+K-1,K) count patterns, so ONE positive window works for all of them.
Combining that window with the uniform K! bound proves strictness for every nonzero D germ simultaneously for ALL physical J(kappa).
Zero D germs force every p_J to vanish there too. The window depends on W_x, M and K, not on the chosen internal family.

This FULL analytic-isometry premise is stronger than the original analytic signal-contraction premise.
For example T_x=(1-x)E is signal-analytic and contractive for positive x near zero,
but a dump block would need Gram (2x-x²)I. An analytic dump block vanishing at zero has squared norm starting at order>=2, not linear x.
Thus an analytic full dilation is not automatic. P133's explicit rational block resolves that analyticity issue for an analytic parameter curve;
its monomial endpoint must still be checked separately. P138's stated incumbent curve also supplies that endpoint at kappa=0.

## 3. Common repair, losses and limits

Let L be a normalized classical kernel IDENTICAL across arms AND across kappa and c*kappa.
For bounded g>=0, form h(n)=sum_z L(z|n)g(z) and require h(n0)=0.
Then the uncontrolled probability difference at n0 contributes zero, and summing all other pointwise inequalities gives the utility order.
It is strict when a reachable nonzero D germ has h(n)>0; impossible or zero-utility records supply no strictness.
This allows a declared collision/dump repair, retaining all raw mass, beyond the original CF/hold-only theorem.
A strength-aware repair applied differently at the two settings, or nonnormalizing success conditioning, is not this kernel.

Loss present already at zero can destroy the monomial FULL endpoint.
To transfer through terminal loss/noise, separately prove a common count kernel and the induced h(n0)=0.
A portwise count-thinning kernel may qualify; an arbitrary coherent/internal-dependent noisy device or repair with null-endpoint gain need not.
Neither measured mean loss nor a signal-only matrix certifies this bridge.
The comparator must admit c*kappa on the same spatial curve; both modeled attempts still inject K photons.
Setup, tag/source preparation, compilation, precision, detector response and wall costs are not equated.
No explicit computable uniform radius, growing-dimension result, adaptive-chain theorem, efficient sampler, novelty, hardware or optimizer-advantage claim follows.
The earlier original theorem and both frozen reviews remain distinct; no P134 law or outcome was evaluated.
