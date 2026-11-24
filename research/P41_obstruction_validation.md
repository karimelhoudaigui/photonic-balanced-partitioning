# P41/R3 exact finite validation

Run: experiments/P41_obstruction_l1/run/manifest.json, schema2, completed and
validated with the installed computation-audit validator. Actual source commit
fe02f170411d7aab8aee4c5b67ad62bfbfc1985b, clean before execution. Contract/code
were committed at281d2be; later intervening commits added only separate theory.

The exact Fraction program retained both rational unitary frames and all10
complete Fock probabilities, including zero-valued and collisional events.
All64 simple labelled graphs, two frames and three penalties were checked:
384 exact identities, with no exclusions or tolerance. All64 adjacency
conditional-negative/complete-multipartite checks pass via all rational
principal minors. The connected epsilon1/4,mu1 witness has a bosonic mean
minus distinguishable mean of -3/16, while its smallest collisional cost is
strictly larger than its feasible minimum1/4.

Runner wall time0.142664 seconds. CPU cap10s, wall cap30s, one thread and
1MiB log cap. No requested affinity or hard-address-space cap is claimed;
the pure-Python finite domain allocates small lists and uses no numerical
library or additional worker. All observed input hashes match before/after.
No hardware/API call, random sampling, optimizer or training was executed.

Verdict: implementation and finite assertions verified by exact arithmetic.
This is not an independent replication or a universal mathematical proof;
the general statements remain separately derived and await independent audit.
It refutes a proposed all-convex-cost no-go, but supplies no algorithmic
advantage over reoptimized/strong classical controls. The new objective route
must still pass the P41 acceptance contract.
