"""P113 prospective independent void/2110 replication; never imports P107."""
import argparse, hashlib, json, os, resource, sys, traceback
from collections import Counter
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path

CAP, RESERVE = 4194304, 65536
BASE = "research/P107_symbolic_filter_main/run_001"
OUT = "research/P113_mean_replication/run_001/data"
SEAL = "99f2d98d93f13c7fc088218bfb06ff39af4c40e9"
ROLES = {k:BASE+"/data/"+v for k,v in (("records","records.jsonl"),("summary","summary.json"),("failure","failure.json"))}
REFS = tuple(BASE+"/"+v for v in ("manifest.json","stdout.txt","stderr.txt","data/records.jsonl","data/summary.json","data/failure.json"))
STATIC = ("AGENTS.md","pyproject.toml","requirements-research-lock.txt",
 "research/P113_independent_mean_certificate.py","research/P113_POPULATION.md","research/P113_contract_TEMPLATE.json",
 "research/P101_FINITE_FILTER_ALL_OUTPUT_CARD.md","research/P107_DECODER_IDENTITIES_REVIEW.md",
 "research/P107_symbolic_filter_validation.py","research/P107_SYMBOLIC_FILTER_POPULATION.md",
 "research/P107_symbolic_filter_contract_TEMPLATE.json","research/P107_INDEPENDENT_SYMBOLIC_CODE_REVIEW.md")
PINS = {"research/P101_FINITE_FILTER_ALL_OUTPUT_CARD.md":"65e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c",
 "research/P107_DECODER_IDENTITIES_REVIEW.md":"9dca56e56c724b67493199f637094dfa59f17e2d12b1d01d93493735fbded9f9",
 "research/P107_symbolic_filter_validation.py":"4e0973ebfe8a250dbf012719087dcb0b7390932acd3ddab4e7055b3808cb2bbc"}
THREADS = ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS")
EXPECTED = {"provenance":1,"fixture":21,"decoder_hand":4,"bernstein_hand":3,"matrix":1,"coefficient":5670,"normalization":1,"decoder_cost":140,"mean_coefficient":162,"endpoint":140,"grid":25,"bernstein_coefficient":3402,"box":42}
DECODERS = ("THRESHOLD","PNR")

def insist(test,reason):
    if not test: raise ValueError(reason)
def scalar(a): return {(0,0):Q(a)} if a else {}
def plus(*items):
    result = {}
    for item in items:
        for key,value in item.items(): result[key] = result.get(key,Q(0))+value
    return {k:v for k,v in result.items() if v}
def times(p,q):
    result = {}
    for (i,j),a in p.items():
        for (k,l),b in q.items():
            insist(i+k<=8 and j+l<=8,"bidegree exceeds eight: "+repr((i,j,k,l)))
            key = i+k,j+l
            result[key] = result.get(key,Q(0))+a*b
    return {k:v for k,v in result.items() if v}
def weight(p,a): return {k:v*a for k,v in p.items() if v*a}
def real(a): return (scalar(a),{})
def zsum(items):
    items = list(items)
    return plus(*(x[0] for x in items)),plus(*(x[1] for x in items))
def zmul(a,b): return plus(times(a[0],b[0]),weight(times(a[1],b[1]),-1)),plus(times(a[0],b[1]),times(a[1],b[0]))
def star(a): return a[0],weight(a[1],-1)
def zreal(a):
    insist(not a[1],"imaginary polynomial survived: "+repr(a))
    return a[0]
def ryser(matrix):
    n = len(matrix)
    insist(n<=4 and all(len(row)==n for row in matrix),"Ryser size outside fixed scope")
    answer = real(1) if not n else real(0)
    for mask in range(1,1<<n):
        term = real((-1)**(n-mask.bit_count()))
        for row in matrix: term = zmul(term,zsum(row[j] for j in range(n) if mask>>j&1))
        answer = zsum((answer,term))
    return answer
def product(items):
    result = real(1)
    for item in items: result = zmul(result,item)
    return result
def transfer():
    a = ({(0,0):Q(1,4),(1,0):Q(1,4),(1,1):Q(1,4),(0,1):Q(1,4)}, {})
    b = ({(0,0):Q(1,4),(1,1):Q(-1,4)}, {(1,0):Q(1,4),(0,1):Q(-1,4)})
    c = ({(0,0):Q(1,4),(1,0):Q(-1,4),(1,1):Q(1,4),(0,1):Q(-1,4)}, {})
    row = (a,b,c,star(b))
    return [[row[(j-i)%4] for j in range(4)] for i in range(4)]
