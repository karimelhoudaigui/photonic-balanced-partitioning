# P129 — finite-phase, fixed-source-count multinomial replacement

Date: 2026-11-26. Parent: `cbd7a39e52d12018d4ac0487fb61402a35fe50cd`.
ROOT supplied this candidate. This is a manual proof and bounded attribution check, not a discovery or execution record.
P128 and the P96/P98 proofs, prior notes, sources, contracts, and raw artifacts are unchanged.

## Claim, input model, and verdict

**Primary verdict: proved as written under the explicit finite-bit input model below.**
Let T be an m-by-K complex occupied-input transfer matrix of a passive vacuum-loss channel,
with known CF input of K distinct single photons and a certificate `||T||op² <= eta < 1`.
For K>=1 and m>=1, the ideal algorithm is:

1. Set M to the smallest power of two strictly exceeding K; draw independent uniform Mth roots z_1,...,z_K.
2. Form `p_j=|(Tz)_j|²/K` for signal rows j=1,...,m, and `p_0=1-sum_j p_j` for loss.
3. Draw K independent categorical outcomes with this common probability vector and aggregate signal counts.

Denote its unconditional signal law by Q_T. Then

\[
 \operatorname{TV}(P_T,Q_T)\le\tau(K,\eta)
 :=\mathbb E_{L\sim\operatorname{Bin}(K,\eta)}
 \left[1-\frac{(K)_L}{K^L}\right]
 \le\min\left\{1,\frac{(K-1)\eta^2}{2}\right\}.
 \tag{1}
\]

The algorithm does not use eta; eta is needed for this error certificate.
It retains all signal counts, including vacuum and collisions, with total count <=K always.
For exact Gaussian-rational T with full binary input length B and certified contraction,
an implementation with a fixed finite number of fair bits can have law Q_hat satisfying
`TV(P_T,Q_hat) <= tau(K,eta)+epsilon`, with bit cost polynomial in
`m,K,B,bitlength(epsilon),log(1/epsilon)` for rational `0<epsilon<1`.
Here Gaussian-rational means entries in Q(i), not a Gaussian optical source.
For arbitrary unencoded complex T only the ideal/oracle statement is asserted.

## 1. Exact finite twirl and sector error

Write `(K)_l=K!/(K-l)!`, `(K)_0=1`. For 0<=l<=K define

\[
 \rho_l=\binom Kl^{-1}\sum_{I\subseteq[K],\,|I|=l}|1_I\rangle\langle1_I|,
 \quad u_z=K^{-1/2}\sum_i z_i|i\rangle,
 \quad\sigma_l=\mathbb E_z\bigl[|u_z\rangle\langle u_z|^{\otimes l}\bigr].
 \tag{2}
\]

The tensor power is a symmetric l-particle condensate, equivalently a normalized l-photon Fock state in orbital u_z.
In the occupation basis its amplitude is `sqrt(l!/(prod_i n_i!)) prod_i(z_i/sqrt(K))^n_i`.
An off-diagonal matrix element carries `prod_i z_i^(n_i-n'_i)`.
Since `|n_i-n'_i|<=l<=K<M`, finite root averaging kills it unless every n_i=n'_i.
Thus the finite twirl equals the continuous phase twirl exactly, and

\[
 \langle n|\sigma_l|n\rangle=\frac{l!}{K^l\prod_i n_i!},\qquad |n|=l.
 \tag{3}
\]

On each CF occupation the ratio of this mass to rho_l's mass is `(K)_l/K^l<=1`.
The total sigma_l mass on CF occupations is `(K)_l/K^l`; rho_l has no other support.
The diagonal probability overlap therefore proves

\[
 D_{\rm tr}(\rho_l,\sigma_l)=1-\frac{(K)_l}{K^l}.
 \tag{4}
\]

This proof needs neither an assertion of optimality among all separable states nor an approximation of the twirl.
The l=0 states are both vacuum; the l=1 states coincide.

## 2. Spectral factorization, mixed error, and direct sampler

