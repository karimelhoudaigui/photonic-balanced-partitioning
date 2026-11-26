# P116 interaction audit and exact P122 count-mirror review

26 November 2026. Non-author MANUAL reconstruction, no execution. Two claim
cards are separated below; the valid catalytic gate is not discarded because
the specified feedback controller has a static terminal-count mirror.

P116 exact source read FULL315 lines: commitfbe08686fe69dd3de14384013fdc0da98e8da541,
research/P116_MEASUREMENT_INTERACTION_ROUTE.md, SHA256
27679d1a076d5e5a48844c11b6a0243e0b9f9570bbcc59de883f093c4c921db9.
P122 exact source read FULL111 lines: commit3c7d7acc8787d44528fad9edb39870d65db3b659,
research/P122_CONJUGATE_FEEDBACK_COUNT_NULL.md, SHA256
d1247c0767711b358daf451c7389dc0fe57cf9384afd6631cfc8389fc372d636.
I sent the conjugation derivation and logical/physical typing objection to ROOT
BEFORE reading P122; ROOT had explicitly requested that critical obligation.
Thus this is independent hand reconstruction of a suggested test, not blind
discovery. P120/other peer verdicts were not read. Both originals stay unchanged.

## Claim A — P116: correct only after stated restrictions

**Primary verdict: CORRECT ONLY AFTER STATED RESTRICTIONS.** The exact
ideal catalytic/X/filter/compiler/resource and success-only veto formulas
pass. Section6 conflates two Hilbert-space types and must not be executed
as unambiguous. Its sign-controlled feedback supplies NO new joint terminal
count law beyond a static circuit; that proposed observable escape is refuted.
The possible utility of retaining failures, or different multi-edge coherent
controllers, is not refuted by this finding.
Component verdicts: ideal gate/formulas PROVED AS WRITTEN within their scopes;
physical all-record specification ILL-TYPED/AMBIGUOUS before clarification;
claimed terminal-count escape from sign feedback REFUTED.

Dependency map: normalized BS coefficients -> successful catalyst Kraus map
-> X/local contractions -> graph edge filter -> compiler/success prefactor
-> weak-strength resource law and one-edge accepted-record veto. A SEPARATE
dependency is a physical mixer on every Fock sector -> branchwise permanent
law -> count-level adaptive novelty. The latter arrow fails by conjugation.

| Obligation | Disposition |
|---|---|
| Known4-CF/8-mode source, code, graph-only weighted edge law | Passed as ideal model |
| Normalized k(n), G_R and nonfactorization | Passed |
| X branch, h/rho compiler and actual herald probability | Passed |
| Weak subdivision cost and fresh-helper accounting | Passed with injection scope below |
| One diagonal layer/equal-X accepted-record veto | Passed with same code/proposals |
| Four/six-subset encoding and paid frontiers | Passed, budget-qualified |
| All-record physical mixer as printed | Ambiguous logical-vs-mode typing |
| Branch permanent/D formulas | Valid only after fixing that physical type |
| Claimed count-level effect from theta_f=+/-theta | Refuted: exact static mirror |
| Present Lucy source/PNR/delay/feed-forward support | Unverified; source correctly gates it |

### Catalytic Fock algebra, including factorials

For B_R=[[r,t],[-t,r]], the coefficient of b†^n c† in
(r b†-t c†)^n(t b†+r c†)/sqrt(n!) has helper-stay term r^(n+1)
and n exchange terms -n r^(n-1)t^2. Input/output normalization is the
SAME sqrt(n!), hence k(n)=r^(n-1)[R-n(1-R)], also giving k(0)=r.
Thus k0=r,k1=2R-1,k2=r(3R-2), and k0*k2-k1^2=-(1-R)^2.

The endpoint Hadamard sends |11> to(|20>-|02>)/sqrt(2). Identical catalysts
multiply both terms by k2*k0; undoing the splitter restores |11> exactly.
The one-photon sectors both acquire k0*k1. Therefore

    G_R=diag(R,sqrt(R)(2R-1),sqrt(R)(2R-1),R(3R-2)),
    g0*g2-g1^2=-R(1-R)^2.

The successful B map preserves the code. It is not a one-particle diagonal
attenuation, but remains a conditioned part of a larger passive experiment.
Helpers are indistinguishable in this derivation. Reusing G_R as the pure
D Kraus map would be wrong; unresolved internal tags leave a mixture.

