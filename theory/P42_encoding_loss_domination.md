# P42 — independent reconstruction of physical-loss domination

Date2026-11-24. Base of this lane: `03e6cf8`, descended from the P41 contract
atf09c7ec. This file is new; sealed P41 inputs and records are unchanged.
Sections 1–7 were derived by the encoding lane after the coordinator supplied
the question, without supplying its proposed proof or constants. Section 8
was added after reading the coordinator's threshold spectral argument and
explicitly attributes that dependence. Shared P41 context and the common
model remain independence limitations. Proof audit and novelty OPEN. No
numerical execution is claimed in this note.

## 1. Physical model and output contract

Let1<=k<=N<=m. A passive lossless m-mode interferometer U receives one
identical photon in each input a in a fixed set A of sizeN, other inputs
vacuum. Every photon undergoes independent uniform pure loss with survival
eta in[0,1]. Uniform loss commutes with U. Source, circuit and detector noise
beyond this channel are not silently included.
There is a single terminal number or threshold measurement. Intermediate
heralding with feedforward is not represented by a single passive U and is
outside the model unless separately reduced to it.

The first output contract accepts exactlyk detected photons with distinct
spatial modes S subset[m], |S|=k. Collisions, different detected counts and
losses are failures, not free retries. The PER-EMISSION-ATTEMPT probability is

    P_eta(S)=mu_(N,k)(eta) sum_(R subset A, |R|=k) |per U[S,R]|^2,
    mu_(N,k)(eta)=eta^k(1-eta)^(N-k).                         (1)

Each R is a possible survivor set, not a trained optimal-state mask. The
conditional law given exactlyk survivors divides the sum bybinom(N,k).
The binomial sector probability isbinom(N,k) mu; these three quantities must
not be conflated. Empty products are1 at endpoints; conditioning on an
event of zero probability is left undefined. The classical proposal may use
the same graph-dependent circuit matrix and input set, with their classical
preprocessing charged. It never needs C* or an optimal partition.

In graph bisection m=2k; S is a feasible balanced subset. No Haar assumption,
fixed density floor, shallow-circuit assumption or smallk is made.

## 2. A polynomial classical CF proposal

Let V=U[:,A], an m-by-N isometry. Draw N independent signs s_a in{-1,+1},
put beta=Vs and I_i=|beta_i|^2. Then sum_i I_i=N. Define

    e_k(I)=sum_(|S|=k) prod_(i in S) I_i,
    B_(m,k,N)=binom(m,k)(N/m)^k.                             (2)

The elementary symmetric mean bound gives e_k(I)<=B. A self-contained proof
is smoothing: among all maximizers at fixed sumN choose one minimizing the
squared Euclidean norm. Replacing any unequal pair by their average does
not decrease e_k (its increase is the nonnegative pair-product increase
times e_(k-2) on the remaining coordinates), while strictly decreasing that
norm. Hence the chosen maximizer is uniform. The casek=1 is the fixed-sum
identity. This proves(2) including zero coordinates.

Classical rejecting proposal:

1. Draw s and compute I.
2. Accept with probability e_k(I)/B, which lies in[0,1].
3. If accepted, draw a k-subset S with mass prod_(i in S)I_i/e_k(I).

If e_k(I)=0, reject. The unconditional classical mass is

    Q(S)= E_s prod_(i in S)I_i / B,    sum_S Q(S)<=1.         (3)

The weighted k-subset draw does not require enumeratingbinom(m,k) subsets.
For nonnegative weights w, build suffix values

    E[m,0]=1, E[m,r>0]=0,
    E[i,r]=E[i+1,r]+w_i E[i+1,r-1].                         (4)

While r items remain, include i with probability
w_i E[i+1,r-1]/E[i,r]; otherwise omit it. Telescoping gives the required
product-weight law. Only positive-probability branches are used. This is
the known conditional-Poisson/diagonal-k-DPP recursion, not a new DP.
The wave costs O(mN), the table O(mk), and the draw O(m); memory beyond
the matrix is O(mk+N). Form=2k,N<=m this is O(mk) arithmetic per proposal.
Matrix construction/validation, random bits, precision and scoring are
additional costs. The exact claim is in the arithmetic model.

