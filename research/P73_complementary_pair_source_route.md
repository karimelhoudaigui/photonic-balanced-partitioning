# P73: complementary pair sources, weak-response controls and preparation costs

25-Nov-2026. STATIC research checkpoint after the P72 freeze. No scientific
Python, import, numerical probability, graph draw, sample, test, source
installation, QPU call or manuscript edit. Two primary papers were checked
through versioned official arXiv text; only this route note is written.

**Decision: REJECT a leading-order optimization/interference claim and any
free-source shortcut. KEEP the exact source law and controls. FOLLOW-UP is
open for finite-strength or different fixed-number sources only after a real
preparation/resource model and a discriminating mechanism are supplied.**
This changes the source and is outside P69's CF-input assumptions. The
analysis does not prove impossibility for all pair-source optimizers, and
it establishes no positive result, hardware readiness or novelty.

## 1. Physical model and complete-count acceptance

Let N=2k be the number of graph vertices, with EVEN k>=2. Let A be a real
symmetric, nonnegative, zero-diagonal weighted adjacency matrix. Put

    W=J_N-I_N+epsilon*A, epsilon>=0,
    Z=lambda*W, lambda>0, ||Z||op<1.

Prepare two INDEPENDENT pure zero-displacement Gaussian states with this
same pair matrix, in red and blue optical modes. This means 2N resolved
optical degrees of freedom: two spatial mode sets, or equivalent color/
polarization/time modes WITH the necessary color-resolved detection. It
is not an ordinary free N-mode binary output.

Keep the full outcome of every source cycle. Accept an oriented balanced
subset S only for the exact counts

    red_i=1[i in S], blue_i=1[i not in S], |S|=k.

Thus there is exactly one photon per graph vertex across the two colors,
k red and k blue photons, and 2k photons in total. Vacua, other photon
numbers, collisions, double-color vertices and missing vertices are paid
failures. S and its complement are distinct color-count outcomes. For odd
k this acceptance has probability zero because each undisplaced Gaussian
color has even parity; the stated even-k restriction is indispensable.

The source is graph-dependent and contains no C*, known partition or optimal
mask. This does not make its preparation, matrix factorization, squeezing,
interferometer compilation, number/color resolution or failed cycles free.
The symbol lambda controls source strength, not a fixed photon number.

## 2. Exact normalized source and raw hafnian law

For one color define

    |psi_Z>=det(I-Z^2)^(1/4)
              *exp[(1/2)*sum_ij Z_ij a_i^dagger a_j^dagger]|0>.

The determinant is positive because Z is real symmetric with ||Z||<1.
For completeness, orthogonally diagonalize Z and transform the optical
modes passively. In one resulting mode with real pair parameter z,

    exp(z*(a^dagger)^2/2)|0>
       =sum_{m>=0} z^m*sqrt((2m)!)/(2^m*m!)*|2m>.

Its squared norm is sum_m binom(2m,m)*(z^2/4)^m=(1-z^2)^(-1/2), the
binomial series. Multiplication over orthogonal modes proves the stated
normalization. Negative eigenvalues only change pair phases, not this norm.

Expanding the pair exponential for a CF occupied set T of even cardinality
sums one product per perfect matching, giving amplitude

    det(I-Z^2)^(1/4)*haf(Z_T).

Every accepted occupation is zero/one, so all Fock factorials are one.
Independence of the two colors multiplies their probabilities. Since haf
on k vertices has degree k/2, the UNCONDITIONAL probability of a particular
accepted oriented S is exactly

    q_epsilon(S)=det(I-lambda^2*W^2)*lambda^(2k)
                    *haf(W_S)^2*haf(W_Sc)^2.

There is one determinant, not its square root or square, after multiplying
two colors. Real nonnegative entries permit squares; a complex version
would require modulus squares. This probability has not been normalized
by the acceptance event. Define

    Pacc=sum_{|S|=k} q_epsilon(S),
    g_B(S)=q_epsilon(S)/Pacc

only when discussing the separate CONDITIONAL proposal law. The raw
normalization includes all other photon-number and collision outcomes.

## 3. Bounded primary-source check and translation

Checked on 25-Nov-2026; the two papers are the whole bounded source scope.
Versioned PDF text and official metadata were read, rather than abstracts
alone. No full paper text is copied into the repository; PDF bytes were
not retained, so no local PDF SHA256 is claimed.

