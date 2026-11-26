# P146-A supplement — weighted graph resources and local recycling prior art

27-Nov-2026; bounded PRIMARY-source verification, literature-check workflow.
Branch `research/p146-c-digital-lucy`; parent P146-C171 remains unchanged.
No source cache/download retained, code, import, experiment, RNG, hardware/API
call, credential access or manuscript/register change. This is an attribution
and hypothesis-translation check, not an independent audit of ROOT's full lemma.

**Disposition:** non-Clifford parity-phase graph resources, dyadic sign
correction, and local recovery of incomplete Clifford graphs are known.
The precise weighted-loss/recycling/drift composition below is **unverified
as prior art within this bounded search**, not certified new. None of these
sources authenticates stationary-spin memory or these operations on Lucy.

## Exact claim being compared and notation dictionary

ROOT's resource is `exp(i sum_(u<v) theta_uv Z_u Z_v)|+>^n`, with known
local Z rotations recorded. In the PAIR-CODE mapping each logical bit picks
one vertex of `(u_j,v_j)`: `x_u=(1+Z_j)/2`, `x_v=(1-Z_j)/2`. Then

    C_G=C0-sum_(j<k) J_jk Z_j Z_k,
    J_jk=(w_uu+w_vv-w_uv-w_vu)/2.

An intrapair edge is constant. This covers only partitions selecting one
vertex per pair, not all balanced partitions. Logical RX mixing is a single
rail-pair rotation in this encoding. A weighted ZZ interaction is still
needed for the cost; known initial |+> preparation is not a solution oracle.
Paid classical paired-Ising search and unrestricted bisection remain controls.

The proposed mediator is `cos(theta)|0>+sin(theta)|1>`, coupled by two known
CZs to u,v and measured in Y. For `|+y>=(|0>+i|1>)/sqrt(2)`, the Kraus map
is `exp(-i theta Z_u Z_v)/sqrt(2)`; relabeling outcomes gives either sign.
Wrong signs require doubled-angle correction. A finite dyadic ladder has a
last stage whose two signs differ by a known local Pauli. This sign convention
and terminal condition must be pinned before assigning a stage count m.

The proposed loss model uses pair-survival `tau=eta^2`, a RUS-CZ completion
probability `r=tau/(2-tau)`, two-CZ stage survival `a=r^2`, and

    S_m=sum_(k=1)^(m-1) (a/2)^k + 2(a/2)^m.

Its missing-edge construction purges a,u,v after destructive failure and
retains other correctly weighted edges. For target degree at most Delta,
`delta=S_min-2(Delta-1)(1-S_min)>0` is the proposed progress certificate.
No source below is cited as proving these exact formulas or all their premises.

## Authenticated primary leaves and their actual guarantees

