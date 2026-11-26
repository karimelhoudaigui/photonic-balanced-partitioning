# P140 public capability check — simulation support is not a Lucy contract

26-Nov-2026. Read-only primary web documentation check by ROOT. No remote
processor/computer was instantiated, no account specs or credentials were
queried, and no job was submitted. Installed Perceval1.3.0 pins are unchanged.
This note neither validates P140's mathematics nor prepares its hardware run.

[Perceval v1.3 feed-forward configurators](https://perceval.quandela.net/docs/v1.3/reference/components/feed_forward_configurator.html)
document measured classical modes, a mandatory default, and conditional
circuit/parameter configurations in an Experiment. The
[v1.3 Computer reference](https://perceval.quandela.net/docs/v1.3/reference/runtime/computer.html)
separately describes local simulated execution, including feed-forward, and
remote computers backed by a communication layer. These are API/model facts.

[Official release notes, v1.0.0](https://github.com/Quandela/Perceval/releases/tag/v1.0.0)
state that remote feed-forward was initially limited to a subset of platforms
and identify sim:slos at that release. This is HISTORICAL evidence of platform
dependence, not evidence that the same restriction still holds in November2026.

Inference: the public software support does not establish Lucy/TGCC's current
in-shot PNR measurement, delay/storage, conditional-switch latency, permitted
input routing, complete-attempt counting or a usable feed-forward endpoint.
Those remain UNVERIFIED. Public mode/photon capacity alone cannot supply them.
An eventual hardware check must use the actual authorized platform contract;
this research cycle does not make that check or any QPU call.

In particular a simulator, a postselected collection of static branches, or
adapting the next shot is not by itself an executed within-shot P140 protocol.
The complete cost of any proposed emulation needs its own comparison. P140
already retains a proper-group/classical veto for its simple graph example;
neither software support nor its nonstatic witness is an optimizer gain.
