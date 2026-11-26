# P145 — recorded support and utility scope review

26-Nov-2026. **Verdict: the stated structural obstruction is proved for the
four recorded fixed blocks and the exact declared Hamiltonian family.**
This diagnoses ineligible support/utility combinations, not a general negative
result about genuine three-source interference or all PLNS constructions.

## Exact evidence and read coverage

Original raw seal: `f18c14763dc9daa9792e7af0cfcead8a8a1bd50b`.
Read the FOUR `block_setup` rows of
`research/P145_declared_screen/run_001/data/graph_events.jsonl`, including each
complete6x6 integer A, h and all20 recorded candidate cuts/gains (80 total).
Entire-file SHA256: `26e5cc6a07615eb9986f5d70653f57bb0bc3364873e6e6e2543c45f6d8eb937e`.
The complete843-line summary was read, SHA256
`65536cb9c047c26ad8c85236bf45e20feb01cb7b2088469a85b2ca2de8b7043a`;
failure.json is null. Summary reports160 contexts, zero modeled optical trials,
zero positive I3 contexts and zero utility envelopes. Those are recorded fields,
not a newly executed or independently replayed160-context calculation.
The frozen driver has SHA256
`2f13709967ddbadae635d38bba55b934f89bbce45bb14042b658197520010b83`.
The engine's Hamiltonian, profile law and uniform-loss routines were text-read.

## Components reconstructed directly from the integer adjacency entries

Indices here are LOCAL receiver indices; occupied inputs are0,1,2.

| Graph/rule | Components of A, ordered by least index | Input photon counts | Fixed matching proper profile |
|---|---|---|---|
| ER/public | {0};{1,2};{3};{4,5} |1,2,0,0|P23|
| ER/paid_near_barrier | {0,4};{1};{2};{3};{5} |1,1,1,0,0|D|
| RR/public | {0,1};{2,3};{4};{5} |2,1,0,0|P12|
| RR/paid_near_barrier | {0,1,3};{2,5};{4} |2,1,0|P12|

P12 means source indices0,1 share a species; P23 means1,2 share one.
These are source-containing components, with initially vacant components retained
separately. They were not inferred from zeros of a Gram matrix or a float cutoff.

## Exact all-parameter consequences

For every finite REAL alpha,beta,t, `H=alpha*A+beta*diag(h)` preserves these
components; so does `exp(-itH)`. Diagonal boundary fields cannot add a missing
cross-component edge. Alpha=0 may split components further but cannot invalidate
the same fixed coarse partition. No floating eigensolver output is needed for this.

Second quantization conserves photon number in each component. Starting from CF
inputs, the full SPATIAL B count law factors into its source-component laws.
Giving DIFFERENT components orthogonal internal tags cannot change that law:
their spatial outputs already have disjoint support. Thus B equals the proper
profile in the table, pointwise on FULL SPATIAL lossless PNR counts at EVERY setting.
ER/near actually has at most one photon per component, so all five laws coincide.
No claim that ALL proper profiles equal B is made for the other three blocks.

A three-cycle exchange term needs both an assignment and its source-cycled
assignment nonzero. That would force each source and its successor to lie in
the same component, hence all three sources in ONE component, which never occurs.
Both oriented three-cycle terms therefore vanish for every output occupation.
The same-setting full-raw I3 law is identically zero, before utility weighting.
Uniform input loss in the recorded model is a common channel commuting with U;
equivalently use its common output-count thinning. Equality and the linear I3
identity survive it. No such assertion is made for arbitrary coherent mixing,
tag-dependent channels or separately normalized rare-event laws.
For a common utility, the matching proper profile also matches B everywhere;
its independent supremum over the SAME admitted parameter family matches B's.
The best proper envelope is therefore at least B's, beyond just the sampled grid.

## The utility zeros have a stronger, separate explanation

ER/public, ER/near and RR/public each record gain0 for ALL20 feasible candidates.
Their raw utility is zero for any optical distribution whatsoever on that pool.

RR/near has exactly ONE recorded improving support, Y={2,4,5}, cost25 versus
current29, gain4. Its component photon counts are(0,2,1), whereas input counts
are(2,1,0). In particular isolated component{4} starts in vacuum and cannot
receive a photon. The improving output is impossible for EVERY internal state
under the exact block-preserving U. The remaining19 candidates have gain0.
Hence J=0 for every tag profile and all real alpha,beta,t, not only the grid.
With loss, a valid3-photon output requires full survival; invalid sectors hold,
so uniform attenuation cannot make this improving support reachable.

## Interpretation and limits

The sealed zeros are preserved; they are structurally predicted for this fixed
protocol and are NOT general evidence against a useful genuine I3 mechanism.
A future discriminator would at least need all three sources in a common spatial
component and a positive-gain support compatible with conserved occupations.
Those are necessary eligibility checks, not a gain theorem or retrospective
permission to replace blocks, change the compiler or rerun this population.
This review does not regenerate graphs, recompute full-graph cuts, replay160
floating laws, certify numerical residuals or run a manifest validator.
Only Git/text/hash reads and manual support algebra were used: no imports/AST,
scientific program, RNG, test, native call, experiment or QPU operation.
No card, source, qualification review or raw artifact was changed; only this note.
