# Independent reconstruction — loss/oracle obstruction

Reviewer p41_adaptive. Claim card received from p41_obstruction, who reports
the root requested review. This file is written BEFORE reading the author's
proof b760636 or source-audit narrative. Shared project context is disclosed;
the reviewer did not author R3 or its experiments. No computation was executed.

## Exact claim card

There are 2k graph vertices, k>=2, and the objective is the cut of an undirected
graph. Let Omega be the oriented balanced subsets and M=|Omega|=binom(2k,k).
There are g>=2 optimal oriented subsets, since complements have equal cut.

The optical continuation has at most n_Q fresh preparation attempts. Attempt
t uses N_t<=N_max photons, selected using arbitrary classical history. Each
photon independently survives with probability eta, conditionally on that
history. A successful candidate requires at least k true surviving/detected
photons FROM THAT ATTEMPT. No photon accumulation across attempts, artificial
clicks, mitigation-generated events, recycling, or completion of a candidate
from fewer than k true photons is allowed. Loss/collision failures stay charged.

The comparison is the optical stage against n_C independent uniform balanced
classical proposals AFTER a common fixed classical front end. Its discoveries
and cost are separate. In the finite-budget comparison n_Q,n_C>=1. Zero-budget
cases are treated separately, not assigned a ratio ceil(0/0).

The photon-count survival cap is

    a = Pr[Bin(N_max,eta)>=k].

This bound deliberately gives the quantum stage the benefit of an ideal
oracle after survival; it does not require C* to be used during training.

## Arrow 1 — adaptive optical survival bound

At any history with no prior optical success, the next success probability
is at most Pr[Bin(N_t,eta)>=k]<=a, by monotonicity in N_t. Therefore if F_t
means no optical success in the first t attempts,

    Pr(F_t) = E[1_(F_(t-1)) Pr(failure_t | history)]
             >= (1-a) Pr(F_(t-1)).

Induction gives

    Pr(at least one optical success by n_Q) <= 1-(1-a)^n_Q.       (1)

Adaptive encodings, source sizes, circuit choices and stopping rules cannot
break this statement while the conditional bound holds. An early-stopping
algorithm can be padded with automatic failures to the same attempt cap.
Independence of *success events* across attempts is not assumed. The per-attempt
conditional physical survival cap is what is required.

## Arrow 2 — uniform baseline and integer budgets

A uniform balanced draw has success probability g/M>=p0=2/M. It can score the
draw and keep its best candidate without knowing C*. Hence its final candidate
is optimal with probability at least 1-(1-p0)^n_C.

Set L=ceil(n_Q/n_C). If L a<=p0, the integer Bernoulli inequality gives

    1-p0 <= 1-L a <= (1-a)^L.

Raise to n_C, then use L n_C>=n_Q:

    (1-p0)^n_C <= (1-a)^(L n_C) <= (1-a)^n_Q.                    (2)

Combining(1)-(2) proves that this classical continuation has at least the
optical upper-bound success probability. The inequality remains valid at
a=0; if a=1 the displayed sufficient condition cannot hold since p0<1.

For deterministic per-proposal costs c_Q,c_C and remaining budget B, the
actual counts are floor(B/c_Q), floor(B/c_C). Average rate comparisons do
not replace these integers. Example of the logical failure: c_Q=2,c_C=3,
B=5,p0=1/3,a=1/5 satisfies c_C a<=c_Q p0, but n_Q=2,n_C=1 and
1-(1-a)^2=9/25>1/3. This is a counterexample to that RATE INFERENCE, not an
implemented optimum-blind quantum advantage. If B<c_C, the baseline may
have zero proposals and a formula using a positive n_C is inapplicable.

More generally c_Q can be an enforced lower cost per optical opportunity
and c_C an enforced upper cost per uniform proposal, giving optimistic and
pessimistic count bounds respectively. Measured means alone do not produce
such deterministic guarantees for random stopping times or random costs.

## Arrow 3 — entropy regime

Let alpha>=1, N_max<=alpha k, and 0<eta<1/alpha. For lambda>0,

    a <= exp(-lambda k) (1-eta+eta exp(lambda))^(N_max)
      <= [exp(-lambda)(1-eta+eta exp(lambda))^alpha]^k.

Optimizing this elementary moment bound gives

    a <= exp(-k I),
    I=alpha D_Ber(1/alpha || eta).                                (3)

At alpha=1 the optimum is a limit lambda->infinity and I=log(1/eta);
indeed N_max<=k then a<=eta^k. If N_max<k or eta=0, a=0 directly. The
relative entropy convention must treat endpoints by their limits.

Since binom(2k,k)<4^k for k>=1,

    a/p0 <= (1/2) exp[-k(I-log4)].                                (4)

Thus delta=I-log4>0 supplies an exponentially small ratio. A sufficient
finite cost-ratio consequence is L<=2 exp(k delta), together with the
previous count definitions. This is a bound on a comparison criterion,
not a claim that all real hardware/classical costs have that ratio.

For alpha=1 and eta<=1/4,

    2a <= 2/4^k < 2/binom(2k,k)=p0.                              (5)

The boundary eta=1/4 has delta=0; its strict finite inequality comes from
binom(2k,k)<4^k, NOT from asserting a strictly positive entropy gap there.
This is a sufficient uniform threshold; finite-k cutoffs can be larger.

For alpha=2,

    I=log(1/[4eta(1-eta)]),
    delta=log(1/[16eta(1-eta)]),

so in the required lower-tail-loss regime eta<1/2, delta>0 holds exactly
when eta<(2-sqrt(3))/4. Failure of this condition is not evidence that a
quantum optimizer succeeds; this particular sufficient bound becomes weaker.

## Counter-readings and necessary exclusions

1. A frontend allowed to find an optimum classically can make overall success
   one even if the optical stage always fails. Equation(1) is not an overall
   hybrid-algorithm bound when those discoveries are added back. An adaptive
   frontend consuming optical data is not automatically a common fixed stage.
2. Marginal transmission is insufficient. If a common Bernoulli coin makes
   all N photons survive together with probability eta, each has marginal
   survival eta but Pr(K>=k)=eta, not a Binomial tail. Conditional independent
   uniform loss, or a justified stochastic upper bound, is essential.
3. A vendor shot defined as a nonempty detection is not a fresh emission
   attempt. Its conditional tail is divided by Pr(K>=1); substituting that
   shot count for n_Q silently removes failures. This theorem cannot certify
   current Lucy performance from marketing transmission values or filtered
   counts lacking an authenticated denominator/cost model.
4. Loss heralding followed by free retries, storing survivors, using dark
   clicks, or completing balanced candidates classically from fewer than k
   detections breaks the necessary-event hypothesis or the attempt cost.
5. New encodings can use fewer than k photons to represent a balanced subset.
   They are outside this photon-per-selected-vertex class, not disproved.
6. C* and g appear in analysis only. Neither the classical uniform sampler
   nor the survival bound requires an optimal mask, known partition or oracle
   stopping test in a real training algorithm.
7. Cost units stay separate: emission attempts, injected photons, scored
   feasible proposals and wall time are not interchangeable. Shared setup and
   actual floors must be established before asserting a matched-cost result.

## Preliminary verdict and provenance

The three arrows are proved under the claim card's exact physical and budget
hypotheses, with the endpoint/positive-count conventions above. This is a
strong regime-specific obstruction, not a universal no-go for photonic graph
optimization, an empirical estimate of device loss, or a novelty verdict.
The author's exact statement and dependencies will be compared only after
this independent reconstruction is committed. No source or numerical audit
has been substituted for this proof reconstruction.
