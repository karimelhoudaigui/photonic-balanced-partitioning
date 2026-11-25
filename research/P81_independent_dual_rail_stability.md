# P81 independent dual-rail stability reconstruction

26 November 2026. **Primary verdict: the proposed stability bound and exact balanced-feasibility rigidity follow under the hypotheses below.** The reconstruction includes the assignment argument and the $N=2$ counterexample. The classical-mixture statement requires conditional, not unconditional, Bernoulli independence. This note is frozen before reading another P81 proof or verdict; ROOT supplied the candidate formulas and route, so this is before-reading reconstruction, not a discovery claim.

## 1. Exact setting

Let even $N\ge4$. There are $N$ qubit pairs of rails, hence $2N$ modes and **$N$ photons**, one per input pair. Let $U\in U(2N)$ be a single fixed lossless passive mode unitary. For $x\in\{0,1\}^N$, let $|x\rangle$ occupy rail $x_b$ of input pair $b$. These are orthonormal Fock states with distinct occupied modes.

The calibration source is the diagonal density matrix
  \[
  \rho_{\rm bal}=\binom{N}{N/2}^{-1}
  \sum_{|x|=N/2}|x\rangle\langle x|.
  \]
It is the uniform incoherent mixture of all balanced basis strings. It is not the coherent Dicke superposition or a mixture of visited strings.

Let $M_a$ be the total photon occupancy of output pair $a$. Write
  \[
  \varepsilon=\Pr_{\rho_{\rm bal},U}[\exists a:\ M_a\ne1].
  \]
The event refers to the full raw output law, with no heralding denominator. Define $\mathcal F_\nu=\sum_a\mathbb E_{\nu,U}[M_a(M_a-1)]$ for either the balanced mixture or the uniform mixture of all $2^N$ code basis states.

We will construct a unitary $V$ consisting of a permutation of whole qubit pairs and one independent $2\times2$ unitary per pair, such that
  \[
  \|U-V\|_F^2\le C_N\varepsilon,\qquad
  C_N=\frac{4N(N-1)^2}{N-2}.
  \]

## 2. Nonnegative factorial-pair kernel

Fix output pair $a$. Let $u_{b\sigma}\in\mathbb C^2$ be column $\sigma$ of its $2\times2$ input block $U_{ab}$, and put
  \[
  R_{ab}=U_{ab}U_{ab}^\dagger,\quad
  t_{ab}=\operatorname{Tr}R_{ab},\quad
  B_{ab}=t_{ab}/2.
  \]
Unitarity gives $\sum_bR_{ab}=I_2$ and $\sum_a t_{ab}=2$. Thus $B$ is nonnegative with every row and column summing to one.

For distinct occupied input modes from pairs $b\ne c$, normal ordering of $M_a(M_a-1)$ gives the kernel
  \[
  K_{bc}^{\sigma\tau}
  =\|u_{b\sigma}\|^2\|u_{c\tau}\|^2+
    |\langle u_{b\sigma},u_{c\tau}\rangle|^2\ge0.
  \]
Indeed $M_a(M_a-1)=\sum_{r,s\in a}a_r^\dagger a_s^\dagger a_s a_r$; on an input with one photon in each chosen mode, the two possible contractions produce these two terms. Terms using the same input photon vanish. Consequently
  \[
  \mathbb E_{x,U}[M_a(M_a-1)]
  =\sum_{b\ne c}K_{bc}^{x_bx_c}.
  \]
This is an ordered-pair sum, not half that sum.

Under the uniform all-code mixture each $(\sigma,\tau)$ has probability $1/4$, while
  \[
  \sum_{\sigma,\tau}K_{bc}^{\sigma\tau}
  =t_{ab}t_{ac}+\operatorname{Tr}(R_{ab}R_{ac}).
  \]
It follows that
  \[
  F_{{\rm all},a}
  =\frac{6-\sum_b[t_{ab}^2+\operatorname{Tr}(R_{ab}^2)]}{4}
  \ge1-\sum_bB_{ab}^2.
  \]
For the inequality, $0\le R_{ab}\le I_2$ implies
$\sum_b\operatorname{Tr}(R_{ab}^2)\le\sum_b\operatorname{Tr}R_{ab}=2$.

For the uniform balanced source, sampling two distinct bit positions gives
  \[
  \Pr(x_b=\sigma,x_c=\tau)=
  \begin{cases}
  (N-2)/[4(N-1)],&\sigma=\tau,\\
  N/[4(N-1)],&\sigma\ne\tau.
  \end{cases}
  \]
