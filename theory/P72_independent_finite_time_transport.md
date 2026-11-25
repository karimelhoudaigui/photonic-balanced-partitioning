# P72 independent derivation: finite norm-time and transport

25 November 2026. Static derivation from the coordinator's candidate, at worktree base c5d5422c9c8266f16ec101caaf1c7ed6617bd36c. No other P72 author file, proof or review verdict was read. The proof-audit workflow and mathematical self-proofreading were applied. No scientific code, import, numerical calculation, test, graph generation, external source query, experiment or QPU operation was executed.

**Primary verdict: conditional on the pinned P71 finite unitary-comparison lemma.** All Taylor, Krylov-range, singular-value, factorial/asymptotic and first-exit steps below are independently derived. The fixed-coupling-rank conclusion follows. The weaker growing-rank conclusion is retained explicitly; a bound exponential in $L$ does not follow in that case from the proposed norm-time assumption alone. This is a transport obstruction with prescribed sources and targets, not a positive optimizer or novelty claim.

## 1. Named dependency and normalized claim

The only imported transport lemma is the finite event bound from research/P71_approximate_cross_rank_transport.md:

- Commit b2f84ccb7383331605e128351c927e66ae0d84cf.
- SHA-256 c320f925b53f68738931da93ef28bb0a2f84f887988404153f974dae8b6cfe03.
- Its exact-rank constant comes from research/P69_low_rank_transport_obstruction.md, commit 48321304296b9492d41294a5a8c96562550f8ffc, SHA-256 37e59633734c16277ed2649c4761fa84a86a8006b164fd4263963e37d7759de4.

The P71 source was read in full as a lemma dependency and its source hash verified. Its separate exact peer review was pending when this task was assigned; this file does not close or relabel that review. No P71 independent-review verdict was needed as proof evidence.

Let $L\ge2$, $d=2L$, $K=2L$, and fix the same input/output mode blocks $C_A,C_B$, each of size $d$. The ideal normalized bosonic source has perfectly indistinguishable photons, one at each of $L$ distinct vertices in each block. The two good raw count events are full collision-free occupation of all $C_A$ or all $C_B$. Probabilities refer to the complete optical count law for this specified ideal input; collisions keep their mass and cost. No physical source-generation probability or free heralded preparation is inferred.

For a unitary $U$, let $s_j$ be its decreasing cross-block singular values, with $s_{d+1}=0$. P71 supplies

\[
P_U(\mathrm{good})\le
\min\{1,p_{L,r}+\sqrt2\,K s_{r+1}\},\qquad 0\le r\le d.
\]

Here $p_{L,0}=0$; for $r\ge1$,

\[
a_{L,r}=\min\left(1,\frac{r(r+1)\cdots(r+L-1)}{L^L}\right),\quad
b_{L,r}=
\begin{cases}
\min\left(1,\left(\frac{L+r}{2r}\right)^r
                 \left(\frac{L+r}{2L}\right)^L\right),&r<L,\\
1,&r\ge L,
\end{cases}
\qquad
p_{L,r}=\min(1,2a_{L,r}b_{L,r}).
\]

The P71 norm constant comes from replacing discarded unitary cosine/sine pairs by identity pairs: the one-particle distance is at most $\sqrt2\,s_{r+1}$. Tensor telescoping multiplies this by $K$ on the normalized symmetric photon space; complete PNR total variation is no larger. There is no extra factorial or factor two. P71 constructs a **unitary comparison matrix**; it does not physically implement that comparison for free.

Now let

\[
H=\begin{pmatrix}X&Z\\ Z^\dagger&Y\end{pmatrix}
=H^\dagger,\quad \operatorname{rank}Z\le h,\quad
U=e^{itH},\quad t\in\mathbb R,\quad
\tau=|t|\,\|H\|_{\rm op}.
\]

The integer $h\ge0$ bounds Hamiltonian coupling rank, not optical cross rank. $X,Y$ are arbitrary Hermitian blocks. Hermiticity gives $U^\dagger U=e^{-itH}e^{itH}=I$. Each shot uses one time-independent $H$; it may have been selected from arbitrary marked classical history before that shot.

For an integer degree $p\ge0$, define

\[
Q_p=\sum_{k=0}^p\frac{(itH)^k}{k!},\quad m=p+1,\quad
E_p(\tau)=e^\tau\frac{\tau^{p+1}}{(p+1)!},\quad E_p(0)=0.
\]

