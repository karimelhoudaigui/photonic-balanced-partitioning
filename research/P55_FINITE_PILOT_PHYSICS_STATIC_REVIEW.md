# P55 finite-neutrality pilot: independent static physics/caller review

## Verdict and exact target

**STATIC PASS for the planned synthetic qualification, not an executed test
result or permission for a main experiment.** No blocking defect remains in
the reviewed revision. The two reservations raised against the initial
implementation are resolved by the pre-data deltas below. There is no
positive scientific or hardware conclusion.

Reviewed initial implementation
`e95bc0f10811c669ec80d6289ca4d23cc1624693`, then the complete deltas
`ef3663ccab90b5c283883f16d5de0ec2d33aedb8` and
`767b7c65fd240e704ded00654f88fbc3b5af3e8d`. The final source, complete
test file, spec, amendment, mathematical execution contract and preflight
contract were read. The two deltas change six files; no spec, old helper,
physical law, graph seed, source, policy grid or shot budget changes.

Final SHA256 pins, computed from `git show 767b7c65:<path>`:

| Path | SHA256 |
| --- | --- |
| `research/P55_finite_neutrality_probe.py` | `f5563a868e6464e39a669d1fdecfb213374d203d0bf91fea64b7de6d69d422d7` |
| `tests/test_p55_finite_neutrality.py` | `0814a0fc39c70778104ea7d012d19c267936556fe893062778dc7539e85525fd` |
| `research/P55_finite_neutrality_spec.json` | `8b99380f8a79130b508800839c7022264e48d35345c3ef8e89d6846e1f12eba0` |
| `research/P55_finite_neutrality_execution_contract.json` | `de8a81b77594978c2080ccb70ec1cb9e690f85ba1a4911a1da17f14b2060ca5e` |
| `research/P55_finite_neutrality_preflight_contract.json` | `dc8d11c70349beda4da5b207a89df9b4a6e330663cf896126e4594ddb3db1a3d` |
| `research/P55_finite_neutrality_contract.md` | `d387d39677007949c871b784d61eaf80fb9fca8ea24e15a60c660f1c940c9ed5` |
| `research/P55_PRE_DATA_AMENDMENT.md` | `e10753db7bba5d0f48cd5832cc2d0b477608ff76efd19e60b157f687ac908bf4` |

## Physics, decoder and controls

The source is twenty distinct single-photon inputs in twenty modes, with
ideal transmission one. The matrix function is
`U(t)=exp(+i t H/||H||op)`, with real symmetric `H_ij=sqrt(w_ij)` and zero
diagonal. The zero graph is covered. Full matrix reconstruction removes
any physical dependence on individual eigenvector gauges or degeneracies.
Both Gram matrices and both sides of the full-input row-mass condition
are checked at the declared tolerance. There is no input partition or
incumbent-dependent source preparation.

The B and b4 paths call the existing full-count optical factory with all
twenty input ports. b4 partitions the inputs into five groups of four,
using two fixed permutations. D samples independent labelled photons.
Fallbacks are rejected. Neither collisions nor non-CF events are rejected.
True twenty-photon PNR hardware capability is not established by this code.

The phase control calls the P48 continuous-phase **multinomial count**
sampler, not the earlier fixed-weight subset sampler. The independent-B
control uses only the one-mode PGFs, with shifted coefficients `h! e_h(q)`;
it explicitly keeps a variable total count and is not a physical fixed-N
source. Decimal80 correction and CDF guards are prospective numerical
checks, not interval certification. The r20 Fraction/Stirling fixtures
exercise the larger cancellation regime without using a DEV graph.

The inclusion process starts with twenty ones and uses directed rates
`|Hbar_ij|^2 n_j(n_i+1)` at a direct horizon tau. It does not square the
already specified horizon. Reaching the event cap preserves the counts,
last elapsed time, next proposed event time and rate, then fails the
pilot; a truncated chain is never decoded. D includes sqrt(2) retimings
and the CTMC includes both t^2 and 2t^2 scales. Thus the known small-hop
classical explanation remains an explicit control.

The unchanged qualified integer DP samples uniformly among **all** balanced
subsets minimizing the photon imbalance, by one exact arbitrary-integer
uniform rank and bijective unranking. It receives counts and a private rank
stream, not graph weights. Variable totals, all-zero counts and odd totals
are part of its domain. All feasible decoded cuts are scored. For the
product control, the declared maximum total400 gives92631 DP cells; the
runtime is polynomial in the actual integer total, not in its bit length.

