#!/usr/bin/env python3
"""Small preregistered local Qwen mission; fixed costs, no hardware or tuning."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
import numpy as np
from scipy.optimize import minimize
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
from photonic_balanced_partitioning.photonic.comparison import CollisionFreeEvaluator, cf_metrics
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    ev=CollisionFreeEvaluator(4);mesh=RectangularMesh(4);base=FixedPhotonObliq(4)
    graphs={'path':[(0,1,1.),(1,2,1.),(2,3,1.)],
            'cycle':[(0,1,1.),(1,2,1.),(2,3,1.),(3,0,1.)],
            'weighted':[(0,1,.7),(0,2,1.2),(1,3,.9),(2,3,1.6)]}
    rows=[];start=time.monotonic()
    for family,edges in graphs.items():
        costs=ev.energies(edges);optimum=float(costs.min())
        for seed in [20261121,20261122,20261123]:
            initial=np.random.default_rng(seed).uniform(-np.pi,np.pi,mesh.num_parameters-4)
            for model in ['bosonic','distinguishable']:
                history=[];best=[float('inf'),None,None]
                def objective(theta):
                    p=ev.probabilities(mesh.unitary(np.r_[theta,np.zeros(4)]),model)
                    metrics=cf_metrics(p,costs,optimum)
                    value=(metrics['conditional_energy']+2*(1-metrics['p_cf'])
                           if metrics['conditional_energy'] is not None else 1e6)
                    history.append(dict(parameters=theta.tolist(),loss=value,metrics=metrics))
                    if value<best[0]:best[:]=[value,theta.copy(),metrics]
                    return value
                minimize(objective,initial,method='COBYLA',options={'maxiter':32,'rhobeg':.35})
                rows.append(dict(family=family,seed=seed,model=model,edges=edges,
                    objective='conditional energy + 2*(1-P_CF), no optimum in loss',
                    optimum_diagnostic=optimum,n_evaluations=len(history),
                    initial=history[0]['metrics'],final=best[2],history=history,
                    uniform_feasible_success=float(np.isclose(costs,optimum,atol=1e-9,rtol=0).mean())))
    hom=np.eye(4,dtype=complex);hom[:2,:2]=np.array([[1.,-1.],[1.,1.]])/np.sqrt(2)
    hom_pcf=base.measure_collision_free_probability(hom)
    assert hom_pcf<1e-12
    result={'question':'Does this bounded optimum-blind n4 protocol establish a useful interference-dependent mechanism?',
            'status':'INCONCLUSIVE','scope':'3 fixed graphs x 3 seeds x 2 statistics; maximum32 exact objective calls each',
            'hypothesis':'A positive claim must survive reoptimized distinguishable and feasible classical controls',
            'non_claims':['No population significance','No QPU or noise evidence','No computational advantage inferred from final sampler enrichment'],
            'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'numpy_version':np.__version__,'runtime_seconds':time.monotonic()-start,
            'physical_shots':0,'hom_p_cf':hom_pcf,'rows':rows}
    (args.output/'raw.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'runs':len(rows),'evaluations':sum(r['n_evaluations'] for r in rows),
                      'hom_p_cf':hom_pcf,'output':str(args.output/'raw.json')}))


if __name__=='__main__':main()
