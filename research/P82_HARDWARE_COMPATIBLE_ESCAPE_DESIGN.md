# P82: nonuniform split, phase scattering and collision repair

26 November 2026. **One concrete changed optimizer is specified below; its positive gate is OPEN.** The equal-loading mean-drift explanation is rejected analytically. Nonuniform loading has an exact surviving two-photon cost term, but that term has a polynomial classical control. Only the larger, raw basin-entry hypothesis remains prospective. No science execution, imports, tests, AST, random draw, numerical allocation, external search, QPU call or manuscript edit accompanies this design.

This checkpoint starts from the healthy independent branch at 13ce8144b49ec91e916e9ca3f7b178c3490547bf. Local frontier reading included the P65 actual main veto/portfolio; P67 flux and covariance; P68 marked-current restriction; P69 full proof, P71 finite statement, P72 norm-time/scope; P74 physical profiles and P76 full-Fock/filter audit; P59 exact-response receipts; P63 actual first-gate veto; and the already reconstructed P77–P81 scopes. ROOT main was 514a42181cc2a1c34e54de424a39cdae510aa204 at first reading and b1fd597f47cf6c18ecb6aa178cf45d08977cda00 at the later receipt lookup. No P79/P80 raw outputs were opened. All earlier proofs and negative records remain intact.

## 1. The change and its precise first gap

Use a weighted undirected graph on **2K vertices and K photons**, with even $K=2d\ge4$. A current balanced subset $S$ has size $K$; write $T=S^c$. This is the direct vertex-occupation model, not $2K$ logical qubits or a balanced logical Dicke register.

The circuit first splits each occupied input into a kept bank and a receiving bank, with nonuniform known probabilities. A phase-programmed interferometer then mixes the receiving bank. At detection, collisions are repaired by an explicit graph-blind feasible decoder rather than discarded or converted to self-loops. The optimizer is a paid basin-hopper, not a claimed Gibbs/Metropolis sampler.

This changes P65's source-to-output architecture, graph compiler and collision treatment. It does not rename the rejected positive-adjacency Cayley grid. P59 already established a fixed-intensity decoded mean channel; that fact is not new here. P63's extensive-phase/top-K optimizer failed its fixed FAST gate. Neither is evidence that this new decoder will work.

**First unresolved implication:** at genuinely large replacement distance, does the full repaired bosonic law enter cheaper basins more often per paid resource than independently optimized D, exact small-group interference controls, recipient-frontier search and serious classical basin search? A nonzero two-photon coefficient does not resolve this.

## 2. Complete source and passive matrix

Draw uniform independent orderings of $S$ and $T$ as paid classical marks, before observing the shot. Divide the input ordering into two lists $I_0,I_1$ of size $d$. Order receiving outputs as pairs $(a_r^+,a_r^-)$, $1\le r\le d$. These are port assignments, not good-partition masks.

Define a fixed centered loading profile
  \[
  h_j=(2j-d-1)/(d-1),\quad
  o_j=\rho(1+\eta h_j),\quad p_j=o_j/(1+o_j),
  \]
and use the same profile on $I_0$ and $I_1$. Parameters satisfy $\rho>0$, $0\le\eta<1$. A future macro-move contract should keep every $p_j$ between fixed positive bounds away from zero and one. The $\eta=0$ case is a required cancellation control. No profile is fitted to an optimum.

Inject one photon in each of the $K$ kept-bank input ports, and vacuum in the receiving inputs. Put
$C=\operatorname{diag}(\sqrt{1-p_i})$ and $D=\operatorname{diag}(\sqrt{p_i})$ in their input order. Apply the exact mode unitary
  \[
  \widetilde U=
  \operatorname{diag}(I_K,W_\phi)
  \begin{pmatrix}C&iD\\ iD&C\end{pmatrix}.
  \]
Thus its occupied columns are $[C;\,iW_\phi D]$. This needs only $K$ ordinary splitters followed by a receiving-bank passive mesh. No inverse mesh on a vacuum bank is required.

Let $F_{rj}=d^{-1/2}\exp(2\pi i(r-1)(j-1)/d)$ and
  \[
  W_\phi=\frac1{\sqrt2}
  \begin{pmatrix}F&D_\phi F\\F&-D_\phi F\end{pmatrix},
  \qquad D_\phi=\operatorname{diag}(e^{i\phi_r}).
  \]
