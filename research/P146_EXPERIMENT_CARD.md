# P146 — change the physical model before another optimizer campaign

27 November 2026. Base `fbefdb4d15120cb550178a83014d59141022939a`.
Original goal remains OPEN. Paper, main and QPU execution stay frozen.

## Competing hypotheses and decisions before execution

**A: retained memory plus measurement-induced cost interactions.** Fresh
mediator photons interfere while logical amplitudes remain in a quantum
register. A non-Clifford ancilla supplies a genuinely weighted ZZ gate.
Benign native failure is corrected and retried; photon loss is NOT harmless.
For an OFFLINE known weighted graph resource, Z measurement/reset of failed
endpoints can preserve the correctly prepared induced graph. This escapes
P145's fixed-size measured-proposal memory premise and a whole-run-restart
loss model. It adds coherent memories, an emission interface, ancilla control,
PNR, conditional readout/reset, rotations and storage time as PAID resources.
None of that interface is authenticated on the actual Lucy account.

The possible positive is a conditional resource-preparation statement, not an
optimizer. For degree Delta, bounded native retry cap R and dyadic edge phases,
the proposed drift is `delta=S_min-2(Delta-1)*(1-S_min)`. If positive, expected
edge macros are at most `g/delta`, with separately charged physical costs.
The mathematical note and independent audit, rather than a finite test count,
must establish that statement. Known RUS/weighted graphs/recycling are prior art.

**B: retain collisions with balanced parent-majority decoding.** The complete
tritter law has a useful third-order term and collision contributions, but
direct classical majority and a distinguishable monomial circuit defeat the
small construction. Single-bit-mutant libraries cannot escape a one-bit local
minimum at any photon number. Reject those optimizer routes without a scan.
Growing, overlapping libraries have no useful-sign or strong-control bridge.

**C: digital logical interactions and balance-preserving mixing.** This changes
the model but generic QAOA/XY mixing is established. Lucy is publicly described
as digital/universal, 12 data qubits/24 modes. Public device descriptions do
not establish account access to a specific complete gate instrument, memory
or adaptive control. Local Perceval gates are not remote capability evidence.

## First discriminating calculation: full physical instrument

Run ONLY `P146_full_instrument_check.py`, after non-author source review and
ROOT authorization in its execution contract. It trains no circuit, generates
no graph population, searches no optimum, uses no RNG and calls no hardware.

Exact Q(i) computation uses the explicit eight-mode loss dilation
`V=diag(H4(z),I)*[[sI,-lI],[lI,sI]]`, `s^2+l^2=1`, occupied columns
`a_x=2x,b_y=1+2y`; `eta=s^2` is photon survival probability. The bottom four
outputs are environment labels traced by the observed controller. Preserve
all36 two-photon Fock records, including zeros, for each of nine settings:

- `z=1,i,(3+4i)/5`;
- `(s,l)=(1,0),(399/401,40/401),(112/113,15/113)`.

Check exact unitarity, all Kraus entries, output factorials and every-input
loss masses. Preserve all64 label-resolved distinguishable paths per setting;
prove their factorization and check all principal minors of each coarse
two-memory partial transpose. A B entanglement witness is a RESOURCE contrast.
The group2-per-batch source exactly reproduces B and is now itself quantum;
it is not an automatic classical null or an advantage acceptance bypass.

Check endpoint purge on a fixed five-data-qubit weighted cycle with one
missing chord, a memory ancilla, loss during either CZ, with/without an
unfinished wrong-sign phase, and all environment/Z outcomes. A Hadamard on
data supplies a negative control: arbitrary unknown-state recovery is false.
This finite fixture does not replace the conditional weighted-purge proof.

Independently compare finite native stopping distributions and phase-stage
recursions to closed r_R,c_R,S_m,work formulas for caps R=4,8, m=1,2,4,
all three transmissions, Delta3. Check all terminating dyadic sign histories
for m=1,...,8 numerically to absolute tolerance1e-12. No larger scan follows.

Local Perceval Naive independently evaluates all36 amplitudes for four logical
inputs and each of three transmissions at z=i:432 native points, including
loss-environment outputs. Native complex values must be finite and within
1e-12; every offending value is retained before rejection. This is a local
physical-amplitude cross-check, not optimization replication or QPU evidence.

## Resources, outcomes and next gate

One worker/thread, wall120s, CPU90s, combined logs1MiB, scientific output3MiB,
zero failed retries, fresh output, source/contract/review hashes and v2 manifest.
Raw output is committed before interpretation; any failure is kept.

An incorrect branch/purge identity REJECTS the proposed resource composition
in its stated model until a separately reviewed correction. Native disagreement
blocks physical qualification. Nonpositive drift only fails that sufficient
bound; it is not an impossibility result. A PASS validates the finite stated
instrument and identities; it does NOT demonstrate novelty, a useful algorithm,
realistic throughput, calibrated loss rates or an optimization advantage.

Before ANY optimizer campaign, supply a complete noncommuting graph algorithm
and its physical instrument. Single-layer bounded-degree mean evaluation has
a cheap local classical contraction. Repeated mixing destroys the simple known
resource recovery premise unless a full resource-to-computation bridge is given.
Pair coding covers only one vertex per public pair; classical paired-Ising and
unrestricted bisection get the same features and preparation credits. Require
independently retuned D, strong feasible search, exact/tensor controls, all shots,
preparation/training/compilation/storage/readout and classical wall costs. Only a
surviving DEV result can justify held-out graphs and independent replication.
No count of passing checks substitutes for that missing useful-sign mechanism.
