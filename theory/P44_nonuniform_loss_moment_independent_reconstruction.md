# P44 — independent nonuniform-loss moment reconstruction

Analytic reconstruction, 2026-11-24, frozen BEFORE reading any author P44
proof. The critical derivation was first sent to the coordinator by message.
No numerical run, primary computation, manuscript edit or QPU call is used.
This file does not change P42 inputs/raw or the P43 records.

## Claim card and verdict

Let N photons occupy N DISTINCT input spatial modes, one photon per mode.
Let T be the system transmission matrix of a passive linear optical network
with all environment inputs in vacuum. T can be rectangular and have arbitrary
nonuniform losses, but must be the SAME spatial contraction for all internal
states when internal states are present. Put eta_max=||T||_op^2 in[0,1].
There is no current-shot herald or loss information used to select/condition
that shot. All loss sectors are retained. For distinct system output modes
S={s_1,...,s_k}, the moment is the unconditional expectation of their actual
detected number operators.

**Verdict: proved as written within these physical hypotheses** for fully
indistinguishable photons:

    mu_S := E[product_(i in S) n_i] <= eta_max^k,
    Pr(exactly clicked support S) <= eta_max^k.                 (P44.1)

Separately, for arbitrary physically admissible internal states, including
correlations, with fixed CF spatial inputs and internal-blind T:

    mu_S <= k! eta_max^k,
    Pr(exactly clicked support S) <= min(1,k! eta_max^k).        (P44.2)

The factorial bound is sufficient here, not asserted sharp. It does not imply
that arbitrary partial distinguishability preserves the stronger constant1.
N is arbitrary finite; the proof has no N<=12 requirement. If k>N the moment
and event are zero. For k=0 the empty product is1 and the empty-support event
has probability at most1; use this deterministic branch rather than an
ambiguous zero-to-zero power at eta_max=0.

## 1. Lossy Heisenberg picture and the CF source

Take a passive unitary dilation, with vacuum environment annihilators e_l.
The ACTUAL output operators have the form

    b_i = sum_a T_ia a_a + sum_l R_il e_l.

They are canonical because of the full dilation. For distinct outputs,
normal ordering gives

    product_(i in S) n_i
      = (b_(s_k)...b_(s_1))^* (b_(s_k)...b_(s_1)).

Only AFTER this normal ordering may vacuum-environment terms be dropped in
the expectation. Defining Ta as a new canonical output operator and commuting
it as though TT*=I would be invalid; that shortcut is not used here.

Let A0 be the N occupied inputs and B=T[S,A0], a k-by-N matrix. Acting the
annihilation product on the normalized source product_(a in A0) a_a^*|0>
cannot use an input twice, because every input has occupancy1. For a chosen
removed subset A of k inputs the amplitude is per(B[:,A]). Residual CF input
states have different hole subsets and hence are orthogonal. Consequently,
for fully indistinguishable photons,

    mu_S = sum_(A subset A0, |A|=k) |per(B[:,A])|^2.          (P44.3)

There is NO factor k!, no conditional surviving-sector normalization and no
(1-eta)^(N-k) factor in this formula. It is the full normally ordered moment,
not the probability that exactly k photons survive. Arbitrary additional
system detections and all losses have already been marginalized.

## 2. Permanent Cauchy--Binet, with all repeated columns retained

For completeness the repeated-column identity can be proved from normalized
Fock amplitudes. In k one-particle dimensions define the unit vector

    |Omega_k> = 1/sqrt(k!) sum_(pi in S_k) |pi(1),...,pi(k)>.

It is the ordered representation of one photon in each of k distinct modes.
For any k-by-k matrix G,

    <Omega_k|G tensorpower k|Omega_k> = per(G).               (P44.4)

The k! equivalent relative permutations cancel the bra/ket normalization.
The vector (B*) tensorpower k |Omega_k> is in Sym^k(C^N). Expand it in the
orthonormal Fock basis indexed by t=(t_a), sum t_a=k. If B[:,t] repeats its
a-th column t_a times, the Fock amplitude is

    conj(per(B[:,t])) / sqrt(product_a t_a!).

Indeed the normalized Fock vector at t sums k!/prod t_a! distinct ordered
words; together with Omega_k's normalization this gives exactly that
denominator. Squaring and summing the amplitudes therefore proves

    per(BB*)
      = sum_(t>=0, sum t_a=k) |per(B[:,t])|^2 / product_a t_a!.
                                                                  (P44.5)

All terms in this expansion are nonnegative. The t in{0,1}^N terms are
exactly (P44.3), so

    mu_S <= per(BB*).                                        (P44.6)

Dropping repeated terms is an inequality; treating the distinct-column sum
as the whole permanent would be wrong. This is the point where a determinant
Cauchy--Binet formula cannot simply be copied for permanents.

## 3. The contraction bound has constant1

Input/output coordinate restrictions are contractions, hence

    0 <= BB* <= eta_max I_k.

By the spectral theorem every eigenvalue of (BB*) tensorpower k lies between
0 and eta_max^k. Applying (P44.4) to the normalized Omega_k gives

    per(BB*) <= eta_max^k.                                  (P44.7)

Combining (P44.3),(P44.6),(P44.7) proves the moment bound. On any outcome
whose clicked support is exactly S, every n_i with i in S is a positive
integer. Thus its indicator is at most product_(i in S)n_i pointwise,
proving the probability bound. In fact the same bound also applies to the
larger event that every mode in S clicks, without requiring other modes empty.

