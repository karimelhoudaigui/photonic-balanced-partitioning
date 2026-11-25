# P65: two prospective nonlinear routes, with their actual obstructions

25-Nov-2026. STATIC only; no hardware, graph, import or simulation.
These proofs concern specified mechanisms, not all photonic algorithms.
They are self-reviewed deductions, not independently certified or novel
results. No positive optimization claim follows.

## A. A diagonal cut filter has a classical latent-state simulation

Let Omega be the balanced subsets, and let a quantum source have arbitrary
density matrix rho with diagonal p(x). Assume p has an actually supplied
classical sampler whose construction/RNG costs are paid. Uniform feasible
subsets are an example; a paid common-incumbent distribution is another.
The proposed imaginary-time filter would be

    F_beta |x> = exp(-beta*C(x)/2)|x>.

It may be synthesized as edge filters or heralded measurement-induced
optical operations. The ideal successful final output law is

    Pr(x|success)=p(x)*exp(-beta*C(x))/Z,
    P_success=Z=E_p[exp(-beta*C(x))].

That conditional energy tilt is real, but does not require coherence.
Classical rejection samples x~p and accepts it with exp(-beta*C(x)),
with exactly the same success probability and output law. It costs one
actual graph score per proposal; no optimum/normalization constant is used.
Optical source/gate/heralding overhead cannot be left unbilled.

The stronger statement preserves failed records, too. Suppose every branch
of every operation, conditional on the preceding classical record h, has a
diagonal Kraus operator

    K_y(h)|x>=k_y(x,h)|x>, sum_y |k_y(x,h)|^2=1.

For the eventual occupation-basis measurement x, the full joint law is

    Pr(x,y1,...,ym)=p(x)*product_j |k_yj(x,h_j)|^2.

To prove this, multiply the diagonal Kraus operators on both sides of rho.
The final diagonal entry contains only rho_xx times the displayed factors;
every off-diagonal element disappears from that measurement. Classical
simulation samples one hidden x~p, then samples successive y using those
same branch probabilities, exposing only the permitted record to the
adaptive controller, and finally outputs x. This also reproduces stopping,
failure outputs and adaptive diagonal choices. It is not only a simulation
of the postselected successful law.

This closes the diagonal-filter-only route under its hypotheses. A genuine
escape requires noncommuting operations or a source law already outside the
supplied classical sampling interface. A general nonlinear gate network is
not assumed diagonal. Exact-real probability operations here are mathematical
interfaces; a practical sampler still pays finite precision and branch-cost
work. No universal matched-wall-clock result is asserted.

## B. Heralded coherent amplification needs a gate-cost window

A different route adds a true reversible cut-threshold oracle, feasible
mixing and coherent amplitude amplification. Given a supplied classical
threshold tau (for example a paid incumbent cut), let

    q=Pr_(uniform balanced x)[C(x)<=tau].

No C* is needed to define this threshold. An IDEAL amplification circuit
using L Grover iterations has marked probability

    p_ideal(L)=sin^2((2L+1)*arcsin(sqrt(q))).

This familiar oracle mechanism is not a new scientific contribution. In
photonic hardware the cut oracle requires logical interactions or operations
induced by measurement; passive mode phases do not implement arbitrary
quadratic logical cut phases for free. Count the source, all ancillas,
reversible arithmetic, herald detectors and failed preparations.

Assume, conditionally, each entire coherent iteration has independent
state-independent success probability h<1, with no recycling or error
correction. Full L-iteration success then has the upper bound

    p_raw(L)<=h^L*(2L+1)^2*q,                            (1)

using |sin(m*a)|<=m|sin(a)| for positive integer m. The sine inequality
follows by expanding (exp(i*m*a)-exp(-i*m*a)) as a telescoping geometric
sum of m terms of modulus |exp(i*a)-exp(-i*a)|.

If a coherent attempt costs at least L+1 common resource units, its raw
success rate per such unit is at most

    q*h^L*(2L+1)^2/(L+1) <=4*q*(L+1)*h^L
                         <=4*q/(1-h).                  (2)

The final inequality holds because (L+1)*h^L is at most
sum_(j=0..L)h^j<=1/(1-h). Thus with FIXED h<1, this model has no
quadratic asymptotic marked-fraction rate improvement as q tends to zero;
its bound is only a constant multiple of q. That is not a claim that every
finite factor is lost. h approaching one with system size, failure recovery,
correlated heralding and error correction are outside the stated model.

More generally m independent heralded gates of individual success at most
p_g require expected preparations at least p_g^(-m) for one fully successful
circuit under the same no-recycling model. This becomes a meaningful
classical-enumeration veto only after ACTUAL gate counts, success upper
bounds, source cost units and a measured competing classical algorithm are
supplied. Comparing an unsupported p_g^(-m) to 2^N would not certify a
practical no-go or a QPU advantage.

This route is deferred at the physical oracle/heralding specification, not
executed or globally impossible. No account/backend capacity or available
gate is assumed, no QPU access is requested, and no paper change is justified.
