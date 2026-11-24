# A score-free classical countercontrol for the leading double-swap amplitude

Author: p41_adaptive. Derived candidate; independent audit pending.
This note does not modify the frozen R1 probe or claim a new benchmark.

Let S be the k occupied inputs, A=H_(Sbar,S) and L=||A||_F^2. For distinct
a,c in S and b,d outside S define

    B_(ac,bd)=|A_ba A_dc + A_bc A_da|^2,
    D_(ac,bd)=|A_ba A_dc|^2 + |A_bc A_da|^2.

The following is an exactly normalized classical attempt with no graph-cost
oracle calls:

1. If L=0, hold at S. Otherwise draw two entries(a,b),(c,d) independently
   with probability |A_ba|^2/L.
2. If an input or output index repeats, hold. Otherwise accept the double
   swap S\{a,c} union {b,d} with probability B/(2D), and hold otherwise.
   If D=0, define rejection; such an entry pair has zero sampling probability.

The acceptance is in[0,1] by |x+y|^2<=2(|x|^2+|y|^2). A fixed unordered
input/output pair occurs under the two entry draws with probability2D/L^2:
each of its two matchings has two draw orderings. Thus the final useful mass
is EXACTLY B/L^2 for that double swap. The remaining probability holds at S.
After O(mk) weight setup, a proposal uses two categorical draws and four
complex entries, not an exhaustive O(m^4) scored neighborhood.

For passive U(t)=exp(-itH), the exact bosonic amplitude for this two-swap
output is -t^2 per(A_[b,d;a,c])+O(t^3): at minimum order the two moved photons
must occupy the new modes, while all other photons stay in place. Therefore
the physical probability is t^4 B+O(t^5). This holds for arbitrary total k,
not only a constant-size interacting block. The classical countercontrol
reproduces its leading coherent two-swap coefficient. When
|t|||H||<=1/(2sqrt(k)), t^4 L^2<=1/16, so the leading classical per-attempt
probability B/L^2 is at least16 times t^4 B wherever B>0.

This coefficient comparison is NOT a finite-t pointwise domination theorem:
the O(t^5) remainder has not been uniformly controlled in this note. Sampling
setup, matrix construction and scoring remain charged; categorical draws,
classical score calls, and physical optical shots are not identical resource
units. No algorithmic advantage or all-angle obstruction follows by itself.

For r moved photons, the same construction samples r independent cross entries,
rejects repeated inputs/outputs, and accepts with
|per(A_OI)|^2/[r! per(|A_OI|^2)]. Cauchy-Schwarz makes this a probability;
r! draw orderings cancel it to give |per(A_OI)|^2/L^r. Computing the acceptance
costs permanents of size r, so this is cheap at r=2 but is not a polynomial
classical sampler for arbitrary extensive r. It supplies a concrete baseline
for proposed low-order escape mechanisms; genuinely many-swap/finite-angle
effects remain an open continuation.
