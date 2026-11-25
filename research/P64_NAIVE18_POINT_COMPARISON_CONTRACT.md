# P64 deterministic N18 probability comparison: prospective contract

2026-11-25. CODE-ONLY, based on sealed P64 qualification4ee15ab. No import,
pytest collection, numerical computation, native calibration, probability query,
phase/count draw or graph was executed while preparing these files. ROOT must
review this exact closure, commit and allocate the single numerical slot before
qualification; main requires a separate explicit decision after qualification.

## Fixed finite assertion and all points

The new wrapper evaluates the COMPLETE P64 fixed-Theta count kernel at seven
prospectively fixed occupations and exactly two phase arrays, then compares
each probability to local Perceval NaiveBackend on an independently built
full18x18 unitary. These are14 selected probabilities, not a complete18-mode
law, total-variation certificate, optimizer trajectory or graph comparison.
All points, including zeros and collisions, are retained without replacement.

Ports are `a*6+i`; each listed triple is `(n_(0,i),n_(1,i),n_(2,i))`.
The first array is allzero. In the second, only b=1,2 and i=1..5 vary:
`theta[b,i]=(5*(b-1)+i)/11`. All gauges remain zero. Exact rational strings
are stored in the spec and converted to float only for trigonometry.

| Frozen occupation | Color totals M | Exact triple pattern |
| --- | --- | --- |
| all18_port0 | (18,0,0,0,0,0) | (18,0,0) at color0; vacuum elsewhere |
| CF_forbidden | (3,3,3,3,3,3) | (1,1,1) at every color |
| M666000 | (6,6,6,0,0,0) | (2,2,2) at colors0,1,2 |
| M444222_left_rotations | (4,4,4,2,2,2) | left rotations0,1,2 of(2,1,1) at0,1,2; left rotations0,1,2 of(1,1,0) at3,4,5 |
| M822222_left_cycle | (8,2,2,2,2,2) | (3,3,2) at0; left rotation(i-1)%3 of(1,1,0) at i=1..5 |
| M660006 | (6,6,0,0,0,6) | (2,2,2) at0,1,5 |
| all18_port12_flat_anchor | (18,0,0,0,0,0) | (0,0,18) at color0; vacuum elsewhere |

Seven distinct full18-count vectors and their triples are literal frozen
spec inputs, visited in phase-major then occupation order. M822222 has final
physical row totals(7,6,5), intentionally exercising the absence of any false
post-projection row-sum-six constraint. The CF vector violates
`sum_i i*M_i=0 modulo6` and remains an explicit exact-zero case. No observed
PNR18 value motivated any point or change. ROOT added port12 BEFORE data;
the original six occupations were preserved.

For port12 every input-column probability is1/18. The normalized full-source
bunching probability is `18!/18^18`, independently of the two gauge-fixed
phase arrays. This exact Fraction anchor is archived and checked for both
engines with the same prospective tolerance, not used to select an outcome.

## Three independent constructions and normalization

1. `P64_independent_F6_pair_source.py` uses pure standard-library exact
   integer pairs in Z[xi], xi^2=xi-1. Pair Fourier columns j and j+3:
   `L_j L_(j+3)=E_j^2-O_j^2`. Each square has six monomials, giving12 terms
   per quadratic, three quadratics and exactly1728 direct products. A separate
   multiset enumerator retains all462 occupations. The unnormalized
   coefficient c_n gives integer weight `prod(n!)*|c_n|^2` over denominator6^6.
   Every signed coefficient and weight is compared exactly to the sealed
   primary source JSON. No production sampler is imported for this component.
   The complete independent table, quadratics, normalization and comparison
   are archived before the caller asserts agreement.
2. The corrected P64 source is immutable and SHA-pinned. The wrapper computes
   P(M) first from exact integer source weights. A zero exact mass returns0
   without calling conditional normalization or project. For positive mass,
   it uses the audited conditional_state/local_distribution/project methods,
   multiplying `P(M)*product(p/fsum(probs))` for the fixed output path. Every
   conditional raw norm, chosen probability, normalized probability and live
   width is archived. A rounded local zero is explicitly distinct from an
   exact zero coarse sector. No sample()/RNG call is made.
3. The reference constructs dense `(I3 tensor F6)`, D, `(F3 tensor I6)` and V
   independently, multiplying the matrices in the physical order. A separate
   scalar entry formula supplies an architecture cross-check. Both complete
   matrices are archived before guard assertions. q and both Gram matrices
   have fixed absolute5e-12 guards. Neither matrix builder imports production
   Fourier/tritter/coefficient/cache helpers. Only the dense reference enters
   the native Naive circuit, with normalized source occupation1^18.

The local Perceval1.3.0 NaiveBackend implementation was READ as text during
authoring: `prob_amplitude` builds an18x18 repeated-row/column submatrix,
calls `exqalibur.permanent_cx` and divides by
`sqrt(prod(output!)*prod(input!))`. No mask, all-state iterator, sampling,
postselection, remote Processor or QPU is used. Native18 objects and all14
queries occur ONLY in separately authorized main, with no preliminary18
warmup or calibration. Native imports, setup and each query are timed.

