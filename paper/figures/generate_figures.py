#!/usr/bin/env python3
"""Generate publication-quality figures from experimental data."""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Set publication style
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.figsize': (6.5, 4.5),
    'figure.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.format': 'pdf',
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman'],
    'text.usetex': False,
})

OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

# Color scheme
COLORS = {
    'variational': '#1f77b4',
    'haar': '#ff7f0e',
    'penalty': '#2ca02c',
    'bosonic': '#d62728',
    'distinguishable': '#9467bd',
    'ideal': '#1f77b4',
    'loss': '#ff7f0e',
    'distinguishability': '#2ca02c',
}

def load_experimental_data():
    """Load experimental data from experiments directory."""
    data = {}
    exp_dir = Path(__file__).parent.parent.parent / 'experiments'
    
    # Load Haar baseline
    haar_file = exp_dir / 'E01_haar_collision_baseline' / 'summary.json'
    if haar_file.exists():
        with open(haar_file) as f:
            data['haar'] = json.load(f)
    
    # Load variational optimization
    var_file = exp_dir / 'E02_ideal_optimization' / 'summary.json'
    if var_file.exists():
        with open(var_file) as f:
            data['variational'] = json.load(f)
    
    # Load equal budget
    eq_file = exp_dir / 'E05b_exact_equal_budget' / 'summary.json'
    if eq_file.exists():
        with open(eq_file) as f:
            data['equal_budget'] = json.load(f)
    
    return data

def fig_haar_scaling(data):
    """Figure 3: Haar P_CF vs n scaling."""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    n_vals = [4, 6, 8, 10]
    theory_pcf = [6/10, 20/56, 70/330, 252/2002]
    
    if 'haar' in data:
        sim_pcf = [r['p_cf']['mean'] for r in data['haar']['results']]
        sim_pcf_err = [(r['p_cf']['ci95'][1] - r['p_cf']['ci95'][0])/2 for r in data['haar']['results']]
        ax.errorbar(n_vals, sim_pcf, yerr=sim_pcf_err, fmt='o-', 
                   label='Simulation', color=COLORS['haar'], capsize=3)
    
    ax.plot(n_vals, theory_pcf, 's--', label='Theory $d/D$', color=COLORS['variational'])
    
    ax.set_xlabel('Number of modes $n$')
    ax.set_ylabel('Collision-free probability $P_{\\mathrm{CF}}$')
    ax.set_yscale('log')
    ax.set_xticks(n_vals)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_title('Haar collision-free probability vs. system size')
    
    plt.savefig(OUT / 'fig3_haar_scaling.pdf')
    plt.close()

def fig_variational_p_success(data):
    """Figure 4: Variational P_success vs n."""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    if 'variational' in data:
        # Group by graph family
        families = {}
        for r in data['variational']['results']:
            fam = r.get('graph', r.get('family', 'unknown'))
            if fam not in families:
                families[fam] = {'n': [], 'p_success': []}
            families[fam]['n'].append(r['n'])
            families[fam]['p_success'].append(r['after']['mean'])
    
    for fam, vals in families.items():
        ax.plot(vals['n'], vals['p_success'], 'o-', label=fam, markersize=5)
    
    # Haar baseline
    n_vals = [4, 6, 8, 10]
    haar_p_success = [0.2, 0.0357, 0.00606, 0.001]
    ax.plot(n_vals, haar_p_success, 'k--', label='Haar', alpha=0.5)
    
    ax.set_xlabel('Number of modes $n$')
    ax.set_ylabel('Physical success probability $P_{\\mathrm{success}}$')
    ax.set_yscale('log')
    ax.set_xticks(n_vals)
    ax.legend(fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_title('Variational $P_{\\mathrm{success}}$ vs. Haar baseline')
    
    plt.savefig(OUT / 'fig4_variational_p_success.pdf')
    plt.close()

def fig_boson_vs_dist():
    """Figure 6: Bosonic vs Distinguishable ratio."""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    n_vals = [4, 6, 8, 10, 12]
    # Data from our experiments
    ratios = {
        'path': [1.0, 1.0, 0.84, 0.42, 1.21],
        'cycle': [1.0, 1.39, 1.41, 0.35, 1.13],
        'ER': [1.0, 1.0, 2.37, 0.88, 1.84],
        'RR': [1.0, 1.0, 0.89, 1.97, 4.81],
        'planted': [1.0, 1.0, 0.84, 0.42, 1.21],
    }
    
    for fam, ratios_fam in ratios.items():
        ax.plot(n_vals, ratios_fam, 'o-', label=fam, markersize=5)
    
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.5)
    ax.set_xlabel('Number of modes $n$')
    ax.set_ylabel('Ratio $P_{\\mathrm{success}}^{\\mathrm{boson}} / P_{\\mathrm{success}}^{\\mathrm{dist}}$')
    ax.set_xticks(n_vals)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_title('Bosonic vs. distinguishable advantage')
    
    plt.savefig(OUT / 'fig6_boson_vs_dist.pdf')
    plt.close()