It is unitary and every entry has modulus $1/\sqrt K$. Physically it is two fixed Fourier meshes, programmable phases on one half, and a parallel balanced-splitter layer. Graph changes alter those internal phases; they do not require a nonlinear optical cost gate.

## 3. Explicit optimum-blind phase compiler

All graph weights $w_{uv}$ and the current $S$ are available to every control. Form
  \[
  Q_{rs}=w_{a_r^+,a_s^+}+w_{a_r^-,a_s^-}
          -w_{a_r^+,a_s^-}-w_{a_r^-,a_s^+},
  \quad A=F\operatorname{diag}(o_j)F^\dagger,\quad
  J_{rs}=Q_{rs}|A_{rs}|^2,\quad r\ne s.
  \]
Choose initial phases from independent uniform fourth roots of unity, using the paid marks. Perform a prospectively fixed number of coordinate sweeps in port order:
  \[
  H_r=\sum_{s\ne r}J_{rs}e^{i\phi_s},\qquad
  \phi_r\leftarrow\arg H_r\quad(H_r\ne0);
  \]
keep $\phi_r$ when $H_r=0$. Each update increases or preserves the explicit classical quantity
$E(\phi)=\sum_{r<s}J_{rs}\cos(\phi_s-\phi_r)$.
This defines $\phi(G,S,\mathrm{marks})$ completely, given $\rho,\eta$ and the sweep count. It uses no $C^*$, optimal mask or selected target. It is a small classical XY optimization, whose full work and any candidates rounded from its phases must be credited and shared. Angle representation, compilation precision and calibration are not free.

The induced feature is intentionally exposed to classical controls. One particularly strong control rounds the same phases by a random hyperplane to select one member of each receiving pair, removes $d$ uniformly chosen vertices from $S$, and applies the same paid local descent. It is a nonlocal classical move from the SAME compiler, not an optical result.

## 4. Exact full-Fock law and collision-tolerant decoder

Let $R\subseteq S$ be the vertices missing from the kept-bank output, $r=|R|$, and let $y\in\mathbb N^T$ be receiving counts, $|y|=r$. Kept occupations are exactly zero or one. Direct permanent expansion gives the complete normalized raw law
  \[
  \Pr_B(R,y)=
  \left[\prod_{i\in R}p_i\prod_{i\notin R}(1-p_i)\right]
  \frac{|\operatorname{per}W_\phi[y,R]|^2}{\prod_a y_a!}.
  \]
Here $W[y,R]$ repeats rows according to $y$. Kept rows force their original input columns; no other term survives. For each $R$, unitarity gives total receiving probability one. Vacuum in the receiving bank, bunching and identity moves remain in this law.

Let $B_y=\{a:y_a>0\}$ and $h=|B_y|$. Draw $F_y$ uniformly among $(r-h)$-subsets of $T\setminus B_y$, and return
  \[
  X=(S\setminus R)\cup B_y\cup F_y.
  \]
Every ideal lossless shot returns a balanced $K$-subset. Collision multiplicities and the repair coins remain raw records; no repeat-until-CF denominator occurs. This repair is classical work, not photons physically filling the missing vertices.

D uses the same formula with $|\operatorname{per}W[y,R]|^2$ replaced by $\operatorname{per}|W[y,R]|^2$. In this flat family the receiving counts are exactly $r$ independent uniform draws on $T$. After the same repair, its receiving subset is uniform among $r$-subsets, independent of $R$. This is a cheap exact classical D control. **D must also optimize independent loading, circuit and proposal families outside this flat restriction.**

## 5. Hand-checked cancellation and the surviving r=2 term

For $r=1$ no phase effect exists. For $r=2$ and EACH fixed removed pair, bosonic bunching at a particular receiver has probability $2/K^2$. The repaired inclusion probability of each receiver is exactly $2/K$: its click probability is $2/K-2/K^2$, and repair from bunches elsewhere adds $2/K^2$.

With equal loading, removed pairs are uniform. For fixed distinct receivers $a,b$, $\sum_{i<j}|\operatorname{per}W[\{a,b\},\{i,j\}]|^2=1-2/K$, independent of phases. Including repaired bunches makes the receiving pair uniform. Cross terms $\Pr(i\in R,a\in X\mid |R|=2)=4/K^2$, for $i\in S,a\in T$, are also phase blind. Consequently the complete $r=2$ mean cut equals the D mean, for every graph. The equal-loading leading mean explanation is **REJECTED**, despite phase-dependent conditional pair probabilities.

