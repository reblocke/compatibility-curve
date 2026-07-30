from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_makefile_exposes_required_commands() -> None:
    makefile = (PROJECT_ROOT / "Makefile").read_text(encoding="utf-8")

    for target in [
        "stage-web:",
        "fmt:",
        "fmt-check:",
        "lint:",
        "test:",
        "e2e:",
        "verify:",
        "serve:",
        "clean:",
    ]:
        assert target in makefile


def test_ci_and_pages_use_repository_targets() -> None:
    ci = (PROJECT_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    pages = (PROJECT_ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")

    assert "make fmt-check" in ci
    assert "make lint" in ci
    assert "make test" in ci
    assert "make e2e" in ci
    assert "make e2e-webkit-smoke" in ci
    assert "make stage-web" in pages
    assert "enablement: true" in pages
    assert "web" in pages


def test_generated_stage_is_ignored_and_not_tracked() -> None:
    gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "web/assets/py/" in gitignore
    assert (
        subprocess.run(
            ["git", "check-ignore", "web/assets/py/manifest.json"],
            cwd=PROJECT_ROOT,
            check=False,
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            ["git", "ls-files", "web/assets/py"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        == ""
    )


def test_required_public_documentation_is_complete_and_has_no_author_prompts() -> None:
    required = [
        "README.md",
        "LICENSE",
        "CITATION.cff",
        "AGENTS.md",
        "CHANGELOG.md",
        "llms.txt",
        "docs/SCIENTIFIC_SCOPE.md",
        "docs/VALIDATION.md",
        "docs/PRIVACY.md",
        "docs/DECISIONS.md",
        "docs/MAINTENANCE.md",
        "docs/RUNTIME_DEPENDENCIES.md",
    ]
    contents = []
    for relative in required:
        path = PROJECT_ROOT / relative
        assert path.is_file(), relative
        contents.append(path.read_text(encoding="utf-8"))
    assert "AUTHOR ACTION REQUIRED" not in "\n".join(contents)


def test_license_identity_is_canonical() -> None:
    license_text = (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8")
    citation = (PROJECT_ROOT / "CITATION.cff").read_text(encoding="utf-8")

    assert "Copyright (c) 2026 Brian Locke" in license_text
    assert "MIT License" in license_text
    assert "family-names: Locke" in citation
    assert "given-names: Brian" in citation
    assert "license: MIT" in citation


def test_readme_records_current_release_and_software_citation() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    citation = (PROJECT_ROOT / "CITATION.cff").read_text(encoding="utf-8")
    maintenance = (PROJECT_ROOT / "docs" / "MAINTENANCE.md").read_text(encoding="utf-8")
    project = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    version = project["version"]

    assert f"Current app version: `{version}`." in readme
    assert f"https://github.com/reblocke/compatibility-curve/releases/tag/v{version}" in readme
    assert "Release maturity: experimental software." in readme
    assert "GitHub publication state is recorded on the versioned release page:" in readme
    assert "Cite the exact tagged software release or commit used" in readme
    assert "[CITATION.cff](CITATION.cff)" in readme
    assert f"version: {version}" in citation
    assert "Status: experimental, actively maintained software." in maintenance
    assert "actively maintained prerelease software" not in maintenance
