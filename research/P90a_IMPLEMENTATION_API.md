# P90a code-only API/schema freeze

This freezes interfaces before isolated fixture/contract writers begin. It does
not authorize import, AST, collection, tests, seed digests, RNG, graph/native work
or execution. Authority remains the unchanged P90a180-line card and143-line
independent card review. No P82 production module is imported or monkeypatched.

## Files and writers

Parent owns research/P90a_source_bound_nonflat_veto.py, P90a_execution_spec.json
and this API. Fixtures writer owns only tests/test_p90a_source_bound_nonflat_veto.py
in .local/p90a-fixtures-code/research/p90a-fixtures-code. Contracts writer owns
only research/P90a_preflight_contract.json, P90a_execution_contract.json and
P90a_IMPLEMENTATION_POPULATION.md in .local/p90a-contracts-code on its own branch.
Both child worktrees must be created from this committed schema before writing.
Their local commits are integrated later; no child file is written in parent.

## Public scalar/compact interfaces

All top-level imports are stdlib. Scientific imports occur only within explicit
NativeDependencies construction or a separately authorized tiny fixture.

- AuditFailure(message,payload=None), ResourceFailure(AuditFailure).
- SystemClock.now() returns(process_CPU,perf_WALL).
- numeric_cap(value,expected,label): finite builtin int/float, excludes bool/string,
  exact numeric equality(no epsilon); cut/mask/count validation stays strict integer.
- canonical_mask(mask,n,rank), mask_from_subset(vertices,n), mask_vertices(mask,n),
  mask_hex(mask,n), read_mask_hex(text,n): exact integer masks/cardinality/padding.
- validate_graph(graph): dynamic even n, symmetric integer nonnegative zero-diagonal.
- scalar_cut(graph,mask): sum across the partition once per edge.
- Candidate(mask,cut,sequence): compact immutable algorithm state, no audit dict.
- CutBatch(n,source_mask,base_cut,inside,outside,cuts,masks): inside/outside rank-order
  tuples; cuts=array('q'), masks=array('I'), both count(n/2)^2 in i-major/a-minor
  order. best_index() selects first minimum. No per-candidate dictionaries.
- exact_swap_batch(graph,mask,rank,base_cut,degree=None): materializes every exact
  delta+base cut and canonical mask; degree/ell cached only within this actual batch.
- m_matrix(batch): M[a,i]=cuts[i*k+a]-base_cut, target rows/source columns.
- compile_feature(batch,np_module,expm): M,H,eigenvalues,d,V, v_gram_error,
  nonflat_max,ipr_sum in Compiled dataclass; no marks/R argument.
- transport_feature(compiled,source_ports,target_ports): Routed(W,w_gram_error,
  frame_gram_error), mapping batch.inside/outside source/target labels to W.
  Pure complex/list guards are allowed; no matrix repair.
- Decoded(mask,kept_counts,receiver_counts,full_counts,vertex_counts,removed_vertices,
  r,h,fill,repair_used). repair_counts(source_ports,target_ports,removed_ports,y,choose)
  validates full count then invokes choose(available,count) only for nondeterministic
  fills. Its mask is the graph-label decoded feasible subset before canonicalization.
- ScoreBook(graph,rank,deps,stream): scalar(mask,phase), batch(mask,base_cut,phase),
  start_chain(chain), flush(writer). It owns graph/rank, global/chain Candidate best,
  count and lightweight pending ScalarEvent/BatchEvent objects. Batch cut/mask arrays
  and min/best updates exist before any owning clock. flush builds audit dictionaries
  and serializes already-existing values outside paid spans; no new candidate/cut.
- bounded_descent(book,mask,value,max_scans): Endpoint(mask,cut,scans,local_optimum).
  Given value is already scored. Only complete best scans; strict improvement.
- duration_difference(outer_record,reported_record,event_id): typed P43 operands,
  unknown CPU/endpoints; reported must be unpaid REPORTED_DURATION with matching case.
- call_boundary_difference(outer_cpu,outer_wall,adapter_cpu,adapter_wall,helper_cpu,
  helper_wall): finite nonnegative operands/differences, no clip, unknown endpoints.
- select_dual_trace(trace,adapter_cpu,adapter_wall,grant,n): dict witness orNone;
  same P50 trace keys, max40000, exact mask/cut/work and chronology guards.
- classify_panel(B_cases,controls,case_ids): exact four-call panel, all B complete;
  inadequate→INCONCLUSIVE_BASELINE_ELIGIBILITY, any failed strict inequality→
  NO_POSITIVE_SIGNAL, otherwise FOLLOWUP_REQUIRED; never positive accepted.
