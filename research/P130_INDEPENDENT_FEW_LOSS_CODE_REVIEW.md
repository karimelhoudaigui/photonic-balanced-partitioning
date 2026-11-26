# P130 — Independent exact-qualification source review

2026-11-26. Reviewer P66, non-author of P130; author of reference producer P107.
Own parent ff2150e75a7e889b85e60ed3ad73bd390f8c2b47.
Method: computation-audit, STATIC ONLY. Outcome: **audited, not executed**.
**Static verdict: PASS, no material correction requested before ROOT binding.**
This verdict authorizes no import, qualification or other scientific execution.

## Exact scope and identity

Fully read ALL 391 lines at 5527fa8695101b712a1902031cd78b0efddec093:

| File | Lines | SHA256 |
| --- | ---: | --- |
| research/P130_few_loss_validation.py | 273 | d31ef94833837bb1f8131453a26a8e97d23878bfc5310fa5e761473d15ee1548 |
| research/P130_population.md | 87 | 59d78121c1b44ef57628dc46d488d27394c849e9b407f13bb3a3a70344d3b0e4 |
| research/P130_contract_TEMPLATE.json | 31 | 0884e794de5a5808dc15f1d98500c450dd24245206bc70780d7b62fed2fa86e2 |

All three Git-blob hashes were checked without executing/compiling their code.
P126's separately audited 231-line proof is the mathematical target. P130 is
a finite r0=2 identity/normalization/PSD qualification for 14 literal matrices,
not an implementation of P126's approximate rejection sampler or its FPRAS leaf.
No P130 outputs exist for this review; I did not open P96/P107 raw payloads.

## Algebra, representation and mathematical assertions

Source lines 26-38 implement a correct row/subset permanent DP: after t rows,
mask entries sum exactly all injections into those t columns. The final full
mask is the permanent, including empty permanent one. Its shape cap is four.
Lines 39-53 perform rational row-pivoted elimination. Pivot swaps flip sign;
unscaled pivot products give determinant, with singular zero and empty one.
The four literal algebra hands include nontrivial swap and singular branches.

No scientific binary float is introduced: matrices, sums, products, divisions,
reference probabilities and exact comparisons use Fraction or exact integers.
All integer/Fraction divisions in the scientific path remain rational.
The selected matrices are real nonnegative; this is not a complex fixture set.
For Fhalf, inverse Fourier reconstruction at x=y=1/2 gives first row
(9,3,1,3)/16, matching the literal circulant. F0=J4/4 and F1=I4 are correct.

Lines 210-214 construct G=A^T A and H=I-G and archive all H principal
determinants before checking them. G is PSD by construction, H is symmetric,
and nonnegative ALL principal minors certify H>=0 exactly, hence contraction.
This includes singular H; an unpivoted-positive-definite test is not substituted.
Lines 224-229 index surviving subsets and their lost complements consistently
with P126; complement size is r, so signed environmental permanents have size<=2.
Both L and I-L are symmetric. All their principal minors, empties included,
are recorded before each PSD assertion; largest dimension is binom(4,2)=6.

Repeated output rows in lines 238-247 represent signal occupations correctly.
The quadratic numerator a^T L a and norm sum a_S^2 are divided by product n_j!,
with no extra r!, N! or subset multiplicity. No negative L term is clipped.
If norm=0, nonnegative amplitudes vanish and numerator is zero; ratio zero is
the correct total convention. Otherwise numerator/norm is the Rayleigh ratio.
The checks preserve all zero, loss and collision states rather than selecting CF.

All Gram binomial moments are recomputed, not copied from references. The
inversion sum has (-1)^(l-N) binom(l,N), and totals compare independently
to reference sector masses. Q=M_N may exceed one but must be <=binom(K,r).
The final FAIL includes all counts below max(0,K-2), without normalization.
The vacuum case uses A=[[]], empty Gram/permanent, L=[1] and I-L=[0].
Z4, zero columns, m<K and F1's identically zero lower sectors are legitimate
boundary probes. X4 is a physical contraction; its archived negative P96 q
is retained only as legacy_P96_surrogate_q, never used as q_P126.

## Population and completion, independently recounted by hand

There are one K0, one K1, four K3 and eight K4 cases. Source-size moments
therefore total 1+2+4*4+8*5=59; sectors total 1+2+12*3=39.
Using stars-and-bars for every total 0,...,K gives the population table's
361 full reference bins and 327 retained top states. P96 contributes 151
selected full bins, P107 three complete 70-bin laws contributes 210.
The signed-input H2/S3 cases are excluded solely for the input-model mismatch;
their 6+10 raw metadata bins still enter the 167-bin reference closure.

