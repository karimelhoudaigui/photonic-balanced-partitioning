# P146-A — Coherent cost interactions with explicitly recyclable branches

27-Nov-2026. MANUAL candidate, shared proposals with ROOT, self-reviewed;
independent review required. Exact base fbefdb4d15120cb550178a83014d59141022939a,
isolated branch research/p146-a-interaction; preceding P145 branch preserved.
Read attachment dd2300f9, P116/P120/P121/P122, P65 diagonal/heralding proof,
P145 receipt and Lucy/TGCC capability notes. No code/import/AST, numerical or
symbolic execution, RNG/test/native/QPU/account access, manuscript or ROOT
register edit. Only this file is added; all previous results/failures stay.

Disposition: a known memory-assisted RUS interaction genuinely changes the
P116 success-only instrument. A derived dyadic cost-phase compiler plus
OFFLINE known-resource recovery admits a conditional linear expected-work
bound below. This is not yet an optimization benefit or novelty claim.
Without the declared memory/interface/readout resources it is not a Lucy plan.

## 1. Recovery criterion and the actual new physical resource

For a resolved branch K on the FULL unknown two-qubit logical space,
K^dagger*K=pI is necessary and sufficient for a proportional unitary.
For recovery by LOCAL unitaries the unitary must itself factor locally.
A diagonal nonzero branch diag(k00,k01,k10,k11) additionally has invariant

    chi=arg(k00)-arg(k01)-arg(k10)+arg(k11) modulo2pi.

Equal magnitudes plus chi0 means local phase gates; unequal magnitudes
mean a filter, even at full rank. Rank collapse cannot be inverted on every
unknown input. Probabilistic inverse filters are different paid instruments.
Unresolved loss channels need their MULTIPLE Kraus operators, not one scalar.

Use two persistent matter qubits A,B with coherent local emission isometries
|x>_A -> |x>_A|a_x>, |y>_B -> |y>_B|b_y>. The four photonic rails are
a0=0,a1=2,b0=1,b1=3. The memory contains the unknown logical amplitudes;
the photons are fresh mediators, not the logical register measured at each
proposal. Coherent emission is a light-matter resource, not passive optics
on a fixed product-Fock input. Logical memory, controls, readout and coherence
time must be counted independently of the two flying photons per attempt.

## 2. Complete four-mode instrument and a failed variable-phase shortcut

Consider the physical unitary, |z|=1,

    U(z)=1/2 [[1,1,1,1],[1,z,-1,-z],
              [1,-1,1,-1],[1,-z,-1,z]].

Its rows can be written U_(j,a_x)=(-1)^(t_j*x)/2 and
U_(j,b_y)=b_j*(-1)^(t_j*y)/2, with
(t0,t1,t2,t3)=(0,1,0,1), (b0,b1,b2,b3)=(1,z,-1,-z).
Normalized two-photon Fock amplitudes give ALL TEN lossless PNR branches:

| Observed count | Memory Kraus K, basis 00,01,10,11 |
|---|---|
| Two photons at j (four records) | b_j*(Z_A Z_B)^t_j/(2sqrt2) |
| Coincidence 0,2 or1,3 (two records) |0|
| j in{0,2}, k in{1,3} (four records) | (b_j/4)*(Z_A+v Z_B), v=b_k/b_j=+z or-z, twice each |

The sqrt2 in bunching is the OUTPUT factorial normalization, not a label
average. Every bunch branch is a recoverable local unitary with probability
1/8. Cross branches satisfy K^dagger*K=(I+Re(v)Z_AZ_B)/8.
Their sum is I/2; bunch branches sum to I/2: the instrument is complete.

For a cross branch, equal singular values hold iff Re(z)=0. At z=+i,
each cross branch is, up to a global phase,
`(S tensor S^dagger)CZ/(2sqrt2)` or
`(S^dagger tensor S)CZ/(2sqrt2)`, S=diag(1,i).
After known local correction, four records give CZ with TOTAL probability
1/2; four bunch records restore the input with TOTAL probability1/2.
At z=-i the roles/phases exchange. Coarse-graining identical operators up
to global phase gives four branches I/2,ZZ/2,L+*CZ/2,L-*CZ/2.

