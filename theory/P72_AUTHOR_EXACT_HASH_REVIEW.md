# P72 exact-hash author review

25 November 2026. **Primary verdict: proved as written**, under the source's stated model and pinned P69/P71 dependencies. All finite inequalities, endpoint cases, fixed-rank rates, growing-rank limitations and first-exit statements checked below are valid. No mathematical source correction is requested.

## Exact source, coverage and independence

Reviewed the complete file research/P72_low_rank_Hamiltonian_finite_time_transport.md in .local/p66-dark-audit:

- SHA-256 f48f7cd39d67788635e8da60d84ebae7125a059f51a48079c49486bde035b76f.
- **All 310 raw lines, 1–310**, including every display and final limitation.
- The supplied author artifact was frozen but uncommitted because that worktree's index was unavailable. This review identifies its exact bytes by hash; it does not invent an author Git commit.

Before reading this author source, I froze the 247-line theory/P72_independent_finite_time_transport.md at commit 3329c6aca2fb2ebda572bdda9e2624b002161f3e, SHA-256 c441aecb7a9b18539fa0764db39c15283e5edc9ffb590e30efddaf41e6c1c34a. That file remains unchanged. Both derivations received the same coordinator's candidate and Taylor/Krylov suggestion, so this is independence before author reading, not an unrelated-method claim or formal verification.

The proof-audit and mathematical-proofreading workflows were applied. Only this review was written. No import, code execution, numerical calculation, test, graph, random draw, native call, experiment, external source query or QPU operation was used.

## The named P71 condition is resolved for this application

The P72 source pins P71 SHA-256 c320f925b53f68738931da93ef28bb0a2f84f887988404153f974dae8b6cfe03 and P69 SHA-256 37e59633734c16277ed2649c4761fa84a86a8006b164fd4263963e37d7759de4. These are exactly the lemma and constants used in the prior independent P72 derivation.

I read the complete P71 exact-hash review, theory/P71_AUTHOR_EXACT_HASH_REVIEW.md, at commit cd59bcfd96eedb8dbf76c258e63f996ee6987567 and verified its SHA-256:

    7a626452c8d6e7cfbaa000bb37fc3f77a736cd5d5c880b011f650af68e7da992

It reviews all 301 lines of P71 at commit b2f84ccb7383331605e128351c927e66ae0d84cf, the same c320 source, and gives the primary verdict proved as written. It checks the complete CS construction, singular endpoints, unitary truncation, symmetric photon lift, trace/TV coefficient $K$ and pinned P69 constants.

Thus the named P71 condition in my earlier P72 report is discharged for the present application by that exact-source peer review. The earlier file's historical conditional verdict is not rewritten. I previously read P71 as a lemma dependency; I do not claim a new independent audit of all P71, its independent 348-line proof, or its full transcript theorem in this review.

The common-classical-postprocessing condition in P71 governs its **transcript comparison**. P72 uses the single-shot full-PNR event bound and then a direct first-exit proof for the actual process. It does not compare transcripts carrying different applied-matrix tags, timing fields or operation-specific diagnostics, and it needs no assertion that such fields coincide. The same two raw target events and the specified CF source are retained in the pointwise application.

## Obligation map

| Author lines | Obligation | Result |
|---|---|---|
| 28–67 | Logical blocks, source, finite statement and endpoints | Passed |
| 69–93 | Common Krylov range and linear $ph$ rank bound | Passed |
| 95–115 | Operator Taylor tail and cross-block compression | Passed |
| 117–133 | Singular-value lemma by dimension intersection | Passed |
| 135–166 | Genuine unitary comparator and raw event/TV constants | Passed using exact P71 dependency |
| 168–201 | Fixed $h$, sublinear norm-time and rate $I(\alpha)$ | Passed |
| 203–222 | Small linear norm-time window and $\gamma$ | Passed |
| 224–251 | Growing $h$, counter-scaling and certificate limitation | Passed |
| 253–296 | Predictable fresh attempts and first accepted exit | Passed under inherited P66 acceptance |
| 298–310 | Scientific scope and disposition | Passed |

