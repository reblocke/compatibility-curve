# Codex AGENTS

## Purpose

- This repository is the focused static app for reconstructing Wald compatibility/confidence
  curves from a reported two-sided 95% confidence interval.
- Released `wald-inference` is the numerical source of truth. The local `compatibility_curve`
  package owns validation, focused response assembly, display-grid choices, warnings, and browser
  serialization.
- The app must answer only the observed-data compatibility question.

## Repository map

- `src/compatibility_curve/` — typed request, narrow response, and core orchestration.
- `web/` — static browser app and Web Worker.
- `scripts/stage_browser_packages.py` — deterministic ignored browser package stage.
- `tests/fixtures/legacy_compatibility.json` — focused B01–B03/B08 migration evidence.
- `tests/` — unit, regression, policy, staging, privacy, and browser tests.
- `docs/` — scope, validation, dependencies, privacy, decisions, and maintenance.

## Commands

- Setup: `uv sync --locked`
- Stage: `make stage-web`
- Format: `make fmt`
- Format check: `make fmt-check`
- Lint: `make lint`
- Non-browser tests: `make test`
- Chromium: `make e2e`
- WebKit smoke: `make e2e-webkit-smoke`
- Full verification: `make verify`

## Authority

1. User request and migration ticket.
2. Released `wald-inference` public root APIs and documented behavior.
3. `README.md`, `docs/SCIENTIFIC_SCOPE.md`, `docs/DECISIONS.md`, and this file.
4. Existing focused tests and code.

## Working rules

- Never implement or copy a Wald formula locally. Add a missing numerical primitive to
  `wald-inference-core`, release it, then adopt the exact artifact.
- Import only public APIs from the root `wald_inference` package. Do not use
  `wald_inference.legacy` or internal submodules.
- Do not add likelihood, support intervals, power, critical effects, selection rules, Type S/M,
  or precision calculations or fields.
- Treat plausible display range, ratio-axis spacing, and guide visibility as presentation
  controls. They must not alter reconstructed summaries or threshold lookup values.
- Keep thresholds explicitly user supplied; do not validate an MCID or turn one into a claim
  rule.
- Preserve strict finite browser JSON. Do not replace undefined or nonfinite values with
  invented numbers.
- Run staging; never hand-edit or commit `web/assets/py/`.
- Pin a core upgrade to an exact release URL and checksum, review its changes, and rerun baseline,
  strict-JSON, staging, Chromium, and WebKit gates.
- Preserve the client-side boundary: no backend, telemetry, persistence, cookies, input-bearing
  URLs, uploads, or PHI logging.
- Keep text/table alternatives; the plot cannot be the only result carrier.

## Skills

- Plan non-trivial changes with `.agents/skills/implementation-strategy/SKILL.md`.
- Verify browser/staging work with `.agents/skills/browser-verification/SKILL.md`.
- Review input or deployment changes with `.agents/skills/privacy-review/SKILL.md`.
- Synchronize behavior and public docs with `.agents/skills/docs-sync/SKILL.md`.

## Done criteria

- Relevant tests pass locally.
- The generated stage is reproducible from a clean checkout without a sibling repository.
- B01–B03/B08 parity, strict JSON, exact core provenance, focused ownership, Chromium, WebKit,
  privacy, accessibility, and exports are verified.
- Public documentation and wording remain consistent with the focused scope.
- The final report names commands, evidence, known limitations, and residual risks.
