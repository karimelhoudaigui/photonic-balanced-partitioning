# P77 exact-hash author review

25 November 2026. **Primary verdict: proved as written under the stated positive source model.** The exact classical identity, finite coefficient certificate, fixed-range asymptotic and adaptive uniform screen are valid. Two local wording clarifications are recommended below; no load-bearing probability, coefficient or inequality repair is required.

## Exact artifact, complete coverage and independence

Author source: research/P77_positive_hafnian_classical_countercontrol.md, commit 851a0cce81cf2ea946d528491319df41b5f08a28, SHA-256

    d8bd1c123e05d92b8df0aa041c9ff8a3037e136e2dd0698de134c0e5b638f67d

**All 159 raw lines, 1–159, were read**, including every display, cost limitation and final disposition. The Git blob was read directly from the named commit and its hash matched the requested source.

Before author access I froze the independent research/P77_latent_matching_countercontrol.md, 199 lines, at commit f0abf6827acdb3479ccd3c1dc5d3d14f93c7097e, SHA-256 ab4f1ab3119f1be0730f3f9354af534724de89bb72f96fddfcd80d1e8a2bf9bc. Its hash remains unchanged. Both derivations received the coordinator's candidate and route; this is before-reading independence, not an unrelated-method or formal-verification claim.

Only this review is written. The proof-audit and mathematical-proofreading workflows were applied. No scientific code, import, AST, numerical evaluation, test, RNG, experiment, backend or QPU call was used. No P75 experimental output was opened or used as evidence.

## Obligation map

| Author lines | Obligation | Result |
|---|---|---|
| 18–32 | Positive weights, two-color source and determinant normalization | Passed; scaling wording clarified below |
| 36–50 | Four independent uniform matchings and $2k$ edge coins | Passed |
| 52–63 | Exact conditional law and paid rejection cost | Passed; zero-weight extension needs nonzero normalization |
| 67–85 | Rayleigh bound, physical $\lambda$ and finite certificate | Passed |
| 92–112 | Factorial envelope, fixed $\rho<e$ and finite-size scope | Passed |
| 116–122 | Predictable source choices and best-cost CDF screen | Passed |
| 124–138 | Coins, bit costs, preprocessing and wall-time exclusions | Passed |
| 142–159 | Positive-class boundary and scientific disposition | Passed |

## Exact masses and matching multiplicities

The source has $N=2k$ vertices, even $k\ge2$, $D=\binom{2k}{k}$ oriented balanced subsets and $m=(k-1)!!$ matchings on each side. The amplitude matrix is real symmetric with zero diagonal and $0<a\le W_{ij}\le b$, with dynamic range $\rho=b/a$. The two independent colors have the same physical pair matrix $Z=\lambda W$, $\lambda>0$, $\lambda\|W\|<1$.

For a specified accepted color-count pattern, each color has $k$ distinct single photons. Its raw probability is $\sqrt{\Delta}\lambda^k\operatorname{haf}(W_S)^2$, where $\Delta=\det(I-\lambda^2W^2)$. The product of the two colors is exactly $c_Bf(S)$ with $c_B=\Delta\lambda^{2k}$, not a square-root or squared determinant. All Fock factorials are one; no acceptance denominator appears.

The source's least-remaining-vertex matching rule is uniform: the probability of any fixed desired matching is $(k-1)^{-1}(k-3)^{-1}\cdots1^{-1}=1/m$. Four independent draws therefore have ordered-tuple probability $m^{-4}$. Ordered pairs are necessary to reproduce the cross terms in a square; there is no extra factor two.

Each matching has $k/2$ edges, so all four have exactly $2k=N$ edge occurrences. Repeated occurrences require distinct independent coins, as the source specifies. Early stopping at a failed coin does not change the all-pass probability. Summing the products gives

\[
q_C(S)=\frac{\operatorname{haf}(W_S)^2
                   \operatorname{haf}(W_{S^c})^2}
                  {D m^4 b^{2k}}.
\]

Thus the accepted conditional law is exactly $f(S)/\sum_Tf(T)$, equal to B's law for every physical $\lambda$. This is an ordinary classical latent filter. It neither computes a hafnian nor purports to realize a physical distinguishable-photon Gaussian law. Generic signed/complex amplitudes cannot be substituted into these Bernoulli probabilities.

As a normalization check, if every off-diagonal weight equals $b=a$, all coins pass and $f(S)=m^4b^{2k}$. The formula reduces to $q_C(S)=1/D$, as direct uniform generation requires.

## Physical coefficient, finite certificate and asymptotic rate

The uniform unit vector has Rayleigh quotient at least $a(N-1)$ even though $W$ need not be positive semidefinite. Hence $\lambda<1/[a(N-1)]$. Every determinant factor $1-\lambda^2\omega_i^2$ is in $(0,1]$, so the source's upper bound for $c_B$ is valid.

The exact coefficient ratio from the independent proof is

\[
R=Dm^4b^{2k}\Delta\lambda^{2k}
<\Gamma_k(\rho)
=Dm^4\left(\frac{\rho}{2k-1}\right)^{2k}.
\]

