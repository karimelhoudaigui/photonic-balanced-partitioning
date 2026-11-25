# P49 caller review — frozen 927448a, before numerical work

**Verdict: CHANGES REQUIRED for the classical setup ledger.** The selection,
evaluation isolation and population logic below pass this static review; no
P49 test/import/graph/sampler was executed by this reviewer. No positive result
is accepted by the frozen code or this review.

Scope/provenance: reviewer `/root/p41_adaptive` authored the imported FAST
helper and its qualification. This is therefore an audit of the independently
authored PRIMARY CALLER, not an independent certification of FAST. Physics
owns the independent FAST/physical-circuit audit. Same broad research context
is shared. The ROOT claim card was read before the primary code; no DEV result
existed or was read here. No encoding file was edited.

Reviewed encoding commit `927448ab1e3434e83c93f436cbfa9681284dc5f2`, card
`dc85fa5b49b095de3ba39c37f35d0cada70b47dd`. Exact SHA256:

- `research/P49_trained_source_probe.py`:
  `cdb0c72d935707965b0c3e28432a72812dc522fbc40e04fa842ac8ea8dbb8a93`
- `research/P49_trained_source_spec.json`:
  `275bb9bcae40e0f4d7ba7ee8945c40435b617c89134f83e8e598ab7437387a42`
- `tests/test_p49_trained_source.py`:
  `0d97a6adaee9d7b4013a24fc0573a5fd3c3193dc12163aec3f73a4abd89e14c3`

The main/preflight JSON contracts close 13/14 paths respectively, including
the imported P48/P43/P45/coherent/FAST modules, both P49 tests, pyproject and
the research lock. Their import paths match this closure. The prospective
42 preflight cases have not run and are not evidence of PASS here.

## Required correction, identified before outcomes

`run_batch` brackets ALL of `observation_components(...)` as `setup`, then
`fast_comparison` excludes ALL `observation_setup_wall_seconds` from its grant.
But that function also hashes role seeds and creates the PIT-jitter RNG (and
other classical RNGs), independently of optical backend construction. This
classical setup is not included in another bracket/ledger. Thus the present
grant is slightly smaller than the declared complete classical B envelope.
ROOT independently identified the same gap.

Separate and record postprocessing RNG/seed/setup compute from the local
count-generator/backend setup. Include the former in B's classical spending
and FAST CPU grant; keep cold imports, optical simulation backend construction
and count-generation runtime excluded. Add a controlled-clock fixture proving
the separation before the next gel/preflight. No algorithm, DEV seed or
photonic source change is required. This is a cost-accounting correction,
not evidence for or against a photonic optimization effect.

## Static checks passing, subject to that correction

1. `run_batch` records every feasible cut including worse outputs in `values`;
   `sum_cuts` sums those actual cuts. `select_policies` uses
   `Fraction(sum_cuts, draws*W)` for each graph then divides their sum equally
   by four. W is the graph edge sum with zero-weight fallback1, not Cref/C*.
   Selection is per model with exact canonical-ID ties. Every graph/policy
   must appear exactly once, with its frozen draw count and denominator.
2. All four common frontends complete before training. Source bases use only
   graph/marks/carried gauge and the fixed rotation family, not source_S0,
   Cref or a sampled partition. All q-dependent objects are rebuilt per basis.
   Training does not modify common Cref/source. Private incumbents are retained
   per arm with separate training, fresh-evaluation and paid-total reports.
3. Five arms use8x4 training draws/graph, sphere4x8, IID2x16. Sphere omits the
   two redundant rotated bases; IID has no circuit parameter. Each arm has
   128 total training and128 evaluation draws. Training namespace491100 is
   distinct from fixed-policy evaluation491200, trials0/1x16; model/policy/case
   enter seeds. All model choices occur before the first evaluation loop;
   there is no subsequent reselection. No optimum/mask/success loss is used.
4. FAST receives paid int64 A, free shared incumbent/verified cut and
   `np.argsort(priority)` as rank[vertex]. The caller uses only returned
   deadline-eligible `best_cut/subset`, not overall late discoveries. Early
   cap/wall flags bar acceptance. Its CPU grant is explicitly from observed
   common/B classical WALL plus one-quarter global B selection wall, minus
   small caller adapter CPU. This CPU-from-wall convention is disclosed.
5. Raw/context/FAST JSON conversion/writes are outside the compute brackets;
   count generation is timed separately. Legacy JSON cannot inflate the FAST
   grant. Legacy score ceilings remain diagnostic, with each baseline paid
   separately. Selected-basis setup bounds are subsets of shared preparation,
   not added twice. Numeric diagnostic construction remains explicitly charged
   current implementation overhead, not a minimal optimized hardware cost.
6. Fixed four-case order/seeds/families are checked. If any context is
   numerically inconclusive, no successful-subpopulation training/evaluation
   is attempted. Partial/error records survive. Aggregate proposal checks and
   paid-photon ledgers include both stages; actual QPU calls remain zero.

Future acceptance still requires held-out panels, independent physical
replication, efficient total-cost comparison and measured hardware costs.
Static agreement here cannot establish timing fairness from an unrun program,
sampler correctness, statistical significance, novelty or a positive gate.
