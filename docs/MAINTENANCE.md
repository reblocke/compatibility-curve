# Maintenance

## Status and ownership

Status: experimental, actively maintained prerelease software.

Maintainer: Brian Locke (`@reblocke`). Use
[repository issues](https://github.com/reblocke/compatibility-curve/issues) for reproducible bug,
scientific-boundary, accessibility, privacy, or documentation reports. Changes are reviewed
through pull requests.

## Dependency updates

Review Pyodide, Plotly, Python, NumPy, SciPy, uv, Ruff, pytest, Hypothesis, Playwright, GitHub
Actions, and the scientific core deliberately.

For a core update:

1. review its release notes and numerical changes;
2. require an exact released pure-Python wheel URL and SHA-256;
3. update `pyproject.toml`, `uv.lock`, and `browser-stage.toml` together;
4. confirm the installed direct URL and wheel `RECORD`;
5. rerun legacy compatibility, strict JSON, effect registry, staging, Chromium, and WebKit
   validation;
6. document any changed value, warning, tolerance, or interpretation.

Do not consume an unreleased sibling checkout or silently widen a tolerance.

## Release process

Use a reviewed pull request. Verify the exact candidate head locally and in a clean clone, then
confirm GitHub CI. After merge, confirm Pages at the merge commit. Only then create an annotated
semantic-version tag on that exact verified commit.

The tag workflow reruns the complete suite and publishes a GitHub prerelease with a deterministic
source archive, browser-stage manifest, and SHA-256 checksums. Promotion from prerelease requires
a passing hosted smoke and portfolio-level validation.

## Compatibility policy

Version 0.1.x is experimental. A change to effect registry handling, request/response keys,
field order, formulas, warnings, CSV columns, or interpretation must be called out in the
changelog and validation record. Scientific changes belong in the core first.

## Deprecation

If the app is superseded or archived, publish a release/changelog notice, mark the repository
status, keep the last static site available when practical, and link prominently to the
successor. Do not silently redirect, delete, or repurpose the URL for a scientifically different
tool.
