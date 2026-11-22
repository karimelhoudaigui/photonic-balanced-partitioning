"""Warm-start a capped mathematical search, retaining every cell and its costs."""
import argparse
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.optimize import minimize


def main(previous,output):
    output.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    spec=importlib.util.spec_from_file_location('p38_effect_frozen',Path('experiments/phase3_effect_search.py'))
    core=importlib.util.module_from_spec(spec);sys.modules[spec.name]=core;spec.loader.exec_module(core)
    old=json.loads(previous.read_text());calls=0;cells=[]
    with (output/'evaluations.jsonl').open('x') as trace:
        for index,cell in enumerate(old['cells']):
            target=F(cell['target']);x=np.array(cell['best']['parameters']);best=None;before=calls
            def objective(parameters):
                nonlocal calls,best
                calls+=1
                if calls>12000:raise RuntimeError('Declared12000-call refinement cap exceeded')
                e=core.decode(parameters);eig,dom,delta=core.constraints(e)
                near=min(eig)>=-1e-8 and min(dom)>=-1e-8
                d=core.distance(e)[0] if min(eig)>=-1e-8 else None
                score=-d if d is not None else 100+1000*float(np.minimum(eig,0)@np.minimum(eig,0))
                row={'call':calls,'cell':index,'parameters':parameters.tolist(),'pinched_distance':d,'delta':delta,
                     'effect_eigenvalues':eig.tolist(),'dominance_margins':dom.tolist(),'target_residual':delta-float(target),
                     'near_feasible':bool(near),'objective':score}
                trace.write(json.dumps(row)+'\n');trace.flush()
                if near and (best is None or d-delta>best['excess']):
                    best={'parameters':parameters.copy(),'excess':d-delta,'distance':d,'delta':delta,'call':calls}
                return score
            result=minimize(objective,x,method='SLSQP',constraints=[
                {'type':'ineq','fun':lambda a:np.concatenate(core.constraints(core.decode(a))[:2])},
                {'type':'eq','fun':lambda a:core.constraints(core.decode(a))[2]-float(target)}],
                options={'maxiter':120,'ftol':1e-10,'eps':1e-7})
            certificate=core.certify(best['parameters'],target) if best else None
            cells.append({'cell':index,'target':str(target),'original_seed':cell['seed'],'calls':calls-before,
                          'previous_calls':cell['calls'],'success':bool(result.success),'message':str(result.message),
                          'iterations':int(result.nit),'parameters':result.x.tolist(),
                          'best':{**best,'parameters':best['parameters'].tolist()} if best else None,'certificate':certificate})
    certified=[c['cell'] for c in cells if c['certificate'] and c['certificate']['certified']]
    summary={'status':'EXACT_STRONGER_LEMMA_REFUTATION' if certified else 'REFINEMENT_NO_CERTIFIED_REFUTATION',
             'cells':len(cells),'new_objective_calls':calls,'previous_objective_calls':old['summary']['objective_calls'],
             'total_objective_calls':calls+old['summary']['objective_calls'],'solver_successes':sum(c['success'] for c in cells),
             'certified_counterexample_cells':certified,'max_near_feasible_excess':max(c['best']['excess'] for c in cells if c['best']),
             'physical_shots':0,'new_fock_simulations':0,'runtime_seconds':time.monotonic()-start,
             'non_claims':['No global proof or certified optimum','Not a measured-TV or algorithm benefit test']}
    (output/'raw.json').write_text(json.dumps({'summary':summary,'cells':cells},default=core.encode,separators=(',',':'))+'\n')
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--previous',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();main(a.previous,a.output)
