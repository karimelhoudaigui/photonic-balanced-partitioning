# P77 exact latent-matching countercontrol for P73

25 November 2026. Static independent reconstruction from the coordinator's candidate, at worktree base 4248181e51b0bbeb0af632f879a125d549def907. No other P77 proof or review was read. Only this file is written; the 179-line P75 checkpoint is preserved. No scientific code, import, AST, numerical evaluation, test, random draw, experiment, source query or QPU call was executed.

**Primary verdict: proved as written under the positive P73 source model.** The classical filter below has exactly the same conditional feasible law as B, without computing a hafnian. Its raw candidate probabilities dominate B under an explicit coefficient test. A sufficient strength-independent test holds for every fixed dynamic range $\rho<e$ and all sufficiently large even $k$, with an explicit threshold. This is a raw-trial countercontrol, not an equal-wall-time theorem, a physical distinguishable source or a positive optimizer result.

## 1. Model and exact quantum coefficient

Let $N=2k$, with even $k\ge2$. Let $W=W^T$ be real with zero diagonal and strictly positive off-diagonal entries. Define

\[
0<a:=\min_{i\ne j}W_{ij}\le W_{ij}\le b:=\max_{i\ne j}W_{ij},
\qquad \rho=b/a\ge1.
\]

This includes $W=J_N-I_N+\epsilon A$ for a real symmetric nonnegative zero-diagonal graph adjacency $A$ and $\epsilon\ge0$: here $a\ge1$ and $\rho=b/a\le1+\epsilon\max_{i\ne j}A_{ij}$. Using the actual minimum improves the coarse bound based only on $W_{ij}\ge1$. The physical pair matrix is $Z=\lambda W$, where $\lambda>0$ and $\lambda\|W\|_{\rm op}<1$.

Prepare two independent pure zero-displacement Gaussian colors with this same $Z$. An accepted oriented balanced subset $S$ means exactly one red photon at each vertex of $S$, one blue photon at each vertex of $S^c$, and vacuum in the other color modes. Write

\[
D=\binom{2k}{k},\qquad m_k=(k-1)!!=\frac{k!}{2^{k/2}(k/2)!},\qquad
F(S)=\operatorname{haf}(W_S)^2\operatorname{haf}(W_{S^c})^2.
\]

$S$ and $S^c$ are distinct color-resolved outcomes, so the count is $D$, not $D/2$. Every perfect-matching weight is positive and therefore $F(S)>0$.

Put $\Delta=\det(I-\lambda^2W^2)$. All its factors are positive and at most one, so $0<\Delta\le1$. A single color contributes probability $\sqrt\Delta\,\lambda^k\operatorname{haf}(W_S)^2$; independence gives

\[
q_B(S)=c_BF(S),\qquad c_B=\Delta\lambda^{2k}.
\]

There is one determinant after multiplying the two colors. All Fock factorials are one. Vacua, wrong total photon numbers, collisions and wrong color patterns are paid failures. The Gaussian pulse has indefinite photon number: $N$ is the accepted target count, not a claim of $N$ injected photons on every pulse.

The conditional feasible law is $g_B(S)=F(S)/\sum_TF(T)$. It is defined since $\lambda>0$ and every $F(S)>0$; no physical preparation or acceptance probability is divided out when comparing raw trials below.

## 2. Constructive classical filter

One classical trial is:

1. Draw $S$ uniformly from the $D$ oriented balanced subsets.
2. Draw two independent uniform perfect matchings $M_1,M_2$ on $S$, and two $M_3,M_4$ on $S^c$.
3. Accept $S$ with probability

\[
r_{\rm lat}(M_1,\ldots,M_4)=
\prod_{\ell=1}^4\prod_{\{i,j\}\in M_\ell}\frac{W_{ij}}{b}.
\]

Otherwise output a failure symbol. There are exactly $4(k/2)=2k=N$ factors, counted with multiplicity when matchings repeat an edge. Each factor lies in $[a/b,1]=[1/\rho,1]$, so this is a valid acceptance probability. No rejection is declared free.

Uniform matchings require no weighted-matching solver: uniformly permute the $k$ vertices and pair consecutive entries. Every unordered perfect matching has the same $2^{k/2}(k/2)!$ preimages, proving uniformity.

For a fixed $S$, each of its matchings has expected weight $\operatorname{haf}(W_S)/m_k$. Independence of the four ordered matching choices proves the exact raw law

\[
\boxed{
q_C(S)=c_CF(S),\qquad
c_C=\frac{1}{D\,m_k^4\,b^{2k}}.
}
\]

In particular, conditioned on accepting,

\[
g_C(S)=\frac{F(S)}{\sum_TF(T)}=g_B(S)
\]

