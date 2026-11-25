# P45-A — occupation-guided cavity completion, before any numerical outcome

Base: `8f83f2bff321f658182a23aacf07d03b12c6633b`. Owner: adaptive lane.
Status: proposed mechanism and self-derived control dictionary; NO P45 run.
The positive discovery target remains OPEN. No theorem below is claimed novel.
This route does not duplicate encoding's stars-and-bars full-Fock decoder.

## Mechanism and first uncertain implication

For m=2k, N=k identical source photons occupy a shared charged classical
anchor S0. Set ell=A1-2A1_S0 and center ell by subtracting its mean. Use
H=normalize(A/||A||+kappa*diag(ell/||ell||_inf))
with zero matrices left zero, and U=exp(-itH). Angles are finite. All N photons
interfere graph-wide; no P43 echo, small isolated module, or CF rejection is used.

Let V=U[:,S0], mu_i=sum_a |V_ia|^2. A detected count n, including collisions
and partial/vacuum detections, supplies centered fluctuations n-eta*mu.
Standardize them using the bosonic variance below, with variance floor1e-12.
The decoder accepts any real standardized field y; it does not require a
physical nonnegative integer vector. This allows strong classical controls.

**Cavity completion:** choose q=ceil(k/2) DISTINCT seed vertices with largest
y_i, using a preassigned random vertex priority for ties. With partial set T,
add one remaining vertex minimizing

    d_i - 2*sum_(j in T) A_ij - lambda*mean_positive_edge_weight*y_i.

Repeat until |T|=k, then score its balanced cut once. No descent follows. The
first term is the exact marginal of cut(T), even while T is unbalanced. These
unbalanced marginal evaluations are CLASSICAL objective work: charge EVERY
candidate marginal inspected, not just the final feasible score. Their count is

    M(m,k,q)=sum_(r=q)^(k-1)(m-r),   score units=M+1.

For (m,k,q)=(16,8,4), M=42; for (20,10,5), M=65. Matrix/feature updates, sorting,
Gaussian factorization, all scoring and all times have separate ledgers too.
The fixed decoder often outputs UNCLICKED vertices. It is outside P44's
click-contained implication, but its classical work is not quantum work.

Hypothesis: the higher-order structure of the full B fluctuation field selects
collectively useful seed sets more often than reoptimized D, correlated fields,
moment-matched fields and classical feasible search after the SAME completion.
First uncertain implication: any B-over-D effect survives the moment-matched
and correlated classical controls, rather than just reflecting larger noise
variance, bunching, decoder quality, or a better classical starting candidate.
This is a falsifiable possibility, not a predicted or promised advantage.

## A shared incumbent that credits decoder-only discoveries

Construct S0 by the same charged best-one-swap front end for all models, at
most8 complete scans. Before stochastic training, evaluate and CREDIT the
observation-free decoder (y=0), a q=0 pure greedy construction, and vacuum
observations n=0 at every network/decoder setting. Their best scored partition
Sref, including S0, defines Cref. All models start with that PUBLIC incumbent.
The optical source stays the original fixed S0; source and incumbent are
separate recorded objects. Do not attribute preparation of S0/Sref, completion
of a vacuum, or improvements already found by these classical calls to photons.
Training gain is max(0,Cref-C(T)) on every raw attempt; every decoder gives a
feasible T and consumes its full classical cost, regardless of n's photon total.

## Exact low-order falsifiers, all computable without permanents

Write p_ia=|V_ia|^2, P=VV*, R=p p^T. For the binary source and uniform independent
fresh loss eta, normal ordering gives

    E n = eta*mu,
    C_D = eta*diag(mu) - eta^2*R,
    C_B = eta*diag(mu) + eta^2*(|P|^2-2R).

The diagonal includes the normally ordered variance correction. The ideal case
eta=1 is the first pilot; no Lucy efficiency is inferred. Standardization is
the SAME sqrt(max((C_B)_ii,1e-12)) for B, D and all raw-field controls.

