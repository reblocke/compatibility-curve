# Scientific Scope

## Focused question

Which candidate effect sizes are more or less compatible with an observed estimate and reported
two-sided 95% confidence interval under a one-parameter Wald approximation?

The app is an educational and research-facing method tool for readers reconstructing uncertainty
from published aggregate estimates. It is not a clinical calculator, diagnostic system,
regulated device, or decision-support tool.

## Candidate-effect interpretation

For each candidate effect value, the app evaluates the standardized distance from the
CI-implied estimate using the reconstructed working-scale standard error. It displays the
corresponding two-sided Wald p-value as compatibility.

A higher curve value means the candidate is closer to the observed estimate in reconstructed
standard-error units and is therefore more compatible with the observed data under this model.
It does not mean the candidate has a higher probability of being true.

In this app, “confidence curve” and “compatibility curve” refer to the same two-sided p-value
function. The set of candidate values with compatibility at least `0.05` corresponds to the
reconstructed 95% Wald interval. The displayed 90%, 95%, and 99% guides are the compatibility
levels `0.10`, `0.05`, and `0.01`; they are presentation references, not decision thresholds.

## Inputs

- **Effect measure:** one of odds ratio, risk ratio, hazard ratio, incidence rate ratio, ratio of
  means, mean difference, risk difference, rate difference, or regression coefficient.
- **Point estimate:** optional finite natural/display-scale number. If supplied, it is checked
  for consistency with the CI reconstruction but does not replace the working-scale midpoint.
- **Lower and upper 95% CI:** required finite numbers with lower less than upper. Ratio-scale
  values must be strictly positive.
- **Null value:** optional finite number, defaulting to `1` for ratio effects and `0` for
  additive effects. Ratio nulls must be positive.
- **Reference thresholds/MCIDs:** zero or more finite natural/display-scale values. Ratio values
  must be positive. The app treats them only as user-supplied candidates.
- **Plausible display range:** optional paired lower/upper values. It changes only the displayed
  and exported grid.
- **Advanced display controls:** ratio-axis visual spacing, an odd grid size from 101 to 1601,
  and guide visibility.

These inputs are intended to be aggregate published or synthetic method values. The app has no
need for identifiers or patient-level data.

## Outputs

The primary output is a single compatibility curve on the natural/display effect scale. Textual
and tabular outputs give:

- the CI-implied estimate on display and working scales;
- the reconstructed working-scale SE and reconstruction diagnostics;
- the reported 95% CI and null;
- standardized distance and compatibility at the null;
- for each threshold, its natural and working values, standardized distance, compatibility,
  direction relative to estimate and null, and reported-CI inclusion;
- structured warnings about reconstruction asymmetry, excluded markers, and finite-grid
  truncation;
- presentation guides, a caption, CSV, and PNG exports.

CSV is intentionally limited to effect display value, effect working value, standardized
distance, and compatibility.

## Working scales and formula authority

Additive effects use the identity working scale. Ratio effects use the natural logarithm and
therefore require positive natural values. On the working scale, the CI midpoint determines the
estimate and the reported 95% width determines the standard error using the standard normal
`0.975` quantile. Candidate standardized distances and two-sided compatibility values are then
computed under the one-parameter Wald approximation.

All numerical primitives come from the public root API of the exact released
[`wald-inference` 0.4.2](https://github.com/reblocke/wald-inference-core/releases/tag/v0.4.2)
artifact. The app does not reimplement them. The release artifact and checksum are recorded in
`pyproject.toml`, `uv.lock`, `browser-stage.toml`, and
[Runtime dependencies](RUNTIME_DEPENDENCIES.md).

## Reconstruction assumptions

- The reported limits represent a two-sided 95% interval.
- A one-parameter Wald approximation is appropriate on the registered working scale.
- The interval limits contain enough precision for midpoint and width reconstruction.
- The reported estimate, when supplied, is compatible with the interval midpoint within the
  core's documented validation tolerance.
- The curve describes compatibility with the observed estimate under the reconstructed model; it
  is not a repeated-study design calculation.

The core may report asymmetric side-specific standard errors or related warnings when a supplied
estimate or interval is inconsistent with a simple Wald reconstruction. The app surfaces those
warnings rather than claiming false precision.

## Threshold status

A reference threshold or MCID is supplied by the user. The app does not establish its clinical,
scientific, or policy validity; choose a direction of benefit; classify a claim; or recommend an
action. “Inside reported 95% CI” is a geometric lookup, not threshold validation.

## Limitations and non-goals

- Only reported two-sided 95% intervals are accepted in version 0.1.x.
- The app does not handle exact confidence distributions, profile likelihood, Bayesian
  posterior distributions, multiparameter covariance, clustered estimates, or model-specific
  transformations beyond the registered identity/log scales.
- Rounding, asymmetric intervals, non-Wald construction, or incompatible transformations can
  make the reconstruction approximate.
- Compatibility values are not probabilities of hypotheses, effect existence, treatment
  benefit, or truth.
- A value crossing any guide does not create a binary significant/nonsignificant conclusion.
- The app does not calculate relative likelihood, S−2 support, power, detectability,
  critical-effect markers, selection probabilities, Type S/M, information multipliers, or
  precision targets.
- The app is not validated for clinical, regulatory, operational, or patient-specific decisions.
