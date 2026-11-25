# P79 prospective raw-PNR even-loop finite validation

26-Nov-2026. **CODE ONLY, NOT EXECUTED.** No source import, AST, collection,
test, random draw, case matrix, native amplitude, sampler or canary was
evaluated during authoring. ROOT must read the five frozen files, obtain an
independent source audit and separately authorize a tiny qualification and
then, if justified, ONE main. This contract is not authorization to execute.
P75b/P75c sources, raw data and receipts remain untouched in their worktree.

## Claim, finite assertion and proof provenance

P78 proposes an exact full unconditioned Gaussian PNR count sampler for real,
symmetric entrywise nonnegative Z with norm below one. Its even rooted-walk
law includes vacuum, bunching and unbounded total counts; it is not a
CF-conditioned sampler or a statement about all Gaussian measurements.
Author note `research/P78_nonnegative_Gaussian_even_loop_sampler.md`, SHA256
`118c88279e01bb13b81450b7f30c2cb55ad852e3a34cfcffbdc56c1c64df7c4a`,
is pinned as an input. The independent reconstruction at commit
`05b10613a1cea1bb8ac68ed3b5e4972f4a6afdb8`, path
`theory/P78_independent_even_loop_sampler.md`, SHA256
`e00cf6fd1003cce8fd7006d422c0b5615f6ddca98cec2f31861e604df228f00f`,
reports a proof in its explicitly ideal sampling model. ROOT's exact-source
review and literature comparison are separate; P79 does not invent their
verdict or make a novelty claim. The peer file is not present in this
worktree's base and is not loaded/executed by P79.

The finite assertion is THREE checks in strict order: independent exact
coefficient identities through total six photons, independent passive
Perceval coherent-sector amplitudes through total four, then fixed-seed raw
loop draws compared with all small-sector bins plus an aggregated tail.
No finite PASS proves an unbounded law, exact finite-bit sampling, global
TV error, practical quantum advantage or QPU capability. No manuscript edit.

## Six literal registered sources, constructed MAIN ONLY

| Case | Pair matrix Z | Perron components | Signed squeeze data |
| --- | --- | --- | --- |
| G1 | [3/10] | singleton r=3/10,v=1 | 3/10 |
| G2 | offdiagonal 3/5, diagonal zero | r=3/5,v=(1,1) | 3/5,-3/5 |
| G3 | diagonal1/5, offdiagonal2/5 | r=3/5,v=(1,1) | 3/5,-1/5 |
| G4 | 3x3 all entries1/6 | r=1/2,v=(1,1,1) | 1/2,0,0 |
| G5 | independent two-mode pairs3/10 and1/2 | two components with their own r,v=(1,1) | 3/10,-3/10,1/2,-1/2 |
| G6 | vvT/12,v=(1,2,1) | r=1/2,v=(1,2,1) | 1/2,0,0 |

No Perron vector is numerically estimated or repaired. All Z,v,r,P entries
are rational. Each exact P_ij=Z_ij*v_j/(r*v_i) row must sum to one; component
partition, support connectivity and absence of cross-block entries are
checked. Integer row CDFs use LCM denominators, with no float normalization.
Strict positive leading principal minors of exact Q=I-Z^2 certify the
physical domain; detQ must also equal the product of1-s_j^2 exactly.

Literal native decompositions are U1, H2 for G2/G3, DFT3 for G4, H2 direct
sum H2 for G5, and G6 columns v/sqrt6,(1,0,-1)/sqrt2,(-1,1,-1)/sqrt3.
Both unitarity orders and U diag(s) UT=Z are checked at residual<=1e-12.
G4 uses complex DFT entries. Signed negative squeezes are coherent source
phases, not an incoherent mixture. These are mathematical sources; squeezers
or color resources are not asserted native to Lucy or any device.

## Phase 1: all exact small-sector coefficients, including zeros

For every occupation at total0,2,4,6, record the rational direct coefficient
haf(Z_n)^2 / product n_i! from repeated labels. Independently build the
matrix polynomial DZ, take traces of its powers2,4,6 divided by their
lengths, then exponentiate their sum by polynomial convolution through
degree6 (up to three powers). These paths share no hafnian computation.
The factor1/length retains rooted/oriented trace multiplicities without any
extra orbit division. Exact equality is required, with all zero rows kept.
Raw reference q=sqrt(detQ)*coefficient is separately recorded in binary64;
there is no sector or CF normalization.

Occupation counts per case are4,16,16,50,130,50, totaling266. They follow
sum over k=0,2,4,6 of binom(m+k-1,k) for mode counts1,2,2,3,4,3.

## Phase 2: independent Perceval passive Fock amplitudes

The frozen P66 helper SHA256
`fb3cf959f022481d360c3371168e0b2f5b97e400b14a4324c43237a162677a9d`
supplies only the version-checked native API/readback. P79 directly builds
complex Perceval Matrix/Unitary backends, avoiding P66's rational-C matrix
coercion for DFT3. NaiveBackend actual compute_max_thread_count is set/read
as1 and rechecked before/after each prob_amplitude call. Loaded-module and
interpreter provenance are retained. No Gaussian native sampler is used.

For every total2/4 output, enumerate EVERY all-even input at that total,
including inputs with a known zero coefficient. Its unnormalized coherent
coefficient is product s_j^(n_j/2)*sqrt(n_j!)/(2^(n_j/2)*(n_j/2)!).
Call native prob_amplitude for every input/output pair and sum the weighted
complex amplitudes before taking the squared modulus. Raw q is
sqrt(detQ)*abs(coherent_sum)^2. Archive all source coefficients, signed/zero
terms, amplitudes, sums and raw q. Never sum probabilities incoherently.

