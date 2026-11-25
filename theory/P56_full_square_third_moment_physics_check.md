# P56 auxiliary check: full-input moments through degree three depend on q

**Proved under the stated full-square, identical-photon assumptions.**
This is a fresh algebraic derivation, not a matrix evaluation or a review of
the forthcoming P56 implementation. No imports, code or numerical work.

Let U be an m-by-m unitary, with one identical photon in EVERY input mode.
Use the complete, unconditioned output Fock law. Set q_ia=|U_ia|^2 and
A=U*diag(t)U, with t formal real commuting variables. Then

    G(t)=E prod_i(1+t_i)^n_i=per(I+A).

The homogeneous component of degree h is the sum of the principal
h-by-h permanents of A. Coefficients are joint binomial moments:
[t^alpha]G=E prod_i(n_i)_alpha_i / prod_i alpha_i!.
Write T_j=Tr(A^j), d_a=A_aa, e_a=(A^2)_aa and D_j=sum_a d_a^j.

For degrees one and two, diagonal and transposition terms give

    P1=T1,
    P2=(T1^2+T2)/2-D2.

For degree three, the identity terms, one-transposition terms and oriented
three-cycle terms are respectively

    (T1^3-3T1 D2+2D3)/6,
    T1(T2-D2)/2 - sum_a d_a e_a + D3,
    T3/3 - sum_a d_a e_a + 2D3/3.

For the last line, Tr(A^3) contains the all-distinct cycle terms, three
copies of sum_a d_a(e_a-d_a^2), and D3. Each oriented three-cycle in a
principal permanent is counted three times by its possible starting point.
Thus there is no missing factorial or cycle multiplicity. Summing gives

    P3=T1^3/6+T1 T2/2+T3/3-T1 D2-2 sum_a d_a e_a+2D3.       (1)

The essential full-unitary identities are

    d_a=sum_i q_ia t_i,
    e_a=sum_i q_ia t_i^2,
    T_j=sum_i t_i^j.

Therefore P1,P2,P3, and ALL joint factorial moments of total order at most
three, are functions of q alone. Flatness is unnecessary. Repeated output
indices are included because this is a formal generating polynomial, not
only a distinct-mode correlation statement. At constant q, these complete
low moments are constant despite changes in higher interference phases.

The proof requires a square unitary and full identical-photon CF input.
It does not establish q-only dependence for a rectangular occupied frame,
bunched input, arbitrary internal Gram matrix, nonuniform contraction,
CF conditioning or threshold postselection. Uniform iid output loss merely
substitutes t->eta*t and preserves this conclusion for these unconditioned
detected moments; it does not preserve a conditioned fixed-N law.

For the proposed P56 fixed output beamsplitter, this lemma applies IF its
new entrywise q is actually theta independent. A fixed output unitary does
not in general preserve that property: the cross terms of mixed rows must
be checked on the particular colored matrix. No such matrix conclusion is
inferred from the word 'fixed' alone.

## What this says about a decoded graph-cut mean

All raw quadratic count means are fixed at fixed q. A graph cut after a
feasible nonlinear decoder is a different observable. With a fixed decoder
kernel, define c_G(n)=E[C_G(output)|n], including any private decoder coins.
The required signal is exactly

    sum_n c_G(n) [p_theta(n)-p_theta0(n)] != 0.               (2)

The low-moment identities annihilate every degree-at-most-three count
polynomial in (2). They do not annihilate an arbitrary count-to-partition
decoder. Degree four is the first possible place for a signal, but it is
incorrect to require a quartic signal in every architecture: P57's cycle
construction already has constant moments through order four and a varying
fifth-order law. Conversely, a varying fourth moment does not by itself
prove (2); compensation across Fock outcomes can cancel the decoded mean.
The concrete P56 obligation is a nonzero projection of the COMPLETE law
difference onto the fixed decoded observable, followed by the paid classical
countercontrols. No novelty, optimization advantage or hardware consequence
is asserted by (1) or (2).