For z!=+/-1, the cross ratio is

    k00*k11/(k01*k10)=((1+v)/(1-v))^2,

negative real for v on the unit circle. Thus chi remains pi, not a tunable
weak cost phase. Away from +/-i the singular values become unequal; at
z=+/-1 the cross map has rank2. Merely turning this phase knob recreates a
parity filter and cannot be declared a locally correctable RUS gate.
The formal identity `(Z_A+zZ_B)(Z_A-zZ_B)/16=(1-z^2)I/16` is only a
POSTSELECTED two-branch inverse, not deterministic recovery or free retries.
The z=i DFT4 primitive is established RUS physics; the table is reconstructed
here to expose all branches, not claimed as a new gate.

## 3. Uniform loss: the branches that a memory does not magically erase

Model common per-photon transmission/detection eta AFTER ideal coherent
emission, independently and uniformly on the four rails, before U(z).
Uniform attenuation can be moved through the passive analyzer. Source
encoding failures, dark counts and nonuniform loss require separate models.
Put M_(A,r)=diag(U_(r,a0),U_(r,a1)), and similarly M_(B,r).
Besides eta*K_n for all ten two-detection records, the complete instrument is

    L^A_(r,y)=sqrt(eta(1-eta))*M_(A,r) tensor |y><y|,
    L^B_(r,x)=sqrt(eta(1-eta))*|x><x| tensor M_(B,r),
    L^0_(x,y)=(1-eta)*|xy><xy|.

There are four observed one-photon ports r, with four unresolved Kraus
operators per port, and one vacuum record with four Kraus operators.
Two-photon, one-photon and vacuum masses sum respectively to eta^2,
2eta(1-eta),(1-eta)^2 for every input. All FIFTEEN raw PNR records remain.
Loss transfers a logical label to the environment and dephases the relevant
memory; preserving the physical spin is not preserving its quantum state.
These projected/dephasing maps are not unitary recovery of arbitrary data.
PNR or an equivalent loss flag is essential: a threshold one-click bunch
record is ambiguous with a lost photon and is not a certified benign repeat.

At z=i define tau=eta^2. A microattempt has corrected CZ success tau/2,
benign repeat tau/2 and loss1-tau. For ARBITRARY UNKNOWN data, if any loss
aborts, eventual success before loss is r=tau/(2-tau); expected attempts
until success OR loss are c=1/(1-tau/2). With at most R microattempts,
success probability is r*[1-(tau/2)^R], and timeout mass is (tau/2)^R.
For g such gates with whole-run abort and no code/recovery, completion is
r^g. This is a model-specific LOSS penalty, not a no-go for recovered raw
outputs. At eta1, r1,c2: benign heralds alone no longer cause a 2^-g penalty.
Finite caps, timeout/loss output and all emitted photons still count.

## 4. A genuine continuously weighted cost phase from a coherent ancilla

ROOT proposed this next gadget; the signs and all stages are reconstructed.
Take an additional MEMORY ancilla cos(theta)|0>+sin(theta)|1>, apply native
RUS-CZ(a,u) then RUS-CZ(a,v), and measure ancilla in the Y basis. If both
native gates complete, the data instrument is

    K_(+Y)=(cos(theta)I-i sin(theta)Z_uZ_v)/sqrt2,
    K_(-Y)=(cos(theta)I+i sin(theta)Z_uZ_v)/sqrt2.                    (1)

Both outcomes are proportional UNITARIES with probability1/2 for arbitrary
data, including entangled inputs. This is a real effective two-occupation
interaction; its chi is +/-4theta. The non-Clifford resource has moved to
coherent ancilla preparation/measurement, which must not be supplied for free.
All native byproducts must be corrected/tracked before the Y measurement.

