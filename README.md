# Wald Compatibility Curve

[![CI](https://github.com/reblocke/compatibility-curve/actions/workflows/ci.yml/badge.svg)](https://github.com/reblocke/compatibility-curve/actions/workflows/ci.yml)

Which candidate effect sizes are more or less compatible with an observed estimate and reported
95% confidence interval under a one-parameter Wald approximation?

This repository provides a focused, static browser app for that question. It reconstructs a
compatibility/confidence curve, marks the CI-implied estimate, null, reported interval, and
user-supplied reference thresholds, and exports the displayed curve. The intended Pages URL is
[https://reblocke.github.io/compatibility-curve/](https://reblocke.github.io/compatibility-curve/).

The app does not calculate an exact profile likelihood, power, critical effects, Type S/M error,
or required precision. It does not validate an MCID, turn a result into a binary
“significant/not significant” label, estimate the probability that a candidate effect is true,
or provide clinical decision support.

Public engineering, scientific-boundary, and accessibility reports use the scoped issue forms in
`.github/`. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md); never put
protected health information, credentials, restricted data, or sensitive values in a public
report. Contribution and release requirements are documented in
[CONTRIBUTING.md](CONTRIBUTING.md).

> **Release metadata:** Current app version: `0.1.3`.
> Release maturity: experimental software. GitHub publication state is recorded on the versioned release page:
> <https://github.com/reblocke/compatibility-curve/releases/tag/v0.1.3>.
> Cite the exact tagged software release or commit used; see [CITATION.cff](CITATION.cff).

## Interpretation

On the effect measure's working scale, the released `wald-inference` core reconstructs

```text
estimate = midpoint of the reported 95% CI
SE = CI width / (2 × z0.975)
standardized distance(candidate) = (candidate - estimate) / SE
compatibility(candidate) = two-sided Wald p-value at that candidate
```

Additive effects use the identity working scale. Ratio effects use the log working scale, so the
CI-implied natural-scale estimate is the geometric midpoint of the interval. A supplied point
estimate validates the interval but does not replace the working-scale midpoint.

The compatibility curve is the two-sided Wald p-value function across candidate effects. Higher
values mean greater compatibility with the observed estimate under the reconstructed Wald model.
The values are not posterior probabilities. Compatibility of `0.05` at a candidate corresponds
to that candidate lying on the reconstructed 95% Wald interval boundary; the app also displays
`0.10`, `0.05`, and `0.01` guide levels.

See [Scientific scope](docs/SCIENTIFIC_SCOPE.md) for assumptions and limitations.

## Worked examples

### Additive effect

For a mean difference with reported 95% CI `0.11` to `0.73`, null `0`, and reference threshold
`0.20`, the reconstructed estimate is `0.42` and the working-scale SE is
`0.15816617164664273`. Compatibility at the null is `0.007920617864625943`; compatibility at
the threshold is `0.16424295999245675`.

### Ratio effect

For an odds ratio with reported 95% CI `1.2` to `2.7`, null `1`, and reference threshold `1.25`,
the reconstructed natural-scale estimate is `1.8`, the log-scale estimate is
`0.5877866649021191`, and the log-scale SE is `0.20687375447019513`. Compatibility at the null
is `0.004493256717721136`; compatibility at the threshold is `0.0779619122829084`.

These are synthetic method examples, not clinical thresholds or treatment recommendations.

## Inputs and outputs

Inputs:

- one of the nine effect measures in the shared core registry;
- optional point estimate;
- lower and upper limits of a two-sided 95% CI;
- optional null value, defaulting to `0` for additive effects and `1` for ratios;
- zero or more user-supplied reference thresholds;
- an optional plausible display range;
- ratio-axis spacing, grid size, and compatibility-guide display controls.

Outputs:

- one compatibility curve and textual alternative;
- the CI-implied estimate, working-scale SE, reported CI, null, and compatibility at the null;
- a threshold lookup with natural and working values, compatibility, relative location, and CI
  inclusion;
- structured reconstruction and display warnings;
- a copyable caption;
- a four-column CSV, dashboard PNG, and figure-only manuscript PNG.

The display range and ratio-axis spacing affect presentation only. They do not recompute the
estimate, SE, null result, or threshold lookups.

## Focused contract

The browser sends strict JSON to `compatibility_curve.contract.calculate_json`. The response has
exactly these top-level sections:

```text
meta
reconstruction
grid:
  effect_display
  effect_working
  standardized_distance
  compatibility
thresholds
intervals_or_guides
warnings
```

The contract intentionally contains no likelihood, support, power, selection, Type S/M, or
precision fields. CSV uses exactly the four grid columns shown above.

## Numerical authority and architecture

`wald-inference` `0.4.1` is the numerical source of truth. It is pinned to its exact released
wheel and SHA-256 in `pyproject.toml`, `uv.lock`, and `browser-stage.toml`. The local
`compatibility_curve` package owns only request validation, focused response assembly, display
grid selection, warnings, and browser serialization.

```text
browser form
  -> dedicated Web Worker
  -> hash-verified generated Python bundle
  -> released wald-inference core + local focused adapter
  -> strict JSON response
  -> text + Plotly curve + explicit exports
```

`scripts/stage_browser_packages.py` copies the installed, locked app and core packages into the
ignored `web/assets/py/` stage and records per-file, per-package, and aggregate hashes. The worker
verifies those bytes before loading Python. Generated Python is never edited or committed.

The creation-time template and scientific dependency provenance are recorded in
[Runtime dependencies and provenance](docs/RUNTIME_DEPENDENCIES.md).

## Local setup and verification

Python 3.12 and [`uv`](https://docs.astral.sh/uv/) are required.

```bash
git clone https://github.com/reblocke/compatibility-curve.git
cd compatibility-curve
uv sync --locked
uv run playwright install chromium webkit
make verify
```

Focused baseline parity can be rerun separately:

```bash
uv run pytest -q tests/regression/test_legacy_compatibility.py
```

To serve the staged app locally:

```bash
make serve
```

Then open `http://127.0.0.1:8000/`. Other useful targets are `make stage-web`, `make fmt`,
`make fmt-check`, `make lint`, `make test`, `make e2e`, and `make e2e-webkit-smoke`.

A new version is published only from an annotated tag whose exact remote tag object resolves to an
event commit already contained in protected `main`. The release workflow binds those identities
before executing repository code, reruns the complete suite with read-only contents permission,
builds a deterministic source archive, browser-stage manifest, and checksums, and transfers them
to a narrowly write-enabled publishing job. Using only the job-scoped GitHub token, that job
creates one draft stable release, re-downloads and compares the exact release body and every
asset, publishes only the verified draft, and verifies the resulting immutable release and asset
attestations. Credentialed commands use an exact checksummed GitHub CLI. Release notes contain
only the tagged version's nonempty changelog section.

## Validation

Frozen compatibility summaries for migration cases B01–B03 and B08 are stored in
`tests/fixtures/legacy_compatibility.json`. They identify the integrated baseline commit and use
the migration matrix tolerance (`rtol=1e-12`, `atol=1e-14`). Tests also cover:

- all core effect types and default nulls;
- strict JSON and nonfinite rejection;
- display-window isolation;
- absence of out-of-scope APIs and response keys;
- exact core wheel/checksum staging;
- Chromium behavior and exports;
- WebKit worker/calculation smoke;
- mobile keyboard, accessible error, privacy, storage, and network boundaries.

See [Validation](docs/VALIDATION.md) for evidence interpretation and release gates.

## Privacy

The app is static and client-side. It has no backend, database, telemetry, cookies, browser
storage, input-bearing URL state, account, or upload path. Inputs exist only in page and worker
memory. CSV and PNG files are generated locally after an explicit export action. Do not enter
protected health information or patient-level data. See [Privacy](docs/PRIVACY.md).

## Related Wald tools

- [Wald inference tools catalog](https://reblocke.github.io/wald-inference-tools/)
- [Adjacent focused app: likelihood support](https://reblocke.github.io/wald-likelihood-support/)
- [Integrated workbench](https://reblocke.github.io/conf_curve_likelihood/)
- [Source repository](https://github.com/reblocke/compatibility-curve)
- [wald-inference Core v0.4.1](https://github.com/reblocke/wald-inference-core/releases/tag/v0.4.1)
- [Privacy note](https://github.com/reblocke/compatibility-curve/blob/main/docs/PRIVACY.md)

These are static navigation links, not runtime dependencies.

## License and citation

Code is MIT licensed. Copyright (c) 2026 Brian Locke. Cite the tagged release or exact commit
used; see [CITATION.cff](CITATION.cff).
