# Grouped-output domination for passive single-photon optimization proposals

Base: `f09c7ec82b2fe23395116e21bd56614f3739107c`.
Author/route: P41 encoding lane. Date: 2026-11-24.
Status: complete derivation below; independent proof audit PENDING.
Novelty: OPEN. The scalar random-sign permanent identity is established prior
work; see `research/P41_encoding_sources.md`. No optimization advantage, QPU
result, or impossibility for unrestricted photonic optimization is claimed.

## 1. Exact claim

Let k>=1 and let V:C^k -> C^m satisfy V*V<=I. The source has one identical
photon in each of k distinct input modes. V is the occupied-input map to the
observed output modes of a passive network, possibly with loss/vacuum modes
omitted. Choose k disjoint nonempty output mode groups G_1,...,G_k. They need
not exhaust all modes and need not have equal sizes.

Accept only occupations with one photon in every G_g and no photons elsewhere.
An accepted output is x=(x_1,...,x_k), x_g in G_g. Since its occupied output
modes and occupied input modes are all distinct, its UNCONDITIONED physical
probability is

    p_V(x) = |per(V[x_1,...,x_k;1,...,k])|^2.

Invalid outcomes, loss and rejected heralds are failures, not free retries.
For paired groups of graph vertices, x selects one vertex from each pair and
is therefore a balanced partition of the paired vertices.

There is a classical randomized algorithm using O(mk) arithmetic and O(m+k)
auxiliary storage per attempted proposal, given V, with subprobabilities
q_V(x) satisfying simultaneously

    q_V(x) >= p_V(x) for EVERY accepted x,
    sum_x q_V(x) <= 1.

It uses no graph score, optimum, mask, permanent, or exponential support
enumeration. A unitary/isometry check is preprocessing, not free validation.
The arithmetic statement is exact; floating implementation needs tolerance
control, and bit complexity depends on the input representation/precision.

## 2. Constructive sampler and proof

Draw independent signs s_a uniformly from {-1,+1}; form beta=V s. For each
group put I_g=sum_(j in G_g)|beta_j|^2 and w=prod_g I_g. Contraction gives

    sum_g I_g <= ||V s||^2 <= ||s||^2 = k.

AM-GM therefore gives 0<=w<=1. Accept with probability w. When w>0, sample
one x_g independently per group with probability |beta_(x_g)|^2/I_g. If a
group intensity is zero then w=0 and the attempt fails. Conditional on s,
the unconditional output mass is exactly

    w * prod_g |beta_(x_g)|^2/I_g = prod_g |beta_(x_g)|^2.

Hence q_V(x)=E_s |f_x(s)|^2, where

    f_x(s)=prod_g sum_a V_(x_g,a) s_a.

The known random-sign permanent identity is

    per(V[x,:]) = E_s [ (prod_a s_a) f_x(s) ].

For completeness, expand the degree-k polynomial f_x. A monomial survives
after multiplication by prod_a s_a only if every variable appears an odd
number of times. Since the total degree is k in k variables, every exponent
must then be exactly one. Its coefficient is the permanent, without an
additional k! or occupation factorial. Cauchy-Schwarz and |prod_a s_a|=1 give

    p_V(x) <= E_s |f_x(s)|^2 = q_V(x).

Normalization follows independently from

    sum_x q_V(x) = E_s prod_g I_g = E_s w <= 1.

The proof applies to every V and fixed grouping, including graph-dependent
choices; it has no distribution-of-graphs, label-order, density-floor, weak-
interference or small-k hypothesis. A graph relabeling transports V and the
groups and preserves the pointwise assertion.

One may OMIT rejection and sample from normalized group intensities on every
attempt, using any fixed product fallback for zero-intensity groups. This
always-feasible law r_V also obeys r_V(x)>=q_V(x)>=p_V(x), because w<=1. It is
often a stronger practical baseline. Its one-score-per-proposal cost must be
recorded rather than hidden.

## 3. What the domination implies for optimization

For ANY set A of accepted outputs, including an unknown-optimum set used only
in retrospective evaluation or a graph-cost threshold,

    Pr_classical(output in A) >= Pr_bosonic(output in A)

per attempted proposal. More generally it holds for every nonnegative utility
u(x). Given a known incumbent cost c, u(x)=max(c-C_G(x),0) therefore gives a
no-smaller classical expected accepted improvement, without knowledge of C*.
Taking the better of the incumbent and one sampled proposal gives a no-higher
classical expected resulting cost. These are single-step conditional results
for every common fixed history from which V is selected.

For a predetermined sequence V_1,...,V_T and groupings, using independent
attempt randomness and a fixed threshold set A, the first-hit probability is
1-prod_t(1-p_t(A)); replacing every p_t by q_t can only increase it. This also
applies to graph-dependent nonadaptive schedules frozen after training.

The algorithm is a strong correlated feasible control, not the independently
routed distinguishable-photon law. It can dominate a bosonic law even where
the latter beats the same-V distinguishable law on selected feasible events.

### Resource limitation that cannot be omitted

