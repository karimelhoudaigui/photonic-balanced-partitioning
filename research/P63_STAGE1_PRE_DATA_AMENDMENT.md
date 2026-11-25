# P63 stage-one amendment, before any data

2026-11-25. ROOT authorized CODE-ONLY implementation following independent
static review `b4bceeb`. No import, pytest collection, graph generation, native
calibration, count/phase draw or main run is supplied by this amendment.
The original architecture/theory and all old raw data stay unchanged in Git.

1. A SPSA step uses ONE ten-coordinate Rademacher Delta_t for BOTH probes
   `Theta_t+c Delta_t` and `Theta_t-c Delta_t`. Count and fresh carried-priority
   streams are independent between signs; directions are independent between
   steps/arms. There are three steps, four draws/sign, a=1/2,c=1/4, exact
   Fraction losses/angles and the final Theta3 only. Every four-shot batch
   mean enters the gradient without incumbent clipping. Each graph pays
   24 training + 16 fresh draws; final means use two fresh batches of eight.
   Bounds are componentwise: final infinity norm <=3, probe norm <=9/4.
2. The future continuous-field control is full-count:
   `z_j=exp(i phi_j)/sqrt(18)`, iid uniform phi, then
   `Multinomial(18,abs(Uz)^2)`. It is not the P43 weighted CF subset arm.
   Every normalized Fock transition has probability
   `abs(per(W[z|x]))^2/(prod(z!)*prod(x!))`, with both repeated rows and
   columns. These definitions are frozen even though optional controls are
   not implemented or run in this first stage.
3. The input j-cycle gives `UP=D U`, D(a,i)=exp(2pi imaginary_unit*i/6).
   Since input1^18 is invariant under that permutation, nonzero output
   amplitudes require `sum_i i M_i == 0 modulo6`. For output1^18 the sum45
   is3 modulo6: collision-free output is impossible for EVERY Theta. All
   attempts and collisions remain; no retry, CF-only sampler or conditioning
   is allowed. Phase averaging preserves the same joint M law and the same
   suppression. The support guard checks only already required main counts;
   qualification must not draw native18 samples.
4. Stage one executes ONLY B80, followed by independent random/spectral
   P50 FAST-from-raw searches on each original graph. Both fixed modes run;
   there is no free mode portfolio, B incumbent, mapping or optical feature.
   If one fixed mode's eligible prefix is no worse than B's all-paid minimum
   on BOTH graphs, status is DEV_REJECTED_FIXED_FAST and every optional arm
   is NOT_RUN_DUE_FAST_VETO. Otherwise any missing eligible result, missing
   timely first scan or early guard gives INCONCLUSIVE_FAST_ELIGIBILITY.
   Complete eligible survival gives STAGE1_OPTIONAL_CONTROLS_REQUIRED.
   NONE of these statuses accepts a positive or declares an optional control
   beaten. Surviving is not permission for a second automatic run.
5. The all-seven-arm seed recipes are frozen in source/spec BEFORE B data.
   Three trained arms have six training batches and two fresh batches/case;
   each of four flat controls has five future eight-proposal fresh batches.
   Embedding, graph weights, batch master, observation, per-shot priority,
   continuous-field coefficients/multinomial and phase-average source/tritter
   roles are distinct. A shared direction has one seed, not a seed per sign.
   Metadata-only global uniqueness qualification covers all registered roles.
   A collision is a retained failure, never an automatic seed-search license.
6. B pays graph copy/validation, its independent embedding/RNG/context,
   one-half of the once-compiled graph-blind F3/F6 basis, its own phase
   circuits/cache, all directions/probes/updates, source-request wrapper,
   priorities, decoding, cuts, actual means and online incumbent. Networks
   are cached privately per case at their exact Fraction theta keys, with at
   most seven actual networks/case. A repeated final network is reused;
   independent observations keep independent batch streams.
7. This explicitly favorable envelope excludes supplied graph GENERATION,
   scientific/native imports, simulator backend setup/count-generation,
   physics diagnostics and evidence IO from FAST's B-only classical grant.
   They are separately recorded. The immutable factory starts its backend
   clock AFTER RNG/source validation: use its RETURNED backend WALL, not the
   whole factory call. Charged setup is total setup WALL minus returned
   backend WALL minus nested diagnostic WALL. Retain total factory CPU/WALL;
   do not invent internal CPU splits. Optional work never funds B. Each FAST
   allowance is `max(0,B_classical_WALL-actual_adapter_CPU)`, optical latency
   is assumed zero, and no hardware timing is inferred. Shared compiler and
   equal-graph B-mean aggregation costs are split equally across both cases.
8. ROOT prospectively accepted a 10,000-proposal FAST guard PER CALL, four
   calls / at most40,000 guarded work units. This guard is not a shot price.
   At N18, checkpoints are bounded by10,000/call: every checkpoint consumes
   positive work except the single anneal-setup checkpoint, which occurs only
   after an81-delta initial scan and is covered by that scan's slack. The
   immutable P50 helper is unchanged. Early cap prevents favorable eligibility;
   a valid timely prefix can STILL veto B. No post-data cap enlargement.

The single-worker caps remain CPU60/wall90, conventional environment threads1
and native documented maximum1, logs32MiB, new scientific output32MiB and
planned logical workspace256MiB. No failed retry, graph replacement, hidden
warmup, larger native18 probe or new hyperparameter after B data is allowed.
A future optional implementation/reproduction needs separate ROOT review and
authorization while preserving this frozen B trajectory and control design.
Useful N18 decoded response remains unknown; no paper, handoff or QPU action.