## Frozen precision, failures and interpretation

ROOT accepted before data:

    abs(p64-pNaive) <= 1e-12 + 1e-7*max(p64,pNaive).

Every pair records absolute AND relative error, allowed error and whether
the absolute term dominates. An absolute-dominated agreement does not
certify relative precision for a rare event; no global TV conclusion follows.
The normalized P64 kernel uses rounded masses and phase values. It is not
the literal finite-bit random-quantile law; this check calls no quantile RNG.
The Naive reference is a different numerical engine, not interval arithmetic.

Both point probabilities, the Naive amplitude, path, full counts, phase,
timings and errors are flushed to JSONL BEFORE comparison assertions. The
analytic anchor is likewise recorded before its assertions. Nonfinite
results or other engine failures stop with the current point and preceding
evidence retained. Earlier raw records and sealed reference data are never
changed. Missing cases, cap, invalid counts/norms/source data, matrix failures
or tolerance failures give INCONCLUSIVE_FIRST_FAILURE, not a selected subset
of successful points. Zero failed retries, replacement points and cap raises.
Invalid nonfinite numbers in failure evidence serialize as explicit tagged
values, preserving the failed payload without nonstandard JSON or numerical
repair. Computational probabilities are never replaced by those tags.

The single-worker limits are CPU60/wall90, conventional environment threads1
set before numerical imports, documented exqalibur Config maximum1 before
factories and after work, logs32MiB/scientific32MiB/logical256MiB. Native
versions are checked against NumPy2.4.6, Perceval1.3.0 and exqalibur1.4.2;
the complete dependency lock is an execution input. OS scheduling, native
RSS/affinity and an optimizer's resource consumption are not certified.

Static storage is bounded by the P64 width6400 and lazy transition130340
entries, small18x18 matrices,462-row independent source, and14 short paths.
There is no S^3 table, full18-mode Fock law, sample stream or graph. A
conservative logical plan with Python/transient headroom stays within256MiB;
native permanent working memory and actual clock time remain unmeasured.
Projected new scientific output is below4MiB, with a32MiB guard/reserve.
The cap is not a claim that fourteen dense18 permanents plus all cold source,
cache and import work will finish; unexpected exhaustion is inconclusive.

## Small qualification and exact future commands

There are22 prospectively authored test items, not yet collected. They cover
the independent exact F6 source against its sealed input, frozen metadata,
pure18x18 matrix identities with ZERO native18 queries, C6/count guards,
mocked zero-M no-division and normalized conditional paths, tolerance/error
labels and exclusive evidence files. The ONLY real native fixtures are five
two-photon/two-mode probabilities: HOM plus a bunched input testing both Fock
factorials. There is no random draw, graph, native18 calibration or production
sampler construction in this qualification.

Both JSON contracts enumerate the SAME16 exact project-relative inputs,
including the code/tests/spec/contracts, immutable P64 source, sealed source
table/manifest, proof and dependency lock. They are prospective v2-runner
contracts, not observed manifests. Use their full execution_artifacts list as
repeated --input arguments. The installed computation-audit runner must use a
fresh separate parent for each stage, --timeout90 --max-cpu-seconds60
--max-threads1 --max-output-bytes33554432, and the planned_results list as
repeated --result paths. Actual before/after input hashes, status, outputs
and timestamps are generated only by an authorized run.

Qualification child argv, AFTER ROOT review and slot allocation:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -c 'import os; os.environ["P64_NAIVE18_QUAL_OUTPUT"]="research/P64_naive18_preflight/run_001/data"; import pytest; raise SystemExit(pytest.main(["-q","tests/test_p64_naive18_probability_check.py","--junitxml=research/P64_naive18_preflight/run_001/junit.xml"]))'
```

The fresh qualification parent is `research/P64_naive18_preflight/run_001`;
its two declared results are junit.xml and data/independent_source.json.
Qualification never starts main automatically. A separate ROOT decision
may authorize this exact main child argv under a new bounded parent:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python research/P64_naive18_probability_check.py --spec research/P64_naive18_probability_spec.json --output experiments/P64_naive18_probability/run_001/data
```

Main declares independent_source.json, two matrices_PHASE.json files,
points.jsonl, failure.json and summary.json. All files use exclusive creation
inside a fresh worktree output directory. The independent source artifact and
matrices remain even if a later point fails. A hard runner kill can omit
final summary/failure files; the manifest then records incomplete bounded
execution. No successful result is represented by this source freeze.

Fourteen agreements would support only these14 fixed probability checks and
the separately exact source table. The scientific optimization target,
complete finite-precision N18 law, global error, full optimizer cost, fresh
graphs, held-out replication, paper and QPU gates remain separate and open.