Nonuniform loading breaks that cancellation. Write $q_0=\prod_{i\in S}(1-p_i)$. For mixed removed pairs $i\in I_0,j\in I_1$, summing their weights before output scoring gives the phase term
  \[
  \frac{q_0}{2}\Re\!\left[
  e^{i(\phi_s-\phi_r)}A_{rs}A_{sr}\right]
  =\frac{q_0}{2}|A_{rs}|^2\cos(\phi_s-\phi_r)
  \]
on receiver pair $(a_r^+,a_s^+)$; its signs on $(+,-),(-,+),(-,-)$ are respectively minus, minus, plus. Same-half removed pairs and repaired bunches have no phase dependence. The linear/single-vertex parts of the cut are phase blind. Therefore the EXACT contribution of the $r=2$ sector to mean cut has phase-dependent part
  \[
  -q_0\sum_{r<s}Q_{rs}|A_{rs}|^2\cos(\phi_s-\phi_r)
  =-q_0E(\phi).
  \]
This is an unconditioned sector contribution, with all other photons' stay probabilities included in $q_0$.

For $K=4$, this reduces to
  \[
  -\frac{q_0}{4}Q_{12}(o_1-o_2)^2\cos(\phi_2-\phi_1).
  \]
It is nonzero when the rectangle contrast and loading contrast are nonzero. Coordinate updates improve or preserve this sector mean for EVERY set of marks, so averaging the uniformly relabeled marks cannot cancel the improvement; strict improvement occurs for nonzero coupling and a nonaligned initial phase. A one-edge receiving graph already supplies a physical algebraic witness, but is trivially solved classically and is not a DEV benchmark.

This surviving term is **not** an irreducible quantum optimizer. It is an explicit polynomial classical phase objective. Fixed $r\le r_0$ full laws can be computed/sampled by enumerating $O(K^{r_0})$ receiving occupations and tiny permanents, with setup and scores paid. Constant-size indistinguishable-species groups are another positive classical control. At macro loading, $q_0$ and the entire $r=2$ sector can be very small; optimizing this coefficient does not prove improvement of the complete mean or basin hazard.

## 6. Actual optimization observable and nonlocal regime

Use a shared bounded classical warmstart and a fixed-budget descent map $\mathcal Q$ on every proposed subset, including its intermediate scored states. Pay every scan, tie coin and score. Do not assume an unbounded descent-to-stationarity algorithm has polynomial cost. Update to a better observed incumbent; no stationary Gibbs claim is made for this current-dependent circuit.

Let $c$ be the actual shared paid incumbent, never an optimum. The exact raw strict-basin hazard is
  \[
  h_B(S,c)=\sum_{R,y}\Pr_B(R,y)
  \binom{K-h}{r-h}^{-1}
  \sum_{\substack{F\subseteq T\setminus B_y\\|F|=r-h}}
  {\bf1}\{C_G(\mathcal Q((S\setminus R)\cup B_y\cup F))<c\}.
  \]
Average over the declared marks and descent coins as well. This nonlinear statistic includes the complete permanent interference at growing $r$, rather than a low count moment. No inequality asserting it beats an efficient control has been proved.

For bisection cost, $r$ and $K-r$ are equivalent through global complementation. The $r=K$ candidate is just $T$, with the same cut; it is not a useful full transfer. Genuinely new displacement beyond three replacements requires $K\ge8$. At $K=4$, the complementary $r=3$ event is only a one-swap and $r=4$ changes no cut. At $K=6$, the 225 two-swap and 400 three-swap candidates are cheap, fully paid classical baselines and cover all cut classes together with smaller swaps. Tiny fixtures establish normalization/interference only.

The prospective hypothesis is limited to larger $K$, a nonnegligible population of $\min(r,K-r)>3$, and useful raw high-order basin entries AFTER the controls below. It is not a claim that the displayed $r=2$ theorem extrapolates.

## 7. Mandatory strongest vetoes and old-bound scope

