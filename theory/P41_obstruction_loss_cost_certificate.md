# P41/R3 — conditional loss-versus-classical-cost certificate

Status: elementary analytic corollary, self-reviewed; no global novelty claim
or claim that all photonic algorithms are impossible. This is not the P41
discovery endpoint and does not replace the existing P37 Haar source theorem.

## Precise class and resource units

The graph has2k vertices, k>=2, and an undirected cut cost. A successful optical
candidate is a balanced partition encoded by at least k genuinely detected
photons. Each fresh optical attempt injects at most N_max photons, each subject
to independent uniform survival eta in [0,1]. No dark-count replacement,
unaccounted heralding/preparation, recycling, quantum memory or classical
completion of a shorter detected string is allowed in this class.

Graph-dependent interferometers, arbitrarily informed parameters and adaptive
choices based on previous measurements are allowed. We bound only discoveries
from the optical output. Optima already discovered by classical preprocessing
or independently generated classical candidates are credited separately.
The comparison is conditional on the same fixed classical front-end history,
or concerns the incremental optical contribution after that front end.

Let g be the number of optimal oriented balanced strings and D=binom(2k,k).
Complementation gives g>=2. Uniform feasible classical sampling has success
p_G=g/D>=p_0=2/D per independent candidate. This lower bound uses no oracle
during sampling or training.

## Universal optical bound, without a Haar assumption

Success requires at least k surviving photons, so conditionally on every
previous history each optical attempt has success probability at most

    a=sum_(j=k)^N_max binom(N_max,j) eta^j(1-eta)^(N_max-j).

Monotonicity in injected photon number makes this valid for adaptive choices
N_t<=N_max. For N_max=k, a=eta^k. The bound permits perfect graph enrichment
after survival and thus is conservative in favor of the optical device.

For at most n_Q attempts, induction on failure histories yields

    Pr(optical discovery)<=1-(1-a)^n_Q.                    (1)

No independence of the adaptive choices is needed; the conditional success
bound and independent uniform survival are the assumptions. Meanwhile n_C
independent uniform feasible draws satisfy

    Pr(classical discovery)>=1-(1-p_0)^n_C.                (2)

This generalizes beyond a Haar-averaged feasibility calculation, but its
survival and elementary sampling ingredients are established and unoriginal.

## Exact finite budgets, and a rational sufficient condition

If fixed full primitive costs satisfy c_Q>0,c_C>0, let n_Q=floor(T/c_Q),
n_C=floor(T/c_C). Ignore quantum training costs only to make its upper bound
more favorable. Using (1)-(2), the classical lower bound dominates whenever

    n_C [-log(1-p_0)] >= n_Q [-log(1-a)].                 (3)

For0<=a<1 a completely rational sufficient condition is

    n_C p_0 (1-a) >= n_Q a,                               (4)

because x<=-log(1-x)<=x/(1-x). This avoids uncertified floating logarithms.
At a=0 the optical component cannot succeed. At a=1 these certificates give
no useful obstruction. The p_0=1 case is only the excluded trivial k=1 graph.
Deterministic cost bounds (upper for classical, lower for optical) suffice;
sample-average timings alone do not certify the finite-floor comparison.

The asymptotic failure-rate condition is

    c_C/c_Q <= [-log(1-p_0)]/[-log(1-a)],

but it is not a guarantee at every finite budget: floor effects must be
checked through (3) or (4). Resource units must not be silently identified.
A classical draw is not a physical pulse, nor is a provider nonempty-event
"shot" a physical injection attempt. Cost ratios require measured accounting.

## Why this is a gate, not a blanket algorithmic impossibility

The certificate can reject an expensive fixed-photon hardware proposal even
if its post-loss conditional quality were perfect. It does not restrict
classically completed lossy encodings, larger fresh sources, error correction,
or algorithms succeeding through their classical subroutine. A useful escape
must name the changed assumption and charge it.

No actual Lucy eta or timing is inferred here from advertised performance.
This lane made no account/API call. Contemporary source/detector calibration
and full preparation/attempt accounting would be needed to instantiate (4).
No quantitative hardware no-go is declared from an unmeasured parameter.
