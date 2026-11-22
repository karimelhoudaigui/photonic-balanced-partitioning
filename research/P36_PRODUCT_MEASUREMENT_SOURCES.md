Retained interrupted literature draft, not a final delivered audit. Source hashes and explicit dictionaries remain inspectable. Correction from the subsequent root cone argument: at complex k3, PSD effects with dominant diagonals DO admit dominant rank-one refinements; the draft paragraph calling this an enlarged domain is superseded for that case by theory/phase3_pinching_dual.md. The quantitative pinched bound remains OPEN.

Original SHA256: 269a7e353ecd0be9c2935c4051a3c056355b6779cc971242518d9f08db7a6576

# P36: product measurement, path discrimination and the missing linear step

Bounded source check, 2026-11-22, using `mathbox:literature-check`. The
existing isolated worktree is `.qwen/worktrees/late2026-loss-review`;
starting commit `498183230922b17a8f52df0907ce6de9603f103d`. Only this new
tracked report is changed. No spatial-Gram or Dittel audit is repeated.

**Result:** one checked primary theorem justifies the exact Naimark-pinching
reduction that preserves internal degrees of freedom. Two closely related
primary complementarity results do not supply the remaining coefficient-one
bound. Their strongest checked scalar coherence relation genuinely allows
square-root behavior, already for three paths. The requested product-state
inequality remains **UNVERIFIED by this source check**; neither its validity
nor its novelty follows from the searches below.

## Exact contract: common product POVM, first k=3

On H=C^k, let M={E_i} be a finite rank-one POVM, with E_i>=0 and sum_i E_i=I.
For a uniform random basis label a, the classical channel is
Pr(i|a)=(E_i)_aa. Fix one maximizing label g(i) for each outcome and put

    delta=sum_i[Tr(E_i)-max_a(E_i)_aa]
         =k-sum_i(E_i)_(g(i),g(i)).

The minimum error of inferring this label **from the fixed measurement's
classical outcome**, optimizing only its decision rule, is delta/k. It is
not automatically an optimal quantum detector-state discrimination error.

Let |pi> range over the k! permutations of |1,...,k>, and define

    |s>=(1/sqrt(k!))sum_pi |pi>,
    rho_sym=|s><s|,       rho_perm=(1/k!)sum_pi |pi><pi|.

The target is TV(M^(tensor k)(rho_sym),M^(tensor k)(rho_perm))<=delta,
with the **same M on every tensor factor**, all outcomes retained, and no
conditioning. Delta>=1 is trivial. At k=3 the coherent subspace has six
permutation basis vectors; it is not a single three-path state.

Both states have one-particle marginals I_k/k. Thus replacing the problem
by a one-particle coherence statement loses the correlation being tested.
Their common-product output laws are exchangeable: within every fiber of
ordered tuples having the same occupation counts, both probabilities are
constant. Consequently forgetting output order preserves their TV exactly.
This equality need not hold for unrelated measurements on different factors.

## H: exact structural source for the proposed pinching route

