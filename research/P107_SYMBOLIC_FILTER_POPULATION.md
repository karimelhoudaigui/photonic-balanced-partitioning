# P107 exact finite-filter discriminator — CODE ONLY

P101 was read in full at69e4a6fe434a677acfc5a7e616471990b16db86b (113 lines), SHA25665e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c. No source/card here has been imported, AST-parsed, evaluated or run. Shell text reads, hashes, line counts and Git are metadata work. No scientific package, RNG, graph draw, native call or probability calibration was used to author it. The three new files must freeze before FULL ROOT+P94 review and separate authorization.

## Exact target and two constructions

Signal modes/source columns are0..3, known CF input has one photon per column; vacuum environment and all lower totals/collisions remain. F_jr=(-i)^(jr)/2. N_jk=sum_r(-i)^((j-k)r)lambda_r with lambda=(1,x,xy,y), T=N/4. All polynomial coefficients are integer Gaussian pairs; variables are REAL formal x,y,z. No floating complex arithmetic.
PGF numerator M_ij=16delta_ij−sum_a conjugate(N_ai)N_aj+sum_a z_a conjugate(N_ai)N_aj. B=per(M)/16^4; D=product diagonal(M)/16^4. Independent B uses all input subsets, repeated-row permanents, squared modulus and a single product r_j! divisor, followed by full multivariate binomial inversion. Exact coefficient divisibility is asserted; no helper/producer import. Shared primitive Gaussian arithmetic/permutation loops are disclosed, so this is an independent mathematical representation, not an independent library implementation.
All occupations total0..4 are generated densely:70. For each occupation emit ALL i,j0..8, hence5670 coefficient records; no sparse-output selection. Degree caps x/y<=8, signal<=4, matrix size<=4, permutations<=24. Static support bound for the target PGF is81*70=5670 monomials; CPU feasibility is prospective, not measured. First cap failure is inconclusive, never a request to retune silently.

## Registered literal qualifications inside the ONE future bounded run

| Fixture | m,K | exact transfer | required law |
|---|---|---|---|
| vacuum |1,0|empty occupied columns|certain vacuum,B=D|
| unary |1,1|1/2|vac3/4,one1/4,B=D|
| identity2 |2,2|I2|only(1,1),B=D|
| rotation2 |2,2|[[3,4],[-4,3]]/5|B20=B02=288/625,B11=49/625;D20=D02=144/625,D11=337/625|
| rankone2 |2,2|all1/2|Bvac1/2,singles0,B20=B02=1/8,B11=1/4;Dvac1/4,eachsingle1/4,D20=D02=1/16,D11=1/8|

Every raw state is emitted, including the fixture zeros:21 fixture records. Four decoder hands:vacuum/all-ones mean8/3 under both; (2,1,1,0) PNR5/2/threshold8/3; (1,2,1,0) PNR3/threshold8/3. Three independent Bernstein hands check constant1, x+y (coefficients(i+j)/8), x^8y^8 (only index8,8 is1). These are predata rational predictions, not measured passes.
Target endpoints: x=y=1 has only(1,1,1,1); x=y=0 has T=J/4 and B total-N law(15/32,1/4,3/16,0,3/32), followed by multinomial(N;1/4). D has Binomial(4,1/4) survival followed by the same multinomial. All70 states at BOTH endpoints are emitted and checked,140 rows. No16-photon/dilation/native enumeration occurs.

## Decoders, means and independent sign status

