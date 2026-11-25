# P47 auxiliary review: prime Fourier dimensions remove centered stationary directions

2026-11-25. Primary verdict: **proved as written**, for real doubly centered
C and the normalized Fourier matrix of prime order b>=2. This is a fresh
reconstruction of the coordinator's auxiliary claim card, sent back before
reading any coordinator proof. No such proof was read. The reviewer authored
the earlier polar-step note: this review is not a new third-party review of
that finite-step argument. It supplies the additional Fourier implication.

Base worktree commit: `9e1d9f900f1c768c399259a8b3fffffe01b43c62`.
The source claim was the coordinator message beginning “Nouvelle carte
auxiliaire ROOT pour P47”, asking whether Pi_F(C odot F)=0 forces C=0 at
prime b. No numerical code, data, P46 implementation or outcome is used.

## 1. Exact claim and dependencies

Index rows r and columns a,c by Z/bZ. Put omega=exp(2 pi i/b),
F_rc=omega^(rc)/sqrt(b). Let C be a REAL b-by-b matrix with

    sum_c C_rc=0 for every r,
    sum_r C_rc=0 for every c.

The metric is Re Tr(X*Y); star denotes conjugate transpose. For G=C odot F,
the tangent projection is Pi_F(G)=G-F sym(F*G). Its vanishing is equivalent
to the Hermiticity of B=F*G. The target is

    b prime and Pi_F(G)=0  ==>  C=0.                    (P)

Dependencies are: the tangent projection identity (previous P47 note,
also immediate from the Hermitian/skew-Hermitian splitting), elementary
finite Fourier inversion, the cycles of a nonzero shift modulo a prime,
and the two centering conditions. No external theorem is needed for (P).
The connection with established Fourier-defect theory is checked separately
below and is not a novel mathematical claim.

## 2. Reconstruction with signs and complex conjugation retained

Define the normalized Fourier transform of column c by

    h_c(d)=(1/b) sum_r C_rc omega^(rd).

Direct multiplication gives

    B_ac=h_c(c-a).

Since C is real, conjugating B_ca gives h_a(c-a). Thus, writing d=c-a,

    B=B*  <==>  h_c(d)=h_(c-d)(d) for every c,d.        (1)

The sign of the Fourier exponent could be reversed consistently without
changing the shift-orbit conclusion. Equation (1) is an equivalence, not a
one-sided relaxation.

For d!=0 and prime b, the map c->c-d is a SINGLE cycle on all b columns.
Consequently h_c(d) is independent of c. The row-sum condition yields

    sum_c h_c(d)=(1/b)sum_r omega^(rd)sum_c C_rc=0.

Hence h_c(d)=0 for every c and every d!=0. At d=0, the column-sum condition
gives h_c(0)=0 directly. Inverse Fourier transformation now yields C_rc=0
for all r,c. This proves (P), including b=2; b=1 is not called prime and
its doubly centered space is already zero.

In fact, if centering is omitted but C stays real, the same shift argument
says h_c(d) is independent of c for each d!=0, while h_c(0) can depend on c.
Fourier inversion therefore gives exactly

    C_rc=alpha_r+beta_c                                  (2)

with real alpha,beta. Conversely every matrix (2) is stationary, because

    F*(C odot F)=F*diag(alpha)F+diag(beta)

is Hermitian. Thus the prime stationary kernel is precisely the 2b-1
dimensional row/column phase-gauge space. Double centering is a complementary
slice removing it. Merely imposing one of the two centering conditions
does not suffice: the remaining zero-mean column or row field is a nonzero
stationary counterexample.

## 3. A quantitative qualification, not a dimension-free gain

The same derivation gives a useful nonzero lower bound. For real doubly
centered C, Parseval's identity gives

    ||G||_F^2=||C||_F^2/b=sum_(c,d)|h_c(d)|^2,
    ||Pi_F(G)||_F^2=(1/4)sum_(c,d)|h_c(d)-h_(c-d)(d)|^2. (3)

At prime b, each nonzero shift is a cycle of length b. Each vector
(h_c(d))_c has zero mean. Fourier diagonalization of that cyclic shift
shows its squared difference has eigenvalues
4 sin^2(pi l d/b), l=1,...,b-1; their minimum is 4 sin^2(pi/b).
The d=0 component is zero by column centering. Consequently

    ||Pi_F(G)||_F^2 >= sin^2(pi/b) ||C||_F^2/b.           (4)

This supplementary bound is derived here, not quoted from a computation.
The ratio can shrink with b. For the normalization ||C||_op=1, the weaker
guarantee obtained from ||C||_F>=1 scales as sin^2(pi/b)/b; it is not an
extensive-response lower bound. Floating point near-stationarity and the
precision of Fourier, norm and polar computations remain implementation
questions. Exact nonvanishing does not license a numerical certificate
with an unspecified error budget.

## 4. Why primality matters, and what composite dimensions actually imply

For arbitrary b, translation by d has gcd(b,d) cycles. Equation (1) only
forces h_c(d) to be constant on each cycle. Counting Fourier coefficients
with the reality pairing h_c(-d)=conj(h_c(d)) gives a REAL kernel dimension

    sum_(d=0)^(b-1) gcd(b,d),  with gcd(b,0)=b.

