# P84: exact passive cost-phase obstruction accepted

ROOT read all303+275 author lines and the259-line independent exact-source
review, reconstructed the algebra, and accepts the theorem under the
specified dual-rail physical contract. There is no source correction.
This closes one tempting oracle construction, not all passive optimizers.

| Artifact | Original commit | SHA256 |
| --- | --- | --- |
| `theory/P84_PASSIVE_GRAPH_COST_PHASE_OBSTRUCTION.md` | a47e27533da1ab37c36dc19f7177f5db2fe35630 | cdb0892f3acaec911e732691bad96f33fea0595188dbb5ba21fb86a825b87786 |
| `research/P84_independent_cost_phase_obstruction.md` | 57068159d45b0881960bfa71804a30c826d345f9 | e2098c9948272126612ab0d13c69898a9e0d112600c870b0984add57f5c26a76 |
| `theory/P84_EXACT_HASH_REVIEW.md` | 2b015e640ef8f2abecd0af34009173ba64377280 | de627da750b7eeb62568f886e1488edd0214b663339ccfe5510e94e0751db685 |

ROOT supplied the candidate before the two separate reconstructions. The
exact-source reviewer subsequently read both. These are independent agent
contexts sharing a model/supervisor, not independent discovery or external
refereeing. The sole named mathematical dependency is accepted P81's exact
balanced-feasibility classification, with its frozen7fe0b14f source hash.

## Accepted statement

Let even N>=4 graph vertices be logical qubits on2N physical rails with
N photons, one per pair. Let C(S) be the real undirected weighted cut on
every balanced |S|=N/2 basis vector. A fixed lossless passive net at angle
gamma must send EVERY such vector to exp(i chi-i gamma C(S))|S>, with one
common chi. There are no ancillas, heralds, filters, losses, nonlinearities
or state-dependent circuits. The following are equivalent:

1. Implementations exist for nonzero angles tending to zero.
2. Implementations exist at every angle.
3. The balanced cut cost is constant.
4. Off-diagonal weights have the form w_ij=a_i+a_j for real vertex a_i.

No continuity/differentiability of the physical circuit family is assumed.
For nonconstant cost of range R, no angle0<|gamma|<pi/R is implementable.
The range is an analysis parameter, not an optimum used by an algorithm.

P81 first reduces the exact feasible circuit to local monomial blocks,
pair permutation and optional global complement. All-basis diagonality
forces identity pair action and prohibits that complement, including N4.
Thus f(S)=B*product_(i in S)z_i. Since f(S)=f(S^c), its square is constant;
gamma(C(S)-C(T)) must lie in piZ. A nonzero cost difference then excludes
an accumulating or open angle set. The all-balanced-cut graph identity is
proved by exchanges, four-vertex matching sums and explicit reconstruction
of a_i, with N4 and signed weights covered.

At a SINGLE isolated angle the stronger exact criterion is that the
phase values equal a common phase times parity on an EVEN-cardinality
vertex set. The lattice condition alone is only necessary. Integer-weight
cuts at gamma=pi supply real exceptions: local degree-parity phases work,
even for a nonconstant cost. Zero angle also works for every graph.

The theorem obstructs a specific coherent oracle, not state preparation,
a classical count-driven optimizer or a collision-repair decoder. It does
not establish an approximate-oracle lower bound; P86 is a separate pending
quantitative extension with its own metric and review. Novelty is OPEN.
No experiment, new runtime claim, paper revision or QPU call follows.