- EvidenceWriter(output,max_bytes=33554432,reserve=1048576): exclusive8-file sink;
  append(stream stem or.jsonl,record), single(stem or.json,record), finish(summary,
  failure), close(). Four streams B_ER/B_RR/paid_ledger/controls. Compact final
  reserve is pre-sized before a verdict; no compression. MemoryWriter records
  those full .jsonl names and singles .json names for scripted qualification.
- run_b_case(raw_graph,case,spec,deps,writer,progress) and
  run_fast_control(raw_graph,case,mode,grant,spec,deps,writer).
- run_workflow(spec,deps,writer) returns final summary, retaining first failure;
  writes exactly metadata/graphs/B_ER/B_RR/paid_ledger/controls/summary/failure.
- role(spec,case_id,arm,name,chain=-1,step=-1,index=0) returns literal tuple only.
  seed_from_role and seed_integrity are MAIN ONLY; qualification mocks/fails them.

## Dependency hooks for a fully scripted96-attempt qualification

deps.clock.now(), guard(), native_readback(), generate_graph(case),
control_seed(role), native_seed(role), permutation(role,values),
split_draws(role,count), cut(graph,mask), swap_batch(graph,mask,rank,base_cut,degree),
compile_matrix(batch), transport(compiled,source_ports,target_ports),
make_sampler(W,sorted_removed_ports,native_seed)→(sample_fn,reported_setup_WALL),
fast_solver(graph,seed,initialization,cpu_budget_seconds,max_proposals),
verify_candidate(graph,mask,cut).

Native sample_fn returns(counts,fallback). r0 never calls it. A fake compile may
return a Compiled with V='SCRIPTED' and a fake transport Routed(W='SCRIPTED',0,0),
so full-size qualification constructs no real12-mode matrix. Fake cut/swap_batch
must avoid graph scoring; generate_graph returns literal mock adjacency. Hook
roles return scripted seeds without invoking any hash or Generator. Native P43
factories are never loaded/constructed by qualification workflow hooks.

## Raw schema essentials

B case_start records priority and exact edge total. Scalar records preserve mask,
cut, sequence, phase and owner span. scored_batch records include batch ID,
score_start,count,phase,owner_span,source mask/base cut, inside/outside, integer
cuts and uint32 masks in full original order. Algorithmic candidate selection is
already completed before that record is built. No individual candidate clock.
reset and attempt_request/outcome preserve chain/step, current before/after,
all seeds/ports/coins, full Compiled/Routed rounded arrays, counts/fill, raw/Q
values, acceptance, own scored/endpoint/global bests and modeled photons.
Factory reports link OBSERVED_SPAN and unpaid REPORTED_DURATION plus paid
DURATION_DIFF IDs. Global/own-chain min includes all144 compiler candidates;
compiler candidates never replace current directly.

Control header records raw adapter/outer clock operands and identified P50
REPORTED_DURATION(cpu+wall,null endpoints,source pin), conservative derived gaps.
One control_trace record stores complete column arrays cpu_seconds,wall_seconds,
best_cut,mask_hex,proposal_count,stage_code. Stage dictionary in metadata/spec is
[initialization,initial_scan,descent_scan,anneal_setup,anneal,uniform_restart,
perturb_best]. No trace duplication in summary. Result stores selected corrected
and direct witness, first-scan corrected clocks, normal return, early guard,
adequate, stop/cap flags, counters and durations. All four calls are normal even
at zero helper allowance; source exceptions remain first failure.

## Prospective fixture/population binding

Exactly254 planned deterministic Naive probability/amplitude observations:
3 HOM(H2),60 flatF4 r2(6 source pairs×10 occupations),191 nonempty toy(H2⊕I2)
points(all source subsets,4*4+6*10+4*20+35). Analytic vacuum is not queried.
Keep all observations/zeros/exception repr in JUnit properties BEFORE assertions;
abs2e-12/rel0, max4 receiving modes/4 photons, native1/env1. No native stochastic,
DEV graph, realK12 matrix/source, production seed digest/PCG or optimizer replay.
Independent Fraction-pair-complex permanents/repair verify exact full toy mean
B−D=-5/192 and B−group2=0(all16 R,including013); flat null is inclusion and
uniform-R receiving/mean cancellation, NOT equality of joint(R,Y) laws.
Tiny n4 Hermitian/exponential fixture may use pinned NumPy/SciPy and an independent
closed-form2×2 exponential. All full96 workflow compiler/scorer/factory/RNG/clocks
are mocked. Test items are fixed by exact node names only at final test freeze.
Portable provenance records versions/critical .py hashes/native/interpreter
identities; only main CLI enforces workstation-specific binary/path pins.

The literal spec supplies18 project execution input paths and18 external pins.
Runner binds only project inputs; source main verifies external hashes BEFORE
scientific imports and records actual identity. Caps60CPU/90WALL/env1/native1,
log4MiB/science32MiB/reserve1MiB/logical256MiB plan/0retry. Results are strict
children of fresh runner parents. No qualification or main is started by a freeze.
