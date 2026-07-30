# Runtime Dependencies and Provenance

## Scientific core

Numerical authority is the released pure-Python wheel:

```text
distribution: wald-inference
version: 0.1.1
release: https://github.com/reblocke/wald-inference-core/releases/tag/v0.1.1
artifact: https://github.com/reblocke/wald-inference-core/releases/download/v0.1.1/wald_inference-0.1.1-py3-none-any.whl
SHA-256: 95bc10d770836544d726362c401032e0640a5a9ec1573f043add7f6bd3a65457
tag commit: d1ffb0baa46eb8ad27175d58c90e4febc0ac2809
license: MIT
```

The app uses the core's public reconstruction, effect-scale, finite-grid, standardized-distance,
and compatibility APIs. The URL and checksum are repeated in `pyproject.toml`, `uv.lock`, and
`browser-stage.toml`. Staging verifies the lock, installed `direct_url.json`, wheel `RECORD`,
package version, and all copied bytes.

## Browser runtime

| Dependency | Version | Purpose | Source/licensing route |
|---|---:|---|---|
| Pyodide | 0.29.3 | CPython/WebAssembly runtime and package loader | Versioned jsDelivr distribution; upstream Pyodide notices apply |
| NumPy | 2.2.6 locked locally; Pyodide package in browser | Arrays and finite vector operations required by the core | PyPI/Pyodide; BSD-family upstream license |
| SciPy | 1.14.1 locked locally; Pyodide package in browser | Normal-distribution primitives required by the core | PyPI/Pyodide; BSD-family upstream license |
| Plotly.js | 3.1.0 | Interactive curve and local PNG rendering | Versioned Plotly CDN; MIT upstream license |

The worker loads Pyodide from its exact versioned jsDelivr path. Plotly uses its exact versioned
CDN path. These static requests contain no user values. Availability still depends on reaching
the CDNs; runtime assets are not vendored in this repository.

`web/assets/py/manifest.json` is generated from the locked environment. It lists exact app/core
versions, artifact metadata, source commit, staged files, sizes, and hashes. The stage is ignored
and regenerated for CI, Pages, and release builds.

## Creation-time template

The repository was created from:

```text
repository: https://github.com/reblocke/scientific-applet-template
template release: v0.1.0
template commit: a360bde95c192d8de4f9a3b531e73600ebf3d8b8
template tree: 6a6c8c33cbef24b5dcbd35706d2292d9d3e5e359
license: MIT
```

The template supplied the engineering shell, worker/staging mechanism, accessibility/privacy
guards, workflows, and documentation structure. The scientific contract, UI, examples, tests,
and wording in this repository are app-specific. There is no runtime dependency on the template.

## Baseline evidence

Focused regression values were extracted from the integrated repository's frozen golden corpus:

```text
repository: https://github.com/reblocke/conf_curve_likelihood
behavior source commit: 830756ecb11b4e8161f8dfe1fc75afc346ef4467
baseline fixture commit: 5fd501dd947d9b951d736014cfc2b310efa5e7b0
baseline tag: pre-split-baseline-2026-07-29
source manifest: tests/golden/manifest.json
focused fixture: tests/fixtures/legacy_compatibility.json
```

Only app-owned compatibility summaries are retained. The fixture contains synthetic numerical
method examples and no patient data.

## Repository license boundary

Original code in this repository is MIT licensed. External runtimes and packages retain their
own licenses and notices. No paper, publisher figure, dataset, or copied clinical artifact is
committed. Dependency licenses and provenance must be rechecked before vendoring or redistributing
external artifacts.
