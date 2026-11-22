# Unattributed root P33 directories: excluded from accepted evidence

During the 2026-11-22 continuation, two untracked directories were observed in
the primary checkout: `results/P33_density_primary/` and
`results/P33_density_replication/`. Their creation was not observed in the
controlled native workflow. They are preserved in place, without modification.

Both manifests name77a8588 with a dirty tree and the same start timestamp,
2026-11-21T23:54:16.186632+00:00, and runtime0.399564 seconds. Their listed
hashed outputs include only stdout/stderr, rather than the scientific JSON.
The replication directory lacks those two listed log files. The primary
pyproject hash also predates the optional SymPy metadata update. These observed
provenance deficiencies prohibit treating the directories as completed,
independently validated native runs. Their origin is unresolved; no cause is
inferred from the anomaly.

No accepted result, figure or claim will use these directories. The current
controlled launcher starts from a committed Git worktree, which does not import
untracked root files. A fresh native cycle must create and hash its own data.
