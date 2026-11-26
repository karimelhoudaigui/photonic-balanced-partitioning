# P100 bounded primary-source attribution: reject-flip lifting

Checked 2026-11-26. **The stationary lifted-kernel machinery is known after
translation. Exact priority for P100's optical cubic/loss composition is
UNVERIFIED.** This is neither a positive optimizer signal nor an independent
correctness verdict on the P100 derivation.
Target research/P100_LIFTED_CHIRAL_PHOTONIC_CARD.md: 203 lines,
`f7d3ba94506fa9b462612e062bf1b1b7bed16cb6`, SHA256
`45586c2b6f243f7edc814775fbfd4546e0e1219b66d2dd7b9480c5b4489b56c6`.
The original card, including its preserved failed gauge subclaim, is unchanged.

## Scope, acquisition and checks

The literature-check/cache instructions were reused. Before new acquisition,
the local P66 and P99 source notes and read-only name/topic searches were
consulted. No matching retained lift record or literature/records cache was
found at root/this worktree. Discovery used five English queries: Turitsyn/
Chertkov/Vucelja skew balance and rejection flip; Diaconis/Holmes/Neal
direction reversal; quantum nonreversible inverse-unitary Metropolis;
bosonic nonreversible Monte Carlo; Layden real symmetric proposals.
Only the THREE publications below were substantively extracted. Historical
names in their citations are not claimed independently authenticated originals.
Selected primary equations/algorithm paragraphs were read in official or
author/institution-hosted full texts; no full-paper proof audit is claimed.
No PDF/text/cache was newly retained locally, so new retained-source SHA256
is NONE. Browser extraction is not local byte authentication. No broader
portfolio is folded into this note.

## S1: replicated skew-detailed-balance construction

Konstantin S. Turitsyn, Michael Chertkov and Marija Vucelja,
*Irreversible Monte Carlo algorithms for efficient sampling*,
Physica D240,410–414 (15-Feb-2011), DOI10.1016/j.physd.2010.10.003.
[Published author-hosted PDF](https://www.mit.edu/~turitsyn/assets/pubs/Turitsyn2011ik.pdf),
section4, pp.411–412, equations(2)–(4), describes two replicas and opposite
within-replica kernels satisfying skew detailed balance. Inter-replica
switching balances their different outgoing probability masses; diagonal
terms enforce stochasticity. Their concrete spin algorithm keeps direction
on accepted moves, with a separately chosen conditional switch on rejection.
It does NOT require that every rejection flip the replica.

Dictionary: their column-transition convention transposes P100's row kernels;
their replicated target is P100's pi(x)/2. This verifies the established
stationarity construction and distinguishes choosing a switching rate from
proving a speedup. Their mean-field spin demonstration is not a theorem for
arbitrary graph optimizers or passive Fock circuits. Overlap: known after
translation for the construction; partial or adjacent for the optical route.
The related arXiv:0809.0916v2 is dated23-Sep-2008; the equation locators here
refer to the 2011 published PDF, not an assumed identical preprint layout.

## S2: exact general kernel, maximal flips and existing comparison theorem

Christophe Andrieu and Samuel Livingstone, *Peskun–Tierney ordering for
Markovian Monte Carlo: Beyond the reversible scenario*, Ann. Statist.49(4),
1958–1981 (2021), DOI10.1214/20-AOS2008.
[Published institutional PDF](https://discovery.ucl.ac.uk/id/eprint/10108137/1/Livingstone_20-AOS2008.pdf),
Section3.3, pp.1967–1968, equations(5)–(7), Algorithm3: paired sub-Markov
T_sigma obey pi(dx)T_+(x,dy)=pi(dy)T_-(y,dx). Writing a_sigma=T_sigma 1,
admissible switches satisfy 0<=rho_sigma<=1-a_sigma and
rho_sigma-rho_-sigma=a_-sigma-a_sigma. Set T_sigma=R_sigma off diagonal,
zero on diagonal. P100 uses the known endpoint rho_max=1-a_sigma.
Theorem6 orders sign-invariant lambda-asymptotic variances, 0<=lambda<1:
rho_min=max(0,a_-sigma-a_sigma) is best, rho_max worst for fixed T.
Theorem7 compares against the reversible average of the SAME T, not D.
Remark9 warns that computing integrated accepted masses can obstruct
implementation. Overlap: known after translation for the stationary lift.

## S3: quantum-generated proposals and the missing nonsymmetric correction

David Layden, Guglielmo Mazzola, Ryan V. Mishmash, Mario Motta, Pawel Wocjan,
Jin-Sung Kim and Sarah Sheldon, *Quantum-enhanced Markov chain Monte Carlo*.
Exact extraction: [arXiv:2203.12497v1](https://arxiv.org/html/2203.12497v1),
23-Mar-2022, main equations(2)–(7),
[PDF supplement](https://arxiv.org/pdf/2203.12497v1), sectionV.C,
equations(S40)–(S42). The later
[Nature619,282–287 version](https://www.nature.com/articles/s41586-023-06095-4)
was published12-Jul-2023, DOI10.1038/s41586-023-06095-4; no identity of all
preprint/journal bytes or equation locators is assumed.

The quantum-to-classical proposal/acceptance loop is established. They choose
REAL SYMMETRIC H so U=U^T and the measured proposal is symmetric, allowing
ordinary cost-only Metropolis without evaluating its probabilities. Generic
Hermitian H is not sufficient for that symmetry. This verifies a boundary
important for P100, not a proof of its complex-H inverse-sign correction.
Their qubit Ising evolution is not passive photonic Fock evolution; P100
still needs its own raw CF reciprocity, decoder and loss argument. No
rejection-flip bosonic construction or cubic formula was extracted from S3.
Overlap: partial or adjacent result only for the exact optical mechanism.

## Disposition of P100's arrows

| Arrow | Bounded disposition |
|---|---|
| Off-diagonal skew balance plus replica switches gives pi/2 | Known after translation, S1/S2 |
| Move keeps sigma, every nonmove flips | Known endpoint rho_max, S2 |
| Quantum proposal permits cost-only acceptance | Known with the required symmetry in S3; P100 uses another proof |
| Complex passive U and U-dagger yield CF inverse-sign reciprocity | Internal P100 dictionary; exact external attribution unverified |
| Orientation-averaged cubic pair exchange and polynomial triad null | Exact combined source attribution unverified |
| eta^K waiting/next-jump formulas; ALL-failure-flip washout | P100 derivation; exact prior-source attribution unverified |

Changing P100's switching/holding rule is a separate design. These variance
comparisons do not order arbitrary-start finite-horizon hitting/best-of-T or
CPU/photonic latency. Source, compilation, accepted-rate evaluation, invalid
counts, scores and flips remain paid. Its washout is rule-specific, not an
intrinsic theorem about uniform loss under every observable-failure policy.

The bounded bosonic search did not authenticate an exact earlier optical
construction; it cannot establish absence or novelty. The inverse-unitary
bridge, all-output repair obstruction, pair-versus-higher-order distinction
and quantitative loss behavior remain separate internal proof obligations.
P100's cubic term already has its explicit classical null; stationarity
machinery supplies no positive gate. Priority and positive goal remain OPEN.
Only this note was written: no code/import/AST/scientific execution/RNG/native/
test/runner/QPU/graph/raw-data/manuscript/push or frozen-source edit occurred.
