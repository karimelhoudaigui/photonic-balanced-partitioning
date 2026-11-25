# P76 exact-hash independent author-proof review

**Primary verdict: proved as written**, for the author's scoped statements
about the weak projected map, exact vacuum-only primitive, composable
diagonal model and classical replacement. No mathematical correction to
the frozen author source is requested. This does not establish a universal
optical impossibility, matched total-resource advantage or hardware result.

## Exact coverage and review provenance

All357 lines of the current root artifact
`theory/P76_weak_filter_route.md` were read. Its exact SHA256 is
`bd1d73a69f15480a7ab8e95ddd5bce38815620ee1234880ec48c3da8f48d08a3`,
original author commit5586b13/root492e744 as recorded by ROOT. The hash
was independently checked before this review. No author file was changed.

Before opening it, the reviewer froze a separate301-line derivation,
`theory/P76_independent_weak_filter_audit.md`, SHA256
`f1242c16ba8ac27019ac70a9eb11ef61b226d166963b04e3f26ede06589c1476`.
Its original worktree index could not be mapped, so there is deliberately
NO fabricated original freeze commit. ROOT preserved those identical bytes
and provenance centrally in commit75e579f BEFORE author access. The original
independent file's hash was reconfirmed unchanged. The failed index was
left intact; no reset, deletion, rebuild or Git mutation was attempted
for this author review.

Review date: 25 November 2026. Worktree `.local/p75-code-review`, prior
committed base10eee38701d9e0cf7f197cd556655b26cc08c277, with the separately
frozen independent note. Only this SECOND report is written. ROOT supplied
the candidate question and later the exact author identifier. The present
comparison is not blind because the author's disposition is visible.
Independent derivation preceded that access; it is not independent
discovery or execution.

Inspection used source text, hashes and hand algebra only. No scientific
import, AST, test, RNG, probability query, circuit construction, simulation,
backend, external source acquisition, manuscript edit or QPU call occurred.
No P75 output or numerical worker data was accessed. All load-bearing
implications here are internally proved; no primary citation or novelty
claim is needed.

## Claim chain and physical object

The author distinguishes three objects correctly:

    physical passive beam splitter on two active rails
       -> projected final logical diagonal, with unflagged leakage
    passive vacuum/count herald with exactly no accepted data leakage
       -> full-support diagonal primitive must factor locally
    abstract genuine composable diagonal instrument
       -> Gibbs bias and an exact latent classical record construction.

The second object is not inferred from the first's projected truth table.
The third is explicitly granted as a different paid resource, not built
by writing down its diagonal. Source preparation and complete source-cycle
normalization remain separate from per-valid-register probabilities.

The dual-rail code has one photon per logical rail pair. Balanced source
labels are fixed-weight strings. In the physical pair-gate discussion the
two qubits must exist, and the full-support primitive is required on all
four two-qubit basis inputs. For N>=4 all four pair assignments occur in
the supported global balanced code. A source-specific transformation on
one known entangled vector is explicitly outside that primitive theorem.

## Beam-splitter Fock map and failure reentry

The author's matrix R_theta=[c,-s;s,c] uses input creation columns.
Multiplying the two active creation factors yields

    (c a^dagger+s b^dagger)(-s a^dagger+c b^dagger)
      =-cs(a^dagger)^2+(c^2-s^2)a^dagger b^dagger
         +cs(b^dagger)^2.

Thus normalized bunched amplitudes are -sqrt(2)cs and +sqrt(2)cs,
and the kept |11> amplitude is q=cos(2theta). One active input photon
has survival amplitude c; zero active photons have amplitude1. In logical
order00,01,10,11 this verifies diag(1,c,c,q) AFTER code projection.

For01/10 the transferred active photon occupies the other qubit alongside
its spectator photon, giving an empty source qubit and a two-photon
destination qubit. For11 the leaked photons bunch in active rails while
spectator logical-zero rails are empty. These are retained data-sector
failures, not photon loss. Vacuum/no-loss flags do not identify them.
Nonzero local attenuation preserves a nonzero amplitude on those paths;
zeroing transmissions cannot provide the desired full-support gate.

