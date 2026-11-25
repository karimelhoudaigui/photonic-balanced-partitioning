# P74: graph-cost phase gates and an unconditional herald-resource screen

25-Nov-2026. STATIC independent derivation from the coordinator's proposed
nonlinear route. No code/import, circuit construction, numerical amplitude,
test, sample, calibration, QPU call, hardware circuit freeze or manuscript
edit. The only source acquisitions were the installed Perceval catalog
implementation bundle and one versioned primary Knill paper.

**Decision: REJECT the simple low-success, no-recovery edgewise profile
under the stated raw-attempt/proposal-count screen. KEEP the nonlinear cost
encoding as a different model. Recovery, improved weak-phase gates and
jointly compiled heralded blocks remain OPEN with explicit resource and
Kraus-operator obligations.** This is not an all-photonic-QAOA impossibility,
a device benchmark, a matched-clock theorem or a positive optimizer result.

## 1. A different encoding: N logical qubits and N signal photons

For even N>=4 encode each vertex bit x_i in a dual-rail qubit with exactly
one photon in its two rails. This uses N signal photons and 2N logical
rails, before ancillary photons/modes. It is not the earlier N-mode,
N/2-photon occupied-subset source. Balanced feasibility means sum_i x_i=N/2.

Let n_i=(I-Z_i)/2 be the logical one-projector, A_ij>=0 graph weights,
d_i=sum_j A_ij, and

    C=sum_{i<j} A_ij*(n_i+n_j-2*n_i*n_j)
      =sum_i d_i*n_i-2*sum_{i<j}A_ij*n_i*n_j.

The optimum-blind cost unitary is therefore

    exp(-i*gamma*C)
      =product_i exp(-i*gamma*d_i*n_i)
         *product_{i<j} exp(+i*2*gamma*A_ij*n_i*n_j).

Only graph weights enter; no C*, optimal-state mask or selected optimum is
used. The one-qubit phases are passive rail phases. The controlled phases
are genuine logical interactions, not merely a one-particle hopping matrix.

The fixed pi-CZ profile below is NOT a native arbitrary weighted phase.
Generic edges require phi_ij=2*gamma*A_ij modulo2pi. A pi-CZ implements only
phi=pi; integer-weight parity at a special gamma is not the full weighted
cost in general. One synthesis of an arbitrary controlled phase uses two
CNOTs and local rotations, making its herald cost worse, not free. With
Rz(theta)=exp(-i*theta*Z/2), the ZZ factor in

    exp(i*phi*n_i*n_j)
      =exp(i*phi/4)*exp(-i*phi*Z_i/4)*exp(-i*phi*Z_j/4)
          *exp(i*phi*Z_i*Z_j/4)

can be CNOT * Rz_target(-phi/2) * CNOT. A Knill CNOT is a Knill CZ conjugated
by target Hadamards. Two monitored CNOTs give the squared herald probability.
This is one explicit profile, not an optimal synthesis theorem.

Uniform feasible superposition |D_N,N/2> has amplitude 1/sqrt(D_N) on
D_N=binom(N,N/2) states. Preparing it is not assumed free. Moreover the
cost layer ALONE only changes its phases, so computational-basis measurement
still gives exactly the uniform feasible law. An optimizing mechanism needs
a noncommuting mixer or other coherent operation. A balanced logical XY
mixer is itself an interaction resource; a generic physical beam splitter
between qubits cannot be declared a deterministic code-preserving XY gate.
Additional mixing, preparation and final feasibility costs remain paid.

## 2. Exact verified profiles: primary scope and local provenance

Primary source1 is the installed Perceval1.3.0 catalog implementation bundle,
read as text, without importing it. Key file hashes are:

| Installed relative file under site-packages/perceval | SHA256 |
|---|---|
| `components/core_catalog/heralded_cz.py` | `b1c0bdee32442243ec9db27e286b96fcbb3769e91b51ddd58a5980cc86a17e8a` |
| `components/core_catalog/postprocessed_cz.py` | `6e7a8f832cff1c8bc259bf055a804f95ddf4de35a4f866d2fa634ab5da8d8a80` |
| `components/unitary_components.py` | `2f4bacd1d3d5c919b32eaaf28d1881a5f49be608ffca4be2ee53886a149786df` |
| `components/experiment.py` | `a221a62d05642d574fae17cfd8177229d41cde47773e678069a26c195d628aa3` |
| `components/component_catalog.py` | `e3abe68ec6cda33fd3d1e1e46887bffbc550679acc521071357ef270129d8c0d` |
| `components/_mode_connector.py` | `12b1855cae85d01ed962f44842fb07f3609fe52b48d4d0c6822c8534cd4d5d55` |

