# P33 numerical refinement and command failure preservation

The exact theorem at checkpoint `75e5831` passed independent proof review.
The review also found a genuine floating-point limitation outside the original
finite grid: at angle 1e-10, subtracting nearly equal intensities produced zero
collision/leakage estimates while the exact two-photon TV is about 2e-20.
The original source, witness and first simulation are retained, not overwritten.

The revised evaluator computes expected collision pairs and dominant-support
leakage as sums of nonnegative terms. A positive derangement series with an
explicit exact-series remainder avoids small-argument exp/log cancellation.
A regression test exercises the discovered angle. These changes preserve the
mathematical definitions and the preregistered case grid.

The returned values remain **float64 estimates**, not interval-certified upper
bounds. The input orthonormality residual and the cancellation-prone subtraction
values are recorded. Numerical tests use stated tolerances. The proof is exact;
an experimental or bit-rigorous confidence certificate needs a separate error
budget and is not claimed here.

The first native seven-role cycle is preserved at branch commit `272c3fd`, with
its primary data and failed replication manifest. The latter failed because the
model dropped --output while transcribing a long command. A short, fixed
`scripts/qwen_density_job.py` entry point now assembles and records every
scientific argument, audits actual raw files, and mechanically writes the finite
evidence report. No interpreter-generated narrative can open a scientific gate.

The corrected implementation and workflow pass 261 current working-tree tests.
The next native cycle must actually execute both primary and fresh-seed jobs
before replication is accepted. Paper and QPU remain closed; novelty remains OPEN.
