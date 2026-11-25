# P71: robust transport bounds from approximate optical cross rank

25-Nov-2026. STATIC derivation of the coordinator's proposed extension.
No imports, numerical computation, matrix generation, native/backend call,
random draw, test, calibration, new data, QPU operation or manuscript edit.
The separate sole numerical worker is not accessed by this review.

**Verdict: proved as written below.** Every unitary is close to a unitary
of truncated cross rank with an explicit operator-norm error. Its complete
K-photon law is correspondingly close in TOTAL variation, giving an additive
robust version of P69. Exponential trapping requires the additive error to
be sufficiently small too; algebraic full rank or a merely small tail does
not by itself settle optimization performance. No positive result, measured
hardware error bound or novelty claim is made.

Exact dependency: the accepted P69 source file
`research/P69_low_rank_transport_obstruction.md`, SHA256
`37e59633734c16277ed2649c4761fa84a86a8006b164fd4263963e37d7759de4`.
This includes the corrected cost-landscape scope: partial states outside the
four bad states and two good targets are uphill; neutral bad states exist.
The following cosine/sine construction is proved internally, including
zero/one singular values, rather than relying on an unauthenticated external
CS-decomposition citation.

## 1. Exact statement and endpoints

Let two logical blocks CA,CB have d=2L modes each, L>=2. The normalized
source has L distinct occupied vertices per block, K=2L photons in total.
The two target events are the full-CF occupation of all CA, or all CB, as
in P69. Let the entire ideal net one-particle unitary, in these SAME input
and output blocks, be

    U=[A C; D B].

Write its sorted cross-block singular values as

    1>=s1>=...>=sd>=0,   s_(d+1)=0.

The singular values of C and D are the same by the construction below.
For an integer 0<=r<=d, there exists a unitary V with optical cross rank
at most r and

    ||U-V||op <= delta(s_(r+1)) <= sqrt(2)*s_(r+1),
    delta(s)=sqrt(2-2sqrt(1-s^2)),  0<=s<=1.

Use the P69 bound p_Lr for 1<=r<=d, and define p_L0=0. Then

    P_U(either good raw target)
       <=min(1,p_Lr+K*delta(s_(r+1)))
       <=min(1,p_Lr+sqrt(2)*K*s_(r+1)).

For r=0, V is block-local and p_L0=0. For r=d, choose V=U: the tail and
comparison error are zero, though p_Ld=1 gives no nontrivial target bound.
If U already has rank at most r, its next singular value is zero and V=U
can be chosen. These statements include every exact-rank endpoint.

All probabilities are raw full-count probabilities, with the specified
ideal CF source. No collision-free denominator, successful-shot selection,
free probabilistic preparation or alternative target decoder is included.
Input/output mode permutations that alter logical event assignments must
be included in the complete U and the same fixed block decomposition.

## 2. Complete cosine/sine form with endpoint construction

The block-column identity A-dagger A+D-dagger D=I implies that D-dagger D
is Hermitian with spectrum in [0,1]. Choose an orthonormal input-CA basis
v_i satisfying

    D^dagger D v_i=s_i^2 v_i,
    c_i=sqrt(1-s_i^2).

This is elementary finite Hermitian spectral decomposition: one can obtain
an eigenvector by maximizing the quadratic form on the unit sphere and
then induct on its invariant orthogonal complement. No choice of basis
inside a degenerate eigenspace changes the conclusions below.

For every c_i>0 define a_i=Av_i/c_i in output CA. These defined a_i are
orthonormal because <Av_i,Av_j>=c_i^2*1[i=j]. For indices c_i=0, complete
them to an arbitrary orthonormal basis of output CA. For every s_i>0 define
b_i=Dv_i/s_i in output CB, which are orthonormal for the same reason. For
indices s_i=0, complete them to an orthonormal basis of output CB. Thus

    U(v_i,0)=(c_i*a_i,s_i*b_i)

for ALL i, including c_i=0 and s_i=0: an undefined normalized vector was
completed only when its coefficient is zero. There is no division by zero.

Define full output vectors

    z_i=(-s_i*a_i,c_i*b_i).

They are orthonormal and orthogonal to every U(v_j,0). Since U is unitary,
their preimages U^dagger z_i lie entirely in input CB. Write these preimages
as (0,w_i); the w_i form an orthonormal input-CB basis. In these four local
input/output bases, U is therefore exactly

    R_s=[diag(c_i) -diag(s_i); diag(s_i) diag(c_i)].

In particular Cw_i=-s_i*a_i and Dv_i=s_i*b_i, proving equality of the two
cross-block singular-value lists. Sorting these pairs gives the required
s1>=...>=sd. The argument covers multiplicities and the endpoints:

