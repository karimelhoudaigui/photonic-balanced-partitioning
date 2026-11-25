# P48-B: fixed marked spectral source basis — prospective DEV veto

Owner encoding,25-Nov-2026. ROOT claim card **bfdff40926ad395a14f64260513b6ef21a1257f5**
(original B e30f75c plus pre-execution preparation amendment) is authoritative.
Earlier heat/Haar card **42572d4** is preserved and NOT
implemented: a Haar input basis would admit a spherical-coherent explanation
of averaged raw counts. P48 changes the occupied source basis and output
subspace, not the frozen negative P47 grid. All P33/P37/E05b/P45/P46/P47 evidence
and the manuscript remain unchanged. No P48 graph outcomes have been opened.

## Hypothesis and physical map

Can the graph-determined bosonic joint law, after its own marginal PIT and a
shared feasible decoder, improve balanced graph cuts beyond independently
selected D, Gaussian, coherent phase/sphere and strong feasible searches?
Projector/covariance changes and B>D on DEV alone cannot establish it.

For N=2K, r=K photons, weighted adjacency A, set L=diag(A1)-A and
Lhat=L/||L||op, or zero for L=0. Draw a single role-seeded vector of uniform
marks xi in[0,1], fixed before outcomes, and diagonalize

    M=Lhat+0.001 diag(xi).

The spectral encoder V consists of the FIRST r eigenvectors in ascending
eigenvalue order. No Haar occupied-basis rotation is applied. Each column's
physically null sign/phase is fixed by a maximum-magnitude component, ties
within1e-12 broken by the predeclared carried vertex priority. This is only
a gauge convention, not a source-basis rotation or a partition oracle.
The graph-blind encoder has V_(pi(i),a)=exp(2pi i i a/N)/sqrt(N), a<r,
with a role-seeded vertex order pi carried under relabeling.

Build U=[V,Vperp], using null_space(V*) ONLY for the orthonormal vacuum
complement. FIRST r columns remain exactly the specified V. CF input is
|1^r,0^(N-r)> in fixed source ports0,...,r-1. All N output modes correspond
to graph vertices; every Fock count, collision and zero mode is retained.
There is no old anchor/transfer block, CF rejection, hidden herald, loss
filter or conditional success renormalization. The isometry is independent
of the frontend anchor and every scored candidate. A known solution is
never loaded into the input. This is ideal passive simulation; actual QPU
mode/source/loss/compilation or throughput compatibility is not claimed.

All N-1 spectral gaps and residuals are recorded. The guard covers every
gap internal to the occupied basis PLUS the occupied/vacuum boundary,
i.e. differences lambda_(i+1)-lambda_i for i=0,...,r-1. They must exceed
1e-12. Unoccupied-complement degeneracies do not change the occupied CF
state and are recorded without an unjustified rejection. The extra vacuum
eigenvector used for classical rounding follows the declared eigensolver
convention; its actually scored discovery is shared regardless of a vacuum
degeneracy. Simple eigenvalues are generic with continuous marks, not an
interval-certified numerical fact. Eigen, occupied-orthogonality and unitary
max-entry residuals must be<=3e-12. Failed guards/PMF arithmetic retain the
graph, partial context, marks and reason as INCONCLUSIVE, never redraw.
The summary disallows positive acceptance and explicitly marks incomplete
populations; a successful subpopulation cannot be promoted as the full test.

For q_ia=|V_ia|^2, mu_i=sum_a q_ia<=1, P=VV*, the CF invariants are

    E n=mu, Cov_B=diag(mu)+|P|^2-2 q q^T.

P is generally nondiagonal; zero graphs can have a diagonal P and empty rows,
which remain valid. The ordinary PSD-Laplacian occupation-energy obstruction
still applies. The target functional is the nonlinear feasible decoder,
not a raw quadratic mean. Spectral filtering, eigensolvers and coherent-field
rounding are established classical tools; no novelty or hardness is inferred.

## Common discoveries and exact information available to controls

