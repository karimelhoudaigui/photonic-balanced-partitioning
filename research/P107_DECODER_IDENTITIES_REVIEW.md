# P107 auxiliary decoder identities: independent manual reconstruction

26 November 2026. **PROVED AS WRITTEN under the stated decoder/symmetry scopes.**
ROOT suggested these auxiliary identities; this is reconstruction, not blind
discovery, a new mechanism or an attribution/novelty claim. Parent16174e28b9008877de615d08b66f7f333a0286ed.
No P107 moving source or raw result was read. P101's frozen decoder and cycle
definitions are the inputs:69e4a6fe434a677acfc5a7e616471990b16db86b,113 lines,
SHA25665e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c.

## Four-port threshold identity: no photon-number restriction

Let C_ij=C_ji=C_kl be the balanced-cut cost for complementary pairs ij,kl,
and cbar=(C_12+C_13+C_14)/3. Set w_ij=C_ij-cbar. Then

    sum_(j!=i) w_ij=0 for each i, and sum_(i<j)w_ij=0.

Use exactly P101's threshold decoder: uniform2-subset of the click set if
there are>=2 clicks; with1 click include it plus a uniform other vertex;
with0 clicks choose a uniform balanced pair. Independent uniform tie coins
are averaged, not optimized. For every count vector its expected score is
cbar EXCEPT when its click set is exactly{i,j}, when the score is C_ij.
Indeed0/4 clicks average all6 pairs, while1/3 clicks average the three
different unoriented partitions once. This uses complement invariance.

For ANY normalized count law P on these four ports, let
V(A)=P(no clicks outside A)=G(z_l=1 for l in A, else0). Inclusion-exclusion gives

    P(click set={i,j})=V({i,j})-V({i})-V({j})+V(empty).

Multiply by w_ij and sum. All singleton terms cancel by the row sums, and
the vacuum term cancels by the total sum, proving the WHOLE-RAW identity

    E_P C(D_T)=cbar+sum_(i<j)(C_ij-cbar)V({i,j}).             (1)

Vacuum, one-click, collisions and every partial-loss branch are included;
no conditioning, CF-output denominator or rare-event division was used.
It holds for arbitrary total photon number K, not just K=4. A separately
flagged uniform fallback has mean cbar and is included by its actual weight.

For known K-distinct-mode CF input and passive vacuum-loss signal matrix T
with four rows, the normalized PGF is

    G_B(z)=per[I_K+T†(diag(z)-I_4)T],
    V_B({i,j})=per[I_K-T†Q_({i,j}^c)T].                    (2)

Here Q selects the two excluded output ports: the DEVIATION from I has
rank<=2; the permanent matrix itself need not have rank2. D replaces the
permanent by the product of diagonal entries. Equation(1) therefore gives
a mean oracle involving six void probabilities for either model. This note
makes no polynomial-runtime claim requiring a fresh P42/source transfer.
It is not an entire-count sampler or a control of hard-tail/hitting statistics.

## PNR correction: total observed photons at most four is essential

P101's PNR decoder ranks counts then breaks ties by a fresh uniform priority.
For sum n<=4 it has the SAME mean score as D_T except the12 records

    n_i=2, n_l=0, n_j=n_k=1, i!=l; write their probability q_(i,l).

For these, PNR always selects i and a uniform member of{j,k}; thresholding
averages all three pairs on{i,j,k}. Their difference is

    (C_ij+C_ik)/2-cbar=(cbar-C_il)/2.                     (3)

Exhaustiveness follows by integer partitions: with0/1 clicks both rules
agree; with2 clicks both choose that pair; with4 clicks all counts are1;
with3 clicks the only possibilities are1110 and2110. The former averages
the same three pairs. There are4 choices of doubled i and3 of empty l.
Thus, writing delta for B minus D at the SAME fixed optical settings,

    delta E_P=delta E_T+
        sum_(i!=l)(cbar-C_il) delta q_(i,l)/2.             (4)

This includes N=0,1,2,3 and every loss pattern. For K>4 the12-only claim
fails: e.g.3110 adds another multiplicity-sensitive record, and2210 also
changes the ranking. Equation(1), with the declared threshold rule, survives.

## P101 cycle reduction and the needed reflection check

For that cycle, adjacent-pair cuts cost3, opposite-pair cuts cost2, cbar=8/3.
Define G_adj,G_opp as V({i,j}) for one adjacent/opposite allowed pair;
q_adj,q_opp as the probability of2110 with doubled i and empty adjacent/
opposite l. These are probabilities of individual records, not their sums.
Rotations give one opposite type. For the two directed adjacent types,
reflection is also needed: the gauged T=F diag(1,x,xy,y)F† is circulant
Hermitian, hence reflection sends T to T*. Conjugating its whole canonical
dilation conjugates every CF amplitude and preserves probabilities. The
filled four-mode CF input is invariant under the port permutation. Therefore
both B and D laws have the required dihedral count symmetry for x,y in[0,1].

There are4 adjacent and2 opposite unordered pairs in(1), giving
delta E_T=(4/3)(delta G_adj-delta G_opp). There are8 adjacent and4 opposite
ordered(i,l) in(4), giving the correction(4/3)(delta q_opp-delta q_adj).
Consequently

    delta E_P=(4/3)(delta q_opp-delta q_adj
                           -delta G_opp+delta G_adj).     (5)

All factors/signs pass independent hand reconstruction. This is a mean
identity, not a b=1 sign proof, reoptimized-control comparison or optimizer
advantage. No science execution/import/AST/symbolic/numerical/RNG/graph/
native/test/runner/raw-data/QPU/paper/push or other file edit occurred.