For eta>0 set `R=T/sqrt(eta)`. As in P128, R is a contraction and
`Phi_T=Phi_R o Loss_eta`, with a vacuum environment and no measured loss flags in the output contract.
Uniform loss produces `sum_l w_l rho_l`, with `w_l=binom(K,l)eta^l(1-eta)^(K-l)`.
Replace it by `sum_l w_l sigma_l`. Orthogonal photon-number sectors make its input distance exactly tau in (1).
Application of Phi_R and PNR measurement can only decrease this distance; output equality is not claimed.

The term in (4) is the probability that l independent uniform labels from [K] contain a collision.
The union bound over pairs gives `(4)<=binom(l,2)/K`.
Since `E[L(L-1)]=K(K-1)eta²`, its binomial average proves the last bound in (1).
For K=2 this average is exactly eta²/2; K=1 gives zero structural error for any physical one-column T.
For K=0 or eta=0 use exact vacuum directly; the latter certificate implies T=0.

Conditional on l,z, the signal/loss measurement of Phi_R on the condensate is multinomial:
each particle has signal probabilities `a_j=|(Rz)_j|²/K` and loss probability `1-sum_j a_j`.
The same z can be drawn before L, since its distribution is independent of L.
Mixing L~Bin(K,eta) is equivalent to K independent Bernoulli survivals followed by these categorical draws.
Their folded signal probabilities are `eta*a_j=|(Tz)_j|²/K`.
All loss outcomes combine into `1-sum_j p_j`, proving the direct algorithm.
In particular `sum_j p_j <= ||T||op² <= eta`, so the probability vector is positive and normalized.

The K categorical trials share z and are conditionally independent, not unconditionally independent.
This phase-correlated particle-separable law is generally not the original distinguishable-particle law D.
Particle separability is also different from a positive Glauber-P coherent-state representation.

## 3. Means, source count, and statistical scope

Finite root averaging gives `E[z_i conj(z_h)]=delta_ih` because M>=2.
Therefore the ideal surrogate has, for every signal row,

\[
 \mathbb E_{Q_T}n_j=K\mathbb E_z p_j=\sum_i|T_{ji}|^2=\mathbb E_{P_T}n_j.
 \tag{5}
\]

Total signal and loss means are also exact. Higher moments and full laws need not coincide.
Unlike P128's Poisson shell this law never exceeds K photons and needs no overflow map.
It supplies neither a physical preparation of the original CF input nor a hardware resource comparison.
In particular, a condensate's cheap classical simulation does not make its optical preparation free.
Every matrix/input/certificate, phase table, random bit, categorical draw, decoder, feature, and score is paid.
No loss record from an actual device is inferred or supplied by this mathematical factorization.

Identical classical decoding/repair/quench contracts (1).
Common classical-observation adaptive policies admit a sum of uniform per-history bounds, capped at one.
Coherent memory, physical timing histories, and conditioning on rare heralds are outside that consequence.
This is a full raw-law additive approximation, not a relative-probability guarantee or a matched-wall-clock advantage.

## 4. Finite-bit construction with fixed caps

Fix exact T in Q(i), its valid contraction certificate, and rational epsilon in (0,1).
All arithmetic in this section is exact rational/integer arithmetic; no floating clipping is needed.
Set `delta=epsilon/(4K)`. For each root zeta_r construct a Gaussian-rational w_r with
`|w_r-zeta_r|<=delta/2`, and set `zhat_r=w_r/(1+delta/2)`.
Then `|zhat_r|<=1` and `|zhat_r-zeta_r|<=delta`.
The approximants can be precomputed for all M<=2K root labels.

For completeness, such approximants have certified polynomial bit cost:
use the geometrically convergent rational arctangent series in
`pi=16 arctan(1/5)-4 arctan(1/239)`, then bounded-argument sine/cosine Taylor series at `2*pi*r/M`.
The identity follows from tangent addition and the quadrant; alternating/geometric tails certify pi's error.
Factorial Taylor tails on a bounded argument give coordinate error delta/4 with a polynomial number of terms and bits.
Angle error is at most twice the pi error; sine and cosine are 1-Lipschitz on the real line.
This establishes the required complex approximation, with bit length polynomial in `log K+log(1/delta)`.