### X branch and exact compiler

For2/3<R<1 put s=3R-2>0. X_B G_R X_B has entries(g1,g0,g2,g1).
The stated local attenuators multiply them by(sqrt(s),s,1,sqrt(s)), giving

    (H,Rs,Rs,H), H=sqrt(R)(2R-1)sqrt(s),
    rho=Rs/(2R-1)^2=1-(1-R)^2/(2R-1)^2 in(0,1), h=H^2.

Set z=sqrt(1-rho). Then z=(1-R)/(2R-1), so
R=(1+z)/(1+2z),s=(1-z)/(1+2z),2R-1=1/(1+2z).
Consequently h=(1-z^2)/(1+2z)^4=rho/(1+2sqrt(1-rho))^4,
exactly the compiler with rho=exp(-gamma). No amplification/CZ is needed.
For every normalized code input, p_herald=h*<exp(-gamma Pi_e)> lies
between h*rho and h. On |++> it is h(1+rho)/2; normalized concurrence
is(1-rho)/(1+rho). Neither entanglement nor h alone is an optimizer gain.

The older no-X magnitude interval follows from
(2R-1)^2<R(2-3R), namely7R^2-6R+1<0. Its roots are(3+/-sqrt(2))/7.
The maximum min(R,R(2-3R)) is1/3 atR=1/3. That prefactor bound is
scoped to those local diagonal contractions; extending it through X is false.
Where all entries are nonzero the phase invariant is pi. AtR=1/2,
balancing yields(1/4)diag(1,0,0,-1), consistent with the cited prior filter.

### Strength, one-edge mixer and graph limitations

For epsilon=1-R, 1-rho=epsilon^2/(1-2epsilon)^2, gamma=epsilon^2+O(epsilon^3),
and h=(1-epsilon)(1-2epsilon)^2(1-3epsilon)=1-8epsilon+O(epsilon^2).
Thus log h(gamma)=-8sqrt(gamma)+O(gamma). For FIXED Gamma>0,
n log h(Gamma/n)=-8sqrt(n Gamma)+O(Gamma)->-infinity. The commuting
accepted-map product is exactly h(Gamma/n)^(n/2)exp(-Gamma Pi_e/2).
This refutes that refinement strategy, not every measurement trajectory.

For q=sqrt(rho), the even output amplitude after the LOGICAL equal-X
mixer is sqrt(h)[cos(2theta)-i q sin(2theta)]/2; the odd amplitude is
sqrt(h)[q cos(2theta)-i sin(2theta)]/2. Their squared moduli give equation7.
The total remains h(1+rho)/2 and every accepted basis probability is<=1/4.
Conditional odd parity is[1-((1-rho)/(1+rho))cos(4theta)]/2, minimized
at theta0 (also periodically). The uniform-code D bypass is an allowed
optimum-blind control with four known injected photons. Pointwise ordering
therefore gives the stated fixed-incumbent independent-attempt best law;
it gives no arbitrary changing-incumbent, all-record or equal-clock order.
The diagonal-layer comparison is to uniform on the SAME2^L code states,
not silently uniform on all binom(2L,L) feasible subsets.

For within-pair weights M and cross weights delta>0, the excluded partition
costs4delta while each one-per-pair code partition costs2M+2delta. Hence
M>delta gives the claimed connected counterexample. Exactly one of the
three unordered pairings is bad, probability1/3 under the stated uniform law.
A paid coarsener may use G; any candidate discovered during it is classical
credit. None of the compiler parameters requires C* or a known solution.

Unrolling g gates uses L+2g injected photons and2L+4g modes. Serial reuse
does not restore detected helper photons. Protected helpers measured only
at the end reproduce a fixed herald branch, not active recovery. The4/h
photons-per-success lower bound concerns fresh FOUR-photon injections and
p_success<=h; it must not be transferred to a recovered-data protocol with
different injection costs. Independent uniform detector efficiency supplies
eta^4 only for valid four-detected-photon events under the stated ideal model.

### Section6 typing and branchwise probability

M_theta=Rx(theta) tensor Rx(theta) in section5 acts on logical|xy>.
The physical single-particle matrix is V_theta=Rx(theta) directsum Rx(theta)
on(a0,a1,b0,b1); only Gamma(V_theta) restricted to the code equals M_theta.
Outside the code, remaining data photon number ranges0..4, so a logical
4-dimensional map does not specify the needed Fock operation. The two
numerical4x4 matrices are also unequal: their first-order generators are
X tensor I+I tensor X versus X directsum X. Thus inserting M_theta as the
one-particle data block specifies a DIFFERENT circuit, not a harmless notation.

