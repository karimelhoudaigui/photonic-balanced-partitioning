"""Render exact P37 root brackets; no new scientific experiments."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def render(raw_path, output):
    output.mkdir(parents=True, exist_ok=False)
    raw = json.loads(raw_path.read_text())
    def midpoint(row):
        def value(x):
            return Fraction(int(x['numerator']), int(x['denominator']))
        return float((value(row['scaled_loss_low'])+value(row['scaled_loss_high']))/2)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    series = [('per_attempt',1,'Per attempt, N=m−1 ↔ m',1),
              ('per_photon',3,'Per photon, N=m−3 ↔ m−2',1),
              ('per_photon',2,'Per photon, N=m−2 ↔ m−1',2),
              ('per_photon',1,'Per photon, N=m−1 ↔ m',3)]
    for criterion, deficit, label, limit in series:
        points = [r for r in raw['transitions'] if r['criterion']==criterion and r['m']-r['source']==deficit]
        line, = axes[0].plot([r['m'] for r in points], [midpoint(r) for r in points], 'o-', label=label, markersize=4)
        axes[0].axhline(limit, color=line.get_color(), linestyle=':', alpha=.4)
    axes[0].set(xlabel='Number of modes m', ylabel='Critical scaled loss m(1−η)',
                title='Exact rational root brackets (display midpoints)')
    axes[0].legend(fontsize=7, loc='lower right')
    selected = [r for r in raw['transitions'] if r['m']==64]
    a = midpoint(selected[0])
    t = [midpoint(r) for r in selected[1:]]
    axes[1].step([0, a, 4], [1,0,0], where='post', label='Per attempt')
    axes[1].step([0, *t, 4], [3,2,1,0,0], where='post', label='Per injected photon')
    axes[1].set(xlabel='Scaled loss λ=64(1−η)', ylabel='Optimal source deficit m−N',
                yticks=[0,1,2,3], xlim=(0,4), title='Finite source phase diagram, m=64')
    axes[1].legend(fontsize=8)
    axes[1].text(.5, -.26, 'Adjacent choices tie at each threshold. At η=1, per-attempt N=m−2 also ties.',
                 transform=axes[1].transAxes, ha='center', fontsize=7)
    fig.suptitle('Haar-averaged feasibility: exactly m/2 clicks, all attempts counted', fontsize=12)
    for ax in axes:
        ax.grid(alpha=.2)
    outputs=[]
    for extension in ('png','pdf'):
        path=output/('loss_source_phase.'+extension)
        fig.savefig(path,dpi=180)
        outputs.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    plt.close(fig)
    receipt={'generated_at':datetime.now(timezone.utc).isoformat(),
             'raw_path':str(raw_path),'raw_sha256':hashlib.sha256(raw_path.read_bytes()).hexdigest(),
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'matplotlib_version':matplotlib.__version__,'outputs':outputs,
             'caveats':['Phase curves follow the self-reviewed finite theorem and exact root brackets, not new simulations.',
                        'At eta=1 per-attempt N=m-2 also ties; at each interior threshold adjacent choices tie.',
                        'No graph-quality or quantum-advantage inference.']}
    (output/'render_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--raw',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    render(args.raw,args.output)
