# P62 focused independent proof audit

**Primary verdict: proved as written.** For feasible cardinalities on a
finite weighted graph, the stated fixed-uniform-embedding/local-control
experiment is stochastically dominated in best-of-T cost by T independent
classical frontiers, with up to2^s paid candidate scores per trial. This is
not equal wall-time or a particular-fixed-embedding guarantee.

Exact audited commit: `aff6ceaa642752d72cbf6ab08251852bf22f1176`.
File: `theory/P62_random_embedding_local_control_obstruction.md`.
SHA256: `138b8a79511ef127480cd23f4a8275e663039b644ab6068daf23a07d4559dd37`.
The complete135-line raw proof was read. No author file was modified.
No computation, code, import, source/graph draw or numerical test occurred.

## Normalized claim and dependencies

Fix G, integer0<=k<=N, active physical set A of size s, a uniform bijection
Pi independent of G drawn ONCE, and fixed integer T>=1. Every fresh shot's
outside joint count law is the SAME nu conditional on Pi and ENTIRE history;
nu is independent of graph, embedding, selected parameters and history.
Tie priorities are fresh and independent, implementing uniform threshold
ties. The reported optical candidates are only topk decoded outputs. A
common graph-only incumbent independent of Pi may be granted to both.
Arbitrary Pi-dependent frontend candidates are explicitly excluded.

The classical trial draws uniform active labels and an ordered complement,
scores every feasible active-subset/complement-prefix completion and returns
the best. For all real c its T-trial best fails the threshold no more often
than the quantum best, including the quantum run's ONCE-drawn Pi.

Dependency chain, all INTERNAL elementary arguments:

1. Uniform-tie ranking implies frontier containment.
2. The conditional outside-law hypothesis implies iid frontier contexts
   GIVEN Pi, despite adaptive/non-iid quantum decoded outputs.
3. Independence of Pi and outside contexts allows uniform-embedding image
   averaging to equal the purely classical one-frontier law.
4. Convexity of x^T yields the mapping-averaged T-shot bound.
5. Graph-cut quadratic deltas yield the paid2s-core work bound.
6. The stated P61 circuit's relative unitary has active support{1,7,13}.

No external theorem, hidden computational range or source calibration is a
load-bearing leaf. The local-channel-to-outside-law statement follows from
partial trace and a trace-preserving operation on A. Conditioning on a
selected channel outcome would change that argument and is excluded.

## Obligation matrix and decisive checks

| Obligation | Finding |
| --- | --- |
| Exact quantifiers / fixed Pi | Passed: Pi is drawn once; only the classical comparator refreshes its frontier roles |
| Adaptive history | Passed: entire-past conditional nu, not unconditional iid output, is the hypothesis used |
| Uniform ties | Passed: a fresh iid uniform continuous-priority representation exists for the stated decoder |
| Frontier containment | Passed: every chosen inactive subset is an ordered prefix of length k minus active count |
| One-shot embedding average | Passed: Pi independent of nu permits reversing the integration/order of choices |
| Fixed-P correlations / Jensen | Passed: E[f_Pi^T] >= (E f_Pi)^T, never substituted by equality |
| Frontend candidates | Passed: graph-only/Pi-independent common data allowed; arbitrary Pi-dependent additions excluded |
| Work / score accounting | Passed in the arithmetic model; no equal-score-count or wall-time assertion |
| Relabeling versus new embedding | Passed and explicitly distinguished |
| P61 locality | Passed by the exact conjugation calculation below |
| Hardware / advantage / novelty | Out of scope; no such conclusion asserted |

Fixing inactive counts/priorities fixes their order rho. A topk selection
choosing active subset T must take the first k-|T| inactive modes. Thus a
bad frontier forces a bad decoded cut regardless of the policy's access to
G,Pi,earlier scores or active/outside correlations. Given Pi, fresh contexts
have constant conditional bad probability f_Pi(c). Their T-fold bad event
has probability f_Pi(c)^T and is contained in the T-fold quantum bad event.
The actual quantum costs need not be independent.