The inverse-block check is exact: R_-theta R_theta=I, so final code
success is one, whereas multiplying projected diagonals gives
diag(1,c^2,c^2,q^2). Noncode intermediate paths account for the difference.
The author correctly refuses to multiply logical projection probabilities
as protected heralds. The statement is algebraic; no numerical circuit
qualification or physical device capability is implied.

## Weak sign, equalization and Boltzmann parameters

At small fixed theta, 2log(c)=-theta^2+O(theta^4) and
2log(cos2theta)=-4theta^2+O(theta^4). Hence the author's expression

    2log K(x_i,x_j)
      =-theta^2(x_i+x_j+2x_i x_j)+O(theta^4)

has the correct coefficients. With theta_e^2=t A_e,
sum_e A_e(x_i+x_j+2x_i x_j)=2sum_i d_i x_i-C_A(x).
On a regular weighted graph and a balanced code, the field term is
constant, leaving +t C_A in the weak log probability: the bare projected
bias favors larger cuts. On nonregular graphs the field is not discarded.
These are finite-instance weak expansions, not uniform graph-size error
or optimizer guarantees.

The cross ratio q/c^2=1-tan^2(theta) is below one for0<theta<pi/4.
Multiplication by local nonzero diagonal factors preserves it. Attenuating
each logical-zero rail by sqrt(q) changes the projected diagonal to
(q,c sqrt(q),c sqrt(q),q). Logical X conjugation on one qubit gives

    G_theta=diag(u,q,q,u), u=c sqrt(q), 0<q<u<1.

This uses contractions and a basis relabeling, without gain or optimum
data. It does not remove the missing code flag. The ratio of cut to
aligned SUCCESS PROBABILITIES is q^2/u^2=q/c^2, not q/u or its reciprocal.
The highest abstract success probability is h=u^2 and tends to one;
it would be incorrect to assign a universal small h cap to this model.

Writing rho=exp(-beta A_e), finite beta>=0 and finite A_e>=0, gives

    tan^2(theta_e)=1-rho,
    c_e^2=1/(2-rho), q_e=rho/(2-rho),
    u_e^2=rho/(2-rho)^2.

The source's parameter formulas are therefore correct. At beta A_e=0
the identity limit is well defined. The strictly positive formulas concern
rho>0; an infinite-beta zero-support limit is not a full-support primitive.
No actual arbitrary-angle heralded gadget is established by these identities.

For an abstract binary diagonal instrument, sqrt(I-G_e^dagger G_e)
is a valid complementary failure operator. This proves mathematical
completeness, not passive realizability. Multiplying accepted diagonals
then gives, per properly prepared uniform register,

    q_success(x)=(A0/D)exp(-beta C_A(x)), A0=product_e u_e^2,
    Pacc=A0 E_uniform exp(-beta C_A).

The conditional law is Gibbs. The factor A0 and all source-preparation
failures remain present before conditioning. If flagged register preparation
has probability p_src, multiplying by p_src is the correct outer-cycle
mass; it is not legitimate to credit every attempted source cycle as a
valid register. Further preparation flags need their actual paid instrument.

## Exact vacuum-only full-support primitive lemma

With two signal photons, vacuum ancillary inputs and passive optics,
a successful branch leaving two photons in the four retained rails has
vacuum on all ancillary outputs. Its signal action is Gamma(T), T the
retained one-particle contraction. Under exact no-leakage and nonzero
diagonal action, write its input-column linear forms as U_i and V_j.
They satisfy

    U_i(z)V_j(z)=k_ij z_(a_i) z_(b_j), k_ij!=0.

The author's polynomial factor lemma is correct. Restricting one target
coordinate to zero forces one restricted linear factor to vanish in a
polynomial ring without zero divisors; dividing out that coordinate then
forces the other factor. For fixed i, the same U_i must be compatible with
both b0 and b1, so U_i is proportional to a_i. Similarly V_j is proportional
to b_j. Thus k_ij=alpha_i beta_j and its cross ratio is one.

