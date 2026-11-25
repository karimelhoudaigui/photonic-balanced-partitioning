# P62: random embeddings convert bounded-output control into classical frontiers

ROOT candidate proof, 25-Nov-2026. INDEPENDENT REVIEW PENDING. This is an
ideal probabilistic/algorithmic statement, not measured equal-wall-time
dominance, universal photonic impossibility, novelty clearance or completion
of the user's positive target. No program, graph or simulation is run here.

## Precise experiment and comparator

Fix any weighted graph G on N labeled vertices, a cardinality k, and a fixed
set A of s PHYSICAL output modes. Draw a uniform bijection Pi from modes to
vertices ONCE, independently of G, and retain it for the whole quantum run.
The policy may know G and Pi, use arbitrary previous observations/scores,
and adapt every parameter that affects the active modes.

Assume that in EVERY fresh shot, conditional on Pi and the ENTIRE past,
the count vector on O=A^c has one fixed law nu. In particular nu depends
on neither G,Pi,the selected parameters nor the past. Fresh outside counts
and independent fresh tie priorities have this same conditional law. No
assumption is imposed on the active counts given those outside counts.

This premise follows for fresh copies of a fixed state when all parameter
dependence is a trace-preserving LOCAL operation on A, followed by complete
number measurement. It does not follow merely from unchanged one-mode
intensities or low moments. All source/preparation/noise dependence outside
A must actually be excluded. Losses and collisions may be retained.

Decode by the k highest counts, breaking threshold ties uniformly. Equivalently
give each mode a fresh independent continuous priority, and rank pairs
(count,priority) lexicographically. Count magnitudes do not otherwise enter
the graph-dependent decoder. The reported candidates come from this decoder;
additional classically discovered candidates are outside this theorem's
decoded-best definition and must be accounted for separately. A common
graph-only initial incumbent independent of Pi can be included in both bests.
An arbitrary Pi-dependent frontend cannot be inserted without a new argument:
its success indicator can correlate with the conditional frontier failure
probability, invalidating the unweighted Jensen step below. There is no
postselection or omitted failed attempt.

Define a PURELY CLASSICAL trial:

1. Draw a uniform ordered partition of the graph vertices into s active
   labels B and a uniformly ordered list v_1,...,v_(N-s) of the rest.
2. For EVERY T subset of B with0<=k-|T|<=N-s, score the feasible set
   S_T=T union{v_1,...,v_(k-|T|)}.
3. Return the best scored cut. All candidates and their scores are paid.

There are at most2^s such candidates; for s<=k<=N-s there are exactly2^s
oriented candidates before any complement/duplicate-score caching. This
algorithm uses G only to evaluate actual feasible cuts, never C*, a known
optimal partition or an optimal-state mask. Repeat trials independently.

## Candidate theorem

For EVERY G, EVERY fixed integer T>=1 and EVERY real threshold c, the
classical algorithm satisfies

    Pr[min_(t<=T) C_G(S_class,t)>c]
      <= Pr[min_(t<=T) C_G(S_quantum,t)>c],                 (1)

where the right probability includes the ONCE-drawn uniform Pi and all
adaptive policy/count/tie randomness. The left uses fresh independent
classical frontiers. Thus the classical best cut stochastically dominates
the photonic best cut after T trials. The quantum law need not be classically
samplable, and the phase policy need not be optimum blind for this upper
bound. Neither assertion supplies a free classical evaluation budget.

## ROOT proof

Within a shot, fix the outside counts and their priorities. They induce an
ordering rho of O independent of every choice of active counts. If the
decoder picks active subset T, it must pick exactly the first k-|T| outside
modes. Therefore its output is ONE of the frontier candidates, regardless
of how strongly active counts depend on G,Pi,history or the outside values.

For fixed Pi let f_Pi(c) be the probability, under nu and outside priorities,
that ALL frontier candidates cost greater than c. The marginal outside law
is fixed conditionally on every past, so its frontier contexts are iid for
this Pi. A bad frontier forces the quantum candidate to be bad whatever
the policy does. Hence

    Pr[all T quantum costs>c | Pi] >= f_Pi(c)^T.             (2)

This can be proved by coupling iid outside contexts in advance, or by
iterating the conditional probability bound; independence of the actual
adaptive quantum candidate costs is NOT asserted.

For ANY fixed physical outside order rho, the uniform Pi sends the ordered
active modes and rho to a uniform ordering of graph vertices. Consequently
the averaged one-frontier bad probability is exactly the classical one:

    E_Pi f_Pi(c) = f_class(c).

Although quantum contexts generally correlate through its fixed Pi, that
correlation cannot be dropped. Averaging(2), then using convexity of x^T,
gives

    Pr[all T quantum costs>c] >= E_Pi[f_Pi(c)^T]
                              >= (E_Pi f_Pi(c))^T
                               = f_class(c)^T.

The last expression is precisely the failure probability of T independent
classical frontiers. This proves(1) and addresses the fixed-embedding
correlation rather than replacing it by iid unconditional quantum shots.

## Work, limits and the proposed N18 circuit

A uniform frontier can be generated in O(N) work. For bounded s, evaluating
it can use one base cut plus deltas in a core of at most2s vertices: the s
active vertices and the s outside boundary positions. With adjacency access
and paid graph loading, a conservative upper bound per trial is
O(E+N+s^2*2^s) arithmetic work. Naively evaluating2^s full cuts is also valid
but more expensive. Preprocessing/storage, random bits, every score and any
repair remain charged. No measured constant, deterministic wall-time ratio,
matched-photon price or automatic same-number-of-scores theorem is supplied.

The statement is about averages over the independent UNIFORM embedding. A
particular fixed favorable embedding may behave differently. A graph-dependent
embedding, graph-dependent outside source/circuit, reused correlated source
copies, extra graph-dependent decoder, changed cardinality or unrecorded
classical discoveries can violate its premises. Growing s can make the
frontier exponential; no efficient general classical sampler follows.
Uniform random physical embeddings are a stronger experimental condition
than merely renaming graph vertices while carrying the SAME physical map.
The latter checks label equivariance and does not average new embeddings.

The proposed P61 single-phase circuit has A={1,7,13}: changing the internal
(b1,i1) phase is conjugated by the fixed F3 on exactly these three outputs;
the final V mixes only color0 ports0,6 and commutes with that operation.
Its outside JOINT law is therefore fixed, not merely its intensities.
With a genuinely independent uniform graph-to-port mapping it has the
eight-candidate obstruction above. This is a reason to change the phase
support before another optimizer pilot, subject to independent verification.
An extensive phase pattern or global graph-dependent network changes a
specific premise; it does not automatically produce an advantage.