For ANY physical inactive order rho, uniform Pi maps its ordered active
list and rho to a uniform vertex ordering. Since nu and priorities do not
depend on Pi, E_Pi f_Pi is exactly the classical one-trial failure. For
T>=1, x^T is convex on[0,1], including the linear T1 boundary. Therefore
quantum failure >= E f_Pi^T >= (E f_Pi)^T = classical failure. The inequality
direction is correct for lower-cost best-of-shot comparison.

The independent reconstruction f301920 used success variables r=1-f; these
are equivalent formulas, not a different hypothesis about the latent Pi.
The fresh-priority assumption is separate from the fixed physical mapping.
All-zero counts and arbitrary threshold ties are covered. At k0 or kN
there is just one feasible candidate. At s0 there is one classical uniform
k-subset per trial. At sN all feasible k-subsets can be scored; efficiency
is no longer promised. No boundary case reverses the stochastic inequality.

## Arithmetic cost bound

For any feasible k, the inactive prefix lengths range from
max(0,k-s) to min(k,N-s). This interval has width at most s, so the variable
core has at most s active plus s inactive boundary vertices, EVEN when
k<s or k>N-s. A base feasible cut costs O(E); make a vertex-to-core index
array/order in O(N). Compute each core vertex's external field by adjacency
scans. Their total visited incidences sum to at most2E, not O(Ns) additional
work when adjacency lists are available.

For base membership x and change d supported in that core,

    C(x+d)-C(x)=sum_i d_i ell_i
                 -2 sum_(i<j in core) w_ij d_i d_j,
    ell_i=sum_j w_ij(1-2x_j).

Each candidate costs O(s^2) from those paid fields/core weights. At most2^s
candidates therefore give O(E+N+s^2*2^s) arithmetic work, including one base
score. Graph loading/storage, random bits, number bit lengths and actual
implementation constants are separate costs; the proof does not hide them
in a universal measured-time dominance statement.

## P61 application and interpretation limits

With L=V(F3 tensor I6) and t=(b1,i1),

    U(phi)U(0)*=L D(phi)L*=I+(exp(i phi)-1)vv*,
    v=L|t>, support(v)={1,7,13}.

V mixes only color0 ports0,6 and hence leaves v unchanged. The local
operation therefore preserves the entire outside joint reduced law, not
only intensities or moments. Fresh copies of the fixed graph-blind source
and a genuinely independent uniform physical map satisfy P62's premise.
This gives the eight-score frontier envelope for P61, without assuming its
outside quantum law is efficiently samplable.

A favorable fixed physical map is not covered pointwise; an explicit full-CF
HOM counterexample is preserved in f301920. Relabeling G while carrying the
same physical map checks equivariance but does not supply fresh embeddings.
Deterministic finite seeds or selected mappings must not be called an
average over all uniform embeddings. No same-wall-time, same-number-of-
scores or all-photonic impossibility is inferred. Changing active support,
source, mapping or decoder can change a premise and needs a new proof.

## Provenance and remaining obligation

The independent derivation was frozen in
`f301920946a5e90fda7c1b03d0c8ecd013342dcc` BEFORE reading this author proof;
its file SHA256 is083bb2b424b2b664250d9d364483eead8da5112989bab0db2288dc4fdb313ab8.
ROOT proposed the hypothesis and conclusion, and broad context is shared:
this is an independent same-team mathematical reconstruction/audit, not an
external blind assessment. Actual commands were read-only git show/hash and
skill/text inspection, followed by this isolated receipt write/commit.

No gap remains in the exact P62 statement. A P61 optimizer pilot is not the
next proof check. For a changed P63 device, first check active support and
the fixed outside-law/embedding assumptions; larger support alone does not
establish a useful mean channel or an advantage. ROOT controls any status
integration and future execution authorization separately.