Couple exact and approximate roots by the same uniform root labels; these labels require exactly `K log2 M` fair bits.
For each phase vector define `v=Tz/sqrt(K)` and `vhat=Tzhat/sqrt(K)` only for the norm argument.
Their norms are <=1 and `||v-vhat||<=delta`.
For the signal-plus-loss categorical vectors p,phat,

\[
 \operatorname{TV}(p,\widehat p)
 \le\sum_j\bigl||v_j|^2-|\widehat v_j|^2\bigr|
 \le(\|v\|+\|\widehat v\|)\|v-\widehat v\|\le2\delta.
 \tag{6}
\]

Here the loss difference is bounded by the sum of signal differences.
The rational implementation computes `phat_j=|(Tzhat)_j|²/K` without computing sqrt(K).
Its exact rational loss residual is nonnegative by contraction and `sum_i |zhat_i|²<=K`.
Coupling K categorical trials gives phase-rounding error <=`2K delta=epsilon/2`.

Choose the smallest power of two D>=`2Km/epsilon`, and let `ell=log2 D`.
Set integer signal weights `h_j=floor(D phat_j)` and `h_0=D-sum_j h_j` for loss.
They are nonnegative and sum to D; their categorical TV error is `sum_j(phat_j-h_j/D)<m/D`.
Each draw uses exactly ell fair bits to obtain an integer in [0,D-1] and a fixed integer-CDF lookup.
Its K-fold error is <`Km/D<=epsilon/2`, with no rejection, abort flag, or expected-time qualification.
Aggregation contracts the error, yielding the claimed `tau+epsilon` total bound.

The number of random bits is exactly `K(log2 M+ell)`; emitted counts are m integers in [0,K].
There are fixed polynomially many setup/phase-table operations, O(mK) rational matrix-vector operations,
and K categorical lookups. Exact intermediate rational bit lengths grow at most polynomially in full input length and these precision parameters.
Thus both arithmetic and random-bit time have deterministic polynomial upper bounds; no unbounded primitive is hidden.
This is not a universal FPRAS for bosonic probabilities: the structural error tau remains.

If only an approximation Ttilde is supplied, its relation to T needs a separate certificate.
If `||Ttilde||<=1` and `||T-Ttilde||op<=zeta`, (6) gives an extra `2K zeta` for the surrogate laws.
An arbitrary-real matrix, measured column efficiencies, or undocumented numerical eigenvectors are not finite binary inputs with that guarantee.
The spectral eta certificate must still concern the target T; a column mean cannot replace it.

## 5. Primary-source scope and relation to P128

Read local P96/P98 prior notes first; then re-extracted the exact official primary version on 2026-11-26.
Michał Oszmaniec and Daniel J. Brod, *Classical simulation of photonic linear optics with lost particles*,
[arXiv:1801.06166v1, 18 January 2018](https://arxiv.org/abs/1801.06166v1),
[primary text](https://arxiv.org/html/1801.06166v1); NJP 20,092002 (2018), DOI 10.1088/1367-2630/aadfa8.
Dictionary: their n=K, l=L, and eta is intensity transmission.
Theorem 1, (20)–(23), already gives the same fixed-L phase-twirled state, exact distance, and its optimality among particle-separable states.
Section III explains independent single-particle sampling through a linear-optical channel, including vacuum dilation.
Section IV.2, (25)–(28), already gives the binomial mixture and exact mixed input distance.
Lemma 1, (29), displays the coarser bound `K eta²/2+eta(1-eta)/2`.
We use input trace distance and output contraction; no printed equality of every output TV with the input distance is adopted.
Overlap: **known after translation of notation** for the separable construction and exact distances;
**formal corollary not stated** for the displayed birthday bound, folded direct sampler, finite twirl and explicit bit construction as extracted here.
Their global priority is unverified; this is not an exhaustive novelty search. No external PDF/source hash is asserted because none was retained.

P128 remains valid: it uses a different, Poisson-number coherent mixture and already attributes the broader framework.
P129 avoids its surplus counts; its ideal law matches the means exactly, and the finite-bit law has the stated additional TV error.
No global ordering of their actual output errors, matched runtime improvement, optimizer gain, or new physical hardware capability is claimed.
Only this note was written; no code/import/AST/scientific calculation script/test/RNG/native/runner/QPU/paper/push occurred.
