# P80 rational killed-walk sampler: exact-source mathematical review

**Primary verdict: proved as written**, under the source's explicit rational
matrix promise and ideal exact Poisson/log-series random primitives. The
complete raw count law, planned-transition bound, polynomial-bit rational
setup and exact rational row coins pass the checks below. No correction to
this frozen source is requested. A full finite-bit sampler or total-runtime
bound remains an identified separate obligation, not a consequence here.

## Exact artifact, scope and provenance

Reviewed all345 lines of
`.local/p66-dark-barrier/theory/P80_independent_rational_loop_sampler.md`,
SHA256
`fcc0150467adda7b509018d2ec440e52e7e40e053b0fe8124aae384a930d5b02`,
original commit
`2c9810ece01584a8baae863d6d81047a3709d5e3`.
The exact hash and line count were independently checked. The author source
was not edited. The source records that ROOT supplied candidate formulas
before its derivation; this review is a subsequent exact-source audit,
not another before-author derivation, independent discovery or novelty claim.

Review date: 26 November 2026. Worktree `.local/p75c-code-review`, starting
at `e490d2261fdfc3ee7957bda4169c4b438d322c6d`. Only this report is written.
The old unavailable worktree index is untouched. The applicable AGENTS.md
and proof-audit obligations apply. Inspection used source text, hashes,
Git metadata and hand algebra. No code/import, AST, test, random draw,
numerical calculation, backend, circuit, QPU or manuscript action occurred.
No other P80 finite-bit work, runs, P79 files or P75 outputs were read.

The accepted P78 checkpoint was read for context. P80 independently derives
the Gaussian PGF and loop intensities, so no unread P78 proof or external
loop theorem is a load-bearing premise of the checks here. This audit
does not assess priority or literature novelty.

## Claim card and implication chain

Let m>=1 and Z be a finite rational, REAL SYMMETRIC, ENTRYWISE NONNEGATIVE
matrix with r=||Z||op<1. The output is the full PNR law of the normalized
pure zero-displacement Gaussian pair state with matrix Z. Vacuum, repeated
occupations, all number sectors and any later rejected classical events
must retain their raw probabilities. General signed/complex Z and changed
measurement models are outside this claim.

For nonzero Z define v=(I-Z)^(-1)1, V=max_i v_i, kappa=1-1/V and
P_ij=Z_ij v_j/(kappa v_i). Add an absorbing death state to complete each
row to one. An ideal Poisson population, log-series even lengths and uniform
roots propose killed walks. Only alive paths returning to their original
root contribute their departure-visit counts; every other mark contributes
zero. The algorithm returns the sum of those counts.

The dependency graph is

    norm promise + nonnegative Neumann series -> rational positive v
    Zv=v-1 and chosen kappa -> rational substochastic P plus death
    Gaussian normalization/number weighting -> complete PNR PGF
    positive convergent trace-log -> even rooted-loop intensities
    marked Poisson + telescoping v ratios -> exactly those intensities
    length expectation + resolvent norm -> Wplan<=m^2*nbar
    integer scaling/minors -> polynomial rational setup representation/work
    rational integer weights + bit rejection -> exact local row coins.

Exact Poisson and log-series draws are named ideal inputs, not proved
finite-bit implementations. The setup-bit and transition-coin claims do
not silently discharge that last sampling obligation.

## Resolvent, rationality and the killed chain

Because r<1, the Neumann series converges in operator norm to (I-Z)^(-1).
Nonnegative summands show v_i>=1, and Zv=v-1 follows exactly. Rational
linear algebra computes v without evaluating the infinite series. If Z
is nonzero, at least one positive entry of Z1 gives V>1, hence0<kappa<1.
If Z=0, the source correctly returns vacuum before dividing by kappa or
normalizing a log-series distribution.

The row sum is (v_i-1)/(kappa v_i)<=1 because kappa is the maximum of
1-1/v_i. All entries and death probabilities are nonnegative rationals.
Zero rows have v_i=1 and die immediately; no v_i vanishes. Reducible
matrices require no arbitrary Perron-coordinate division or component
root reweighting. The extra death state is classical bookkeeping, not
an extra optical mode.

The source's optional r<=kappa check is also correct: choose a nonzero
eigenvector coordinate maximizing |x_i|/v_i. Nonnegative Z and Zv<=kappa v
give |eta||x_i|<=kappa|x_i|. Symmetry then identifies r with the largest
absolute eigenvalue. Neither r nor an eigenvector is needed for setup.

