# P71 exact-hash independent author-proof review

Primary verdict: **proved as written**, under the source's stated physical
model and common-classical-postprocessing condition. The complete-law
constant is K, and the adaptive transcript comparison and its weaker
marginal E_U bound are valid with the common history schema described
below. No mathematical correction to the current source is requested.

## Exact revision, scope and independence

Reviewed all 301 lines of ROOT's
`research/P71_approximate_cross_rank_transport.md` at commit
`b2f84ccb7383331605e128351c927e66ae0d84cf`, SHA256
`c320f925b53f68738931da93ef28bb0a2f84f887988404153f974dae8b6cfe03`.
Coverage includes every section, endpoint, displayed formula, transcript
claim and final limitation. The displayed P69 constants were compared
with the pinned dependency SHA256
`37e59633734c16277ed2649c4761fa84a86a8006b164fd4263963e37d7759de4`.

Before reading that P71 source, the reviewer froze an independent
348-line derivation in commit
`5a1ff715759bbbfdd50cfb75c0aae3f7db6c0628`, file
`theory/P71_independent_effective_rank.md`, SHA256
`33ccc65cf779f76cbb57da787522267dbc0379d8e96555f6ca50ac0569256dc8`.
Its hash was checked unchanged for this review. The comparison is not
blind because the author's verdict was visible on opening the source;
neither that verdict nor ROOT's prior reading is a mathematical premise.
The transcript extension was checked directly below, rather than inferred
from agreement with the earlier pointwise proof.

Authored 2026-11-25 in `.local/p66-dark-barrier`, starting at the independent
P71 checkpoint. Only this new review file is written. The proof-audit and
mathematical-proofreading workflows were applied. No other proof was
edited, and no scientific import, test, numerical computation, graph,
random seed/draw, experiment, backend or QPU call was used. No external
CS theorem or novelty conclusion is assumed.

## Normalized claim and dependency graph

The physical space has two blocks of dimension d=2L, L>=2. The source
has K=2L photons, with L distinct occupied vertex modes per block. Targets
are the two full-CF one-block occupations. All probabilities are raw and
include collision outcomes in the complete normalized PNR law. U is the
entire unitary after source preparation, including coherent rerouting,
relative to these same physical blocks and decoder labels.

For 0<=r<=d, truncating its cross singular values after the first r gives
a unitary V of cross rank at most r and distance at most

    delta(s_(r+1))=sqrt(2-2sqrt(1-s_(r+1)^2))
                    <=sqrt(2)*s_(r+1),

with the explicit convention s_(d+1)=0 and V=U at r=d. The pointwise
claim then follows from

    explicit CS construction -> unitary truncation and norm delta
    tensor telescoping -> K times the one-particle error
    pure trace distance -> full PNR TV with the same K coefficient
    exact P69 target bound for V -> additive target bound for U.

The graph gap and predictable acceptance rule give the direct first-exit
consequences. Sequential coupling gives a separate transcript-law
consequence; it does not require the graph barrier or a common dark
projector. Each dependency is either explicitly proved in the source,
the previously verified exact P69 bound, or a stated model convention.

## Critical finite-dimensional checks

### Completed CS bases and singular-value ordering

The source writes U=[A C;D B]. Diagonalizing D^dagger D gives an input
CA basis v_i, sorted eigenvalues s_i^2 in [0,1], and c_i=sqrt(1-s_i^2).
The identities A^dagger A=I-D^dagger D and the orthogonality of v_i prove
that Av_i/c_i, where defined, are orthonormal. The analogous statement
holds for Dv_i/s_i. Each missing vector occurs only at a zero coefficient;
arbitrary orthonormal completion therefore preserves every asserted image.

For the completed a_i,b_i bases, alpha_i=(c_i a_i,s_i b_i) and
z_i=(-s_i a_i,c_i b_i) form orthonormal complementary families. Since
alpha_i=U(v_i,0), U^dagger z_i has zero CA component and defines a full
input-CB basis w_i. This proves the two-by-two rotation decomposition and
Cw_i=-s_i a_i, Dv_i=s_i b_i. Both cross singular-value multisets are
therefore exactly the same, not merely equal in rank.

At s_i=0, the images are (a_i,0) and (0,b_i); at s_i=1 they are
(0,b_i) and (-a_i,0). No undefined quotient remains at either endpoint.
Repeated singular values may be assigned any completed paired basis and
then sorted; splitting a repeated value at the cutoff does not change
the maximum discarded norm. Both source proof and prior independent
proof establish this without assuming a generic nondegenerate matrix.

### Truncation, exact delta and rank endpoints

