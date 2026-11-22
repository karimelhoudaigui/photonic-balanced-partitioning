# Figures Directory

This directory should contain the following publication-quality figures (to be generated):

## Required Figures

1. **fig1_mapping.pdf** - Photonic mapping: graph → interferometer → collision-free = balanced partition
2. **fig2_hom.pdf** - HOM effect: P_CF=0 for 50:50 BS with |1,1⟩ input
3. **fig3_haar_scaling.pdf** - Haar P_CF vs n: theory vs simulation
4. **fig4_variational_p_success.pdf** - Variational P_success vs n: beats Haar and Penalty
5. **fig5_pareto_frontier.pdf** - Pareto frontier: P_CF vs P_opt|CF for different objectives
6. **fig6_boson_vs_dist.pdf** - Bosonic vs Distinguishable P_success ratio vs n
7. **fig7_equal_budget.pdf** - Equal budget comparison: Variational vs Penalty
8. **fig8_qpu_protocol.pdf** - QPU protocol flowchart
9. **fig9_noise_robustness.pdf** - Noise robustness: loss and distinguishability
10. **fig10_objective_comparison.pdf** - Objective comparison radar chart

## Generation Scripts

Figures should be generated from the experimental data in `experiments/` using the plotting scripts in `scripts/plot_results.py` and `experiments/plot_results.py`.

## Style Guidelines

- Use consistent color scheme across all figures
- Vector format (PDF) for publication
- Font size: 10pt minimum for axis labels
- Include error bars (95% CI) where applicable
- Consistent legend placement
