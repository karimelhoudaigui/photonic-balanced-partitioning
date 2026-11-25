# Uniform loss reveals factorial moments by detected sector

2026-11-25. Fresh analytic derivation from the P51 card, with no author proof,
code/import, numerical run, graph, calibration or hardware call. **The lemma
below is proved for fixed-total full occupation laws.** Its consequences are
distribution identities/bounds, not matched-cost or optimizer advantages.
No novelty is claimed; independent proof review remains necessary.

## Exact law and theorem

Let p,q be probability laws on nonnegative m-mode occupations n with the
SAME fixed total |n|=r. Let b>=0 be an integer. Assume all joint factorial
moments of total degree<=b match. Write

    M_p(t)=E_p[prod_i (n_i)_(t_i)],   t!=prod_i t_i!.

Apply independent uniform thinning: each photon is retained with probability
eta, independent of every other photon and mode. For0<eta<1 the exact full
detected-occupation law is

    p_eta(t)=eta^|t| (1-eta)^(r-|t|) M_p(t)/t!,    |t|<=r.          (1)

Proof: condition on n and multiply binomial probabilities
prod_i binom(n_i,t_i) eta^t_i (1-eta)^(n_i-t_i). Fixed |n|=r puts the loss
power OUTSIDE the expectation. This is the entire output event, with every
unlisted detected mode empty; it is not an inclusive click moment or a
success-conditioned probability. Collisions are retained throughout.

Equation(1) immediately gives

    p_eta(t)=q_eta(t) for |t|<=b,
    TV(p_eta,q_eta)<=Pr[Binomial(r,eta)>b].                        (2)

For the second statement, both laws have the SAME sector mass
w_s=binom(r,s)eta^s(1-eta)^(r-s). On the unmatched sectors, half the sum of
absolute differences is at most half their combined mass, hence the tail
in(2), with NO extra factor2.

## Common conditional shape and an exact TV decomposition

For every0<=s<=r define on |t|=s

    p^[s](t)=M_p(t)/(t! binom(r,s)).                              (3)

It is normalized because
sum_(|t|=s) prod_i binom(n_i,t_i)=binom(r,s). Thus the conditional shape
given exactly s detections is independent of eta whenever that sector has
positive mass. Matching moments through b gives p^[s]=q^[s] for s<=b.
The sectors have disjoint support, so exactly

    TV(p_eta,q_eta)=sum_(s=0)^r w_s TV(p^[s],q^[s]).                (4)

At eta0 both outputs are vacuum and TV=0. At eta1, p_eta=p and q_eta=q.
Zero-mass sectors are not observed conditional distributions there, though
(3) defines their algebraic continuation. There is no need to evaluate an
ambiguous0^0. If b>=r then already p=q and both sides of(2) are0. Vacuum
r0 likewise gives a single identical law. For b<r, the eta1 tail bound is
the valid but generally trivial TV<=1.

If the first DIFFERENT factorial moment degree is h, finiteness also gives

    TV(p_eta,q_eta)
      = eta^h/2 * sum_(|t|=h) |M_p(t)-M_q(t)|/t! + O(eta^(h+1))    (5)

as eta tends to0 with r fixed. The leading coefficient is positive. This
does not assert a uniform-in-r approximation or an eta^r factor for h<r.

## When exact eta^r scaling holds after a decoder

If all degrees<=r-1 match, every lower sector cancels and the signed law is

    p_eta-q_eta = eta^r (p-q),                                   (6)

where the right side is embedded in the full r-detection sector. In
particular TV(p_eta,q_eta)=eta^r TV(p,q).

Let D be ANY fixed Markov decoder of the entire occupation, including common
randomized tie-breaking and a failure output if wanted. It must be the SAME
map for p,q and across eta in the following equality. Linearity gives

    D(p_eta)-D(q_eta)=eta^r (D(p)-D(q)),
    TV(D(p_eta),D(q_eta))=eta^r TV(D(p),D(q)).                     (7)

For a decoder D_eta that depends on eta but is common to the two sources,
the valid equality instead has D_eta on BOTH sides of(7). It does not
identify the decoded contrast with that at eta1. Contraction always gives
TV(D_eta(p_eta),D_eta(q_eta))<=eta^r TV(p,q) in case(6), and the tail bound
in the general case. Source-dependent or separately retuned decoders are
not the same channel and need a new comparison.

Conditioning and renormalizing on successful detections changes this law:
given all r photons survived, the shape is p or q, with no eta^r attenuation.
That event occurs with probability eta^r; rejected attempts and photons must
remain charged. A click-conditioned comparison cannot inherit(7) for free.

## H4 consequences, without a positive claim

For the two four-photon H4 phase laws, P51 low-order invariance gives b3=r-1.
Let t_phi=cos^2(phi). The earlier35-pattern table yields

    TV(p_phi,p_psi)=|t_phi-t_psi|/2,
    TV(p_(phi,eta),p_(psi,eta))=eta^4 |t_phi-t_psi|/2.

In particular the phi0/pi2 full-Fock contrast is eta^4/2. For the FIXED
uniform-tie top2 decoder of the prior checkpoint, its contrast to phi0 is
eta^4 sin^2(phi)/12. The lower sectors are exchangeable: their coefficient
polynomials through degree3 are symmetric power-sum expressions. They all
decode uniformly. Hence the complete lost top2 law has the exact classical
mixture

    (1-eta^4 sin^2(phi)/4) U6 + (eta^4 sin^2(phi)/4) UX.            (8)

Here the decoder uses positive iid jitter<1/2 to break equal counts uniformly,
without a finite bucket or fixed-priority beta0 rule. Centering by eta instead
of1 is only a common offset in this specific full-Hadamard family and changes
no exact ranking. It is not such a null for arbitrary nonuniform mu.

For full-input Hadamards with N>4, only b3 is proved here. Their general bound
is Pr[Binomial(N,eta)>=4], at most binom(N,4)eta^4, NOT eta^N. It can be close
to1 at fixed nonzero eta and large N. Comparing B with D also does not meet
the b3 premise: their second moments differ.

## Counterexamples to enlarged scopes

- Without a FIXED common total, matching low moments is insufficient even
  for vacuum probability. In one mode, p(n1)=1 and q(n0)=q(n2)=1/2 both
  have mean1. Yet q_eta(vac)-p_eta(vac)=eta^2/2.
- With NONUNIFORM efficiencies the lost-sector shape need not be universal.
  For p concentrated on(1,1) and q half(2,0)/half(0,2), both have total2 and
  the same first moments. Their vacuum probabilities differ by
  (eta1-eta2)^2/2. The mode-dependent loss power cannot leave the expectation.
- Herald selection, loss-dependent source/circuit selection, or an internal-
  state dependent loss channel is not the fixed uniform thinning model.
  Nor does an independent-marginal classical arm with random total meet it.

No photon/detection/programming cost is eliminated by these identities. They
describe attenuation of a distributional contrast on all attempts; they do
not certify an efficient optimizer, prohibit a global mechanism, calibrate
a device or justify a QPU call.
