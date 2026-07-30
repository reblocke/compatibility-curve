from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from compatibility_curve import CompatibilityRequest, ValidationError, calculate, calculate_json

FIXTURE_PATH = Path(__file__).parents[1] / "fixtures" / "legacy_compatibility.json"
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
RTOL = FIXTURE["provenance"]["rtol"]
ATOL = FIXTURE["provenance"]["atol"]


@pytest.mark.parametrize("case_id", ["B01", "B02", "B03"])
def test_ordinary_legacy_compatibility_subset(case_id: str) -> None:
    case = FIXTURE["cases"][case_id]
    response = calculate(CompatibilityRequest.from_mapping(case["request"]))
    expected = case["expected"]
    reconstruction = response["reconstruction"]
    threshold = response["thresholds"][0]

    for key in (
        "estimate_display",
        "estimate_working",
        "standard_error_working",
        "compatibility_at_null",
    ):
        assert reconstruction[key] == pytest.approx(expected[key], rel=RTOL, abs=ATOL)
    assert threshold["effect_working"] == pytest.approx(
        expected["threshold_working"], rel=RTOL, abs=ATOL
    )
    assert threshold["compatibility"] == pytest.approx(
        expected["threshold_compatibility"], rel=RTOL, abs=ATOL
    )
    if case_id != "B03":
        assert max(response["grid"]["compatibility"]) == pytest.approx(1.0, rel=RTOL, abs=ATOL)

    if case_id == "B03":
        assert response["grid"]["effect_display"][0] == expected["display_first"]
        assert response["grid"]["effect_display"][-1] == expected["display_last"]


def test_b03_reconstruction_and_threshold_are_identical_to_b02() -> None:
    cases = FIXTURE["cases"]
    b02 = calculate(CompatibilityRequest.from_mapping(cases["B02"]["request"]))
    b03 = calculate(CompatibilityRequest.from_mapping(cases["B03"]["request"]))

    assert b03["reconstruction"] == b02["reconstruction"]
    assert b03["thresholds"] == b02["thresholds"]
    assert {warning["code"] for warning in b03["warnings"]} == {
        "display_excludes_estimate",
        "display_excludes_lower_ci",
        "display_excludes_upper_ci",
        "display_excludes_threshold",
    }


@pytest.mark.parametrize(
    "case_id",
    [
        "B08a-additive-midpoint",
        "B08b-s-minus-2-clipping",
        "B08c-log-likelihood-fallback",
        "B08d-ratio-natural-clipping",
    ],
)
def test_extreme_finite_cases_match_summaries_and_remain_strict(case_id: str) -> None:
    case = FIXTURE["cases"][case_id]
    request = CompatibilityRequest.from_mapping(case["request"])
    response = calculate(request)
    reconstruction = response["reconstruction"]

    for key, value in case["expected"].items():
        assert reconstruction[key] == pytest.approx(value, rel=RTOL, abs=ATOL)
    assert all(math.isfinite(value) for values in response["grid"].values() for value in values)
    assert all(0.0 <= value <= 1.0 for value in response["grid"]["compatibility"])
    json.loads(calculate_json(json.dumps(case["request"])))

    if case_id in {
        "B08a-additive-midpoint",
        "B08b-s-minus-2-clipping",
        "B08d-ratio-natural-clipping",
    }:
        assert "grid_truncated" in {warning["code"] for warning in response["warnings"]}


def test_unrepresentable_extreme_distance_is_rejected_before_json() -> None:
    case = FIXTURE["cases"]["B08e-unrepresentable-design-distance"]
    with pytest.raises(ValidationError, match=case["expected_error"]):
        calculate(CompatibilityRequest.from_mapping(case["request"]))


def test_integrated_design_flag_is_not_part_of_the_focused_contract() -> None:
    request = {
        **FIXTURE["cases"]["B08e-unrepresentable-design-distance"]["request"],
        "design_enabled": True,
    }
    with pytest.raises(ValidationError, match="Unexpected field: design_enabled"):
        CompatibilityRequest.from_mapping(request)
