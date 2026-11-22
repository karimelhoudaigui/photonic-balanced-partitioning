# Qwen infrastructure validation — 2026-11-21

This report distinguishes installed tooling, observed execution and scientific
acceptance. A configuration flag or an exit0 alone is not capability evidence.
These are observed outcomes of the completed bounded validation campaign.

| Required gate | Observed status | Evidence |
|---|---|---|
| QWEN INSTALLED | PASS | `qwen --version` = 0.28.0; official npm package |
| LOCAL MODEL | PASS | Ollama 0.32.0; actual Metal load of Qwen3.5-1.9B Q4_K_M, native tool-call response and recorded model digest |
| TOOL CALLING | PASS | Actual read_file,run_shell_command and report creation in isolated validation worktree |
| PYTHON EXECUTION | PASS | Qwen invoked pytest tests/test_hom.py; raw tool output: 8 passed |
| SUBAGENTS | PASS via saved Workflow | Two distinct native child contexts executed sequentially, with actual pytest/write receipts and exact worker-to-critic text transfer. Direct model-generated agent calls remain unreliable. |
| AGENT TEAM | FAIL | Bounded 240-second native test called task_create/team_create but never dispatched a teammate or completed the lifecycle. |
| REPO ACCESS | PASS | Observed AGENTS.md read and reports/QWEN_SMOKE_REPORT.md creation |

Core smoke accepted by Astra:
`results/qwen_cycles/20261121T000644Z-validation/` and its independent
`supervisor_evidence_audit.json`. The worker branch has commitddf337a containing
its observed pytest report. No manuscript hashes changed. Astra separately ran
58HOM/objective/Perceval tests;those operator tests are not misattributed to Qwen.
Eight infrastructure tests cover secret stripping,local-only routing,
agent definitions,paper hash sensitivity,populated sparse worktrees,false PASS
prevention and continuation provenance. The complete working repository passed
192 tests in 28.03 seconds with the scientific Python 3.11 environment, including
42 earlier Phase2 draft tests outside the scoped infrastructure changes.

The successful basic execution alone does **not** certify native delegation
or reliable scientific reasoning by this small model. Seven official-frontmatter
roles are loaded by Qwen Code and versioned. The bounded external orchestrator
runs roles sequentially on the same local model in an isolated worktree;this is
separate from Qwen's experimental native Agent Team runtime.

Controlled failed probes are retained in results/qwen_cycles/. They exposed:
macOS profile syntax;an invalid initial denial-only preflight;small-context
max_tokens:1 clamping;thinking-only empty replies;missing memory-index loops;
missing required agent description;self-execution instead of delegation;and an
unpopulated initial sparse checkout. These were not counted as PASS. Provider
retries,time,turns and worker concurrency are bounded by the launcher.

The final native subagent isolation probe is
`results/qwen_cycles/20261121T005428Z-native-tool-isolation/`. It allowed the parent
only the agent tool and supplied exact JSON, but the model still emitted invalid
arguments (missing description and using name instead of subagent_type). The
tool rejected the call. This falsifies the idea that removing self-execution
tools alone makes this model a reliable delegating supervisor.

The native Agent Team probe is
`results/qwen_cycles/20261121T004414Z-team/`;its independent audit records zero
delegations. A task list entry is not a running agent. No parallel ensemble was
launched. That direct agent-tool/team route remains FAIL; it is distinct from
the later successful native Workflow route below. Autonomous research quality
is not certified by either a feature flag or a successful dispatch.

First scientific execution and fresh-seed replication produced 36 optimizations
and 1152 exact objective evaluations. Qwen really ran the commands, but the first
worker's narrative contained invented uncertainty and mislabeled results;Astra
rejected it. The critic and replication writer did not complete their reports
within their caps. All failed process statuses/logs are preserved. Astra completed
the independent critical review and verified raw calculations without attributing
that work to Qwen. The controller's cycle_evidence_complete flag correctly remainsFALSE.

`reports/ASTRA_QWEN_FIRST_CYCLE_AUDIT.md` records the commands,results,scope and
rejection reasons. All 1152 metric/loss records were independently checked; 18 best
bosonic circuits match Perceval to 3.33e-16. The small initial cycle enrichment
over distinguishable controls reversed on fresh seeds. Scientific verdict:
INCONCLUSIVE;no advancement to QPU or paper. The canonical raw data and validated
manifest are in `results/qwen_n4_supervisor/`.

