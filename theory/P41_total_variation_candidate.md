# P41/R4 — lossless graph total variation with a certified collision gap

Base: f09c7ec82b2fe23395116e21bd56614f3739107c. Root derivation,
independently reconstructed analytically by the obstruction lane. Novelty OPEN.
This is a candidate mechanism and an elementary certificate, not an advantage.

Let m=2k, k>=2, and let n be a nonnegative integer occupation with sum n_i=k.
For nonnegative weighted graph G, define F_G(n)=sum_edges w_ij |n_i-n_j|.
It agrees with balanced cut cost on collision-free occupations, while it is
not the old quadratic occupation objective. The old same-frame PSD quadratic
dominance does not determine its bosonic/distinguishable comparison.

Define the complete-graph regularizer

    R_k(n)=sum_(i<j)|n_i-n_j|-k(m-k).

For S_l={i:n_i>=l}, the discrete coarea identity gives

    R_k(n)=k^2-sum_(l>=1)|S_l|^2.

The level sizes are nonnegative integers with sum k. Thus R>=0, equality
holds exactly at a collision-free occupation, and a collision implies
|S_1|<=k-1. Among partitions of k with at least two positive parts, the
largest sum of squares is (k-1)^2+1. Therefore

    R_k(n)>=2(k-1) on every collisional occupation.

The bound is attained by (2,1,...,1,0,...,0). It requires no optical assumptions.
Let S0 be any scored feasible partition, with cost C0; no optimum is computed.
Choose lambda=(C0+epsilon)/(2(k-1)), epsilon>0. The objective

    J_G(n)=F_G(n)+lambda R_k(n)

has every collisional value greater than C0, and equals cut cost on CF.
Consequently its full-Fock global minima are exactly the balanced optima.
This is a ground-state encoding, NOT an efficient minimization proof. Charge
the construction and scoring of S0. If C0=0, a classical zero-cost solution
is already known and must not be presented as photonic discovery.

## Changed bottleneck and discriminator

The obstruction lane derives a connected k2 case with lower bosonic L1 mean
than distinguishable mean and valid ground encoding. The first new question
is whether a full many-photon finite-angle graph-dependent family can exploit
this without handing all useful scores to a classical search first. A positive
same-frame mean is insufficient; optimize the distinguishable parameters
independently and compare best feasible candidates found at charged budgets.

The exploratory first family is U=exp(-itH) on all m modes, not a constant-size
interacting block. H uses the adjacency and single-flip features at a random
feasible anchor, with antisymmetric sign-feature phases. It sees no optimal
labels. The angles tested include genuinely finite t after ||H||=1 scaling,
outside the small-t regime where R1 supplies a classical proxy. Global
hyperparameters train on development graphs only. If it fails there, preserve
the negative and do not open held-out outcomes merely to find a favorable one.

This family can still fail through a zero-angle minimum, collisions, weak
proposal quality, an independently trained D control or serious feasible
classical search. Any such result closes only this family/protocol.

## Loss caveat

The fixed total k is essential. The vacuum gives R_k=-k(m-k), so applying
this formula to lossy counts would reward photon loss. The initial experiment
is strictly ideal lossless. Any future loss extension must explicitly score
losses as failures and prove its cost/normalization convention before use.
No QPU protocol is authorized by a positive expectation diagnostic alone.