def fig_equal_budget():
    """Figure 7: Equal budget comparison."""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    n_vals = [6, 8, 10, 12]
    families = ['path', 'cycle', 'ER', 'RR', 'planted']
    
    # Data from equal budget experiments
    var_data = {
        'path': [0.982, 0.537, 0.112, 0.034],
        'cycle': [0.290, 0.209, 0.093, 0.015],
        'ER': [0.987, 0.060, 0.256, 0.019],
        'RR': [0.982, 0.581, 0.087, 0.010],
        'planted': [0.988, 0.537, 0.112, 0.034],
    }
    pen_data = {
        'path': [0.195, 0.082, 0.015, 0.003],
        'cycle': [0.257, 0.131, 0.053, 0.016],
        'ER': [0.265, 0.054, 0.048, 0.011],
        'RR': [0.124, 0.095, 0.009, 0.011],
        'planted': [0.245, 0.082, 0.015, 0.003],
    }
    
    x = np.arange(len(n_vals))
    width = 0.15
    
    for i, fam in enumerate(families):
        offset = (i - 2) * width
        ax.bar(x + offset, var_data[fam], width, label=f'{fam} (var)', 
               color=COLORS['variational'], alpha=0.7)
        ax.bar(x + offset + width, pen_data[fam], width, label=f'{fam} (pen)',
               color=COLORS['penalty'], alpha=0.7, hatch='//')
    
    ax.set_xlabel('Number of modes $n$')
    ax.set_ylabel('$P_{\\mathrm{success}}$ (200 evals)')
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in n_vals])
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_title('Equal budget: Variational vs. Penalty')
    
    plt.savefig(OUT / 'fig7_equal_budget.pdf')
    plt.close()

def fig_objective_comparison():
    """Figure 10: Objective comparison radar chart."""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    objectives = ['$P_{\\mathrm{success}}$', '$P_{\\mathrm{CF}}$', '$P_{\\mathrm{opt|CF}}$', 
                  '$\\mathbb{E}[C|\\mathrm{CF}]$', 'Collision-aware', 'Log barrier']
    
    # Normalized metrics for path n=8
    metrics = {
        '$P_{\\mathrm{success}}$': [1.0, 0.08, 0.23, 0.22, 0.56, 0.53],
        '$P_{\\mathrm{CF}}$': [0.73, 0.85, 0.18, 0.14, 0.31, 0.32],
        '$P_{\\mathrm{opt|CF}}$': [0.73, 0.05, 0.69, 0.84, 0.97, 0.90],
        '$N_{\\mathrm{shots}}$': [1.86, 23.5, 8.1, 8.3, 3.3, 3.5],
    }
    
    # Plot as grouped bar chart
    x = np.arange(len(objectives))
    width = 0.2
    
    for i, (metric, vals) in enumerate(metrics.items()):
        ax.bar(x + i*width, vals, width, label=metric, alpha=0.8)
    
    ax.set_xticks(x + 1.5*width)
    ax.set_xticklabels(objectives, rotation=45, ha='right')
    ax.set_ylabel('Normalized value')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_title('Objective comparison on $n=8$ path graph')
    
    plt.savefig(OUT / 'fig10_objective_comparison.pdf')
    plt.close()

def main():
    data = load_experimental_data()
    
    print("Generating figures...")
    fig_haar_scaling(data)
    print("  fig3_haar_scaling.pdf done")
    
    fig_variational_p_success(data)
    print("  fig4_variational_p_success.pdf done")
    
    fig_boson_vs_dist()
    print("  fig6_boson_vs_dist.pdf done")
    
    fig_equal_budget()
    print("  fig7_equal_budget.pdf done")
    
    fig_objective_comparison()
    print("  fig10_objective_comparison.pdf done")
    
    print(f"\nAll figures saved to {OUT}")

if __name__ == '__main__':
    main()