def void_pair(t,allowed):
    h = [[zsum([real(int(i==j))]+[(weight(v[0],-1),weight(v[1],-1)) for a in range(4) if a not in allowed for v in [zmul(star(t[a][i]),t[a][j])]]) for j in range(4)] for i in range(4)]
    return zreal(ryser(h)),zreal(product(h[i][i] for i in range(4)))
def record_probability(t,n):
    rows = [t[j] for j in range(len(n)) for unused in range(n[j])]
    denominator = 1
    for count in n: denominator *= factorial(count)
    amplitude = ryser(rows)
    intensities = [[(zreal(zmul(v,star(v))),{}) for v in row] for row in rows]
    return weight(zreal(zmul(amplitude,star(amplitude))),Q(1,denominator)),weight(zreal(ryser(intensities)),Q(1,denominator))
def at(p,x,y): return sum((a*x**i*y**j for (i,j),a in p.items()),Q(0))
def affine_then_bernstein(p,left,bottom,width):
    local = {}
    for (i,j),a in p.items():
        for r in range(i+1):
            for s in range(j+1):
                local[r,s] = local.get((r,s),Q(0))+a*comb(i,r)*comb(j,s)*left**(i-r)*bottom**(j-s)*width**(r+s)
    coefficients = {}
    for u in range(9):
        for v in range(9):
            coefficients[u,v] = sum((a*Q(comb(u,r),comb(8,r))*Q(comb(v,s),comb(8,s)) for (r,s),a in local.items() if r<=u and s<=v),Q(0))
    return coefficients
def polynomial(p): return [[i,j,a] for (i,j),a in sorted(p.items())]
def json_default(v):
    if isinstance(v,Q): return str(v)
    raise TypeError(type(v).__name__)
def safe(root,name):
    p = Path(name)
    insist(not p.is_absolute() and p.parts and p.as_posix()==name and all(v not in (".","..") for v in p.parts),"unsafe input name")
    cursor = root
    for part in p.parts:
        cursor /= part
        insist(not cursor.is_symlink(),"symlinked input")
    insist(cursor.is_file(),"input missing/not regular")
    return cursor
def hexword(value,n): return isinstance(value,str) and len(value)==n and all(c in "0123456789abcdef" for c in value)
def authorization(root,name):
    b = json.loads(safe(root,name).read_text())
    insist(b["binding_state"]=="ROOT_AUTHORIZED" and b["run_authorized"] is True,"ROOT authority absent")
    insist(hexword(b["reference_seal_commit"],40) and b["reference_seal_commit"]==SEAL and b["reference_roles"]==ROLES,"original opaque seal/roles")
    rows = b["artifacts"]
    table = {r["path"]:r for r in rows}
    refs = b["artifacts_reference"]
    insist(len(table)==len(rows) and name not in table and set(STATIC)|set(REFS)<=set(table),"required input closure")
    insist(all(p in STATIC or p in REFS or (p.startswith("research/") and p.endswith(".md") and not p.startswith(BASE+"/")) for p in table),"only extra frozen review notes")
    insist(len(refs)==6 and {r["path"] for r in refs}==set(REFS) and all(r==table[r["path"]] for r in refs),"six reference descriptors")
    insist(len(b["execution_artifacts"])==len(table)+1 and set(b["execution_artifacts"])==set(table)|{name},"binding self-input closure")
    for path,r in table.items():
        f = safe(root,path)
        insist(type(r["bytes"]) is int and r["bytes"]==f.stat().st_size and hexword(r["sha256"],64),"descriptor size/format")
        insist(path not in REFS or r["bytes"]<=CAP,"reference file cap")
        insist(hashlib.sha256(f.read_bytes()).hexdigest()==r["sha256"],"descriptor hash")
        insist(path not in PINS or r["sha256"]==PINS[path],"frozen mathematical context")
    insist(hexword(b["source_sha256"],64) and hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==b["source_sha256"]==table[STATIC[3]]["sha256"],"actual frozen source")
    return b