Installed agent infrastructure is not scientific completion. The useful delivered
mode is bounded,sequential Qwen execution with independent Astra acceptance.
The 8 GiB host and observed 2B-model instruction/report errors do not support a
claim of reliable autonomous research. Larger local models were not downloaded
to mask this limitation. No paid inference fallback was used.
PAPER_READY remainsFALSE;QPU_GATE remainsCLOSED. No QPU request has been made.

Cleanup: the model was unloaded and the temporary Ollama listener was stopped.
The failed native team's empty metadata (zero members) was archived locally,
not deleted. This was supervisor cleanup, not a successful native team shutdown.
Evidence: `results/qwen_cycles/20261121T004414Z-team/supervisor_cleanup.json`.
The launcher starts a new loopback-only server when the next bounded run needs it.

## Native Workflow checkpoint, 2026-11-21 10:16 UTC

`results/qwen_cycles/20261121T101415Z-workflow/` supersedes the earlier
SUBAGENTS failure for the supported saved-Workflow path. An explicit workflow
tool call with a committed name avoids asking the small model to generate
native agent-dispatch arguments. Headless slash invocation had stalled and
is retained separately as an unsuccessful probe.

Astra retained both native child transcripts, their metadata, the runtime
journal and the written report. `supervisor_workflow_audit.json` verifies two
distinct completed child IDs, the experiment-runner's actual eight-test receipt,
the subsequent critic's successful write, and the exact worker text in the
critic's prompt. Timestamps show sequential execution. Manuscript hashes match.
This is observed native delegation and communication, not the main model
performing both tasks itself. The separate native Agent Team lifecycle remains FAIL.

Scientific interpretation remains supervised. The critic incorrectly alleged
that pytest must create deliverable files and that an all-pass result violates
negative-result documentation. The parent misattributed the critic's text to
Astra. These statements are rejected; successful communication does not validate
their content. The seven-role density workflow now adds a bounded scientific
execution and fresh-seed replication, whose outcome requires a separate audit.

The current root tree passes 217 tests. New native-workflow evidence tests reject
missing child receipts, overlapping workers and absent result handoff. Workflow
concurrency is one, stall retries are disabled, dispatch/turn/time caps are
explicit, and named workflows are the only permitted workflow source. The local
runner is a hashed project copy of the trusted computation-audit tooling, so
Qwen never needs access to the credential-protected ~/.codex directory.

## Completed seven-role scientific cycle — 2026-11-22

`results/qwen_cycles/20261122T014822Z-workflow/` now demonstrates nine completed
native child contexts across all seven roles. Timestamps establish sequential
execution. Full transcript prompts establish three exact prior-result handoffs.
Four actual parameterless MCP actions have successful receipts: primary,
adversarial finite-data audit, fresh-seed replication and paired-data audit.
Both scientific manifests validate; all300 grid circuits retained. Astra's
separate audit adds12 Perceval/independent labelled-DP checks, max error6.67e-16.
The scientific worktree passes248 tests. Manuscript OS denial and hashes PASS.

The local stdio MCP bridge is versioned in scripts/research_actions_mcp.py;
it supplies fixed argv and pinned Python, prohibits arbitrary arguments, caps
runtime, refuses evidence overwrites and marks scientific writes non-idempotent
to prevent transparent transport replay. The launcher approves only this reviewed
server inside its isolated runtime. Earlier structured-output attempts failed;
their model requests lacked the promised synthetic tool. The successful path
uses plain completion and independently audited raw tool responses.

Observed gates: QWEN INSTALLED PASS; LOCAL MODEL PASS; TOOL CALLING PASS;
PYTHON EXECUTION PASS; SUBAGENTS PASS via saved Workflow; REPO ACCESS PASS;
AGENT TEAM remains FAIL for its distinct lifecycle. A functioning saved Workflow
is not reported as a functioning Agent Team. Reliable autonomous scientific
reasoning remains unestablished: multiple mathematical/report statements were
wrong and rejected, even though native execution/communication succeeded.

The accepted data, source commitfe7d616 and rejected narrative are detailed in
reports/ASTRA_P33_COMPLETED_CYCLE_REVIEW.md. Native process exit0 is still not an
acceptance rule. The original optimization goal remains OPEN; novelty remains
OPEN; PAPER_READY=FALSE; QPU_GATE=CLOSED. The temporary local model was unloaded
and the launcher-owned server stopped after the bounded287.93-second cycle.