Require error<=1e-12+1e-7*max(abs(observed),abs(reference)), recording both
the bound and its dominant branch. Output points per case2,8,8,21,45,21
total105; native amplitude calls2,21,21,108,390,108 total650. The latter
count is out2*m+out4*binom(m+1,2). These are complete total2/4 sectors;
they are not all photon numbers or a global TV comparison. No stochastic
phase starts unless every exact/native point and population count passes.

## Phase 3: raw loop sampling, paid proposals and fixed statistics

Six fixed PCG64 seeds7910001..7910006 map in order to G1..G6, each20,000
draws, maximum120,000. G5's components use successive independent variates
from its one registered stream. Per component J is Poisson with mean
-m/2*log1p(-r^2); each proposed half-length is NumPy logseries(r^2), root
uniform, and2l exact-rational-CDF transitions follow. Count departure visits
only; accept the internal walk iff it returns to the root. Rejected visits
are discarded, but every proposed loop and transition is charged. Independent
components add their counts. Every complete RAW draw is streamed/flushed,
including vacuum, collisions and every tail count, with its seed/id/count
vector/photons/proposedloops/acceptedloops/proposedsteps. No shot selection.

Poisson/logseries and r^2 are floating implementations, not a finite-bit TV
certificate. Lengths/J/output counts have unbounded support; there is no
truncation or replacing an interrupted draw with zero. A fixed GLOBAL
5,000,000 proposed-transition cap aborts before the next transition and
preserves its partial context and all previous rows. CPU/wall/byte failures
similarly preserve prefixes; there are zero retries and no conditioning
credit from a resource abort.

Fixed bins are EVERY occupation total0,2,4,6 plus ONE tail>6 per case:
5,17,17,51,131,51 bins, total272. The tail reference is1-fsum(finite raw
q), with strict [0,1] check and NO clipping/renormalization. Every bin,
including zero-reference and zero-observed bins, gets a two-sided marginal
Clopper-Pearson interval from SciPy beta.ppf using delta=.01/272; endpoint
counts0/N use exact0/1 bounds. Record count, reference, interval and coverage
with floating-reference tolerance1e-12. Bonferroni nominal family error is
1% under the ideal iid model. This is not a global TV interval or finite-bit
certification. Any first exclusion is STATISTICAL_DISCREPANCY (possibly a
family false alarm), retained without rerun. Later bins/cases stay unrun;
summary completed_bins/planned_bins and phase flags expose the prefix.

Case statistics follow its complete20,000 draws. Descriptive observed mean
photons and paid steps are recorded before interval decisions, alongside
exact source mean sum s^2/(1-s^2), expected proposed steps sum m_c*r_c^2/
(1-r_c^2), and P78 bound m_total*meanphotons. No mean confidence interval,
timing advantage or acceptance-renormalized photon cost is invented.

## Resources, failures, qualification and execution boundary

One worker; CPU60s/wall90s; conventional thread environment1 and actual
native readback1; logs4MiB, records30MiB, scientific32MiB, combined36MiB.
Logical256MiB is a PLAN, with no hard RSS/address-space or affinity claim.
Fresh exclusive output and streaming/flush prevent overwrites. First
implementation/native failure stops all phases; future phase flags remain
NOT_RUN. ResourceStop gives INCONCLUSIVE_RESOURCE_LIMIT; failure detail and
already completed rows are retained. Runner interruption may leave only a
prefix/manifest or missing result: it never becomes a negative observation.
Every true result must be sealed before interpretation, and the v2 manifest
validated against its actual producer. No automatic resume/retry exists.

The separately authorized tiny qualification will contain EXACTLY12 test
functions: one-mode coefficients, pair/zero outputs, collided vs distinct
two-photon factorials, nonuniform Perron rows/rooted cycle weight, invalid
Perron/row data, raw normalizers/physical boundary, pivot-swap/poly cross
terms, signed coherent coefficients/zero sources, CP0/N endpoints, strict
resource/exclusive prefix/serialization, CLI rejection before factory,
and TWO fixed HOM points11->11/20 with actual native1/JUnit provenance.
Only literal physical matrices<=2 and expanded hafnian matrices<=2 are
constructed. Trace-polynomial scalar checks may reach degree6 on<=2modes;
all direct Gaussian occupations and native fixtures have at most2 photons.
No cases(), production draw function, main population, TMSV draw, seed/RNG,
optimizer or source installation is invoked by qualification.

Both JSON contracts bind exactly the SAME TEN project inputs: instructions,
package metadata/lock, P78 author, frozen P66 loader, and these five new
files. There are no new dependencies, downloads, npm/Ollama/QPU calls or
credentials. Persistent Python3.11.15 CLI validates its profile before
creating output; helpers and tests remain portable as in P66's loader.

Prospective child commands (NOT authorization):

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B -m pytest -x -q -p no:cacheprovider tests/test_p79_even_loop_validation.py --junitxml=research/P79_even_loop_preflight/run_001/junit.xml

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B research/P79_even_loop_validation.py --output research/P79_even_loop_main/run_001/data

Use installed computation-audit run_experiment.py, matching --root/--contract,
EXACT repeated --input entries and all --result entries; fresh run_001 only,
--timeout90 --max-cpu-seconds60 --max-threads1 --max-output-bytes4194304.
Qualification and main need separate ROOT decisions after source/proof
review; no scientific execution occurred while these files were authored.