- s_i=0,c_i=1: U(v_i,0)=(a_i,0), and z_i=(0,b_i);
- s_i=1,c_i=0: U(v_i,0)=(0,b_i), and z_i=(-a_i,0).

No nonunique normalization or unproved generic-nondegeneracy assumption is
used. The local basis changes remain block-diagonal unitary transformations.

## 3. Truncation is unitary, not a nonunitary matrix approximation

Keep (c_i,s_i) for i<=r. For i>r replace the pair by (1,0), and undo the
SAME block-local input/output basis changes to define V. The resulting
matrix is unitary, and its cross rank is the number of nonzero kept s_i,
which is at most r. Simply zeroing small entries or replacing C alone would
not generally preserve unitarity; that is not this construction.

After pairing the two local coordinates for each i, the difference U-V is
unitarily equivalent to a direct sum of zero blocks for i<=r and

    [c_i-1 -s_i; s_i c_i-1]

for i>r. The latter block's adjoint times itself is

    [(c_i-1)^2+s_i^2]*I=2*(1-c_i)*I.

Its operator norm is delta(s_i). This function is nondecreasing on [0,1],
so the whole norm is delta(s_(r+1)) when r<d. Equivalently it is
2*sin(arcsin(s_(r+1))/2). Since

    delta(s)^2=2*s^2/(1+sqrt(1-s^2))<=2*s^2,

the advertised sqrt(2) bound follows, including s=0 by continuity or direct
substitution. Keeping all pairs yields V=U and zero error when r=d.

The construction is existential and mathematical. No cost-free physical
compilation, accessible circuit, efficient controller or source calibration
is inferred from computing this comparison V.

## 4. Full K-photon trace distance and PNR total variation

For unitary U,V, tensor telescoping gives

    ||U^(tensor K)-V^(tensor K)||op<=K*||U-V||op.

Each of the K summands has one U-V factor and unitary factors elsewhere.
Restricting to the normalized symmetric K-particle subspace cannot increase
the norm, so

    ||Gamma_K(U)-Gamma_K(V)||op<=K*||U-V||op.

For a normalized source, let phi and chi be its two output state vectors.
Their Euclidean distance is at most this quantity. The trace distance of
the corresponding pure density operators is

    Dtrace=sqrt(1-|<phi,chi>|^2)<=||phi-chi||.

For completeness, the density-operator difference is supported on their
at-most-two-dimensional span, has trace zero and eigenvalues
plus/minus sqrt(1-|<phi,chi>|^2). The stated trace distance is HALF its
trace norm. The final inequality follows from

    2-2Re(z)-(1-|z|^2)=|1-z|^2>=0, z=<phi,chi>.

For complete PNR measurement, let E be the sum of the outcome projectors
where P_U exceeds P_V. The total variation is Tr(E*(rho_U-rho_V)), at most
the trace of the positive part of that trace-zero Hermitian difference,
namely Dtrace. Thus the complete normalized raw count laws obey

    TV(P_U_full, P_V_full)<=min(1,K*||U-V||op).

There is no additional factor 1/2 to attach to K: it has already entered
the definition of trace distance and classical total variation. Global
one-particle phases can make the norm bound loose while leaving every count
probability unchanged; this does not invalidate the upper bound or justify
halving its constant. The result is not claimed phase-optimal or tight.

Any COMMON classical decoding, repair or acceptance map contracts this TV
bound. But P69's good-event bound refers specifically to its two full-CF
block targets; a different decoder does not automatically inherit that
separate target probability estimate. Conditional CF laws would introduce
a new denominator and are outside this raw-law statement.

## 5. Robust target bound

The comparison V has cross rank at most r, so P69 bounds its probability
of the two good targets by p_Lr. The SAME event probabilities under U and
V differ by at most their complete-law total variation. Substitution of
section 3's distance proves the finite statement in section 1.

For clarity the exact comparison constant is

    p_L0=0,
    a_Lr=min(1,r(r+1)...(r+L-1)/L^L), r>=1,
    b_Lr=1 if r>=L,
    b_Lr=min(1,((L+r)/(2r))^r*((L+r)/(2L))^L) if 1<=r<L,
    p_Lr=min(1,2*a_Lr*b_Lr).

This is a uniform event upper bound; neither p_Lr nor the additive error is
an achieved success probability. The source's L/L block occupations and
full-CF target are indispensable hypotheses for invoking P69.

## 6. Adaptive histories and transcript comparison