The discarded channels become identity rotations, retaining unitarity.
Their difference blocks have adjoint-square 2(1-c_i)I, hence norm
delta(s_i). The direct-sum norm is the maximum, namely delta(s_(r+1))
for r<d. Rationalization gives

    delta(s)^2=2s^2/(1+sqrt(1-s^2))<=2s^2.

The statement is valid at zero by direct evaluation and at one with
delta(1)=sqrt(2). At r=0 the comparator is block-local; at r=d it is
exactly U. If the original cross rank is already at most r, all discarded
channels are identities and V=U. No optimal approximation or efficient
physical realization of V is needed to apply the universal P69 bound.

### Fock normalization, trace and complete-law TV

Tensor telescoping has exactly K terms, each with a single U-V and
unitary factors elsewhere. Its norm bound restricts to the symmetric
K-photon subspace without amplification. The normalized CF input in this
subspace carries no extra K! factor. Thus the two output vectors phi,chi
obey ||phi-chi||<=K||U-V||op.

For their pure density operators, the difference on their at-most-two-
dimensional span has opposite nonzero eigenvalues
sqrt(1-|<phi,chi>|^2). The linearly dependent case has trace distance
zero. The half-trace-norm convention therefore gives

    Dtrace=sqrt(1-|z|^2)<=||phi-chi||,
    ||phi-chi||^2-(1-|z|^2)=|1-z|^2>=0,
    z=<phi,chi>.

For a PNR event projector E, its expectation on the trace-zero density
difference is at most the trace of the positive part, Dtrace. Choosing
the event where P_U exceeds P_V gives the half-sum TV norm. Hence
TV<=min(1,K||U-V||op): there is no missing factor two or further half
to attach to K. The law includes every occupation of total photon number
K, including collisions.

A global one-particle phase gives Gamma_K(U) a global K-fold phase and
leaves probabilities unchanged. It can make the operator bound loose;
it does not invalidate it. Nothing here asserts phase-optimized distance,
a tight universal K constant, or an achieved probability.

The source's p_Lr, rising-factorial source factor and target factor match
the pinned P69 formula, including p_L0=0 and the r>=L trivial target
factor. At r=d, p_Ld=1 is correctly reported as uninformative. The same
two CF events must be used under U and V. Shared classical processing
contracts TV but cannot silently give P69's target estimate to a changed
decoder, collision repair event or conditionally normalized CF law.

## Predictable transcript comparison: explicit verification

### Measurable comparison choice

The source requires a consistent measurable basis selection. Such a choice
exists on the finite-dimensional unitary group, without requiring global
continuity. Ordered Hermitian eigenvalues are continuous: their min-max
Rayleigh-quotient characterization changes by at most the operator-norm
perturbation. That characterization itself follows by using the top-k
eigenspace for equality and intersecting any k-dimensional space with the
orthogonal complement of the first k-1 eigenvectors for the reverse bound.
Partitioning by their multiplicity pattern, each distinct-eigenvalue spectral projector
is a polynomial in D^dagger D with denominators that are nonzero on that
pattern. These projectors are consequently Borel measurable. Within each
range, project the coordinate basis vectors and use the first nonzero
residual as each Gram-Schmidt pivot. Nonzero tests and normalization are
Borel on the corresponding finite branches. The same coordinate method
completes the missing a_i,b_i at endpoints. Multiplication by U^dagger
then gives measurable w_i and hence a measurable V(U).

Degeneracies and endpoint jumps may cause discontinuity, which is harmless
for this claim. The underlying controller choices must be measurable and
made before the new optical output, as stated. This supplies well-defined
comparison kernels rather than a nonmeasurable pointwise selection.

### What the shared transcript contains

The source explicitly imposes the SAME classical postprocessing rule.
Mathematically this is a common kernel F(h,n) applied to a common history
schema h and the next raw outcome n, including shared conditional control
randomization. It can record arbitrary common reference control choices,
past outcomes, acceptance coins and classical states. Conditional on a
matched h, the prepared source is identical in both processes, so section
4's law bound applies even if that source is outside the bad-state set.

This does not assert closeness of logs with an extra field recording the
different actually applied matrix U_j(h) versus V_j(h), different backend
timings, or other operation-specific diagnostics. Those would not be the
common kernel F(h,n). Comparing such logs can have TV one even when the
count laws are arbitrarily close. This is the scope of the existing
common-postprocessing hypothesis, not a change to the source statement.

### Coupling and the marginal E_U bound

For finite PNR outcome probabilities p_n(h),q_n(h), an explicit measurable
maximal coupling uses common masses m_n=min(p_n,q_n). With probability
a=sum_n m_n, draw the same outcome from m/a. Otherwise draw from the two
residual distributions; their supports are disjoint, so these outcomes
differ. At a=0 or a=1 the unused normalized branch is unnecessary. This
has the correct marginals and mismatch probability 1-a=TV. The formulas
are measurable in h. The common control kernel can be sampled identically
first, and common classical processing identically afterwards.

