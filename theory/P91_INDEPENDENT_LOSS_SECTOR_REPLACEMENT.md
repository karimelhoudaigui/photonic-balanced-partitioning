# P91: whole-law replacement under a certified spectral loss bound

**Primary verdict: proved under the precise passive-vacuum model below.**
A known collision-free k-photon input and a certified intensity bound
`||T||op^2<=eta` admit a classical small-survivor-sector replacement with
complete raw PNR TV error at most a binomial tail. Any common classical
decoder or quench contracts that error. This is a conditional mathematical
statement, not a calibrated Lucy conclusion, cost advantage or novelty claim.

ROOT supplied the candidate route and numerical expressions before this
independent static reconstruction. No other P91 proof was read. Only this
file is written. No scientific code/import, AST, test, RNG, seed/graph
generation, native probability, experiment outcome, QPU or manuscript
action occurred. The only external access was the public CEA documentation.

## 1. Exact source, channel and observation model

Let T be an `m_out by m_in` transmission matrix for a passive linear
optical channel with vacuum environmental inputs. Thus `T^dagger T<=I`.
No gain, thermal/nonvacuum environment, dark-count substitution,
nonlinearity or herald-conditioned channel is implicit. Input is the
known normalized Fock state with one identical photon in each of a
specified set A of k distinct input modes and vacuum elsewhere.
The k=0 vacuum case is immediate.

Assume a **certified spectral intensity upper bound**

    ||T||op^2 <= eta,       0<=eta<=1.

A mean transmission is not this premise. The measured object is the
entire raw output occupation vector, including vacuum, collisions and
all loss events. One raw source attempt remains one attempt. Detector
filtering/accepted-event conditioning is not a normalization step here.

The construction uses known T and ideal arithmetic/categorical sampling.
It does not supply a finite-bit implementation or a numerical calibration
error certificate. A fixed input can equivalently restrict T to its
occupied-input span, treating every unused input as vacuum. The full
norm bound above is sufficient; a separately certified norm bound on
that restricted matrix also suffices.

## 2. Nonuniform loss factors through uniform input loss

For `eta>0`, put `T'=T/sqrt(eta)`, a contraction. Choose a vacuum
isometric dilation of T' with environment matrix E' satisfying

    E'^dagger E'=I-T'^dagger T'.