class Journal:
    def __init__(self,path):
        insist(path.parent.is_dir() and not path.parent.is_symlink() and not path.parent.parent.is_symlink() and not path.exists() and not path.is_symlink(),"fresh strict output child")
        path.mkdir()
        self.path,self.bytes,self.rows = path,0,0
        self.stream = (path/"records.jsonl").open("x",encoding="ascii")
    def emit(self,value):
        text = json.dumps(value,default=json_default,allow_nan=False,sort_keys=True,separators=(",",":"))+"\n"
        insist(self.bytes+len(text.encode("ascii"))<=CAP-RESERVE,"scientific aggregate reserve")
        self.stream.write(text)
        self.stream.flush()
        self.bytes += len(text.encode("ascii")); self.rows += 1
    def finish(self,summary,failure):
        self.stream.close()
        payloads = [json.dumps(v,default=json_default,allow_nan=False,sort_keys=True)+"\n" for v in (summary,failure)]
        insist(self.bytes+sum(len(v.encode("ascii")) for v in payloads)<=CAP,"scientific aggregate cap")
        for name,text in zip(("summary.json","failure.json"),payloads):
            with (self.path/name).open("x",encoding="ascii") as f: f.write(text)
def fixtures(journal):
    def check(label,actual,expected):
        journal.emit({"kind":"hand_fixture","case":label,"actual":repr(actual),"expected":repr(expected)})
        insist(actual==expected,"hand fixture "+label)
    check("empty",ryser([]),real(1))
    check("complex",ryser([[real(1),({},scalar(1))],[({},scalar(1)),real(1)]]),real(0))
    t = [[real(Q(3,5)),real(Q(4,5))],[real(Q(-4,5)),real(Q(3,5))]]
    check("rotation",[record_probability(t,n) for n in ((2,0),(1,1),(0,2))],[(scalar(Q(288,625)),scalar(Q(144,625))),(scalar(Q(49,625)),scalar(Q(337,625))),(scalar(Q(288,625)),scalar(Q(144,625)))])
    check("affine_linear",affine_then_bernstein({(0,0):Q(1),(1,0):Q(1),(0,1):Q(1)},Q(1,4),Q(1,2),Q(1,4)),{(i,j):Q(7,4)+Q(i+j,32) for i in range(9) for j in range(9)})
    check("top_basis",affine_then_bernstein({(8,8):Q(1)},Q(0),Q(0),Q(1)),{(i,j):Q(int(i==8 and j==8)) for i in range(9) for j in range(9)})
