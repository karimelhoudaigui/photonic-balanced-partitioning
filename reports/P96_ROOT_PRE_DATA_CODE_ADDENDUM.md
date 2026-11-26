# P96 ROOT predata addendum: rejected observations preserved

Read the complete76-insertion/18-deletion diff of original0eabdadc70c2b7085c40b22183320e8655d00e1d,
parentac67650, after the prior full550-line read. All five affected files
are covered; nominal physics/population/tolerances/resource caps are unchanged.
The new source has366lines, tests134/11 functions, contracts37+24/population47.
Source SHAee3592ef608b0b7ad19ba81babcdc369bf4da50e319f3f00baf868074d83c223;
tests SHAa5b7d94dcf9b202fc30309e57e63227700a1c65c5964140e4334535560a45c1a.
All8 static and8 critical external hashes were verified without executing
scientific code; predata_metadata_v2.json preserves this exact new closure.
Original metadata/reviews and old source remain in Git. Neither old nor
new source has been imported, collected, qualified or run at this checkpoint.

P62's165-line exact-old-freeze review45d73ccf was fully read and preserved.
It identifies E1: failed nonfinite/native-thread/construction observations
could be omitted. The present diff fixes those native rejection paths:

- Nonfinite floats become explicit strict-JSON diagnostic objects, then
  finite guards reject them after the raw row is emitted. They cannot be
  valid numeric PASS observations.
- Raw backend return repr is reset per point, then saved BEFORE conversion
  and the finally thread check. A post-call drift therefore preserves the
  returned observation in failure.prefix even if native_raw is unreachable.
- Thread failures carry their actual native and six environment values.
- Root operands, spectra/eigenvectors, U and both Grams/residuals are emitted
  BEFORE their finite/positive/unitarity rejection checks. Nothing is clipped.

Two added pure tests exercise strict serialization through Evidence and
record actual drift using a fake configuration; neither imports a native
library. Synthetic outputs are represented in JUnit, never physical data.
Thus prospective qualification changes9->11 before any execution, while
167 exact bins/159 native amplitudes/28 marginals stay fixed.
An exact-algebra assertion before returning audit still preserves T/start/
traceback rather than every derived coefficient; the independent review
states that diagnostic limit, and no unavailable calculation is invented.

ROOT finds E1's native-observation loss addressed and no new nominal blocker.
This addendum is a static review, not a passed test or execution authority.
Read P62's independent exact-new-diff addendum before separately authorizing
ONE11-test pure qualification. Seal raw before reading, then separate receipt;
only afterward bind/authorize native main. New code remains local until the
full existing suite passes. paper/, main and QPU remain frozen.
