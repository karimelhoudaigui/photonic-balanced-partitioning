# P80: rational setup and bounded-bit raw-count approximation

ROOT accepts the two separately reconstructed and exact-source-reviewed
mathematical constructions below. Composing their explicitly verified
premises gives a finite-bit approximation theorem for the COMPLETE raw
PNR law of a rational, real symmetric, entrywise nonnegative Gaussian
pair matrix. This strengthens P78's ideal-arithmetic statement. It is a
classical simulation result, not a positive graph optimizer or a novelty
certificate. No executable finite-bit implementation was run.

## Exact evidence and dependency closure

ROOT read every line of both sources and both exact-source audits:

| Object | Original commit | SHA256 | Lines |
| --- | --- | --- | ---: |
| `theory/P80_independent_rational_loop_sampler.md` | 2c9810ece01584a8baae863d6d81047a3709d5e3 | fcc0150467adda7b509018d2ec440e52e7e40e053b0fe8124aae384a930d5b02 | 345 |
| `research/P80_finite_precision_loop_sampling_route.md` | 57b3ecceb366dd7cc6e69b55eae7451eaed67ec3 | 5fa9ce9441691b639a8208b536172fa67ba6972edb01ea7bb45990eb0050b10b | 155 |
| `theory/P80_RATIONAL_EXACT_HASH_REVIEW.md` | 1db79063c76089353f724befd3bf33e75a74d824 | a58616b86fd51a24bab65bef12a8ed6caaec17936a654ebcf581b672d3186148 | 257 |
| `theory/P80_FINITE_BIT_EXACT_HASH_REVIEW.md` | 41a572e2717190a49c335a0f0ef37fe799dc0daf | e8459ea8f2012ae8b550c3df3f89e5f1c5a0ab8c72abcd1fdb83c34198a755a9 | 246 |

ROOT supplied candidate formulas before the two first reconstructions.
Their authors did not read each other's P80 source before freezing.
The subsequent exact-hash reviewer read the sources; this is an audit,
not another before-reading derivation. ROOT independently checked the
change of measure, cost algebra, flag coupling, rational Poisson tables
and bit bounds. No gap requiring a source correction was found.

The finite-bit source deliberately states assumptions A (the optical
full-count law) and B (the rational planned-work bound). A is discharged
by accepted P78 and the independently repeated rational loop argument.
B is discharged by the 345-line rational construction and its exact
audit. This checkpoint composes them; the original conditional source
and its historical review remain unchanged.

## Rational replacement for the Perron oracle

Let Z be an m-by-m rational real symmetric entrywise nonnegative matrix
with spectral norm r<1. The source is pure, undisplaced and specified by
Z itself at the counted output. For Z=0 return the exact vacuum. Otherwise
put v=(I-Z)^(-1)1, V=max_i v_i, kappa=1-1/V and

    P_ij=Z_ij*v_j/(kappa*v_i).

The vector v is rational and >=1; Zv=v-1. Thus P is rational and
substochastic. A death state supplies each row's missing probability.
All planned steps, including steps of paths rejected by death, remain
paid. Uniform roots and closed surviving even paths have the same loop
intensities as P78 because all v factors telescope around a loop.
There is no irreducibility, minimum positive entry or Perron-vector
oracle premise. Matrix setup and rational coin costs are included.

With S=m*kappa^2/(1-kappa^2) and the emitted mean photon number
nbar=Tr[Z^2(I-Z^2)^(-1)], the proved bounds are

    S <= m^2*nbar.

One derivation uses V-1<=sqrt(m)*r/(1-r) and
a^2/(1+2a)<=m*r^2/(1-r^2), where a=sqrt(m)*r/(1-r).
Exact rational matrix setup has polynomial bit cost in m and the input
encoding length B. The rational note alone still uses ideal Poisson and
logarithmic-series primitives; those are removed by the next construction.

## Bounded-bit theorem and explicit failure records

Given rational 0<epsilon<1, there is a bounded random-bit algorithm with
worst-case bit/time/memory cost polynomial in

    m, B, nbar, 1/epsilon

(including epsilon's encoding), whose law on raw occupation vectors plus
a distinct FLAG differs in TV by at most epsilon from the target PNR law
embedded with zero FLAG mass. Vacuum, all collisions and the unbounded
target tail are retained in the theorem. The algorithm never conditions
away a failed prefix. The dependence on numerical nbar and 1/epsilon is
essential; this is not polynomial in their logarithms alone.

The mechanism marks independent Poisson populations at every half-length
l, with rational mean m*kappa^(2l)/(2l). Set

    T=2*max(1,ceil(4*S/epsilon)), M=T/2, beta=S/(T+2).

Sample only lengths1..M, recording FLAG on a total planned-step overflow
or on a separate beta flag coin. In the proof, the latter coin can be
coupled to cover every omitted long proposal while staying independent
of the retained short populations. This costs at most beta+S/T<=epsilon/4;
the algorithm never needs to calculate the omitted-tail probability.

Finite rational Poisson tables use w_j=a^j/j!, a finite upper enclosure
U=sum_(j<n)w_j+2*w_n>=exp(a), and an explicit overflow outcome. Choosing
n>=max(2,6a,log2(4/delta)) bounds the enclosure deficit. Downward dyadic
rounding of each finite mass assigns residual mass to overflow, retaining
nonnegativity and a TV budget delta. No unbounded random-bit rejection
loop remains. All M tables, capped occupancies, roots, row transitions,
flag coin, setup and outputs enter the complexity analysis.

The full proved TV budget is at most

    epsilon/4 + epsilon/8 + epsilon/8 + epsilon/8 = 5*epsilon/8.

The last three terms cover all Poisson tables, the flag coin, and the
at-most M roots plus T transitions, respectively. A FLAG may be mapped
to a designated occupation vector if a vector-only interface is needed;
TV contracts, but the flag bit must remain recorded. A flagged zero is
not a genuine measured vacuum. No efficient rare-CF or favorable-cost
conditional sampler follows from this absolute-error statement.

## Scientific consequence and remaining limits

Within this rational nonnegative-matrix class, complete raw photon-count
statistics have a constructive polynomial-parameter classical weak
simulation. A graph encoding in this class cannot rely simply on a
claimed absence of such a classical raw sampler. All sampling/rejection,
compiler, adaptation and classical setup costs still need an explicit
matched comparison in an optimization benchmark. This theorem supplies
no measured wall-time ordering or useful constants for this laptop/QPU.

P79 is a separate finite validation of a floating, Perron-based loop
implementation. Its NumPy Poisson/logseries variates do not implement
this bounded-bit theorem and receive no TV certificate from it.
Signed/complex non-gauge pair matrices, displacement, changed quantum
inputs, later coherent mode mixing and generic finite-Fock passive
circuits are outside the positive-loop premise. Known loop ingredients
were attributed in P78; P80 originality remains unresolved. The requested
positive optimum-blind optimizer goal stays OPEN; paper/main/QPU stay frozen.

Subsequent bounded primary check: P85 authenticates the same pure raw-PNR
class in Quesada–Arrazola(2020), where approximate classical simulation was
already proposed. Its estimator/precision guarantees are distinct from this
proved contract; no first broad nonnegative-GBS simulation attribution is
justified. See reports/P85_ROOT_ATTRIBUTION_CHECKPOINT.md and the original
versioned source links. The present exact theorem/TV proof is unchanged.