Every coefficient is positive for $N\ge4$. Termwise comparison of the nonnegative kernels therefore gives
  \[
  \mathcal F_{\rm all}
  \le\frac{N-1}{N-2}\mathcal F_{\rm bal}.
  \]

On a code output every factorial pair moment vanishes. On any output with total photon number $N$,
$\sum_aM_a(M_a-1)\le N(N-1)$. Hence
  \[
  \mathcal F_{\rm bal}\le N(N-1)\varepsilon,\qquad
  \mathcal F_{\rm all}\le
  \frac{N(N-1)^2}{N-2}\varepsilon.
  \]
The fixed total photon number is essential to this upper bound.

## 3. Assignment lemma proved internally

For every doubly stochastic $N\times N$ matrix $B$, some permutation $\pi$ satisfies
  \[
  \sum_a B_{a,\pi(a)}\ge\sum_{a,b}B_{ab}^2.
  \]

Here is a complete support-and-decomposition argument. In the bipartite positive support of $B$, any row set $A$ has total mass $|A|$, all entering its neighbor columns, whose total column mass is at most their number. Thus $|\mathcal N(A)|\ge|A|$.

To see why this guarantees a perfect matching, take a maximum-cardinality matching and suppose a row is unmatched. Explore alternating paths from that row, following unmatched edges to columns and matched edges back to rows. A reached unmatched column would augment the matching. Otherwise every reached column is matched to a reached row other than the starting row; every neighbor of a reached row is reached. The reached rows therefore outnumber their neighbor columns by one, a contradiction. Thus a positive-support perfect matching exists.

Subtract $\theta$ times its permutation matrix, where $\theta$ is the smallest matched entry. If $\theta=1$, the matrix already is that permutation matrix. Otherwise divide the residual by $1-\theta$: it is doubly stochastic and has strictly smaller positive support. Iteration terminates because at least one positive entry vanishes each time and zeros remain zero. Recombining the steps writes $B=\sum_j\lambda_jP_{\pi_j}$ with $\lambda_j\ge0$, $\sum_j\lambda_j=1$.

Finally,
$\sum B_{ab}^2=\langle B,B\rangle=\sum_j\lambda_j\langle B,P_{\pi_j}\rangle$.
At least one matching has weight at least this average, proving the claim. No external matching or decomposition theorem is left as a citation dependency.

## 4. Off-block mass and unitary completion

Choose that assignment and define
  \[
  \delta=\sum_a\sum_{b\ne\pi(a)}\|U_{ab}\|_F^2
  =2\left(N-\sum_aB_{a,\pi(a)}\right).
  \]
The preceding moment and assignment inequalities imply
  \[
  \delta\le2\left(N-\sum_{a,b}B_{ab}^2\right)
  \le2\mathcal F_{\rm all}.
  \]
This $\delta$ is one-particle matrix mass, not a probability.

Each matched block $A_a=U_{a,\pi(a)}$ is a contraction. Choose a unitary polar completion $Q_a$ by an SVD, including arbitrary unitary completion on zero singular subspaces. Its singular values $s_{a1},s_{a2}\in[0,1]$ give
  \[
  \|A_a-Q_a\|_F^2
  =\sum_i(1-s_{ai})^2
  \le\sum_i(1-s_{ai}^2)
  =2-\|A_a\|_F^2.
  \]
Set $V_{a,\pi(a)}=Q_a$ and other blocks to zero. It is unitary. Summing the last inequality costs at most $\delta$ on matched blocks, while all unmatched entries cost exactly $\delta$. Therefore
  \[
  \|U-V\|_F^2\le2\delta\le4\mathcal F_{\rm all}
  \le\frac{4N(N-1)^2}{N-2}\varepsilon.
  \]
This proves the claimed constant, including $\varepsilon=0$.

## 5. Full-sector stability and the classical law at V

On the entire $N$-photon sector, second quantization is the restriction of $U^{\otimes N}$ to the symmetric tensor space. Telescoping the tensor product gives
  \[
  \|\Gamma_N(U)-\Gamma_N(V)\|_{\rm op}
  \le N\|U-V\|_{\rm op}.
  \]
For a pure input, output trace distance is at most the norm of the vector difference; mixed inputs follow by convexity or purification. Photon counting and any common classical postprocessing contract trace distance. Thus for every input density matrix in that sector,
  \[
  d_{\rm TV}(p_U,p_V)
  \le\min\{1,N\|U-V\|_{\rm op}\}
  \le\min\{1,N\sqrt{C_N\varepsilon}\}.
  \]
