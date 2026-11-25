# P53b bounded fixed-point main — exact candidate awaiting independent review

**Program status: EXACT_POINT_ENDPOINT71_SEPARATION_CERTIFIED at x=1/4,
theta=pi/3.** The saved rational dual has minimum signed gap 767/327680
against ALL 71 fixed endpoint mean vertices. This is a candidate exact
counterexample to that fixed mean closure, pending ROOT/physics independent
verification. It is NOT an accepted optimizer positive, continuously
reoptimized-b4 comparison, held-out benchmark, runtime or hardware result.

The single point was fixed in proposal a0a6881/1dbb3f9 before evaluation.
Source/tests/contracts froze at bb0ba2d; ROOT and physics returned static PASS.
Twenty synthetic qualification tests passed and were sealed at
fa3eb9a991ec8bb17860ad5609669257a21c0908. ROOT separately authorized this ONE
main at that clean HEAD, 13 exact inputs, CPU20s/wall30s/thread1/log4MiB,
scientific output4MiB/planned64MiB. No point, library, solver, witness rule,
cap or source was changed, and no retry or additional LP was performed.

Actual child command:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python \
  research/P53b_fixed_point_discriminator.py \
  --spec research/P53b_fixed_point_spec.json \
  --output experiments/P53b_fixed_point/run_001/data
```

The v2 manifest at experiments/P53b_fixed_point/run_001/manifest.json records
completed/exit0, bounded wall2.072363s, all 13 input hashes unchanged, clean
source and both scientific outputs present. The validator returned
`valid evidence record`; stderr is empty. The numerical slot was explicitly
released immediately after validation, before reading stored margin fields
and writing this receipt. No new solve, sample or point followed.

Frozen source SHA256:
66ed6abdb1005c961d9bb54fe70008241ef37fe56d8d548e48173d5e9c01c908.
Pinned P53 exact source/library and immutable P53/P52 providers passed their
hash checks. Physical target and vertices were loaded as exact Q, never
rationalized from floating proposals. All exact incident identities passed.

The two provider calls produced solver status0/successTrue. Primal numerical
NO_MATCH residual0.002340698242187522 did not yield an exact membership
witness. Its nonmatch alone is not separation. The separate dual proposal
yielded a rational witness with exact L1=1, rescaling divisor1, and all 71
stored gaps strictly positive; minimum 767/327680. Native readback is
threads1, paralleloff, random_seed5201001, time_limit1s. These are readings
of the frozen program's evidence, not an independent proof reconstruction.

The posthoc nonnegative graph uses common shift1/2 and shifted weight sum14.
Its exact normalized mean margin is 767/4587520. The common crossing total16
makes the shift algebraic; this graph is explicitly labeled
POSTHOC_ADVERSARIAL_GRAPH_WITNESS_ENDPOINT71_ONLY. It was constructed by the
separator, not drawn as DEV/held-out, and has no optimizer-resource claim.
There is no C*, known partition, physical/MC sample, QPU or manuscript update.

Scientific artifacts:

- certificate.json.gz SHA256
  bd9874399ffed241b045f09a5a4f155d7d60263e7314a55e1bfd2358c9022dbe.
  Contains exact target/library, all labels/proposals and rational witnesses;
  compressed size5340 bytes.
- summary.json SHA256
  3d269a9015b679a419d0950b7014a5ea4c4313202affc79a126c5e0c00b87d8d.

ROOT/physics must independently check the original exact target, all 71
inequalities and nonnegative graph identity before accepting even the scoped
mathematical conclusion. P53's previous global Bernstein failure remains
preserved. No automatic continuation, new graph benchmark or paper change
is authorized by this candidate result.
