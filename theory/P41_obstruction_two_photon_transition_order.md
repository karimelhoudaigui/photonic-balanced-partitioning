# P41/R3 — two-photon raw proposals cannot strictly dominate every move

Base f09c7ec82b2fe23395116e21bd56614f3739107c. Analytic self-review only;
independent proof audit pending. No new numerical experiment or novelty claim.

Let S={a,b} be the current collision-free two-photon configuration in m modes.
Apply any passive unitary and retain the complete physical attempt law. Let
q_B(S,T), q_D(S,T) be the unconditioned probabilities of a collision-free
two-element output T for indistinguishable and independently routed labelled
photons. Collision attempts are failures/self-loops, not renormalized away.

**Theorem.** If q_B(S,T)>=q_D(S,T) for every collision-free T!=S, then equality
holds for every such T. Thus a two-photon passive proposal cannot improve at
least one nontrivial move while weakly improving all other nontrivial moves
against the same-unitary distinguishable proposal.

Proof. Set u=U[:,a],v=U[:,b], z_i=u_i conjugate(v_i). Then sum_i z_i=0 and

    q_B(S,{i,j})-q_D(S,{i,j})=2Re(z_i conjugate(z_j)), i!=j.

For any i outside S, all pairs {i,j} differ from S, so by the hypothesis every
Re(z_i conjugate(z_j)) is nonnegative. Orthogonality gives

    0=Re(z_i conjugate(sum_j z_j))
     =|z_i|^2+sum_(j!=i)Re(z_i conjugate(z_j)).

Every summand is nonnegative, so z_i=0. Hence z is supported within S.
Every T!=S contains an index outside S and its probability difference is zero.
For m=2 there are no nontrivial feasible moves and the conclusion is vacuous.

This is a row-wise raw-proposal statement. With a common Metropolis acceptance
function that is strictly positive on all distinct feasible states (finite
inverse temperature and finite energies), a pointwise off-diagonal ordering
of accepted kernels is equivalent to the same proposal ordering, so strict
ordering is also impossible. It does not order spectral gaps or mixing times:
tradeoffs among moves can improve them. At zero temperature some acceptances
vanish, so the inference from accepted kernels back to all raw proposals is
invalid. Nor does this theorem compare reoptimized interferometers.

Conditioning on no collisions changes the denominator and is outside the
theorem. The optical rejection probability must remain charged in any claim
about physical attempts. The result is not a generic statement that quantum
Markov chains cannot help optimization.

## Why the proof cannot be extended by changing the photon count

For three occupied input modes, the normalized Fourier tritter has probability
1/3 for its unique collision-free output and the independent routing reference
has probability 3!/3^3=2/9. This is a familiar three-photon interference fact,
not a new benchmark. A six-mode off-diagonal unitary with the tritter in both
off-diagonal blocks transports an occupied three-mode set to the other set;
on that input its only collision-free move has probability1/3 versus2/9.
Thus an unqualified extension of the theorem to three photons is false.

In balanced n6,k3 partitioning this specific move is merely complementation,
which has exactly the same cut cost as the starting partition. It provides no
optimization benefit. With deterministic spectators one can make a nontrivial
three-vertex exchange, but a fixed-size classical correlated proposal can
perform that exchange directly; it must be included as a control.

The useful frontier is therefore not a new same-circuit factor alone. A
candidate needs a graph-dependent tradeoff among many feasible transitions,
and comparison of mixing/discovery at matched complete cost. This theorem
can reject a proposed uniform two-photon Peskun-dominance explanation, while
leaving the P41 discovery objective open.
