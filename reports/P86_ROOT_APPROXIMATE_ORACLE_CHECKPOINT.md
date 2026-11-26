# P86: accepted quantitative passive cost-phase error floor

ROOT's171-line proof, the separately frozen256-line reconstruction and
299-line exact-source review were read completely and reconciled. The
stated bound is accepted without correction. The common phase, norm and
source restrictions are part of the result, not optional qualifications.

| Artifact | Original commit | SHA256 |
| --- | --- | --- |
| `theory/P86_APPROXIMATE_PASSIVE_COST_PHASE.md` | daf49c64feb070f82412b8c3f59a63d8eb4f742d | a8074fd204b5294d455601a1e44751b1cc6656e0f565b4e10ddefe100564a932 |
| `research/P86_independent_approximate_cost_phase.md` | 36ff60481e259438fd9d4cf58ef6953109572384 | cf156f61e2c47864c024cc471d6e1fc873aec18158ba5a4c70898d456eb8342a |
| `theory/P86_ROOT_SOURCE_EXACT_REVIEW.md` | 93139b42d3e1056f90c67411530d1a51f05334f0 | 88b3df748ceb2b5e6327a90a8b155ca117c9d85acf349986e5d08e2a9c458682 |

ROOT supplied the route before the second author worked. The reviewer
wrote its entire standalone audit of ROOT's source before reading the
independent reconstruction, retaining its pre-comparison hash. This is
independent reconstruction/source review with shared supervisor/model
context, not independent discovery, external review or novelty evidence.

## Accepted theorem

For even N>=4, N photons on2N dual rails, fixed lossless passive U with
no ancillas, heralding, loss or filters, and complement-invariant C(S),
define delta as the MAXIMUM state-vector error over ALL balanced basis
inputs, minimized over ONE COMMON global phase chi relative to
exp(i chi-i gamma C(S))|S>. For every balanced pair S,T,

    delta >= |sin(gamma*(C(S)-C(T)))|/(2b_N),
    b_N=1+N sqrt[4N(N-1)^2/(N-2)].

The error is phase-sensitive. Per-basis PNR/fidelity cannot detect the
desired relative phases and receives no such lower bound. Allowing a
separate fitted phase for each input would invalidate the claim.

The proof bounds P81's uniform raw leakage by delta², constructs its
local-block/pair-permutation V and compares each column with error
e=b_N*delta. Large e>=1/2 is trivial. Smaller e forces every diagonal
V amplitude above7/8 in modulus; two balanced00/01 patterns then rule
out a nonidentity pair permutation by one local unitary row norm. Local
blocks need not be monomial. Their complementary diagonal amplitude
products are constant, giving2|sin(gamma difference)|<=4e. All constants,
N4 patterns and zero-entry cases were checked without code.

For fixed N and fixed nonconstant range R, this implies
liminf delta/|gamma|>=R/(2b_N), so error o(|gamma|) is impossible in this
metric for an arbitrary, even discontinuous, family U_gamma. Identity
still gives O(|gamma|) approximation. The same lower bound holds for
the stronger restricted-subspace operator norm, in that ONE direction.
True extrema are analysis parameters; no encoder receives C* or a mask.

No fixed absolute error, dimension-uniform bound, approximate graph-weight
classification, all-sampling-optimizer obstruction, hardware capability
or novelty is proved. Integer-weight phases at pi and constant costs
correctly give zero sine bounds. P82's current-dependent Fock/repair sampler
is a different task. P87 is a separately frozen proposed sharp fixed-N
extension; it is not an unstated premise or already accepted here.

No numerical experiment, scientific import, backend or RNG was needed.
The existing1187PASS executable tree is unchanged. Manuscript/main/QPU
remain frozen, and the positive optimizer objective remains OPEN.
