# P81: accepted stability of passive dual-rail code preservation

ROOT read the complete358-line derivation, independently frozen178-line
reconstruction and286-line exact-source audit. The quantitative bound,
exact boundary, exception and qualified adaptive consequence are accepted
under their stated physical and source hypotheses. This is an obstruction
for one specified class, not a positive optimizer or all-optics no-go.

## Exact reviewed evidence

| Object | Original commit | SHA256 |
| --- | --- | --- |
| `theory/P81_dual_rail_balanced_average_stability.md` | 0a51544a1a449c64b87cb48e82bf637583402278 | 7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f |
| `research/P81_independent_dual_rail_stability.md` | 13ce8144b49ec91e916e9ca3f7b178c3490547bf | b9261878a61760ab68a44c2519c2a76712f13673d73c21eee92eafac4b2f4fb0 |
| `theory/P81_EXACT_HASH_REVIEW.md` | f915cf90a79429d09fd8de9854ab42b1e08b861c | 5abfd4c9e5fa86452b83fae995cbe754ddf35e39bc74b0007bc1033c1bcb64e0 |

ROOT supplied the candidate formulas before the first two authors worked.
They froze separately without reading another P81 proof/verdict or talking
to one another. The third reviewer subsequently read both exact sources.
This is reconstruction and audit by independent agent contexts, with a
shared supervisor/model context; it is not independent discovery or an
external referee report. ROOT checked the decisive algebra, quantifiers
and boundary cases separately. No author correction was required.

## The accepted physical theorem

Let even N>=4 label N logical qubits on2N rails with exactly N photons.
Let U be one fixed lossless passive mode unitary, with no ancillas,
heralding, filtering or discarded outcomes. Its calibration source is
the UNIFORM INCOHERENT mixture of every balanced code basis string,
each with one photon per rail pair and N/2 logical ones. Let epsilon be
the raw probability that an output rail pair has occupancy different
from one. This includes wrong-pair occupancy without same-mode collision.

There exists a physical unitary V made of a permutation of WHOLE rail
pairs and independent two-mode unitaries, such that

    ||U-V||_F^2 <= 4*N*(N-1)^2*epsilon/(N-2).

For any common density matrix in the N-photon sector the full raw PNR
laws then satisfy

    TV(P_U,P_V) <= min(1,2*N*(N-1)*sqrt[N*epsilon/(N-2)]).

The calibration premise concerns the stated mixture for this same U;
the norm conclusion applies to any N-photon state. An efficient sampler
at V additionally requires a known code basis input or an efficiently
sampled diagonal mixture and accessible local probabilities. Conditional
on the basis label, local outcomes are independent Bernoullis and B=D.
The unconditional mixture may be correlated; an arbitrary entangled
input receives no efficient-sampling conclusion.

## Why the bound holds and where it stops

The ordered bosonic factorial-pair kernel is
q(u,v)=||u||^2||v||^2+|u^dagger v|^2>=0. For2x2 blocks U_ab put
R_ab=U_ab U_ab^dagger and B_ab=Tr(R_ab)/2. Unitarity makes B doubly
stochastic. Averaging the pair kernel over all code basis inputs gives

    F_(a,all)=[6-sum_b((Tr R_ab)^2+Tr(R_ab^2))]/4
             >=1-sum_b B_ab^2.

The6 is4+2 from the two-dimensional output pair. Balanced pair-pattern
weights are at least (N-2)/(4(N-1)), so nonnegative termwise comparison
and fixed total photon number give

    F_all <= (N-1)/(N-2)*F_bal
          <= N*(N-1)^2*epsilon/(N-2).

An internally proved Hall/decomposition argument selects a permutation
with selected B mass>=sum B_ab^2. The off-block Frobenius mass is at most
2F_all. Unitary polar completions of selected2x2 contractions, including
zero singular values, cost at most that same mass. Thus ||U-V||F²<=4F_all.
Tensor telescoping on the symmetric N-photon sector and trace-distance
contraction give the TV coefficient above, without an extra factor two.

At epsilon0, U is exactly local up to whole-pair permutation. If EVERY
balanced basis input also has exactly balanced output weight, each local
Bernoulli variance vanishes. The allowed actions reduce to pair
permutations, local rail phases and either no bit flips or GLOBAL
complement. This monomial refinement uses exact feasibility; approximate
code leakage alone does not establish its quantitative version.

N2 is a genuine exception: swapping only a1 and b0 fixes balanced01/10
but sends00 and11 out of the pair code. A visited-only subset also fails
to supply the premise at larger N. A coherent Dicke state has off-diagonal
input terms absent from the proof. Loss/heralding/additional modes,
input-dependent nets and coherent multishot memory are different models.

For measured/reset adaptive protocols, a full counterfactual calibration
premise is required for EACH realized net at each common history/mark.
With a common classical count-driven controller and a measurable V
selection, transcript TV is at most the sum of conditional absolute
errors (or their expectations). This is not visited-only certification,
relative rare-event accuracy or a matched CPU/hardware cost comparison.

The coefficient grows as order N² before multiplying sqrt(epsilon), so
the bound may be uninformative at practical leakage. Large leakage and
nonmonomial/full-cross-rank designs remain research routes, with failures
charged. No novelty or hardware claim is accepted. No numerical P81
experiment ran; empirical calibration would need a new statistical
contract. The user's positive optimization target remains OPEN.
