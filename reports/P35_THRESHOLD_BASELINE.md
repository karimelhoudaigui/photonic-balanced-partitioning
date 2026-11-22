# P35: exact classical threshold-objective baseline validated

Implementation and finite checks PASS. This implements a known marginal
algorithm; it is not a new permanent method or an optimization advantage.
The coordinator completed it after the assigned agent's quota interruption.
There is no fresh independent agent audit of this implementation. Independent
mathematical code paths and Perceval supply the finite controls below.

`src/photonic_balanced_partitioning/photonic/threshold_marginals.py` evaluates
one- and two-output vacuum permanents with Gaussian-rational input and integer
coefficient DP. It keeps off-diagonal polynomial states, applies the diagonal
factorials, and performs no floating clipping. Complete-frame validation is
exact by default. `encode_binary_frame` is explicitly separate: it exactly
encodes supplied binary entries, and disabling physical validation evaluates
their formal polynomial only. It does not certify the true device's matrix.

The API returns threshold click means, pair moments and original symmetric
QUBO expectations, including the off-diagonal factor two. Collisions are
included. No conditioned feasible objective, full sampler, optimum label,
source-selection algorithm or sampled modal candidate is implemented here.
Repeated occupation of an input is outside this distinct-column model.

Seven meaningful tests pass: exact HOM vacuum1/2 and click moments; all moments
and QUBO mean against explicit exact Fock-routing permanents at m4/N2,m4/N4,
m6/N3; vacuum/unary conventions; exact validation versus binary encoding;
and shape/resource guards. The complete existing suite passes271 tests, with
six warnings about Perceval's fallback to a temporary cache.

The committed source678f79d then executed the fixed12-circuit P35 validation:
seeds20261122..20261133, six exactly orthonormal rational complex frames and
six explicitly unvalidated binary encodings of QR unitaries. Every circuit
was compared with complete Perceval SLOS laws. The six exact physical cases
also matched all independently enumerated rational Fock moments and QUBO
energies by exact equality, including N=m. No optimum enters the experiment.

Observed maxima against Perceval: click means5.552e-16, pair moments5.552e-16,
QUBO mean7.106e-15. The run completed; its valid v2 manifest and complete raw
frames, rational moments, energies, reference laws and work counters are in
`experiments/P35_threshold_marginal/run/`. Physical shots0. The internal
validation runtime0.130seconds includes reference calculations and is not a
standalone baseline timing benchmark or a device speed comparison.

Logical counters record DP calls, cache hits, state visits, nonzero transitions
and peak state count. The reported bit size scans stage coefficients and final
results; it is not a profile of every arithmetic temporary. Frame construction,
exact Gram validation, scoring, reference computations and optimizer work are
additional costs. Default state/transition guards bound each marginal call;
the external scientific runner enforces the120-second/one-thread experiment cap.

The known polynomial mechanism and exact-source overlap are documented in
`theory/phase3_threshold_lowrank.md` and `research/phase3_lowrank_sources.md`:
Aaronson–Arkhipov's fixed-rank observation and Ivanov–Gurvits's coefficient DP
precede this implementation. An ideal unconditioned threshold-QUBO mean does
not require enumerating the full Fock law merely to evaluate its value.
This does not efficiently solve global nonconvex optimization or reproduce
finite-shot training noise. The next authentic ObliQ comparison must still
implement its variational tail, source discovery and decoder with charged
costs and the literal/corrected angle variants kept separate.

Decision: KEEP this executable exact classical control for future comparisons.
No manuscript or hardware gate opens. General P36 remains conjectural.