for every finite physical source strength. This is not a weak-response expansion. Two matchings per color are essential: they represent all ordered pairs of amplitude matchings in the square. One matching per color weighted by $W_{ij}^2$ would instead produce the different incoherent law.

The filter needs neither $\lambda$ nor $\Delta$, and uses no optimum value, target mask or known good partition. Its input is the same graph-dependent $W$ available to the Gaussian source.

This is a classical latent rejection construction. It is not asserted to be the distribution of physically distinguishable photons. Nonnegative real weights are essential to this acceptance rule; arbitrary complex or signed hafnian interference terms cannot be used as probabilities.

## 3. Exact raw comparison and probability caps

Define

\[
R=\frac{c_B}{c_C}
=D\,m_k^4\,b^{2k}\,\Delta\lambda^{2k}.
\]

Then $q_B(S)=R\,q_C(S)$ for every feasible $S$, and $P_{\rm acc,B}=R P_{\rm acc,C}$. Thus **$R\le1$ is the exact condition for this filtered C control to dominate B pointwise**. If $R>1$, B exceeds this particular filtered control by that factor; it does not follow that B beats other classical controls or has a resource advantage.

The classical construction itself ensures $0<P_{\rm acc,C}\le1$; in fact $P_{\rm acc,C}\ge\rho^{-2k}$. Rejection sampling an accepted output can require exponentially many trials. Its expected trial count is $1/P_{\rm acc,C}$, and all such trials are paid.

Let $u=N^{-1/2}(1,\ldots,1)^T$. Then

\[
\|W\|_{\rm op}\ge u^TWu
=\frac1N\sum_{i\ne j}W_{ij}\ge a(N-1)=a(2k-1).
\]

The physical source condition therefore gives $\lambda<1/[a(2k-1)]$. Using also $\Delta\le1$ and $\rho=b/a$,

\[
R<
\Gamma_k(\rho):=
D\,m_k^4\left(\frac{\rho}{2k-1}\right)^{2k}.
\]

Consequently $\Gamma_k(\rho)\le1$ is a sufficient test **uniform in every physical $\lambda$**. The inequalities are strict for the source model $\lambda>0$.

For any feasible target set $\mathcal A$,

\[
P_B(\mathcal A)=R P_C(\mathcal A)
\le R P_U(\mathcal A)
\le\Gamma_k(\rho)P_U(\mathcal A),
\]

where $U$ is the fresh uniform feasible proposal. The middle inequality holds because C first draws that same uniform candidate and then filters it. The last inequality is strict for a nonempty target set; the empty set has probability zero in all models. Thus $P_{\rm acc,B}\le\min(1,\Gamma_k(\rho))$; the probability cap remains necessary outside the sufficient regime.

## 4. Elementary factorial bound and explicit range

For an integer $n\ge1$, monotonicity of $\log x$ gives

\[
n\log n-n+1\le\log(n!)
\le n\log n-n+1+\log n.
\]

Use the upper inequality at $k$ and lower inequality at $k/2$ in the formula for $m_k$. The constant terms cancel:

\[
\log m_k\le\log k+\frac{k}{2}(\log k-1),\qquad
m_k\le k(k/e)^{k/2}.
\]

Also $D\le2^{2k}$. Therefore

\[
\begin{aligned}
\Gamma_k(\rho)
&\le k^4(\rho/e)^{2k}
       \left(\frac{2k}{2k-1}\right)^{2k}\\
&\le e^2 k^4(\rho/e)^{2k},
\end{aligned}
\]

using $\log(1+x)\le x$ and $2k/(2k-1)\le2$. No asymptotic factorial theorem is needed.

For fixed $1\le\rho<e$, put $\delta=\log(e/\rho)>0$. The sufficient envelope is $\exp(2+4\log k-2\delta k)$ and tends to zero exponentially. An explicit, conservative finite threshold is

\[
\boxed{\quad
k\text{ even},\qquad
k\ge\max\left\{2,\frac{4\log(4/\delta)-2}{\delta}\right\}.
\quad}
\]

Indeed $\log k\le(\delta/4)k-1-\log(\delta/4)$, obtained from $\log y\le y-1$. At that threshold $2+4\log k-2\delta k\le0$, so $\Gamma_k(\rho)\le1$. This proves the advertised strength-independent raw-trial domination for all sufficiently large even $k$, not just an infinitesimal $\epsilon$ window. It is uniform in physical $\lambda$ and permits finite $\epsilon$ whenever its actual dynamic range qualifies; it does not assert the condition for arbitrary $\epsilon$.

For finite small $k$, retain the exact test rather than assuming that $\rho<e$ alone suffices:

