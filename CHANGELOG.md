# Changelog

All notable changes are recorded here. This repository follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.5] - 2026-07-31

- Update the locked test/build toolchain to pytest 9.1.1 and setuptools 83.0.0.
- Update the reviewed, full-SHA GitHub Actions pins used by CI, Pages, and release workflows.
- Publish the maintenance-only app state as an immutable patch release so the hosted Pages commit,
  package metadata, citation, and release artifacts identify the same source commit.
- Preserve the exact Core v0.4.2 pin, numerical behavior, focused response/export contracts,
  browser behavior, scientific tolerances, and client-side privacy boundary.

## [0.1.4] - 2026-07-31

- Adopt the official stable, immutable `wald-inference` v0.4.2 wheel from annotated tag target
  `8afd0a463cc1d2586b8ce5cf92f40900647c3190`, pinned to SHA-256
  `225331d7b9d7b70e2508eecb92851a92a8c4e245baf412a1eb0f464d85da1349`. Core v0.4.2 changes
  release governance only and preserves every numerical API and frozen baseline value.
- Synchronize app version 0.1.4 across package metadata, citation, browser staging, visible runtime
  copy, lockfile, and tests while preserving the exact compatibility-only response/export
  contracts, scientific tolerances, and client-side privacy boundary.
- Harden CI, Pages, and release automation with least-privilege permissions, full-SHA Action pins,
  checkout credential isolation, and disabled dependency caching for release artifacts.
- Require an annotated tag whose exact remote tag object is bound to the event commit on protected
  `main` and the authoritative project version before repository code is executed, without making
  GitHub signature verification a release gate.
- Use only the job-scoped GitHub token for remote tag and release operations; remove the external
  settings credential and prepublication immutable-settings query while retaining exact draft
  body/asset comparison and post-publication immutable-release and asset verification.
- Add grouped weekly Dependabot proposals, private vulnerability reporting guidance, contribution
  policy, scoped issue forms, a pull-request checklist, and repository-policy regressions.
- Preserve every scientific and browser contract and the compatibility-only negative scope; no
  Wald formula is added or copied locally.

## [0.1.3] - 2026-07-30

- Add explicit README metadata for the current app version, experimental maturity, exact versioned
  release URL, GitHub publication state, and software citation guidance.
- Keep maintenance status independent of prerelease or stable GitHub promotion state.
- Add a repository-policy regression that keeps README release/version/citation metadata aligned
  with package and `CITATION.cff` versions.
- Preserve all scientific, focused-response, browser UI, privacy, and export behavior; Core remains
  pinned to `wald-inference` v0.4.1.

## [0.1.2] - 2026-07-30

- Wrap Plotly figure titles into bounded lines so every supported effect label remains readable
  inside a 390-pixel viewport and in responsive exports.
- Strengthen the mobile Chromium regression from document containment to rendered title
  bounding-box containment.
- Preserve all numerical, focused-response, privacy, and export contracts.

## [0.1.1] - 2026-07-30

- Publish the navigation-enabled Pages source as a checksum-addressed patch release so the
  deployed app, annotated tag, and release artifacts resolve to the same commit.
- Prevent narrow-screen horizontal overflow by allowing result panels to shrink and resizing the
  Plotly plot only after the results are visible and one animation frame has elapsed.
- Preserve the v0.1.0 focused contract and exports while upgrading the sole numerical authority
  to checksum-pinned `wald-inference` 0.4.1; no Wald formula is added or copied locally.

## [0.1.0] - 2026-07-29

- Implement the focused compatibility/confidence-curve request and response contract.
- Delegate reconstruction, scale conversion, standardized distance, and compatibility to the
  exact `wald-inference` 0.1.1 release artifact.
- Add the nine shared effect measures, reference-threshold lookup, display-only window and axis
  controls, compatibility guides, structured warnings, and strict JSON.
- Add the accessible static browser UI, direct plot markers, textual summary, copyable caption,
  focused CSV, dashboard PNG, and manuscript PNG.
- Freeze B01–B03 and B08 compatibility parity evidence from the integrated baseline.
- Add deterministic core staging, scientific-ownership checks, privacy/storage/network tests,
  Chromium E2E, WebKit smoke, documentation, citation, and related-tool routing.

This initial prerelease records software and scientific-reference validation; it does not claim
clinical validation or completion of the independent portfolio-wide review.

[Unreleased]: https://github.com/reblocke/compatibility-curve/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/reblocke/compatibility-curve/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/reblocke/compatibility-curve/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/reblocke/compatibility-curve/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/reblocke/compatibility-curve/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/reblocke/compatibility-curve/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/reblocke/compatibility-curve/releases/tag/v0.1.0
