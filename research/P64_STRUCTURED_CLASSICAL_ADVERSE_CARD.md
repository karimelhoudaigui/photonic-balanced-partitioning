# P64 static adverse gate: complete fixed-Theta P63 replacement

25-Nov-2026. Proposal plus analytic proof, before any P63 graph/pilot.
Base `682d3573c47ffe4261ae4c018d2132af8e5d8a8e`.
Full derivation: `../theory/P64_fixed_phase_complete_structured_sampler.md`.
STATIC ONLY: no import, numerical computation, graph, draw, simulation,
calibration, tests or QPU call. This card authorizes no execution.

The P63 count model admits a classical COMPLETE fixed-Theta sampler for
the stated ideal N18 architecture. It preserves the coherences removed
by phase averaging. Therefore the phase-average/species/D controls alone
would be incomplete adverse controls for a later P63 claim.

## Exact construction and stronger finite bound

1. Compute the three COMMON F6 source laws with normalized Fock amplitudes.
   Source coefficients can be found exactly in Z[xi], xi^2=xi-1; all 462
   occupations and exact zeros remain in qualification evidence.
2. Draw three independent source occupations and sum their six color totals
   to obtain M. DISCARD the latent rows: only coarse M is conditioned on.
3. Reconstruct every compatible ordered row triple coherently. Enumerate
   the first two source rows; the third is M minus those two. Include the
   fixed-Theta phase in each product amplitude and divide by sqrt(P(M)).
4. Sequentially measure the six colorwise three-mode blocks. Group the
   current map by unmeasured suffix; sum local-input amplitudes before
   squaring and sum squared magnitudes over distinct suffixes. Sample the
   full output triplet, project and renormalize the suffix map, then repeat.
5. Retain all 18 output counts and every collision; apply the same graph
   embedding and uniform-top-nine decoder with the declared RNG rules.

A direct cyclic-column symmetry proves a NECESSARY Fourier residue rule.
Exactly 80 of the 462 occupations pass it, so the true nonzero support has
size s<=80. **s=80 is NOT assumed or evaluated**; further cancellations are
allowed. Fixing M determines the third row from the first two, giving
R_M<=s^2<=6400 coherent configurations. A density matrix of width R_M^2
and an S^3 table are both unnecessary.

At a color with total T, use the full binomial(T+2,2) outputs, even though
each input coordinate is at most six. Streaming each suffix's output vector,
then recomputing only the selected row, avoids a suffix-by-output buffer.
The theory note gives a fixed-N18 coefficient-product bound
6400*(195+6) per shot, with setup/grouping/phase/precision/RNG work additional.
It gives compact-array prospective storage formulas, not a measured RSS or
runtime. This finite bound does not establish polynomial scaling with N.

## Review/execution boundary and required next contract

ROOT must review the static claim and proof first. A later authorized code
qualification must freeze exact source conventions, zero handling, transition
orientation/factorials, all output ranges, precision and error policy, fixed
seeds/RNG namespaces, operation/byte caps and ONE numerical-worker slot.
Use no graph, optimum, embedding search or decoded favorable selection in
that qualification. A phase-sensitive synthetic comparison and a case with
distinct orthogonal suffixes must be independently referenced.

Precomputation/memoization, exact source setup, both kinds of tritter,
imports, initial/cold work, per-Theta phase construction, all pair searches,
normalization and RNG are charged. A warm cached final draw is not the
cost of the sampler. Future finite-precision output must be called
approximate unless a certified exact categorical route is actually supplied.

The naive 462^3 space is 98,611,128 triples and 1,577,778,048 bytes for
complex128 values alone. **Do not allocate it.** The pair enumerator avoids
it; no dense table, transition cache or code execution is approved here.
Unexpected precision/resource failures must be retained as inconclusive,
without pruning configurations, relaxing caps or replacing seeds.

## Consequence for the research gate

This sampler reproduces the entire ideal count law at every input Theta,
so a later adaptive optimizer can also be reproduced in law, including
all decoded objectives and its training history. It is consequently a
stronger architecture-specific adverse replacement than phase averaging.
An empirical win over a separately sampled exact-law replacement can only
be a finite-sample or implementation/cost effect; equal laws have equal
population decoded means at the same Theta. No pathwise paid-best
domination or practical runtime comparison follows from equal laws alone.

The scientific positive objective against physical D, strong classical
search and full-cost held-out replication remains OPEN. No graph result,
runtime, QPU readiness, hardware realization, asymptotic hardness, novelty,
quantum advantage or paper change follows from this static note.

Self-review only. No executable code was added; pytest was not run under
the explicit no-import/no-numerical-execution boundary. A merge, if later
requested, still requires the repository's existing-test gate.
