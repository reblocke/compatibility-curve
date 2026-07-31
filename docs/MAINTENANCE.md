# Maintenance

## Status and ownership

Status: experimental, actively maintained software.

Maintainer: Brian Locke (`@reblocke`). Use
[repository issues](https://github.com/reblocke/compatibility-curve/issues) for reproducible bug,
scientific-boundary, accessibility, or documentation reports. Report vulnerabilities and privacy
defects privately through [SECURITY.md](../SECURITY.md). Changes are reviewed through pull
requests.

## Dependency updates

Review Pyodide, Plotly, Python, NumPy, SciPy, uv, Ruff, pytest, Hypothesis, Playwright, GitHub
Actions, and the scientific core deliberately. Dependabot groups weekly `uv` and GitHub Actions
updates for review; it does not authorize automatic merging. Keep each third-party Action pinned
to a full commit SHA with its reviewed version in a comment.

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

The release workflow binds the exact remote annotated tag object to the event commit before it
executes repository code. It requires the event commit to be contained in protected `main`, parses
the project version with isolated Python, reruns the complete suite under read-only contents
permission, disables the shared dependency cache for the release build, and creates the
deterministic source archive, browser-stage manifest, and SHA-256 checksums before a release
exists. A separate job with narrowly scoped contents-write permission uses an exact checksummed
GitHub CLI and the job-scoped GitHub token to create a draft stable release with every asset,
re-download and compare the draft assets and release body, and publish only the verified draft.
It then requires the published release to be immutable and verifies the release and every asset
attestation. The tag must equal `v` plus the authoritative project version, and the public release
body contains only that version's nonempty changelog section.

If the workflow fails after draft creation, retain the draft for inspection. Repair the workflow
and create a new tag only after the failure is understood; never move a published tag or replace a
published asset. The draft is the candidate; publish once into the intended stable lifecycle state
after hosted Pages and portfolio-level validation are complete.

Repository settings must retain read-only default workflow permissions, protect `main` and `v*`
tags, enable private vulnerability reporting and Dependabot security updates, and enable immutable
releases before the next tag is created. Confirm that setting operationally before tagging; the
workflow carries no external repository-settings credential and verifies immutability after
publication with its job-scoped GitHub token.

## Compatibility policy

Version 0.1.x is experimental. A change to effect registry handling, request/response keys,
field order, formulas, warnings, CSV columns, or interpretation must be called out in the
changelog and validation record. Scientific changes belong in the core first.

## Deprecation

If the app is superseded or archived, publish a release/changelog notice, mark the repository
status, keep the last static site available when practical, and link prominently to the
successor. Do not silently redirect, delete, or repurpose the URL for a scientifically different
tool.
