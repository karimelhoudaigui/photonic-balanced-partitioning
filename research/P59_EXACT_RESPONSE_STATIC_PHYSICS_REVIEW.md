# P59 exact fixed response: static physics and source review

**STATIC PASS for the separately planned16-item qualification.** No blocking
error was found in the exact source, harmonic convention, decoder or status
logic. This is not an executed qualification, full calibration or permission
to execute either. No imports, tests, graph, phase scan, source recurrence
or numerical computation were run by this reviewer.

Exact target: `3c18f2fba061573fef33e5c07467e6b92ab873e0`. The complete341-line
source,146-line tests, spec,130-line contract, both JSON contracts, claim
card and two precode derivations were read. Exact SHA256 pins:

| File | SHA256 |
| --- | --- |
| `research/P59_exact_fixed_response.py` | `f1d79ac3940b9c02826d0150dcea8470e2ccc9e5f995615b0ead9aa765de0374` |
| `tests/test_p59_exact_fixed_response.py` | `7f1da4d13df247082ee115b94232adadd898f2700de1d6efe781ba84a18433c6` |
| `research/P59_exact_fixed_response_spec.json` | `2b0a0564ad4dfb747bae25441cc9ceaac0c8d6590232d31a765b867a6e3ef1e2` |
| `research/P59_exact_fixed_response_contract.md` | `14f0cfe729847071c6f157e79e1e24b53483b55b0891dd819b6365e638b8b0ad` |
| `research/P59_exact_fixed_response_execution_contract.json` | `71ceff53aae136b403379fd5fa390ff1f1f06a6f7aeb710762cb483f1017e841` |
| `research/P59_exact_fixed_response_guards_contract.json` | `3448bc81c9810d0a1c0a97e1c04b05f74348e08d9d0624ad24d1d9948dfba6a8` |

## Matrix, source and Fock factors

The raw6-column construction uses omega=xi-1, omega^2=-xi and the stated
outputs2a+i/inputs2b+j convention. Only columns2,3 on odd rows carry zeta.
The LEFT rotation of ordered rows0,2 is exactly[[3,-4],[4,3]]/5. Those two
rows are phase free before rotation, so their mixing changes intensities
without making them phase dependent. The exact Laurent column Gram150I
and complete intensity table match the fixed device.

In particular the mixed row0 coefficients are3-4omega^b, giving squared
norms1,37,37; row2 coefficients4+3omega^b give49,13,13. The unchanged rows
have squared norm25. Division by150 yields the listed row/column-stochastic
q. This independently verifies the nonflat intensity table and the chosen
rotation sign. No photon source or output-index substitution is hidden.

Input is six identical single photons, one in each of six input modes;
eta1 and complete PNR counts are required. The paired input columns give
(E_b+zeta_b O_b)(E_b-zeta_b O_b). Thus the full creation polynomial has only
c0+c2*zeta^2, not a charge1 coefficient. Multiplying the ACTUAL six columns
in the source recurrence tests that factorization rather than assuming it
as the input. Exact zero intermediate coefficients may be deleted without
losing any final occupation: all462 final tuples are explicitly restored.

For raw Q coefficients, the normalized amplitude is
sqrt(f_n)*(c0+c2*zeta^2)/150^3, f_n=prod_i n_i!. Consequently probability
MULTIPLIES by f_n and divides by150^6, with no extra input factorial. This
is consistent with permanent divided by output factorials in the separate
fixture. The normalized-versus-raw likelihood formulas have been clarified
in the separate P60 delta ab929e8; the phase-average sampling table must
include f_n/150^6 even though that factor cancels in a row's rejection ratio.

### Fresh manual fixture reconstruction

Before reading the author's precode fixture derivations, I restricted the
actual source columns to x=x0,y=x1. Their paired product is

    (x^2-25y^2) [(33-40xi)x^2-25zeta^2 y^2]
                   [(-7+40xi)x^2-25y^2].

The x^4 y^2 coefficients are c0=(-35050,1000), c2=(175,-1000), c1=0.
Their cross product c2*conj(c0)=(-6958750,34875000). With f=4!2!=48,
-2*48*34875000/150^6=-124/421875. This independently confirms the sign,
factorial and raw-source normalization of the720-permutation guard. It
does not compute any of the15 aggregated decoded derivatives.

## Spectra, low moments and complete enumeration

For F2=alpha+beta*xi, the positive-harmonic probability convention gives

    f(phi)=u+(2alpha+beta)cos(2phi)-sqrt(3)beta sin(2phi).

