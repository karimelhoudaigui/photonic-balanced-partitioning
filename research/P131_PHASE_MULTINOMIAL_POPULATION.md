# P131 prospective exact qualification population and implementation binding

During P131 authoring no import, AST, collection, test, scientific execution, RNG, or raw-reference payload read occurred.
No authorization is conveyed by this document or the inactive contract TEMPLATE.
ROOT must inspect the complete frozen source and a separate non-author review, bind actual immutable references,
then give distinct authority for one bounded run. Zero failed retries; no calibration or precision rescue.

## Production scope and exact finite-bit semantics

`P131_phase_multinomial.py` is standalone standard-library code, with an explicit caller-owned fair-bit callback.
There is no implicit RNG, seed, NumPy, Perceval, native sampler, or producer import.
Its supported matrices are rectangular m-by-K Gaussian-rational contractions with m>=1 and 0<=K<=7.
M is the smallest power of two greater than K, so M<=8; K=0 has a separate zero-bit vacuum branch.
K>=8 returns `UnsupportedScope` with status UNSUPPORTED and bits_read=0, before any bit callback.
This bounded implementation does not implement the general-M theorem in P129.

Every matrix is checked by exact Hermitian Schur-complement PSD elimination of I-T†T.
Zero pivots require a zero remaining row/column; no numerical eigenvalue, clipping, or tolerance appears.
The only phase approximation is inward eighth roots: a=floor(S/sqrt(2))/S, using integer square root.
S is the smallest power of two with 2/S<=delta=epsilon/(4K); axes are exact.
The integer residuals `S²-2n²>=0` and `2(n+1)²-S²>0` certify the branch.
Diagonal root error squared is <2/S²<=delta²; all approximants lie in the unit disk.
There is no adaptive precision or retry when a comparison fails.

epsilon is exactly 1/1024. D=2^ell is the smallest power of two >=2Km/epsilon.
For each phase context compute rational p_j=|(T zhat)_j|²/K, integer h_j=floor(D p_j), and loss h_0=D-sum_j h_j.
The implementation orders all signal rows first, with loss last in its integer CDF.
Each sample consumes exactly K phase blocks of log2(M) bits, then K categorical blocks of ell bits.
All blocks are fully consumed even for zero T; counts include vacuum/collisions, total signal <=K.
Invalid callback values are rejected with their observed return representation, never clipped or replaced.

## Frozen literal case population

| case | m | K | M^K | full signal bins | eta certificate |
|---|---:|---:|---:|---:|---|
| V0 | 1 | 0 | 1 | 1 | 0 |
| U1 | 1 | 1 | 2 | 2 | min(trace,Gershgorin) |
| H2 | 2 | 2 | 16 | 6 | same, signed real matrix |
| D3 | 3 | 3 | 64 | 20 | same |
| R3a | 1 | 3 | 64 | 4 | same |
| R3b | 1 | 3 | 64 | 4 | same |
| S3 | 2 | 3 | 64 | 10 | same, signed real matrix |
| B4 | 2 | 4 | 4096 | 15 | same |
| D4 | 4 | 4 | 4096 | 70 | same |
| Z4 | 2 | 4 | 4096 | 15 | 0 |
| R4 | 1 | 4 | 4096 | 5 | min(trace,Gershgorin) |
| C3 | 2 | 3 | 64 | 10 | same |
| X4 | 1 | 4 | 4096 | 5 | 1, endpoint diagnostic |
| G4 | 4 | 4 | 4096 | 70 | 1, endpoint diagnostic |
| G4atten | 4 | 4 | 4096 | 70 | 1/16, exact spectrum |

The first13 matrices are literal P96 cases, in their original order, including the original physical trace1 counterexample X4.
That P96 counterexample concerns its different trace<=1/2 theorem; it is not an unphysical matrix.
For real P96 matrices the validator constructs Gram entries independently and uses min(trace, maximum absolute Gram row sum).
It also checks eta*I-T†T by the production exact PSD certificate, recording the pivots.
G4 has literal circulant first row `(15/32,7/32+i/16,3/32,7/32-i/16)`.
It is checked against F diag(1,1/2,1/8,1/4) F† with F_jr=(-i)^(jr)/2 and exact Fourier orthogonality.
G4atten is exactly G4/4; its intensity transmission bound is 1/16.

There are exactly15 cases, 29,011 phase contexts, 307 reference/output bins, and300 input-occupation PGFs.
The13 P96 cases contribute20,819 contexts/167 bins; the two added matrices contribute8192 contexts/140 bins.
All contexts, even duplicates/zeros, are enumerated and recorded, with no random source.
All signal occupations of total0..K are retained, including zero probabilities.
The ideal law matches the mean exactly; dyadic rounding is only approximately mean preserving, with its discrepancy recorded.

