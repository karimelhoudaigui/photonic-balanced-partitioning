# Independent experiment protocol audit

Reviewer: objectives/baselines agent, independent of the experiment-runner author.
Scope: read-only inspection of `experiments/run_research.py`, `experiments/launch.py`,
`photonic/comparison.py`, `photonic/mesh.py`; executable finite probes below.
No experiment source or existing raw run was modified by this audit.

Checkpoint at audit completion: Git `5ce1dc127a95c092a433f6b5a4ea6ed7b8865f38`,
with additional dirty working-tree changes. Source SHA256:

- `experiments/run_research.py`: `b80eb6be9f34ed25e8e04c2b74b7f5f11365c37784ea3842cbc1be081c48aeec`
- `experiments/launch.py`: `de233c0e4607a7eb1e5484e82850fe8c9b790e7aac79529c84d3135f82d7bc9b`
- `photonic/comparison.py`: `4cbe9662c1d5629a2f320b90685c418a6ab5d2a97d9830fad285a196478b6f52`
- `photonic/mesh.py`: `6313fa4d021762c8bcbaee340d1106d9f36154cb85b3451fc4ea5a47683472d9`

These are finite ideal, lossless simulations. No QPU or noise claim is supported.
A supplementary review of the separate exact-budget runner follows below.
It does not retroactively change the original E05 protocol.

## Findings that constrain conclusions

1. **Original E05 matches maximum budgets, not actual costs.** COBYLA can stop
   early, and the penalty and photonic parameter dimensions differ. The code
   records actual evaluations and shots correctly; its summary explicitly says
   matched maximum budgets. Calling this a demonstrated equal-physical-cost
   comparison would overstate the experiment. A separate experiment with exact
   calls/attempts and full discovery curves is needed.

2. **Original random-balanced training is an analytic allocation.** It records
   `budget*shots` training attempts without drawing those batches; only the
   heldout binomial is sampled. Its per-attempt success probability is exact
   and valid. It does not supply observed best-so-far energies, time of first
   optimum, or a physically executed training trace. A fair discovery comparison
   should count optima found during all training attempts, including for this
   very competitive direct feasible sampler, rather than only compare the final
   fixed-circuit heldout probability.

3. **Ideal aggregate t intervals are descriptive, not inferential.** Path and
   cycle graph instances repeat identical graphs. At n=4 the degree-3 regular
   family is also the same complete graph. Seeds for initial circuits and training
   are reused across graph families, inducing dependence. The mixture of graph
   families, graph instances, and training repeats is not an iid sample of graph
   problems. E05 labels this limitation correctly. E02/E03/E04/E07 summaries
   now carry the same explicit descriptive-only caveat in the audited source.
   Use per-instance paired contrasts, report
   within-instance training-seed variation, and aggregate over independently
   sampled graphs only with a stated target population. Two random instances per
   family do not establish robust broad population significance.

4. **Success-oracle improvement is partly built into selection.** For success
   training, the returned circuit is the best loss on a trace that includes the
   initial circuit. Thus after-before success cannot be negative in exact
   arithmetic; positive enrichment over the first circuit alone does not show
   that the optimizer beats equally budgeted search. E02 is an optimum-oracle
   state-preparation diagnostic. The current E02 run matrix correctly includes
   best-of-120 Haar alongside COBYLA at n=4,6,8; evaluate the paired final-success
   contrast against that comparator, rather than infer optimizer value solely
   from after-before enrichment. E04 additionally has random ansatz parameters
   at n=4,6, which are not Haar draws. The Haar branch saves the actual selected
   complex unitary; its parameter trace is not a mesh decomposition of that U.

5. **No optimum leakage was found in the original E05 collision loss.** Exact
   `C*` and success diagnostics are computed/stored, but the optimized value
   uses only conditional cut energy and collision mass. Selection uses only the
   sampled loss; the stored exact probabilities do not choose the circuit.
   E02/E03/E04 success losses explicitly use the optimum oracle. Preserve this
   distinction. Independent heldout RNGs make the fixed-circuit Wilson intervals
   valid as ideal binomial marginal intervals; they are not across-training-seed
   uncertainty intervals.

6. **Do not select the best lambda/objective/depth for free.** Separate lambda
   rows are valid. Selecting the winner among three lambda runs while charging
   only one run's training budget is a hyperparameter-selection advantage. The
   same applies to nine objective variants and multiple mesh depths/optimizers.

