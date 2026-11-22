# Historical P20 evidence: do not overwrite

The initial and larger-training archives were validated and integrated in
5dbdbc3; their independent integration review is a4d4745. Read
`reports/P20_INTEGRATION_REVIEW.md` for scope and provenance limitations.

The historical drivers use fixed output paths and overwrite existing files.
Do not replay them in this checkout. Preserve their original source bytes,
which are pinned by the manifests. Any new campaign needs a fresh isolated
checkout/output guard and its own execution record. No new campaign was run
for integration.

These are 64 independent synthetic proposals from each fixed anchor, not
executed adaptive trajectories or hardware shots. Equal attempts per case do
not establish equal total preprocessing, training, query or photon resources.
The chosen zero-interaction kernels match the classical product control.
Stored exact-replacement counts reuse checked probabilities and seeds;
their identical values are not an independent empirical replication.