## Critical finite checks

With $d=2L$, $K=2L$, the source has $L$ distinct occupied modes per block and the targets are the two full-CF one-block occupations. The complete one-particle propagation is $U=e^{itH}$ for one Hermitian block matrix $H=\left(\begin{smallmatrix}X&Z\\Z^\dagger&Y\end{smallmatrix}\right)$, fixed during the shot. The parameter $h$ is the integer Hamiltonian coupling-rank bound, not the graph matching weight and not the optical rank.

The recurrence

\[
R_{k+1}=XR_k+Z(H^k)_{BB},\qquad R_0=0,
\]

puts every polynomial cross range inside the **same nested** span of $X^a\operatorname{range}Z$, $0\le a<p$. Therefore $\operatorname{rank}(Q_p)_{AB}\le ph$; no quadratic sum over unrelated monomial rank estimates is needed. Arbitrary within-block detunings and noncommutation are allowed.

For $m=p+1$, the factorial inequality $(m+j)!\ge m!j!$ gives the claimed remainder

\[
\|U-Q_p\|_{\rm op}\le e^\tau\tau^m/m!=E_p(\tau),
\qquad \tau=|t|\|H\|_{\rm op}.
\]

Compression preserves that upper bound. For $q=ph<d$, the top $q+1$ right-singular-vector span of $U_{AB}$ intersects the kernel of $(Q_p)_{AB}$ because their dimensions sum to at least $d+1$. A unit vector in the intersection proves $s_{q+1}(U_{AB})\le E_p$. The relevant kernel is correctly the cross-block kernel, not the kernel of the full polynomial matrix. Repeated or zero singular values do not invalidate the dimension argument.

P71 is then applied to the actual **unitary $U$**. It supplies a unitary comparison matrix $V$ with cross rank at most $q$ and distance at most $\delta(s_{q+1})\le\sqrt2 E_p$. The symmetric $K$-photon lift and complete-law TV bound contribute exactly $K$, yielding

\[
P_U(\mathrm{good})\le\min\{1,p_{L,q}+\sqrt2 K E_p\}.
\]

The optional $\delta(\min(1,E_p))$ refinement is valid since $\delta$ is increasing and a unitary cross block is a contraction. There is no missing factor two, Fock factorial or CF denominator. The nonunitary $Q_p$ is never treated as a physical proposal or inserted into P69.

The endpoints are correctly separated. At $h=0$ the propagator is block-local and cannot move an $L/L$ source into one block. At $t=0$ it is identity. At $p=0$, $Q_0=I$, $q=0$ and the finite error is $e^\tau\tau$, with $p_{L,0}=0$. Zero $\tau$ has exact zero remainder, so no logarithm of zero or $0^0$ is used. At $q\ge d$ only the trivial bound is taken; the source also correctly notes that $q\ge L$ can already make the P69 term trivial even if $q<d$.

## Asymptotic constants and growing-rank distinction

For fixed $h\ge1$, $p=\lfloor\alpha L/h\rfloor$, $0<\alpha<1$, gives $m/L\to\alpha/h$ and $q\le\alpha L$. The factorial integral proves

\[
\log E_p\le m[\rho+1+\log\rho],\qquad \rho=\tau/m.
\]

Thus $\tau=o(L)$ makes this error super-exponentially small in $L$ in the stated upper-bound sense. The P69 target factor has exponent $I(q/L)\ge I(\alpha)>0$; the source factor is at most one. The resulting bound $P_U(\mathrm{good})\le e^{-LI(\alpha)+o(L)}$ correctly absorbs its constant prefactor and the $K=2L$ error prefactor. It is a sufficient upper rate, not an achieved probability.

In the small linear window, $c+\log(ec)<0$ implies $ec<1$. With $\tau\le cp$ and $m=p+1$, the source's replacement of $(ec)^m$ by the larger $(ec)^p$ is in the correct direction. Consequently $E_p\le e^{-\gamma p}$ for $\gamma=-(c+\log(ec))>0$. The rate $\min(I(\alpha),\gamma\alpha/h)$ absorbs all polynomial prefactors for fixed $h$.