## 3. Fourier/Bessel domination, including N>k

For fixed S, let f_S(s)=prod_(i in S) sum_(a in A)V_ia s_a. For each
R subset A with |R|=k, its degree-k Fourier coefficient is

    E_s [(prod_(a in R)s_a) f_S(s)] = per U[S,R].             (5)

Indeed any contributing monomial must be odd on allk coordinates in R;
total degree k then forces exactly one copy of every such coordinate and
zero copies elsewhere. No factorial is missing because S and R are CF.
The distinct sign characters prod_(a in R)s_a are orthonormal. Bessel gives

    E_s |f_S(s)|^2 >= sum_(|R|=k) |per U[S,R]|^2.            (6)

Combining(1),(3),(6) proves physical pointwise domination whenever

    B_(m,k,N) eta^k(1-eta)^(N-k) <= 1.                      (7)

Under(7), Q(S)>=P_eta(S) simultaneously for every accepted S. The always-
feasible variant omits the rejection and draws from the normalized product-
weight law, with a uniform k-subset fallback when e_k(I)=0. Its output law
is pointwise >=Q, so it too dominates. Its higher frequency of scored
candidates must be charged.

WhenN=k, (7) becomes

    eta <= m/[k binom(m,k)^(1/k)].                          (8)

For m=2k this is2/binom(2k,k)^(1/k); eta<=1/2 is sufficient for everyk,
becausebinom(2k,k)<=4^k. The finite criterion(8) is stronger than that
simple uniform constant. This is not a claim of an optimal classical
threshold; it is a sufficient threshold for this explicit construction.

For anyN>k the maximum of mu_(N,k) over eta occurs ateta=k/N. Thus an
all-transmission sufficient condition is

    binom(m,k)(k/m)^k(1-k/N)^(N-k) <= 1.                    (9)

In particularN=m satisfies(9), since its left side is a binomial point
probability. Near-full sources can also satisfy it; see Section6.

## 4. A history-independent uniform proposal and adaptive first-hit result

The k-photon passive representation U^(k) is unitary. The number states |R>
for the CF surviving inputs are orthonormal, so for every fixed CF output S,

    sum_(R subset A, |R|=k) |<S|U^(k)|R>|^2 <= 1.           (10)

This is ordinary Hilbert-space Bessel, distinct from the sign-cube Bessel
step(6). Therefore P_eta(S)<=mu_(N,k). A UNIFORM feasible k-subset draw,
which does not need U or any circuit training, pointwise dominates whenever

    binom(m,k) eta^k(1-eta)^(N-k) <= 1.                    (11)

Condition(11) is generally more restrictive than(7), but its history-INDEPENDENT
dominator yields an additional adaptive theorem. Let B be any fixed set of
feasible subsets, e.g. a graph-cost threshold. Suppose every fresh optical
attempt can choose U_t, sourceA_t, N_t and eta_t from its classical history,
but(11) holds on every possible history. There is no persistent quantum
memory or history-dependent change of the target B. Then

    Pr(optical hit B by T attempts)
       <= 1-(1-|B|/binom(m,k))^T.                          (12)

Proof: before a first hit, each conditional success probability is at most
|B|/binom(m,k), so the conditional failure probability is at least the
complement. Iterate conditional expectation. Independent uniform feasible
draws attain the right side. This does not require efficiently reproducing
the optical history. Applying(12) to every fixed cost threshold gives
stochastic domination of the best cost after T attempts. In particular,
its tail bound gives an optical expected first-hit attempt count AT LEAST
that of the uniform geometric law for a nonempty B, allowing infinity;
it does not give an upper bound on the optical hitting expectation.

For m=2k, eta_t<=1/4 is a simple sufficient condition uniformly over all
k<=N_t<=m: binom(2k,k)mu<=4^k eta_t^k<=1. This includes oracle-informed
circuits as a mathematical statement, although oracle inputs remain forbidden
in the project's training experiments.

N=m has a sharper statement for perfectly identical photons. Conditional
onK=k survivors, the input density is

    rho_k=Pi_(CF,k)/binom(m,k).