For theta=pi/2^(m+1), integer m>=1, request +theta. Upon the wrong sign,
use a fresh ancilla for angle2theta, then4theta, etc. After k wrong signs
the accumulated data phase is -(2^k-1)theta. At stage m the angle is pi/4;
its wrong sign differs from the desired result by -pi/2, corrected by iZ_uZ_v.
There are at most m phase gadgets, not an unbounded angular random walk.
Native benign RUS failures remain microattempts with the above loss model.

Let a=r^2, q=a/2, using the stipulated TWO-CZ compiler at EVERY stage.
Each completed nonterminal gadget either succeeds or continues with probability
a/2; terminal completion accepts both Y outcomes. Hence

    S_m(a)=sum_(k=1..m-1)q^k+2q^m,
    E[N_gadgets]=sum_(j=0..m-1)q^j,
    C_m:=E[N_microattempts]=c*(1+r)*sum_(j=0..m-1)q^j.              (2)

These are success-before-loss and UNCONDITIONAL work until success/loss.
The second native CZ is attempted only if the first succeeds before loss,
probability r. This proves its factor1+r without pretending every gadget
always pays two completed gates. All native attempts emit TWO photons.
The terminal pi/4 phase can alternatively use one CZ plus local phases;
that is a better DISTINCT compiler, not silently substituted into (2).
General angles/weights need their actual dyadic compilation and error budget;
(2) does not assert free exact preparation of arbitrary real rotations.

For a logical cut cost, x_i=(1-Z_i)/2 gives
exp[-i gamma*w*(x_u XOR x_v)] equal, up to global phase, to
exp[+i gamma*w*Z_uZ_v/2]. Thus theta=gamma*w/2 uses only public weights,
never an optimum. Local fields are additional one-qubit Z rotations.
Pair-code choices select one of two vertices per bit, guaranteeing balance
within a restricted2^n code, not the full binomial bisection space. The P116
support counterexample still applies. A full vertex register instead needs
a cardinality-preserving logical mixer. Cost phases alone followed by Z
measurement do not improve the initial classical distribution (P65).

## 5. Recycling LOSS for an OFFLINE known weighted resource, not unknown data

Let the data resource initially be |+>^n, with a known partial weighted graph
state product_(e built)exp(i theta_e Z_uZ_v)|+>^n. Native CZs and all tracked
byproducts are diagonal; during a macro only its ancilla and endpoints u,v
are additionally involved. A loss may occur during either CZ or after wrong
intermediate signs. Abort that macro, measure ancilla AND u,v in Z, apply
known neighbor rotations, and reset deleted sites to |+>.

Why recovery is exact on the REMAINING sites: conditioning on z_u,z_v turns
every incident phase exp(i theta Z_uZ_w) into a known one-qubit rotation on w.
All temporary phases on uv and ancilla-endpoint edges become scalars. The
loss Kraus operators above are diagonal/projective on these same sites; after
their Z measurements, unobserved environment labels only change scalar weights.
Every surviving conditional state is the SAME induced weighted graph state
with known local rotations, even if the initially lost photon was unidentified.
No H or other noncommuting DATA gates may have intervened. Arbitrary unknown
algorithmic input does not have this replaceable-known-resource guarantee.

Fix a SIMPLE target resource graph with g>=1 edges and maximum degree Delta>=1.
Every macro targets a MISSING edge; select by any supplied paid rule, never C*.
Let W count only correctly completed target edges; temporary wrong phases
are not counted. If the macro succeeds, W increases by1. If it loses a photon,
purging its endpoints removes at most b=2(Delta-1) correct edges: the targeted
uv edge was missing. Other correctly built edges and memory nodes are retained.

For targets with respective m_e, put S_*=min_e S_(m_e)(a), C_*=max_e C_(m_e).
Assume ideal coherent memory, deterministic declared ancilla/Z/Y preparation,
readout/reset/corrections, exact gate model and conditional loss probabilities.
Before completion the expected increment satisfies

    E[Delta W | history] >= delta:=S_*-b*(1-S_*).

