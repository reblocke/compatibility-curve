# Validation

## Evidence layers

Passing software tests demonstrates consistency with the stated contract and frozen references;
it does not prove that a Wald approximation is appropriate for a particular reported interval or
use case.

The validation strategy separates:

1. numerical parity with the integrated app's frozen compatibility baseline;
2. delegation and ownership checks against the released core;
3. request, strict-JSON, warning, and export contract checks;
4. browser, accessibility, privacy, and deployment checks.

## Frozen baseline provenance

`tests/fixtures/legacy_compatibility.json` is a compact focused extraction from
`reblocke/conf_curve_likelihood` golden fixtures at commit
`830756ecb11b4e8161f8dfe1fc75afc346ef4467`. That source manifest records its original request
and response hashes and NumPy/SciPy environment.

The focused fixture retains only compatibility-owned inputs and expected summaries. It does not
copy likelihood, support, critical-effect, power, selection, Type S/M, or precision fields.

Local scientific comparisons use:

```text
rtol = 1e-12
atol = 1e-14
```

Browser cross-engine comparisons may use `rtol=1e-10` and `atol=1e-12`. Tolerances must not be
widened merely to make a failure pass.

## Covered migration cases

| Case | Focused evidence |
|---|---|
| B01 | Additive estimate `0.42`, SE `0.15816617164664273`, null compatibility `0.007920617864625943`, threshold compatibility `0.16424295999245675` |
| B02 | Ratio estimate `1.8`, log estimate `0.5877866649021191`, log SE `0.20687375447019513`, null compatibility `0.004493256717721136`, threshold compatibility `0.0779619122829084` |
| B03 | Grid endpoints `0.9` and `1.1`; reconstruction and threshold rows identical to B02; excluded-marker warnings required |
| B08a | Opposite-signed near-limit additive bounds retain a finite midpoint, grid, and JSON |
| B08b | Near-limit positive additive bounds retain finite summaries and an explicit truncated-grid warning |
| B08c | Extreme standardized distance returns finite zero compatibility without nonstandard JSON |
| B08d | Near-maximum ratio bounds retain finite working/display grids and an explicit truncated-grid warning |
| B08e | An unrepresentable standardized distance raises `ValidationError` before serialization; integrated design fields are rejected as out of scope |

B01 and B02 also verify that ordinary grids reach compatibility one. CI-limit compatibility is
covered through the released core's frozen tests and the focused core-delegation boundary.

## Scientific ownership

AST and source-policy tests require the local package to import only public APIs from the root
`wald_inference` package. They prohibit internal/legacy imports and out-of-scope core functions.
The app calls the core for reconstruction, scale conversion, grid construction, standardized
distance, and compatibility. It contains no local normal-tail or Wald formula.

The browser effect options must match the core registry in key, order, label, family, and default
null. Package tests bind core `0.1.1` to the same release URL and SHA-256 in metadata, lock, stage
configuration, installed direct URL, and wheel `RECORD`.

## Contract and interpretation

Unit and regression tests cover:

- required, optional, paired, finite, positive-ratio, and grid-size validation;
- a supplied estimate validating rather than replacing the CI midpoint;
- exact top-level response order and four grid fields;
- absence of likelihood/design/precision keys recursively;
- compatibility range and finite output properties;
- strict input and output JSON, including rejection of `NaN` and infinities;
- display-range isolation and structured excluded-marker warnings;
- exact guide levels and focused CSV columns.

Browser tests verify the same estimate, null compatibility, SE, and threshold values in rendered
text/table output. The caption explicitly states the working interpretation and excludes profile
likelihood and posterior-probability meanings.

## Browser, privacy, and accessibility gates

Chromium E2E covers runtime initialization, ordinary ratio and additive cases, validation and
worker recovery, presentation-only windows, textual/table/plot agreement, exact CSV headers,
2800×2000 manuscript PNG, 1600×1200 dashboard PNG, caption clipboard, mobile layout, and keyboard
navigation.

WebKit smoke covers worker initialization and an end-to-end calculation. Static and dynamic
privacy checks require no backend, telemetry, storage, cookies, IndexedDB, input-bearing URL, or
user value in a network request. Accessible checks require labels, linked/focusable errors,
status announcements, visible focus, a skip link, text/table output, and a plot description.

## Commands

```bash
uv sync --locked
uv run playwright install chromium webkit
make verify
uv run pytest -q tests/regression/test_legacy_compatibility.py
uv run python scripts/stage_browser_packages.py
git diff --check
git status --short
```

A release additionally requires a clean-clone run, passing GitHub CI, and a smoke test of the
deployed Pages URL at the exact reviewed commit.

## Release evidence record

For each release, record:

- reviewed commit and tag;
- app, core, Python, Pyodide, NumPy, SciPy, Plotly, and browser versions;
- core artifact URL/checksum and stage manifest checksum;
- unit, regression, policy, staging, Chromium, and WebKit results;
- deployed Pages smoke result;
- known scientific and deployment limitations.
