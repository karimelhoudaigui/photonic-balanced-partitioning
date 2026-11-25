# P49 raw quadratic objective: independent analytic check

2026-11-25. Target: the coordinator's auxiliary claim about
S(R)=sum_a q_a^T L q_a and the B/D means of n^T L n. Primary verdict:
**proved as written** for the FULL, unconditional count law under the
hypotheses below. The pointwise PSD comparison in section4 also holds.
Neither statement concerns P49's already frozen feasible-cut/PIT objective.
No card, code, raw or experiment was changed. No numerical work was run.

## 1. Conventions and scope

Let E be an N-by-K isometry, R a K-by-K unitary and V=ER. Inject one photon
in each of K distinct inputs, vacuum in the others; B denotes perfectly
indistinguishable photons and D fully distinguishable photons with labels
forgotten. Retain every output occupation, including collisions. Define

    Q_ia=q_ia=|V_ia|^2, q_a=column a of Q,
    P=VV*=EE*, mu_i=P_ii=sum_a q_ia,
    S(R)=sum_a q_a^T L q_a=Tr(LQQ^T).

Here L is the FIXED real symmetric graph Laplacian; nonnegative graph
weights give L>=0. The symbol |P|^2 means ENTRYWISE absolute square,
not P squared as a matrix. Covariances and Q are real. Transpose T is
therefore appropriate for q and mu; star is conjugate transpose for V/P.
No conditioning on CF/success, decoder, internal species or loss is included.

## 2. Fresh derivation of moments

Distinct CF input occupations give E[n_i]=mu_i. Normal-order expansion of
n_i n_j yields, with the Kronecker delta term also covering i=j,

    E_B[n_i n_j]
      =mu_i mu_j+delta_ij mu_i+|P_ij|^2-2sum_a q_ia q_ja,
    E_D[n_i n_j]
      =mu_i mu_j+delta_ij mu_i-sum_a q_ia q_ja.          (1)

For B, the two contractions of DISTINCT source labels contribute the
direct product and exchange product. The a=b term must be removed from
BOTH contractions because each input contains only one photon, producing
the factor2. D has only independent categorical source particles and
removes that term once. Thus

    Cov_B=diag(mu)+|P|^2-2QQ^T,
    Cov_D=diag(mu)-QQ^T.                               (2)

As a normalization check, both covariances annihilate the all-ones vector:
Q^T 1=1_K and (|P|^2 1)_i=(P^2)_ii=P_ii=mu_i.
Total detected photon number is exactly K, as required. There is no K!
renormalization of these already normalized CF states.

For real symmetric L,

    E[n^T L n]=mu^T L mu+Tr(L Cov).

In components Tr(L|P|^2)=sum_ij L_ij |P_ji|^2
=sum_ij L_ij |P_ij|^2 because P is Hermitian. No complex transpose or
extra factor2 is missing. Substitution gives exactly

    J_B(R)=mu^T L mu+Tr(L diag(mu))+Tr(L|P|^2)-2S(R),
    J_D(R)=mu^T L mu+Tr(L diag(mu))-S(R).               (3)

For an undirected graph, n^T L n=sum_(i<j) w_ij(n_i-n_j)^2. This
single-edge convention agrees with (3); a double sum would require1/2.

## 3. Consequence for raw-objective training

P and mu are fixed by the subspace E throughout the spectral R family.
Therefore every term in (3) except S(R) is a fixed constant. For ANY
nonempty allowed R set, including a finite nonconvex grid,

    argmin_R J_B(R)=argmin_R J_D(R)=argmax_R S(R),       (4)

whenever these extrema are attained. The frozen finite grid attains them;
over the entire unitary group compactness and continuity also suffice.
Ties agree exactly. No convexity, local-gradient or asymptotic argument
is used. If L=0 or K=0/1, the appropriate constant/tied cases are included.
The statement concerns only the fixed-E spectral family, not comparison
with a Fourier frame having a different P.

## 4. Pointwise positive-semidefinite comparison

Define z_ab=v_a elementwise-multiplied by conj(v_b), with v_a a column
of V. Direct entrywise expansion gives

    |P|^2=sum_(a,b) z_ab z_ab*,
    QQ^T=sum_a z_aa z_aa*,
    C_R:=|P|^2-QQ^T=sum_(a!=b) z_ab z_ab* >=0.          (5)

Consequently for L>=0,

    J_B(R)-J_D(R)=Tr(L C_R)
      =sum_(a!=b) z_ab* L z_ab >=0                     (6)

at EACH R. In graph-edge form this is

    2sum_(i<j) w_ij sum_(a<b)
      |V_ia conj(V_ib)-V_ja conj(V_jb)|^2 >=0.          (7)

This also shows where the ordered/unordered source-pair factor2 belongs.
The difference is zero for K1. As a hand check, K=N=2, a balanced real
beam splitter and one unit-weight graph edge give B energy4 and D energy2.
Equations (5)-(7) do not require a numerical eigenvalue check. Without
L>=0, the identities and argmin relation (3)/(4) remain valid, but the
nonnegative comparison (6) would not follow.

## 5. Boundary of the result

The output used by P49 is a balanced BINARY partition AFTER a model-specific
marginal PIT, top-q seeding and greedy completion. Its cut can be written
x^T L x in that binary x, but x is a nonlinear, randomized function of the
raw occupations. Its mean is not (3). No ordering of decoded feasible
means, improving mass, tails, best-of shots, adaptive search or resource
efficiency follows from (4) or (6). Internal-species models are not included
in the B/D argmin identity either.

Thus the raw quadratic proxy cannot be advertised as a B-specific benefit
of R or substituted for the already frozen training loss. Conversely this
note does NOT refute the P49 feasible-decoder hypothesis. That remains an
empirical and theoretical obligation against independently trained controls
and the actual total-cost classical envelope. This is a direct covariance/
PSD calculation, not a novelty or general quantum-impossibility claim.

Provenance: algebra was reconstructed and sent by message before this note;
existing P49 source-mixing review f898028e3b9f38d4e520ddde100a34285e01369d
was consulted only for conventions. Local checks were read-only status/log
and text searches, followed by whitespace/hash checks at commit. No Python,
matrix evaluation, simulation, test, DEV graph or QPU was used. The reviewer
is a prior author of related physics notes, so this is a fresh derivation
of the auxiliary identity, not third-party revalidation of those notes.
