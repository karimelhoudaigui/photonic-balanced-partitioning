# P89 independent exact-source mathematical audit

26 November 2026. **Primary verdict: proved as written**, under the stated
fresh uniform source-mark and lossless raw-proposal hypotheses. No optimizer
performance, novelty, fixed-seed independence or post-quench result is proved.

## Claim card and exact target

For a fixed real-weighted undirected graph on `2K` vertices, `K>=2`, fix
`|S|=|T|=K`. A uniform source ordering sigma is independent of all other
fresh marks. The removed port set P and receiving/repair construction do not
read sigma; let `r=|P|`, `R=sigma(P)` and `X=(S\R) union Y`, `Y subset T`,
`|Y|=r`. At each positive-probability size r, the asserted law is

    Pr(R=R0,Y=Y0 | G,S,r) = mu_(G[T],r)(Y0)/binom(K,r).

The resulting raw cut mean is equation (2) of the source, including its
half-replacement specialization and endpoint cases. Changed compiler examples
demonstrate the separate roles of source-label blindness and induced-subgraph
dependence, rather than positive optimization results.

Exact artifact: `theory/P89_INDEPENDENT_REMOVAL_FACTORISATION.md`, 215 lines,
commit `f775f68233279cd3551f28a1176275596f607ed1`, in
`.local/p81-exact-review`, SHA-256
`e99a1e32ca6ea64c4b038fda1ef31ce8ee8e902cfa7feaa27737567d31ab7350`.
All 215 lines were read. This is a separate audit of that frozen document,
not an edit of its primary evidence.

## Dependencies and obligations

The implication chain is: explicit independent marks and sigma-blind
receiving law -> finite permutation fiber count -> conditional product law
-> internal/cross-edge indicator averages -> raw quadratic mean.
The K4 examples additionally use a displayed flat passive family, the
normalized two-photon permanent rule and uniform graph-blind repair.
These leaves are internal finite algebra or explicit hypotheses, with no
external theorem or computational evidence required.

| Obligation | Status | Decisive check |
|---|---|---|
| Uniform labeled removals conditional on receiving data | Passed | Every fiber has `r!(K-r)!` source orderings |
| Receiver depends on `G[T]` in the frozen compiler | Passed | Prior exact source review plus bounded text check of `compile_receiver` |
| Cross-edge coefficient and edge-count convention | Passed | Crossing indicator gives `1-r/K+(2r/K-1)1_Y(j)` |
| Endpoint and half-replacement cases | Passed | `r=0,K` give `Wcross`; `r=K/2` removes the receiver-dependent cross term |
| K4 marked covariance | Passed | Joint raw CF masses `q0/2` and `q0/8`; constant repair term cancels |
| Cross-only receiving contrast | Passed | Raw `r2` one-edge contrast `-q0/2`, then marked-order weight `1/24` |
| Deterministic PCG realizes the ideal independent law | Out of scope | Explicitly not asserted |
| Quench, canonical removal masks, adaptive advantage | Out of scope | Nonlinear maps/selection need not preserve the product law |

## Critical derivation checks

Conditioning on every other mark fixes P and Y while leaving sigma uniform.
There are exactly `r!(K-r)!` bijections taking P to a prescribed R0.
This probability is independent of the fixed receiving data, so averaging
those data at size r yields the claimed product law. It covers `r=0,K`
as singleton fibers as well. Unique desirable removal has probability
`1/binom(K,r)`, while a desirable family has its cardinality divided by that
same denominator. This is not a bound on total optimization success.

For an internal S edge, exactly one endpoint is removed with probability
`2r(K-r)/(K(K-1))`. For a cross edge i,j, independence gives

    E[1_edge_crosses | Y,r] = 1-r/K+(2r/K-1)1_(j in Y).

An internal T edge contributes its cut indicator under Y. Adding unordered
internal edges and each S–T edge once reproduces equation (2), including
real signed weights. At half replacement the coefficient of every
receiver-dependent cross-edge marginal vanishes. This does not eliminate
the receiving induced-subgraph term or control the tail of the raw cost.