The contraction premise here is spectral, not just a bound on each row's
individual intensity. It is independent of N. For N>=k the universal support
cap is sharp within the stated class: route k chosen source inputs into S
with transmission amplitude sqrt(eta_max), and deterministically lose all
other occupied inputs. Then the event that all k survive has probability
eta_max^k and is exactly the target support. This is a diagnostic routing,
not a proposal to discover an optimal graph partition.

## 4. Arbitrary internal states: a separate routing bound

Purify any internal density operator if necessary. A CF input identifies an
internal factor per occupied input mode, though these factors can be correlated.
For distinct outputs, resolve the number operators over an orthonormal
internal basis, normal order, and drop vacuum environment inputs as above.
Group terms by the removed source subset A. Different hole subsets still
have orthogonal residual spatial occupations; internal correlations cannot
remove that orthogonality.

For fixed A, each routing pi from those k inputs to the k output positions
has scalar amplitude

    c_pi = product_(j=1)^k B_(j,a_(pi(j))).

Its internal/residual/purification vector v_pi is normalized: summing the
squared norms over resolved output internal indices equals the input
expectation product_(a in A) n_a=1. This argument needs no product-state or
single-Gram assumption. The vectors v_pi need not be orthogonal or identical.
The contribution from A is precisely

    ||sum_(pi in S_k) c_pi v_pi||^2.

Hilbert-space Cauchy--Schwarz bounds it by k! sum_pi |c_pi|^2. Summing over
A and then dropping the distinctness condition on input routings gives

    mu_S <= k! sum_(a_1,...,a_k DISTINCT) product_j |B_(j,a_j)|^2
         <= k! product_j sum_a |B_(j,a)|^2
         <= k! eta_max^k.                                   (P44.8)

Every dropped term is nonnegative. This proves the robust cap (P44.2), with
the same pointwise event-to-moment step. Fully distinguishable product labels
make the routing vectors orthogonal and satisfy the better constant1 by the
same nonnegative injection sum, but this does NOT make every partial case
bounded by the larger of the identical/distinguishable answers.

The known six-active-mode/species example with two spectator outputs has
moment coefficient7/6 and refutes extending (P44.1) to arbitrary internal
states. No numerical DFT rerun is made here. The constant k! deliberately
does not claim that invalid extension or monotonicity in distinguishability.

## 5. Adaptive search consequence and its resource scope

Suppose every fresh attempt at any allowed classical history h has CF source
and a passive vacuum-environment map T_h with ||T_h||^2<=eta0. The number N
and map may depend on history. In the fully indistinguishable case, each
fixed target support has conditional probability at most eta0^k.
Let D=binom(2k,k) be the number of oriented balanced supports. For a fixed
favorable set A, uniform feasible classical draws have success probability
p=|A|/D, while optical attempts have conditional probability at most
|A| eta0^k. With the P42 guaranteed budgets nC>0 and
L=ceil(nQ/nC), treating nQ=0 separately, it is sufficient that

    L D eta0^k <=1.                                         (P44.9)

The same first-hit/Bernoulli argument then gives domination for every fixed
cut threshold and hence final best cost, starting from a common frontend.
This is not transcript equality or a comparison of uncharged classical
candidates. Current-shot herald conditioning, retries and classical support
completion cannot be silently counted as single primitive detections.
Deterministic budget/cost inequalities are premises, not consequences of the
moment bound or mean device latency.

At equal attempt budgets L=1, D<=4^k shows that eta0<=1/4 is sufficient,
without ANY uniform-loss hypothesis. Exact finite D can improve the sufficient
threshold. For arbitrary internal states replace the cap in (P44.9) by
k! eta0^k. There is no dimension-uniform eta0=1/4 consequence from that robust
factor; its sufficient thresholds depend on k. Probabilities may always be
clipped above by1, without renormalizing accepted outcomes.

## 6. Scope falsifiers and calibration limits

- CF input is essential for (P44.1). Four photons from ONE input sent through
  a balanced two-output splitter with independent transmission eta give
  E[n_1 n_2]=4*3*(eta/2)^2=3 eta^2, exceeding eta^2. At eta=1/10 the exact
  two-click support probability is2167/80000, also above1/100. This is an
  algebraic scope check, not new data or a counterexample within the CF claim.
- The contraction is common to internal degrees. Polarization/frequency-
  dependent maps cannot be replaced by one T without a justified model.
- Vacuum environments matter. Extra thermal photons, bright ancillas, gain,
  dark counts or other added excitations do not satisfy the proof's channel.
- A mean transmission is not eta_max. A map perfectly transmitting k chosen
  source modes and losing the remaining N-k has mean source survival k/N,
  but eta_max=1 and target-support probability1. Replacing eta_max by k/N
  would give a false cap. A restricted occupied-input transmission norm can
  be used for a known source, but still requires a justified spectral bound.
- No operator norm, transfer matrix or confidence bound has been calibrated
  for Lucy here. The parameter eta_max and any certified upper bound on it
  are theoretical inputs. This result does not infer a hardware efficiency,
  available operation, detector mode, preparation rate or QPU decision.

## Freeze, provenance and next check

No author P44 proof, numerical raw or new calculation was read before this
reconstruction. The source card and prior P42/P43 mathematical context were
available; this is an independent derivation of that card, not a novelty
review. The ingredients are standard Fock normalization, normally ordered
passive-loss moments, permanent Cauchy--Binet, tensor-product norm bounds and
Cauchy--Schwarz. No new global mathematics or physical optimization advantage
is claimed. Commit this file before any author comparison, then audit any
received proof at its exact SHA in a distinct receipt. No P42/P43 artifact
is overwritten to record this result.
