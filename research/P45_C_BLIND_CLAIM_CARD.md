# P45-C claim-first review packet

This packet states mathematical targets without an author verdict. No P45-C
code, numerical raw or executed pilot exists. Do not substitute older P42/P44
data as evidence for these targets. Reconstruct the objects and factors before
reading `theory/P45_C_balanced_suppression_attempt.md`.

1. For b>=2, rho=sqrt((b-2)/(2(b-1))), beta=(1-rho)/b and
   gamma=sqrt(1-rho^2), define B=rho I+beta J, C=gamma(I-J/b),
   U=[[C,B],[B,-C]]. Input: one identical photon in every old mode, none in
   new modes. Check unitarity, exact old/new balance, and the full CF proposal
   kernel with all non-CF outcomes merged into one failure.
2. Partition a CF support by pair-index types empty, old-only, new-only, both.
   Let counts(e,u,v,d) obey e=d and b=2d+u+v. Test whether its probability
   depends only on(d,u,v), with multiplicity b!/(d!^2 u!v!). Independently
   derive a polynomial coefficient formula for each amplitude and the resulting
   classical CF-plus-failure sampling complexity, including repeated pair
   indices and exact arithmetic qualifications.
3. For unitary W of size q, let H=[[0,W],[W*,0]], P=(I+H)/2, Q=I-P,
   U(W)=[[Q,P],[P,-Q]], with2q occupied old inputs and2q vacant new inputs.
   Audit invariance of number probabilities under W->D_A W D_B* and complex
   conjugation, and the implications/limits for W=exp(i tau C), C real symmetric.
4. For z=exp(i phi), check the four-mode unitary
   V=1/2[[1,1,1,1],[1,z,-1,-z],[1,-1,1,-1],[1,-z,-1,z]]. Derive its permanent
   and identify exactly what its phase dependence does and does not imply.

Keep constant-block exact replacement, growing-b algebra, raw versus
CF-conditioned probabilities, graph scoring/label budgets, and search advantage
as separate obligations. No novelty or universal optimization conclusion is
part of this packet.