For d and -d distinct, their gcd(b,d) complex parameters together count
2gcd(b,d) real parameters. For the self-conjugate d=b/2 at even b, there
are gcd(b,d) real parameters. At d=0 there are b real parameters. These
facts justify the count, including even b, without double counting.

The row/column fields (2) lie in this kernel for every b. Every real C
splits uniquely into its doubly centered part ZCZ and a row/column field
(as matrices); subtracting that field preserves stationarity. Hence the
dimension of the doubly centered stationary space is

    sum_(d=1)^(b-1) [gcd(b,d)-1].                       (5)

It is zero exactly for prime b>=2. For example, the formula gives 1 at b=4,
17 at b=12 and 12 at b=14, whereas b=13 and b=17 give zero. These are
symbolic integer evaluations, not numerical experiments.

A direct composite witness can also be constructed. Choose 0<d<b with
g=gcd(b,d)>1 and a real nonzero f_c constant on translation-by-d cycles
with sum_c f_c=0, for example f_c=cos(2 pi c/g). Set

    h_c(d)=h_c(-d)=f_c, all other h_c(e)=0, if d!=-d;
    h_c(d)=f_c, all other h_c(e)=0, if d=-d mod b.

Its inverse Fourier transform is a real nonzero doubly centered C and
satisfies (1). Thus composite dimensions permit stationary signals. This
does NOT assert that every composite graph or every nonzero signal stalls.
Realizability of a particular signal by additional graph constraints is a
separate question; the prior b=4 positive graph already realizes one.

## 5. Consequence for the previously frozen P47 step

For real graph swap costs in the declared inside-by-outside convention,
R=ZDZ is real and doubly centered. At prime b with R!=0, C=R/||R||_op is
nonzero, so (P) ensures Pi_F(C odot F)!=0. The prior ambient-step result
with h=max(||C odot F||_op,max_ij|C_ij|) and epsilon=1/(4h) then implies

    Y=polar(F-epsilon(C odot F)) != F,
    S_D(Y)-S_D(F)
      <=-||R||_op(1/epsilon-max_ij|C_ij|)||Y-F||_F^2<0.

This is a strict proxy-cost descent for b=13/17 under R!=0. The R=0 branch
still returns F and remains in coverage. It does not prove a global minimum,
an actual block-cut improvement, a raw or PIT-decoded advantage, a bosonic
advantage over distinguishable particles, or a useful size of the response.
Classical assignment already solves this routing proxy globally, and the
intensity direction is shared by the classical controls. This auxiliary
lemma can motivate a prospective dimension choice, not retrospectively
filter P46 or change its frozen settings/outcomes.

## 6. Exact relation to known Fourier defects

The source inspected is Tadej and Zyczkowski, *Defect of a unitary matrix*,
[arXiv:math/0702510v2](https://arxiv.org/abs/math/0702510v2), revised
20 December 2007; journal version LAA 429 (2008), 447-481. Its
[PDF](https://arxiv.org/pdf/math/0702510v2), Definition 2.1/equation (6),
Theorem 5.3/equation (142), and section 5.2(i)/Table 1 were inspected.
The theorem's defect formula is (5); the prime specialization gives zero.
The original source uses normalized Fourier matrices.

The precise translation is that i(C odot F) preserves moduli to first
order and is tangent to the unitary group exactly when F*(C odot F) is
Hermitian. Thus our kernel is the infinitesimal phase-preserving tangent
space; removing row/column gauges leaves the source's defect. The inspected
source states and derives the formula (with its alternate-form proof in
Appendix B); a complete independent audit of that entire paper was not
performed. Our proof above is self-contained. The lemma is a reformulation
of established Fourier-defect structure, not new theory.

## 7. Obligations, provenance and commands

| Obligation | Result | Evidence |
|---|---|---|
| Complex conjugation and frequency orientation | passed | Direct entries of B and equation (1) |
| Prime shift transitivity | passed | Every d!=0 is invertible modulo b |
| Both centering hypotheses used | passed | Row sums remove d!=0; column sums remove d=0 |
| Smallest prime and composite boundary | passed | b=2 proof; composite construction and b=4 witness |
| Strict finite step | passed with stated dependency | Previous P47 polar lemma plus (P) |
| Uniform extensive response or optical gain | not addressed | Not implied by the lemma |
| Attribution | passed for bounded comparison | Exact version and locators above |
| Numerical implementation/error certificate | out of scope | No code or calculation |

Actual checks: read the proof-audit skill and relevant obligation checklist;
`git status --short`; reconstructed the coordinator claim in a message
before external-source inspection; primary-source browser reads; manual
Fourier algebra; Git whitespace/scope and SHA256 checks at commit. No Python,
simulation, P46 CLI/data access, test suite, QPU or numerical sampling was
performed. This file is a new independent reconstruction of the auxiliary
claim within the same team's/model's limitations, not a claim of fresh
independent validation of all prior P47 components. No gap remains for (P)
under its real, prime, double-centering hypotheses.