The author does not silently extend this to growing $h$. Under $h_L=o(L)$ and $\tau_L=o(L/h_L)$, only $\log E_p\le-\omega(L/h_L)$ follows generally. In the author's example, $h_L=\lceil\sqrt L\rceil$, $\tau_L=\sqrt L/\log L$, $m=\alpha\sqrt L+O(1)$. The elementary factorial integrals give

\[
\log E_p
=\tau_L+m(1+\log(\tau_L/m))+O(\log m)
=-\alpha\sqrt L\log\log L+O(\sqrt L).
\]

This checks the displayed coefficient and error scale; it is sublinear in $L$. The example limits the **remainder certificate**, not the actual physical event probability. When $h_L$ is comparable to $L$, bounded degree can leave $K E_p$ large even if $E_p\to0$. The additional explicit exponent condition in section 8 is sufficient, and the finite formula remains the safe general conclusion.

## First-exit proof and cost restrictions

For the P66 original or connected cost family, only the two full-block targets improve on the four bad states. Other bad states tie; every feasible state outside those six has increase at least $g>0$. A fresh normalized CF source is prepared at each current state. Collisions self-loop, and only accepted CF optical proposals update that state.

The author permits predictable choices of $H_j,t_j,h_j,p_j$ before the new shot. Since the finite theorem holds for each such choice, its random bound $b_j$ is a valid conditional good-event bound. Its cases are correctly ordered: $h_j=0$ or $t_j=0$ gives zero; otherwise $q_j\ge d$ gives one, and $q_j<d$ uses the displayed finite expression.

At zero temperature, before improvement the process remains in the bad class. The indicator-weighted expectation of $b_j$ therefore bounds each possible first exit. At finite temperature the inherited P66 Metropolis rule gives uphill acceptance at most $e^{-\beta_jg}$, for $\beta_j\ge0$. Summing these conditional first-exit bounds proves the source formula. No independence, comparison-process coupling or common dark subspace is needed. An arbitrary different acceptance rule or an extra Hastings factor would require verifying the same uphill bound; no detailed-balance claim is used here.

Random history-specific degrees, ranks, norm-times and temperatures stay **inside expectations**, or are replaced by deterministic almost-sure envelopes. In the fixed-$h$ corollary, the supremum of $\tau_j/L$ over all still-bad histories and relevant attempts is explicitly controlled. A common analysis degree can be chosen whether or not it was physically logged by the controller. Thermal escapes must separately satisfy the required error budget. No conclusion is made for arbitrary thermal schedules or arbitrary initialization.

All optical attempts retain $K=2L$ injected photons and complete raw outcomes. There is no free CF repetition, source repair or external classical candidate insertion in this chain statement. The source's raw-probability obstruction supplies no measured total-resource comparison.

## Scope, proofreading and closure

The author's exclusions match the proof: one static Hamiltonian per shot, fixed logical blocks and source/target decoder, full Hermitian norm in $\tau$, and no unaccounted coherent segments, extra modes, filters or measurement/feedforward. Products of different propagators cannot inherit the one-$X$ Krylov bound by assertion. Large within-block detunings are explicitly included in $\|H\|$.

Dimensionless norm-time is not wall time, simulator CPU time, calibrated optical duration or a QPU budget. The graphs and prescribed warm starts remain engineered and classically transparent. Nothing here proves generic graph hardness, a P65-panel obstruction, device/source readiness, positive optimization or novelty.

Mathematical proofreading covered all 310 author lines and this review. No objective sign, index, normalization, degree, endpoint or range inconsistency was found. Routine author edits: none. Mathematical-token changes: none. Validation consisted only of text reading, source/review hash checks and Git whitespace checking; no build or test was run in this expressly static task.

There is no remaining P72 mathematical gap under the stated model and exact pinned dependencies. The previously conditional P71 input is supported by the identified exact-source peer review, without claiming a new audit of all P71 here. The author proof and the independent 247-line derivation remain unchanged.