This theorem compares attempted proposals and nonnegative utility, not all
definitions of total computational cost. The classical sampler can return
MORE feasible candidates, hence may make more graph-score evaluations at
equal attempt count. A binding smaller realized score budget is not covered.
If one phase-and-score step costs no more than one charged physical optical
attempt, the domination transfers to that measured cost model. That inequality
must be established for an application, not assumed from the word classical.
Report attempts, injected photons, graph-score queries, preparation/training
and CPU/wall time separately.

Pointwise domination does not automatically imply an efficient simulation of
an arbitrary adaptive quantum training transcript. A garbling using ratios
p_V(x)/q_V(x) would generally require permanents. Nor does it prove that the
same parameter optimizer finds equally good V under distinct noisy training
objectives. Those training questions remain OPEN. Freezing a learned V and
replacing only inference by this sampler is nevertheless a valid ablation.

## 4. Separable state cover and the two-qubit frontier

Define the unnormalized product vector

    chi_s = tensor_g (sum_(j in G_g) beta_j |j>_g),
    Sigma = E_s |chi_s><chi_s|,
    T = E_s (prod_a s_a) chi_s.

T is precisely the unnormalized accepted bosonic state. Sigma is fully
separable, Tr Sigma=E_s w<=1, and

    Sigma - |T><T| >= 0.

Indeed for any test vector z this is the nonnegative variance
E_s|<z,chi_s>|^2 - |E_s (prod_a s_a)<z,chi_s>|^2. Thus this is an operator
statement, and the scalar probability bound holds in any product readout
basis obtained by local group unitaries.

Writing p=||T||^2>0 and phi=T/sqrt(p), any lower bound on the trace of a
separable PSD operator dominating |phi><phi| yields a preparation-probability
upper bound. In robustness notation this gives

    p [1+R_generalized(phi)] <= 1,

when generalized robustness is defined as the minimum trace of such a
separable PSD cover minus one. This definition is explicit so this consequence
does not rely on an unverified entanglement-measure identity.

For TWO dual-rail groups a direct proof avoids that external dependency.
Split the two orthonormal occupied columns u,v into A and B; no losses or
other output modes in this paragraph. Let x=||u_A||^2, y=||v_A||^2 and
z=|<u_A,v_A>|^2. Orthogonality gives <u_B,v_B>=-<u_A,v_A>. The rejected
two-photon probability is

    1-p = xy+(1-x)(1-y)+2z.

The accepted 2x2 amplitude matrix is T=u_A v_B^T+v_A u_B^T. Its conditional
pure-state concurrence is C=2|det T|/p. The determinant identity gives

    p C = 2 sqrt[(xy-z)((1-x)(1-y)-z)]
        <= xy+(1-x)(1-y)-2z <= 1-p.

The radicands are Gram determinants and nonnegative. Hence

    p <= 1/(1+C).

This is SHARP for every C in [0,1]. Choose normalized orthogonal columns

    u=(sqrt(a),0,sqrt(1-a),0),
    v=(0,sqrt(1-a),0,sqrt(a)),       a in [1/2,1].

Then p=a^2+(1-a)^2, pC=2a(1-a)=1-p, and C continuously spans [1,0].
The full state is not a heralded usable Bell pair: the one-per-group event is
a coincidence/postselection condition. Do not confuse this with a theorem
about detecting only additional ancilla photons and retaining unmeasured
logical photons.

## 5. Scope, extensions and escape conditions

- Arbitrary groups, including singleton groups for specified single-photon
  herald detections, are allowed. Vacuum output modes can be omitted. Passive
  loss gives a contraction and only reduces accepted k-photon probabilities.
- Extra SINGLE input photons are allowed if every photon is assigned to one
  accepted one-photon output group (logical or herald). This does not cover
  arbitrary herald-pattern unions that cannot be represented by one grouping.
- An input occupation exceeding one introduces occupation factorials and is
  not covered by the unit-constant assertion as stated.
- General k-of-m collision-free decoding is a union of many transversal
  families; summing separate covers can destroy normalization. This theorem
  does not close that class, arbitrary collision recycling, quantum memory,
  intermediate adaptive quantum measurements or active/nonlinear elements.
- Unknown source/detector noise and dark counts are not silently represented
  by V. All experimentally used assumptions require separate validation.

The failed all-CF extension has an explicit exact control. Take occupied
columns u=(3/5,4/5,0,0) and v=(0,0,3/5,4/5). The six unstratified products
E_s |(Vs)_i(Vs)_j|^2, i<j, sum to913/625>1. They are not a probability law.
Normalizing by that sum can destroy their pointwise dominance. This refutes
that extension of the construction, not every possible classical control.

## 6. Route disposition

The deterministic feasibility/product-state fact is a known limiting input.
The useful new route-specific consequence is the explicit normalized correlated
classical control for grouped accepted output utility. Whether this composition
has appeared previously is unresolved; scalar Gurvits/Glynn ingredients are
known and must be attributed. It is not a blanket impossibility theorem for
photonic balanced optimization, and it does not close P41's unrestricted goal.
Next: independent proof audit, exact finite falsification, primary-source
comparison, and measured resource-aware use as a baseline in any paired-output
proposal experiment. No manuscript or hardware advancement follows yet.