The finite conclusion, whenever $r=ph<d$, is

\[
\boxed{\quad
P_{e^{itH}}(\mathrm{good})
\le \min\{1,p_{L,ph}+\sqrt2\,K E_p(\tau)\}.
\quad}
\]

For $ph\ge d$, take $r=d$ and retain only the trivial probability bound one. The degree $p$ is a mathematical certificate parameter; it is not an executed optical circuit depth.

## 2. Cross-range induction

Write $B_k=(H^k)_{AB}$ and $D_k=(H^k)_{BB}$. Block multiplication gives exactly

\[
B_0=0,\qquad B_{k+1}=XB_k+ZD_k.
\]

For $k\ge1$ put $\mathcal K_k=\operatorname{span}\{X^a\operatorname{range}Z:0\le a<k\}$. Since $B_1=Z$, its range lies in $\mathcal K_1$. If $\operatorname{range}B_k\subseteq\mathcal K_k$, then $XB_k$ has range in the span with exponents $1,\ldots,k$, while $ZD_k$ has range in $\operatorname{range}Z$. This proves $\operatorname{range}B_{k+1}\subseteq\mathcal K_{k+1}$.

These spaces are nested. Therefore, with $\mathcal K_0=\{0\}$,

\[
\operatorname{range}(Q_p)_{AB}\subseteq\mathcal K_p,\qquad
\operatorname{rank}(Q_p)_{AB}
\le\dim\mathcal K_p\le p\,\operatorname{rank}Z\le ph.
\]

No commutation of $X,Y,Z$ is assumed. The fixed $X$ within the shot is what makes this one Krylov span applicable to every monomial.

## 3. Taylor remainder and singular tail

The matrix series is absolutely convergent in operator norm. Submultiplicativity and $(m+j)!\ge m!\,j!$ give

\[
\|U-Q_p\|
\le\sum_{k=m}^\infty\frac{\tau^k}{k!}
\le\frac{\tau^m}{m!}\sum_{j=0}^\infty\frac{\tau^j}{j!}
=E_p(\tau).
\]

Compress to the cross block: for $C=U_{AB}$ and $B=(Q_p)_{AB}$, $\|C-B\|\le E_p(\tau)$ and $\operatorname{rank}B\le r=ph$.

Here is the required singular-value argument without assuming that $Q_p$ is unitary. For $r<d$, take the span $W$ of $r+1$ leading right singular vectors of $C$. Its dimension is $r+1$, while $\dim\ker B\ge d-r$. Their intersection contains a unit vector $v$. On $W$, $\|Cv\|\ge s_{r+1}$; since $Bv=0$,

\[
s_{r+1}\le\|Cv\|=\|(C-B)v\|\le E_p(\tau).
\]

The kernel used here is the kernel of the **cross block** $(Q_p)_{AB}$, not the kernel of the entire polynomial matrix. The argument includes zero singular values and an approximant of rank smaller than $r$.

Substitution into the named P71 lemma proves the displayed finite conclusion. The polynomial $Q_p$ is only a rank-approximation witness. In general it is not unitary, and it is never inserted into P69 as a physical proposal. In particular no full Fock probability law, photon normalization or tensor telescoping estimate is assigned to a nonunitary $Q_p$.

If $h=0$, then $Z=0$ and $H,U$ are block-local: the good probability is exactly zero. If $t=0$ or $\tau=0$, $U=I$ and it is again zero. These exact cases override any looser certificate. For $p=0$, the finite argument still works with $(Q_0)_{AB}=0$, $r=0$, and $E_0=e^\tau\tau$.

## 4. Factorial estimate and fixed coupling rank

For every integer $m\ge1$, monotonicity of the logarithm gives

\[
\log(m!)\ge\int_1^m\log x\,dx
=m\log m-m+1\ge m\log m-m.
\]

For $\tau>0$ and $\rho=\tau/m$ this yields

\[
\log E_p(\tau)\le\tau+m\log(\tau/m)+m
=m[\rho+1+\log\rho].
\]

Zero $\tau$ was handled separately, so no logarithm of zero is taken.

Fix an integer $h\ge1$ and a constant $0<\alpha<1$. Choose $p=\lfloor\alpha L/h\rfloor$. Then $r=ph\le\alpha L<L$, and $m/L\longrightarrow\alpha/h>0$. If $\tau_L=o(L)$, then $\rho_L\to0$; hence $\rho_L+1+\log\rho_L\to-\infty$ and