The author's $B(k,\rho)$ is this same $\Gamma_k(\rho)$. Its condition $B(k,\rho)\le1$ therefore implies $q_C(S)\ge q_B(S)$ for every feasible $S$. No favorable seed, optimum value, training mask or known solution is needed by the sampler.

The direct uniform screen is independently correct: $\operatorname{haf}(W_T)\le m b^{k/2}$, so $q_B(S)\le\Gamma_k(\rho)/D$. Equivalently C is a filter on a uniform candidate, and its raw candidate mass cannot exceed $1/D$. Retaining and scoring all those candidates is a stronger uniform control, but its conditional law is not $g_B$.

The factorial prefactor was checked with both integral bounds:

\[
n\log n-n+1\le\log(n!)
\le n\log n-n+1+\log n.
\]

Using the upper bound at $k$ and lower bound at $k/2$ cancels the additive constants and gives $m\le k(k/e)^{k/2}$. Together with $D\le4^k$ and $(2k/(2k-1))^{2k}\le e^2$, this proves exactly

\[
\Gamma_k(\rho)\le e^2k^4(\rho/e)^{2k}.
\]

For every fixed ratio cap $\rho<e$, this is exponentially small and eventually below one. The source correctly retains the exact finite certificate at small $k$, does not assert the endpoint $\rho=e$, and does not assert all-$\epsilon$ domination. The P73 bound $\rho\le1+\epsilon A_{\max}$ is sufficient; actual minimum-weight normalization can improve it.

The explicit threshold in the earlier independent note is an additional sufficient check, not a missing step in the author's asymptotic claim. With $\delta=\log(e/\rho)>0$,

\[
k\text{ even},\qquad
k\ge\max\left\{2,\frac{4\log(4/\delta)-2}{\delta}\right\}
\]

ensures $\Gamma_k(\rho)\le1$. Indeed the tangent inequality $\log x\le x/4+\log4-1$, applied to $x=\delta k$, bounds $2+4\log k-2\delta k$ by $4\log(4/\delta)-2-\delta k\le0$. This supplement leaves the frozen 159-line proof unchanged.

## Adaptive and resource scope

For a fixed objective threshold below a common initial incumbent, let $\mathcal A$ be its feasible sublevel set. At every still-unsuccessful history satisfying the finite certificate, the next raw optical hit probability is at most $|\mathcal A|/D$. Conditional survival induction therefore bounds the success probability after $T$ raw attempts by $1-(1-|\mathcal A|/D)^T$, exactly the fresh iid uniform control's success probability. No independence of B outcomes or knowledge of that cardinality by the controller is needed.

The result presumes only those credited source candidates are new, unless extra classical candidates are shared/accounted as the source explicitly requires. Training attempts and failed source cycles cannot be omitted. This is not a comparison after conditioning on accepted shots or after a favorable seed search.

One latent trial requires four direct matchings and at most $2k$ edge-coin tests; every drawn matching, rejected prefix and credited score is paid. It may take exponentially many trials to obtain an accepted conditional sample. The source explicitly distinguishes per-trial arithmetic work from total expected rejection cost and rational-weight bit costs. It assumes no constant-time arbitrary-real exact coin.

The Gaussian source has indefinite photon number; $N$ is the accepted target count, not a fixed number injected on every failed pulse. Preparation, readout, graph input, compilation, scoring, data movement and parallelism need their own ledger before any wall-time, energy or hardware comparison. Lines 133–138 expressly decline that conversion, and this review does not supply it.

## Read-only mathematical proofreading and closure

Two precise local clarifications are warranted:

1. **Line 32:** write the intended minimum-one normalization explicitly as $W'=W/a$, $\lambda'=a\lambda$, giving $\lambda'W'=\lambda W$. The phrase about rescaling both “by $a$” is ambiguous without the inverse directions. The rest of the proof already keeps $a$ explicitly and does not depend on an erroneous simultaneous multiplication.
2. **Lines 56–59:** the raw identity extends to nonnegative weights with zeros and $b>0$, but its conditional-law statement requires $\sum_Tf(T)>0$. This is automatic in the main strictly positive model. If that sum vanishes, both acceptance probabilities are zero and no conditional accepted law exists.

These are local wording qualifications, not repairs to the main positive-model theorem. No author or independent-proof edit is applied. Mathematical-token changes: none. Coverage: all 159 author lines and this review. Validation: static reading, exact hash checks and Git whitespace checking only; no build or test was run.

There is no load-bearing mathematical gap under the stated source and raw-trial hypotheses. The ordinary positive-weight expansion and elementary factorial bounds establish the result internally; no external theorem or publication-priority claim is needed. No novelty search or novelty certification is performed here.

The positive dense-pair class is screened when its finite certificate passes. Sparse zero-minimum pair matrices have no finite ratio of the required kind; a sparse graph $A$ with the positive $J-I$ background is still included. The generic complex/signed, large-range, changed-source and matched-total-cost questions remain outside this conclusion. The general P75 Gaussian overlap conjecture is not used. The frozen author source and independent 199-line note are preserved, and the positive optimizer objective remains open.
