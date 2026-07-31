# Decisions

## 2026-07-31 — Publish reviewed maintenance updates as v0.1.5

The v0.1.5 patch records reviewed build/test dependency and GitHub Actions updates and restores
exact identity among the hosted Pages commit, package metadata, citation, annotated tag, and
immutable release artifacts. These maintenance updates do not change the checksum-pinned Core
v0.4.2 authority, any numerical result, focused response or export contract, scientific tolerance,
browser behavior, or client-side privacy boundary.

## 2026-07-31 — Adopt stable Core v0.4.2 without numerical change

The v0.1.4 app patch adopts the stable, immutable `wald-inference` v0.4.2 release at commit
`8afd0a463cc1d2586b8ce5cf92f40900647c3190`, annotated tag object
`26ea4a721b2dfa07f75c2f388a42d6272c88477c`, and exact wheel SHA-256
`225331d7b9d7b70e2508eecb92851a92a8c4e245baf412a1eb0f464d85da1349`. Core v0.4.2 changes only
repository and release governance; it preserves every formula, public API, tolerance, dependency
resolution, and frozen baseline value, including the v0.4.1 strict ratio-underflow repair.

The app still imports only root-public APIs and adds or copies no Wald formula. Its focused
compatibility response, exports, interpretation, privacy boundary, and scientific tolerances
remain unchanged; exact pin, lock, staging, legacy parity, strict-JSON, Chromium, WebKit, and
no-sibling clean-checkout verification are release gates.

## 2026-07-31 — Release verification uses repository workflow credentials only

This decision supersedes only the signed-tag-verification and dedicated settings-secret portions
of the 2026-07-30 governance decision below. A release still requires an annotated version tag.
Before repository code runs, the workflow requires the local tag to be an annotated tag at the
event commit, binds that tag to the exact remote tag object and event commit, requires protected
`main` containment, and matches the tag to the authoritative project version. GitHub's
`verification.verified` and `verification.reason` fields are no longer release gates; a tag may be
signed, but a valid GitHub signature is not required.

Repository release immutability remains an operator prerequisite, but the workflow no longer
queries that setting with an external administration-read credential. Remote tag inspection and
release publication use the job-scoped GitHub token. The publishing job still creates a draft,
compares its exact body and every downloaded asset before publication, then requires the published
release to report `isImmutable = true` and verifies the release and each asset attestation with the
same job-scoped token. All other least-privilege, protected-history, deterministic-artifact, and
one-time publication controls from the prior decision remain in force.

## 2026-07-30 — Fail-closed repository and release governance

Third-party GitHub Actions are content-addressed by full commit SHA and receive grouped,
review-only Dependabot proposals. Ordinary CI has explicit read-only contents permission; Pages
and release jobs receive only their required writes. Checkout credentials are not persisted, and
the release-artifact build disables shared dependency caching.

A release requires a GitHub-verified signed annotated tag and enabled repository release
immutability. The tag must equal `v` plus the authoritative project version. Before isolated
version parsing or repository code execution, the workflow binds the remote tag object to the
event commit and requires that commit to be contained in protected `main` history. It then builds
and checksums all assets, extracts a nonempty body from only that version's changelog section,
transfers the complete bundle to a separate publishing job, creates a draft stable release,
re-downloads and compares every draft asset and its body, and publishes only after exact
verification. Credentialed release commands use an exact checksummed GitHub CLI; the
pre-publication immutability query uses a dedicated administration-read Actions secret. A failed
run leaves an inspectable draft rather than an incompletely published release.

Private vulnerability reporting is the disclosure path. Public issue forms explicitly exclude
credentials, restricted data, sensitive user values, and protected health information. These
governance changes do not alter the app version, numerical authority, browser contract, or
compatibility-only scientific scope.

## 2026-07-30 — Bound responsive plot-title rendering

The app inserts deterministic line breaks into its Plotly title and verifies the rendered SVG
bounding box at a 390-pixel viewport. This presentation-only correction prevents visually cropped
titles without changing inputs, numerical responses, textual alternatives, or export data.

## 2026-07-30 — Upgrade the numerical authority to repaired Core v0.4.1

The v0.1.1 app patch adopts the annotated `wald-inference` v0.4.1 release at commit
`f4613177b6dc81d194aa70762152de2bfa86663b`, using the exact wheel SHA-256
`d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b`. The release fails closed
when a finite ratio working-scale value would underflow to an unrepresentable natural-scale zero.
The app still imports only root-public core APIs and adds or copies no Wald formula.

## 2026-07-29 — Released core owns all Wald calculations

The initial app consumed public root APIs from exact `wald-inference` 0.1.1. It did not copy a
formula, import legacy/internal modules, or call the broad integrated summary. This established
one numerical authority and made the focused contract independently auditable.

## 2026-07-29 — Compatibility-only response

The response is limited to metadata, reconstruction, the four-field compatibility grid,
threshold rows, compatibility guides, and warnings. Likelihood, support, power, critical effects,
selection, Type S/M, information, and precision are excluded even if the core can calculate
them.

## 2026-07-29 — Fixed reported 95% intervals in version 0.1.0

The interface accepts only two-sided 95% confidence limits. Arbitrary confidence levels would
change validation, labels, reconstruction semantics, fixtures, and interpretation and require a
separate reviewed change.

## 2026-07-29 — CI midpoint remains authoritative

A supplied point estimate is validation evidence but does not silently replace the reconstructed
working-scale midpoint. This preserves the integrated baseline contract and avoids mixing a
rounded point estimate with interval-derived uncertainty.

## 2026-07-29 — Display choices are presentation-only

Plausible display bounds define only the x-grid shown and exported. Ratio-axis linear/log
spacing and guide visibility are front-end choices and are not sent to the scientific contract.
Summary and threshold results remain invariant.

## 2026-07-29 — Thresholds are reference markers, not claim rules

The app reports compatibility and relative location for user-supplied thresholds. It does not
validate an MCID, assign benefit direction, classify a claim, or recommend a decision.

## 2026-07-29 — Static worker with verified generated stage

Python runs in a restartable Web Worker. The installed locked app and core packages are staged
from `browser-stage.toml`, and file/package/bundle hashes are checked before import. Generated
files remain ignored and reproducible from a clean checkout.

## 2026-07-29 — Strict client-side privacy boundary

There is no backend, telemetry, persistence, cookie, account, upload, or input-bearing URL.
Exports are local and explicit. Expanding this boundary requires a new privacy decision.

## 2026-07-29 — Creation-time template, no shared UI runtime

The repository was created from `scientific-applet-template` 0.1.0 at commit
`a360bde95c192d8de4f9a3b531e73600ebf3d8b8`. The copied browser shell may evolve locally and has
no runtime dependency on the template repository.