\[
\log E_p(\tau_L)=-\omega(L)
\]

in the upper-bound sense: $E_p(\tau_L)$ is smaller than $e^{-cL}$ eventually for every fixed $c>0$. Zero-error subsequences satisfy this statement automatically.

The exact-rank term is also exponentially small. For $x=r/L\in(0,1)$ its uncapped target factor is $e^{-LI(x)}$, where

\[
I(x)=(1+x)\log2-(1+x)\log(1+x)+x\log x.
\]

Indeed this follows by taking logarithms of $b_{L,r}$. Also $I(1)=0$ and $I'(x)=\log(2x/(1+x))<0$ on $(0,1)$, so $I(x)>0$. Since $x\le\alpha$ and $a_{L,r}\le1$,

\[
p_{L,r}\le2e^{-LI(\alpha)}.
\]

For $r=0$ the same inequality holds because $p_{L,0}=0$. The factor $K=2L$ cannot destroy the super-exponential error certificate. Thus the complete finite hazard bound is $e^{-\Omega(L)}$ for fixed $h$ under $\tau_L=o(L)$. Neither the exact-rank term nor the additive certificate is an achieved probability.

## 5. Explicit small norm-time window

Let $p\ge1$ and choose any fixed $c>0$ satisfying

\[
c+\log(ec)=c+1+\log c<0,\qquad
\gamma=-(c+1+\log c)>0.
\]

If $\tau\le cp$, then $\rho=\tau/(p+1)\le c$. The function $x+1+\log x$ is increasing for $x>0$, so

\[
\log E_p(\tau)\le-\gamma(p+1)\le-\gamma p,\qquad
E_p(\tau)\le e^{-\gamma p}.
\]

Zero $\tau$ is again exact. For fixed $h$ and $p=\lfloor\alpha L/h\rfloor$, this supplies an exponential-in-$L$ certificate even in the stated small linear norm-time window. For growing $h$, its exponent is proportional to $p$, not automatically to $L$.

## 6. Growing coupling rank: the necessary limitation

Let $h=h_L\ge1$ grow and retain $p=\lfloor\alpha L/h_L\rfloor$. Set $n_L=L/h_L$. Since $m=p+1>\alpha n_L$, the assumption $\tau_L=o(n_L)$ implies $\rho_L=\tau_L/m\to0$. Dividing the same factorial bound by $n_L$ proves only

\[
\log E_p(\tau_L)=-\omega(L/h_L)
\]

in general. When $L/h_L\to\infty$, $p$ is of that scale; if it stays bounded, this notation asserts error decay without an extensive exponent. This hypothesis alone does not imply $-\Omega(L)$ for unbounded $h_L$. The exact-rank term still has the $e^{-\Omega(L)}$ bound because $ph_L\le\alpha L$, but the additive $2L E_p$ term can dominate or even make the probability certificate vacuous.

A symbolic certificate example makes the distinction explicit. Take $h_L=\lfloor\sqrt L\rfloor$ and $\tau_L=1$. Then $\tau_L=o(L/h_L)$ and $m=\Theta(\sqrt L)$, while $E_p=e/m!$. The inequalities

\[
m\log m-m+1\le\log(m!)\le m\log m
\]

give $\log E_p=-\Theta(\sqrt L\log L)$, which is not $-\Omega(L)$. This is an analytic limitation of this certificate, not a physical transport counterexample or numerical experiment. It does not assert that the actual good probability has that decay.

For any horizon $T_L$, a separate sufficient additive-error requirement is $K T_L E_p(\tau_L)\to0$, or an exponential version of it if exponential trapping is claimed. A statement merely that $E_p$ is small is insufficient.

## 7. Marked histories, first exits and finite temperature

Use the original or connected P66 four-clique cost family and its prescribed bad whole-clique warm start. To avoid a notation collision, call the matching edge weight $\mu>0$; $h$ above remains the Hamiltonian coupling-rank bound. Heavy weight $M$ and cross weight $w=0$ or $0<w<\mu/L$ satisfy $M(L-1)>L\mu$. The only better feasible states are the two full-block targets; every feasible state outside those and the four bad states costs at least $C_{\rm bad}+g$, where $g=2M(L-1)-2L\mu>0$.

