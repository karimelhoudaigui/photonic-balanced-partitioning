# P109 independent admissible-scale control review

2026-11-26. Non-author manual audit; no scientific execution.
Source: `research/P109_ADMISSIBLE_SCALE_DOMINATION.md`, all 113 lines read,
commit `b8bf28709b9065812eaf22ac6a20bb84f7573d9b`.
Source SHA256: `41b0cde5178af1b91e86823726307f7907bd7a377ec10afefc2f8842f9895353`.
Review parent: `cd95b1a3299db73633b03ccebed739cca128683c`.

**PASS under the explicit admissible-control, source and hold assumptions.**
No blocking algebraic gap found. This is a sufficient comparison against a
supplied stronger-transmission D control, not a no-go for arbitrary B circuits
or a quantum-advantage test with measured total costs. No novelty assessment.

## 1. Reconstructed probability inequality, including collisions

Take K>=1 distinct occupied input ports, one ideal photon each, vacuum in
all other inputs. B has identical internal states; D has mutually orthogonal
labels, with the same label-independent transfer. The K occupied columns
and a full-K signal occupation n define a repeated-row K-by-K matrix M.
Set n!=product_j n_j!. Direct Fock normalization and labeled assignment give

    p_B(n;T_B)=|per M|^2/n!,
    p_D(n;T_B)=per(|M|^2)/n!.

For D, each physical labeled assignment to occupation n appears n! times
in the repeated-row permanent, explaining this same divisor. No input
occupation factorial remains because the input is CF. Let z_sigma be the
K! permutation products. Cauchy gives |sum z_sigma|^2<=K! sum|z_sigma|^2;
dividing by n! proves p_B<=K! p_D for every full-K occupation.
Complex phases do not affect the inequality. Repeated rows do not invalidate
it. In fact a fully bunched output has identical permutation products and
saturates the factor K! whenever its probability is nonzero.

For supplied T_D=cT_B, each K-photon D intensity term acquires c^(2K).
Thus c^(2K)>=K! proves p_D(n;T_D)>=p_B(n;T_B), without a ratio or
survival normalization. If p_D=0 all permutation products vanish, so B=0;
zero channels, zero rows and destructive-interference zeros cause no gap.
For K=1, K!=1, c>=1 and the argument reduces to the one-photon intensity
comparison; at c=1 B and D coincide. Vacuum K=0 is outside the statement.

Normalization is not assumed from this inequality: it comes from the
separate hypothesis that BOTH transfers are physically admissible
contractions in the allowed control family. The sufficient norm margin
||T_B||<=1/c alone does not establish hardware reachability or compile costs.
There is no asserted componentwise order for any lower-photon sector.

## 2. Common decoder, failure atom and fixed repetitions

Let V be any declared subset of full-K signal occupations, and k(a|n) the
same randomized balanced decoder in both arms. Every outcome outside V
maps to a single fixed hold atom a0. For an event E excluding a0,

    P_D(E)-P_B(E)
      =sum_(n in V) k(E|n)[p_D(n)-p_B(n)] >=0.

This remains true if some valid outcomes also decode to a0. The total
non-hold mass dominates under D and the remaining aggregated hold mass is
therefore no greater; its individual loss/collision constituents need not
be ordered. Events containing the hold atom are not generally ordered in
the same direction. This is why identical invalid-event handling matters.

Set a0's cost to C0 and retain R=min(C0,C_a). For t<C0,
P_D(R<=t)>=P_B(R<=t); for t>=C0 both probabilities equal one. Equivalently
I=C0-R has P_D(I>=d)>=P_B(I>=d) for every d>0. Finite graph costs make
the expectations well-defined, giving E_D R<=E_B R. With T_attempt fresh
independent trials from the unchanged source/incumbent/circuit, the chance
of no candidate of cost <=t<C0 is (1-P(C_a<=t))^T_attempt. This proves the
same order for the best retained cost. Common independent decoder randomness
is included in those trials. Neither sampling nor decoding needs C*.

Changing incumbents, circuits, stopping rules, source statistics or correlated
trials requires another argument. Marginal one-attempt order alone does not
prove arbitrary adaptive-trajectory or correlated-best-of-T domination.

## 3. Preparation and external attenuation are hypotheses, not free controls

A common preparation-success probability s, with all preparation failures
held, multiplies each relevant event probability by s. A fixed common scalar
external transmission eta multiplies each full-K probability by eta^K.
Thus s eta^K preserves the inequality, including s=0 or eta=0. The ideal
known CF state and its COMMON success/failure law must be verified for the
comparison; different or unmodeled source branches are not covered.

The physical pair is sqrt(eta)T_B and sqrt(eta)(cT_B); the nominal cT_B
itself must be admissible. Removing external attenuation from only D is
not authorized by this theorem.
A small measured norm after external attenuation cannot manufacture an
unavailable nominal scaling. In particular P101's norm-one nominal filters
cannot meet c>1 for K>=2; hardware loss does not change this fact.
Equal attempt and injected-photon accounting does not establish equal
source latency, preparation, mesh, calibration, decoder or total wall costs.

## 4. P106 instance independently checked again

For F with rows (1,q),(q,1),(p,p),(p,p), p=exp(-1),q=exp(-3),
F^dagger F has eigenvalues (1+q)^2+4p^2 and (1-q)^2.
The inequalities exp(1)>2 and exp(3)>131/8>16 imply

    ||(2/3)F||^2 < (4/9)[(17/16)^2+1]=545/576<1.

Both gamma_B=1/3 and gamma_D=2/3 are physical, c=2 and K=2. Hence
D_new(n)>=8 B_old(n) for every full-K occupation, collisions included.
The decoder uses only the six CF receiver pairs; their exact cut gains
are -4, four copies of -6, and -8, with all invalid events held. Summing
these strictly beneficial gains proves D_new's expected improvement is at
least eight times B_old's. This is the same legal control as our P106 audit.

The positive same-T raw mean effect is also preserved: with gamma=1/3,
E_B C_out-E_D C_out=-8gamma^4[exp(-6)+6exp(-5)+2exp(-4)]<0.
The retuned D comparison defeats that B operating point, not the existence
of interference or every scale-retuned B family. Scoring the complete six
candidate pool is an additional paid local frontier, not an all-wall-time
or changing-pool theorem. Neither argument uses a known optimum.

## 5. Accepted scope

The result extends to full-K collisional decoding only with the required
number information. Under the ideal fixed-K passive model, K distinct
threshold clicks certify a CF full-K event; verified triggers/denominators
and absence of additional photons/noise remain necessary for hardware use.
Useful decoding of partial-loss records breaks the common-hold assumption.
Retuned control admissibility is falsifiable and must be demonstrated for
each proposal; if it fails, no positive result or no-go follows automatically.
Accept the conditional obstruction and its P106 application. No imports,
tests, numerical/native/QPU runs, manuscript or frozen-source edits occurred.
