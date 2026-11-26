# P128 — spectral-loss coherent replacement, with bounded primary attribution

Date: 2026-11-26. Parent: `43ada0fe3220e09220ee3eb7acf9e55fc1a73b14`.
ROOT supplied the candidate; the derivation below is a manual reconstruction, not an independent discovery.
No scientific program, import, RNG, experiment, native call, or QPU call was used.

## Claim and disposition

**Primary verdict: proved as written in the ideal-real sampling model specified below.**
For known collision-free input with one photon in each of K occupied modes, let
T be the m-by-K complex signal transfer matrix of a passive, vacuum-environment channel.
Assume a certified operator-norm bound `||T||op² <= eta < 1`, with `eta > 0`.
There is a positive coherent-mixture signal-count law Q satisfying

\[
 \operatorname{TV}(P_T,Q)\le E(K,\eta):=1-(1-d(\eta))^K,\qquad
 d(\eta)=\eta+(1-\eta)\log(1-\eta).
 \tag{1}
\]

This covers the entire raw signal PNR law, including vacuum, loss, and collisions.
It is a classical approximation, not a distinguishable-particle identity.
The exact input-state distance is E; the output distance need not equal E.
Finite-bit worst-case sampling complexity and the precise priority of this fixed-radius choice remain unverified here.
The broad coherent/thermal replacement mechanism and its spectral-loss extension are already established prior art.

## 1. Factorization and its certificate

Set `R=T/sqrt(eta)`. Then R is a contraction and
`Phi_T = Phi_R o Loss_eta`, where the loss acts identically on the K input modes.
For example, the composed vacuum-noise Gram matrix is
`(1-eta)RR† + (I-RR†) = I-TT†`; the signal matrix is `sqrt(eta)R=T`.
This identifies the vacuum passive channel, not a chosen measured environment record.
Unused vacuum inputs can be appended when input and output dimensions differ.
Uniform loss sends the CF input to

\[
 \rho_\eta^{\otimes K},\qquad
 \rho_\eta=(1-\eta)|0\rangle\langle0|+\eta|1\rangle\langle1|.
 \tag{2}
\]

The certificate concerns the occupied matrix, allowing arbitrary complex phases and correlated mode-dependent loss after factorization.
Individual column intensities or a mean transmission do not certify it.
Indeed, K aligned columns of squared norm eta have squared operator norm K eta.
This is the P91/P92 distinction, not a new hardware-efficiency estimate.

## 2. Fixed-radius replacement and exact input error

Let `nu=-log(1-eta)`. Define a single-mode state by a uniform optical phase:

\[
 \sigma_\nu=\frac1{2\pi}\int_0^{2\pi}
 |\sqrt\nu e^{i\theta}\rangle\langle\sqrt\nu e^{i\theta}|\,d\theta
 =e^{-\nu}\sum_{n\ge0}\frac{\nu^n}{n!}|n\rangle\langle n|.
 \tag{3}
\]

This is a nonnegative Glauber-P mixture on a circle: Poisson number statistics, not a thermal Gaussian mixture.
Its vacuum probability is `1-eta`; its one-photon probability is `(1-eta)nu <= eta`.
The inequality follows from `-(1-eta)log(1-eta) <= eta`.
Its mass on n>=2 is exactly `d=eta-(1-eta)nu`.

On every binary occupation string, `sigma_nu^tensorK` has probability no larger than
`rho_eta^tensorK`; outside the binary support the latter has zero mass.
Consequently their probability overlap is `(sigma_0+sigma_1)^K=(1-d)^K`.
Both states are diagonal, hence with trace distance normalized by one half,

\[
 D_{\rm tr}(\rho_\eta^{\otimes K},\sigma_\nu^{\otimes K})
 =1-(1-d)^K\le \min\{1,Kd\}.
 \tag{4}
\]

An equivalent maximal coupling is `N_i ~ Poisson(nu)`, `X_i=1[N_i>=1]`.
Then X_i is Bernoulli(eta); the occupation vectors disagree exactly when some N_i>=2.
CPTP contraction under Phi_R, followed by PNR measurement, proves (1).
No positivity of T, Haar averaging, collision conditioning, or detected-photon herald is used.