Once a physical V_f is fixed on all sectors, (V_f directsum I_flags)W_e
does give the correct branch(f,n) probability: the later data operation
commutes with the protected flag projector. For CF input the B expression
is |per U_f[rows,occupied_cols]|^2/(f!*n!); the fully tagged D expression
is per(|U_f[rows,occupied_cols]|^2)/(f!*n!). Both include all assignments
and bunching; no herald denominator or B-Kraus reuse is allowed. Summing
all8-port total4 occupations gives330 records. That tiny exact full-Fock
mirror and the paid four/six-candidate frontier remain mandatory, not free.

## Claim B — exact P122 lemma and application: proved as written

**Primary verdict: PROVED AS WRITTEN** for the111-line clarified P122.
Let W be real, input a fixed normalized Fock state, and flags protected.
For each measured f select V or conjugate(V) on data. For a fixed final
(f,n), commuting the flag projector through the data operation gives its
probability from U_f. With U=(V directsum I)W, U_f is U or conjugate(U).
The repeated-row/column permanent is therefore conjugated, preserving its
squared modulus and every Fock normalization factor. Fully tagged D has
identical entry intensities and labeled-assignment sums. This proves equality
at EACH joint flag/data record, including vacuum/partial-data/wrong-code
branches. Nonzero-event conditioning and common classical decoding preserve
an EXACT equality; no approximate rare-event bound is being misapplied.

P116's W_e is real: all specified preparation/splitter/permutation/attenuator
matrices are real. Intended V_(-theta)=conjugate(V_theta); the same identity
also holds for the literal logical-tensor-as-mode-matrix reading. Accordingly
the specified +/-theta policy has exactly the STATIC +theta terminal count
law under EITHER reading, separately for B and D. A classically annotated
setting label cannot expose a difference in those joint counts. The physical
conditional quantum states/instruments may differ, and actual switching costs
need not equal static costs; neither is identified by this proof.

This is the decisive veto on the proposed adaptive count escape. It does not
repair P116's typing, equalize B with D, prove that failure records never help,
or exclude a different complex/non-conjugate multi-stage instrument. P122
correctly keeps those questions open and requires new specification/review.

## Primary leaves and hardware boundary checked26-Nov-2026

Only selected primary passages were browsed; no external PDF/cache artifact saved.
No retained external source SHA exists. No priority claim follows.

- [Lvovsky/Mlynek quant-ph/0202164v1](https://arxiv.org/html/quant-ph/0202164v1),
  27-Feb-2002, Theory equations2--5: single-photon-assisted conditional BS
  catalysis is established; equation4 models threshold detection, and later
  source vacuum/dark-count terms show why ideal PNR cannot be inferred.
- [Okamoto et al.0905.0074v1](https://arxiv.org/html/0905.0074v1),1-May-2009,
  equation1 gives the exact1/4 even-parity filter with minus sign. The
  experimental paragraph uses four threshold coincidences, contrasting
  intermediate number-resolved heralds. This supports the fixed-point
  attribution, not priority for the entire tunable graph architecture.
- [Official Perceval v1.3 notebook](https://perceval.quandela.net/docs/v1.3/notebooks/Quantum_teleportation_feed_forward.html),
  sectionsII--III: measured-mode configurators are demonstrated on a simulated
  circuit, including a postprocessed CNOT. This is not an installed-API test
  or a certificate for true intermediate Lucy readout/control.
- [Quandela October2025 whitepaper](https://www.quandela.com/wp-content/uploads/2025/10/202510-Quantum-HPC-Quandela-Whitepaper.pdf),
  printed pp7--8,12: PNR/feed-forward are discussed as additional modules and
  in simulation. The dated roadmap neither certifies nor disproves present
  account capability. Source purity, four-photon indistinguishability, flags,
  delays, preparation/empty attempts and real loss still require verification.

Only this review was written. No P116/P122/P110 source or contract was edited;
no import/AST, scientific script, test, native, simulation/DEV, RNG, graph draw,
runner/QPU, manuscript edit or push occurred. The positive objective remains OPEN.
