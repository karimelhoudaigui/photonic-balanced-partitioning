# Density certificate: absolute success errors, conditioning, and rare-event limits

Base: `75e5831` (the density-certificate research checkpoint).
Scope: a focused application and counterexample, not a new circuit/graph sweep,
optimizer, manuscript section, novelty claim, or QPU proposal. The density bound
in `theory/phase3_density_certificate.md` is a named dependency: this note does
not replace its pending independent proof/novelty audit. The probability
arguments and the exact two-photon example below are reconstructed directly.

## What an accepted density certificate implies

Let P=p_b and Q=p_d be the complete, unpostselected Fock laws of the *same*
occupied-column frame V, with distinct single-photon inputs and fixed photon
number k. TV(P,Q)=(1/2)sum_t|P(t)-Q(t)|. Let epsilon be any verified upper bound
on this TV, in particular the density envelope if its hypotheses and proof are
accepted. For every fixed success event A,

    |P(A)-Q(A)| <= epsilon.

A may specify optimal bisections retrospectively, or a declared cut-quality
threshold; this statement does not supply C* to an optimizer. It compares neither
reoptimized circuits nor a classical correlated sampler. It gives an absolute
probability error, not a relative approximation for every rare event.

For independent raw attempts from a fixed circuit, if p=P(A)>0 and q=Q(A)>0,
expected first-hit attempts are T_b=1/p and T_d=1/q. If q>epsilon,

    1/(q+epsilon) <= T_b <= 1/(q-epsilon),
    q/(q+epsilon) <= T_b/T_d <= q/(q-epsilon).

The lower bound can be capped at one attempt when needed. Thus relative
waiting-time control requires epsilon/q to be small. If q is of order epsilon,
the TV certificate alone does not establish such control; inversion at q-epsilon
is then unavailable. No confidence interval is manufactured from this exact
inequality. State-preparation/training time and source/detection losses are
separate physical costs, absent from this ideal statement.

## Conditioning: the max-denominator inequality is valid

For a common event F, assume a=P(F)>0 and b=Q(F)>0. Then

    TV(P(.|F),Q(.|F)) <= TV(P,Q) / max(a,b).

Proof. Suppose a>=b and use probability densities p,q against a common reference
measure (or finite Fock masses). The triangle inequality gives

    a TV(P(.|F),Q(.|F))
      = (1/2) integral_F |p-(a/b)q|
      <= (1/2) integral_F |p-q| + (a-b)/2.

But integral_(F^c)|p-q| >= |P(F^c)-Q(F^c)|=a-b. Adding the two regions bounds
the last display by TV(P,Q). Swap P,Q if b>=a. Both conditional laws must exist;
a positive value of only the larger acceptance mass is insufficient.

In the single-occupation photon model define the expected bosonic collision
pair count M=E_b sum_i n_i(n_i-1)/2, as at checkpoint 75e. The independent model
has mean pair count M/2. A colliding output contains at least one pair, hence

    Q(CF) >= 1-M/2,       P(CF) >= 1-M.

These are pair-moment/Markov bounds, not identities for general k. If M<1 they
guarantee both CF probabilities are positive. More generally assume both are
positive and M<2. Then

    TV(P(.|CF),Q(.|CF)) <= min(1,epsilon/(1-M/2)).

The bound is still absolute. The exact acceptance denominator can be used when
the moment-only lower bound is weak. An HOM counterexample has M=1,
P(CF)=0,Q(CF)=1/2; its bosonic conditional law is undefined. It prevents silently
using the positive distinguishable acceptance bound as proof of both premises.

## Exact flat-density two-photon family

Take m=4,k=2, w1=(1,1,0,0)/sqrt(2), w2=(0,0,1,1)/sqrt(2), and

    V=(w1,w2) [[c,-s],[s,c]],   c^2+s^2=1, 0<=s<=c.

All four first occupation means a_i stay exactly 1/2 and VV* is constant. This
means *first moments* are flat; second moments and the output law change. Let
F=CF. For the unit-weight path 0-1-2-3 the optimal partitions are 01 and 23.
The two-photon permanent formula gives the following complete output classes:

