# P57 follow-up — one explicit wider routing graph (STATIC only)

This is a structural proposal, NOT a new run, model installation or accepted
positive. P57's full-law O(L) parity sampler remains decisive for its cycle.
The independent audit is theory/P57_adaptive_independent_review_5432b7d.md.

## Single modification

Replace the single routed cycle by TWO successive routed stages separated
by a third coupling matching. Let L=s^2 cells on a torus, s>=3,
Cx(x,y)=(x+1,y), Cy(x,y)=(x,y+1), and Qx=Zx Cx, Qy=Zy Cy. Use

    U_grid = B diag(I,Qy) B diag(I,Qx) B.

This is an explicit three-beamsplitter-matching network with horizontal and
vertical routes, source one upper photon per cell and lower vacuum. The
occupied-input transfers are

    upper = (I+Qx+Qy-Qy Qx)/(2*sqrt2),
    lower = (I+Qx-Qy+Qy Qx)/(2*sqrt2).

For s>=3 the four displacements are distinct, so their entry intensities
are1/8, independent of phase. D is phase blind with fixed angles. This
does not establish phase-independent lower count moments: the occupied
projector is not the identity, and short multi-source loops can respond.

After the horizontal route cell v has m_v=1-q_v+q_(v-ex). Let r_v in{0,1,2}
be its lower-rail occupation after the middle matching. Final cell totals
obey N_v=m_v-r_v+r_(v-ey). The all-cell-total1 equation is now a two-field
discrete divergence constraint, not the one-dimensional recurrence forcing
q constant. Its UNCONSTRAINED linear kernel has dimension L+1. Occupation
bounds/HOM amplitudes still need checking; kernel dimension alone does
not count nonzero coherent paths or prove hardness.

The natural tensor graph is a two-dimensional grid with a frontier of s
channels, not the two-state ring boundary. The P57 bond2/parity derivation
therefore does not carry over. Before claiming that every reordering or
another specialized sampler fails, one would need a rank/width argument
for the actual nonzero tensors. No such global complexity claim is made.

## One meaningful first mathematical discriminator

Use the SAME graph core and SAME all-attempt feasible decoder/greedy
acceptance for every control. The target is the accepted-gain function

    G_G(phi)=E_phi [C_inc-C_G(D(n))]_+.

Choose ONE registered elementary loop flux phi, not a favorable event.
The first obligation is a NONZERO exact Fourier coefficient of this full
function after all outcomes are included. The single-cycle audit supplies
the concrete anchor K_G=-10 and gain5/256 versus15/256 on its rejected
barrier example; it also shows why a tail probability or linear cut proxy
is insufficient. That example is not evidence for this wider network.

No graph-dependent phase rule is justified until a coefficient/sign is
derived WITHOUT precomputing an improving move for free. A calculation
that already scores a better move must credit it to the classical search.
Any later comparison must retime/reoptimize D and permutations, all allowed
species groupings, phase/sphere controls, width-aware tensor sampling and
a paid nonlocal feasible classical proposal. All photons, rejected outcomes,
graph extraction, delta/phase computation and decoder costs remain charged.

The modification escapes a specific proof premise, not all efficient
classical simulation. It changes the low-moment mechanism and must face
those new confounds. No new coefficient, graph, draw or code was computed;
independent analysis and a separate bounded contract are required first.