For `0<=eta<1`, direct integration of `d'(eta)=-log(1-eta)` gives

\[
 d(\eta)=\sum_{r\ge2}\frac{\eta^r}{r(r-1)}
 =\frac{\eta^2}{2}+O(\eta^3)
 \le\frac{\eta^2}{2(1-\eta)}.
 \tag{5}
\]

Thus K eta² -> 0 suffices as eta -> 0; for K->infinity, K eta <= 1 is a sufficient subregime, not necessary.
The chosen nu is not asserted to minimize the distance over all coherent mixtures or even all Poisson means.
For K=0 or eta=0 the signal law is exactly vacuum; take that branch without division.
The excluded eta=1 limit cannot be substituted into the finite nu formula.

## 3. Explicit classical ideal-real sampler and resource scope

Draw K independent uniform phases, `z_i=exp(i theta_i)`, then form

\[
 \beta=\sqrt\nu Rz=\sqrt{\nu/\eta}\,Tz.
 \tag{6}
\]

Conditional on beta, draw independent counts `n_j ~ Poisson(|beta_j|²)`.
Passive vacuum channels map a coherent input to a coherent signal output, which proves this sampler for Q.
Its matrix-vector work is O(mK) real arithmetic operations, in addition to K phase draws and m Poisson draws.
Input acquisition, spectral certification, matrix preparation, random primitives, output handling, decoder, and scores must all be paid.
This is neither a wall-clock benchmark nor a polynomial finite-bit theorem by arithmetic counting alone.

The conditional total mean is `Lambda=||beta||² <= K nu`.
The phase-averaged signal mean is `(nu/eta)Tr(T†T)`, whereas the true CF mean is `Tr(T†T)`.
Thus Q is not moment matched and not the distinguishable law D.
Realizing (6) physically through the original T would use coherent input mean `K nu/eta > K`.
Through the mathematical residual channel R its coherent input mean is K nu.
Neither realization supplies a matched photon-budget comparison with the original experiment.

## 4. Surplus counts, common decoding, and history

P_T is supported on total count <=K; Q can output more than K photons.
One may keep Q on the common count alphabet, with P_T zero on these extra records.
Alternatively predeclare a map F that is identity on totals <=K and sends every surplus record to one fixed legal record.
Then `F_*P_T=P_T` and `TV(P_T,F_*Q)<=E`; there is no renormalization or retry.
If the chosen record is vacuum, its algorithmic overflow origin must be disclosed, never called an observed physical vacuum.
The surplus probability itself is at most E.

A bounded-output ideal-real version first draws total count from
`{0,...,K,OVERFLOW}` with Poisson(Lambda) probabilities.
On total n<=K it draws `Multinomial(n; |beta_j|²/Lambda)`; on overflow it applies F, and Lambda=0 gives vacuum.
This exactly samples F_*Q without materializing an arbitrarily large occupation vector.
It still presumes exact real probability primitives.

Any identical classical decoder, repair, or quench contracts (1).
For a finite classical-observation adaptive protocol, a uniform per-history certificate gives transcript TV at most the sum of its per-attempt bounds, capped at one.
This requires the same policies/postprocessing and fresh randomness; it does not cover coherent memory, hardware timing trajectories, or arbitrary measured environment flags.
Conditioning on a rare herald can amplify the error; no relative conditional guarantee follows.

## 5. First unclosed computational bridge

An executable finite-bit theorem needs a representation of complex T and its certificate, approximations to nu/phases/intensities,
and bounded discrete sampling with a common explicit error and coin/output budget.
For orientation, coherent-state trace distance is at most the Euclidean amplitude error.
A phase mesh with maximum angular error h changes the input amplitude vector by at most `sqrt(K nu)h`.
Also independent Poisson laws at rate vectors a,b have TV at most `sum_j |a_j-b_j|` by a coupling.
These facts identify usable continuity bounds, not a completed bit-complexity proof.
For rational B-bit eta, nu is O(B) when `1-eta >= 2^-B`; naive series taking time proportional to `1/(1-eta)` would still be insufficient.
Rational phase/log approximations, rate rounding, and the finite Poisson-total/multinomial categorical probabilities require separately specified precision and worst-case randomness caps.
No efficient exact Turing sampler is claimed by replacing these obligations with the phrase “sample a Poisson.”

