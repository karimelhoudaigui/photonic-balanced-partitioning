# Completed native density cycle: independent acceptance and limits

Accepted: real sequential native coordination and the finite simulation records.
Rejected: the local model's mathematical/scientific narrative. The original
optimization goal remains OPEN; PAPER_READY=FALSE and QPU_GATE=CLOSED.

Cycle `20261122T014822Z-workflow` started2026-11-22T01:48:22.554784Z from
85b341415c16d3e8757110abb368ec29aee333b6 and finished in287.93 seconds.
The observed native workflow is wf_8abfd3b3327f373b: nine completed, distinct
child contexts across all seven project roles, sequentially. Actual four typed
MCP calls have matching successful responses, each exactly once with `{}`.
The physics role ran five tests. Three exact prior-result handoffs were verified
from full native prompts, not truncated metadata descriptions. Raw contexts,
journal, workflow state, tool receipts and checks are in
`results/qwen_cycles/20261122T014822Z-workflow/`.

Reproduction entry point:

```sh
scripts/run_research_cycle.sh --mode workflow --workflow-name density-research-cycle \
  --workflow-agents 9 --wall-time 1500 --max-failed-retries 0
```

The launcher creates a new branch/worktree, uses only the local model, permits
one inference/worker, and keeps failed runs. The successful protocol uses plain
agent completion plus typed action receipts. Earlier schema attempts did not
expose the promised synthetic tool in observed model requests; those failed
probes are retained and do not count as successful validations.

## What actually ran

The primary and fresh-seed simulations completed in11.109 and10.420 seconds,
under separate300-second limits. Both v2 manifests validate against the frozen
origin worktree. That worktree's raw data and reports have commit
fe7d616eca483157de08985b1bd84a0e8b9863eb, without automatic merge.
Unmodified copies with an explicit hash/path preservation map are in
`results/P33_density_supervised/20261122T014822Z/`. These copies are distinct
from the unattributed root directories, which remain excluded.

| Quantity | Primary | Replication |
|---|---:|---:|
| Complete fixed-grid circuits, m4/6/8/10/12 | 150 | 150 |
| Complete Fock outcome probability pairs (bosonic, distinguishable) | 443220 | 443220 |
| Fixed sharpness cases | 7 | 7 |
| Factorized dilute counterexamples | 6 | 6 |
| Certificate-only cases, m32/64/128 | 36 | 36 |
| Original Perceval cross-check circuits | 10 | 10 |
| Physical shots | 0 | 0 |

All prescribed families, strengths and seeds are present; primary and
replication seed sets are disjoint. All collisions remain in both full laws.
The larger dimensions have no full-distribution simulation. This is exact-law
enumeration with floating arithmetic, not Monte Carlo sampling or evidence
about a random graph population; confidence intervals are not invented.

## Astra's separate computational audit

`scripts/audit_density_cycle.py` checks every full Fock basis for completeness,
all raw normalizations, TV values, collision-pair moments in both statistics,
collision-free masses, preserved hashes, fixed grids and the larger-case scope.
It additionally reconstructs12 selected m4/6/8 circuits using spectral `eigh`
rotations instead of the generator's `scipy.expm`; fresh Perceval SLOS bosonic
laws and an independently coded labelled categorical DP verify both laws.
This is an independent code path under coordinator self-review, not a new
fresh-agent audit or interval certificate.

Observed maxima: normalization2.843e-14; bosonic moment error1.39e-16;
distinguishable moment error3.33e-14; both fresh physical comparisons6.662e-16.
TV and collision-free raw-value recomputations agree exactly in the same float
arithmetic. The largest positive bound excess is2.23e-16, within the stated
1e-9 validation tolerance; it is **not** a rigorous numerical upper enclosure.
The audit v2 manifest at `audit/manifest.json` validates and reports completed.
The isolated scientific worktree passes248 tests; the main tree's earlier264
also includes16 preserved untracked Phase2 draft tests.

Derived PNG/PDF figures: `figures_final/density_checkpoint.{png,pdf}` under the
preserved evidence root. Panel A shows240 nonzero-strength grid cases;60 zero
cases remain in raw data. Panel B shows the sharp leading coefficient and finite
slack. Panel C retains the dilute obstruction. Panel D shows certificate
calculations only, with six fixed seeds per strength/mode combination. No
larger full simulation or optimization gain is implied.

## Narrative rejection and scientific decision

Qwen's mathematical role asserted mean intensity1 instead of k/m=1/2 and
misstated the bound as c>=M. Its critic/final lead repeated these errors.
The algorithm role discussed a nonexistent final optimization objective; there
is no optimizer in this contract. The experiment role incorrectly suggested
the larger cases were included in full simulations and that collision effects
were absent. The first lead denied file access. Such prose is rejected; native
dispatch/communication is real but reliable autonomous scientific reasoning
by this1.9B model is not established. Script-generated review files identify
their authorship and do not masquerade as model-derived proofs.

The exact density theorem at75e5831 separately passed the independent proof
review4420e17. These300 cases support its implemented finite consequences and
reproduce the expected sharpness/obstruction, without proving a universal claim.
N1/N2 prior-art overlap is established; exact density-composition attribution
remains OPEN. The float underflow witness64ad463 reinforces that a rigorous
numerical certificate needs a separate error budget. New adaptive replacement
consequences are self-reviewed and separately recorded as P34.

Decision: SUPPORTED for the preregistered finite assertions within tolerance;
KEEP raw data and native infrastructure evidence; REJECT unverified narrative
and advancement of the original algorithm/paper/QPU claims. Next scientific
obligations are attribution and fresh review of operational consequences, plus
a changed mechanism addressing the demonstrated classical-baseline obstruction.
