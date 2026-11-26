# P82a — sealed recorded audit run_002 receipt

Date: 2026-11-26. Scope: postseal reading and provenance receipt only.

**Verdict: FINITE_RECORDED_DATA_AUDIT_PASSED for these stored records;
the primary experiment remains INCONCLUSIVE_FAST_ELIGIBILITY.**
There is no positive acceptance, accepted strict FAST veto, or authorization
to proceed to hardware. This receipt neither repeats the checker nor adds
an experiment. ROOT executed the checker; its author subsequently read
the sealed outputs under separate postseal authorization.

## Immutable provenance and execution

- Primary source freeze: 94f80b94f75317524c202ce9ef5bf932d78ddc5e;
  source SHA256 7e1a0d037f5fe0a6af036c1b2a92e765981c93e8d473535984e6f07ea7acfbbc.
- Primary execution: 39b61bb9289cab7439ca15a4aa79d265b068f6f9;
  primary raw seal: debd8235217a8ebe42aa62734d339ab1bd4ea004.
- Original pre-B checker freeze: 34c9513072d385373805215dba6679ffb5686ab9,
  source f595fcaea18dee10b7c89982c2ef700cadca417ec8b2ff63557e95b0e9ba9529.
- Current administrative version: a965e08dbbade4a6ea45d785b0b6fa37af3c8e3a;
  source SHA256 56a3bb2a686203a4e3752687f7e42170d65a5ccfe5987989fbff333fb39afcfd;
  tests SHA256 38383d9e304e26dc3a1f01e7a8d47ab915ed8cc3d1ec3e600b69caa0909d92b4;
  spec SHA256 222e9cd9681eb893655dc08671ad794048dcd174a8896a5b3b9ce69745696499.
- That postdata change accepts the producer wall cap as finite numeric
  EXACTLY 90 seconds, either int or float; it adds no epsilon and changes
  no scientific comparison, role, compiler, cost, or decision rule.
  The archived original and failed first audit remain distinguishable.
- Audit execution ROOT commit: 45d3dce3b39a699a6ca3cf7eac79faae9a5223ff.
- Audit raw seal BEFORE interpretation: b7a19df965d3e6772933bc2bb4ee475011574ca3.
  Only this later receipt is written in the isolated review worktree.

The actual argv matches the bound planned argv exactly: persistent
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python, -B,
research/P82a_independent_raw_audit.py, --binding,
research/P82a_independent_audit_dataset_binding_v2.json, --output,
research/P82a_independent_audit_main/run_002/data.
The runner output parent is research/P82a_independent_audit_main/run_002;
both declared JSON results are inside it. No replacement argv was used.

Started 2026-11-26T02:10:50.294514+00:00; runner runtime 1.321817 seconds;
completed, exit 0, no missing or invalid result. Caps: CPU 30 seconds,
wall 60.0 seconds, threads 1, log 4,194,304 bytes; logical memory
268,435,456 bytes is a PLAN, with no enforced memory limit recorded.
Contract guards remain raw 33,554,432 bytes/output 524,288 bytes,
one worker, zero automatic retries, native calls 0, optimizer replays 0.
Python 3.11.15, NumPy 2.4.6, NetworkX 3.6.1 and macOS arm64 are recorded.
These audit timings are not optimizer or hardware performance evidence.

The manifest honestly records dirty=true. ROOT identifies the user
.DS_Store edit as its cause; read-only status at receipt time showed that
tracked change alone. The 51 execution/input paths match the contract;
all 51 before/after hash pairs agree. A text-only current SHA256 recheck
of every one of those 51 files also passed. No dirty-tree exemption was
used for a pinned input. ROOT reports its separate v2 validator PASS;
this receipt did not rerun that validator or any checker/test.

Binding SHA256: 2ff637e912dbd5db274678c2b03e45b7eb88992074a91cff258c5a11812e41e2.
Execution-contract SHA256: 8472a3a98b40f4ca2ea896adef85d056a8532807532ab3e3a694b89ff8fca17a.
The binding records sealed/authorized state, project-relative source,
manifest, data and qualification paths, hashes and byte sizes; the audit
manifest supplies the complete repeated 51-input closure without copying
the B records into this worktree.

## Actual sealed audit artifacts

Paths below are relative to research/P82a_independent_audit_main/run_002/.