**1. Wein et al. — directly relevant existing Clifford recycling.**
[2412.08611v2](https://arxiv.org/html/2412.08611v2), 19-Dec-2025;
*Minimizing resource overhead in fusion-based quantum computation using hybrid
spin-photon devices*, PRX Quantum 6,040362 (2025), DOI10.1103/8l5g-x3b7.
Read §§II.1.4, B.3 and Appendix H, particularly its Erasure logic and Fig.10.
Sources store partial graphs; a loss triggers local Z measurements/reset,
and some completed subgraphs/extra edges survive for later attempts. Failed
generation periods need not reset unfinished resources. **Known after
translation of notation** for partial reuse, rather than global restarting.
B.3 also states that its RUS CZ acts on arbitrary spin states, not just graph
states, with correctable identity failures; detectors resolve at least two
photons. H models a particular staged Clifford resource and uses Monte Carlo,
not a theorem for arbitrary weighted graphs. It assumes a feed-forward clock
and fast single-qubit operations. Its timing assumptions are not ours by default.

**2. de Gliniasty et al. — physical spin-memory primitive, not Lucy access.**
[Published Quantum 8,1423](https://quantum-journal.org/papers/q-2024-07-24-1423/),
24-Jul-2024, *A Spin-Optical Quantum Computing Architecture*;
associated [2311.05605v5](https://arxiv.org/html/2311.05605v5), 17-Jul-2024.
The checked §§1–2 and Fig.1 place physical information in emitter spins;
emitted ancilla photons interfere and are detected, with routers and PNR
detectors in the architecture. **Partial or adjacent result only** for
the requested hardware: an ordinary deterministic single-photon source is
not automatically an accessible spin qubit. The browser rejected the 12-MB
arXiv PDF and its HTML stops during §2; later sections/appendices were NOT
verified here. The precise dephasing instrument is therefore a separate leaf,
not proved by a publisher abstract or these checked introductory sections.

**3. Kissinger–van de Wetering — weighted non-Clifford resources and correction.**
[1704.06504v3](https://arxiv.org/pdf/1704.06504v3), 16-Apr-2019 (PDF dated
17-Apr); *Universal MBQC with generalised parity-phase interactions and Pauli
measurements*, Quantum 3,134 (2019), DOI10.22331/q-2019-04-26-134.
§1 pp.2–3 defines `P(alpha)=exp(-i alpha ZZ/2)` graph edges; non-Clifford
angles give non-stabilizer resources. Repeated edges add angles. §7 pp.16–18
explicitly corrects sign errors through successively doubled dyadic angles
until a known Pauli remains. Thus ROOT's `theta=-alpha/2` resource notation
and sign-doubling ingredient are **known after translation of notation**.
The paper supplies deterministic MBQC patterns once their resource is available;
it does not establish this lossy two-CZ mediator, local-purge policy or S_m.
Its own backward references also preclude treating weighted graph resources
as a newly introduced concept here; this note does not claim earliest priority.

**4. Lim–Beige–Kwek — the original stationary-qubit RUS contract.**
[quant-ph/0408043v4](https://arxiv.org/pdf/quant-ph/0408043v4), 20-Apr-2005;
*Repeat-Until-Success Quantum Computing*, associated PRL95,030505 (2005).
Read pp.1–3, Eqs.(2–12): arbitrary stored two-qubit input, emitted time-bin
photons, two entangling and two local-correctable outcomes, each probability
1/4 in the ideal model; mean two rounds for CZ. **Known after translation**
for preserving spin data through ideal retry outcomes, **partial or adjacent**
for photon-loss recycling and arbitrary weighted resource construction. It
does not grant nondestructive reuse of flying photons or an account API.

## What transfers by algebra, and what still needs its own proof

The weighted pruning identity is a **formal corollary not stated in these
checked passages**, conditional on actual Z measurements of deleted vertices.
For `A` deleted, observed eigenvalues `z_i=±1`, and retained set B,

    <z_A|psi> = 2^(-|A|/2) e^(i constant)
      [product_(j in B) exp(i Z_j sum_(i in A) theta_ij z_i)]
      exp(i sum_(j<k in B) theta_jk Z_j Z_k)|+>^B.

Hence retained edge weights are unchanged and neighbor Z rotations are known.
Z dephasing on nodes subsequently Z measured does not change this normalized
conditional state. Tracing an unmeasured failed node is NOT the same pure-state
certificate. For generic weights these byproducts are arbitrary Z rotations,
so a Clifford/Pauli frame alone is insufficient unless their angles permit it.
Unmodeled coherent or non-diagonal damage to retained spins is outside this arrow.

With that instrument and fixed m, Delta, eta and a uniformly positive delta,
an elementary bounded-progress stopping argument gives expected macro count
at most `|E|/delta`: apply conditional drift to the correct-edge count stopped
at completion and then take the finite-truncation limit. Primitive RUS rounds,
ancilla preparation and readout/reset need controlled expected costs; storage
errors must also satisfy the instrument premise. Initial preparation/output
costs at least O(n), separately from this edge-macro count. This is a conditional
composition argument, not a theorem quoted
from Appendix H, nor a worst-case time bound. Constants need not stay bounded
if precision/depth or loss scales with graph size. Without the drift premise,
this argument proves no efficient construction. Conversely, assuming a global
all-gates-survive factor `r^g` would discard the explicitly allowed local reuse.

Search coverage: existing local records first; named Wein/SPOQC/Lim sources;
bounded weighted-graph/phase-gadget and loss/recycling queries, plus the checked
parity-phase paper's related-work/correction passages. No full citation closure,
independent novelty search or all-current-literature review. No exact external
weighted-recycling/drift theorem was authenticated; that is an OPEN attribution
question, not evidence of discovery. This route concerns resource preparation,
not a proven optimization advantage, practical throughput or verified Lucy service.
