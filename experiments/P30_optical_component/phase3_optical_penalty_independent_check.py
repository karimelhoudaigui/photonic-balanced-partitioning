"""Reproduce the independent finite physics review, from phase3-physics root."""
import hashlib,json,math
from itertools import permutations
from pathlib import Path
import numpy as np
from photonic_balanced_partitioning.photonic.optical_penalty import OpticalPenaltyAnchor

module=Path('src/photonic_balanced_partitioning/photonic/optical_penalty.py')
before=hashlib.sha256(module.read_bytes()).hexdigest()
rows=[]
for m,source in [(3,(1,1,1)),(3,(2,0,2)),(4,(2,1,1,1))]:
    rng=np.random.default_rng(683100+m+sum(source))
    q=rng.uniform(-3,2,(m,m));q=(q+q.T)/2
    order=tuple(reversed(tuple((i,j) for i in range(m) for j in range(i+1,m))))
    anchor=OpticalPenaltyAnchor(q,2,'literal_archive',pair_order=order)
    u=anchor.unitary();actual=anchor.fock_probabilities(source)
    columns=[i for i,count in enumerate(source) for _ in range(count)]
    routing=list(permutations(range(sum(source))))
    errors=[]
    for state,p in actual.items():
        indices=[i for i,count in enumerate(state) for _ in range(count)]
        sub=u[np.ix_(indices,columns)]
        permanent=sum(math.prod(sub[j,pi[j]] for j in range(len(pi))) for pi in routing)
        norm=math.prod(math.factorial(c) for c in source+state)
        reference=abs(permanent)**2/norm
        errors.append(abs(p-reference))
    rows.append(dict(m=m,source=source,full_fock_outcomes=len(actual),max_independent_probability_error=max(errors),raw_norm=sum(actual.values())))
    assert max(errors)<1e-11 and abs(sum(actual.values())-1)<1e-11
assert before==hashlib.sha256(module.read_bytes()).hexdigest()
result=dict(source_sha256=before,checks=rows,method='Explicit repeated-column/row permutation permanent, including factorials; independent of creation recurrence.',seeds='683100+m+sum(source)',status='PASS')
serialized=json.dumps(result,indent=2)+'\n'
Path('/private/tmp/phase3_optical_penalty_independent_receipt.json').write_text(serialized)
print(serialized)
print('receipt_sha256',hashlib.sha256(serialized.encode()).hexdigest())
