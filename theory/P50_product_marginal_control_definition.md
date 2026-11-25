# P50 independent-B-marginals control: pre-data definition and static cost

2026-11-25. Requested and assessed BEFORE source freeze, graph generation or
outcomes; adopted prospectively in ROOT `ded2cfb086fe791a9dfac1176d610ed880a33c7d`.
No code, numerical run, timing or source qualification is supplied here.
This is an elementary classical counter-control, not a new photonic mechanism.

## Exact mathematical law

Fix an isometry V in C^(N by r), CF input photons and q_ia=|V_ia|^2. Each
row has sum mu_i<=1. For the genuine B one-mode occupation, direct expansion
of annihilation operators gives

    E[(n_i)_h]=(h!)^2 e_h(q_i),
    G_i(z)=E[z^(n_i)]=sum_(h=0)^r h! e_h(q_i)(z-1)^h,
    p_i(t)=[z^t]G_i(z)
          =sum_(h=t)^r (-1)^(h-t) binom(h,t) h! e_h(q_i), 0<=t<=r.    (1)

Here (n)_h is the falling factorial. The coefficient h! e_h belongs to
the SHIFTED (z-1)^h basis and is NOT itself a probability. Sampling must use
the ordinary z^t coefficients p_i(t) after the transform. These are valid
one-mode probabilities of the stated normalized Fock source, sum to1, and
satisfy

    E[n_i]=mu_i,
    Var(n_i)=mu_i+mu_i^2-2 sum_a q_ia^2 = (Sigma_B)_ii.                (2)

The classical control draws independent integer variables X_i~p_i and an
independent iid jitter vector, then applies exactly the declared policy

    y=H(X-mu)+beta*zeta,   S=declared_bucket_topK(y,carried_priority).

It is the PRODUCT of the B one-mode marginals, not the bosonic joint law,
not a detector model and not a physical photon source. Do not reject, retry
or condition on sum X=r. The total count is random with mean r, and values
above/below r are legitimate raw outcomes of this classical arm. Its photon
budget is not this random total; it injects no photons.

The control matches INPUT one-mode marginals and input diagonal variances.
After H it has covariance H diag(diag(Sigma_B)) H^T; the B covariance is
H Sigma_B H^T. It does not generally match final marginals or final variances.
This differs from the separate independent FINAL-variance Gaussian control.
Adding a common scalar to every field entry does not change exact ranking,
and the frozen anchored tie rule preserves that null in exact arithmetic;
there is no reason to force the sampled total to r.

## Complexity and numerical implementation boundary

Compute all elementary symmetric polynomials of a row by the usual descending
degree update, then perform (1). Both stages take O(r^2) arithmetic per row:
O(N r^2) preprocessing, O(N r) saved PMF/CDF storage. Here a basis needs at
most100*(17+1)=1800 entries. Independent inverse-CDF sampling costs O(Nr)
with a simple bounded scan, or O(N log r) with binary search; no permanent,
global Fock law or exponential support enumeration is required.

This is plausibly modest at the declared sizes, NOT a measured promise that
ten full arms fit CPU60/wall90. The complete resource projection and actual
qualification must still justify the unchanged caps before the main run.
If they do not fit, preserve the failure; do not retry or silently truncate.

The existing P48 `repair_probability_row` plus
`factorial_marginal(row,True)` implements (1) using Fraction inputs and
Decimal80. Its alternating transform, row repair, negative-mass clipping,
normalization and float conversion have recorded finite errors. This is a
numerical implementation of the exact target law, not interval certification
or literal exact arithmetic sampling. Never rescale a genuine subunit row
to sum1. Record PMF normalization, minima, L1 repairs, mean/variance residuals
and any discrepancy between the table mean and the declared mu used to
center. Significant probability/support failures must be inconclusive.

All source construction, row tables, CDFs, RNG setup, draws, H, jitter, ranking,
fitness and tuning belong to THIS control's ledger. No PMF/covariance/CDF work
may enter B's allowance. In particular do not call the all-model marginal
builder on the B path merely to prepare this control. Give the arm the full
four-basis/alpha/beta grid: right rotation changes q and these marginals.
Its independently selected policy uses the same exact all-shot mean and
fresh evaluation protocol, not B's selected policy or best-looking outcomes.

## Fixtures and interpretation

- Vacuum gives all X_i=0. A monomial frame gives the same deterministic
  counts as B. Column phases/conjugation do not change q; carried row
  relabeling carries the product law and the subsequent field rule.
- At r1, X_i are independent Bernoulli(mu_i), whereas a physical photon is
  one categorical draw. Exclude this classical arm from the physical
  r1=B=D=b4=phase=sphere equality fixture. Nonconservation is intentional.
- For a balanced two-photon HOM pair, each of two output marginals has
  p(0)=p(2)=1/2. The product control has four outcomes (0,0),(2,0),(0,2),(2,2),
  each probability1/4; the physical B law only has the middle two, each1/2.
  This is a simple exact normalization/independence/nonconservation fixture.
- Check (1)–(2), valid support, exact small rational rows, normalized CDFs,
  all zero-probability bins and the separate mean centering diagnostic.

If this classical arm explains a putative B effect, no useful source-joint
correlation has been established by that effect. If B beats it, the physical
fixed-total constraint or second moments remain possible explanations;
neither hardness nor advantage follows. Conditioning the product on total r
would be another classical control, computable by a truncated sum DP in
O(Nr^2), but changes its marginals and is NOT the present arm. The current
definition is a useful cheap first veto, not an exhaustive classical boundary.

Actual work: direct creation-operator/combinatorial reconstruction and a
read-only inspection of the existing scalar P48 marginal functions, plus
the ROOT addendum. No imports, tests or calculations were executed.