Apply this coupling at each still-matched history. After its first mismatch,
propagate each marginal with its own correct kernel. Let M_(j-1) be the
event of no earlier mismatch and H^U_(j-1) the U-history marginal. If
the conditional law difference is at most e_j(h), then

    P(first mismatch at j)
       <= E[1_{M_(j-1)} e_j(H^U_(j-1))]
       <= E_U[e_j(H_(j-1))].

The first indicator need not be a function of U-history alone; its value
in the coupling is at most one. Dropping it and using the correct U
marginal proves the source's weaker E_U bound. Thus

    TV(transcript_U,transcript_V)
       <=min(1,sum_j E_U[e_j(H_(j-1))]).

For deterministic e_j envelopes, conditional survival at step j is at
least 1-e_j after any earlier matched history. Induction gives the sharper
1-product_j(1-e_j) bound. No independence of optical outputs, controllers
or mismatch events is assumed. For history-random tail envelopes the
expectations are essential; a realized random sum is not an unconditional
numerical upper bound. This verifies both transcript claims in the source.

## Graph first exit, temperatures and error regimes

The separate direct argument uses the P66 graph classification. A partial
clique cuts at least M(L-1), and exactly one partial clique is impossible
for a balanced 2L subset. Connected cross edges add at least 2wL^2, while
bad states cost 2Lh+2wL^2 and targets cost 4wL^2. For M(L-1)>Lh and
0<w<h/L, or w=0 in the disconnected case, only the targets improve on
the four bad states; every feasible state outside those six is uphill
by at least g=2M(L-1)-2Lh. Other bad states tie, as the source specifies.

At each still-bad history, the pointwise good-event hazard is at most
p_Lr+e_j, where e_j=min(1,sqrt(2)K eta_j). At zero temperature this
immediately gives the stated finite-T bound. At finite beta_j, before
the first accepted exit every other accepted exit has increase at least
g and acceptance at most exp(-beta_j g) under the declared Metropolis
convention. The indicator-weighted E_U formula in source section 6 is
therefore valid, including arbitrary predictable eta_j,beta_j. It is a
direct first-exit estimate and does not require a successful transcript
coupling or independent attempts. Zero contributions after adapted
stopping give the stated stopped version.

Polynomial tails do not automatically preserve an exponential hazard
certificate. For T=L^a and K=2L, the additive term has scale T K eta_L;
eta_L=o(L^(-a-1)) makes that term vanish but can leave only a polynomial
bound. An exponential expected-attempt conclusion does not follow from
that finite-horizon statement. The source's requirement that the full
additive hazard bound itself be exponentially small is correctly read
as a requirement of this certificate, not a necessary condition for the
actual physical probability to be exponentially small by some other
mechanism. Its final discussion explicitly avoids that overclaim.

Algebraic full rank of exp(itH) is likewise not an automatic performance
escape. P71 needs a quantitative singular-tail bound, and no actual
circuit/device tail is certified here. No inference about positive
optimization, typical starts, measured budgets, hardware readiness or
novelty is justified by this static comparison.

## Obligation matrix and closure

| Obligation | Review result |
|---|---|
| Exact source hash, complete coverage and prior independent freeze | Passed |
| CS completed bases, ordering, degeneracies, s=0 and s=1 | Passed |
| Unitary truncation, exact delta, sqrt(2), r=0 and r=d | Passed |
| K-fold symmetric lift, trace/Euclidean constants and global phases | Passed |
| Full PNR TV and fixed event/decoder | Passed |
| P69 constants and mathematical-only comparator V | Passed |
| Measurable spectral and endpoint choices | Passed by explicit Borel selection |
| Predictable common-history transcript coupling | Passed with the stated common kernel |
| Product survival and marginal E_U mismatch estimate | Passed; no independence required |
| B/G/outside classification and finite beta | Passed under declared acceptance |
| Polynomial versus exponential tail scope | Passed; additive limitation preserved |
| Actual-matrix or timing audit logs, changed source or physical filters | Outside the common transcript/model hypotheses |
| Numerical tail certificate, optimizer benefit and novelty | Not established |

There is no remaining mathematical gap in the normalized claim under its
stated common-kernel/model hypotheses. No source correction or executable
validation is required for this proof-only audit. Any later application
must separately establish its actual conditional singular-tail bounds and
retain all collision, source and resource accounting.

Text reads and SHA256 checks established artifact identity; Git whitespace
checks accompany this review's commit. The full review received final
mathematical proofreading for block conventions, spectral indices, trace
normalizations, coupling marginals, measurability and conditional scopes.
No imports, tests, scientific computations, seeds/draws, backend runs or
QPU operations were performed. The independent 348-line proof is preserved.