7. **Same-circuit controls and reoptimization answer different questions.**
   Comparing bosonic, distinguishable, and multinomial statistics for a fixed
   trained U isolates the effect of changing particle statistics on that U.
   Reoptimizing each model at the same budget compares algorithms. Neither alone
   supplies a quantum speedup or proves that collective interference is useful
   against classical feasible search. Both controls are present in the runner.

8. **Shallow-mesh reachability is strongly label dependent.** Input photons
   occupy consecutive first-k modes; two adjacent-mode layers cannot access all
   balanced bitstrings. Finite checks give 3/6 supported CF outcomes at n=4,
   7/20 at n=6, and 5/70 at n=8 for generic angles. At n=6 neither {0,3,4} nor
   its complement {1,2,5} is accessible at depth two. This can forbid the optimum
   before optimization starts. Natural path/community labels can favor the
   consecutive input pattern. A relabeling control and a reachability upper
   bound are needed before attributing shallow-depth effects to interference.

9. **Zero-angle anchor starts can create higher-order plateaus.** Photonic
   probabilities vary quadratically or at higher order around permutations.
   Default Nelder–Mead uses a very small simplex at zero coordinates. Even a
   universal full mesh may show no oracle-success improvement with this start.
   A graph-realizable control below reaches zero with COBYLA, approximately
   1e-26 with Nelder–Mead, but .167 with random full-mesh search at 120 calls.
   This distinguishes landscape/initialization failure from representational
   impossibility. A fixed declared angle jitter or conditional-energy loss is
   a useful follow-up, with every initialization trial charged.

10. **The spectral anchor already solves most declared small graph slots.**
    For the exact E07 family/seed list, spectral partitioning produces an optimum
    in 10/12 n=4 slots, 9/12 n=6 slots, and 8/12 n=8 slots. These 27/36 deterministic
    preparations have success one without multiphoton interference. High average
    final success of the hybrid therefore has a direct classical explanation.
    Preserve all slots and separately report the nine nonsaturated starting cases.
    `anchor_classical_objective_evaluations=1` counts a cut evaluation but omits
    the eigensolve's runtime and classical work; charge that preprocessing too.

11. **Recorder infrastructure is environment specific.** `launch.py` embeds an
    absolute installed Mathbox recorder path. Raw runner commands remain directly
    replayable using `run_research.py` and the declared arguments in a fresh output
    directory, but reproducing the same manifest wrapper requires that installed
    skill version. Source hashes and numerical package versions are recorded.

12. **Original E06 had an assertion-tolerance bug, not a physics counterexample.**
    `lower <= collision+tol <= upper+tol` cancels tolerance from the upper bound.
    For k=2 the analytic equality can fail that exact floating comparison. The
    failed run is preserved. The coordinator corrected it to separate tolerated
    inequalities before later runs and scheduled E06b. No theory rejection follows
    from this implementation failure.

## Executed finite probes

Environment: project `.venv`, Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1.
No raw existing experiment files were altered. The complete probe input is below;
its stdout is retained here. These are bounded diagnostic probes, not a new
population benchmark, and no v2 manifest was generated for them.

```sh
PYTHONPATH=src:experiments .venv/bin/python /tmp/pasqal_protocol_probe.py
```

Save this exact input as `/tmp/pasqal_protocol_probe.py`:

```python
import itertools
import numpy as np
from run_research import optimize, graph
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh, partition_permutation
from photonic_balanced_partitioning.photonic.comparison import CollisionFreeEvaluator
from photonic_balanced_partitioning.classical.baselines import spectral_partitioning

for n in (4,6,8):
    ev=CollisionFreeEvaluator(n)
    mesh=RectangularMesh(n,2)
    theta=np.random.default_rng(631+n).uniform(.3,1.2,mesh.num_parameters)
    p=ev.probabilities(mesh.unitary(theta))
    reachable=[S for S,q in zip(ev.partitions,p) if q>1e-20]
    print('depth2',n,'reachable_CF',len(reachable),'of',len(p),'supports',reachable)
    if n==6:
        print('target034',p[ev.partitions.index((0,3,4))],
              'complement125',p[ev.partitions.index((1,2,5))])

# A real graph whose unique optimal bisection, up to complement, is 034|125.
n=6;ev=CollisionFreeEvaluator(n);mesh=RectangularMesh(n)
edges=[(i,j,1.) for S in ((0,3,4),(1,2,5)) for i,j in itertools.combinations(S,2)]
energies=ev.energies(edges);initial=np.zeros(mesh.num_parameters)
for method in ('Nelder-Mead','COBYLA','SPSA','random'):
    r=optimize(ev,energies,mesh,initial,'bosonic','success',120,123,method=method)
    print('actual_graph_zero_initial',method,r['n_evaluations'],r['after']['p_success'])

for n in (4,6,8):
    ev=CollisionFreeEvaluator(n);mesh=RectangularMesh(n)
    nonsaturated=[]
    for family in ('path','cycle','regular','erdos_renyi','weighted','planted'):
        for instance in range(2):
            g=graph(n,family,20261120+10000*n+instance)
            e=ev.energies(g.edges)
            s=spectral_partitioning(n,list(g.edges))
            if s.energy>e.min()+1e-10:
                nonsaturated.append((family,instance,s.energy,float(e.min()),s.partition))
                seed=20261120+100000*n+1000*instance
                anchor=partition_permutation(n,s.partition)
                r=optimize(ev,e,mesh,np.zeros(mesh.num_parameters),'bosonic',
                           'success',120,seed+77,anchor=anchor)
                print('nonoptimal_spectral_probe',n,family,instance,'evals',r['n_evaluations'],
                      'before',r['before']['p_success'],'after',r['after']['p_success'])
    print('n',n,'spectral_solved',12-len(nonsaturated),'of',12,'nonoptimal',nonsaturated)
```