Let U_j(h) be selected before shot j from the complete marked classical
history h, including its chosen internal random controls. Compare it with
a truncated V_j(h) constructed as above at the SAME history. Choose these
comparison kernels predictably, using a consistent measurable basis choice
inside degeneracies; finite spectral decomposition with coordinate-based
orthonormal completion provides one such selection. No comparison cost is
credited as free work of an implementable optimizer.

Suppose deterministic eta_j bound s_(r+1)(U_j(h)) at every matching history.
Set e_j=min(1,sqrt(2)*K*eta_j). With the same classical postprocessing rules,
the conditional next-step laws are within e_j in TV. Sequential maximal
coupling, maintaining equal histories until the first mismatch, yields

    TV(transcript_U,transcript_V)
       <=1-product_j(1-e_j)<=min(1,sum_j e_j).

This needs no independence of the physical results or controller actions.
If eta_j depends predictably on history, the safe mismatch sum instead uses
expectations of the conditional e_j on still-matching histories. In
particular a weaker valid version is

    TV(transcript_U,transcript_V)
       <=min(1,sum_j E_U[e_j(H_(j-1))]).

The indicator of no previous coupling mismatch can only reduce each term;
the U-history is a marginal of that coupling. A random history-specific
right-hand side is not an unconditional numerical bound without such an
expectation or deterministic almost-sure envelope.

For the P66 cost family a simpler direct first-exit proof suffices. Only
accepted optical CF proposals update the current source; collisions are
paid self-loops, with no external candidates or restarts. Until
an accepted exit from B, every current source has L distinct occupied
vertices per block. The accepted state is one of four bad states; the only
strictly better states are the two targets, and every other feasible state
OUTSIDE B and those targets is uphill by at least g>0. With deterministic
tail bounds eta_j and zero temperature,

    P_U(improvement by T)
       <=min(1,T*p_Lr+sqrt(2)*K*sum_{j=1}^T eta_j).

At finite deterministic beta_j add sum_j exp(-beta_j*g). For arbitrary
predictable eta_j,beta_j, one safe expression is

    min(1,T*p_Lr
      +sum_j E_U[1[no earlier accepted exit from B]
                  *(min(1,sqrt(2)*K*eta_j)+exp(-beta_j*g))]).

At zero temperature omit the thermal term. Earlier adaptive stopping is
represented by zero contributions after stopping. These are raw-attempt
bounds, not measured wall-time claims or statements about reaching the
specified bad source from a random initialization.

## 7. Effective-rank conclusions and their necessary error budget

For r=o(L), P69 gives p_Lr<=exp(-L*log(2e)+o(L)). Suppose a uniform tail
bound eta_L applies to T attempts. The robust zero-temperature bound is

    P_U(improvement by T)
       <=min(1,T*[p_Lr+sqrt(2)*K*eta_L]).

For a polynomial horizon T=L^a, a sufficient condition for its extra error
to vanish is K*T*eta_L->0. Since K=2L, eta_L=o(L^(-a-1)) suffices.
This may give a finite-polynomial-horizon obstruction, but it does NOT
supply an exponential expected-attempt lower bound.

To retain an exponential obstruction, the full additive hazard bound
p_Lr+sqrt(2)*K*eta_L must itself be exponentially small. For example an
exponentially small eta_L with an appropriate polynomial prefactor can
suffice; an unspecified 'small' tail or a merely inverse-polynomial error
cannot establish that conclusion. Finite-temperature accepted escapes
must be controlled too. No tail bound has been measured for an actual
P65 circuit, Lucy device or proposed hardware instance in this checkpoint.

The P69 symbolic exp(itH) example has full cross rank even when the
Hamiltonian cross block has rank one. The present result explains the
logical limitation of citing that algebraic full rank as an automatic
escape: small added singular channels may have too little total effect
over the available photon/attempt budget. Conversely, when the tail error
makes this inequality vacuous, the theorem does not refute usefulness.
A numerical rank threshold without an actual error certificate is not a
new physical mechanism or a rigorous effective-rank conclusion.

## 8. Audit boundary

The complete CS construction, its zero/one endpoints, truncation norm,
K-photon lift, trace-distance factor, full-law measurement contraction and
predictable-history bookkeeping were proved internally. The P69 exact
source/target bound is the pinned mathematical dependency. No external
paper was assumed to establish the needed theorem; attribution/novelty is
unclaimed, and these elementary ingredients are not presented as new.

No source qualification, executable implementation or numerical experiment
was run or proposed here. A later application must independently justify
its singular-value/tail bound, preserve the raw failure accounting and
state the actual photon/attempt budget. This static theorem alone supplies
no hardware readiness, positive optimizer, held-out replication or paper
update. The user's positive research objective remains open.