## Complete raw PGF and loop proposal factors

Orthogonal diagonalization of real symmetric Z and the one-mode central-
binomial norm series give squared norm det(I-Z^2)^(-1/2) for the pair
exponential. Weighting the state by product_i z_i^(N_i/2),0<=z_i<=1,
replaces Z by B=sqrt(D) Z sqrt(D), D=diag(z). Squaring the weighted norm
therefore gives

    G(z)=sqrt(det(I-Z^2))/sqrt(det(I-B^2))
        =sqrt(det(I-Z^2))/sqrt(det(I-(DZ)^2)).

For positive D, DZ and B are similar; continuity covers zero entries.
All determinants under these square roots are positive in this domain.
G(1)=1, and G(0) is the true Gaussian vacuum mass. No collision-free or
photon-number conditioning was inserted.

The trace-log series converges absolutely because the relevant even traces
are bounded in absolute value by m*r^(2l). Expanding the trace explicitly
gives one nonnegative product for each indexed rooted closed walk of
length2l, with intensity weight(w)/(2l). There is no additional division
by reversal, root rotations or periodicity; the trace already specifies
the indexed tuples. Terminal return is not counted a second time in the
departure-visit monomial. Diagonal self-loops and repeated vertices are
included. Summed intensity is -log det(I-Z^2)/2<infinity, so the compound-
Poisson distribution is well defined and has the stated complete PGF.

Write L=-log(1-kappa^2), Lambda=mL/2. For a specified alive closed path,
the product of transition probabilities is

    product_t P_(i_t,i_(t+1))
       =kappa^(-2l) weight(w) v_terminal/v_root
       =kappa^(-2l) weight(w).

Multiplying by the Poisson population, length law and uniform-root factor
gives exactly

    (mL/2)*[kappa^(2l)/(lL)]*(1/m)
       *kappa^(-2l)weight(w)=weight(w)/(2l).

Thus no survival conditioning or substochastic-row renormalization is
missing. A dead or nonreturning mark has zero count vector and PGF1;
these marks still consume proposal work. The marked-Poisson identity
E[F(z)^J]=exp(Lambda(F(z)-1)) proves the full output PGF. Finite Lambda,
finite almost-sure lengths and finite planned walks imply almost-sure
termination in the stated ideal random-primitive model, not a deterministic
time or memory cap.

## Independent reconstruction of the crucial work inequality

The log-series expectation is
E[2l]=2*kappa^2/[(1-kappa^2)L]. Multiplication by E[J]=mL/2 yields

    Wplan=m*kappa^2/(1-kappa^2).

This charges every planned step, including unused tails after death.
Actual transitions are bounded pathwise by that planned count. Each mark
plans at least two steps, so E[J]<=Wplan/2.

Differentiating G(u,...,u) at1, or summing loop jump sizes, gives

    nbar=Tr[Z^2(I-Z^2)^(-1)].

For nonzero Z, symmetry gives an eigenvalue of absolute size r, so
nbar>=r^2/(1-r^2). This uses the emitted full-source mean, not accepted or
detected photons. The quantity is rational for rational Z.

Now v-1=(I-Z)^(-1)Z1. Euclidean norm bounds give

    V-1<=||v-1||_2<=sqrt(m)*r/(1-r)=a.

Both x/(1+x) and x^2/(1-x^2) are increasing on their applicable positive
domains. Therefore

    kappa^2/(1-kappa^2)
       <=a^2/(1+2a)
        =m*r^2/[(1-r)*(1-r+2sqrt(m)r)]
       <=m*r^2/[(1-r)*(1+r)]
       <=m*nbar.

The middle direction is essential and correct:
1-r+2sqrt(m)r-(1+r)=2r(sqrt(m)-1)>=0. All denominators are positive.
Multiplying by m proves Wplan<=m^2*nbar. No spectral gap, connectivity,
positive-entry lower bound or Perron oracle entered this argument. The
zero matrix was already handled separately; m=1 gives equality for a
nonzero positive diagonal singleton.

## Polynomial-bit setup and exact row coins

