# P37 independent proof review

**Verdict: proved as written.** Under even m>=8, k=m/2, k<=N<=m and
0<eta<1, the two per-attempt candidates, four per-injected-photon candidates,
root uniqueness/order and stated fixed-lambda asymptotic follow. No missing
implication or valid counterexample was found. This is a correctness verdict,
not a novelty, graph-quality, hardness or advantage claim.

## Target and independence

Target commit: `d402374b21a812de1d1b5658fac37d294a20a035`.
Raw proof: `theory/phase3_loss_source_selection.md`, SHA256
`fda5160d1d4eb232f67eae09cfcfabf3024822ea1e0720ef639267374a642807`.
Known-law contract: `research/phase3_threshold_contract.md`, SHA256
`00ef816e77d1238590b8cddccde1eda3b0822620c2d6b4cbdd66879cf9dbddc9`.

Reviewer `/root/physics` was not the proof author. The raw proof and known-law
contract were read directly; the coordinator's verdict, report, numerical
probe and previous P37 results were not read or used. A pre-existing clean
worktree at the requested base was limited to these sources with sparse
checkout. The author/status header supplied no evidence for this verdict.
The reconstruction and exact check below were independent of the coordinator's
implementation. No source/proof, shared registry, manuscript or QPU changed.

## Claim card and dependency graph

Each attempt injects N distinct single photons independently of a Haar mode
unitary. Uniform independent loss has survival eta; acceptance is exactly k
threshold clicks. Failed attempts, including complete loss, count. The compared
functions are S_N=E h(L), L~Bin(N,eta), and b_N=S_N/N. Source choices are
restricted to integers k,...,m. This is an ensemble-averaged count law, not a
claim about every fixed interferometer or a trained graph solver.

The dependency graph is:

1. Known Haar uniform-Fock law + uniform-loss commutation -> binomial mixture.
2. Stars-and-bars expression for h -> two exact adjacent lossless ratios.
3. Coupling or size bias -> adjacent S_N and b_N differences as binomial
   expectations of fixed coefficient sequences.
4. One sign change -> one interior zero; increasing likelihood ratio under
   increasing binomial size -> strict root order.
5. These signs + source cap -> all global maximizers and boundary ties.
6. Fixed-lambda loss moments + peak-normalized estimates -> first-order ratios.
7. Unique finite roots + two fixed-lambda sign brackets -> root limits.

| Obligation | Status | Decisive reconstruction |
|---|---|---|
| Haar and uniform-loss dictionary | Passed | Primary results and independent stars-and-bars count |
| h ratio and difference signs | Passed | Exact cancellation shown below |
| g ratio and size-bias shift/factors | Passed | R~Bin(N-1), eta^2, argument R+1 checked |
| One-crossing lemma, zeros and endpoints | Passed | Strict monotonicity after division by first negative power |
| Strict order of roots | Passed | Increasing likelihood ratio and negative new coefficients |
| Global two/four-candidate conclusions | Passed | Adjacent sign sequence excludes nonadjacent maxima |
| Smallest m=8 | Passed | Sign boundary4.8; exact rational polynomials/root brackets |
| eta=0, eta=1 and lambda=0 | Passed | Exclusions/ties and zero-loss expansion checked separately |
| Fixed-lambda expansion including tails | Passed | Peak normalization prevents a small-denominator tail error |
| Root-limit sandwich | Passed | Correct correspondence s=1,2,3 to each adjacent root |
| Expected first-success photon interpretation | Passed with stated independent-refresh condition | Constant source N and IID attempts |
| Fixed-U, fixed-budget or graph-quality extensions | Excluded | Not asserted by this proof |

## Known-law source check

