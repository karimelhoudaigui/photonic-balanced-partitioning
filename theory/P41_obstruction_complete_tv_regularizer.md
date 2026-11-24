# P41/R3 — checking the complete-graph total-variation regularizer

Parent proposed R_k and its coarea identity. This lane reconstructs the bounds
after seeing that proposal, and derives the three-photon comparison below.
This is analytic self-review, not a blind external proof certificate.

Let n in Z_+^m have fixed total k, with m>=k>=2, and define

    r_l(n)=#{i:n_i>=l},
    R_k(n)=sum_(i<j)|n_i-n_j|-k(m-k).

## Exact identities and sharp collision certificate

The integer coarea identity |a-b|=sum_(l>=1)|1_(a>=l)-1_(b>=l)| gives

    sum_(i<j)|n_i-n_j| = sum_l r_l(m-r_l)
                           = mk-sum_l r_l^2,
    R_k(n)=k^2-sum_l r_l^2.                                (1)

For collision-free n, r_1=k and other r_l=0, so R_k=0. If there is a
collision, the positive integer sequence r_l has sum k and largest entry at
most k-1. Its square sum is at most (k-1)^2+1: transferring mass from any
smaller positive entry to a larger one increases the square sum, until the
partition is (k-1,1). Therefore

    R_k(n)>=2(k-1) on collisions,                          (2)

with equality for occupations (2,1,...,1,0,...,0). Nonnegativity and the
zero set follow. These are exact fixed-particle statements.

There is also the useful comparison

    2M(n)<=R_k(n)<=2(k-1)M(n),                             (3)
    M(n)=sum_i binom(n_i,2).

For the lower bound, draw the k cells of the occupation Young diagram, with
row lengths n_i (reordering rows does not change either expression). The
number of pairs sharing a row is M and the number sharing a column is
sum_l binom(r_l,2). No pair shares both. Hence their sum is at most binom(k,2),
and (1) gives the bound. Equality is attained by one fully occupied mode.

For the upper bound write q=k-r_1. Since integer squares dominate their
arguments,

    R_k<=k^2-r_1^2-(k-r_1)
        =q(k+r_1-1)<=2(k-1)q<=2(k-1)M.

The collision-free case is immediate; otherwise r_1<=k-1 and M>=q.
The upper bound is attained by the single-doublon configuration in (2).

## Optimum-blind ground-state penalty

For a nonnegative weighted graph G let F_G(n)=sum_edges w_ij|n_i-n_j|.
Choose any classically known feasible k-subset S0 and let B=C_G(S0).
Its scoring/preparation cost must be charged. If

    lambda>B/[2(k-1)],

then every ground state of F_G+lambda R_k is collision-free: its value on
any collision exceeds B, whereas S0 has value B. No C* is used.

At matched certificate margin lambda=mu/[2(k-1)], (3) gives
lambda R_k<=mu M pointwise. Thus this is a genuinely weaker penalty away
from a single doublon, despite the same generic ground-state certificate.
It does not alone establish a lower bosonic mean, a favorable optimization
landscape or a resource advantage. For k=2, R_2=2M identically, so there is
no improvement over the old penalty at that photon count.

## Three-photon expectation: a sharp same-frame cost of this regularizer

Let V be an m-by-3 orthonormal occupied frame, q_ia=|V_ia|^2, and define

    S2=sum_i sum_(a<b) q_ia q_ib,
    T=sum_i q_i1 q_i2 q_i3.

For distinguishable labelled routing, E_D M=S2; for identical bosons,
E_B M=2S2. For a triple bunch in mode i, the probability is six times the
distinguishable probability. Thus the change in total triple-bunch probability
is 5T. Every three-photon occupation is of type111,210 or300, for which
(M,R)=(0,0),(1,4),(3,6). If Delta means B minus D, then

    Delta E R=4 Delta P_210+6 Delta P_300
             =4 Delta E M-6 Delta P_300
             =4S2-30T.                                   (4)

Since V V* is a projection, sum_a q_ia<=1 for every output row. For rows
with positive q_ia,

    (q_i1 q_i2+q_i1 q_i3+q_i2 q_i3)/(q_i1 q_i2 q_i3)
       =sum_a 1/q_ia >=9/(sum_a q_ia)>=9.

Zero entries follow directly. Therefore T<=S2/9 and

    Delta E R>=(2/3)S2>=0.                                (5)

The lower factor2/3 is sharp: the balanced three-mode Fourier tritter has
q_ia=1/3 on its three occupied rows, S2=1,T=1/9 and Delta E R=2/3.
It can be embedded in m6,k3 by appending vacuum outputs. This regularizer
therefore has a definite nonnegative same-frame bosonic cost at k3, though
the graph-weighted L1 term can in principle compensate it. (5) is not stated
for k>=4: the new occupation type22 changes the relation, and more moments
enter. No empirical check is substituted for that missing general argument.

## Loss warning and marginal computability

All identities require sum_i n_i=k. Applying R_k to a vacuum/loss outcome
without changing its definition gives a negative value and can recreate the
discard-reward bug. Future noisy objectives must explicitly assign failures
to events with fewer than k detections, or prove a different extension; no
postselection normalization may erase their resource cost.

The training objective must use E[R_k(n)], not R_k(E[n]). For m=2k the
uniform mean vector n_i=1/2 gives R_k(E[n])=-k^2, even for a distribution
supported entirely on valid binary occupations, where E[R_k(n)]=0. Jensen's
inequality is not an equality and does not turn fractional mean occupations
into a valid collision certificate.

For any fixed total k,

    F_G(n)=sum_i d_i n_i-2sum_edges w_ij min(n_i,n_j),
    R_k(n)=k(k-1)-2sum_(i<j)min(n_i,n_j).

Thus both means depend only on one- and two-mode PNR marginals, and
E min(n_i,n_j)=sum_(l>=1)Pr(n_i>=l,n_j>=l). A fixed-rank permanent/PGF
method may evaluate these without full Fock enumeration. This last algorithmic
bridge is a proposed continuation, not implemented or complexity-verified here.
The parent already identified its overlap with the known P35 rank-two method.
