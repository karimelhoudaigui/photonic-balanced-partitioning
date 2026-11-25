# P53d: a fixed cut-mean separation from every 4+4 control phase

25-Nov-2026. Exact finite, computer-assisted statement with independently
reconstructed control coefficients. This is a photonic mechanism witness,
NOT an optimization advantage, novelty clearance or a hardware result.

## Objects and theorem

Use exactly the original P52 eight-mode family

    U(phi) = [[W,D(phi)W],[W,-D(phi)W]] / sqrt(2),
    D(phi)=diag(1,exp(i phi),exp(2i phi),exp(3i phi)),

with W one-half times rows(1,1,1,1),(1,1,-1,-1),(1,-1,1,-1),
(1,-1,-1,1). Inject one photon into each input, retain every complete ideal
number-resolving outcome, and select four highest-count modes with uniform
ties. For a decoded subset S let X_ij(S) indicate crossing edge{i,j} and
w(S)=(X_04(S)-X_15(S))/2.

B denotes all eight identical photons at the FIXED phase pi/3. For each
of the35 unordered complementary four-input groups G,Gc, let B4(G,phi)
denote four identical photons in each group, with the two groups mutually
distinguishable, at an arbitrary common real phase phi. Then

    E_B[w] = -767/327680,
    E_B4(G,phi)[w] - E_B[w] >= 57/32768 > 0

for EVERY G and EVERY phi. The uniform law on all70 balanced subsets
also obeys that lower bound. These are conservative certified bounds;
the minimizing phase or the attained smallest gap is not asserted.

Adding1/2 to every edge weight gives the SAME elementary posthoc graph
used in P53b: a_04=1,a_15=0, all other edges1/2, total weight14. Every
balanced cut has16 crossing edges, so its added cost is8. Dividing by14
gives the normalized mean-cut lower bound57/458752. No new graph was
selected in extending the phase-control family.

## Finite exact certificate and independent reconstruction

For each four-input group and330 occupations, the creation coefficient
C_n(z) is an integer polynomial of degree at most12; z=exp(i phi).
Its probability is prod(n_i!)*C_n(z)C_n(z^-1)/8^4. Two species convolve
probabilities; there is NO extra final-occupation factorial.

For each of6435 final occupations, the exact conditional w has numerator
s(n) over840. Consequently every control mean has an exact cosine series
a_0+sum_(k=1)^12 a_k cos(k phi). The complete finite certificate checks

    a_0 - sum_(k=1)^12 |a_k| - E_B[w] >= 57/32768

for all35 groupings, and the uniform gap separately. Since |cos|<=1,
these inequalities prove the continuum assertion. No phase grid, float
LP, guessed optimum, Bernstein control or numerical tolerance is used.

Primary certificate44df171e... was independently reconstructed in
research/P53d_independent_check.py, source SHA256
047ff5d95c947d159eca551e298fae07fb3db2acaf6f5c9807fca629d3bde5d2.
That code expands24 permanent monomials per four-photon occupation instead
of using the primary creation recurrence; enumerates all70 feasible subsets
instead of its tie formula; and uses two separately bounded integer einsums
instead of its matrix products. All23,100 coefficients,300,300 Laurent
entries,108,900 decoder-matrix entries,35 spectra and105 old anchors agree.
Its unique replay7611d76/root967bb07 confirms both bounds exactly.
The B value uses the pinned previously reviewed P53 source/checkpoints.
Detailed commands, integer overflow bounds, hashes, qualification13PASS and
independence limits: research/P53d_independent_check_receipt.md.

## Scientific limits

The check is posthoc and nonblind within the same team. It separates one
fixed linear mean from4+4 controls in this architecture; it does not imply
separation from7+1,6+2,5+3, arbitrary internal states or all classical models.
The separately frozen P58 SAME-phase bipartition calculation addresses a
different finite question and is not part of this continuum proof.
No full-law, best-of-budget, graph-population, cost or optimizer improvement
follows. The posthoc graph is small and classically trivial. In particular,
this theorem does not satisfy the user's positive optimizer target and
does not authorize manuscript changes, held-out opening or QPU execution.