For K3 the two-operator minor count per case is 4+16+16=36; for K4 it is
4+32+128=164. Including K0/K1 gives 4+8+4*36+8*164=1468.
The nominal record sum is
1+4+2+361+14+59+39+1468+327+39+14=2328.
Every counter and completed-case list must match before a success status.
The enumeration has no seed, stochastic selection, stride or favorable filter.

Comparison mismatches are archived with match=false and accumulated through
the full population unless a distinct physical/integrity assertion fails.
That policy matches the MD; it is not a retry. Other caught exceptions preserve
state, traceback and the flushed prefix as INCONCLUSIVE_FIRST_FAILURE.
Nonzero mismatch count yields EXACT_COMPARISON_FAILED, never a prefix pass.
Hard resource kills can leave no finals: ROOT must treat missing finals as
inconclusive/invalid evidence, irrespective of an earlier matching prefix.

## Producer schema independence and provenance

P130 imports no P96/P107/P43 module or native/scientific package. Its permanent
DP and environmental quadratic form differ from the producers' implementations.
Read ONLY the relevant producer SOURCE serialization/definition sections:
P96 ee3592ef608b0b7ad19ba81babcdc369bf4da50e319f3f00baf868074d83c223,
P107 4e0973ebfe8a250dbf012719087dcb0b7390932acd3ddab4e7055b3808cb2bbc.
Their current file hashes match these pins. P96 exact_law expands a full
multivariate PGF by permutations; P107 uses its frozen Gaussian-integer
polynomial engine. P130 does not reevaluate either producer.

P96's spaced JSON writer matches the exact_case_start/raw/audit substring
filter. All 13 input plus 13 audit records and 167 unique dense raw occupations are
required; selected inputs are compared to literals and raw loss metadata
is checked. Its physical output p and legacy q are separately named.
P107's compact JSON writer matches the grid filter; source occupation order
matches P130's recursion. All 25 points and 9612 lines must be present,
while only the three declared diagonal B lists are consumed as comparison laws.
Original complete summary/failure states are required for both references.
This is compatible with those exact pinned bytes, not a universal JSON reader.

The authorization gate precedes catalog/algebra/ref-payload evaluation and
output creation. It requires ROOT_AUTHORIZED/true, exact seals/roles, unique
descriptor paths, twelve reference descriptors also present in the main table,
and a closure containing its active binding. Relative canonical non-symlink
regular files are required; every descriptor's SHA/bytes is checked, then
rechecked after computation, including the active binding's own digest.
The formerly uninitialized binding_sha is defined at source line 189 before
the provenance row at 196. I found no corresponding unresolved-name defect.

Minimum closure is 11 STATIC descriptors +12 reference files + active binding
=24 runner inputs, with explicitly allowed extra frozen review metadata.
The passive TEMPLATE lists only the static scaffold and has false authority;
ROOT must construct the actual full binding/runner closure, not execute it as-is.
Git seal labels alone do not prove original bytes. ROOT owns exact Git-blob
equality for all six files at each original seal, including opaque manifest/logs,
and must inspect the separate metadata binding before any launch.
This source review asserts no completed binding or verified future manifest.

## Resources, output handling and precise limitations

The planned command is the TEMPLATE's persistent Python3.11.15 -B invocation
with --binding research/P130_execution_binding.json; it was NOT executed.
Six thread variables must equal one; no native thread state is used or claimed.
Source CPU60 and FSIZE4MiB limits are real POSIX limits. The writer enforces
aggregate science4MiB, reserves64KiB, and separately checks summary/failure
joint size<=64KiB. Each emitted row is flushed, outputs are exclusive and
the data child must be fresh. No file is overwritten after a partial failure.

ROOT separately owns fresh ENTIRE output parent, wall90, combined runner logs
4MiB, single worker, all repeated input bindings, result presence/exit status
and raw sealing before interpretation. Parent existence is needed by the
source constructor; installed runner creates that parent. There is no RSS
or affinity enforcement claim. No runtime/output-size success is yet observed.
If a final serialization/cap failure occurs outside the main try, no clean
status should be inferred: retain the prefix and runner failure, zero retries.

A later finite pass could support these identities on this population, including
zero sectors and signs. It would not establish P126's universal theorem,
validate an FPRAS implementation, calibrate a device, show optimizer benefit
or prove a practical speed advantage. No input training/optimal-state mask occurs.

All 391 frozen lines were read before verdict; no raw reference law was previewed.
I am independent of P130's author, not independent of my P107 reference producer
or prior P126 review. No imports/AST/collection, numerical program, tests, RNG,
native/FPRAS/runner/validator/QPU call or manuscript change was performed.
Only this standalone review was written; static PASS is not execution authority.
