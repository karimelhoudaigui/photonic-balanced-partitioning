"""Self-review of float semantics; exact rational underflow witness, not new physics."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path
import numpy as np
from photonic_balanced_partitioning.photonic.density_certificate import density_certificate, cycle_envelope


def main(output):
    # Exact orthogonal two-column rotation, padded with two exactly zero rows.
    # Every nonzero row has intensity exactly one. No tiny row is discarded.
    t=Fraction(1,2**600)
    cosine=(1-t*t)/(1+t*t);sine=2*t/(1+t*t)
    assert cosine*cosine+sine*sine==1
    exact_tv=2*cosine*cosine*sine*sine
    frame=np.zeros((4,2),complex)
    frame[:2]=[[float(cosine),-float(sine)],[float(sine),float(cosine)]]
    observed=density_certificate(frame)
    assert exact_tv>0 and observed['expected_collision_pairs']==0
    assert observed['refined_density_cycle_tv_bound']==0
    assert observed['numerical_semantics']=='FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED'
    envelope=[]
    with localcontext() as context:
        context.prec=90
        for value in ['1e-20','1e-10','.01','.099','.1','.2','.5','.99']:
            x=Decimal.from_float(float(value))
            reference=min(Decimal(1),(((-x).exp()/(1-x))-1)/2)
            estimate=cycle_envelope(float(value))
            envelope.append({'sigma_input':value,'float_estimate':estimate,
                'decimal_90_digit_reference_at_float_input':str(reference),
                'float_minus_reference':str(Decimal.from_float(estimate)-reference)})
    result={'assertion_tested':'Floating estimates are not rigorous numerical upper bounds; exact rational underflow witness.',
        'review_provenance':'COORDINATOR_SELF_REVIEW; the separately requested fresh agent was quota blocked',
        'underflow_witness':{'m':4,'k':2,'rotation_t':'1/2^600','exact_positive_row_intensity':1,
            'exact_full_law_tv_numerator':str(exact_tv.numerator),
            'exact_full_law_tv_denominator':str(exact_tv.denominator),
            'float_frame':frame.real.tolist(),'observed':observed},
        'envelope_roundoff_cases':envelope,'physical_shots':0,
        'interpretation':'Confirms the explicit floating limitation. Does not refute the exact theorem or imply a material failure at the preregistered grid scale.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as stream:json.dump(result,stream,indent=2)
    print(json.dumps({'underflow_witness_verified':True,'exact_tv_positive':True,
                      'returned_estimate':0,'theorem_refuted':False,'physical_shots':0}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