| Selected size $k$ | Vertices $N$ | Exact sufficient factor $\Gamma_k(\rho)$ |
|---|---:|---|
| 2 | 4 | $6(\rho/3)^4$ |
| 4 | 8 | $70\cdot3^4(\rho/7)^8$ |
| 6 | 12 | $924\cdot15^4(\rho/11)^{12}$ |

For example the first test is exactly $\rho^4\le27/2$. These are sufficient conditions, not optimized source bounds or necessary thresholds. The stronger general-Gaussian $k=2,4$ results in P75 are separate.

The dynamic-range criterion is invariant under scaling $W$ by a common positive constant and scaling $\lambda$ inversely; the physical $Z$ is unchanged. No conclusion is excluded merely because the sufficient bound $\rho<e$ fails; the exact $R$ or $\Gamma$ test may still work.

## 5. Costs and the stronger unfiltered control

The exact conditional sampler needs graph preprocessing and four uniform matchings, $N$ edge-factor lookups/multiplications and an acceptance coin per trial. This is $O(N)$ arithmetic operations per trial, plus preprocessing and any score computation. A dense input scan to find $a,b$ costs $O(N^2)$; storing/accessing the graph and evaluating its cut are paid as well. It is not a claim of polynomial total expected time for rejection-conditioned sampling.

The mathematical law uses exact uniform choices and an exact Bernoulli coin. For finite rational weights the product is rational and the coin can be implemented by an exact integer draw; its bit lengths and random-bit costs must be counted. No $O(N)$ bit-complexity or finite-precision exactness claim is made for arbitrary real encodings.

More simply, the uniform candidate $S$ already exists before the latent rejection. A stronger classical baseline scores **every** such candidate and can omit the matching filter altogether. Its proposal is uniform, not $g_B$; those two descriptions must not be conflated. When $\Gamma_k(\rho)\le1$, the inequality in section 3 proves that this unfiltered baseline dominates every feasible target event per raw trial. All quantum failures and all classical work remain counted.

If source parameters vary predictably between pulses while the same deterministic sufficient bound applies, the pointwise inequality holds conditionally at every history. For a process whose only new candidates are these outputs and a fixed objective threshold, multiplying conditional failure bounds gives the corresponding best-of-$T$ domination by fresh uniform feasible proposals, with a common initial incumbent. This uses raw trials and no acceptance postselection.

None of this equates a physical source pulse with a classical trial in wall time, energy, compilation, number/color resolution or hardware cost. Those quantities require an explicit end-to-end resource ledger. The source's indefinite photon number is not replaced by a fictitious fixed injected-$N$ accounting.

## 6. Scope, first unresolved implication and disposition

| Obligation | Result |
|---|---|
| Four matching draws and $2k$ acceptance factors | Passed; ordered pairs and repeats retained |
| Exact conditional $g_C=g_B$ without hafnian evaluation | Passed for real nonnegative weights |
| Quantum determinant and $\lambda^{2k}$ | Passed; one determinant after two independent colors |
| Exact raw coefficient comparison | Passed with $R\le1$ |
| Strength-independent sufficient test | Passed with $\Gamma_k(\rho)\le1$ |
| $e^2k^4(\rho/e)^{2k}$ envelope and explicit threshold | Passed by factorial integrals |
| Small $k$ and failed sufficient tests | Exact finite condition retained; no reversed advantage inferred |
| Uniform candidate retained on latent rejection | Stronger baseline, with a different conditional law |
| Physical D, complex amplitudes, matched wall/hardware costs | Not established by this construction |

Odd $k$ is outside the matching construction and P73's accepted source sector: the two zero-displacement colors cannot each emit an odd photon number, so B's acceptance is zero. At $\lambda=0$ it is also zero; its conditional accepted law is then undefined. The nontrivial construction above uses the stated even $k$ and $\lambda>0$.

There is no mathematical gap in this countercontrol within the stated positive model. The first uncertain implication would be converting raw-trial domination into a matched total-resource statement; that has not been supplied or claimed. For matrices outside the sufficient dynamic-range/size condition, exact conditional classical sampling is still available but its rejection cost and the raw coefficient comparison must be evaluated honestly. Failure of this sufficient test proves no photonic advantage.

The domination theorem requires $a>0$ and does not cover a directly sparse $W$ with zero off-diagonal entries by pretending its dynamic range is finite. The latent identity can still be meaningful for nonnegative weights when its normalization is nonzero, but no $a$-based large-size conclusion is asserted there. Generic complex or signed matrices are likewise outside the stated probability filter.

The result materially closes the finite-strength raw-pulse opportunity for a bounded-dynamic-range P73 class at the stated sizes. It does not settle the broad pure-Gaussian CF-overlap conjecture, generic encodings, arbitrary Gaussian sources, source feasibility or novelty. No paper, shared ledger or numerical artifact is changed. The positive optimization objective remains open.
