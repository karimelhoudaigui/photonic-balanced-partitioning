# P36 falsifiable strengthening: linear leakage bound

Base715143f, 2026-11-22. The exact P33 density theorem is retained. New
CONJECTURE, not a result: for every orthonormal complex occupied frame,
complete bosonic and distinguishable occupation laws satisfy
TV<=min(1,delta), delta=sum_i(sum_a|V_ia|²-max_a|V_ia|²).
Single occupation in distinct inputs; no loss, conditioning or hardware.
The existing proof gives only the larger cycle envelope. Existing P33 cases
motivate this question but cannot prove it. Physics pursues an independent
analytic route; literature checks the exact stronger statement.

Discriminator:256 complete-law finite circuits, including full occupation
m=k=3/4/6/8 and balanced m2k=4/6/8/10. Five fixed seeds per size and four
strengths0.03/0.15/0.5/1.0. Coordinate starts everywhere; disjoint-pair starts
at balanced sizes. Sixteen extra deterministic collective rank-one unitaries
cover the fully occupied sizes and the same strengths. All cases retained,
including delta>=1 where the conjecture is trivial. No favorable filter or
performance/population inference. Fixed seed2026112200+100*m+repeat.

Bosonic complete law uses the existing validated Fock creation recurrence;
distinguishable law uses independent labelled categorical DP. Retain unitaries,
full bases/laws, delta, raw excess, normalization and every counterexample.
Numerical falsifier: TV-min(1,delta)>1e-9. Every candidate needs independent
Perceval and preferably an exact/symbolic witness before a mathematical
refutation. Smaller excess remains recorded, not silently promoted.
Check the existing P33 envelope separately to detect implementation regressions.

One thread,120-second cap, complete Fock cap30000 states, no local model.
No optimizer, paper or physical shots. Outcome SUPPORTED refers only to the
finite grid; absent a proof the universal statement stays conjectural.
If false, retain the sharpest surviving bound and exact obstruction. If true
in this grid, the next task is the missing general implication, not more
unchanged favorable sweeps.
