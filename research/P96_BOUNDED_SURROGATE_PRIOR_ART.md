# P96 bounded attribution: two-moment positive loss surrogate

Checked2026-11-26. **Classical inversion and lossy-photon simulation have
established prior art; priority for P96's exact combined statement remains
UNVERIFIED.** No inspected source is claimed to state the complete positive
support<=2 law, exact TV identity and24e_3 bound under Tr(T-dagger T)<=1/2.
Failure to extract that statement is not evidence that it is new.

Target: research/P96_COLUMN_LOSS_CLASSICAL_SURROGATE.md, original
`6f4e7fb90e284a8e358c55886ddd2032d45811f9`, SHA256
`b378ebd6bb0bb6f981e9fe395938e3a43aec7775f761b81cda7b394f6dc1e94e`.
That169-line proof is unchanged. This is attribution, not another proof audit.

## Acquisition and bounded strategies

The literature-check/cache instructions were reused. Read-only stable-topic
checks found no .research-cache/literature/records in project or worktree.
Existing P42/P44 source records and P94's authenticated counting-characteristic
record were consulted before the network. StrategyA searched photon loss,
nonuniform simulation and two-photon moment approximation. StrategyB searched
factorial moments, Janossy/inclusion–exclusion, Bonferroni and low-density
realizability. Only primary arXiv versions/publisher records support this note.
Retained external PDF/hash:NONE; selected online HTML extraction is available,
with no local byte-authentication/full-PDF reading claim. No large download,
new cache/checkout, ledger or other artifact was created; disk was about1.2GiB
free. HTML rendering dates are not substituted for the arXiv revision dates.

## S1: inclusion–exclusion, moments and configuration probabilities