## 6. Three authenticated primary comparisons

Checked 2026-11-26; exact arXiv versions below are the extraction identities, with published counterparts indicated.
No full PDF was retained, so no acquired-source content hash is asserted. The report hash seals only this report.

**S1 — Rahimi-Keshari, Ralph, Caves**, *Sufficient Conditions for Efficient Classical Simulation of Quantum Optics*.
[arXiv:1511.06526v2, 22 June 2016](https://arxiv.org/abs/1511.06526v2),
[primary text](https://arxiv.org/html/1511.06526v2), PRX 6, 021039, DOI 10.1103/PhysRevX.6.021039.
Extracted §II.1, equations (2)–(4), and §III.1, (23)–(27): positive coherent mixtures propagate by a lossy linear transfer matrix.
Dictionary: their row-vector L convention is transposed to our column-vector T convention.
This establishes the classical-process ingredient after notation translation, subject to sampleable distributions.
Their §III.2 single-photon example uses on-off detectors and random-count noise, not the exact approximation (4).
Overlap: **known after translation of notation** for coherent propagation; **partial or adjacent result only** for this error bound.

**S2 — Oszmaniec, Brod**, *Classical simulation of photonic linear optics with lost particles*.
[arXiv:1801.06166v1, 18 January 2018](https://arxiv.org/abs/1801.06166v1),
[primary text](https://arxiv.org/html/1801.06166v1), NJP 20, 092002, DOI 10.1088/1367-2630/aadfa8.
§IV.1, (22)–(24), constructs phase-averaged particle-separable fixed-l approximants.
§IV.2, (25)–(29), mixes these with binomial weights; Lemma 1 gives `Delta <= n eta²/2 + eta(1-eta)/2`.
Here n=K and eta has the same intensity-transmission meaning.
The locator for that uniform-loss bound is Lemma 1, not Corollary 1, which concerns fixed l.
Their approximant preserves the binomial photon-number sectors, unlike this product Poisson shell.
Overlap: **partial or adjacent result only** for the exact fixed-radius bound; the small-surviving-fraction simulation regime is established prior work.

**S3 — García-Patrón, Renema, Shchesnovich**, *Simulating boson sampling in lossy architectures*.
[arXiv:1712.10037v3, 24 July 2019](https://arxiv.org/abs/1712.10037v3),
[primary text](https://arxiv.org/html/1712.10037v3), [Quantum 3, 169](https://quantum-journal.org/papers/q-2019-08-05-169/).
§3.1, Theorem 2 and (8)–(9), replaces lossy CF input by product thermal states with error <=epsilon when transmission mu<=sqrt(epsilon/N).
Dictionary: N=K, mu=eta; their thermal parameter lambda may be set to mu and is not P128's nu.
§5, (18)–(19), (26), (38)–(43), supplies coherent constellations, matrix propagation, and approximate Poisson sampling.
§7 uses maximum singular intensity transmission and channel contraction for nonuniform losses.
Overlap: **known after translation of notation** for the spectral-loss/coherent-sampling framework; **partial or adjacent result only** for (4)'s fixed-radius exact error.
Their numerical approximation discussion does not, without a checked transfer, discharge §5's bit contract here.

## 7. Bounded attribution and next obligation

Existing P96/P98 prior records were consulted before the net; searches targeted coherent/thermal lossy-single-photon replacement and phase-randomized coherent approximation.
Authentication used official version metadata and the primary passages listed above; no exhaustive citation, language, or priority search occurred.
The exact shell formula was not extracted from these three sources. Its priority remains **UNVERIFIED**, not “new by absence.”
The strongest present result is the self-contained ideal-real bound (1), with disclosed surplus handling and classical resource costs.
A certified finite-bit sampler and an independent proof review are separate next obligations; no optimizer advantage, hardware calibration, or positive goal is established.
