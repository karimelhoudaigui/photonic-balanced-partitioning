# P80: a finite-bit bridge using rational length intensities

26 November 2026. **Result: the finite-bit approximation route closes conditionally on the two premises below.** It returns a full raw count approximation with an explicit failure flag and total variation error at most the requested epsilon. Its bit cost is polynomial in dimension, rational input length, actual mean photon number and inverse error. This is a static theorem, not an implementation or runtime measurement. No other P80 derivation or verdict was read.

## 1. Contract and the two separate premises

Let $m\ge1$ and $Z\in\mathbb Q^{m\times m}$ be symmetric, entrywise nonnegative, with $\|Z\|_{\rm op}<1$. Let rational $0<\varepsilon<1$. Let $B$ bound numerator/denominator encoding lengths of the entries and epsilon; if $B$ denotes matrix input only, add the epsilon encoding length to the input-size parameter.

Use these two premises, without claiming to reprove them here:

* **A, optical law:** the complete raw PNR law $\mu_Z$ has PGF
  \[
  G_Z(z)=\left[\frac{\det(I-Z^2)}
                       {\det(I-(D_zZ)^2)}\right]^{1/2},
  \qquad D_z=\operatorname{diag}(z_i),\quad z_i\in[0,1].
  \]
  Equivalently, its positive even rooted-loop intensities are products of $Z$ entries divided by loop length, with all periodic/rooting multiplicities retained.
* **B, effective work:** for
  \[
  v=(I-Z)^{-1}{\bf1},\quad V=\max_i v_i,\quad
  \kappa=1-V^{-1},\quad
  S=\frac{m\kappa^2}{1-\kappa^2},\quad
  \bar n=\operatorname{Tr}[Z^2(I-Z^2)^{-1}],
  \]
  the estimate $S\le m^2\bar n$ holds.

Premise A is the optical bridge in the P78 candidate d42b4b3f37a28329a9d7f6d9b80cd03edea4c5bc, SHA-256 118c88279e01bb13b81450b7f30c2cb55ad852e3a34cfcffbdc56c1c64df7c4a. Premise B is separately supplied for this route; this note must not be cited as its independent proof. Without B, everything below still proves polynomial cost in $m,B,S,1/\varepsilon$.

If $Z=0$, return true vacuum without a flag. Otherwise the nonnegative Neumann series gives $v\ge{\bf1}$ and $V>1$, so $0<\kappa<1$. The exact rational substochastic matrix
  \[
  P_{ij}=\frac{Z_{ij}v_j}{\kappa v_i},\qquad
  P_{i\dagger}=1-\sum_jP_{ij}
  \]
is valid, since its row sum is $(1-v_i^{-1})/\kappa\le1$. The symbol $\dagger$ is absorbing; any absorbed proposal is rejected. Planned length still counts after absorption.

Exact rational elimination computes $v,\kappa,P,S,\bar n$ with polynomial encoding lengths and polynomial bit work in $m,B$: clear denominators and apply determinant/minor bounds or fraction-free elimination. The norm condition is an input promise; it can also be checked through exact positive definiteness of $I-Z$ in this symmetric nonnegative class. No Perron eigenvector, irrational probability oracle or logarithm oracle is needed.

## 2. Remove the transcendental random primitives

Put $p=\kappa^2$. In the ideal Poisson/logarithmic-length proposal process, independent Poisson marking gives a count $J_\ell$ for each planned length $2\ell$, with
  \[
  J_\ell\sim\operatorname{Pois}(a_\ell),\qquad
  a_\ell=\frac{m p^\ell}{2\ell}\in\mathbb Q,\qquad \ell\ge1.
  \]
Indeed the Poisson mean times its length probability cancels the two logarithms. Finite collections have product PGF $\prod_\ell\exp(a_\ell(t_\ell-1))$; the total intensity is finite because $p<1$.

For each such proposal, start uniformly in $[m]$ and run $2\ell$ transitions under $P$, with absorption. Retain it only on return to its starting mode, adding visits before the final return. For any specified closed walk, the intensity is
  \[
  \frac{a_\ell}{m}\prod_{j=0}^{2\ell-1}P_{i_j i_{j+1}}
  =\frac{1}{2\ell}\prod_{j=0}^{2\ell-1}Z_{i_j i_{j+1}},
  \]