### K4 source-informed witness

Using the declared two-mode Fourier blocks, the four-mode family is

    W(z) = (1/2) [[1, 1,  1,  1],
                  [1,-1,  z, -z],
                  [1, 1, -1, -1],
                  [1,-1, -z,  z]],  z=+1 or -1.

For output pair `{0,1}`, input pairs `02,13` have probability
`(1+cos(phi))/8`, pairs `03,12` have `(1-cos(phi))/8`, and `01,23`
have zero. Each bunched output has probability `1/8`, independent of
the input pair and z. Repair therefore adds `2*(1/8)*(1/3)=1/12`
to this labeled output pair in every case; that term cannot create
the claimed covariance.

With odds `(a,b,a,b)=(1/2,3/2,1/2,3/2)` and
`q0=product(1-p_i)=16/225`, an input pair has raw mass `q0*o_i*o_j`.
Let `j*=sigma^-1(s*)`. The source-informed phase rule selects z+ for
`j*=0,2` and z− for `j*=1,3`, before any split. Averaging these four
positions gives the raw CF masses

    Pr(Y0,r2)_CF = q0*(a^2+b^2+2ab)/8 = q0/2,
    Pr(s* in R,Y0,r2)_CF = q0*(a^2+ab)/8 = q0/8.

Since `Pr(s* in R | r2)=1/2`, their raw covariance difference is
`q0/8-(q0/2)/2=-q0/8`. The repaired-bunch contribution cancels.
Exactly one of the 24 uniform target orderings uses this branch, while
the others are source-blind, giving `-q0/192=-1/2700` overall.
This is a raw size-weighted difference; a covariance conditional on r2
would additionally divide by `Pr(r2)`. The source does not confuse them.

### Cross-informed but source-blind witness

Take the fixed receiving edge to join the labeled plus pair in the marked
ordering. For each fixed input pair, repaired one-vertex marginals are
`1/2`: flat output mean is `1/2`, bunching subtracts `1/8` from its
support probability, and repair adds `1/8` back. Hence the raw r2
edge-cut difference between phase zero and pi is minus twice the
difference in that pair's joint inclusion mass:

    -2*q0*(a^2+b^2-2ab)/4 = -q0/2 = -8/225.

Marking only one target ordering gives `-1/675`. A cross-edge bit may
choose these two phases without reading sigma. Thus mu can change with
cross edges at fixed `G[T]`, while uniform R and independence from Y
survive. The explicit marked-order rule avoids cancellation from averaging
a label-independent port-phase change. These are changed-law witnesses;
their special marked labels do not certify a relabeling-robust optimizer.

## Source correspondence, boundaries and provenance

The already audited compiler at `94f80b94` uses `source_order` only for
its length. A bounded text reread of `compile_receiver` and its wrapper
confirms that graph accesses forming Q use target vertices only. The
factorization therefore matches its ideal raw dependency structure. This
is not a new full source audit or a claim about deterministic role seeds.

R denotes physical removed source labels before canonicalization. Applying
a common complement representative preserves cut values and thus equation
(2), but need not preserve the interpretation or law of a derived removal
mask. The graph-dependent quench, acceptance, completed-only selection and
adaptive incumbent updates cannot inherit the factorization without a new
argument. Fresh marks at each history support a conditional one-step law,
not a global trajectory or optimizer no-go. Loss/resource-selected laws
and full-cost comparisons remain separate obligations.

There is no remaining gap within the stated theorem. The cheapest next
proof-level check for any changed compiler is its actual dependence on sigma
and cross edges; no additional probability run is needed to accept P89.
The positive optimization objective remains open.

Review provenance: separate reviewer of the frozen author's proof, with
ROOT's candidate/claim context available; not blind independent discovery.
All displayed checks above are hand algebra. Only instruction/document/source
text reads, file hashes and isolated report/Git operations were used. No
outcome, seed value, generated graph, import, AST, test, RNG evaluation,
numerical matrix/probability execution, native call, QPU or manuscript edit
was involved. No primary proof or pilot parameter was changed.