* **Paid recipient frontier:** draw $R$ from its known classical law and enumerate all $\binom K r\le2^K$ receiving subsets. At the same $R$, its best raw score pathwise dominates every repaired optical candidate; no photonic data are needed to draw the classical $R$. For domination after descent, apply and pay the same capped descent to EVERY enumerated candidate; raw-score domination alone does not prove endpoint domination. Use this control whenever its work fits the grant, especially at finite hardware sizes. P62's exact random-embedding/top-K hypotheses are not this current graph compiler and decoder, but its paid $s=K$ frontier lesson applies directly.
* **First DEV veto, favorable to B:** give fixed classical modes the original graph and their own seeds, charging their setup/adapter work, under B's own paid classical allowance with ZERO assumed optical latency. Include the recipient frontier, phase-hyperplane control, zero-optics continued descent, multi-swap/tempering and FAST. If any one fixed cheap mode beats B on every prospectively fixed DEV anchor, reject before D/species expansion or hardware work. No free per-graph best-of-mode portfolio.
* **Full comparison if that veto survives:** independently train D, at least the exact small-group interference controls, and strong correlated feasible search. Pay all B/D training, sources, raw shots, compiler, phase sweeps, routing, repairs and descent; credit all paid best candidates. A B-versus-flat-D contrast alone cannot pass.
* **P65/P67/P68:** the P65 finite veto is preserved; no grid rerun. Internal phase changes here are not output/input gauge phases, and no transpose coin is used to claim reversibility. Paid individual marks and current-state encoding give covariance in law rather than the exact pathwise graph/stabilizer covariance of P67–P68. Engineered four-clique instances remain easy classical controls, not favorable benchmarks.
* **P69–P72:** the net receiving cross block is $iW_\phi D$, with $K$ singular values $\sqrt{p_i}$; it is not a low-rank weak transport model in these banks. This alone says nothing about ranks in some other target partition. More decisively, the primary event is a classically repaired subset, not the literal full-CF target used by those theorems. Any CF-only diagnostic still receives their applicable rank/tail screen.
* **P74/P76/P81:** there is no nonlinear logical phase, Dicke preparation, composable projected filter or hidden code measurement. The whole passive matrix is used on Fock space. Output code leakage is retained and decoded; no uniform balanced logical-basis code-preservation premise is claimed. Routing pairs are not a protected balanced logical encoding.
* **P77–P80 and earlier decoder work:** a finite single-photon Fock source is not a nonnegative Gaussian pair source, so the positive-hafnian/even-loop samplers do not provide this law. Conversely P59's mean channel and P63's collision-retaining decoder do not establish performance; the P63/P65 FAST failures remain decisive negative precedents.

## 8. Hardware and prospective evidence boundary

Only finite Fock input, vacuum ports, passive splitters/phases and one final count measurement are required. Fourier meshes are fixed; graph-dependent phases and loading angles are compiled and charged. Logical graph labels can be mapped to the fixed occupied input ports, with all mapping/routing included. There are no helper photons, intermediate nondestructive measurements, squeezing, quantum memory or nonlinear gates.

This is compatible with a programmable passive-mode model, not a statement that current Lucy/TGCC supplies a chosen $2K$-mode/$K$-photon job or ideal PNR. The local 24-Nov compatibility snapshot does not authenticate today's allocation. Available ports, inputs, calibration, detector output, losses and all attempt denominators must be verified before a separate hardware contract. The decoder needs click supports, but claims about the lossless full-count law still require complete photon/loss accounting. Lost or hidden samples cannot silently be repaired as if the source were lossless.

Any later qualification must first check the full law, factorials, uniform-loading cancellation, nonuniform rectangle coefficient, D repair law, complement symmetry and the paid frontier. A future DEV card must freeze instances, all caps/seeds/parameters, tie rules, first-failure policy and independent source checks before outcomes. Use fresh unplanted graph draws and uniform relabels with the compiler carried along; label repeats are not independent graph evidence. Fresh held-outs remain unopened until a genuinely surviving DEV gate.

No experiment is allocated by this note. **KEEP only as a falsifiable larger-displacement design; REJECT low-order mean interference, constant intensity, full transfer, or a small-fixture B/D contrast as positive optimizer evidence.** The first missing implication is the total-cost high-order basin advantage after the explicit classical controls. The user's positive target stays OPEN.
