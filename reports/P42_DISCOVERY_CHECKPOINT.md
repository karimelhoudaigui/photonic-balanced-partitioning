# Discovery checkpoint: P41–P42, 24 November 2026

The optimum-blind optimization-advantage target is **OPEN**. P41 explored new
mechanisms; P42 establishes a substantial obstruction for a specified lossy
direct-support class, with independent proof review and a different physical
implementation. Neither a positive optimization benchmark nor a hardware result
has been obtained. The manuscript and the validated P33/P37/E05b evidence remain
unchanged. QPU_GATE=CLOSED under the user's positive-replication requirement.

## What has actually been established

Let a balanced partition be a k-subset of m=2k graph vertices. Prepare N identical
photons in distinct inputs, apply any graph/history-dependent passive unitary,
and assume fresh independent uniform survival eta. Every output mode is observed
or required empty with rejection charged. Accept a candidate only when exactly
k graph modes click; include collisions and every surviving photon sector.
The present attempt's lost-input identities cannot control its unitary.

For any specified candidate S, its unconditioned probability obeys

    Pr(S) <= b_N,k(eta)
           = sum_{ell=k}^N min[binom(N,ell),binom(ell-1,k-1)]
                            eta^ell (1-eta)^(N-ell).

This follows from the spectrum of the lost-input mixture and the rank of the
accepted-support projector. It requires no Haar assumption, graph optimum,
training mask or optimizer-convergence assumption. If N is adaptive, maximize
over EVERY admissible N; the cap need not increase with N.

Let b be that maximum, D=binom(2k,k), nQ an upper bound on physical optical
attempts, and nC>0 a guaranteed number of uniform feasible classical draws.
For L=ceil(nQ/nC), the condition L*D*b<=1 proves that uniform feasible search
stochastically dominates the best newly measured optical cost. This applies to
every graph, every fixed cost threshold and arbitrary classical adaptation of
the permitted optical controller. The same constant uniform target probability
avoids a coupling assumption between different adaptive histories.

In particular b<=[eta/(1-eta)]^k, so eta<=1/5 is sufficient at equal proposal
counts for every k and source ceiling. Eta is survival: this is a **high-loss**
regime. The frozen proof's heading “low-loss” is a terminology issue recorded
by its reviewer; its mathematical formulas and assumptions were not changed.
For PNR acceptance requiring exactly k surviving photons the per-string cap is
eta^k(1-eta)^(N-k), giving a separate sufficient eta<=1/4 range.

For arbitrary fixed Fock occupations and internal distinguishability, use the
companion block-trace bound rather than the identical-input formula. Loss
remainder t has coefficient prod_i binom(s_i,t_i); the sum of the largest
projector-rank number of block traces bounds each support. The identical rank
is binom(ell-1,k-1); the internal-state-agnostic ordered rank is
k!*Stirling2(ell,k). With unknown internal states, block traces are NOT in
general the spatial eigenvalues.

This theorem does not cover arbitrary decoders completing a partial support,
nonuniform or internal-dependent loss, herald-selected present-trial routing,
quantum memory, coherent feedforward or arbitrary input superpositions. It does
not rule out ideal high-transmission optimization. Additional classical
discoveries must be credited to the front end or a common incumbent. Hardware
shot counts, emission attempts, injected photons and scored candidates are
different resources. Measured mean latencies cannot supply guaranteed costs.

## Evidence and independence

| Evidence | Frozen source and outcome |
|---|---|
| Author proof and calculator | Pre-run commit 525e2549907a478623df7c0e49190c423e5e8291; [proof](../theory/P42_threshold_loss_obstruction.md), [general extension](../theory/P42_general_fock_loss_extension.md), [contract](../research/P42_loss_spectrum_contract.json). |
| Independent identical-source reconstruction and audit | Reviewer p41_adaptive reconstructed before reading the author proof; [exact-hash verdict: proved as written](../theory/P42_adaptive_review_525e254.md). Shared P41 context is disclosed. |
| Independent general-source proof review | Physics derived the ordered partial-trace normalization before reading the author proofs; [exact hashes and proof verdict](../research/P42_replication_report.md). |
| Primary execution | [Immutable run_001](../experiments/P42_loss_spectrum/run_001/manifest.json): 462 exact finite table rows, 2375 source-partition rows and 80 optical checks. All registered assertions pass; loss-commutation residual at most 1.1102230246251565e-15. Child CPU 3.550s; runner wall 4.059s. |
| Independent physical replication | [Immutable run_001](../experiments/P42_replication/run_001/manifest.json), preregistered c4a178d7c9786d4e32d4c02b24dbed0abf2f7c87: 42 configurations, 168 laws, 2880 support/encoding checks. Normalized spatial/internal bosonic state, partial trace and tensor-power unitary; only stdlib+NumPy, no production or primary imports. |
| Replication outcome | [Complete receipt](../research/P42_replication_report.md): finite tolerance 1e-10 passed; maximum probability/trace residual 1.4432899320127035e-15, minimum cap margin -1.1102230246251565e-16. CPU 0.368s; runner wall 0.721s. No primary code/raw was read before the frozen run. |

