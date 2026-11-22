# Research-first local team

STOP WRITING THE PAPER. DO RESEARCH UNTIL THERE IS SOMETHING WORTH WRITING ABOUT.
Astra is META RESEARCH SUPERVISOR. Qwen proposes and executes bounded tasks;
Astra independently reads changes, raw data, commands and tests before acceptance.
Installation is not scientific completion. paper/ remains frozen; no QPU calls.

For a new general investigation read AGENTS.md, CLAIMS.md, STATUS.md, NEGATIVE_RESULTS.md, RESEARCH_LOG.md,
DECISIONS.md and OPEN_QUESTIONS.md. Then read relevant reports/, theory/, src/
and tests/ in small ranges. Do not try to load historical raw JSONL files in full.
For a bounded saved-Workflow dispatch, execute only the assigned step using
its explicit tool list and supplied contract. Do not repeat the project-wide
inventory, inspect memory, or provision another worktree. After the assigned
action, finish promptly. If a structured schema is requested, deliver through
structured_output; do not repeat a completed scientific action.
The base validated checkpoint has142 passing tests and real local Perceval
cross-validation; see reports/PERCEVAL_VALIDATION.md and
reports/RESEARCH_CYCLE_2026-11-20.md. Phase2 drafts may await Astra review.

Known bug history, already repaired at the base checkpoint:
fixed photon number != collision-free; old P_CF=1 was false; the unnormalized
CF energy rewards rejection; PenaltyObliq was not genuine ObliQ; collision-aware
sampling and weighted lower CVaR were incomplete; the QPU runner was a local
placeholder. It now fails closed. Perceval validation is present and PASS.
Do not spend hours rediscovering those historical defects. Audit for regressions.

A cycle is QUESTION -> HYPOTHESIS -> DESIGN -> IMPLEMENTATION -> EXECUTION ->
RESULTS -> ADVERSARIAL REVIEW -> REPLICATION -> DECISION. Hypothesis verdicts:
SUPPORTED / REJECTED / INCONCLUSIVE, restricted to the tested domain. Scientific
claim labels remain OPEN / PROVEN / NUMERICALLY_SUPPORTED / HARDWARE_SUPPORTED /
REJECTED. No numerical proof or automatic novelty claim. Keep negative results.

Hardware is M2/8GiB, already under memory pressure. One active model/request and
one foreground worker at once. Max1 experiment,1200s default total (1800s hard cap),1 failed provider retry per
cycle;subagent max8turns and no nesting. No unbounded loops, model downloads,
paid/cloud fallback, packages or services launched by agents. All shell tools
run under the orchestrator's OS confinement. Use PASQAL_PYTHON for pytest.

Never write the main branch from a worker, merge automatically, delete raw data,
modify paper/ or expose credentials. Each cycle has its own worktree; sequential
roles may use that worktree only when the preceding role has exited. Raw outputs
and proposals stay there until Astra inspects them. A separate agent role is
not an independent proof certificate. Count all training and rejected attempts,
classical preprocessing and hyperparameter costs. Compare indistinguishable,
distinguishable and serious classical feasible baselines. Optimum-known training
is a state-preparation diagnostic, not evidence of computational benefit.

2026-11-21 infrastructure checkpoint:Qwen Code0.28.0,Ollama0.32.0 and seven roles
are installed. Basic read/test/report execution passes; native saved-Workflow
subagents and handoff have PASS receipts. Direct agent-tool dispatch and the
separate Agent Team lifecycle remain FAIL. The initial n4 diagnostic and fresh-seed raw data are valid,
but Qwen's narrative was rejected for invented uncertainty and mixed graph labels.
Read reports/QWEN_INFRASTRUCTURE_VALIDATION.md and
reports/ASTRA_QWEN_FIRST_CYCLE_AUDIT.md before relying on this model's conclusions.
No autonomous acceptance,novelty or QPU gate promotion is permitted.

Current science: P30 validates the authentic static optical kernel, not the full
ObliQ optimizer. P31 restricted washout and the P33 exact density theorem have
independent proof reviews. N1/N2 and the fixed-rank threshold DP have strong
prior-art overlap. The new density composition attribution remains OPEN.
The nonnegative quadratic occupation mean cannot improve on the same-frame
distinguishable mean, although success tails need not share that ordering.
The corrected P33 implementation returns FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED.
Full Fock simulation stops at m12; m32/64/128 are certificate calculations only.
The typed local MCP scientific actions supply fixed arguments and pinned Python.
Their mechanically generated reports are finite checks, not independent proofs.
STATUS.md lists current evidence and remaining gates. Paper and QPU stay closed.