Thus v=2alpha+beta and r=f'(0)/sqrt(3)=-2beta, exactly as implemented.
The stored sin2/sqrt3 value is r/2. All proof quantities remain Python
integers/Fractions, including zero values; clock readings alone are strings.
The cross uses c2*conj(c0), not its conjugate, which would reverse the slope.

The three even and three odd output coordinates give236 parity-allowed
occupations:28+90+90+28 for even totals0,2,4,6. The remaining226 are
structural zeros. c0 requires at least two even photons and c2 at most four.
These are checks over all462 rows, not conditioning or pruning. Complete
mass is required as a spectrum(1,0,0), so normalization holds for ALL phases.

The diagonal PGF implementation uses shifted coefficients h!*e_h(q), then
the exact binomial coefficient transform to a complete PMF. It is not a
binomial-distribution approximation. Six modes times seven counts give42
bins, including zero count. Joint factorial power vectors number6+21+56=83.
The ordered-index moment_target expression agrees term by term with the
previously derived full-square P1/P2/P3 theorem, including equal-index delta
terms and the coefficient12 on sum_a q_ia q_ja q_ka. The full-square,
full-CF, identical-input and unconditioned assumptions hold here.

## Decoder, class Gram and status scope

Every occupation compares all20 size-three subsets and averages uniformly
over all maxima. No complementary quotient is taken before tie averaging.
Each chosen cut has incident crossing sum3 and total9, which the kernels
and all aggregate spectra check. Tie counts{1,2,3,4,6,10,20} and LCM60 are
properties of the COMPLETE462-row decoder domain, including zero-weight
occupations. They are not frequencies of experimentally observed outcomes
or necessarily the tie support on positive-probability rows.

There are ten complementary cut classes. Two different classes have
crossing-vector dot product5; a class has self-dot9. The Gram is4I+5J.
Hence p_class=(crossing_class dot edge_means-5)/4. The code applies this
to the constant coefficient and divides each nonconstant harmonic by4,
then compares with direct class aggregation. Constants/mass/incidence
checks are consistent. All15 edge and10 class spectra are retained.

Nonzero r means an actual center0 decoded mean channel. If every r is zero
but some v survives, a finite cosine channel remains and the registered
gradient-at0 rule fails. Both must vanish to call the edge means invariant.
The Gram supplies a further scoped fact: if BOTH harmonics vanish on ALL
edges, the entire unoriented cut-class law is invariant, and therefore every
cut-cost tail on those six vertices is invariant too. This does not assert
raw PNR invariance (already disproved by the fixture), oriented-subset
invariance, another decoder's invariance or a universal optical obstruction.

## Curvature, controls and execution boundaries

The rational bound B_e=4(|v_e|+|r_e|) dominates
|f_e''|<=4|v_e|+2sqrt(3)|r_e| globally. For nonnegative weights A_e,
F=sum A_e f_e has |F''|<=M=sum A_e B_e and h=F'(0)=sqrt(3)sum A_e r_e.
If h is nonzero then M>0; phi=-h/M yields the conditional RAW mean decrease
h^2/(2M), and |phi|<=sqrt(3)/4. If h=0 the rule claims no strict gain. For
an objective normalized by total graph weight W>0, divide the raw gain by
W (or normalize h,M consistently). No graph is evaluated in this calibration.

The source/test/code inspection supports16 prospective guards: no test
calls calibrate(), main(), or full six-photon creation. Six-photon work is
only the one720-term permanent fixture. Full creation is used only for the
small two-photon HOM law. The13 declared inputs include both JSON contracts,
tests, source/spec/card, pinned derivations, instructions and software pins.
CPU20/wall30/thread1,4MiB separate scientific/log budgets and64MiB planned
logical workspace are declared; they are not measured execution or RSS.
Fresh output, exact serialization, pre/postcompression scientific caps and
first failure preservation are correctly scoped. No retry or automatic main.

P60 additionally requires the fixed two-phase bosonic-mixture control and,
for this finite calibration, the paid classical phase-average table/rejection
replacement once that table is verified. The calibration's nonzero response
would not defeat a classical exact-law sampler: N6 has462 Fock rows and ten
unoriented feasible cuts. Neither a nonzero phase channel nor its conditional
mean descent demonstrates optimized, scalable, equal-cost or hardware
advantage. These later controls need not be implemented to ask this exact
finite calibration question, but cannot be omitted from a positive algorithm
interpretation. No novelty or genuine-six-photon witness follows.

I authored the reused P56 low-moment note and P60 control analysis and
previously reviewed related source physics. These dependencies and shared
context are disclosed; this receipt is independent source scrutiny, not a
new blind physical replication. All actions were read-only git/shell text
inspection plus this new review write/commit. ROOT retains separate control
of qualification and main execution authorizations.