Let independent z_a be uniform in {1,-1,i,-i}, and I=|Vz|^2. Expanding the fourth
moment of these phases gives E I=mu and Cov(I)=|P|^2-R. Therefore the independent
sum

    Y = (n_D-eta*mu) + eta*(I-mu)

has EXACTLY zero mean and covariance C_B. This is an O(mN) classical field,
not an asserted physical count distribution. Passing it through the SAME
nonlinear completion tests whether the proposed gain needs more than this
specific low-order surrogate. Also compare a Gaussian with covariance C_B,
and independent Gaussians with the SAME marginal variances. A negative answer
does not prove every distribution with matching moments is equivalent.

Other mandatory controls: independently reoptimized D; phase-multinomial
mean-field sampling; species of bounded size4; zero/vacuum decoder calls;
paired B fields with randomly permuted vertices, preserving their value
multisets while destroying graph alignment. Additional paired decoding is
explicit extra classical work, not an extra physical shot or a free candidate.

## Known mean-field envelope, reused rather than rediscovered

The random-phase condensate/multinomial control is already established in
Tichy et al., [arXiv:1312.3080v2, Eqs3-4](https://arxiv.org/pdf/1312.3080v2).
The continuous-phase overlap/twirl weight c_N=N!/N^N is a known input:
Hayashi et al., [arXiv:0710.1056v2, Eqs33-40](https://arxiv.org/html/0710.1056v2),
as previously audited in `research/P41_obstruction_phase_proxy_sources.md`.
Neither this sampler nor that weight is a new P45 result.

For clarity the finite-phase implementation has the same positive CF block.
The normalized N-photon condensate has source-Fock amplitudes

    sqrt(N!/(N^N*r!))*z^r,       sum_a r_a=N.

On twirling independent L-th roots, L>=2, the character of r=(1,...,1) cannot
alias another nonnegative composition of N: congruence r_a=1 mod L requires
every r_a>=1, and their sum is already N. Thus

    rho_field = (N!/N^N)|1^N><1^N| + rho_rest,  rho_rest>=0.

The same passive loss channel, positive measurement and arbitrary fixed decoder
preserve this PSD inequality. Consequently q_field(T)>=c_N*p_B(T) for ANY
completion output event, with unconditioned losses and collisions. Classically
sample z, then N independent categorical draws with probabilities |Vz|^2/N
(and loss category1-eta). This is the mean-field control, not exact B sampling.

The overhead1/c_N is already large at N8/10 (approximately416/2756). This is a
control envelope, NOT unit-coefficient domination or a finite-budget no-go.
For p_B=1 and q_field=c_N, no finite number of field draws guarantees success1;
do not infer full best-cost stochastic domination from this factor alone.
Adaptively replacing proposals also changes histories. Novelty of any concrete
optimization composition remains unassessed; do not claim it from a source search.

## Smallest proposed dev veto

Four NEW weighted ER/RR graphs at m16/20, fixed seeds in the companion contract;
2 replicates,4 network settings*2 decoder settings*4 draws=256 B attempts total.
Every sampled control separately chooses its own global setting. The same
decoder and full common preprocessing apply to every model. Each strong
classical baseline gets1376 score units per m16 graph/replicate,2112 per m20
case, matching32 completed samples, PLUS the same charged common front end.
This small pilot has little power and accepts NO positive discovery. No held-out
graph is opened, no QPU is called and the manuscript stays unchanged.

If B fails against moment-matched or correlated controls, or multistart feasible
search reproduces its best costs at the recorded score/time frontiers, reject
this mechanism/budget. A follow-up requires pooled improvement over separately
tuned D and every declared field/b4 control on at least3 of4 graph units,
evidence of graph alignment versus permuted observations, and no explanation
by decoder-only discoveries or strong feasible search. Even then it is only a
candidate for a fresh frozen held-out/independent experiment. No p-value,
universal novelty claim, measured hardware-resource edge or quantum advantage
can be accepted from this development screen.