These are analytical proof verdicts and finite numerical checks with different
roles. Floating arithmetic is not interval certification. The replication uses
fresh seeds 2026112471/72, versus primary 2026112451/52. It tests equal, orthogonal
and complex partially overlapping product internal states; the broader
arbitrary-internal-state quantifier rests on the proof, not exhaustive sampling.
The coordinator inspected the new code, raw laws, commands and manifests before
integrating the isolated commits. All inputs/outputs retain their original hashes.

Root primary Git was dirty only through the pre-existing user .DS_Store; the
eight declared execution inputs were committed and unchanged. The independent
pre-run worktree was clean. The original pre-run commits remain on worker refs;
cherry-pick integration revisions must not replace their provenance identifiers.

## Failed extensions are part of the result

1. A bunched four-photon input split into two outputs at eta=0.1 gives two-click
   probability 2167/80000=0.0270875, above the inapplicable distinct-input cap
   0.01. This falsifier is also observed in the independent replication.
2. Two internal species in a DFT6 block plus two spectators violate the naive
   identical-input extension: a specified four-click contribution is at least
   (7/6)*eta^4*(1-eta)^4, exceeding [eta/(1-eta)]^4 at eta=0.01. The derivation
   is retained in [the counterexample](../theory/P42_adaptive_partial_distinguishability_counterexample.md).
   The N8 example has NOT been independently numerically replicated; the new
   ordered-rank proof avoids the invalid extension.
3. The exact cap is nonmonotone in source size: b_(5,3)>b_(6,3) for
   0<eta<1/3. Checking only Nmax would be unsound.

No efficiency value used in these examples was measured on Lucy. The table is
a conditional model certificate, not an operational verdict about that account.

## Mechanism search beyond the archived benchmark

| Route | Result and remaining boundary |
|---|---|
| P41/R1 graph-dependent chiral exchange | Derived the genuine cubic bosonic exchange current, then constructed a positive classical proposal reproducing it through cubic order with an explicit TV remainder. 72 registered finite cells pass a separate sparse-Fock/Ryser comparison. This rejects the proposed leading weak-angle mechanism as an advantage argument; finite angles remain open. [Theory](../theory/P41_adaptive_chiral_proxy.md), [raw and interpretation](../research/P41_adaptive_result.md). |
| P41/R2 grouped feasible encoding | Classical random-wave sampling pointwise dominates the unconditioned grouped feasible probabilities, including graph-dependent fixed circuits. Independent reconstruction passes; 1260 Fock outcomes and two Perceval comparisons are retained. Core phase-twirl/Glynn ingredients are known. Adaptive-history and matched-realized-score extensions are NOT automatic. [Review](../theory/P41_adaptive_grouped_independent_review.md), [scope counterexamples](../theory/P41_encoding_scope_counterexamples.md). |
| P41/R3 nonlinear occupation objective | A connected L1 example with valid collision penalty has lower bosonic than distinguishable mean, refuting an overbroad extension of the older quadratic mean obstruction. 384 exact identities and 64 graph cases pass. It is a mechanism diagnostic, not a search advantage. [Derivation](../theory/P41_obstruction_l1_escape.md), [data](../experiments/P41_obstruction_l1/run/manifest.json). |
| P42 direct-support search with loss | The new spectral/block-trace bound and fixed-target search consequence above close an entire adaptive approach class when the explicit cost certificate holds. No ideal universal impossibility is claimed. |
| P43 continuation | Source-check the exact classical evaluation of local L1 means, and require a changed global/tail/decoder mechanism before a new optimization campaign. No positive mean diagnostic can open the QPU gate. |

## Attribution and next discriminator

Post-integration verification at bc75c741fdedadf2d101d59490c593f77b2665d3:
521 tests pass, all five P41/P42 manifests validate, publication CHECK_PASS,
and git diff against release2744395 is empty for paper/. The separate archive
receipt verifies all602 historical scientific files. Actual commands and full
stdout/stderr are retained in [verification.json](P42_validation/verification.json).
The six pytest warnings concern Perceval's sandbox cache fallback; no test failed.

The uniform loss mixture, spectral rank inequality, fixed-size weighted sampling
and adaptive first-hit inequalities have established ingredients. Exact primary
locators are in the [independent receipt](../research/P42_replication_report.md)
and [encoding source audit](../research/P42_encoding_sources.md).
The bounded source search has not established originality of the complete
search obstruction. **Complete-composition novelty remains OPEN.**

Do not repeat E05b or increase shots in the same generic ansatz. A useful next
route must evade an identified hypothesis, identify what interference changes,
and preregister development graphs, independently optimized D, strong feasible
classical controls, relabelings, fresh seeds and total-cost accounting before
held-out evaluation. Higher conditional postselection quality and preparation
of a classically discovered solution do not count.

Hardware work requires a positive independently replicated optimizer result,
then a frozen small circuit and verified device/source/detection/attempt/cost
semantics. No such result is claimed here; no QPU calls were made. The delivered
paper/main.pdf remains the release artifact with SHA256
271946c9043d26c0e00a964591e9a47541d5816c399e7a52a62032630650243f.
