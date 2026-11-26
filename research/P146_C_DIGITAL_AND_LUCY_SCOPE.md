# P146-C — cardinality-preserving logical cost and Lucy capability scope

27-Nov-2026; STATIC primary-source check and hand derivation only.
Isolated branch `research/p146-c-digital-lucy`, base
`fbefdb4d15120cb550178a83014d59141022939a`; the previous agent branch is retained.
No API/account query, token, job, simulation, RNG, test, source change or manuscript edit.

**Disposition:** a graph-dependent logical ZZ phase with logical XY mixing is
a concrete change from P145's passive one-particle proposal. Its algorithmic
framework is already known. Lucy is publicly advertised as universal; the
account-accessible, all-branch implementation needed here is NOT established.
The first bridge is a specified physical logical gate, not an optimizer pilot.
No positive signal, hardware impossibility or novelty certificate follows.

## Public Lucy facts versus an executable gate contract

Primary pages checked directly on 27-Nov-2026, after consulting the existing
`reports/LUCY_P132_PUBLIC_CAPABILITY_CHECK.md`, P140 capability record and
`docs/LUCY_TGCC.md`. Live pages are dated observations, not immutable editions.

| Primary source and locator | What it establishes | Missing implication |
| --- | --- | --- |
| [Quandela Lucy](https://www.quandela.com/qpus/lucy/), Technical Specifications and gate-fidelity panels | MOSAIQ-12; 12 data qubits, 24 modes, all-to-all topology, universal chip, listed SDKs; vendor reports 2-qubit fidelity 99.0±0.8% and six fully entangled qubits | Neither 24 logical qubits nor an arbitrary-depth fault-tolerant gate machine; panels do not specify our accessible heralding, compilation or failure interface |
| [CEA delivery announcement](https://www.cea.fr/presse/Pages/actualites-communiques/ntic/quandela-livre-lucy-ordinateur-quantique-TGCC.aspx), 23-Oct-2025, introduction | Delivered universal digital photonic machine with 12 qubits at TGCC | An earlier upgrade roadmap is not evidence of an already accessible 24-qubit system |
| [TGCC public stack](https://www-hpc.cea.fr/tgcc-public/en/html/toc/QuantumSoftwareStack.html), build 2026-09-08.1512, Lucy Hardware; Using Lucy | Up to 12 photons in 24 fibres; Irene/myQLM access; Perceval `BasicState`, beam splitter, `Experiment`, terminal `sample_count`; per-platform specifications are separately retrieved | This example is not a logical ZZ/XY gate contract or permission to query the account |

The TGCC example contains a minimum-detected-photon filter and separate sample
and shot limits. It does not expose the complete source-pulse/failure ledger.
Its indicative average transmittance 2% is neither a certified spectral-loss
bound nor a current calibration. Earlier CNOT examples on this page run on
Qaptiva/local simulation; their presence does not authenticate a Lucy gate.

[Perceval v1.3 feed-forward configurators](https://perceval.quandela.net/docs/v1.3/reference/components/feed_forward_configurator.html),
introductory example and class contracts, model measured classical modes,
conditional circuits and a mandatory default branch; the example uses SLOS.
[Computer v1.3](https://perceval.quandela.net/docs/v1.3/reference/runtime/computer.html),
introduction/SimulatedComputer/available parameters, distinguishes simulation
from remote acquisition and platform-specific features. A model API does not
certify Lucy support for every model component. No remote object was created.

Thus passive coupler/phase programming and terminal sampling have a public
interface example. The checked sources do not settle our account's ancilla
injection/routing, actual PNR versus threshold/pseudo-PNR, intermediate
herald access, surviving-data delays/memory, intrashot conditional switching,
logical entangling-gate compilation or raw all-branch reporting. These remain
**unverified**, not absent. The product's no-decoherence slogan does not supply
a lossless, indefinitely stored data-qubit primitive. Its all-to-all topology
does not identify spare hardware coupler qubits available to an experiment.

## Precise changed logical mechanism and a hand-checkable gate witness

Use four dual-rail logical qubits: eight data modes, four data photons, one
photon per pair; a logical bit is `x_i=n_(i,1)`. Restrict to `sum x_i=2`.
For public nonnegative graph weights, define

    H_C(G)=sum_(i<j) w_ij (1-Z_i Z_j)/2,
    H_XY,ij=(X_i X_j+Y_i Y_j)/2.

Both commute with logical Hamming weight. A paid basis warm start followed by
a nontrivial XY preparation, `exp(-i gamma H_C)`, then an XY mixer defines
a feasible proposal. A cost phase applied to a basis state alone changes no
count law. A connected logical mixer graph can connect the fixed-weight
basis, although a single disjoint-pair mixer has only its smaller orbit.
All graph weights/features and prepared candidates are available to controls;
neither optimal masks nor C* enters preparation, parameters or acceptance.

The cost term includes `exp(+2i gamma w_ij n_(i,1)n_(j,1))` after local phases.
This is a quartic photonic interaction on the code, rather than a quadratic
one-particle Hamiltonian. Logical XY on two encoded qubits is likewise not
automatically a physical beam splitter between rails: code leakage matters.

For an exact, intentionally easy witness, prepare

    |psi0>=(|10>+|01>)_12 (|10>+|01>)_34 / 2.

The two Bell preparations are charged logical operations/resources, not a
free collision-free photon input. On its four-dimensional support put
`u=x_1`, `v=x_3`. For the single public edge `{1,3}` of weight one,
`C=u xor v=(1-Z_u Z_v)/2`; the cost phase has diagonal
`(1,e^(-i gamma),e^(-i gamma),1)`. Its cross ratio is `e^(2i gamma)`;
unless `gamma` is a multiple of pi it cannot factor into two local diagonal
phases. This excludes that local-phase replacement, not every measured
passive realization or classical sampler. At `gamma=pi/2` it is CZ times
known local phases. The logical pair mixers act as
`M=exp[-i beta(X_u+X_v)]`. Direct Pauli conjugation gives

    <Z_u Z_v> = -sin(4 beta) sin(gamma),
    E C = [1+sin(4 beta) sin(gamma)]/2.

Indeed `M† Z M=Z cos(2 beta)+Y sin(2 beta)`, while the cost conjugates
`Z_u Y_v` to `Z_u Y_v cos(gamma)-X_v sin(gamma)` and symmetrically.
At `beta=-pi/8,gamma=pi/2` the ideal mean is zero. A classical assignment
also attains zero immediately; all six balanced four-bit cuts are cheap.
This is a phase/mixer witness, not an optimizer benchmark or new QAOA result.

## Known primary ingredients and the exact transfer boundary

- Hadfield, Wang, O'Gorman, Rieffel, Venturelli and Biswas,
  [1709.03489v2](https://arxiv.org/pdf/1709.03489v2), 28-Feb-2019 revision
  (PDF dated 1-Mar); *From the Quantum Approximate Optimization Algorithm to
  a Quantum Alternating Operator Ansatz*, Algorithms 12,34 (2019), Appendix
  A.3.2, printed p.38: minimum bisection uses fixed-weight basis, ZZ cost
  phases and ring XY mixers. **Known after translation of notation** for
  the mechanism above; gamma/sign/XY-factor conventions are rescaled. Its
  qubit gate counts do not include this photonic encoding/heralding overhead.
- Knill, Laflamme and Milburn, [quant-ph/0006088v1](https://arxiv.org/pdf/quant-ph/0006088v1),
  20-Jun-2000, *Efficient Linear Optics Quantum Computation*, §§III–VI;
  associated Nature 409,46–52 (2001), DOI10.1038/35051009. §V Eq.(8) gives
  a heralded nonlinear-sign operation of ideal success 1/4; two such gates
  give controlled sign with success 1/16. Each uses a single-photon plus
  vacuum ancilla and number-sensitive herald. **Known after translation**
  for a possible gate ingredient, conditional on the stated resources.
  One such cost CZ on four data qubits has six photons/twelve modes in this
  elementary construction; Bell preparation, mixers, loss and further gates
  are additional. This partial count does not establish that the full circuit
  fits Lucy, that generic angles are exposed, or that failures preserve data.
- Lim, Beige and Kwek, [quant-ph/0408043v4](https://arxiv.org/pdf/quant-ph/0408043v4),
  20-Apr-2005, *Repeat-Until-Success Quantum Computing*, pp.1–3, Eqs.(1–12);
  associated PRL95,030505 (2005). Qubits reside in stable source ground states;
  emitted photons are measured, and unsuccessful ideal branches leave a
  locally recoverable stationary-qubit state. **Partial or adjacent result**:
  this is not a repeat-until-success contract for destructively measured
  flying Lucy data photons. Loss/error recovery also needs its own contract.
- Dürr and Høyer, [quant-ph/9607014v2](https://arxiv.org/pdf/quant-ph/9607014v2),
  7-Jan-1999 revision, *A Quantum Algorithm for Finding the Minimum*, Th.1,
  algorithm and final remarks: O(sqrt(N)) probes with success at least 1/2,
  amplified to 1-2^(-c) with O(c sqrt(N)) query-model work. Its stated timing
  conventions count a search iteration as one step and omit some classical
  work. **Conditional** for P65-C: coherent reversible comparison/marking,
  uncomputation, feasible-superposition preparation and reflections must be
  implemented and charged. A classical cut lookup or heralded shot is not
  automatically that oracle; this is not a physical speedup guarantee.

## First bridge, strongest controls, and stop condition

Require an all-sector instrument for the declared logical gate: accepted
Kraus maps equal a known scalar times the desired unitary on all declared
code coherences, and ALL other Kraus branches complete a trace-preserving
physical process. Record fresh helpers, source preparation, unused ports,
detectors, herald misclassification, code leakage, loss, delays, feed-forward,
resets and compilation error/cost. Destructive failures require new data;
RUS requires an explicit recoverable failure map and surviving memory.
Terminal postselection alone does not certify composable intermediate gates:
leakage paths can return to the code later. If only one final measurement is
available, assess that entire unrolled circuit and every failed attempt.

P116's successful nonlinear filter is not this unitary cost phase; its real
prefix/plus-minus feedback count null (P122) cannot supply it. P65-C already
requires an honest oracle/heralding specification. P145's fixed three-photon
one-body kernel mirror does not literally cover the ideal quartic logical
gate, but a compiled constant-size passive/measurement circuit still admits
fixed-photon exact controls; P143's weak-instrument premises must be checked.

The first decisive classical veto is exhaustive feasible enumeration and an
exact four/six-dimensional logical simulator with independently optimized
parameters and identical public graph features; preparation and compiler
search are paid. Then use full physical fixed-Fock/all-branch simulation,
independently retuned D/proper species including ALL helpers, and classical
local/multiswap/tempering controls at growing size. D is the tagged physical
instrument with unresolved tags, not B's ideal successful CZ Kraus supplied
for free. An abstract nonphotonic digital gate has no automatic D definition.
Count all failed attempts, photons, data resets, source/host/communication
time and every scored candidate. Conditional quality or query count alone
cannot pass the total-resource gate. No physical instrument means DEFER;
classical dominance means reject the scoped optimizer candidate.

Coverage: named primary editions, their located passages and current official
capability pages; existing local overlap records checked first. No exhaustive
priority search, confidential slide use or source download/cache was needed.
Exact formulas here are hand derivations, not measured gate results. Hardware
availability, practical benefit and any new composition's novelty remain OPEN.