Teiko Heinosaari and Takayuki Miyadera, *Qualitative Noise-Disturbance
Relation for Quantum Measurements*,
[arXiv:1303.5530v2](https://arxiv.org/abs/1303.5530v2), 2014-01-07,
eight-page primary PDF, matching Phys. Rev. A 88, 042117 (2013).
Checked §IV, **Theorem 1**, PDF pp. 3–4, equations **(4)–(6)** and proof.

The source permits finite or countable POVMs on a finite or separable input
space. For a Naimark dilation (K,Ahat,W) of A, its least-disturbing channel
is, in the source's Heisenberg convention,

    Lambda_A(C)=sum_g W† Ahat_g C Ahat_g W.

Every A-compatible channel is a postprocessing of this channel. The
Schrödinger-picture composition order is reversed from the source's
Heisenberg order. The chosen dilation need not be the minimal one.
**Authentication/extraction verified.** This is a structural ordering
theorem, not a quantitative upper bound in a calibration error.

### Dictionary and exact implication for our product measurement

Write E_i=|e_i><e_i| and define the isometry W:H->C^r by
W_ia=<e_i|a>, where r is the number of fine outcomes. Let

    P_g=sum_(i:g(i)=g) |i><i|,
    A_g=W†P_gW=sum_(i:g(i)=g)E_i,
    F(rho)=sum_g P_g W rho W† P_g.

The P_g are orthogonal projectors in the dilation, sum_g A_g=I, and
delta=k-sum_g(A_g)_gg. F is exactly the Schrödinger channel from H, with
all degrees of freedom inside each dominant-label block retained.

Let C measure the fine coordinate basis |i> in the dilation. Since every
|i> lies in its own assigned block,

    Tr[|i><i| F(rho)]=Tr[E_i rho],       M=C o F,
    M^(tensor k)=C^(tensor k) o F^(tensor k).

This explicit factorization verifies compatibility directly, as well as
matching H's theorem. It keeps the common product measurement; there is no
replacement by an arbitrary collective detector. Contractivity now gives

    TV(M^(tensor k)(rho_sym),M^(tensor k)(rho_perm))
       <= (1/2)||F^(tensor k)(rho_sym-rho_perm)||_1.

**Application verdict: verified, known after translation of notation** for
the least-disturbing construction; the displayed product bound is a
**formal corollary not stated**. H supplies no bound by delta for this pair.
Its additional quantitative Theorem 3 concerns worst-case decoding
disturbance, in a different direction and metric, so is not adopted here.

### The k=3 finite residual question

The physics route's block reduction can be expressed entirely in A_g. For
r=(r_1,r_2,r_3) in {1,2,3}^3, define the six-by-six Gram matrix

    G_r(pi,tau)=prod_(j=1..3) (A_(r_j))_(pi(j),tau(j)).

Indeed its vectors are tensor_j P_(r_j)W|pi(j)>. The corresponding block
of F^(tensor 3)(rho_sym-rho_perm) is T_r(J_6-I_6)T_r†/6. Polar
decomposition of T_r therefore gives

    D_pinched=(1/12)sum_r
       ||sqrt(G_r)(J_6-I_6)sqrt(G_r)||_1.

Here J_6 is the all-ones matrix. H authenticates the preceding channel
reduction, not the proposed quantitative lemma D_pinched<=delta.
The matrices A_g also come from a finer dominant-label rank-one
decomposition; replacing them by arbitrary PSD effects satisfying only a
diagonal calibration inequality enlarges the domain.

Moreover D_pinched is the distinguishability available to a possibly
**collective** final measurement of the retained quantum blocks. Therefore
D_pinched<=delta would be a sufficient, potentially stronger lemma. Finding
D_pinched>delta would refute that lemma but would not by itself refute P36:
the optimal block Helstrom test might not be realizable by the required
common product measurement. No numerical case is promoted to a theorem here.

## B1: minimum-error path information versus l1 coherence

Emilio Bagan, János A. Bergou, Seth S. Cottrell and Mark Hillery,
*Relations between coherence and path information*,
[arXiv:1509.04592v2](https://arxiv.org/abs/1509.04592v2), 2015-12-10,
five-page primary PDF; Phys. Rev. Lett. 116, 160406 (2016).
Checked **(3), (5)–(9)**, PDF p. 2, and proof on p. 3.

For a d-path particle controlled-coupled to initially pure detectors,

    |Psi>=sum_a sqrt(p_a)|a>|eta_a>,
    sigma_ab=sqrt(p_a p_b)<eta_b|eta_a>,
    X=C_l1(sigma)/d,

the source proves

    (P_s-1/d)²+X² <=(1-1/d)².

P_s optimizes the measurement discriminating the **detector states** with
priors p_a. The allowed priors need not be uniform. **Verified extraction**;
**partial or adjacent result only** for P36.

Even if one had a matching detector model whose optimal error were
e=1-P_s, the conclusion would only be

    X²<=2(1-1/d)e-e².

There is no identification here of X with the product-measurement TV, or
of this detector ensemble's e with delta/k. In particular, setting
|eta_a>=W|a> would give orthogonal detectors and P_s=1 for every POVM,
because W†W=I. It would not reproduce the fixed-coordinate MAP error.
Conversely, the diagonal classical record states with entries (E_i)_aa
do reproduce delta/k as optimal discrimination error, but are mixed and
do not identify the required coherent detector dilation or its output law.
One cannot silently exchange these models.

## B2: the sharper operational relation still allows square-root behavior

Emilio Bagan, John Calsamiglia, János A. Bergou and Mark Hillery,
*Duality games and operational duality relations*,
[arXiv:1708.03968v1](https://arxiv.org/abs/1708.03968v1), 2017-08-13,
eight-page primary PDF; Phys. Rev. Lett. 120, 050402 (2018).
Checked state model **(3)–(5)**, **Lemma 1, (9)**, pp. 2–3, and the
symmetric ensemble success formula **(12)**, p. 4. Its proof is in the
supplement, ending with **(69)**, p. 8.

The model permits a general particle density matrix sigma, coupled without
changing path populations to pure detector states. P_d is optimal detector
discrimination with priors sigma_aa; X is normalized l1 coherence after
tracing out those detectors. Lemma 1 proves the tight bound

    X <= (d-2)e/d+(2/d)sqrt[(d-1)e(1-e)],
    e=1-P_d.

**Verified extraction**, **partial or adjacent result only** for P36.
The phase game permits unrestricted phase-discrimination measurements;
it does not impose the common tensor-product POVM and permutation inputs.

At d=3 the bound is X<=e/3+(2/3)sqrt[2e(1-e)]. The source identifies a
saturating family: uniform coherent particle input and detector states
with a common real pair overlap s in [0,1]. Then

    X=2s/3,
    P_d=[sqrt(1+2s)+2sqrt(1-s)]²/9,
    e=s²/2+O(s³) as s->0.

The last expansion is an elementary translation of (12). It gives
X/e->infinity. Thus no universal estimate X<=constant*e is available for
these scalar source quantities, even at three paths. This refutes that
shortcut, **not** the product-measurement claim P36.

Calling Theorem 1 of B2 a “linear duality relation” does not change this:
its combined-game bound is (P_phase+P_way)/2<=1/2+1/(2sqrt(d)), with a
nonzero finite-d offset. It is not P_phase-1/d<=1-P_way. The tighter
finite-d region above retains its square-root edge.

## Exact implication status and remaining bottleneck

| Arrow | Verdict | Missing bridge |
|---|---|---|
| Fixed basis-label inference error equals delta/k | Verified classical identity | No quantum detector ensemble is implied. |
| Fine M factors through the grouped, internal-state-preserving Naimark channel | Verified; H plus explicit dictionary | No quantitative delta estimate in H. |
| Common product M on the permutation states is bounded by D_pinched | Verified contractivity corollary | The trace-norm bound can be strictly stronger than the measured question. |
| B1/B2 coherence-path discrimination relation implies P36 | Unverified; the naive scalar-linear substitution is invalid | Need the exact correlated permutation states, product restriction and calibrated error in the same model. |
| D_pinched<=delta at k=3 on the actual dominant-refinement domain | Unverified | No checked source supplies this quantitative inequality. |

Neither d=3 single-particle paths nor d=6 permutation paths may be
substituted without a dictionary. The former has already discarded the
permutation correlations; the latter changes the allowed measurement and
does not identify its six-way discrimination error with delta/3. A generic
square-root information-disturbance or diamond-norm estimate does not fill
these gaps. This review supplies a known exact reduction and a verified
non-implication of the scalar shortcut, not an attribution or proof of the
coefficient-one product inequality.

## Artifacts and bounded coverage

Exact cached primary artifacts in this worktree:

| Source | PDF SHA256 | Extracted-text SHA256 |
|---|---|---|
| H, [1303.5530v2 PDF](https://arxiv.org/pdf/1303.5530v2) | `238bd8841d1641c00be2db060f96970327ee3551c3d3266cf986910ecadfeeb6` | `71d7ed481ebd576ee1eed4c0c9d12aa9a6f4b733be7d01dd90e49232e7358bc5` |
| B1, [1509.04592v2 PDF](https://arxiv.org/pdf/1509.04592v2) | `63aacd0c8858e75ede34d4cb3db60922209c851dadabb29cd18430d62ab4d698` | `03a8c3ec6774bd08c729033324a96ef74e2404d2059626810fe8c7b18319356e` |
| B2, [1708.03968v1 PDF](https://arxiv.org/pdf/1708.03968v1) | `74d18b1d9fe447319aa88b5b348b4cbf56d96ea5f35483b0038dde2f16dc703e` | `b72239b57955f7057482fe151259c2bebac0f69a53fedca4f073d79166993fa1` |

The ignored directories `.local/references/p36_heinosaari_1303.5530v2/`,
`.local/references/p36_bagan_1509.04592v2/` and
`.local/references/p36_bagan_1708.03968v1/` each retain a PDF, pypdf 6.4.0
text extraction and source metadata JSON. These are not part of the Git
commit. PDF theorem numbering is used: HTML conversions can renumber
equations inside the source proofs.

This was a focused check of three nearby primary results, following the
path/coherence and least-disturbing-instrument citation chains. Search
queries included `coherence path information minimum-error`,
`Duality games operational duality relations`,
`least disturbing channel Naimark theorem`,
`product measurement permutations coherence distinguishability` and
`measurement basis calibration error coherence rank-one`. Unrelated hits,
missing hits and abstracts were not theorem evidence. The physics reviewer
shared the current pinching route; this was not a blind independent audit
of that route, nor an exhaustive review of its conjectured finite inequality.
No numerical search, QPU or manuscript work was performed. Global novelty
and the general validity of P36 remain unresolved.