Tobias Kuna, Joel L. Lebowitz and Eugene R. Speer, *Realizability of point
processes*, arXiv:math-ph/0612075v2,20-Mar-2007,
[version](https://arxiv.org/abs/math-ph/0612075v2),
[primary text](https://arxiv.org/html/math-ph/0612075v2).
Section3 equation(3.19) gives the correlation-to-configuration inversion

    p_n^Lambda=sum_{r>=0}(-1)^r/r! integral_{Lambda^r}rho_{n+r}.

Sections1/3 explicitly use simple point configurations, with distinct positions;
the finite-set version has occupations0/1. Setting correlations above order2
to zero in this inversion yields the formal structure q2=rho2, q1=rho1-
integral rho2, q0=1-integral rho1+(1/2)integral rho2. This is a truncation of
the factorial-correlation hierarchy BEFORE inversion, not conditioning the
true law on N<=2. Nonnegativity remains a separate problem in the paper.

P96 uses count-valued modes, including double occupations: translating via
factorial measures (or distinct auxiliary marks) is necessary before merging
points back into modes. That translation supplies q(2e_j)=g_jj/2 and lists
j<l only once. Overlap:formal corollary not stated, not a verbatim bosonic
theorem. Theorem3.1's small-density realization has integrability/stability
conditions and a Kirkwood higher-correlation ansatz; it is not P96's trace
criterion. The exact TV=(N-1)^2-tail formula was not extracted from this source.

## S2: established fixed/uniform-loss approximate simulation

Michał Oszmaniec and Daniel J. Brod, *Classical simulation of photonic linear
optics with lost particles*, arXiv:1801.06166v1,18-Jan-2018;
New J. Phys.20,092002(2018), DOI10.1088/1367-2630/aadfa8.
[Version](https://arxiv.org/abs/1801.06166v1),
[primary text](https://arxiv.org/html/1801.06166v1).
SectionIV.1 Theorem1/equation(22) gives the closest particle-separable
approximation to the canonical l-survivor state, with trace distance
Delta_l,K=1-K!/[K^l(K-l)!]. Corollary2 transfers an upper bound to number
measurement after arbitrary passive optics. SectionII.3 equation(9) gives
uniform-loss binomial mixing; sectionIV.2 equations(25)–(29)/Lemma1 bound
the corresponding mixed-state error by eta^2 K/2+eta(1-eta)/2.

The efficient small-error regime is l=o(sqrt(K)), or eta K=o(sqrt(K)) for
uniform independent loss. These are known lossy-simulation obstructions.
They approximate by mixtures of separable states across survivor sectors,
not P96's correlated output law supported on0/1/2. P96 allows a general
occupied-column Gram matrix, not just C=eta I. Overlap:partial or adjacent
result only for the exact P96 construction, not a claim of disjoint regimes.
Only the stated upper bounds are used; no output-TV equality is imported.

## S3: nonuniform loss is already a classical-simulation subject

Daniel Jost Brod and Michał Oszmaniec, *Classical simulation of linear optics
subject to nonuniform losses*, arXiv:1906.06696v4,11-May-2020;
Quantum4,267(14-May-2020), DOI10.22331/q-2020-05-14-267.
[Version/text](https://arxiv.org/html/1906.06696v4),
[publisher](https://quantum-journal.org/papers/q-2020-05-14-267/).
Theorem1, section3/equation(3), constructively extracts input losses eta^s_i
using shortest input-output paths. Section6 Theorem4/equation(22) gives a
sampling-error bound when only O(log K) inputs have short paths and the
remaining effective transmissivity decreases sufficiently with K.
This is genuine nonuniform-loss prior art. Its geometric/channel conditions
are not the assertion that measured column norms alone equal independent
input transmissivities. It does not supply P96's displayed q/TV formula.
Authentication/extraction verified; overlap:partial or adjacent result only.

## Known counting ingredient and disposition of the exact arrows

The prior P94 check authenticated Seron–Novo–Arkhipov–Cerf,
[arXiv:2212.09643v2](https://arxiv.org/html/2212.09643v2),13-Sep-2024,
section2.1 equations(14)–(20): Fock counting characteristics are permanents
of occupied-input compressions of U-dagger Lambda U. Applied to a vacuum
dilation this is the standard generating-function ingredient behind P96's
per(I+(z-1)C); factorial differentiation is a formal finite-polynomial step.
This does not attribute the full surrogate or coefficient24 to that paper.

| P96 arrow | Bounded source disposition |
|---|---|
| Factorial moments -> order-two configuration masses | Known inversion; count/bunching translation required, S1 |
| Those masses are positive from mu<=1/2 | Internal P96 Gram/row bound; exact external attribution unverified |
| TV=E[(N-1)^2 1_{N>=3}] | General classical deficit identity in P96; exact prior-source attribution unverified |
| CF moments <=(r!)^2 e_r(c), then24e3<=4mu^3 | Standard Gram/permanent/factorial ingredients; exact combined attribution unverified |
| Strong losses permit approximate classical simulation | Established, S2/S3, under their own hypotheses |

No implication equates a mean device efficiency with a certified occupied-
column budget, or column bounds c_i<=eta with ||T||^2<=eta. The valid general
consequence is ||T||^2<=sum_i c_i; P96 still needs explicit T/phases and all
setup/sampling/decoder costs. Generic low mean alone does not make truncated
moment masses positive. P96's bosonic CF pair coefficients and correlated
loss treatment remain load-bearing, with all raw vacuum/collisions retained.

Search record: eleven English discovery queries across the two strategies,
including `Oszmaniec Brod ... lost particles nonuniform losses`, `Janossy second
factorial truncation`, `factorial moments at most two`, `Janossy Bonferroni
approximation`, and `total variation (N-1) boson loss`. Selected backward
references were followed at citation level; Ambartzumian–Sukiasian1991 was
not independently authenticated. Same-searcher second strategy, no exhaustive
forward citations/patents/non-English survey. No absence-to-novelty inference,
new science computation, import/test/RNG/native/runner/QPU/paper/push or
existing proof/source/contract/raw edit occurred. Global priority remains OPEN.