- Hamilton, Kruse, Sansoni, Barkhofen, Silberhorn and Jex, *Gaussian Boson
  Sampling*, [arXiv:1612.01199v2](https://arxiv.org/pdf/1612.01199v2), revised
  20-Apr-2017, PRL119,170501. Page3, Eqs.(10)--(11), gives the pure squeezed-
  state matrix B=T diag(tanh r_j) T^T and CF probability proportional to
  |haf(B_T)|^2 with the Gaussian normalization. Here B is Z; the determinant
  conversion and two-color multiplication were derived in section2.
  Implication: verified; overlap label: known after translation of notation.
- Arrazola and Bromley, *Using Gaussian Boson Sampling to Find Dense
  Subgraphs*, [arXiv:1803.10730v2](https://arxiv.org/pdf/1803.10730v2), revised
  30-Jul-2018, PRL121,030503. Pages1--3, Eqs.(1)--(2) and graph-encoding
  discussion, apply hafnian-weighted CF sampling to graph-density heuristics.
  This is an adjacent known graph-sampling mechanism. It does not establish
  this complementary balanced two-color route, its preparation, or a matched
  total-cost advantage against the controls required here.
  Implication for our positive objective: unverified; overlap: partial or
  adjacent result only.

A two-paper check is not a novelty search. The squeezed/CF hafnian law and
dense-subgraph motivation are already known; no originality claim follows
for the complementary variant or the internal expansions below. Existing
project text contained no match for these two stable identifiers in the
reviewed research/theory/reports paths; that absence has no novelty meaning.

## 4. Correct weak min-cut response, at fixed graph size

Let m_k=(k-1)!!, with haf(empty)=1. For a selected k-vertex set T write
E_T=sum_{i<j in T} A_ij and W_A=sum_{i<j}A_ij. Each edge occurs in exactly
(k-3)!! perfect matchings of the complete k-vertex graph, with the empty
case supplying the k=2 convention. Therefore

    haf(W_T)|_(epsilon=0)=m_k,
    d/d epsilon log haf(W_T)|_0=E_T/(k-1).

The conditional unnormalized B weight is f_B(S)=haf(W_S)^2*haf(W_Sc)^2.
Its first log derivative is

    2*(E_S+E_Sc)/(k-1)=2*(W_A-C_A(S))/(k-1).

At epsilon=0 the conditional law g0 is uniform on all balanced oriented
subsets. Normalizing gives, for this FIXED finite A,k,

    g_B(S)=g0(S)*[1-2*epsilon*(C_A(S)-E0 C_A)/(k-1)]
              +O_(A,k)(epsilon^2),
    E_B C_A=E0 C_A-2*epsilon*Var0(C_A)/(k-1)+O_(A,k)(epsilon^2).

This has the desired min-cut sign when the uniform cut variance is positive.
It is a conditional-law derivative, not an unconditional hardware success
rate, uniform-in-size estimate, optimization guarantee or quantum advantage.
The common lambda/determinant factors cancel from this conditional law,
even if source strength is adjusted with epsilon to remain physical.

## 5. Incoherent matching control and an explicit cheap feasible control

Define a combinatorial incoherent control by

    f_M(S)=haf((W elementwise-squared)_S)
              *haf((W elementwise-squared)_Sc),
    g_M(S)=f_M(S)/sum_T f_M(T).

It sums probabilities of matching alternatives rather than their coherent
amplitudes. This is a CLASSICAL mixture/combinatorial control, not an
automatically established physical fully-distinguishable Gaussian source.
Because W_ij^2=1+2*epsilon*A_ij+O(epsilon^2), its conditional log-weight
has EXACTLY the same first derivative as f_B, and hence the same first-order
cut drift. No leading interference benefit survives this control.

Exact arbitrary-weight sampling from these hafnian weights is NOT declared
free. One latent construction samples a weighted perfect matching of the
full N-vertex graph with edge weights W_ij^2, then colors k/2 of its k edges
red uniformly. Its S marginal is proportional to f_M: the respecting
matchings factor into matchings on S and Sc. Generating that global weighted
matching is a real classical sampling problem, whose cost must be included.
Near complete uniform weights it can use rejection from uniform perfect
matchings, with every rejection paid; no general rapid-mixing or polynomial
exact-sampler theorem is assumed here.

There is an even cheaper explicit feasible sampler matching the entire
FIRST-order B law without computing or sampling hafnians. Under g0, an
edge is uncut with probability u=(k-1)/(2k-1). Let

    a=2*epsilon*W_A/(2k-1),  0<=a<=1.

With probability 1-a draw g0. Otherwise choose an edge with probabilities
A_ij/W_A and draw g0 conditioned on keeping its endpoints on the SAME side.
This conditional draw is direct: equally choose both endpoints selected or
both excluded, then choose the remaining balanced subset uniformly. The
two populations have equal cardinality because N=2k. If W_A=0 use g0.
The resulting EXACT nonnegative classical law is

    g_class(S)=g0(S)*[1-2*epsilon*(C_A(S)-E0 C_A)/(k-1)].

Graph reading, edge alias setup, random choices, feasible subset generation
and subsequent cut scores are paid polynomial operations. It uses no C*,
mask or optimal state, has no optical postselection, and establishes a real
weak-response falsifier. Outside a<=1 this particular linear mixture is
not asserted to be a probability law.

## 6. First relative coherence term and its polynomial feature

For k>=4, let M be a UNIFORM perfect matching on a k-vertex selected set T.
Set X_T=sum_{e in M} A_e, Q_T=sum_{i<j in T} A_ij^2 and
V_T=Var_M(X_T).
Expanding the product of its edge amplitudes gives

    haf(W_T)/m_k=E_M product_{e in M}(1+epsilon*A_e).

Writing the second product coefficient as (X_T^2-sum_{e in M}A_e^2)/2
and expanding the logarithm proves

    log haf(W_T)^2
      =2 log m_k+2*epsilon*E_M X_T
           +epsilon^2*(V_T-Q_T/(k-1))+O(epsilon^3),
    log haf((W elementwise-squared)_T)
      =log m_k+2*epsilon*E_M X_T
           +epsilon^2*(2*V_T-Q_T/(k-1))+O(epsilon^3).

Thus, after conditional normalization,

    log g_B(S)-log g_M(S)
      =-epsilon^2*[(V_S+V_Sc)-E0(V_S+V_Sc)]+O_(A,k)(epsilon^3),
    E_{g_B} C_A-E_{g_M} C_A
      =-epsilon^2*Cov0(C_A,V_S+V_Sc)+O_(A,k)(epsilon^3).

There is no guaranteed favorable sign for that covariance. The first
coherent distinction is a matching-weight variance bias, not a new first-
order cost tilt. For k=2 there is a unique matching in each side, V_T=0,
and the B and combinatorial matching conditional laws coincide at ALL
strengths; it is not an interference benchmark.

The variance is computable in O(k^2) from the selected adjacency matrix.
Let d_i^T=sum_{j in T}A_ij. A matching contains a particular edge with
probability 1/(k-1), and two disjoint edges with probability
1/[(k-1)(k-3)]. Different overlapping edges cannot coexist. Therefore

    V_T=Q_T/(k-1)
          +(E_T^2+Q_T-sum_i(d_i^T)^2)/[(k-1)(k-3)]
          -E_T^2/(k-1)^2.

The numerator uses twice the sum over unordered disjoint edge pairs, derived
by subtracting incident-edge pairs from all pairs. This checks the factors
without an independent-photon assumption.

For example the positive classical surrogate weight

    exp[-2*epsilon*C_A(S)/(k-1)
         +epsilon^2*(V_S+V_Sc-(Q_S+Q_Sc)/(k-1))]

matches log f_B up to its graph-only constant through second order. Evaluating
this feature is cheap; exact sampling, mixing and score budgets remain paid
and are NOT proved free. Finite-strength higher-order matching correlations
and their optimization value remain unestablished. No finite graph or seed
has been selected to force a favorable covariance.

## 7. Raw acceptance at the complete-background point

At epsilon=0, W=J_N-I_N has eigenvalues N-1 once and -1 with multiplicity
N-1. Hence physical lambda satisfies 0<lambda<1/(2k-1), and exactly

    Pacc0=binom(2k,k)*[(k-1)!!]^4*lambda^(2k)
            *(1-lambda^2*(2k-1)^2)*(1-lambda^2)^(2k-1).

This is the probability of ALL balanced accepted colored outcomes, not a
selected optimum. Every accepted S is conditionally uniform at this point.

An elementary uniform upper bound already gives an exponential source-cycle
penalty. From

    n log n-n+1<=log(n!)<=n log n-n+1+log n

and m_k=k!/[2^(k/2)*(k/2)!], one obtains
m_k<=k*(k/e)^(k/2). Drop the determinant factors, use
binom(2k,k)<=4^k and lambda<(2k-1)^(-1), giving

    Pacc0<=k^4*exp(-2k)*(2k/(2k-1))^(2k)
           <=exp(4/3)*k^4*exp(-2k)
           <=e^2*k^4*exp(-2k).

The middle inequality uses log(1+x)<=x and 2k/(2k-1)<=4/3 for k>=2.
Bounds are capped by one when needed at small sizes. This is not a TV
statement and does not extrapolate to all epsilon or other source families.
It rules out treating complete-background postselection as a free
optimization gain; a direct classical uniform feasible draw reproduces
its accepted law without these failures.

## 8. Photon costs: vacuum and all number sectors are included

For one eigenmode of Z with parameter z, differentiating the normalization
series gives mean photons z^2/(1-z^2). Passive mode transformations preserve
total photon number. The mean for BOTH independent colors is therefore

    nbar=2*Tr[lambda^2*W^2*(I-lambda^2*W^2)^(-1)].

This includes vacuum and every multi-pair sector. It is not 2k photons per
source cycle: only accepted cycles have that exact count. Source/operation
time, squeezing and pump costs are additional resources, not certified by
this mean signal-photon count. Per-attempt useful yield and per-generated-
photon useful yield are respectively Pgood and Pgood/nbar.

At epsilon=0, positivity of the spectral factors gives

    nbar>=2*lambda^2*N*(N-1), N=2k.

Combining this with the previous derivation, but keeping the two powers
of lambda needed for the denominator, proves uniformly over physical lambda

    Pacc0/nbar
       <=[(N-1)/(2N)]*binom(N,k)*m_k^4/(N-1)^N
       <=(1/2)*e^2*k^4*exp(-2k).

Thus choosing an arbitrarily weak, mostly-vacuum source does not evade the
complete-background penalty by changing the denominator to photon count.
For iid source cycles continued until acceptance, expected cycles are
1/Pacc and expected generated photons are nbar/Pacc; counting only the
2k photons of successful cycles would omit failures. This photon formula
does not prove an exponential penalty for every finite-epsilon encoding.

## 9. Preparation bridge and precise rank obstruction

This model cannot be assumed available from the existing CF single-photon
passive setup. A full nonzero pure Gaussian state has unbounded even photon-
number support, as section2's one-mode expansion demonstrates. A finite-m
Fock input, vacuum ancillas and passive optics conserve total photon number;
counting herald modes leaves at most m photons. No such finite resource
can EXACTLY produce the full Gaussian state, even after mixing herald
branches. Squeezing or another non-number-conserving resource would be real.
No claim about native Lucy squeezing capability has been checked or assumed.

There is a separate necessary bound even for a TWO-photon-sector substitute.
Represent a pure pair by its symmetric coefficient matrix M in
(1/2)*sum_ij M_ij a_i^dagger a_j^dagger|0>. Passive optics transform it by
M to U*M*U^T and preserve its rank. Two distinct CF input photons give
M=e_a e_b^T+e_b e_a^T of rank two. A generic full-rank W on N>2 vertices
cannot be prepared from those two photons by passive optics and vacuum
alone. W is full rank at epsilon=0, with determinant
(N-1)*(-1)^(N-1), and remains full rank in a fixed-size neighborhood;
full rank is generic rather than guaranteed at every parameter.

More generally inject m distinct CF photons and herald m-2 detected photons,
leaving a pure pair. Each input creation operator becomes a linear form
with retained signal coefficient vector v_a and detected-mode terms. The
heralded degree-two signal polynomial is a sum over choices of two retained
input factors:

    sum_{a<b} c_ab*(v_a dot s^dagger)*(v_b dot s^dagger).

Its symmetric pair matrix has range inside span{v_1,...,v_m}, so rank at
most m. An exact rank-N pair matrix therefore requires m>=N in THIS
preparation class. This is necessary, not sufficient; no herald success
probability, efficient protocol or full Gaussian preparation follows.
Passive branch-dependent feedforward preserves each branch's pair rank;
forgetting branches normally gives a mixture, not the required pure pair.

A fixed-N hafnian/pair-polynomial source is a possible DIFFERENT model.
Its normalization, acceptance rate, preparation and herald budget must be
derived for that source. One cannot substitute it into this note and keep
the Gaussian determinant law or use the two-photon rank argument as a
universal lower bound for every many-photon encoding. Approximate or
truncated preparations similarly need explicit error and success budgets.

## 10. Scientific disposition and the first unresolved implication

The changed source supplies a genuine conditional min-cut bias, unlike the
wrong-direction full-input weak hop of P54. But the first-order signal is
classically reproduced, the first relative coherence term is a polynomial
matching-variance feature with no guaranteed beneficial sign, and the
Gaussian complete-background event has an exponential paid rejection cost
under both attempt and signal-photon denominators. Its new source/readout
requirements have not been connected to the actual platform.

REJECT: a first-order interference advantage, a free Gaussian/pair source,
a two-CF-photon passive implementation of generic W, and interpreting accepted
colored samples without their failure/preparation costs. KEEP: the exact
law, finite-order controls and scoped preparation obstructions. FOLLOW-UP:
finite-strength correlations beyond cheap controls, or a materially different
fixed-number/non-Gaussian source, remain OPEN with their source-cost and
strong-baseline obligations. They are not ruled out by this checkpoint.

The next unresolved implication is whether any such finite-strength source
can deliver useful conditional structure that survives independently optimized
physical distinguishability controls, strong feasible search and its OWN
raw preparation/counting budget. No experiment, optimizer or QPU run is
justified by the weak derivative alone. The user's requested positive,
independently replicated optimization result remains open.