One explicit choice is the positive square root on the right, stacked
below T'; the resulting orthonormal columns extend to a passive unitary
after adding vacuum modes. Compose uniform input loss of transmission
eta with this dilation. Its transmitted matrix is T, and its environment
columns, stacked in two independent vacuum banks, are

    E_comp = [sqrt(1-eta) I ; sqrt(eta) E'].

Their Gram matrix is

    E_comp^dagger E_comp
      =(1-eta)I+eta(I-T'^dagger T')=I-T^dagger T.

This proves equality of the reduced channels, not only matching means.
Indeed two environmental column families with the same Gram matrix
are related by an isometry on their spans: send each linear combination
of one family to the same combination of the other. Equal Gram matrices
make this well-defined and norm preserving. Complete orthonormal bases,
adding unused vacuum modes if necessary, to extend it to a unitary.
Its passive Fock action is confined to the traced environment, so the
system output channel is unchanged. No named external dilation theorem
is needed for this finite-dimensional argument.

Consequently the original channel equals **uniform loss first**, then
the passive-vacuum channel T'. At eta=0, T=0 and the output is vacuum
exactly, with no division or residual channel needed. Eta=1 also causes
no exception: the first loss stage is identity.

## 3. The survivor mixture is exact for the specified Fock source

At the uniform-loss stage each occupied creation operator becomes
`sqrt(eta) b_i^dagger+sqrt(1-eta)e_i^dagger`. Expanding the product
over A and tracing the environment gives

    rho_after_uniform_loss
      =sum_(J subset A) eta^|J| (1-eta)^(k-|J|) |1_J><1_J|.

Different lost-source subsets have orthogonal environment occupations,
which kills their cross terms. No surviving photon is declared
distinguishable: within a fixed J the remaining state is the usual
indistinguishable-boson Fock state and can still interfere fully.

The number L of first-stage survivors is therefore `Bin(k,eta)`.
Conditional on L=l, J is uniform among the `binom(k,l)` source subsets.
For any known efficiently sampled classical mixture of such inputs,
first draw its actual source label and apply this construction. Its
sampling/setup costs remain paid. A hard source distribution, a coherent
superposition of source occupations or arbitrary internally entangled
photons does not inherit this simple efficient-source claim.

## 4. Exact small sectors and a normalized full-attempt replacement

Choose an integer cutoff `s>=0`. Draw L and J from the stated law.
For `L<=s`, simulate T' on input J, including its additional losses,
exactly in the ideal arithmetic model. A passive dilation has finitely
many modes M. At l photons its complete occupation population has size
`binom(M+l-1,l)`. Each probability is the squared repeated-row permanent
divided by the Fock factorial products. Enumerating this finite law
and marginalizing its environment therefore gives the exact raw system
law. At fixed s, the photon-sector part is polynomial in mode count;
dilation/setup and probability arithmetic still have to be performed.

For `L>s`, return an explicit flag, or any fixed cheaply sampled
normalized fallback on the same raw count space. Vacuum is one possible
fallback. This is a replacement branch in a normalized sampler, not
discarding an attempt or resampling until a small sector occurs.

Couple the true and replacement processes using the same L,J. On the
low branch their conditional laws are identical. They can diverge only
on the high branch. Thus, for complete raw PNR laws P,Q,

    TV(P,Q) <= beta_(k,s,eta)
       :=Pr[Bin(k,eta)>s].                                (1)

With an explicit new flag outside P's count alphabet, TV equals beta
on that augmented alphabet; mapping it to a fixed raw fallback contracts
TV. If T' loses additional photons, the high first-stage branch may
produce few detected photons, so the tail can be conservative. It is
not a cutoff applied to the observed accepted photon count.

For `0<=s<k`, the nonnegative integer `binom(L,s+1)` is at least one
whenever `L>s`. Counting surviving `(s+1)`-subsets gives

    beta <= E binom(L,s+1)=binom(k,s+1)eta^(s+1),           (2)

clipped at one if desired. For `s>=k`, beta is zero. These statements
also cover eta=0/eta=1 by their direct binomial laws.

## 5. Decoding, classical adaptivity and absolute-error meaning

Any identical classical randomized decoder, loss/failure policy, quench
or score applied to both raw outputs is a Markov kernel. TV contracts,
so (1) persists even with classical completion of unclicked vertices.
The decoder must be defined on all raw losses/failures; an existing
lossless-only decoder is not silently changed by this theorem.

For a fresh-shot, measured/reset protocol with at most t raw attempts,
suppose each common history has a known source and a certified bound
eta_h, with no hidden coherent memory. Couple matching histories and
apply (1) to the next common kernel. A first-divergence argument gives

    TV(full raw/classical transcripts)
      <=min(1,sum_(j=1..t) E_P beta_(k_h,s,eta_h)).          (3)

Uniform upper bounds on k and eta give the simpler t-times-tail bound.
Common count-driven stopping rules can be padded with stop symbols.
Hardware/simulator timing tags or unrelated time-based stopping are
not covered by an unproved coupling. No continuity of the controller's
matrix choices is needed; their conditional spectral bounds are needed.

These are absolute errors. They do not prove a relative success ratio,
stochastic optimizer domination or equal-cost advantage. A bounded
score's mean error is at most its range times the relevant TV bound.
Conditioning on a rare herald, all-photons-detected event or accepted
sample may amplify error by an inverse acceptance scale; (1)-(3) do
not transfer unchanged to such conditional laws. The photon input cost
is k per attempted modeled source pulse, including flagged/vacuum
fallbacks, not the number of first-stage survivors or returned samples.

## 6. Hypothetical arithmetic and the actual public Lucy evidence

If a separate calibration really certified eta<=1/50 at every permitted
history, s3 and k<=12 would give the 96-attempt conservative bound

    96*binom(12,4)/50^4=47520/6250000=0.0076032.

For k<=8 the corresponding number is

    96*binom(8,4)/50^4=6720/6250000=0.0010752.

These are hand-checked hypothetical upper bounds, not data or exact
tail evaluations. They are not instantiated by the public mean below.

The [CEA TGCC public stack documentation](https://www-hpc.cea.fr/tgcc-public/en/html/toc/QuantumSoftwareStack.html)
has header `2026-09-08.1512`. Its **Lucy Hardware** paragraph lists
up to twelve photons and twenty-four fibers. Its **Using Lucy / From
Qaptiva simulation to Lucy** section describes average transmittance
of two percent and says the metrics are indicative and can change.
Those public statements are not a per-session calibration, a current
account allocation, or an operator-norm upper bound. No get_specs or
QPU call was made; only the public page was read.

Even the stronger mathematical interpretation `Tr(T^dagger T)/24=.02`
would not imply `||T||op^2<=.02`: a diagonal channel with one intensity
.48 and twenty-three zeros has that mean and spectral intensity .48.
Thus neither hypothetical bound above is a Lucy hardware conclusion.
The needed certificate is a suitable worst-direction/occupied-subspace
transmission bound for every allowed circuit, not a mean scalar.

## 7. Noise, cost and scientific boundary

Known common classical detector/noise postprocessing contracts TV and
can be appended with its own paid simulation cost. A known classical
mixture of passive-vacuum channels can be treated realization by
realization if the same uniform norm certificate holds. Arbitrary
decoherence, nonvacuum source noise, dark counts, unknown internal
states or memory cannot be declared free consequences of (1). Loss
has not turned the surviving bosons into independent classical photons.

T, its accuracy certificate, dilation, source sampling, sector
probabilities, categorical draws and the common controller/quench all
require classical work. Exact ideal sampling is not a finite-bit TV
implementation or a measured CPU bound. Physical source preparation
and failures also remain costs; no successful-preparation denominator
or free squeezing/entangled source is assumed. No optical/classical
latency ratio, end-to-end speedup or matched-resource superiority follows.

Lossy boson sampling and low-photon classical simulation are established
topics; novelty and exact prior overlap are not checked here. The safe
result is the explicit conditional whole-law replacement and its
transcript/error accounting. It does not close the positive optimization
goal or authorize a new experiment, hardware submission or paper edit.