Recorded support checks:

```text
depth2 4 reachable_CF 3 of 6 supports [(0, 1), (0, 2), (1, 2)]
depth2 6 reachable_CF 7 of 20 supports [(0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 2, 3), (0, 2, 4), (1, 2, 3), (1, 2, 4)]
target034 0.0 complement125 0.0
depth2 8 reachable_CF 5 of 70 supports [(0, 1, 2, 3), (0, 1, 2, 4), (0, 1, 3, 4), (0, 2, 3, 4), (1, 2, 3, 4)]
```

Recorded full-mesh zero-initial graph control:

```text
actual_graph_zero_initial Nelder-Mead 120 1.186383292284896e-26
actual_graph_zero_initial COBYLA 120 0.0
actual_graph_zero_initial SPSA 120 1.4200825625734138e-05
actual_graph_zero_initial random 120 0.1667397508819877
```

Recorded nonsaturated spectral graph probes (repeat zero only; every run 120 calls,
before success zero):

| n | family | instance | oracle-success after zero-start COBYLA |
|---:|---|---:|---:|
| 4 | erdos_renyi | 0 | 0.9999409470303325 |
| 4 | planted | 0 | 0.999991137470795 |
| 6 | weighted | 0 | 0 |
| 6 | weighted | 1 | 0 |
| 6 | planted | 1 | 0 |
| 8 | regular | 1 | 0.9971886940621413 |
| 8 | erdos_renyi | 0 | 0 |
| 8 | weighted | 1 | 0.9884914695072563 |
| 8 | planted | 0 | 0 |

These probes do not establish an asymptotic plateau theorem. They falsify the
interpretation that zero oracle-success improvement necessarily indicates an
unexpressive full mesh, and they identify a cheap discriminating initialization
experiment. The broad scientific question remains OPEN.

## Supplement: exact-budget E05b source review

Source reviewed: `experiments/run_equal_budget.py`, SHA256
`764fa0aee5adf0519c6ebcdfb3aa2d38a7382e7882369b979ad918c18ad3252b`.
This is a new runner, not a rewrite of E05 raw evidence.

**Finite implementation checks PASS for the tested n=4 path probes.** The source
now draws all uniform-balanced training batches, preserves counts for every
model, fills early convergence to exactly the declared budget, and scores first
optimum discovery throughout training and heldout attempts. The optimum mask is
used after the training value has been computed and does not feed the objective,
parameter selection, or completion rule. Completion proposals use a shared
predeclared scale .1 around the retained point. The full budget is used even
if retrospective scoring has already found an optimum, so no oracle stopping
rule leaks into training.

Verified accounting/indices:

- Exactly `budget` objective calls, each with exactly `shots` multinomial counts.
- Exactly 4096 independent-stream heldout draws; total `budget*shots+4096`.
- First-hit attempt is one-indexed with the correct batch offset. The stored
  first hit belongs to the first training batch containing an optimum, or to
  heldout attempts if all training batches failed.
- Training feasible/optimal counters equal sums over the raw trace. All
  infeasible/collision outcomes remain in the cost denominator.
- Repeated seed runs give identical traces, parameters, heldout counts, first-hit
  indices, and final exact probabilities (runtime fields are excluded).
- The penalty early-stop completion branch was exercised: 62 fallback calls in
  a 120-call n=4 path test. Its budget is still exactly 120, not 58.

Executed probe commands (complete input):

