# P82a first recorded audit: metadata type failure preserved

The ONE authorized recorded-data main ran at ROOTd156aa5, with the
predata scientific checker sourcef595fcae and qualified21 synthetic
fixtures. All46 execution inputs were unchanged. The runner honestly
records dirty=true because of the user's pre-existing .DS_Store file,
which was left untouched and is outside the scientific closure.

The runner returned failed/exit1. ROOT committed its FIVE raw files at
b4aa0f3 BEFORE opening the audit summary/failure or logs. The two logs
are empty; both declared results exist. Runner elapsed0.158351s,
CPU30/WALL60/environment-thread cap1, no missing or invalid result.
The v2 manifest validates against the then-current tree with status
FAILED; validity is not a successful audit verdict.

The recorded result is AUDIT_MALFORMED, location manifest/wall-cap,
message scalar type mismatch, detail repr90.0. The frozen checker
compared this legitimate v2 REAL timeout field to an integer90 through
its strict integer-type comparison. The runner serializes --timeout
as a float, so90.0 was rejected even though the duration is exactly90s.
ROOT's static review missed that representation mismatch; the original
21 fixtures did not exercise this complete producer-limit check.

This happens inside verify_closure BEFORE MainReplay. No classical
graph/mark reconstruction, role-seed hashing, cut validation, native
sampler or optimizer ran. Opaque path/size/hash checks preceded the
failed cap check. It is a checker metadata defect, not a discrepancy
in the primary experiment or its physical model. The96 B outcomes,
all photons, controls, timing limits and primary data remain unchanged.

[Raw failure](../research/P82a_independent_audit_main/run_001/data/audit_failure.json)
and [manifest](../research/P82a_independent_audit_main/run_001/manifest.json)
are immutable. Branch research/p82a-audit-v1-evidence atb4aa0f3 retains
the complete old46-input state, including original checker qualification,
for validation after a corrected source is integrated elsewhere.

ROOT commissioned only a narrow administrative correction: accept
finite numeric timeout90/90.0 by EXACT value, with no epsilon; keep
integer cuts/masks/log/CPU/thread checks strict. Add a synthetic real-
format regression. Checker author receives failure metadata only and
remains blind to B objective/graph/count values. New source/qualification
paths must freeze, be reviewed and pass before any separately authorized
audit run_002. No rerun is automatic. The primary P82a classification
remains provisional and inconclusive, with no advantage or strict veto.

The original prelaunch path rejection,21-test qualification and this
distinct audit failure are all preserved. Nothing is relabeled as a
physics result, successful audit, independent replication or QPU evidence.