## Independent exact oracle and comparisons

The validator uses its own complex-rational class and sparse labeled-column subset DP permanent.
It does not import P96, P107, P110, or their matrix/PGF helpers.
For input occupation a with total K, its normalized Fock PGF is
`per(M(z)[a,a])/a!`, where `M(z)=I-T†T+T†diag(z)T` and BOTH input indices repeat according to a.
The ideal phase-twirled mixture weight is independently `K!/(K^K a!)`.
Both factorial divisors are required; a hand case with a=(2,0), T=(1/2,0) has probabilities9/16,3/8,1/16.
Every input PGF and every final bin is archived before comparisons are counted.
The finite law is an exact integer multinomial sum over ALL contexts, divided by M^K D^K.
No Monte Carlo, permanent FPRAS, floating probabilities, or tolerance appears.

P96 references are all167 original `exact_raw` p values.
P107 references are all5670 dense B/B_moment coefficients, divided by65536 and evaluated exactly at x=1/2,y=1/4.
The70 attenuated references are derived by exact common signal thinning of the70 base bins, intensity1/16; no new producer run is assumed.
Check full normalization/nonnegativity/realness, exact ideal means, finite-ideal TV<=epsilon,
reference-ideal TV<=tau, reference-finite TV<=tau+epsilon, and tau<=min(1,(K-1)eta²/2).
tau is the exact binomial average of 1-(K)_L/K^L, not a sampled estimate.

The eta=1 tests are explicitly endpoint diagnostics outside P129's strict eta<1 header.
Their separately stated endpoint proof is simply R=T, uniform loss1=identity, L=K;
the same fixed-sector distance is 1-K!/K^K, and contraction gives its output bound.
The finite-bit positivity/coupling proof already uses only ||T||<=1.
This endpoint extension does not silently change the frozen P129 source.

Twelve literal hand groups precede reference reading: vacuum, four unary CDF endpoints,
two H2 full-block CDF vectors, doubled-input factorial PGF, unsupported-K8 rejection,
noncontraction rejection, zero-pivot/nonzero-row rejection, and bool-bit rejection.
They consume fixed literal vectors only; no `getrandbits` provider or actual random draw is invoked.

## Provenance, limits, and failure semantics

The inactive TEMPLATE specifies the complete static schema paths. ROOT must copy/bind actual frozen source bytes if absent here.
The future active binding excludes its own descriptor/selfhash but includes itself once in runner execution_artifacts.
It must bind all six P96 files to original seal240c7e5518fbcd69d8f22bbe5e8ead3c1bbbc9c1
and all six P107 files to original seal99f2d98d93f13c7fc088218bfb06ff39af4c40e9.
Hash/size and original Git blob equality are checked BEFORE any reference payload is parsed.
Source schemas are fixed at P96 0eabdadc70c2b7085c40b22183320e8655d00e1d and P107 6d9c16cde14ff25d51593c75607c712dcd7e9326.
The persistent Python3.11.15 CLI interpreter and actual observed external pin hashes are required; no SHA is invented in the TEMPLATE.
All six thread environment variables must already be1 and -B must be active; no OS-thread/native-thread claim is made.

Prospective caps: CPU120s, wall180s, one worker, logs4MiB, scientific aggregate8MiB uncompressed.
Each summary/failure file is capped64KiB; records retain a combined128KiB final reserve.
RLIMIT_FSIZE is8MiB per file; the writer additionally enforces the aggregate science cap.
Logical memory plan is256MiB, not hard RSS enforcement. No source calibration or benchmark supports these caps.
Static work bounds:300 population DP permanents plus one hand DP permanent; each K<=4 permanent has <=32 labeled-column transitions,
each transition multiplies a <=70-term polynomial by a <=5-term linear polynomial.
Finite aggregation has <=29,011*70*5 small-integer factor accesses, with one compact context row each.
These are finite work/space bounds, not runtime guarantees; resource exhaustion is preserved as inconclusive.

Ordinary scientific comparison failures are all recorded and accumulated while subsequent registered comparisons continue.
An exception/provenance/resource/output failure preserves its first prefix and stops; no retry or substituted zero is allowed.
Final summary distinguishes completed cases, a partial current case, and NOT_RUN cases.
A hard kill may leave only the flushed record prefix and runner metadata; missing final files cannot constitute PASS.
Raw outputs, logs and manifest must be committed before interpretation. No optimizer, hardware, equal-wall claim, positive signal, novelty, or QPU result follows.
