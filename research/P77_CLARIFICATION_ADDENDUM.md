# P77 clarification addendum

25 November 2026. **Primary verdict: both local qualifications in the original exact-hash review are resolved; its mathematical verdict remains valid.** No load-bearing probability formula, inequality, coefficient certificate, model assumption or resource conclusion changed.

## Exact versions and reading coverage

I read all 162 lines of research/P77_positive_hafnian_classical_countercontrol.md at commit f6470ae1361b8fe39ce7056ee5437d4189315d9d, SHA-256

    2a05e676adcb3778bc947f66a6b0880a4b998754d36af2067643cb675271d8b0

I also read the complete file diff from commit 851a0cce81cf2ea946d528491319df41b5f08a28 to this revision. The original 159-line source has SHA-256 d8bd1c123e05d92b8df0aa041c9ff8a3037e136e2dd0698de134c0e5b638f67d. The diff contains exactly the two requested clarification hunks.

The original review remains research/P77_AUTHOR_EXACT_HASH_REVIEW.md at commit d12c432d6993b7110c0de340e22d6354f6db6311, SHA-256 2b5156319c38b5d106370c2a281ff39dfde64a9db7a1cbfab5525a303a0d4b90. This addendum supplements that review rather than replacing its source identification or before-reading provenance.

## Resolution of the two qualifications

1. The rescaling is now explicit: $W'=W/a$ and $\lambda'=a\lambda$, so $\lambda'W'=\lambda W=Z$. It preserves the physical contraction condition and the dynamic range $b/a$. The factors in both raw masses also cancel: $f(W')=a^{-2k}f(W)$, while $\lambda'^{2k}=a^{2k}\lambda^{2k}$ and $b'^{2k}=a^{-2k}b^{2k}$. Thus no raw or conditional probability changes.
2. Equality of the conditional accepted laws is now expressly conditioned on $\sum_Tf(T)>0$. The source states that this is automatic for its main strictly positive model and that neither conditional law exists when the sum is zero. This correctly qualifies the optional zero-weight extension without changing its raw identity or extending the positive-range certificate to $a=0$.

The four independent matchings, $2k$ edge occurrences, determinant and squeezing powers, Rayleigh comparison, finite certificate, factorial envelope, fixed-range asymptotic, adaptive best-cost screen and paid-trial limitations are textually unchanged outside those two hunks. Their original audit continues to apply. In particular this remains a comparison of raw mathematical attempts, with no matched wall-time, energy, fixed injected-photon or hardware advantage claim.

## Preservation and scope

Only this new addendum is written. The following existing files retain their recorded bytes:

| Artifact | SHA-256 |
|---|---|
| Original exact-hash review, 111 lines | 2b5156319c38b5d106370c2a281ff39dfde64a9db7a1cbfab5525a303a0d4b90 |
| Before-reading independent P77 proof, 199 lines | ab4f1ab3119f1be0730f3f9354af534724de89bb72f96fddfcd80d1e8a2bf9bc |
| P75 overlap-route checkpoint | 9015bc5e484c4a01696c04ea84a78906f8373a46d52f6339396a32185715fdfd |

Validation is static full-text and diff reading, source-hash verification and Git whitespace checking. No scientific execution, import, AST, test, RNG, backend, QPU call or P75 experimental-output reading occurred. The proof-audit and mathematical-proofreading workflows were reused for this bounded review.

No new theorem, external attribution, novelty certification, positive optimizer result or permission for a further experiment follows from these clarifications.
