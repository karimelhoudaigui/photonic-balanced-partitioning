#!/usr/bin/env python3
"""Falsify shallow-mesh enrichment by changing vertex labels alone."""
import argparse
from itertools import permutations
import json
from pathlib import Path
import numpy as np
from run_research import graph, optimize, save, clean
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh
from photonic_balanced_partitioning.photonic.comparison import CollisionFreeEvaluator


def structural_support(mesh,k):
    support=np.eye(mesh.n,dtype=bool)[:,:k]
    for a,b in mesh.pairs:
        union=support[a] | support[b]
        support[a]=union;support[b]=union
    return support


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    if any(p.name not in ['stdout.txt','stderr.txt'] for p in args.output.iterdir()):parser.error('Refusing overwrite')
    n=6;ev=CollisionFreeEvaluator(n);rows=[]
    with (args.output/'runs.jsonl').open('w') as raw:
        for family in ['path','cycle','regular','erdos_renyi','weighted','planted']:
            for instance in range(2):
                graph_seed=20261120+10000*n+instance
                g=graph(n,family,graph_seed)
                for label in range(5):
                    perm=(np.arange(n) if label==0 else np.random.default_rng(graph_seed+99000+label).permutation(n))
                    edges=[(int(perm[i]),int(perm[j]),w) for i,j,w in g.edges]
                    costs=ev.energies(edges);optimum=float(costs.min())
                    assert abs(optimum-min(ev.energies(g.edges)))<1e-10
                    seed=20261120+100000*n+1000*instance
                    for depth in [2,6]:
                        mesh=RectangularMesh(n,depth)
                        structural=structural_support(mesh,n//2)
                        reachable=np.array([any(all(structural[S[a],p[a]] for a in range(n//2))
                                           for p in permutations(range(n//2))) for S in ev.partitions])
                        accessible_optimum=bool(np.any(reachable & np.isclose(costs,optimum,atol=1e-9,rtol=0)))
                        initial=np.random.default_rng(seed+mesh.num_parameters).uniform(-np.pi,np.pi,mesh.num_parameters)
                        for model in ['bosonic','distinguishable']:
                            fitted=optimize(ev,costs,mesh,initial,model,'success',120,seed+77)
                            if not accessible_optimum:assert fitted['after']['p_success']<1e-10
                            record=dict(n=n,family=family,instance=instance,graph_seed=graph_seed,seed=seed,
                                label_index=label,vertex_map=perm.tolist(),edges=edges,depth=depth,model=model,
                                structural_reachable_cf=int(reachable.sum()),any_optimum_reachable=accessible_optimum,
                                optimum=optimum,**fitted)
                            raw.write(json.dumps(clean(record),allow_nan=False)+'\n');raw.flush()
                            rows.append({k:v for k,v in record.items() if k not in ['trace','parameters','edges','best_unitary_real','best_unitary_imag']})
            print(f'label control {family}: {len(rows)} runs',flush=True)
    groups=[]
    for model in ['bosonic','distinguishable']:
        for depth in [2,6]:
            for original in [True,False]:
                subset=[r for r in rows if r['model']==model and r['depth']==depth and (r['label_index']==0)==original]
                groups.append(dict(model=model,depth=depth,labeling='original' if original else 'random_permutation',
                    runs=len(subset),mean_p_success=float(np.mean([r['after']['p_success'] for r in subset])),
                    structurally_inaccessible_optimum_runs=sum(not r['any_optimum_reachable'] for r in subset)))
    save(args.output/'summary.json',dict(experiment='E09 label/reachability falsification',n=6,
        graph_slots=12,labelings_per_slot=5,optimizer='COBYLA',objective='success oracle diagnostic',
        budget=120,physical_shots=0,model_runs=len(rows),
        note='Same underlying weighted graphs and same initial circuit across relabelings; descriptive fixed-grid comparison',results=groups))


if __name__=='__main__': main()