If delta>0, stop at T when all g edges are complete. Since W_(t wedge T)<=g,
telescoping conditional expectations gives
`delta*E[t wedge T]<=E[W_(t wedge T)]-W0<=g-W0`.
Monotone convergence proves

    E[T] <= (g-W0)/delta,
    E[N_microattempts] <= C_*(g-W0)/delta.                          (3)

For the second bound, charge each reached macro its conditional EXPECTED
work C_e; summing those charges needs no independence from its success.
Gate-mediated photon injections are twice this number. Purge/readout/reset,
ancilla preparation, idle-memory time, setup and final transfer/readout are
ADDITIONAL paid costs. With a supplied finite per-macro bound on those costs,
their expected total has the same multiplier. No device rate is inferred.
An explicit cap t_max has timeout probability at most (g-W0)/(delta*t_max);
timeouts/partial resources remain recorded, not renormalized as successful.

For each fixed Delta and finite angle set, eta sufficiently near1 makes
S_* near1 and delta positive: this is a nonempty conditional resource window.
Indeed S_m(a)>=a/(2-a) for all m, so a>2b/(1+2b) suffices uniformly in m;
precision/control costs still depend on angle representation. These are
coarse sufficient bounds, not optimal thresholds or a calibrated Lucy claim.
This removes the product-of-all-gates survival assumption by LOCAL pruning,
not by declaring lost unknown data recoverable. Offline graph-resource
recycling is established prior art; novelty of this elementary bound is unassessed.

The native microattempt loops used in (2) are an EXPECTED-work idealization.
A bounded implementation caps each native gate at R microattempts and purges
the macro's ancilla,u,v on either loss OR timeout. Substitute throughout
`r_R=r*(1-(tau/2)^R)`, `c_R=c*(1-(tau/2)^R)`, `a_R=r_R^2`.
The same drift proof applies when its NEW delta_R is positive. With at most
t_max macros, microattempts are at most2*m_max*R*t_max and raw gate photons
at most4*m_max*R*t_max; non-gate preparation/readout photons remain extra.
This supplies finite physical algorithm limits, not retries of a failed
scientific run. No cap or timeout outcome is removed from the ledger.

## 6. Decisive controls, exact scope of the escape, and hardware gate

Fully D must be modeled on the matter-photon instrument. For j!=k its two
unresolved labeled assignments are PRODUCT memory Kraus operators
`diag(U_(j,a_x)) tensor diag(U_(k,b_y))` and its j/k-swapped partner.
They add INCOHERENTLY. For bunch jj use the one product with NO sqrt2.
Thus a D retuning of this local-emission/tag-preserving optical architecture
has separable conditional maps and cannot create CZ|++> from product memories.
The two coincidences suppressed in B are generally NONZERO in D and must
have an explicitly defined controller action. A scalar replacement of the
already successful logical CZ is invalid (P120). This proves a physical
resource contrast, not optimization superiority against classical computation.

A group of TWO identical flying photons PER MICROATTEMPT reproduces the
entire B memory instrument, including loss/recovery; distinct microattempts
never interfere optically. By induction its whole joint record/memory process
matches B even when the memory register is entangled. Therefore this route
CANNOT claim B superiority over that group2 control. Such a control is now
a quantum computational resource, not automatically a classical null. No
previous group2/3 acceptance condition is silently waived by changing models.

Clifford-only CZ/S/H/Pauli preparations and measurements have a stabilizer
mirror. The non-Clifford ancilla/weighted phases in (1) escape THAT premise,
but small registers still require exact state/channel simulation, and larger
ones require strong tensor/stabilizer-rank and classical feasible-search
controls with identical weights, pairing/block features and scored candidates.
Useful noncommuting cost dynamics, matched total costs, labels/seeds/held-out
graphs and independent replication remain UNPROVED. A nontrivial chi or
polynomial resource preparation alone does not supply the missing gain sign.