| outcome class | count | P per outcome | Q per outcome |
|---|---:|---:|---:|
| double occupancy in one mode | 4 | c^2 s^2/2 | c^2 s^2/4 |
| CF pairs 01 and 23 | 2 | c^2 s^2 | c^2 s^2/2 |
| CF pairs connecting the two groups | 4 | (c^2-s^2)^2/4 | (c^4+s^4)/4 |

Both probability columns sum to one. Put M=2c^2s^2. Direct summation yields

    TV(P,Q)=M,
    P(A_opt)=M,          Q(A_opt)=M/2,
    P(F)=1-M,            Q(F)=1-M/2.

Thus, for 0<s<=c, P(A_opt)/Q(A_opt)=2 even while M->0. The first-hit costs are
T_b=1/M and T_d=2/M; both diverge. This is compatible with absolute output-law
approximation becoming arbitrarily accurate.

This family meets the density theorem with c_density=1/2. For M<1/8 its refined
leading envelope is epsilon=M+O(M^(3/2)); the exact TV=M supplies the sharp
absolute reference. The success event itself has probabilities of order M, so
the certificate cannot be promoted to a 1+o(1) relative replacement guarantee.
Here the success-event difference is M/2, not the entire TV M.

The exact conditional quantities are

    P(A_opt|F)=M/(1-M),     Q(A_opt|F)=M/(2-M),
    TV(P(.|F),Q(.|F))=M/[(1-M)(2-M)].

The conditional success ratio (2-M)/(1-M) tends to two, while conditional TV
tends to zero as M/2. At M=1/2 the max-denominator inequality is sharp:
conditional TV=2/3=TV(P,Q)/Q(F). This endpoint can be checked using a fully
rational frame with rows (1,-1)/2,(1,-1)/2,(1,1)/2,(1,1)/2. At s=0 both success
probabilities vanish: waiting times are infinite and their ratio is undefined,
rather than a measured twofold gain at that endpoint.

As a separate familiar ceiling, Cauchy on the k! routing amplitudes gives
P(t)<=k! Q(t) for each occupation and hence P(A)<=k! Q(A). The factor two in this
example saturates that two-photon enhancement bound. It is not a new effect or
a complexity-theoretic result.

## Correlated classical control and scientific boundary

A classical control supplied with the two displayed mode groups chooses either
01 or 23 with a fair coin and returns that pair. It uses no C* or optimum test
in its sampling rule, is always balanced, and has optimum probability one *for
this deliberately constructed path example*. The graph and groups are aligned
by construction. This is an adversarial illustration, not a preregistered graph
population benchmark or a claim that group discovery is free on unknown graphs.
Classical draws/cut queries and physical photon attempts also remain different
cost units; the example establishes ease, not a measured wall-clock speedup.

The complete quantum family is itself classically easy: draw one of its three
group-occupation classes and then split uniformly within each two-mode group.
The rare-event enhancement over independently distinguishable photons therefore
is not evidence against classical correlated simulation or evidence of useful
quantum computation. Reoptimized controls, accepted-event counts, total physical
attempts and classical discovery costs would all need separate treatment.

## Receipt and disposition

`experiments/P33_density_success_scope/` contains a small exact-rational check:
five fixed Pythagorean rotations (t=1/8,1/32,1/128,1/512,1/2048 with
c=(1-t^2)/(1+t^2),s=2t/(1+t^2)), zero and fully mixed endpoints, full ten-outcome
probability tables, conditioning, waiting-time fractions, and the zero-CF HOM
guard. The optional density-envelope values are floating diagnostics, not
interval-certified values or an independent proof of checkpoint 75e. No sweep,
training, random sample, new graph ensemble, or hardware experiment is run.

**Decision:** reject the claim that an absolute density/TV certificate rules out
all relative rare-success enrichment or automatically dequantifies first-hit
cost. Keep the valid absolute event and conditional bounds, with positivity and
scale conditions explicit. The constructed twofold example is not a novelty or
advantage claim. No shared registry, source module, manuscript, or QPU gate is
changed.
