from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "src" / "compatibility_curve"
ALLOWED_CORE_IMPORTS = {
    "DEFAULT_EFFECT_TYPE",
    "ValidationError",
    "__version__",
    "build_grid",
    "compatibility_curve",
    "from_working_scale",
    "get_effect_spec",
    "max_safe_grid_span",
    "reconstruct_wald_from_95_ci",
    "standardized_distance",
    "to_working_scale",
}
PROHIBITED_CORE_APIS = {
    "design_metrics_for_true_effects",
    "legacy_critical_effect_distance",
    "legacy_critical_effect_markers",
    "log_relative_likelihood",
    "precision_target_results",
    "relative_likelihood",
    "selection_rule_spec",
    "solve_required_precision",
    "support_comparison",
    "support_interval",
    "wald_point_summary",
}


def test_app_uses_only_root_public_compatibility_core_apis() -> None:
    imported: set[str] = set()
    for path in SOURCE_ROOT.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "wald_inference":
                imported.update(alias.name for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("wald_inference.")
            if isinstance(node, ast.Import):
                assert not any(alias.name.startswith("wald_inference.") for alias in node.names)

    assert imported <= ALLOWED_CORE_IMPORTS
    assert imported.isdisjoint(PROHIBITED_CORE_APIS)
    assert {
        "compatibility_curve",
        "reconstruct_wald_from_95_ci",
        "standardized_distance",
    } <= imported


def test_app_source_contains_no_local_wald_or_out_of_scope_implementation() -> None:
    production = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(SOURCE_ROOT.glob("*.py"))
    )

    assert "wald_inference.legacy" not in production
    assert "scipy" not in production
    for api in PROHIBITED_CORE_APIS:
        assert api not in production
    for fragment in [
        "norm.sf",
        "norm.cdf",
        "math.erf",
        "selection_rule",
        "information_multiplier",
    ]:
        assert fragment not in production


def test_exact_core_release_is_consistent_across_lock_and_stage_configuration() -> None:
    project = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    lock = (PROJECT_ROOT / "uv.lock").read_text(encoding="utf-8")
    stage = (PROJECT_ROOT / "browser-stage.toml").read_text(encoding="utf-8")
    artifact = (
        "https://github.com/reblocke/wald-inference-core/releases/download/"
        "v0.4.1/wald_inference-0.4.1-py3-none-any.whl"
    )
    digest = "d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b"

    assert f"{artifact}#sha256={digest}" in project
    assert artifact in lock
    assert f"sha256:{digest}" in lock
    assert artifact in stage
    assert digest in stage