The graph has scaled weights2 on{0,2} and{1,3},1 on all other edges, cut divided by2; its balanced costs are2 or3. PNR ranks counts then each of24 equally weighted tie permutations. Threshold with>=2 clicks chooses all2-subsets uniformly, one click adds a uniform other vertex, and no clicks chooses uniformly among6. These are exact expected scores, not one physically scored partition or a best-of-run record. All140 occupation/decoder means are cached once, archived and charged to the worker; every control receives the same frozen information.
Each decoder has81 dense B/D/difference mean coefficients,162 rows. ALL25 rational grid pairs x,y in{0,1/4,1/2,3/4,1} emit both70-bin probability lists and both means; normalization/positivity and mean-vs-direct-sum gates are exact. Grid negativity is retained even while later registered boxes continue.
For EACH decoder all boxes at levels0,1,2 are processed:1+4+16=21, total42; ALL81 degree(8,8) Bernstein coefficients per box are emitted,3402 rows. No adaptive refinement or early successful stop. For box[a,a+w]×[b,b+w], univariate transform S_ik=sum_(r<=min(i,k)) binom(k,r)a^(k-r)w^r binom(i,r)/binom(8,r); tensoring S gives the coefficients. At9 local nodes{0,1/2,1}², compare exact Bernstein evaluation to direct power evaluation before accepting the box.
Nonnegative coefficients on EVERY box of ONE WHOLE level certify the square for that decoder. A negative Bernstein coefficient proves nothing by itself. Any negative grid value is COUNTEREXAMPLE_TO_SQUARE_ONLY; otherwise without a complete level, INCONCLUSIVE. A simultaneous grid-negative/whole-level-positive observation is an ENGINE failure. ENGINE_PASS is independent of whether a sign certificate succeeds.
The physical family lies on0<y<x<1 with y=x^(2+sqrt(3)); a square certificate covers it, while an off-curve negative grid point does NOT refute the physical-beta claim. A nonnegative square certificate would concern this fixed graph/decoder mean against same-parameter D only; it implies no best-of-T, first-hitting, paid-budget or other-graph conclusion. The three-cut classical optimizer obstruction remains.

## Raw schema, closure and caps

Coefficient record:kind=coefficient,occupation[4],powers[i,j],denominator65536,B/D/B_minus_D/B_moment each=[real_integer,imag_integer] NUMERATOR. Divide by denominator for the coefficient; nominal imaginary entries must be zero. Ordering is total0..4,recursive first coordinate ascending,then i0..8/j0..8. Every zero/negative value is retained; observed coefficients precede assertions. P110 may use this frozen schema for a separate fixed-point comparison after producer raw seal, never moving source/results.
Hand record total9612:1 provenance+21 fixtures+4 decoder hands+3 Bernstein hands+1 family matrix+5670 coefficient+1 normalization+140 decoder cost+162 mean coefficient+140 endpoint+25 grid+3402 Bernstein coefficient+42 box. Registered tasks78:5 fixtures,decoder-hand,Bernstein-hand,symbolic,2 endpoints,25 grids,42 boxes,classification. No retries/seed changes/alternative models. All computations are deterministic exact arithmetic; RNG/native calls0.
Persistent Python3.11.15,-B,six env thread variables1,one worker,CPU60/wall90. Hard/soft FSIZE4MiB and source science aggregate4MiB/reserve64KiB; runner logs4MiB separately. Fresh parent research/P107_symbolic_filter_main/run_001 with exclusive data child. Errors retain coefficient/box prefixes, failed task, NOT_RUN registry and traceback; hard interruptions may leave missing finals and remain inconclusive. No RSS/affinity claim or measured-runtime assertion.
The passive TEMPLATE supplies the source closure but cannot launch itself. P101 bytes exist in ROOT, not necessarily this checkout; do not copy/guess input hashes. ROOT must integrate frozen bytes and create a separate active v2 binding with ROOT_AUTHORIZED,run_authorized=true, actual source SHA and every actual regular nonsymlink descriptor plus binding self-input without selfhash. The script verifies all hashes/sizes and P101's exact frozen SHA BEFORE work. No authorization carries over from an earlier experiment.
No graph-optimizer performance, novelty, hardware access or paper/QPU gate is claimed. Passing internal hands or a finite sign certificate does not authorize another case, native call, dataset, publication or rerun. Seal the entire raw directory before interpretation; then inspect actual manifest/status/counts/errors. P33/P37/E05b, P98 and all negatives remain unchanged.