Bouland et al., arXiv:2312.00286v2, version19 March2025, Section4, Lemma1,
Eq.(6), gives the click-count probability under the uniform occupation law.
Its n,c map to this proof's surviving photon count l and click target k.
Choose k occupied modes and distribute l photons positively among them:
there are C(m,k)C(l-1,k-1) such occupations, out of C(m+l-1,l).
This verifies the exact h(l) in the stated range. [Primary source](https://arxiv.org/html/2312.00286v2#S4)

Arkhipov–Kuperberg, arXiv:1106.0849v1, Proposition1 and Corollary2, identifies
the Haar-twirled state with the maximally mixed state on the fixed-photon
symmetric sector for any input independent of the Haar unitary. Conditional
on L survivors, the input mixture remains independent of that unitary. Uniform
loss commutes with passive mode evolution, and independent photon survival
gives L~Bin(N,eta), so mixing h(L) is legitimate. Mode-dependent loss or
conditioning on all N surviving would change this argument. [Primary source](https://arxiv.org/html/1106.0849v1)

The exact primary versions were opened and the relevant statements/proofs read
on2026-11-22. These source-dependent implications are verified; the internal
root theorem is not being attributed to those sources. No broad novelty search
or new source archive was undertaken in this review.

## Exact ratios and candidate reduction

For l>=k, canceling successive binomial coefficients gives

    h(l+1)/h(l) = l(l+1)/[(l-k+1)(m+l)],
    ratio_h-1 = k(m-2-l)/[(l-k+1)(m+l)].

The denominator is positive. The exceptional l=k-1 difference is h(k)>0;
earlier differences are zero. Thus d(l)=h(l+1)-h(l) is positive for
k-1,...,m-3, zero at m-2, and negative at m-1. At each eligible N<=m-2,
Bin(N,eta) gives positive mass to a strictly positive coefficient, so
S_(N+1)-S_N=eta E d(L)>0. The final adjacent difference has positive low
coefficients and one negative last coefficient. Therefore exactly one a_m
separates its signs, and only m-1 or m can maximize. Domain k<=N is important:
the proof is not claiming strict increase among the impossible sources N<k.

Put g(l)=h(l)/l, l>=1, with g(0)=0. The identity
`C(N,l)/N = C(N-1,l-1)/l` gives

    b_N = eta E g(R+1), R~Bin(N-1,eta),
    b_(N+1)-b_N = eta^2 E [g(R+2)-g(R+1)].

The eta^2 factor and argument R+1 are correct. For l>=k,

    g(l+1)/g(l) = l^2/[(l-k+1)(m+l)],
    numerator(ratio_g-1) = [m(m-2)-(m+2)l]/2.

Its zero is m-4+8/(m+2), strictly between m-4 and m-3 for even m>=8.
Consequently Delta g is positive from k-1 to m-4, negative from m-3 on,
and zero earlier. This proves strict increase of b_N through N=m-3 and
reduces the global problem to the four displayed candidates.

## Root uniqueness and order, reconstructed

For a sequence with positive terms before negative terms, let a be the first
negative index. After eta=t/(1+t), the binomial expectation has the sign of
Q(t)=sum_r C(n,r)c_r t^r. In Q(t)/t^a every positive term has a strictly
negative exponent, every negative term a nonnegative exponent. Its derivative
is strictly negative because at least one positive term is present. The limit
at zero is positive infinity; the limit at infinity is negative, possibly
negative infinity. Initial, intermediate or terminal zero coefficients do not
alter this argument. Thus the interior root is unique with the required sign.

For the root comparison, at a zero for size n the likelihood ratio of size
n+1 to size n on r<=n is
`w(r)=(1-eta)(n+1)/(n+1-r)`, strictly increasing in r. Subtract w(a) times
the old zero expectation. Positive coefficients lie below a and contribute
strictly negatively; negative coefficients lie at/above a and contribute
nonpositively. The new r=n+1 term is negative in each application here.
The new expectation is therefore strictly negative at the old root, so its
unique root is smaller.

For photon efficiency the relevant sequence is c_r=Delta g(r+1), and sizes
n=j-1 for j=m-3,m-2,m-1. Its new coefficients are indeed negative, giving
tau_(m-1)<tau_(m-2)<tau_(m-3). At a fixed eta the adjacent differences in
the four-candidate list are then positive followed by negative; only their
single peak, or its adjacent tie, can be global. There is no missing
nonadjacent-crossing condition.

At eta=0 all S_N and b_N vanish; this is excluded, not an interior unique
maximum. At eta=1, S_(m-2)=S_(m-1) are the lossless maxima, and b_(m-3)
is unique. These are explicitly restored by the proof. The restriction m>=8
is substantive: at m=6 the g-ratio zero is the integer3 and creates the known
lossless tie; the strict boundary placement used here would fail.

## Boundary asymptotic and root limits

Fix integer s>=1 and lambda>=0, with N=m-s, eta=1-lambda/m. For all sufficiently
large even m these parameters satisfy the source and survival domains, with
eta=1 allowed for the zero-loss asymptotic when lambda=0. For the S ratio let
T~Bin(m-s,lambda/m), so l=m-s-T. For the b ratio the size-biased identity
instead gives T~Bin(m-s-1,lambda/m), again with argument l=m-s-T. This one-step
shift changes E T only at order1/m and does not change either leading term.

For a=s+T<=m/4 the two exact relative differences have uniformly bounded
denominators of order m^2. Expansion gives

    d(l)/h(l) = (a-2)/(2m) + O((1+a)^2/m^2),
    Delta g(l)/g(l) = (a-4)/(2m) + O((1+a)^2/m^2).

It remains necessary to justify weighted expectations rather than silently
replace them by unweighted ones. Let H*=h(m-1) and G*=g(m-3). Both are true
lossless peaks. On the core, summing adjacent relative changes between l and
the peak bounds the peak-normalized deviation by C(1+a)^2/m. The at most two
positions above the g peak obey the same estimate. Both normalized functions
are everywhere at most one; if the displayed upper estimate is larger than
one it is harmless, not a supposed small-error approximation at every T.

For fixed lambda, every fixed moment of T is uniformly bounded and
E exp(uT)<C_(lambda,u) for fixed u>0. The complementary event T>m/4-s
therefore has exponentially small probability and polynomial moments on that
event are exponentially small as well. The functions and their differences
are bounded by a constant times their respective peak. Hence this tail is
negligible **after dividing by the peak**. This normalization is essential:
an absolute small-tail argument without it could fail if the peak were small.
The exceptional h(k-1)=0 transition lies entirely in the tail for large m.

For either normalized weight w, these estimates imply

    E w = 1+O(1/m),
    E(Tw) = E T+O(1/m) = lambda+O(1/m).

Thus the weighted mean of T is lambda+O(1/m), and the mean normalized
denominator is bounded away from zero. Taking expectations in the exact
coupling/size-bias identities and multiplying by eta yields precisely

    S_(N+1)/S_N-1 = (s+lambda-2)/(2m)+O(m^-2),
    b_(N+1)/b_N-1 = (s+lambda-4)/(2m)+O(m^-2).

Constants may depend on fixed s and lambda. No assertion for fixed nonzero
loss fraction or growing lambda has been smuggled into this argument.

For a_m use s=1 in the first expansion: the leading sign is lambda-1.
For tau_(m-3), tau_(m-2), tau_(m-1) use respectively s=3,2,1 in the second,
giving signs lambda-1, lambda-2, lambda-3. Evaluating at two fixed values
limit±epsilon gives opposite signs for all sufficiently large m. The finite
unique-root theorem then sandwiches each scaled loss, proving limits1,1,2,3
in the stated order. A uniform expansion over all lambda is not required for
this two-point argument.

## Independent exact smallest-case checks

The optional script uses no coordinator code or previous result. For m=8,k=4
it constructs each S_N directly from the binomial mixture using rational
polynomials. The lossless values are

    h(4)=7/33, h(5)=35/99,
    h(6)=h(7)=175/429, h(8)=490/1287.

It verifies lossless per-attempt maxima6,7; unique per-photon maximum5;
eta=0 values; and the positive/nonnegative coefficients giving strict earlier
growth. After dividing the eta^4 zero at the excluded endpoint, the adjacent
root polynomials, up to their positive scalar factors, are:

| Crossing | Polynomial |
|---|---|
| S8-S7 | 132 eta^4-630 eta^3+1134 eta^2-910 eta+273 |
| b6-b5 | 90 eta^2-208 eta+117 |
| b7-b6 | -180 eta^3+630 eta^2-728 eta+273 |
| b8-b7 | 462 eta^4-2160 eta^3+3780 eta^2-2912 eta+819 |

Forty exact rational bisections give disjoint sign brackets:

    a8 in (0.8918971853872790, 0.8918971853881885),
    tau7 in (0.7189451717713382, 0.7189451717722477),
    tau6 in (0.8271736763708759, 0.8271736763717854),
    tau5 in (0.9676496163856427, 0.9676496163865522).

The receipt retains the rational bracket endpoints and exact signs; these
decimal renderings are only for readability. Symbolic checks also recover
the two exact ratios and the lambda=0 leading coefficients for s=1,...,4.
These finite/symbolic checks are not the proof of all-m uniqueness or the
fixed-lambda limit; those were reconstructed above.

## Reproduction, hashes and safe interpretation

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python experiments/P37_independent_review/check.py
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py experiments/P37_independent_review/manifest.json --root .
```

Python3.11.15, SymPy1.14.0; fixed deterministic inputs, no random seed or
sampling. CPU0.581948 seconds with a30-second process limit and one thread.
The final manifest validates, status completed; input hashes agree before and
after execution. No broad or unchanged large experiment was rerun.

| Artifact | SHA256 |
|---|---|
| `check.py` | `538d5c22a4d87f1e25c3482d10c2b29a25cefa3c5c90b8f5ee44cbf9c6c6ae5f` |
| `receipt.json` | `bdeb9944df466d35989a324ad6f0647c7b91b0e68e92d220023a9f588fb7788c` |
| `manifest.json` | `babacf5d7a3172299b044604adcc76d85736aeae9ad08a1bb591a61f3ecb8e2c` |

There is no remaining proof gap identified. The result selects source sizes
for a known, classically calculable ensemble marginal under two explicitly
different resource objectives. The expected first-success photon cost N/S_N
requires independent refreshed attempts at fixed N; for a Haar unitary drawn
once the relevant object is E_U[N/p_U], potentially infinite. Fixed total
photon-budget allocation is a different objective. Neither the phase diagram
nor its asymptotic yields graph-quality enrichment, a trained-circuit sampler,
or a quantum advantage. No novelty verdict is supplied by this review.