One weighted ZZ layer on |+> followed by local Rx, with bounded resource
degree Delta, also has a classical CUT-MEAN evaluator: a two-site cost term's
backward observable uses at most2(Delta+1) sites, so direct local contraction
costs O(g*2^O(Delta)). Include this control if optimizing mean cut; it is not
a sampler theorem or a decomposition of the GLOBAL clipped-improvement tail.

P121/P65 no-recovery caps do not apply to the locally recycled instrument as
stated. P122's conjugate-count shortcut is not a theorem about this retained
memory channel. P145's measured tiny kernel omits its growing quantum memory;
its herald counts here are themselves easy to simulate and prove no gate.
P143's fixed-CF common-spatial deterministic-null hypotheses are not granted
for the joint coherently encoded matter/flying system. None of these facts
invalidates the original scoped results or proves a general quantum advantage.

Required physical capabilities: coherent stationary memories, emission that
preserves memory amplitudes, controllable ancilla rotations and local data
phases, complete PNR/loss flags, repeated conditional emission and correction,
Z/Y memory readout/reset, calibrated eta and coherence across the whole capped
preparation. Photonic delay loops instead incur their own storage losses.
docs/LUCY_TGCC.md and QPU_COMPATIBILITY.md verify NONE of this stateful
interface; a universal MODE unitary is not a universal LOGICAL gate service.
No login/job or contact with Laurent is authorized or performed here.

## 7. Bounded primary verification and next falsifier

Official version histories and the passages below were read, not just abstracts.
No source artifact was retained (SHA256 NONE), no cache/ledger/manuscript edited.
Searches targeted KLM, RUS/memory/loss and stabilizer controls, not global priority.

| Primary source | Read passages and limited transfer |
|---|---|
| Knill--Laflamme--Milburn, [quant-ph/0006088v1](https://arxiv.org/pdf/quant-ph/0006088v1),20-Jun-2000 | Introduction p1; VI.A--B pp3--4; VI.D p5. Teleportation/resource construction and known computational-basis failure measurements are established; they do not make every failed gate locally unitary. |
| Lim--Beige--Kwek, [quant-ph/0408043v4](https://arxiv.org/pdf/quant-ph/0408043v4),20-Apr-2005 | pp2--3 Eqs2--15 and Figure2: stable source qubits, double encoding, four corrected branches, DFT4 rail mapping. The z=i primitive is known after notation translation. The body's generated date is not the arXiv revision date. |
| Wein et al., [2412.08611v2](https://arxiv.org/pdf/2412.08611v2),19-Dec-2025 | II.A.4/Figure2 pp3--4; AppendixH pp20--22/Figure10. Hybrid spin memory, hardware feed-forward, loss dephasing and partial graph-resource recovery are explicit. This is NOT a statement of today's Lucy API or of our optimization performance. |
| Aaronson--Gottesman, [quant-ph/0406196v5](https://arxiv.org/pdf/quant-ph/0406196v5),18-Jun-2008 | II/Theorem1 p3 and III pp3--4: tableau simulation supplies the Clifford control. Arbitrary non-Clifford phase gadgets are not covered by that restricted theorem. |

Authentication/extraction: VERIFIED within these passages. Application of the
new formulas requires their explicit ideal memory/loss/representation premises.
Known RUS/recycling/stabilizer ingredients are not rediscovered novelty; the
coherent weighted-resource composition and bound(3) await external priority
checking and independent proof review. No positive scientific goal is closed.
First falsifier: reconstruct ALL Kraus branches and the purge/drift invariant,
including incomplete wrong-sign phases and every loss record. Any branch
that cannot be reset with the stated induced-resource remainder breaks (3).
Only then consider a bounded exact channel check under NEW authorization.
No numerical campaign or claimed optimizer is authorized by this note.