Thus U^(k)rho_k U^(k)*<=I/binom(m,k), and each CF output probability is
at most1/binom(m,k), for EVERY interferometer. Uniform feasible draws
dominate already per observed k-survivor sector, before charging the
binomial loss lottery. Multiplying by that lottery preserves the per-
emission result for everyeta. The adaptive argument(12) follows as well.
This is not P37's Haar average: U can be graph-trained or history-dependent.
It still accepts CF exactlyk survivors, not arbitrary threshold k-clicks.

## 5. Threshold decoding: collisions need not be discarded at low eta

Now accept any detected occupation t whose SUPPORT is S, |S|=k, allowing
l=|t|>=k detected photons. This is the threshold-bitstring model used by
P37, unlike the exact-CF contract above. Keep N in[k,m] and set r=eta/(1-eta)
for0<eta<1. For fixed t of totall define

    f_t(s)=prod_i (sum_a V_ia s_a)^(t_i) / sqrt(prod_i t_i!).

Its Fourier coefficient for any R of sizel is exactly the physical Fock
transition amplitude per(U[t,R])/sqrt(prod_i t_i!). Distinct R characters
are orthonormal, so

    sum_(|R|=l) Pr(R -> t) <= E_s |f_t(s)|^2.               (13)

Multiply by eta^l(1-eta)^(N-l), sum over all t with support S and l<=N,
then extend that positive sum tol=infinity. It follows that

    P_eta(threshold support S)
      <= (1-eta)^N E_s prod_(i in S)[exp(r I_i)-1].         (14)

The extension to infinity introduces virtual extra-photon terms only in the
CLASSICAL upper cover, not in the physical source or its raw data.

For fixed signs put w_i=expm1(rI_i) and

    W_s=(1-eta)^N e_k(w).                                  (15)

Whenever W_s<=1 for all signs, draw signs, accept with probability W_s,
and draw a product-weight k-subset using(4). The resulting mass is the
right side of(14), hence it dominates every physical threshold bitstring.
Omitting rejection again gives an always-feasible dominating law. Complexity
is O(mN+mk) plus m exponentials and scoring, not an exponential enumeration
of photon occupations. Numerical exponentials and tiny weights need controlled
precision; no finite-bit implementation theorem is asserted here.

Here is an explicit uniform sufficient transmission range. Let independent
Poisson counts have means rI_i; their total L is Poisson with mean lambda=Nr.
The count of nonempty modes K has

    Pr(K=k)=exp(-lambda)e_k(expm1(rI)),
    Pr(K=k)<=Pr(L>=k).

Forlambda<=k, the elementary exponential-moment bound gives

    Pr(L>=k)<=exp(-lambda)(e lambda/k)^k.

Consequently

    W_s <= (1-eta)^N (e Nr/k)^k
         = [e (N/k) eta (1-eta)^(N/k-1)]^k.                 (16)

Let

    eta_threshold = [1-sqrt(1-2/e)]/2.                      (17)

This root is less than1/3 becausee>9/4. Ifeta<=eta_threshold, lambda/k
<=2eta/(1-eta)<=1 forN<=2k. Also, foralpha=N/k in[1,2], the function
alpha(1-eta)^(alpha-1) increases withalpha: its logarithmic derivative is
1/alpha+log(1-eta)>=1/2+log(2/3)>0, again usinge>9/4. Thus(16) is at most

    [2e eta(1-eta)]^k <= 1.                                (18)

Equations(14)–(18) therefore give a normalized efficient classical control
for ALL balanced threshold supports, including collisions and every physical
survivor sector, under(17), m=2k andk<=N<=m. No Haar assumption is used.
This is a worst-case sufficient bound, not an optimal transmission boundary.
It is not a full-output quantum-law simulator and has no TV approximation
claim. It targets nonnegative support utility per physical attempt.

## 6. Near-full-source all-eta CF corollaries

For reference, the exact criterion(9) has simple balanced near-full cases.
An elementary central-binomial bound is

    a_k=binom(2k,k)/4^k <=1/sqrt(3k+1).