All graph, marker, order, matrix and PMF data are shared. Use the immutable P43
graph convention: ER p=.35 or RR degree4, weights1..9. A role-seeded common
initial feasible subset gets at most8 complete strict best-swap scans.
The cap is not a certificate unless a full scan finds no improvement.
Score ALL K^2 final-anchor swaps and record their Delta, with inside rows
and outside columns; this table is used only by classical matching, never
to construct V. The source ports remain0,...,r-1, irrespective of the anchor.

Before proposals, score both top-K and bottom-K rounding of EACH of the
r+1 lowest marked-Laplacian eigenvectors. Ties use the same vertex priority.
For EACH encoder also score/share top-K and bottom-K of mu and of EVERY
column q[:,a]. Score one labelled maximum-product distinct-destination
assignment with cost -log(max(q,1e-300)), in carried-priority row order.
The floor, number of affected entries, assignment and construction time are
recorded. This maximizes one labelled intensity product, not the permanent
sum or exact D probability of a support. These classical preparation
discoveries belong to Cref, including their sorting, matrix and scoring costs.
Also score zero-field q=ceil(K/2), pure greedy q=0, and all-zero-count
midpoint-PIT counterfactuals for all five discrete models, both encoders,
both lambdas. Every inspected marginal and final feasible cut is charged.
The best of EVERY scored common discovery is Cref and is available to every
arm/baseline. No frontend improvement is credited to a photon observation.
All numerical marginal and matrix work is charged ONCE to shared preprocessing.

The shared immutable P45 decoder seeds the highest q=ceil(K/2) fields, then
greedily completes to K using exact cut marginals with lambda0/1 field bias.
It costs100 informative units/proposal at N26,173 at N34. These counts track
informative evaluations; already known cuts can be recomputed inside measured
time, so they are not an exact counter of every repeated function invocation.
Completion can fill unclicked modes, outside the click-contained P44 premise.

## Seven primary arms and numerical marginal contracts

All seven use the SAME four encoder/lambda settings and their own unconditional
marginal transform u_i=F_i(n_i-1)+xi_i PMF_i(n_i), independent jitters per mode
and shot, separate from photon, coherent coefficient and multinomial RNGs.
True PMFs imply uniform marginals; the production tables are numerical,
without a certified interval, relative-tail or joint-copula guarantee.

B and D use one-mode generating coefficients r!e_r(q) and e_r(q). Species
have independent input groups of size AT MOST4, with per-group B marginals
convolved. Group assignment is fixed by a source-port permutation before
outcomes; no arbitrary internal-Gram shortcut is used. Coefficients use
Decimal80 and all corrections/minimum/sum diagnostics are saved. A numerical
PMF below-1e-12 or sum error>1e-12 makes the case inconclusive.

The two strong coherent controls use the same V:

- Continuous phase: z_a=exp(i theta_a)/sqrt(r), theta iid uniform[0,2pi),
  then counts~Multinomial(r,|Vz|^2).
- Spherical: z=g/||g|| for iid circular complex Gaussian g, then the same
  multinomial. Norm checks and all generation costs are recorded.

Their analytic marginal helper is imported unchanged from adaptive source
**6c980d3f684ef32295eeb394272f6218fbbc2402** (local cherry-pick642c2da),
SHA256 **a231a94578daf43993f62e393f1c58f90030a693ad2bf7722977ae65e181b2ac**.
Independent qualification **51d406e846a388e1e830641959b1274178de1389**
(local31b7b6d) recorded26 PASS, including24 exact Fraction fixtures, and a
validated v2 manifest. It uses q with sum mu<=1, NEVER row-normalizes to1.
Phase shift coefficients are

    c_h=(r)_fall_h h!/r^h [t^h] product_a sum_m q_a^m t^m/(m!)^2;
    spherical c_h=(r)_fall_h mu^h/(r)_rise_h.