because the $v$ ratios telescope. Thus A identifies its output with $\mu_Z$; no collision-free conditioning is used. Its total planned length $W$ satisfies
  \[
  \mathbb EW=\sum_{\ell\ge1}2\ell a_\ell
  =m\sum_{\ell\ge1}p^\ell=S.
  \]

## 3. A finite reference experiment, including flagged overflow

Choose even integer and length cutoff
  \[
  T=2\max\{1,\lceil4S/\varepsilon\rceil\},\qquad M=T/2,
  \qquad \beta=\frac{S}{2(M+1)}=\frac{S}{T+2}.
  \]
Then $S/T\le\varepsilon/8$ and $0\le\beta<\varepsilon/8$.

The probability that the ideal process has any length exceeding $2M$ is at most
  \[
  \sum_{\ell>M}a_\ell
  \le\frac{\sum_{\ell>M}2\ell a_\ell}{2(M+1)}
  \le\beta.
  \]
Use an independent rational Bernoulli$(\beta)$ flag $F$. On $F=1$, return FLAG. Otherwise draw only $J_1,\ldots,J_M$. If their total planned length exceeds $T$, return FLAG; otherwise generate their walks and return their count vector.

This is a controlled upper-abort construction, not an assertion that omitted loops are vacuum. To couple it with the ideal process, couple $F$ monotonically to the event that any omitted proposal exists. That event has probability $\theta\le\beta$ and is independent of the short process: set $F=1$ on it, and on its complement with probability $(\beta-\theta)/(1-\theta)$. This coupling is a proof device; the algorithm computes only rational $\beta$, never $\theta$.

On $F=0$, the ideal process has no omitted proposals. If the short planned sum also stays below $T$, all counts agree. Markov's inequality therefore gives
  \[
  d_{\rm TV}(R,\iota\mu_Z)
  \le\beta+\Pr[W_{\le M}>T]
  \le\beta+S/T\le\varepsilon/4.
  \]
Here $R$ is the reference law on $\mathbb N^m\sqcup\{\mathrm{FLAG}\}$ and $\iota\mu_Z$ assigns no mass to FLAG. This bound also bounds reference flag probability. Neither failed test triggers a retry.

For each retained length, it suffices to draw a capped count with states
$0,\ldots,K_\ell,*$, where $K_\ell=\lfloor T/(2\ell)\rfloor$ and $*$ means overflow. An overflow already implies the planned cap is exceeded; aggregated nonoverflow counts are also checked. This finite description exactly realizes $R$ before probability approximation.

## 4. Explicit rational Poisson approximation lemma

For rational $a\ge0$, integer $K\ge0$ and rational $0<\delta<1$, the capped Poisson law on $0,\ldots,K,*$ admits a dyadic probability vector within TV distance $\delta$, computable with polynomial bit cost in the rational input lengths, $K+1$, $a+1$ as numerical values, and $\log(1/\delta)$.

Choose integer
  \[
  n=\max\{2,\lceil6a\rceil,\lceil\log_2(4/\delta)\rceil\}.
  \]
Compute $w_j=a^j/j!$ rationally and set
  \[
  U=\sum_{j=0}^{n-1}w_j+2w_n,\qquad s=1/U.
  \]
The exponential tail after $w_n$ has successive ratios at most $a/(n+1)<1/6$, so $U\ge e^a$. Also $n!\ge(n/e)^n$ and $e<3$ give $w_n\le2^{-n}\le\delta/4$. Consequently
  \[
  0\le1-e^a/U\le2w_n\le\delta/2.
  \]
Define $q_j=sw_j$ for $0\le j\le K$ and $q_*=1-s\sum_{j=0}^K w_j$. These are nonnegative and sum to one, since the finite exponential sum is at most $e^a\le U$. Relative to the exact capped Poisson vector, all finite-state masses only decrease. Therefore its TV error is
  \[
  (e^{-a}-s)\sum_{j=0}^K w_j
  \le1-e^a/U\le\delta/2.
  \]

Choose the least nonnegative $b$ with $2^b\ge2(K+1)/\delta$. Replace each finite $q_j$ by $2^{-b}\lfloor2^bq_j\rfloor$ and put the residual on $*$. This adds TV at most $(K+1)2^{-b}\le\delta/2$. The vector is exactly normalized; drawing it uses exactly $b$ fair bits and an integer CDF. There is no uncomputed exponential or tail-normalization constant.