| Artifact | Bytes | SHA256 |
|---|---:|---|
| manifest.json | 20951 | bb6724faceef47e172958054eea84e5088a925543905f6b0bafbe2f2c261a23d |
| stdout.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| stderr.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| data/audit_summary.json | 2638 | da4e5aab5e7dad751e3b52ce80355f679fff0485eaa19311fb08b1f97f604bc9 |
| data/audit_failure.json | 5 | 38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed |

Total: 23,594 bytes. Failure is JSON null; audit logs are empty.
The producer's separate stderr retains its Perceval writable-folder,
temporary-cache, Matplotlib and Fontconfig warnings; it is pinned too.

## Finite recorded outcome

The frozen checker reports both B cases complete: 48 attempts each,
96 full count records and 768 modeled injected source photons overall.
Its independent recorded checks cover registered graphs/marks, exact
cuts/canonical masks, all 64 neighbors, Q-best and three 16-step current
resets per case, matrices/features/rounded-H semantics, full counts and
repair, typed paid clocks and selected-prefix lineage. The 3,507 stored
score rows per case give 7,014 total; this is recorded consistency, not
a fresh physics run or an independent Born-law reproduction.

| Case | All-paid B best cut | Paid WALL grant | r histogram, r=0 through 8 |
|---|---:|---:|---|
| ER8201601 | 46 | 0.14144878596925992 s | 0,2,4,14,11,12,4,1,0 |
| RR8201602 | 22 | 0.13791904402751243 s | 0,2,9,5,16,10,2,4,0 |

The r=4 counts are 11 and 16; all cardinalities remain in the raw
population. No macro-r=4 conditioning supplies the computational budget.
FAST_RANDOM checkpoints number 226/229 (ER/RR); FAST_SPECTRAL number
228/229, totaling 912. Each actual archived selected prefix is timely
under the frozen conservative CPU AND WALL accounting and has cut
46/22, equal to the corresponding B best. All four calls returned
normally but hit the 10,000-proposal early guard and are comparison-
ineligible. Actual proposal counts are 10000/9963 for RANDOM and
9962/9963 for SPECTRAL; the latter three stop before another full scan.
Equality supplies no strict-improvement veto; the guard
cannot support positive acceptance. The producer and checker therefore
agree on INCONCLUSIVE_FAST_ELIGIBILITY, positive_accepted=false;
Tier 2 and D/species controls are NOT_RUN, not passed.

Paid-ledger reconstruction preserves the favorable B WALL grant and
charges P50 call-boundary residuals in both clock domains for prefix
eligibility. Factory backend CPU allocation remains UNKNOWN/null.
No contiguous endpoints are invented for reported durations. Compiler
ordering before R is source-bound plus independent mark reconstruction,
without separate timing endpoints. Custom policies receive recorded
mask/cut/work/cache/clock checks, not private policy replay.

## Qualification and failed-attempt preservation

Qualification run_003 remains the separately sealed 22/22 synthetic PASS:
raw b3260916043361327dfddb668f6456aa5634bf86, receipt
8b132778a6db3a293b1a202a2b80ed6f9676f548. Its 11 inputs stayed unchanged;
runner completed/exit0 in 0.684385 seconds, no failures/errors/skips or
warnings. That qualification did not evaluate DEV/main role streams.
The original 137-line run_002 qualification receipt is unchanged too.

Preflight run_001 rejection ebee1a041d8a9c564fb8c9a012ea7753045f2026
remains preserved: invalid result/output nesting, no child execution.
Audit main run_001 remains preserved on
research/p82a-audit-v1-evidence at b4aa0f3161c7772a13a0247db1246dc4cffc414a:
MALFORMED manifest/wall-cap, float 90.0 versus strict expected int,
stopped before MainReplay. The separately authorized corrected run_002
does not erase or relabel that failure as a pass or an automatic retry.

No scientific execution, import, RNG replay, native call, optimization,
test rerun, raw edit or data copying was performed for this receipt.
The finite pass proves neither Born law nor global TV accuracy, optimum,
equal-resource performance, physical replication or quantum advantage.
P82a supplies no accepted positive result or permission for hardware,
another main run or a postdata guard/tolerance change. The wider positive
optimizer objective remains open; this receipt initiates no followup.