def reference(root,journal,state):
    occupations = sorted(((a,b,c,d) for a in range(5) for b in range(5) for c in range(5) for d in range(5) if a+b+c+d<=4),key=lambda n:(sum(n),n))
    counts,seen,means,bern,grids,boxes = Counter(),set(),{},{},{},{}
    with safe(root,ROLES["records"]).open(encoding="ascii") as handle:
        for line_number,line in enumerate(handle,1):
            state["reference_line"] = {"number":line_number,"bytes":len(line),"prefix":line[:8192]}
            insist(len(line)<=65536,"oversize reference record")
            r = json.loads(line); k = r["kind"]
            insist(k in EXPECTED,"unknown reference kind"); counts[k] += 1
            if k=="coefficient":
                n,e = tuple(r["occupation"]),tuple(r["powers"])
                key = (n,e)
                insist(n in occupations and e in [(i,j) for i in range(9) for j in range(9)] and key not in seen and r["denominator"]==65536,"dense coefficient metadata")
                seen.add(key)
                b,d,delta,alt = (r[v] for v in ("B","D","B_minus_D","B_moment"))
                insist(all(len(v)==2 and all(type(z) is int for z in v) for v in (b,d,delta,alt)) and b==alt and delta==[b[0]-d[0],b[1]-d[1]] and b[1]==d[1]==0,"reference internal coefficient schema")
            elif k=="mean_coefficient":
                key = r["decoder"],*r["powers"]
                insist(key not in means,"duplicate mean coefficient"); means[key] = tuple(Q(r[v]) for v in ("B","D","B_minus_D"))
            elif k=="bernstein_coefficient":
                key = r["decoder"],r["level"],*r["box"],*r["index"]
                insist(key not in bern,"duplicate Bernstein coefficient"); bern[key] = Q(r["value"])
                insist([Q(v) for v in r["lower"]]==[Q(r["box"][i],2**r["level"]) for i in (0,1)] and Q(r["width"])==Q(1,2**r["level"]),"box coordinate metadata")
            elif k=="grid":
                key = tuple(Q(v) for v in r["point"])
                insist(key not in grids and [tuple(n) for n in r["occupation_order"]]==occupations,"complete grid order")
                for label in ("B_probabilities","D_probabilities"):
                    values = list(map(Q,r[label])); insist(len(values)==70 and min(values)>=0 and sum(values)==1,"reference grid normalization")
                grids[key] = r["means"]
            elif k=="normalization":
                insist(r["denominator"]==65536 and r["B"]==r["D"]==[[[0,0],[65536,0]]],"formal normalization record")
            elif k=="box":
                key = r["decoder"],r["level"],*r["box"]
                insist(key not in boxes,"duplicate box status"); boxes[key] = r["nonnegative"]
            elif k=="provenance": insist(r["source_sha256"]==PINS["research/P107_symbolic_filter_validation.py"],"original source provenance")
    state.pop("reference_line",None)
    journal.emit({"kind":"reference_population","counts":dict(counts),"coefficient_metadata":len(seen)})
    insist(counts==Counter(EXPECTED) and len(seen)==5670 and sum(counts.values())==9612,"entire producer population")
    insist(set(means)=={(d,i,j) for d in DECODERS for i in range(9) for j in range(9)},"complete mean coefficient domain")
    expected_bern = {(d,l,i,j,u,v) for d in DECODERS for l in range(3) for i in range(2**l) for j in range(2**l) for u in range(9) for v in range(9)}
    insist(set(bern)==expected_bern and set(boxes)=={k[:4] for k in expected_bern} and set(grids)=={(Q(i,4),Q(j,4)) for i in range(5) for j in range(5)},"complete Bernstein/grid domains")
    summary = json.loads(safe(root,ROLES["summary"]).read_text())
    failure = json.loads(safe(root,ROLES["failure"]).read_text())
    journal.emit({"kind":"reference_final_state","summary":summary,"failure":failure})
    insist(failure is None and summary["ENGINE_PASS"] is True and summary["records"]==9612 and summary["FAILED_TASK"]==summary["NOT_RUN"]==[] and summary["counts"]=={"coefficients":5670,"boxes":42,"bernstein_coefficients":3402,"grid":25},"complete successful original engine")
    return means,bern,grids,boxes,summary["certificates"]