G_theta's cross ratio u^2/q^2>1 violates this exact factorization, so it
cannot be the asserted primitive in this resource model. The conclusion
requires equality in the COMPLETE retained two-photon sector; only a
projected logical diagonal does not meet the premise. Nonvacuum helpers,
changed photon resources, a nondestructive monitor, restricted known
sources or a different global code remain outside the lemma. The author
does not promote a two-qubit primitive result into a theorem about every
many-qubit optical circuit.

## Classical record construction and its limits

Given a genuine diagonal success map K_j|x>=f_j(x)|x>, let
p_j(x)=|f_j(x)|^2<=1. Starting from the uniform Dicke source, the
joint unnormalized string/success-prefix mass is

    (1/D)product_(j<=m) p_j(x).

Sampling a SINGLE uniform feasible latent X and tossing the prescribed
local coins reproduces that expression. Summing over X gives each optical
prefix survival probability; consecutive differences give the first-failure
index law. Accepted strings and coarse pass/fail abort records therefore
match exactly. This construction needs neither an optimum shift nor a
partition function and does not assume a free normalized Gibbs sample.

If every resolved outcome Kraus operator is diagonal, multiplying its
squared coefficients gives the author's complete branch formula. This
also supports adaptive diagonal choices driven by the SAME observed
history. The latent X is used to draw prescribed outcome probabilities,
not to grant the classical controller hidden information. A known basis
permutation can be tracked on X, even if it fails to commute with a
diagonal filter; noncommutation alone is not an interference witness.

With only a diagonal SUCCESS map, unresolved failure effects or maps may
be nondiagonal. The author correctly limits the guarantee to success and
aggregated first-failure records, not every failed Fock pattern or detailed
failure-dependent resource. A noncommuting continued state update, coherent
mixer, leakage/reentry block or genuinely difficult initial basis law
requires a new argument. The full-outcome diagonal hypothesis supplies
the stronger branch result; it is not silently inferred from a success
truth table.

For the Gibbs special case, direct classical rejection with probability
exp(-beta C_A(X)) may omit A0 because C_A>=0 and all u_e^2<=1. It keeps
the same conditional law with at least the acceptance probability. Scoring
that cut and evaluating the local coins remain actual work. The author
explicitly requires efficiently specified local factors and does not
claim arbitrary hard global diagonal oracles are efficiently simulated.

The separate independent note derives a further raw-proposal-count
domination by uniform feasible draws for diagonal-only fixed-basis trials.
The author need not state that stronger consequence for its exact-control
conclusion to hold. Neither result, nor absence of photons in a classical
implementation, automatically establishes equal wall-time or total-cost
advantage without a measured ledger. Source preparation, ancillas, reached
failures, scores and compilation remain paid in the author's formulation.

## Obligation matrix and disposition

| Obligation | Review |
|---|---|
| Exact357-line author hash and prior301-line independent freeze | Passed; independent source unchanged |
| Full-Fock beam-splitter signs and sqrt(2) factors | Passed by hand expansion |
| Vacuum flags versus data-code leakage and inverse reentry | Passed; no instrument shortcut |
| Weak bare sign, fields and projected equalization | Passed on stated weak/positive domains |
| rho/theta/q/u mapping and per-register versus source-cycle mass | Passed with failures retained |
| Vacuum full-support/no-leak factorization lemma | Proved by shared linear factors |
| Coarse success-prefix and first-failure control | Exact under diagonal-success/abort assumptions |
| Detailed records and adaptive full-outcome construction | Correctly requires stronger instrument data |
| Basis permutations versus recombining mixers | Correctly separated |
| Actual source/gadget, complete CPU/photon/wall ledger | Not supplied or claimed |
| Universal optics no-go, novelty, positive optimizer or QPU | Not established |

No remaining load-bearing gap was found in the exact source's actual
claims. Its strongest safe disposition is supported: reject the vacuum-
flag composability shortcut and a diagonal-only coherence claim; retain
the projected identities and abstract classical control; require a genuine
new operation/source/instrument before a physical optimizer followup.
No source edit, test, experiment or hardware action is authorized by this
review. Final mathematical proofreading checked basis signs, cross-ratio
orientation, positivity endpoints, accepted versus raw mass, no-leakage
quantifiers, failure-record scope and resource qualifiers. The original
independent proof and unavailable Git index are preserved unchanged.
