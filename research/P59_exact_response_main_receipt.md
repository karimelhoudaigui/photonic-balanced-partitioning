# P59: exact fixed-intensity decoded mean response

25-Nov-2026. **Primary result: NONZERO_FIXED_CENTER_EDGE_RESPONSE.**
The ONE fixed N6 family has a phase-dependent decoded feasible mean at
constant intensity matrix, complete one-mode marginals and all factorial
moments through order3. This closes the small physical-channel question.
It does NOT establish an optimization advantage or complete the research goal.
Independent quadratic/hypergeometric reconstruction is still PENDING here;
no result or primary table was sent to that auditor before its code freeze.

## Observed execution and provenance

ROOT authorized one full main after the16 small guards passed. It ran from
clean `9dd58cfa0ced998dc312b70b85662b02b7948685` with unchanged primary source
SHA256 `f1d79ac3940b9c02826d0150dcea8470e2ccc9e5f995615b0ead9aa765de0374`.
Source/spec/parameters remain those fixed before any aggregated response.

The pinned Python3.11.15 child command was:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python research/P59_exact_fixed_response.py --output experiments/P59_fixed_response/run_001/data
```

The installed Mathbox v2 runner used
`research/P59_exact_fixed_response_execution_contract.json`, its EXACT13
inputs, fresh parent output `experiments/P59_fixed_response/run_001`, and all
THREE declared result paths. Observed UTC start2026-11-25T14:44:19.463293+00:00,
runner0.849464s, exit0/status`completed`, stderr0, failure.json=null. Calibration
CPU0.358334s/wall0.36074012494646013s exclude JSON/export; runner time is the
complete child scope. These are calibration costs, not a hardware speed claim.

Enforced CPU20s/wall30s/environment threads1/log4MiB. Scientific outputs are
capped4MiB both inflated and compressed by the source. Planned logical64MiB
is not an observed RSS/affinity guarantee. No cap/failure/retry or parameter,
center, mixer, precision, graph or source change occurred. The numerical slot
was explicitly released immediately after the child returned.

The v2 validator with `--root` returned valid evidence, run completed; ALL13
before/after input hashes agree. The six raw/log/manifest files were committed
FIRST at **ea2e6a9**, before opening/interpreting the scientific summary. This
receipt uses only recorded summary/manifest data; no author rerun or new
numeric audit was performed.

## Exact assertion actually checked

All462 six-photon occupations were retained, including226 parity structural
zeros and any additional zeros. Their c0/c1/c2 integer-Q coefficients and
all probability/decoder kernels are in raw.json.gz. c1 vanishes identically.
The formal column Gram is150I; q is the fixed nonuniform matrix; probability
mass is1 for all phases. The independent precode PNR fixture matches.

All42 complete one-mode PMF bins and ALL83 joint factorial moments through
order3 match their exact q-only constant targets with zero phase harmonics.
The decoder averages all maximizing triples, preserves every collision, and
has tie-count support{1,2,3,4,6,10,20},LCM60. All incident/total crossing
identities hold. The15 edge spectra and10 direct complementary-cut spectra
agree under the independent Gram9/5 inverse with factor1/4. There is no
floating tolerance, graph, LP, random draw, optimum or phase scan.

Each exported spectrum has the exact form

    f_e(phi)=u_e+v_e*cos(2phi)+(sqrt3/2)*r_e*sin(2phi),
    r_e=f'_e(0)/sqrt3.

The COMPLETE15-entry slope table, in the preregistered order, is:

| Edge | r_e |
| --- | ---: |
|0,1|−12151/1265625|
|0,2|0|
|0,3|361049/31640625|
|0,4|0|
|0,5|−57274/31640625|
|1,2|5669/1265625|
|1,3|−5362/3515625|
|1,4|−203/253125|
|1,5|8729/1171875|
|2,3|−59251/31640625|
|2,4|0|
|2,5|−82474/31640625|
|3,4|−13223/6328125|
|3,5|−833/140625|
|4,5|18298/6328125|

Thus12 slopes are nonzero; none was selected to define the device or center.
All15 u/v/r/curvature entries, including zeros, are exported in summary.json
and raw.json.gz. Nine of the ten complementary-cut slopes are nonzero; only
the even-mode class{0,2,4} has zero sine/cosine response. All ten full class
spectra remain exported. No favorable class/edge/graph is chosen as a benchmark.

## Meaning and limits

This is an actual decoded-mean channel beyond fixed q and third-order moments,
rather than a PNR-only fixture or energy proxy. For NONNEGATIVE supplied graph
weights A, the already fixed coefficients permit h=sqrt3*sum A_e*r_e and the
rational global curvature bound M=sum A_e*4*(|v_e|+|r_e|). The predeclared
phase−h/M has conditional mean decrease at least h²/(2M) when h!=0; if h0
there is no strict-gain claim and if M0 choose0. No graph or phase was evaluated
by this main. The step is bounded by sqrt3/4; no post-outcome center was used.

Calibration/storage/validation, phase accuracy and all physical/classical
resource costs remain paid obligations. N6 has only10 complementary balanced
cuts, so exact feasible search is trivial. Genuine six-photon dependence,
comparison with independently optimized distinguishable/partial species,
full-count continuous-phase/sphere and product-marginal controls, matched
classical costs, held-out graphs/relabeling/seeds and physical replication
are NOT established. An exact classical control table/explanation could
reproduce these responses; that is a mandatory next discriminator, not a
claim excluded by this calibration.

No universal no-go, positive optimizer benchmark, advantage, novelty or
hardware compatibility follows. No manuscript, QPU, provider calibration,
Laurent handoff or old scientific archives were changed by this run.

## Immutable artifact hashes

All files are under `experiments/P59_fixed_response/run_001/`:

| File | Bytes | SHA256 |
| --- | ---: | --- |
|manifest.json|10695|`06a043715849213315e2705c469241726f05b9a3c3d799325d85972aa97b75e3`|
|stdout.txt|13343|`427307e395bde66983d7458686b86175459dd33c7cacbf453fdad02e9e5e8779`|
|stderr.txt|0|`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`|
|data/raw.json.gz|23348|`47c352223f58b9a75fcdfe245cf2091d07377aaa870bbff723a7df3230826766`|
|data/summary.json|21248|`d682fafa8d3151871c740a73b6b8d0d343bcd3596975aa85d9b59d91690a4b67`|
|data/failure.json|5|`38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed`|

Total68639bytes, including44601bytes of scientific result files. These bytes
remain immutable; later independent review/replication receives separate
identified receipts and does not rewrite this run or its predeclared scope.

## Subsequent exact independent replication

The pending statement at the top is superseded by
research/P59_independent_quadratic_main_receipt.md: independently constructed
three-factor/hypergeometric code matches2928 comparisons exactly, including
all462 states,15 edges,ten classes,42 bins,83 moments and status. The engine
froze without reading the complete primary response; its hypothesis/PNR
fixture and broad team context were shared. This confirms the finite physical
mean channel and does not establish optimization advantage or hardware value.
