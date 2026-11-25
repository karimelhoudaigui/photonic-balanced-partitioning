# P54: weak full-input graph hopping biases the wrong cut direction

ROOT derivation, 25 November 2026. **Internal proof; separate reconstruction
pending.** This is a falsification of one proposed mechanism, not a general
passive-optics obstruction or a positive optimizer result. No computation,
new graph, training, known optimum or hardware is used below.

Let N=2K>=4, w_ij=w_ji>=0, w_ii=0. Put H_ij=sqrt(w_ij), H_ii=0 and
U(t)=exp(i t H). Inject one photon into every one of the N modes. Retain
every output count and decode its K largest entries, choosing uniformly
among all boundary ties. Define X_e(S)=1 when balanced subset S crosses
edge e, C(S)=sum_e w_e X_e(S), W=sum_e w_e, and
q=K/(N-1). Let P0 be uniform on all balanced subsets.

For a FIXED finite graph, as t->0, the bosonic decoded law satisfies

    P_B,t(S) = P0(S) [1 + 4t² (C(S)/q - W)] + O_G(t⁴).

The distinguishable-photon law satisfies the same formula with4 replaced by2.
The remainder constants may depend on N,H; no size-uniform bound is claimed.
Consequently

    E_B,t C = E_0 C + (4t²/q) Var_0(C) + O_G(t⁴),
    E_D,t C = E_0 C + (2t²/q) Var_0(C) + O_G(t⁴).

If C is nonconstant on balanced subsets, the leading response **increases**
the cut we seek to minimize, with twice the distinguishable coefficient.
If its uniform variance is0, C is constant on every feasible subset and
there is no cut optimization problem for this graph/constraint. Complementing
the topK choice preserves the same cut and cannot reverse this conclusion.

## Derivation

The many-body generator is sum_ij H_ij a_i^dagger a_j. From |1,...,1>, a
directed hop j->i creates occupation2 at i,0 at j,1 elsewhere, with generator
matrix element sqrt2 H_ij. Thus each such bosonic count has probability
2t² w_ij+O_G(t⁴), and the unchanged count has probability
1-4t² W+O_G(t⁴). All other counts have probability O_G(t⁴). The absence of
odd orders follows because H is real and changing t to -t complex conjugates
every Fock amplitude. There are finitely many count patterns at fixed N.

For distinguishable independent photons, a directed hop has probability
t² w_ij+O_G(t⁴), the unchanged count has probability1-2t² W+O_G(t⁴), and
all other patterns again have O_G(t⁴) probability. These are unconditioned
probabilities per full N-photon injection, without collision rejection.

For a given undirected edge e={i,j}, the two directions have equal leading
weight. TopK decoding includes the doubled site and excludes the empty site,
then selects K-1 of the remaining N-2 tied sites uniformly. Averaging the
two directions gives R_e=P0 conditioned on X_e=1. Since P0(X_e=1)=q,

    R_e(S)=P0(S) X_e(S)/q.

Adding the unchanged-count and rare-hop contributions therefore gives

    P_B,t=(1-4t² W)P0 + 4t² sum_e w_e R_e + O_G(t⁴),

which is the asserted law. Normalization holds to this order because
E_0 C=qW. Multiplying by C and summing gives the variance formulas.

## Classical control and exact limits of the conclusion

Whenever 4t² W<=1, the displayed leading law is itself an exact classical
mixture: with probability4t² W, choose an edge with probabilities w_e/W
and draw a uniform feasible subset conditioned on crossing that edge;
otherwise draw P0. W=0 uses P0 directly. Edge preprocessing and balanced
subset generation need no optimum. This is a genuine nonnegative law, but
it approximates the optical law only to the stated local order.

Alternatively the D family at time sqrt2*t matches the B leading law. Thus
the doubled interference rate alone cannot defeat independently retuned D.
No equality of finite-strength laws, clock/resource dominance, all-order
simulation theorem or useful finite-t optimum is proved. Using H_ij=w_ij
instead of sqrt(w_ij) changes the tilt to C_(w²); its covariance with C_w
need not be replaced by Var(C_w) without a separate argument. A different
decoder, partial filling, complex hopping, finite strength or intermediate
measurement is a different scientific question.
