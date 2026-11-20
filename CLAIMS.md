# Scientific Claims Registry

Format:
```
CLAIM-XXX
Statement:
Status: conjecture | proven | simulated | qpu-validated | rejected
Evidence:
Files:
Dependencies:
Last reviewed:
```

## Current Claims

### CLAIM-001
Statement: A passive linear interferometer conserves total photon number: [U, N] = 0.
Status: proven
Evidence: Unitary transformation preserves number operator
Files: theory/photon_number_theorems.tex
Dependencies: None
Last reviewed: 2026-11-20

### CLAIM-002
Statement: In the collision-free sector H_k^CF, all outcomes satisfy Σx_i = k exactly.
Status: proven
Evidence: By construction, H_k^CF only contains states with n_i ∈ {0,1} and Σn_i = k
Files: theory/photon_number_theorems.tex
Dependencies: CLAIM-001
Last reviewed: 2026-11-20

### CLAIM-003
Statement: Fixed photon number (∑n_i = k) implies collision-free occupations (n_i ∈ {0,1}).
Status: rejected
Evidence: Counterexample: |2,0,0,0⟩ has k=2 photons but collision
Files: reports/collision_bug_audit.md
Dependencies: None
Last reviewed: 2026-11-20

### CLAIM-004
Statement: P_CF = 1.0 for fixed-k photon interferometers.
Status: rejected
Evidence: P_CF < 1 for generic interferometers; must be measured
Files: src/photonic/fixed_photon_obliq.py
Dependencies: CLAIM-003
Last reviewed: 2026-11-20

### CLAIM-005
Statement: Penalty-based QUBO transforms sparse graphs into dense QUBOs with O(n²) couplings.
Status: conjecture
Evidence: Mathematical derivation pending
Files: theory/penalty_analysis.tex
Dependencies: None
Last reviewed: 2026-11-20

### CLAIM-006
Statement: The fixed-photon approach reduces the number of QUBO couplings compared to penalty-based methods.
Status: conjecture
Evidence: Pending comparison
Files: reports/feasibility_n4.md
Dependencies: CLAIM-001, CLAIM-002
Last reviewed: 2026-11-20