Induct fromk=0 using a_(k+1)/a_k=(2k+1)/(2k+2); the squared comparison
to sqrt((3k+1)/(3k+4)) reduces tok>=0.

ForN=2k-1, the left side of(9) is

    2 a_k [1-1/(2k-1)]^(k-1) <= 2/sqrt(3k+1) <=1.

Use the empty-product convention atk=1. Thus N=m-1 also satisfies CF
domination for everyeta. ForN=2k-2, k>=3, the bound is

    4 a_k [(k-2)/(k-1)]^(k-2) <=4/sqrt(3k+1).

This is sufficient fork>=5; k=3 and4 give5/8 and35/72 directly. These
are exact symbolic corollaries, not numeric sweeps. They do NOT imply the
same all-eta result for threshold supports with more thank surviving photons.

## 7. Resource contract, calibration and non-implications

All domination statements compare attempted proposals or specified physical
survivor sectors. A classical feasible control may score more candidates
than the optical process at equal raw attempt count. Therefore equal
REALIZED objective-query count, total wall time, memory or monetary cost
does not follow automatically. Use joint declared ceilings, or establish
a measured inequality c_classical-wave+c_score<=c_optical-raw-attempt in the
chosen common cost model. Uniform controls avoid circuit construction and
training altogether, which can strengthen the cost comparison, but their
scoring time is still charged. Classical arithmetic is not injected photons.

A common classical frontend F(G,H,seed) may construct the source, V and a
fixed mode-to-vertex decoding from graph G and classical history H. Charge
its construction, all training scores and all tuning in both comparisons.
A fixed-circuit substitution can reuse an already learned V, retaining the
cost of acquiring it; that substitution is not a proof that a wholly
classical optimizer can learn the same V at the same cost. Changing the
frontend's feedback history changes V and need not preserve the wave-law
comparison through an entire adaptive training run. The uniform result in
Section 4 instead eliminates dependence on V and therefore proves its stated
adaptive bound without reproducing that history. A history-dependent
many-to-one decoder or classical repair step needs its own comparison;
uniform k-subsets cannot silently be identified with its resulting partition
law. For a fixed shared decoder, the pointwise laws can instead be pushed
forward and good-set cardinality is that of its preimage.

Terminal-best statements here refer to decoded optical support candidates
and any COMMON INITIAL incumbent. If a frontend also scores or returns
additional classically generated candidates, the overall hybrid best cost
is not bounded solely by the optical hit calculation. Those candidates
must be shared with the classical control, charged, and separately included
in its comparison. No arbitrary classical solver is hidden in a free
frontend. See the explicit scope checks in P42_encoding_scope_checks.md.

For physical data, use calibrated emission-attempt denominators and upper
confidence bounds appropriate to the actual loss model; do not substitute
vendor nonempty-detection shots or a public average transmittance. Uniform
loss/source assumptions and identical photons are hypotheses, not inferred
from a platform name. State-dependent or mode-dependent losses, dark counts,
input multiphotons and unrecorded filtering require new analysis.

The wave/threshold dominators depend on the common V. They imply nonnegative
utility and fixed/nonadaptive batch first-hit domination, not a universal
equal-feedback-policy adaptive theorem; P41's abstract trap counterexample
still applies. The history-independent uniform criterion(11) is different
and DOES yield the adaptive first-hit bound(12). It cannot be transferred
outside its hypotheses.

Perfect indistinguishability matters to the simple Fock projector argument
in(10). Do not silently use it for arbitrary internal Gram matrices. A
vector-valued random-wave proof can cover known internal pure states, using
beta_i=sum_a U_ia s_a phi_a and I_i=||beta_i||^2; occupied full orbitals remain
orthonormal. Then(6)/(13) hold componentwise and the same normalizers apply,
but computing intensities can cost O(mN^2) for a general known Gram matrix.
That extension needs separate audit; it is not the O(mk) scalar claim.

No numerical experiment, independent proof acceptance, novelty certificate,
hardware validation or manuscript integration has been performed for P42.
The scalar permanent identity, uniform-loss mixture, elementary-symmetric
DP and Poisson Chernoff bound are established ingredients. The composition
and optimization scope must receive independent source comparison.