The last coefficient is exactly
$2N(N-1)\sqrt{N/(N-2)}$, asymptotic to $2N^2$.
This is an absolute TV bound, not relative control on rare-event probabilities or an advantage gap.

For a code basis input, $V$ sends each input photon to a distinct output pair. Within its pair it chooses a rail with the probabilities of one column of $Q_a$. The full output-bit law is a product of $N$ Bernoulli laws; ordinary labeled distinguishable particles give exactly the same count distribution there. No inter-pair bosonic interference remains.

For a classically samplable diagonal mixture, first sample its basis string and then those conditional Bernoulli laws. The unconditional mixture can be correlated. The polynomial draw/arithmetic count presupposes efficient access to those local probabilities and to the source-mixture sampler; preparation, representation and finite-bit approximation costs remain paid. The norm result itself needs no such source representation, but arbitrary entangled inputs do not inherit this efficient-sampler conclusion. Equality with a distinguishable law here is at $V$, not a claim of exact equality at the original $U$.

## 6. Exact balanced-feasibility rigidity

Suppose the uniform balanced basis source always yields a feasible output: one photon per pair **and** exactly $N/2$ occupied one-rails. Each basis input must then succeed with probability one, since a finite average of nonnegative failure probabilities is zero. Code leakage is zero, so the preceding theorem gives $U=V$.

For any fixed balanced input, the output bits under $V$ are independent Bernoulli variables $Y_a$. Their sum is constant, so
$0=\operatorname{Var}(\sum_aY_a)=\sum_a p_a(1-p_a)$.
Every term vanishes. Each local column used by such an input is therefore deterministic. Both bit values occur in balanced basis inputs at every input pair; unitarity of each $2\times2$ block makes it monomial.

After accounting for the pair permutation, let $F$ be its set of input bits that are flipped. For every balanced $x$, preservation of weight requires
  \[
  N/2+|F|-2\sum_{b\in F}x_b=N/2.
  \]
If $F$ is nonempty and proper, choose $b\in F,c\notin F$ and a balanced input with $x_b=1,x_c=0$. Swapping those two bits preserves input balance but changes the sum over $F$ by one, contradicting the displayed condition. Thus $F=\varnothing$ or $F=[N]$.

The exact allowed form is therefore a qubit-pair permutation, arbitrary rail phases, and either no bit flips or a global bit complement. Conversely these forms send every balanced basis state to another balanced basis state up to phase. Mere exact code preservation is weaker: local Hadamard blocks preserve one photon per pair while generally changing Hamming weight.

## 7. Boundary checks and excluded inferences

* **N=2 fails.** With pairs $(a_0,a_1)$ and $(b_0,b_1)$, physically swap only $a_1$ and $b_0$. Balanced $01$ is unchanged and $10$ has its two occupied modes exchanged, so both balanced Fock states are fixed and feasible. Inputs $00$ and $11$ instead put both photons in one output pair. This mode permutation is not a permutation of whole pairs with local $2\times2$ blocks. The equal-bit pair probabilities are zero, exactly where the comparison proof fails.
* **Larger feasibility leakage is a valid upper bound.** Code failure is contained in full infeasibility, so one may replace epsilon by an upper bound on average full feasibility failure. Quantitative proximity to monomial blocks does not follow from the argument given here; the monomial refinement above uses exact feasibility.
* **A sampled or coherent source changes the premise.** On a single chosen code input, swapping two occupied rails in different pairs fixes that Fock state but is generally not a whole-pair permutation. Thus zero leakage on a visited subset cannot replace uniform coverage. A coherent balanced superposition has off-diagonal input terms absent from the mixture moment calculation; no theorem for it is established here.
* **Fixed U and full raw accounting matter.** Input-dependent interferometers, loss, additional modes with heralding, nonlinear or nonpassive transformations, and discarding failed outputs do not satisfy this unitary/raw-source contract. An empirical average is not the exact uniform leakage parameter without a separate valid inference.
* **No universal optimizer or resource conclusion.** The calibration bound concerns this one fixed map. It grants no guarantee for an arbitrary sequence of newly selected maps, arbitrary entangled-source sampling, equal wall-time budgets or free state preparation. The dimension-dependent constant grows as $4N^2$ and the TV coefficient as $2N^2$.

The proposed mathematical implications have no remaining internal gap under this contract. This note proves neither novelty nor positive optimization performance. Only this new file is written. No other P81 proof/verdict, P79/P80 experimental output, external source, scientific code, import, AST, test, RNG, numerical evaluation, backend, QPU call or manuscript change was used.