## Selection, paid classical work and resolved defects

Each model independently trains on24 draws per graph and evaluates on16
fresh draws per graph. Selection uses exact Fraction means of every shot
from the candidate policy, with equal graph weight and canonical policy
ties. All six selections are written before fresh evaluation begins.
Training cuts remain part of that model's paid incumbent. No optimum is
used, no model borrows another model's preparation, and no candidate feeds
back into the optical source or neutral decoder.

The first implementation incorrectly excluded the entire optical factory
call from B's classical setup. Inspection of the immutable helper showed
that its RNG/source-validation prefix precedes its own backend clock.
The final revision subtracts **only the returned backend WALL**. The outer
setup and factory total WALL/CPU remain recorded; the unmeasured inner CPU
split is explicitly `None`, never reconstructed from WALL or rerun. The
new mock checks factory7=backend5+prefix2, plus caller2: classical WALL4.
This resolves the cost reservation. Tiny clock tolerances are numerical
guard tolerances, not a hardware measurement theorem.

B's own preparation, classical setup, exact rank/DP/count validation/cut,
aggregation and selection fund the FAST allowance. Other controls, optical
simulation/count generation, recording and descriptive diagnostics do not.
The declared conversion is B classical WALL to FAST CPU, minus actual
adapter CPU, with zero assumed optical latency. It is an engineering
comparison favorable to B, not an equal-hardware-cost proof. CPU splits
are not available after the corrected factory accounting.

The fixed random and fixed spectral FAST algorithms each receive the
allowance separately. A veto requires one fixed algorithm to match or beat
B on both graphs; a free best-of-two portfolio is not used for that veto.
Only eligible online snapshots can be credited. A paid initialization may
refute, but follow-up requires a timely first complete scan, eligible
status and no early resource-cap flag. Late completed best values cannot
replace the eligible prefix.

The second reservation concerned only within-batch seed collision checks.
The added metadata fixture checks all596 seed hashes globally, including
all72 training and108 possible evaluation batches, observation/rank/phase
roles, groupings and FAST. It covers policies that will not be selected.
The fixture is to fail before data on any collision, without replacing a
seed. This resolves the missing prospective coverage; uniqueness is not
claimed as already measured here.

## Qualification, interpretation and provenance limits

The complete final test source contains45 prospective parametrized items.
It covers synthetic graph guards, generator sign/scale/relabeling, r20
PGFs, direct-time CTMC/cap preservation, full-source factory arguments,
integer count guards, native Config mocks, costs, policy selection, global
seed metadata, nullable FAST prefixes, veto logic and retained failure JSON.
The two DEV seeds are not used by synthetic graph construction; the mocked
main failure test replaces graph construction before its call. Actual
optical and continuous-phase draws are mocked in this qualification.

Main/preflight closures contain18/19 declared inputs. The planned main
retains480 draws,80 B draws/1600 simulated injected B photons,60CPU/90wall,
one configured native maximum thread,32MiB output and256MiB planned logical
workspace. Neither a hard RSS guarantee nor an observed OS thread count
follows. Failures remain inconclusive, with first evidence and no retry.
`FOLLOW_UP_ONLY` requires strict per-graph fresh mean improvement over all
five count controls and strict paid-best improvement over both eligible
fixed FAST algorithms. `positive_accepted` stays false in every branch.
Two DEV graphs and this finite grid cannot establish general advantage,
held-out performance, novelty or QPU feasibility.

The reviewer previously derived the neutral-decoder small-hop checkpoint
and reviewed reused source/helper physics; those are disclosed same-team
dependencies, not a newly independent physical replication of those
modules. This receipt is an adversarial source/caller review before data.
It does not repeat the Perceval validation or treat code as a proof of
runtime, sampling accuracy or future experimental success.

Actual actions for this receipt were read-only `git show`, `git diff`,
`git ls-tree`, `sed`, `rg`, SHA256 hashing, and this new report write/commit
in the isolated replication worktree. No Python import, pytest, source
execution, DEV graph generation, sample, numerical experiment, network
provider call or QPU call was performed for P55. The archived P53c run is
separate evidence and was not modified. Qualification and any subsequent
main require their own ROOT execution authorization and actual manifests.