The index $n$ is selected by rational/integer comparisons to powers of two. Exact terms through $\max\{K,n\}$ have bit lengths polynomial in that index and the encoding of $a$; a common denominator divides a power of its denominator times a factorial. Summation, reciprocation, flooring and CDF construction are therefore polynomial bit operations. The displayed logarithm is an index bound, not a required real-arithmetic primitive.

## 5. A bounded finite-bit algorithm and its total error

Use the lemma for each length with
  \[
  \delta_{\rm Pois}=\frac{\varepsilon}{8M}.
  \]
Their joint mismatch probability is at most $M\delta_{\rm Pois}=\varepsilon/8$, including all overflow states and any early stopping.

For any rational categorical vector with $d$ states, round its first $d-1$ entries down to multiples of $2^{-b}$ and put the residual on the last state. It stays nonnegative, normalized, and has TV error at most $(d-1)2^{-b}$. This provides bounded-bit draws for the Bernoulli flag, uniform starts and transition rows. Use absorption as the residual state for a row, and the least nonnegative precision meeting each error bound.

Approximate the Bernoulli flag to TV error $\varepsilon/8$. Approximate every start and row draw to error
  \[
  \delta_{\rm mark}=\frac{\varepsilon}{8(T+M)}.
  \]
Once the planned cap passes, there are at most $M$ proposals and $T$ transitions. Sequential coupling, conditional on an agreeing past, bounds all mark errors by $(T+M)\delta_{\rm mark}=\varepsilon/8$. No assumption of independent output photons enters this coupling.

Let $\widehat R$ be the resulting finite-bit law. The complete bound is
  \[
  d_{\rm TV}(\widehat R,\iota\mu_Z)
  \le\underbrace{\varepsilon/4}_{\text{reference flags}}
     +\underbrace{\varepsilon/8}_{\text{Poisson tables}}
     +\underbrace{\varepsilon/8}_{\text{flag coin}}
     +\underbrace{\varepsilon/8}_{\text{walk marks}}
  =5\varepsilon/8\le\varepsilon.
  \]
In particular finite-bit flag probability is at most $5\varepsilon/8$. No failed prefix is discarded to obtain an apparently exact accepted law.

If an interface insists on a PNR vector, map FLAG to a designated vector, for example zero, while retaining an explicit flag bit. The vector marginal still has error at most epsilon by TV contraction; flagged zero is a substitute, not true optical vacuum. Conditioning on no flag is a different law and is not the theorem. The same fixed classical acceptance/decoding can be applied to both laws; conditioning on a rare event may amplify their error.

## 6. Bit complexity and scope

We have $T=O(1+S/\varepsilon)$ and $M=T/2$. Each exact intensity $a_\ell=mp^\ell/(2\ell)$ has polynomial encoding length in $T,m,B$, and numerical value at most $m/2$. The Poisson lemma therefore needs
$n=O(m+\log(M/\varepsilon))$ and $K_\ell\le T/2$.
Even constructing every table separately uses at most polynomially many operations on polynomial-size integers. The flag and all row/start tables have polynomial encoding and dyadic precision $O(\log(m(T+M)/\varepsilon))$.

There are $M$ capped Poisson draws, at most $M$ start draws, and at most $T$ row draws. Each uses a fixed finite number of fair bits; no rejection primitive has an unbounded retry count. Count accumulation, temporary visit vectors and absorption handling take polynomial work, and every returned count is at most $T$. The target's unbounded support is covered by the error/flag argument, not assumed absent.

Thus setup, memory, random-bit use and worst-case arithmetic bit work are polynomial in $m,B,S,1/\varepsilon$. Premise B converts this to polynomial in $m,B,\bar n,1/\varepsilon$. This is a mathematical resource bound; the degree and constants are not a practical-performance claim. Near criticality, $\bar n$ may itself be large.

The first formerly missing finite-bit implication is closed by rational length intensities, explicit overflow domination, and normalized Poisson/CDF approximations. Remaining dependencies are exactly A and the conversion B. This does not establish an efficient exact Turing sampler, polynomial dependence only on input length and $\log(1/\varepsilon)$, cheap rare-event conditioning, a matched QPU budget, or a positive optimizer result.

Only this note is written. No implementation, import, AST, scientific calculation, test, RNG, sampler, benchmark, native backend, QPU call, manuscript change or external query was executed.