If input numerators/denominators have at most B bits, multiplying all m^2
denominators gives a positive common Q with log2 Q<=m^2 B. M=Q(I-Z) and
the right-hand side Q1 are integer data of polynomial bit length. A minor
of order k has at most k! products of k bounded entries, giving polynomial
bit lengths in m,B. Cramer's ratios therefore bound each exact v_i's
reduced numerator and denominator. Rational comparisons, kappa and row
products/quotients/sums preserve polynomial bit sizes.

This representation argument alone would not make a factorial determinant
expansion efficient. The source separately supplies a valid polynomial
method: M is symmetric positive definite, so each leading elimination
pivot is nonzero. Its Schur-complement entries and transformed right-hand
side are ratios of minors by the block determinant identity. Reduced-
fraction Gaussian elimination has polynomial-sized intermediates and
O(m^3) arithmetic operations. Back substitution can likewise keep reduced
fractions of polynomial size: its solution entries have the Cramer bounds,
and intermediate sums contain at most m products of such bounded terms.
Ordinary exact integer arithmetic/gcd on these bit lengths gives polynomial
SETUP bit work. No numerical stability or floating elimination is assumed.

The promise r<1 need not be evaluated during setup. If input certification
is desired, rational symmetry/nonnegativity and exact positive definiteness
of both I-Z and I+Z suffice for symmetric Z to have all eigenvalues in
(-1,1). An uncertain measured matrix is a different input-error problem.

For a rational row, including death, choose a positive common denominator
q and nonnegative integer weights summing exactly to q. Uniform integer
selection from0,...,q-1 via ceil(log2 q) unbiased bits, rejecting integers
>=q, is exact. The expected number of attempts is2^ceil(log2 q)/q<2 for
q>1; q=1 is deterministic. Row common denominators and prefix weights
remain polynomial-bit quantities. Thus exact row transitions do not hide
irrational Perron ratios. Rejection gives almost-sure finite and expected
polynomial local bit work, NOT a deterministic upper bound on the number
of bit attempts for every random sequence.

## Boundaries, missing implementation obligations and decision

The zero source, zero rows, reducibility, diagonal singleton, bipartite
period-two support and negative eigenvalues of an entrywise nonnegative
symmetric matrix all satisfy the proof's actual premises. For a singleton
[s], kappa=s and its loop PGF is sqrt((1-s^2)/(1-s^2 z^2)). For the two-mode
off-diagonal pair, all alive even paths close and the PGF is
(1-s^2)/(1-s^2 z1 z2). These are hand-derived symbolic consistency checks,
not numerical validation. Independent colors and later classical event
filters preserve the corresponding product/rejection probabilities when
their full costs are retained.

Lambda and normalized log-series probabilities still contain logarithms;
rational kappa does not by itself supply an exact finite-bit Poisson or
length generator. The source explicitly leaves these primitives, full
bit-work/precision contracts and any rounded sampler's TV control open.
No alternative P80 finite-bit work was used to close that dependency here.

Wplan is a count of planned transitions. It omits paid setup, primitive
generation, dense row selection, output initialization, storage and scoring.
Near criticality nbar and expected work can be large, even exponential in
input bit length. The theorem does not claim polynomial total time in B,
bounded output memory, a hardware-clock comparison or free rare-event
conditioning. Reusing immutable setup for fixed Z is valid; changing Z
requires its new setup.

| Obligation | Review result |
|---|---|
| Exact345-line source and honest candidate provenance | Passed |
| Rational positive v, kappa and substochastic/death rows | Passed |
| Raw Gaussian PGF, even-rooted weights and factor1/(2l) | Passed |
| Uniform-root intensity and death/nonreturn bookkeeping | Passed |
| Planned-work formula and Wplan<=m^2*nbar | Independently reconstructed; passed |
| Rational setup representation and polynomial setup algorithm | Passed with exact reduced arithmetic |
| Rational local row coins | Exact, expected local bit work; unbounded rejection tail |
| Complete finite-bit random primitives and total runtime | Explicit separate obligations |
| Global Gaussian classicality, optimizer/hardware/novelty claims | Not established or inferred |

No load-bearing mathematical gap was identified in the frozen source's
actual ideal-model and rational-setup statements. KEEP that theorem with
its random-primitive and resource limits. A full implementation requires
separately validated exact random-variate generation and a complete cost
contract before throughput or quantum-comparator conclusions. This audit
authorizes no computation or hardware action. Final hand proofreading
checked death/return conventions, determinants, even-loop/root factors,
inequality directions, rational bit sizes, boundary cases and the distinction
between planned work and complete sampling cost.
