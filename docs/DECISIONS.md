# Decisions

## 2026-07-29 — Released core owns all Wald calculations

The app consumes public root APIs from exact `wald-inference` 0.1.1. It does not copy a formula,
import legacy/internal modules, or call the broad integrated summary. This keeps one numerical
authority and makes the focused contract independently auditable.

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
