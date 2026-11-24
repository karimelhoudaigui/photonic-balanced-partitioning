# P41 encoding — two exact limits of the domination implication

This note supplements the frozen grouped-output proof, without changing its
input hash or its finite record. These are logical range checks, not positive
quantum optimization results. Author derivations; independent audit pending.

## A. Accepted-query conditioning can reverse the comparison

In the sharp two-group family, take c=3/5,s=4/5 and the occupied columns

    u=(c,0,s,0),   v=(0,s,0,c),
    groups A={0,1}, B={2,3}.

The only nonzero accepted bosonic probabilities are

    p(0,3)=c^4=81/625,    p(1,2)=s^4=256/625.

Thus P_F=337/625. The random-sign sampler has group intensities exactly one
for every sign vector, so it always returns a candidate. Its four masses are

    q(0,3)=81/625, q(1,2)=256/625,
    q(0,2)=q(1,3)=144/625.

It dominates p pointwise, yet for A_good={(0,3),(1,2)} the rates per returned
candidate are p(A_good)/P_F=1 and q(A_good)/sum(q)=337/625. Per attempted
proposal, both have exactly337/625 success. The optical failures explain the
difference; they must be charged. This construction is already classically
reproducible because the occupied columns have disjoint physical supports,
so it is not an interference-dependent benefit.

Consequently a statement at equal proposal count cannot simply be relabeled
as a statement at equal REALIZED number of scored feasible candidates. A
binding score-query budget or large score cost needs separate accounting.

The exact columns/accepted laws for this example were included in the frozen
16-case probe before execution; this interpretation does not add a new sample.

## B. Local pointwise domination does not preserve an arbitrary feedback policy

Consider an abstract incumbent-only greedy process with states c,a,b,g of
costs4,3,2,0. A returned candidate is retained if it improves the incumbent.
The same fixed update policy is used by two proposal kernels P and Q.

At c, P returns a with probability1/2 and failure with probability1/2.
At c, Q returns a with probability1/2 and b with probability1/2.
At a, BOTH return g deterministically. At b, BOTH return b forever. At g,
both remain g. Thus Q has no less mass than P on every VALID candidate at
every shared history/state. It also has at least as much immediate expected
positive improvement at each common state.

Starting at c, by time3 the P policy reaches g with probability

    1/2 + (1/2)(1/2) = 3/4.

The Q policy reaches g only when its first candidate was a, so its probability
by time3 is1/2. Its additional immediate improvement to b leads into a trap.

This is a counterexample to a LOGICAL inference from pointwise per-step
subprobability domination to equal-feedback-policy multi-step domination.
It is not claimed to be a physically realized pair of optical kernels, and
does not refute a stronger theorem exploiting additional optical structure or
an intelligently changed classical policy. It shows why that additional
argument is necessary. The fixed/nonadaptive first-hit corollary remains valid.

## C. Arbitrary collision-free subsets require a normalization factor

For a k-column contraction V, the unstratified random-sign mass over ALL
collision-free k-subsets of m output modes is E_s e_k(|Vs|^2), where e_k is
the elementary symmetric polynomial. Its natural upper bound is

    A_(m,k)=binom(m,k)(k/m)^k.

It follows by pairwise averaging of intensities at fixed sum<=k: holding all
but two coordinates fixed, e_k is an increasing affine function of their
product at fixed pair sum. Repeated smoothing reaches equal coordinates.
For m=2k this factor is binom(2k,k)/2^k, which grows exponentially in k.

The exact k2,m4 control u=(3/5,4/5,0,0), v=(0,0,3/5,4/5) has unstratified
mass913/625>1, as retained in the finite record. Dividing by an upper envelope
gives q_normalized(x)>=p_b(x)/A_(m,k), not unit-constant domination. Therefore
the grouped theorem does not close general fixed-number collision-free graph
bisection; choosing a single pair matching genuinely restricts the acceptance
family. An arbitrary union of independently normalized covers cannot be used
without accounting for its total mass.
