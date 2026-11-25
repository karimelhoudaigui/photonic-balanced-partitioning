# P53c exact same-phase controls: source/caller static review

Verdict: **STATIC PASS for the declared18-fixture qualification**, no
load-bearing physics/caller blocker found. I did not import this source,
evaluate a new control/physical target, construct a full library, run a test
or LP, or inspect new P53c data. Qualification and main outcomes remain unknown.
The card review a67f29e is separate; this receipt concerns the actual code.

Exact immutable audited commit
`c197ee7b9cba83278bcca704c0b8dbd04a9ab662`. Complete files read:

| Artifact | SHA256 |
|---|---|
| research/P53c_same_phase_controls.py | 737d6743f184661c4352d93c40410679bec5b5e739aa2cd964a63b919eaa53e2 |
| tests/test_p53c_same_phase.py | 5a39505fe47a32d56501368f450a6fa09496f4e2762719828c279c41824d322d |
| research/P53c_same_phase_contract.md | 5a3d9596df2d90dc65021ade0e07a43f66e25feb70be914a8f87798b2c43c7a7 |
| research/P53c_same_phase_execution_contract.json | cab9a67805379cf071ddb78ac7670265beced7c1071a44847fae3d1674a3e137 |
| research/P53c_same_phase_preflight_contract.json | fc92d68ef52e719f80a657d1b4110c610725c8ff8d27937f2b311ec7f220859a |
| research/P53c_same_phase_spec.json | 3f78b8bd71fa7948a17603da816b067866a0221148388f19672b428f4fcc3191 |

I did not write these files. I previously audited P53/P53b and independently
checked the P53b finite certificate, so I know the endpoint result. This is
same-team, post-result code/physics review, not blinded/external validation or
a new independent reconstruction of the original eight-photon source.

## Ring, unitary and Fock factors

The pair rules correctly implement xi²=xi-1, conjugate(xi)=1-xi, with norm
a²+ab+b². The six stored powers are correct. `columns_at_pi3` uses output
row mod4 phase only for inputs4..7, with the lower-right minus sign and the
original Walsh sign table. It is the same U8 at theta=pi/3, not a different
angle chosen from the several theta values sharing x=1/4. The normalizing
entry scale is1/sqrt8. The independent bit-sign/quadratic-field entry fixture
and exact unnormalized Gram8I check the matrix interpretation.

The polynomial product uses unnormalized creation coefficients C_n, not
normalized Fock amplitudes. For four distinct occupied ports, amplitudes are
C_n*sqrt(prod n!)/8² and probabilities prod n!*norm(C_n)/8^4. Code multiplies
the output factorial once and checks nonnegative integer mass8^4. All330
occupations, including zero pairs, are stored. Input ports are checked
distinct/in-range/Python-int, so no omitted input-occupation factorial occurs.

The24 independent coefficient fixtures mean two group choices times twelve
output occupations. The reference enumerates **distinct permutations of the
repeated output-row multiset**, assigning one row per distinct source. This
directly equals C_n: a full labelled permanent sum would repeat each routing
prod n! times. There is therefore NO further factorial division in this
reference. Its arithmetic is Q+Q*sqrt(-3), with an independent sign/root entry
formula, not the production pair multiplication or SIGNS table. Tests compare
both complex coefficients and factorial-weighted probabilities, including
eight bunched cases and four mixed cases per group.

## Species convolution and complete population

Two four-photon species are distinguishable from one another and coherent
only within each group. Their detected count law is the convolution of the
two probabilities. `probability_convolution` has no extra final factorial
or amplitude interference and checks exact mass8^8. Its independent toy
law deliberately distinguishes eight-bunched and4+4 counts, catching that
factorial error. Exact-zero arithmetic skips do not remove output rows.

The builder computes70 input-group laws once, then every complementary split
whose first group contains0, exactly35. It keeps all6435 output counts,
ring coefficients/group probabilities/occupation laws/rank/means and labels.
The immutable420 tie map is applied unchanged; the known4+4 tie fixture has
15 completions, crossing probabilities0,2/3,8/15 at its specified edges.
`_push_scalar` checks mass and incident identities. Appending35 means to all
71 old means retains all106 entries and duplicates; new entries have exact
integer numerators, bounds0..1 and incident4/total16 checks. Label semantics
come from the explicit builder enumeration, not an outcome-based filter.

## Fixed old graph and expanded mean certificate

Main verifies all three immutable helper-source hashes and P53 source/library
pins, recomputes the same exact target, and requires equality to the saved
P53b target and all71 saved means. The saved dual and normalized graph are
read as canonical rational fields from the pinned checkpoint; historical LP
floats do not supply proof data. Its old gap is checked positive and the
saved normalization relation is checked exactly. The prior independent
checker already checked the complete original graph conversion on those bytes.

For all35 new controls, diagnostics use the SAVED weights, normalized graph
and scale, checking normalized margin equals signed margin/scale. Every
margin is preserved; negative, zero and positive minimum statuses are distinct.
Neither a beaten old graph nor a failed old functional is called membership.
The graph is not altered to rescue an apparent improvement.

`solve106` explicitly requires106 means, calls the unchanged qualified primal
and dual proposers once each and verifies exact29-equality primal weights or
all106 exact dual inequalities. New classification strings say EXPANDED106;
winning-arm status0/successTrue gates and retained timeout candidates remain
separate from exact validity. The function does NOT call P53b's discriminator,
classifier or ENDPOINT71-labelled graph constructor. The new dual remains a
functional, with no new benchmark graph. Contradictory exact witnesses are
preserved then cause main failure, accepting neither.

## Caller, output and remaining evidence

The spec fixes x=1/4/theta=pi/3, populations/calls/caps and no positive flag.
Main creates a fresh output directory before constructing new controls.
All raw exact controls,106 labels/kernels, old diagnostics and LP/exact
witnesses are archived; canonical rational JSON encoding handles diagnostics.
Uncompressed certificate<=4MiB-64KiB, summary<=64KiB, total scientific output
<=4MiB. Timer fields are inside-main work; the external runner must cap the
whole child including imports. Fifteen main inputs/sixteen preflight inputs,
CPU20/wall30/thread1,64MiB scientific-data projection are declared, without a
hard Darwin memory guarantee. No cap/run outcome is established by this review.

All18 fixtures were read, not run: independent ring/Gram/24 coefficients,
two group masses/bunching, invalid source ports, probability convolution,
ties, complete append/mutations, synthetic saved-graph identity/tampering/
falsification, expanded classifications/mocked calls/timeouts/no-new-graph,
fixed spec and pinned checkpoint. Qualification constructs two nonglobal
four-photon group laws, not a complementary full new control or106 fit, and
does not read/evaluate the real B target or invoke a native LP.

Required next evidence is targeted qualification, then a separately authorized
main and exact post-run witness review. Any success concerns one finite mean
hull only. It does not compare full laws/tails, continuously optimized b4,
phase/sphere/Gauss, strong feasible classical search, total resources, loss,
scalability or hardware. The N8 graph remains trivially searchable over70
feasible subsets. No code/raw/proof/manuscript or goal status was changed here.