Primary source2 is E. Knill, *A Note on Linear Optics Gates by Post-Selection*,
[arXiv:quant-ph/0110144v2](https://arxiv.org/pdf/quant-ph/0110144v2), official
version metadata25-Oct-2001, related PRA66,052306. Equations(2)--(8) require
zero logical leakage and equal success amplitudes except the controlled
phase. Equation(11) and its following paragraph give a two-helper-photon
pi-phase implementation with success2/27. This verifies a state-independent
heralded PROFILE, not a universal upper bound for all gates/resources.
No local PDF hash or exhaustive literature/optimality claim is made.

The catalog heralded-CZ implementation has six optical modes: four data
rails and two single-photon ancillary modes. Its experiment registers
one input AND one expected output photon on each ancillary mode4,5, with
no additional logical postselection predicate. The comments identify the
paper's circuit and account for beam-splitter phase conventions. The primary
paper explicitly imposes the no-leakage conditions, so its accepted Kraus
operator on the dual-rail code is, up to a global phase,

    K_success=sqrt(2/27)*CZ.

K_success^dagger K_success=(2/27)*I on the logical code. Hence success is
state-independent even for an input entangled with the rest of a register.
The installed numerical catalog decomposition was not executed or separately
certified here; the mathematical profile is authenticated from the paper.

The catalog postprocessed-CZ instead has two VACUUM ancillary modes with
expected input/output0 and ALSO a predicate requiring one photon in each
data-rail pair. It is a different instrument. Its1/9 is derived next from
the local beam-splitter/permutation definitions, not used as a nondestructive
herald success rate.

## 3. The1/9 profile and an explicit failure-reentry counterexample

Use the catalog Hadamard beam-splitter convention with

    a=1/sqrt(3), b=sqrt(2/3), BS=[[a,b],[b,-a]].

Following the two catalog mode permutations, the data-to-data submatrix
when the two ancillary outputs are vacuum is

    T=[[a,0,0,0],
       [0,-a,b,0],
       [0,b,a,0],
       [0,0,0,a]].

Let Pcode select one photon in rails0,1 and one in rails2,3. In the logical
basis defined by occupied pairs(0,2),(0,3),(1,2),(1,3), direct two-photon
permanents give

    Pcode*Gamma(T)*Pcode=(1/3)*diag(1,1,1,-1).

Thus the single-block logical POSTSELECTION success is1/9. Vacuum heralds
alone do not certify the code: for the input with photons in rails1,2,
the middle block yields amplitude1/3 for one photon each and amplitudes
-2/3,+2/3 for bunched outputs2,0 and0,2. Those failure branches have vacuum
ancillas too, and two photons in one qubit instead of one in each.

Now concatenate two identical raw blocks WITHOUT measuring/projecting the
logical code between them. On those same rails1,2, the one-particle matrix
B=[[-a,b],[b,a]] satisfies B^2=I. No ancillary photon is involved on that
subspace. The same input returns to its valid logical state with probability
ONE after two blocks, even if separate vacuum ancillas are checked. Naively
multiplying1/9 by1/9 would predict1/81. This is a full-Fock failure-reentry
counterexample, not an advantage or a correct two-gate logical implementation
on every input.

Algebraically, Pcode*K2*K1*Pcode includes
Pcode*K2*(I-Pcode)*K1*Pcode, omitted by multiplying the projected logical
matrices. Logical data projectors act on reused modes and do not commute
through later blocks. Final software postselection is not an intermediate
nondestructive code measurement. Catalog composition also has postselection
consistency checks; nothing here claims it silently permits every unsafe
logical concatenation. The error is replacing a physical block by its
conditioned logical matrix without proving composability.

## 4. Protected herald flags may be measured at the end

For the Knill heralded profile, accepted ancilla measurements already leave
the logical code invariant. If every gate uses DISTINCT flag modes, and
all later operations act as identity on those logical flag degrees of
freedom, final measurement of all flags is equivalent to measuring them
immediately. Their projectors commute with all later operations. Multiplying
accepted Kraus operators then gives the valid all-herald probability.
Real-time feedforward is not required for THIS probability identity.

Static inspection of standard catalog Experiment composition supports this
model: heralded subexperiments are copied; ModeConnector appends fresh
ancillary modes at the current circuit size; normal integer mappings skip
old herald modes; and consistency permits connections only to PHOTONIC
outputs, not HERALD outputs. Routing permutations and their inverses can
move and restore the flag labels without reusing them for the new gate.
The corresponding catalog processor wrapper delegates to this experiment.

This is an implementation-model observation, not a run of a compiled
multi-gate circuit or evidence of native Lucy nondestructive detection,
quantum memory, feedforward or even a supported remote source. A raw Circuit,
manually reused ancillary rails or cleared port metadata need a fresh audit.
If flags are only measured at the end, all their photons/modes must be
provided for the whole fixed circuit; early-abort savings are not automatic.

## 5. Exact no-recovery product bound

Assume a completed logical attempt requires at least g nondeterministic
gate successes, with every realized conditional accepted probability at
most h<1 on its valid current code state. Reject the attempt on an uncorrected
failure, and do not recycle a failure branch into acceptance. This is satisfied
by the specified ideal Knill profile with h=2/27, fresh helper photons and
protected separate herald records. If a gate accepts several corrected
outcomes, h must bound their TOTAL accepted probability, not one chosen
pattern while forgetting the others.

Condition successively on the entire past. On the all-accepted prefix,
the next success probability is at most h. The tower rule yields

    P(all required heralds accepted)<=h^g.

State-independent Kraus operators sqrt(h_j)*U_j give equality product_j h_j
before any other source/loss/readout failure. The upper bound remains valid
for adaptive gate choices/history if the same conditional cap holds and at
least g such successes are required on every completed branch. Distinct
protected deferred flags give the same statement by section4. Arbitrary
postselected logical filters do not satisfy these premises merely by having
a single-gate conditional1/9 success.

Let q(S) be the unconditional probability that an outer attempt returns
feasible S WITH all required accepted heralds. Source/preparation and final-
feasibility failures count as failures, not successful candidates. Conditioning
first on a properly prepared code source gives the product bound; averaging
over preparation can only decrease it. Then

    q(S)<=h^g,  sum_S q(S)<=h^g.

This is a subprobability law of successful proposals. Failures repaired to
the incumbent are not counted as successful proposals and retain their
physical cost; no pointwise domination of the repaired full Markov kernel
is asserted.

## 6. Uniform-feasible domination and its exact scope

There are D_N=binom(N,N/2) oriented balanced candidates. If

    D_N*h^g<=1,

then q(S)<=1/D_N for every S. A uniform feasible proposal u(S)=1/D_N
therefore dominates the raw successful proposal mass on EVERY set A:

    sum_{S in A}q(S)<=|A|/D_N.

With a common initial incumbent, this implies first-order stochastic
dominance of the BEST RECORDED cut after one proposal: below the incumbent
cost use the corresponding cost sublevel, and at or above it both best-cost
CDFs equal one. Failures are paid self-loops, not favorable outputs.

If the bound holds conditionally after every adaptive history, a fixed
sublevel A has per-attempt hit probability at most |A|/D_N. No independent
quantum shots are assumed. Induction gives a T-attempt quantum hitting
probability at most

    1-(1-|A|/D_N)^T,

exactly attained by iid uniform feasible candidates. Consequently uniform
feasible search dominates best-recorded-cut CDFs at every T under this
RAW-ATTEMPT count comparison. Every paid training attempt belongs in T.
This is not a wall-clock, circuit-compilation, energy, CPU or equal-shot-
score-cost theorem. The operations and score evaluations of both methods
still require an actual matched-resource ledger before a broader claim.

For completeness, write N=2m and b_m=binom(2m,m)/4^m. Then b_1=1/2 and

    b_(m+1)/b_m=(2m+1)/(2m+2)<1.

Thus D_N<=2^(N-1), strictly for N>=4. If the STIPULATED implementation
uses at least one capped-success entangler for each edge of a connected
NONTRIVIAL interaction graph, g>=N-1. With h<=1/2 this proves the screen,
strictly for N>=4. Knill's2/27 profile is well inside that cap; two such
successes per arbitrary-angle edge only worsen this simple profile.

This edge count is NOT a compiler lower bound. Zero phases, canceled gates,
joint compilation and phase identities can change it. For example, complete
uniform-weight graph cut is constant on balanced subsets, so the entire
cost phase is global there and needs no entangling gate. A connected input
graph alone never proves g>=N-1 for every encoding or parameter choice.

## 7. Real resource accounting, including early abort

The logical source already costs N signal photons in2N rails. Dicke-state
preparation, its ancillary photons/heralds, parameter selection and any
noncommuting mixer are additional. No nondestructive Dicke projection is
provided by measuring data photons and forgetting that the state was
destroyed. Every logical-code or balanced-output rejection remains paid.

A fixed Knill edgewise circuit with g gate gadgets uses two auxiliary
photons per gadget. If all modes are launched before final herald reading,
its gate ancillas cost2g photons per outer attempt, plus the logical source
and preparation resources. That is the protected-deferred-herald case.

If actual intermediate flag detection AND on-demand injection allow abort
before the next gadget, the expected ancillary count conditional on starting
a valid register is instead

    2*sum_{j=1}^g h^(j-1)=2*(1-h^g)/(1-h)

for the ideal constant-h no-recovery chain. Later resources are charged only
when reached. This does not improve the all-gate success probability h^g,
and it does not remove preparation of a fresh N-photon register on each
outer restart. Using2g unconditionally in that abort model would overcharge;
assuming the abort savings for a fixed static device would undercharge.
Neither architecture or timing capability is inferred for Lucy.

## 8. What must change before a positive experiment is plausible

For a complete algorithm define Y as its unconditional usable logical-output
probability, including preparation, accepted gate records and readout. If
Y<=1/D_N, then the same pointwise screen holds regardless of how favorable
its conditional candidate distribution is. Escaping this particular screen
requires Y>1/D_N; this is NECESSARY to escape the screen, not sufficient
for optimization advantage, independence/relabeling replication or hardware
readiness.

For a product profile with ideal other stages this requires

    product_j h_j>1/D_N,
    geometric_mean(h_j)>D_N^(-1/g).

Preparation loss makes the requirement stronger. For N=4, D_N=6: even a
jointly compiled single logical cost block would need usable probability
above1/6 to evade this probability ceiling. That exact threshold is a
screen, not a prediction of any attainable gate. For g asymptotic to c*N,
the threshold tends to 2^(-1/c), in particular
one half when g is asymptotic to N. For g of order N^2 it approaches one
with deficit of order1/N. This follows from
2^N/(N+1)<=D_N<=2^N: the central coefficient is the largest of N+1
binomial coefficients summing to2^N. No actual device values are inserted.

A weak controlled phase can have a different profile, approaching the
identity as its angle tends to zero. The checked pi-gate does NOT prove a
universal h<=1/2 for such gates. High-success entangled-ancilla schemes,
error correction, recovery or repeat-until-success change the assumptions
and remain separate routes. No source, boost or feedforward is assumed free.

## 9. A conditional recovery escape, and why Knill does not supply it for free

A logically consistent abstract recovery instrument would have

    K_s=sqrt(h)*U_phi,
    K_f=sqrt(1-h)*V,

where V is a KNOWN code-preserving unitary. Completeness holds exactly.
After failure, apply V^dagger and retry with fresh ancillas. With at most R
tries per logical gate, success becomes

    h_R=1-(1-h)^R,

and expected trials until success or cap are h_R/h. Unlimited retries have
mean1/h trials per gate while retaining the unknown logical register, if
all stated lossless recovery assumptions hold. This is an abstract instrument
check, not a passive optical construction of U_phi.

It shows a genuine mathematical way to escape the h^g all-first-try model.
For example, R>=ceil(log(2g)/[-log(1-h)]) ensures
(1-h)^R<=1/(2g), hence h_R>=1-1/(2g), and
Bernoulli's inequality yields h_R^g>=1/2. This can pass the1/D_N ceiling
for N>=4, but needs the new recovery operation, fresh ancillas, physical
memory/feedforward and their actual failure/loss costs. No optimizer benefit
follows from passing a necessary probability screen.

The Knill profile does not have ONLY known-unitary failure branches. In
the paper's active-mode coordinates, input signal00 with helper11 has a
failure output signal11/helper00 whose two-photon amplitude is

    per[[sqrt(2)/3,2/3],[-2/3,sqrt(2)/3]]=-2/9.

Its nonzero probability is4/81. The two inactive logical rails still carry
their original photons, so this branch leaves four data photons rather than
a two-photon logical pair. A passive unitary correction cannot restore the
code by changing photon number. The simple K_f model is therefore FALSE
for all failures of this checked profile. Partial recoveries, replacements
or error-corrected schemes need their own complete instrument and yield
analysis, not the formula h_R applied by assumption.

A second open alternative is a JOINT heralded cost/mixer block whose complete
accepted Kraus map is K=sqrt(H)*U_target on the relevant feasible code,
with zero leakage. Its success need not equal the product of isolated gate
rates. The cheapest discriminating proof-level check is K^dagger K=H*I,
correct target phases/interference and all noncode amplitudes zero, followed
by an actual preparation-inclusive H large enough to beat the1/D_N screen.
A catalog single-gate simulation or a logical postselected truth table alone
does not supply that bridge.

## 10. Scientific disposition

The nonlinear cost operation is a substantive change from passive hopping,
but cost phases alone do not bias Dicke measurement. Under the verified
low-success no-recovery edgewise profile, even an ideal conditional sampler
cannot overcome the uniform-feasible raw-proposal screen on the stated gate
counts. Ancilla-failure branches, postselection, preparation and mixers
cannot be removed from that accounting.

The negative screen closes only this simple profile and counting comparison.
Weak phases with better profiles, correctable failures, resource-state
amplification and jointly compiled blocks are OPEN hypotheses requiring
new conditional-to-unconditional evidence. Nothing here assumes native Lucy
support, requests QPU access, or certifies matched total-resource advantage.
The user's positive, reproducible optimization objective remains open.