Only feasible CF outputs are scored. Use the P66 acceptance probability $\min(1,e^{-\beta_j(C(T)-C(S))})$, with its non-uphill zero-temperature limit. No detailed-balance or stationarity conclusion is needed; an additional Hastings factor would require checking the stated uphill acceptance bound separately.

Before each shot, condition on the whole marked history and chosen internal controls. A fresh CF state is prepared at the current subset, and a single static Hermitian $H_j$ is selected before evolution. Suppose its cross coupling rank is at most $h$ and its norm-time is $\tau_j$. While no accepted exit from the bad class has occurred, the finite bound gives conditional raw improvement hazard at most

\[
q_j=\min\{1,p_{L,ph}+\sqrt2\,K E_p(\tau_j)\}.
\]

At zero temperature all non-target CF exits are uphill and rejected. Collisions are paid self-loops, neutral bad states may be accepted, and only these optical proposals update the source. With deterministic bounds $0\le\bar q_j\le1$ valid for every still-bad history,

\[
P(\text{improvement by }T)
\le1-\prod_{j=1}^T(1-\bar q_j)
\le\min(1,\sum_{j=1}^T\bar q_j).
\]

No independence of outcomes or fixed dark subspace is needed. A common bound $0<\bar q\le1$ gives expected continued attempts at least $1/\bar q$ and expected injected photons at least $K/\bar q$. A zero bound means no improvement; stopped runs receive only finite-budget accounting. Every attempt injects all $K=2L$ photons.

At finite inverse temperature $\beta_j\ge0$, before the first accepted exit, any non-good exit is accepted with total probability at most $e^{-\beta_jg}$. Let $A_{j-1}$ denote no earlier accepted exit, with its indicator zero after stopping. A safe unconditional statement for predictable random controls is

\[
P(\text{improvement by }T)
\le\min\left(1,\sum_{j=1}^T
E[\,1_{A_{j-1}}(q_j+e^{-\beta_jg})\,]\right).
\]

At zero temperature omit the thermal term. Deterministic norm-time envelopes and deterministic almost-sure lower bounds on $\beta_j$ may replace these random quantities. A realized history-specific sum is not an unconditional numerical bound, and replacing random $\beta_j$ by its mean is unjustified. The implication “improvement requires a first accepted exit” remains valid even if later behavior outside the bad class is arbitrary.

For exponential finite-temperature conclusions the thermal escape contribution must be exponentially controlled too, for example by a deterministic $\beta_jg\ge c_\beta L$. Positive $g$ alone does not suffice. In particular $\beta=0$ is vacuous here; no claim is made about P65's actual anneal or tested graph panel.

## 8. Scope and obligations

| Obligation | Status |
|---|---|
| Taylor cross-range dimension at most $ph$ | Passed by nested Krylov-range induction |
| Norm remainder $e^\tau\tau^{p+1}/(p+1)!$ | Passed by the factorial tail comparison |
| Singular tail bound from a nonunitary approximant | Passed by the cross-kernel/SVD intersection |
| Physical low-rank comparison and $K$-photon constant | Named pinned P71 dependency |
| Exact-rank event constant | Named pinned P69 dependency through P71 |
| Zero coupling, zero time and degree zero | Passed; exact block-local cases separated |
| Fixed $h$ and small norm-time window | Passed with the stated constants and limits |
| Growing $h$ | Only the weaker certified rate stated above; no exponential-in-$L$ inference |
| Marked histories and finite temperatures | Passed with conditional hazards/first-exit expectations |
| Generic graphs, P65 panel, wall-time/QPU budgets, novelty, positive optimization | Not established |

The proof concerns one time-independent Hamiltonian during each shot. Arbitrary time-dependent Hamiltonians or products of different exponential segments do not share the displayed single-$X$ Krylov argument and are not covered. Changes of logical blocks, additional modes, nonunitary filters, different source/decoder or extra unmodeled coherent routing likewise require their own argument.

The parameter $\tau=|t|\|H\|$ is dimensionless norm-time. It is not simulator CPU time, wall time, calibrated hardware duration or a QPU resource price. The cost graphs are explicit and classically easy: connected components or six whole-clique unions supply classical certificates. The prescribed warm start is not a claim about typical random initialization.

The strongest conclusion is the finite raw-event bound and its scoped fixed-rank low-norm-time obstruction, conditional on the named P71/P69 transport lemma. This review has not altered a manuscript, shared ledger, global research status or any numerical artifact. The positive optimizer objective and publication-level novelty remain open.