```sh
PYTHONPATH=src:experiments .venv/bin/python - <<'PY'
from run_equal_budget import train
edges=[(0,1,1.),(1,2,1.),(2,3,1.)]
for model,lam in [('bosonic',None),('distinguishable',None),('multinomial',None),
                  ('classical_penalty',.1),('classical_penalty',1.),
                  ('classical_penalty',10.),('random_balanced',None)]:
    a=train(model,4,edges,123,7,16,2.,lam)
    b=train(model,4,edges,123,7,16,2.,lam)
    assert a['n_evaluations']==7 and len(a['trace'])==7
    assert all(sum(r['counts'])==16 for r in a['trace'])
    assert sum(a['heldout_counts'])==4096 and a['total_shots']==4208
    assert a['training_optimal_count']==sum(r['optimal_count'] for r in a['trace'])
    assert a['training_feasible_count']==sum(r['feasible_count'] for r in a['trace'])
    for key in ('trace','heldout_counts','first_optimum_attempt','parameters','final_p_success'):
        assert a[key]==b[key],(model,key)
    positive=[r for r in a['trace'] if r['optimal_count']]
    if positive:
        batch=positive[0]['evaluation']
        assert (batch-1)*16 < a['first_optimum_attempt'] <= batch*16
    elif a['first_optimum_attempt'] is not None:
        assert 112 < a['first_optimum_attempt'] <=4208
    assert a['best_valid_cost'] >= a['optimum']-1e-10
    print(model,lam,'calls',a['n_evaluations'],'counts_total',a['total_shots'],
          'first_hit',a['first_optimum_attempt'],'fallback',a['fallback_evaluations'],
          'best_cut',a['best_valid_cost'],'PASS')
for model,lam in [('bosonic',None),('classical_penalty',10.),('random_balanced',None)]:
    r=train(model,4,edges,123,120,16,2.,lam)
    assert len(r['trace'])==120
    assert sum(sum(x['counts']) for x in r['trace'])==1920
    assert r['total_shots']==6016 and sum(r['heldout_counts'])==4096
    assert r['training_optimal_count']==sum(x['optimal_count'] for x in r['trace'])
    print(model,lam,'n_evals',r['n_evaluations'],'fallback',r['fallback_evaluations'],
          'training',r['training_shots'],'total',r['total_shots'],'PASS')
PY
```

Observed output:

```text
bosonic None calls 7 counts_total 4208 first_hit 3 fallback 0 best_cut 1.0 PASS
distinguishable None calls 7 counts_total 4208 first_hit 3 fallback 0 best_cut 1.0 PASS
multinomial None calls 7 counts_total 4208 first_hit 3 fallback 0 best_cut 1.0 PASS
classical_penalty 0.1 calls 7 counts_total 4208 first_hit 11 fallback 0 best_cut 1.0 PASS
classical_penalty 1.0 calls 7 counts_total 4208 first_hit 11 fallback 0 best_cut 1.0 PASS
classical_penalty 10.0 calls 7 counts_total 4208 first_hit 11 fallback 0 best_cut 1.0 PASS
random_balanced None calls 7 counts_total 4208 first_hit 3 fallback 0 best_cut 1.0 PASS
bosonic None n_evals 120 fallback 0 training 1920 total 6016 PASS
classical_penalty 10.0 n_evals 120 fallback 62 training 1920 total 6016 PASS
random_balanced None n_evals 120 fallback 0 training 1920 total 6016 PASS
```

The small 7-call test emitted SciPy's warning that COBYLA normally requires at
least `num_vars+2` MAXFUN. The runner's explicit StopBudget still enforced seven
actual calls. This warning is irrelevant to the declared 120-call n=4,6,8 runs.

Remaining interpretation limits:

- Model streams share seeds, creating deliberate common-random-number coupling;
  individual Wilson intervals are valid, but cross-model results are paired,
  not independent samples.
- `median_first_attempt_given_found` explicitly excludes censored runs. It must
  not be reported as an unconditional time-to-solution. Report censoring and
  discovery curves or a fixed-budget success rate alongside it.
- Physical attempt equality is ideal and lossless. Emission/detection losses,
  programming overhead, and authentic optical penalty resources are absent.
- `sample_score_lookups` counts processed attempts, including collision sentinels;
  it is not a count of independent graph cut oracle evaluations. The full score
  table is enumerated offline for simulation/scoring, and its size/setup runtime
  are recorded. This cannot support an efficient classical-computation claim.
- No full n=6 or n=8 E05b population experiment was executed by this reviewer;
  that evidence belongs to the coordinator's manifest-recorded run.