def main():
    resource.setrlimit(resource.RLIMIT_FSIZE,(CAP,CAP)); resource.setrlimit(resource.RLIMIT_CPU,(30,30))
    parser = argparse.ArgumentParser(); parser.add_argument("--binding",required=True); args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    insist(sys.version_info[:3]==(3,11,15) and all(os.environ.get(v)=="1" for v in THREADS),"Python/thread profile")
    b = authorization(root,args.binding); journal = Journal(root/OUT)
    state,done,failure,mismatches,examples,comparison_counts = {"phase":"initial"},[],None,0,[],Counter()
    def compare(key,actual,expected):
        nonlocal mismatches
        match = actual==expected
        state["last_comparison"] = {"kind":"comparison","key":key,"independent":actual,"reference":expected,"match":match}
        journal.emit(state["last_comparison"])
        comparison_counts[key[0]] += 1
        if not match:
            mismatches += 1
            if len(examples)<8: examples.append(key)
    try:
        journal.emit({"kind":"provenance","source_sha256":b["source_sha256"],"reference_seal":SEAL,"reference_artifacts":b["artifacts_reference"],"binding":args.binding,"binding_sha256":hashlib.sha256(safe(root,args.binding).read_bytes()).hexdigest(),"Python":sys.version,"environment":{v:os.environ.get(v) for v in THREADS}})
        state["phase"] = "five hands"; fixtures(journal); done.append("hands")
        state["phase"] = "independent void/2110 construction"
        t = transfer()
        journal.emit({"kind":"matrix","T":[[[polynomial(v[0]),polynomial(v[1])] for v in row] for row in t]})
        parts = {"VA":void_pair(t,{0,1}),"VO":void_pair(t,{0,2}),"qA":record_probability(t,(2,0,1,1)),"qO":record_probability(t,(2,1,0,1))}
        for label,values in parts.items():
            for i in range(9):
                for j in range(9): journal.emit({"kind":"component","name":label,"powers":[i,j],"B":values[0].get((i,j),Q(0)),"D":values[1].get((i,j),Q(0))})
        mean = {"THRESHOLD":[plus(scalar(Q(8,3)),weight(plus(parts["VA"][a],weight(parts["VO"][a],-1)),Q(4,3))) for a in (0,1)]}
        mean["PNR"] = [plus(mean["THRESHOLD"][a],weight(plus(parts["qO"][a],weight(parts["qA"][a],-1)),Q(4,3))) for a in (0,1)]
        delta = {d:plus(mean[d][0],weight(mean[d][1],-1)) for d in DECODERS}
        for d in DECODERS:
            for i in range(9):
                for j in range(9): journal.emit({"kind":"independent_mean","decoder":d,"powers":[i,j],"B":mean[d][0].get((i,j),Q(0)),"D":mean[d][1].get((i,j),Q(0)),"difference":delta[d].get((i,j),Q(0))})
        insist(all(at(delta[d],Q(e),Q(e))==0 and delta[d]=={(j,i):a for (i,j),a in delta[d].items()} for d in DECODERS for e in (0,1)),"endpoint/x-y identities")
        done.append("means"); own = {}
        state["phase"] = "independent two-step Bernstein"
        for d in DECODERS:
            for level in range(3):
                for i in range(2**level):
                    for j in range(2**level):
                        state["box"] = [d,level,i,j]
                        coeff = affine_then_bernstein(delta[d],Q(i,2**level),Q(j,2**level),Q(1,2**level))
                        for (u,v),value in coeff.items():
                            key = d,level,i,j,u,v; own[key] = value
                            journal.emit({"kind":"independent_bernstein","key":key,"value":value})
        state.pop("box",None); done.append("Bernstein")
        state["phase"] = "authorized original reference parsing"
        reference_means,reference_bern,grids,boxes,certificates = reference(root,journal,state); done.append("reference_complete")
        state["phase"] = "all exact coefficient comparisons"
        for key,expected in reference_means.items():
            d,i,j = key
            compare(["mean",*key],tuple(p.get((i,j),Q(0)) for p in (*mean[d],delta[d])),expected)
        for key,value in own.items(): compare(["Bernstein",*key],value,reference_bern[key])
        done.append("all_coefficients"); derived = {}; state["phase"] = "grid/box/certificate statuses"
        for d in DECODERS:
            negative,full = [],[]
            for i in range(5):
                for j in range(5):
                    x,y = Q(i,4),Q(j,4)
                    actual = tuple(at(p,x,y) for p in (*mean[d],delta[d]))
                    compare(["grid",d,i,j],actual,tuple(Q(grids[x,y][d][v]) for v in ("B","D","B_minus_D")))
                    if actual[2]<0: negative.append([str(x),str(y),str(actual[2])])
            for level in range(3):
                flags = []
                for i in range(2**level):
                    for j in range(2**level):
                        flag = all(own[d,level,i,j,u,v]>=0 for u in range(9) for v in range(9)); flags.append(flag)
                        compare(["box_status",d,level,i,j],flag,boxes[d,level,i,j])
                if all(flags): full.append(level)
            insist(not (negative and full),"independent sign contradiction")
            derived[d] = {"status":"COUNTEREXAMPLE_TO_SQUARE_ONLY" if negative else ("NONNEGATIVE_ON_WHOLE_SQUARE" if full else "INCONCLUSIVE"),"whole_levels":full,"negative_grid_points":negative,"physical_beta_curve_decided_by_negative_grid":False}
            compare(["certificate_status",d],derived[d],certificates[d])
        insist(comparison_counts==Counter({"mean":162,"Bernstein":3402,"grid":50,"box_status":42,"certificate_status":2}) and journal.rows==7555,"entire independent comparison population")
        done.append("all_statuses")
    except Exception as exc: failure = {"state":state,"exception":repr(exc),"traceback":traceback.format_exc()}
    status = "INCONCLUSIVE" if failure else ("COMPARE_FAILED" if mismatches else "COMPARE_PASS")
    summary = {"status":status,"completed":done,"NOT_RUN":[v for v in ("hands","means","Bernstein","reference_complete","all_coefficients","all_statuses") if v not in done],"comparisons":dict(comparison_counts),"mismatches":mismatches,"examples":examples,"records":journal.rows,"certificate":derived if status=="COMPARE_PASS" else "NOT_ACCEPTED","full_count_law_independently_recomputed":False,"optimizer_advantage":False,"native_calls":0,"RNG_draws":0}
    journal.finish(summary,failure)
    if status!="COMPARE_PASS": raise SystemExit(1)
if __name__=="__main__": main()
