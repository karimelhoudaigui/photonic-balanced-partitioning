# P54 / STAT H0: independent full-input small-hop reconstruction

This derivation was completed and frozen before reading ROOT's proof
`theory/P54_full_input_small_hop_obstruction.md` (announced commit4d6826d).
Only the question/scope was supplied: even N, fullCF input, U=exp(itA), raw
topN/2 with uniform ties. Encoding supplied scope information only (real
symmetric zero-diagonal guide, coupling/objective weights must be separated),
without formulas/verdict. ROOT's later message identified its narrower choice
A_ij=sqrt(w_ij); my general covariance derivation and weighted counterexample
were already transmitted before that message. No author proof, numeric data,
graph benchmark, import, executable calculation or test was used here.

## Domain and fixed decoder

Let m=r=N be even, N>=2, with one perfectly indistinguishable photon in every
input. A is a fixed Hermitian spatial matrix, t real, U(t)=exp(itA).
Every count pattern is retained. Decode the largest K=N/2 integer counts;
if necessary choose uniformly among tied labels, independently of t/history.
There is no loss, postselection, smoothing field, PIT, greedy completion or
conditioning on collision-free output. Iid continuous jitter supported on
[-beta,beta],0<beta<1/2 implements the same tie law. Statements are for
fixed finite N,A as t→0, not uniform bounds in growing graph size.

Write u for the uniform law on all binom(N,K) balanced subsets and

    p_* = Pr_u(edge crosses) = N/[2(N-1)],
    g_ij=|A_ij|² for i<j, W_g=sum_(i<j) g_ij,
    C_g(S)=sum_(i<j) g_ij 1[edge ij crosses S].

For the objective graph, w_ij=w_ji are fixed real weights (nonnegative for
the intended minimum-bisection problem), W_w=sum w_ij, and C_w is its cut.
Coupling amplitudes A_ij and objective weights w_ij are distinct quantities.

## Fock perturbation, including collision sectors

The N-particle generator is H=sum_ij A_ij a_i†a_j. Acting on |1,...,1>, its
diagonal part is just the global energy trA. A directed hop j→i gives the
normalized Fock state with n_i=2,n_j=0 and all other counts1, with matrix
element sqrt2 A_ij. Therefore that pattern has probability
2t²g_ij+O(t³). All other noninitial patterns require at least two applications
of H and have probabilityO(t⁴). Normalization gives initial-pattern mass
1-4t²W_g+O(t³). No collision sector has been discarded in this calculation.

For fully distinguishable single-photon inputs, the same directed one-hop
pattern has probabilityt²g_ij+O(t³); its initial mass is1-2t²W_g+O(t³).
Source-permutation routings of the all-one count pattern first contribute at
order4. Thus its entire leading decoded correction is half the bosonic one.

For real symmetric A, H is real in the normalized Fock basis. Transition
probabilities are even analytic functions of t (complex conjugation t→-t).
This upgrades all decoded-law remainders below toO(t⁴), for both B and D.
For general complex Hermitian A, O(t³) is the safe assertion made here.

## Exact leading decoded law

After one directed hop, i must be in the topK subset and j out; choose K-1
of the other N-2 labels uniformly. Pairing the two directions of an unordered
edge gives exactly u conditioned on that edge crossing. Indeed each crossing
subset has one compatible direction and probability
1/[2 binom(N-2,K-1)]=u(S)/p_*. A noncrossing subset has zero probability.

Hence, pointwise (and therefore in finite-support TV),

    mu_B(t)(S)=u(S)[1+4t²(C_g(S)/p_*-W_g)]+O(t³),
    mu_D(t)(S)=u(S)[1+2t²(C_g(S)/p_*-W_g)]+O(t³).

For real A the remainders areO(t⁴). All coefficients sum correctly since
E_u C_g=p_*W_g. In particular the mean objective obeys

    E_B C_w = p_*W_w + (4t²/p_*) Cov_u(C_w,C_g) + remainder,
    E_D C_w = p_*W_w + (2t²/p_*) Cov_u(C_w,C_g) + remainder.

This concerns the feasible decoded cut itself, rather than an undecoded
quadratic count proxy. It still proves only a local perturbative statement.

## Sign restriction, and a weighted counterexample to overextension

If g=alpha*w with alpha>=0, the drift is proportional to Var_u(C_w)>=0.
For minimization the bosonic leading perturbation is unfavorable (or zero),
twice the D coefficient. This includes unweighted adjacency guides A=w up
to scaling; for arbitrary nonnegative weighted objectives it includes the
specific real guide A_ij=sqrt(alpha*w_ij). Diagonal phases do not alter the
leading coefficient. N=2 is degenerate: the feasible cut cost is constant.

It does **not** imply that an arbitrary weighted adjacency guide A=w has the
same sign: then g=w² entrywise and the relevant quantity is covariance, not
variance. Here is an entirely rational N4 counterexample. Let

    w01=w23=1, w02=9/5, w13=0, w03=w12=19/20,
    A_ij=w_ij, A_ii=0.

The three unordered balanced partitions, each representing two equally likely
subsets under u, have:

| Partition | C_w | C_(w²) |
|---|---:|---:|
| 01 / 23 | 37/10 | 1009/200 |
| 03 / 12 | 19/5 | 131/25 |
| 02 / 13 | 39/10 | 761/200 |

Their exact mean C_w is19/5. Thus

    Cov_u(C_w,C_(w²))
      = [-(1/10)(1009/200)+(1/10)(761/200)]/3
      = -31/750.

Since p_*=2/3, the B t² coefficient is-31/125 and the D coefficient-31/250.
This refutes a universal nonnegative-sign extension to A=w weighted guides;
it does not refute the sqrt(w) restriction. Positive rescaling of A only
rescales these coefficients positively. The zero-weight absent edge is
permitted; continuity also gives nearby strictly positive-weight examples.
This is a hand-derived counterexample, not an executed benchmark or a claim
of optimization advantage over the classical law below.

## Necessary classical rare-hop control, with resource scope

For 4t²W_g<=1 the following is an exact classical mixture M_B(t): with
probability1-4t²W_g draw u; otherwise choose unordered edge with weightg/W_g,
choose its crossing orientation fairly, and uniformly choose K-1 remaining
vertices. If W_g=0 draw u (diagonal-only A leaves all-one counts unchanged).
This sampler reproduces the entire displayed order2 B law, with TV error
O(t³), or O(t⁴) for real A. M_D uses rare-hop probability2t²W_g.

Preprocessing g/edge sampling costs O(N²) in a dense representation; an alias
table can then draw an edge, and a uniform remaining subset costs O(N).
Graph scoring/guide construction/tie randomness remain charged separately.
This is a necessary cheap control; polynomial simulability or its existence
alone does not prove a total-resource dominance theorem. It does not match
the full finite-angle quantum law or establish a sharp uniform remainder.

For clarity, complement unweighted guides g=1-w reverse the drift, since
C_g=K²-C_w, giving negative covariance. The same rare-hop sampler explains
that leading improvement; it is not a new positive mechanism. Constant g
gives zero leading correction for every objective. For sqrt(w) guides, zero
variance means all feasible cut values are identical, not full ranked-law
equality. Finite collective angles, other photon inputs, detectors, fields,
decoders and higher-order mechanisms remain outside this local statement.

No mathematical novelty is claimed. This is a frozen independent derivation
and domain/counter-control check, to be compared with the author's exact
proof only after this checkpoint is committed.
