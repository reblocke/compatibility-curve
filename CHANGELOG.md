# Changelog

All notable changes are recorded here. This repository follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

- Harden CI, Pages, and release automation with least-privilege permissions, full-SHA Action pins,
  checkout credential isolation, and disabled dependency caching for release artifacts.
- Require a GitHub-verified signed annotated tag on protected `main`, bound to the event commit and
  authoritative project version before repository code is executed.
- Install an exact checksummed GitHub CLI, require repository immutability through a dedicated
  administration-read secret, and verify the complete draft body and asset set before one-time
  stable publication.
- Add grouped weekly Dependabot proposals, private vulnerability reporting guidance, contribution
  policy, scoped issue forms, a pull-request checklist, and repository-policy regressions.
- Preserve version `0.1.3`, the exact `wald-inference` v0.4.1 wheel and checksum, every scientific
  and browser contract, the compatibility-only negative scope, and the client-side privacy
  boundary.

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

[Unreleased]: https://github.com/reblocke/compatibility-curve/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/reblocke/compatibility-curve/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/reblocke/compatibility-curve/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/reblocke/compatibility-curve/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/reblocke/compatibility-curve/releases/tag/v0.1.0
