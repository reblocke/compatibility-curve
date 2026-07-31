from __future__ import annotations

import re
from pathlib import Path

from wald_inference import EFFECT_SPECS

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEB_ROOT = PROJECT_ROOT / "web"


def test_worker_is_manifest_driven_and_verifies_before_import() -> None:
    worker = (WEB_ROOT / "pyodide_worker.js").read_text(encoding="utf-8")

    assert "manifest.packages" in worker
    assert "fileRecord.path" in worker
    assert "PACKAGE_FILES" not in worker
    assert "fetchVerifiedBundle()" in worker
    assert worker.index("await fetchVerifiedBundle()") < worker.index("importScripts(")
    assert worker.index("failed integrity verification") < worker.index("loadPyodide(")
    assert "if (bundle.manifest.pyodide_packages.length > 0)" in worker


def test_production_web_code_has_no_persistence_telemetry_or_input_urls() -> None:
    production = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(WEB_ROOT.rglob("*"))
        if path.is_file() and "assets/py" not in path.as_posix()
    )

    forbidden_fragments = [
        "localStorage",
        "sessionStorage",
        "indexedDB",
        "document.cookie",
        "location.search",
        "location.hash",
        "sendBeacon",
        "gtag(",
        "analytics",
        "console.log",
    ]
    assert not [fragment for fragment in forbidden_fragments if fragment in production]
    assert "new URL(path" not in production
    for argument in re.findall(r"fetch\(([^,)]+)", production):
        assert "input" not in argument.lower()


def test_ui_contains_accessibility_scope_and_text_alternatives() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    css = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

    assert 'aria-live="polite"' in html
    assert 'role="alert"' in html
    for control_id in [
        "effect-type",
        "estimate",
        "ci-lower",
        "ci-upper",
        "null-value",
        "thresholds",
    ]:
        assert re.search(rf'<label for="{control_id}"', html)
    assert "<details>" in html and "<summary>" in html
    assert 'class="skip-link"' in html
    assert 'aria-describedby="plot-description"' in html
    assert 'id="reconstruction-summary"' in html
    assert ":focus-visible" in css
    assert "They are not posterior probabilities" in html
    assert "clinical decision support" in html


def test_browser_effect_options_match_the_released_core_registry() -> None:
    config = (WEB_ROOT / "js" / "config.js").read_text(encoding="utf-8")
    configured = re.findall(r'key: "([a-z_]+)"', config)

    assert configured == list(EFFECT_SPECS)
    for key, spec in EFFECT_SPECS.items():
        section = config.split(f'key: "{key}"', maxsplit=1)[1].split("},", maxsplit=1)[0]
        assert f'label: "{spec.label}"' in section
        assert f'family: "{spec.family}"' in section
        assert f"defaultNull: {spec.default_null:g}" in section


def test_exports_use_exact_focused_columns_and_separate_png_hooks() -> None:
    exports = (WEB_ROOT / "js" / "exports.js").read_text(encoding="utf-8")
    keys = re.findall(r'\{ key: "([^"]+)", label:', exports)

    assert keys == [
        "effect_display",
        "effect_working",
        "standardized_distance",
        "compatibility",
    ]
    assert "exportDashboardPng" in exports
    assert "exportManuscriptPng" in exports
    assert "height: 1000" in exports
    assert "width: 1400" in exports
    assert "scale: 2" in exports
    assert "copyCaption" in exports
    assert "filenameSlug" in exports
    assert not {
        "relative_likelihood",
        "log_likelihood",
        "power",
        "type_s",
        "type_m",
    } & set(keys)


def test_related_wald_tool_blocks_are_static_compact_and_exact() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    expected_links = [
        "https://reblocke.github.io/wald-inference-tools/",
        "https://reblocke.github.io/wald-likelihood-support/",
        "https://reblocke.github.io/conf_curve_likelihood/",
        "https://github.com/reblocke/compatibility-curve",
        "https://github.com/reblocke/wald-inference-core/releases/tag/v0.4.2",
        "https://github.com/reblocke/compatibility-curve/blob/main/docs/PRIVACY.md",
    ]

    html_block = html.split('<section id="related-wald-tools">', maxsplit=1)[1].split(
        "</section>", maxsplit=1
    )[0]
    readme_block = readme.split("## Related Wald tools", maxsplit=1)[1].split("\n## ", maxsplit=1)[
        0
    ]

    assert "<h2>Related Wald tools</h2>" in html_block
    assert re.findall(r'href="([^"]+)"', html_block) == expected_links
    assert re.findall(r"\]\((https://[^)]+)\)", readme_block) == expected_links
    assert "wald-inference Core v0.4.2" in html_block
    assert "wald-inference Core v0.4.2" in readme_block
    assert "Privacy note" in html_block
    assert "Privacy note" in readme_block
    assert "fetch(" not in html