## 8. Coordinator-origin threshold rank bound and uniform adaptive control

This section was added AFTER the coordinator communicated the spectral
argument. It is a verification and refinement, not a blind reconstruction.
The photon identity and loss hypotheses of Section 1 remain essential.

Let l be a detected-photon sector. Its unnormalized density operator is

    rho_l = eta^l(1-eta)^(N-l) U^(l) Pi_(A,CF,l) U^(l)*,

where Pi_(A,CF,l) projects onto the binom(N,l) distinct-input survivor states.
Thus rho_l <= eta^l(1-eta)^(N-l) I. The projector onto occupation states with
SUPPORT exactly S, |S|=k, has rank binom(l-1,k-1), by positive compositions
of l into k parts. It follows that

    P_eta(threshold support S) <= M_(N,k)(eta),
    M_(N,k)(eta) = sum_(l=k..N) binom(l-1,k-1)
                                  eta^l(1-eta)^(N-l).       (19)

One may replace each binomial rank in(19) by
min{binom(l-1,k-1),binom(N,l)}, using also the sector trace bound; the
unrefined expression is sufficient below. Neither expression is asserted to
be sharp or physically saturable simultaneously across sectors.

Write D=binom(m,k). A uniform feasible draw dominates every threshold output
per physical attempt if D M_(N,k)(eta)<=1. A history-dependent source and
transmission are allowed if the same uniform cap holds at every history.
As in Section 4, the decoder is a fixed support-to-partition mapping and the
target good set B is fixed by a graph-cost threshold.

There is also a rigorous allowance for DIFFERENT declared attempt ceilings.
Let the optical algorithm use at most n_Q fresh attempts and the uniform
classical search n_C>=1 independent feasible draws. Put

    L=ceil(n_Q/n_C) if n_Q>0, and L=1 if n_Q=0,
    M_max=sup M_(N_t,k)(eta_t) over all admissible histories.

If L D M_max<=1, then uniform classical search stochastically dominates the
optical terminal best cost AMONG SUPPORT CANDIDATES and a common initial
incumbent. To prove it, put p=|B|/D. Each conditional optical
hit probability before its first hit is at most p/L, whence its no-hit
probability is at least (1-p/L)^n_Q. Since n_Q<=L n_C and
(1-p/L)^L>=1-p, this is at least (1-p)^n_C, exactly the no-hit probability
of the classical control. This holds for every fixed cost threshold, with
arbitrary classical-history changes of U, A, N and eta satisfying the cap.
Fresh attempts have no coherent quantum memory linking them; classical
adaptation between attempts is allowed. The argument compares declared attempts; obtaining n_Q
and n_C from equal total measured cost still requires the Section 7 model.

A simple improvement of the coordinator's initial all-N transmission bound
comes from discarding only the factor (1-eta)^(N-l)<=1 and extending l:

    M_(N,k)(eta)
      <= sum_(l=k..infinity) binom(l-1,k-1) eta^l
       = [eta/(1-eta)]^k,      0<=eta<1.                   (20)

The last equality is the elementary negative-binomial generating function.
For m=2k, D<=4^k, so eta<=1/5 gives L=1 uniform domination for EVERY k,
EVERY N in[k,m], EVERY U and threshold support, including all collisions.
This is adaptive domination by a control that needs neither V nor optical
training. It is not a claim that1/5 is optimal. For general L, the sufficient
finite-k criterion is L D [eta_max/(1-eta_max)]^k<=1. If eta_max is below1/5,
the allowed optical-to-classical attempt ratio can grow exponentially withk;
whether that allowance covers measured scoring and optical costs is an
experimental resource-accounting question.

The coordinator's initial alternative bound was

    M_(N,k)(eta) <= (1-eta)^N [eta/(1-2eta)]^k
                   <= [eta(1-eta)/(1-2eta)]^k, eta<1/2.

It follows by extending the sum after factoring eta^k(1-eta)^(N-k).
Together with D<=4^k it gives eta<=(3-sqrt(5))/4. Equation(20) is at least
as strong for eta>=0 in that range. These displayed bounds are algebraic
proofs, not finite parameter sweeps or new observed QPU measurements.