Sphere uses a positive beta-binomial/binomial mixture. Vacuum r0, mu0,
mu1/r1 and mu1/r>1 are handled explicitly. The latter is generally NOT a
point mass. All helper PMF/CDF/correction diagnostics are saved. Its arithmetic
tolerance is1e-60 at precision80; passing it is not an interval error proof.
No empirical calibration is used in P48. The r+1-root rule appears only in
independent finite COUNT fixtures. Both production phase counts AND the
nonpolynomial rounding baseline below use CONTINUOUS phases throughout.

The caller represents float q exactly as Fraction. If a row exceeds1 solely
by at most3e-12, it subtracts the explicit excess from its largest component,
records the L1 repair and uses the SAME repaired q for B/D/b4/phase/sphere.
Any larger excess fails numerically. No row with mu<1 is rescaled. The tiny
repair describes numerical input error; it is not exact equality with the
uncorrected sampler. Both raw/used mass and every repair are retained.

Gaussian_Bcov samples its declared raw B covariance. Tiny negative eigenvalues
are clipped only above the-1e-10 failure threshold. Exactly empty rows are
zeroed in the factor to avoid amplifying numerical leakage. Phi divides by
the ACTUAL factor variance; exactly zero variance receives independent uniform
jitter. Target and factor residuals are separate. It need not match a photonic
PIT bivariate copula. IID uses independent uniform fields. Matching these
controls alone does not establish an irreducible multiphoton mechanism.

## Five strong feasible baselines

Anneal, spectral+swap, collective KL, shared-Delta block matching and
spectral_coherent_rounding each receive their own full3200/5536 informative
cut-score budget per graph/trial, matching the arm's32 decoded proposals.
No free portfolio maximum is taken. Matching keeps the inherited fixed-anchor
Bernoulli.25/.5 block proposals and Hungarian destinations, scoring REAL cuts.
The new rounding baseline cycles deterministically through
blind/phase,blind/sphere,graph/phase,graph/sphere. It scores top-K |Vz|^2,
then at most TWO complete strict best-swap scans (or the remaining budget),
logging every inspected candidate and global best. No CF/PIT restriction is
imposed on these stronger classical methods. Every solve/round/refinement is
charged in time and informative scores. Per-query timestamps support joint
observed-time AND score prefixes. Cold imports, recording and simulator costs
are reported; they cannot establish QPU latency or hardware runtime benefit.

## Frozen population, checks and outcomes

NEW DEV, no held-out or graph replacement: N26/r13 ER4802601,RR4802602;
N34/r17 ER4803401,RR4803402. Two trials0/1, four settings, eight draws per
setting/graph/trial =>256 per primary arm,3840 injected simulated photons
per optical arm. All tuning cells and costs remain; selection is independent
per arm on pooled DEV gain max(0,Cref-cut), null if all gains zero. Marks,
orders, species, production and baseline roles use fixed481010..481200
namespaces in the JSON spec. All data are retained even if Cref already
happens to be an optimum; no exact solver or optimum is consulted.

Source/helper/spec/contracts/tests are committed before any P48 experiment.
Root/physics review exact hashes before CPU authorization. Planned preflight:
24 integration cases plus26 helper cases. It independently enumerates small
Fock permanents/labeled particles, species4+1, covariance, all small phase
assignments, source-basis versus vacuum rotations, carried labels/marks,
zero-graph mu0/mu1, occupied/boundary/vacuum degeneracies, explicit repairs,
PIT/Gaussian factor variance, decoder/rounding budgets, retained numerical
failure, direct intensity roundings, labelled assignment optimum and one
local Clifford call. No DEV outcome appears in those fixtures.

One unique main only after PASS and explicit coordinator slot. CPU60/wall90,
one thread/worker, output32MiB, planned arrays256MiB. Runner enforces process
CPU/wall/log caps, script checks data bytes per graph. No Darwin hard memory
or affinity promise. No automatic retry, graph substitution or overwriting.
All partial/failure files survive. No QPU, credentials, remote messages or
paper changes. Decisions: REJECT frozen mechanism/budget if explained by
strong controls; FOLLOW-UP only for a signal worth fresh-seed/relabeling and
independent replication; INCONCLUSIVE for resources/numerical ambiguity.
No positive result or hardware gate can be accepted on these four DEV graphs.
