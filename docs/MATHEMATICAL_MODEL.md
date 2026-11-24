# Mathematical model and conventions

The graph is simple, undirected, even-order, with finite nonnegative weights. For binary x with sum x=n/2, C(x)=sum_(ij) w_ij |x_i−x_j|. Complementary strings have equal cost but remain separate detector outcomes. K4 has minimum4 and six optimal strings; K2,2 has minimum2 and four.

For the direct encoding, m=n modes and k=n/2 distinct single-photon inputs enter a lossless passive unitary. V comprises its occupied columns, with V†V=I. Every k-photon Fock occupation, including collisions, is retained. Bosonic probabilities are permanent amplitude squares divided by output factorials; distinguishable probabilities sum labeled assignment probabilities with their labels forgotten.

Validity F requires no collision AND k detected photons. Success O is validity plus retrospectively optimal cost. Per injected attempt, P_success=P(F)P(O|F). After loss, vacuum is collision-free but not valid. Observed emission/trigger/injection denominators must be specified.

For P33 define q_ia=|V_ia|², a_i=sum_a q_ia, M=sum_i(a_i²−sum_a q_ia²)=E_b sum_i binom(t_i,2), delta=sum_i(a_i−max_a q_ia). M counts expected unordered collision pairs, not collision probability. The spatial amplitude-magnitude Gram is B_ab=sum_i sqrt(q_ia q_ib), with B_aa=1. It differs from the photons' internal Gram S.

If every positive a_i≥c>0, delta≤M/c. For M<c²/2, delta≤[c−sqrt(c²−2M)]/2. The paper proves the full-TV envelope through ||B−I||_F≤2sqrt(delta)+delta and a permanent/cycle bound. The small-M leading envelope M/(2c) holds with c fixed; mean k/m cannot supply that floor. The float API is not interval certification.

The P37 alternate source protocol injects N in [m/2,m] and accepts exactly m/2 threshold clicks under Haar averaging. Its h(l) composition law, two/four candidate theorem and boundary eta=1−lambda/m are in theory/phase3_loss_source_selection.md and the manuscript. It is distinct from direct N=k collision-free encoding.

Training costs and feasibility are accessible without C*. The new optimization.training_loss API rejects optimum-oracle objectives; exact simulated probability enumeration still has a classical cost. Older diagnostic APIs/scripts remain archived and explicitly oracle-labeled.

See [noise assumptions](NOISE_MODEL.md), [full proofs in the manuscript](../paper/main.tex) and [theory sources](../theory/phase3_density_certificate.md).
