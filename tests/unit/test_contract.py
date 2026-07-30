from __future__ import annotations

import json
import math

import pytest
from hypothesis import given
from hypothesis import strategies as st
from wald_inference import EFFECT_SPECS

from compatibility_curve import (
    CompatibilityRequest,
    ValidationError,
    calculate,
    calculate_json,
)

TOP_LEVEL_KEYS = [
    "meta",
    "reconstruction",
    "grid",
    "thresholds",
    "intervals_or_guides",
    "warnings",
]
GRID_KEYS = [
    "effect_display",
    "effect_working",
    "standardized_distance",
    "compatibility",
]
PROHIBITED_KEYS = {
    "critical_effect",
    "design",
    "information_multiplier",
    "likelihood_ratio",
    "log_likelihood",
    "power",
    "precision",
    "relative_likelihood",
    "selection_rule",
    "support",
    "type_m",
    "type_s",
}


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for nested in value.values() for key in _all_keys(nested)}
    if isinstance(value, list):
        return {key for nested in value for key in _all_keys(nested)}
    return set()


def _ordinary_request(effect_type: str = "mean_difference") -> CompatibilityRequest:
    ratio = EFFECT_SPECS[effect_type].family == "ratio"
    return CompatibilityRequest.from_mapping(
        {
            "effect_type": effect_type,
            "lower": 1.2 if ratio else 0.11,
            "upper": 2.7 if ratio else 0.73,
            "thresholds": [1.25 if ratio else 0.2],
            "grid_points": 401,
        }
    )


def test_response_contract_is_narrow_ordered_and_compatibility_only() -> None:
    response = calculate(_ordinary_request())

    assert list(response) == TOP_LEVEL_KEYS
    assert list(response["grid"]) == GRID_KEYS
    assert not (_all_keys(response) & PROHIBITED_KEYS)
    assert response["intervals_or_guides"]["compatibility_guides"] == [
        {"label": "90%", "compatibility": 0.10},
        {"label": "95%", "compatibility": 0.05},
        {"label": "99%", "compatibility": 0.01},
    ]


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_contract_rejects_nonstandard_json_numbers(constant: str) -> None:
    with pytest.raises(ValidationError, match="Non-finite JSON constant"):
        calculate_json(f'{{"lower": {constant}, "upper": 1}}')


def test_contract_returns_strict_json() -> None:
    response_json = calculate_json(
        json.dumps(
            {
                "effect_type": "mean_difference",
                "lower": 0.11,
                "upper": 0.73,
                "thresholds": [0.2],
                "grid_points": 401,
            }
        )
    )

    assert "NaN" not in response_json
    assert "Infinity" not in response_json
    assert list(json.loads(response_json)) == TOP_LEVEL_KEYS


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({}, "Missing required field"),
        ({"lower": 0, "upper": 1, "power": 0.8}, "Unexpected field"),
        ({"lower": True, "upper": 1}, "Lower 95% confidence limit must be a number"),
        ({"lower": 0, "upper": "1"}, "Upper 95% confidence limit must be a number"),
        ({"lower": 0, "upper": 1, "thresholds": "0.2"}, "JSON array"),
        ({"lower": 0, "upper": 1, "grid_points": 400}, "odd"),
        ({"lower": 0, "upper": 1, "grid_points": 99}, "between"),
        (
            {"lower": 0, "upper": 1, "display_range_lower": -1},
            "must be supplied together",
        ),
    ],
)
def test_request_validation_is_explicit(payload: object, message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        CompatibilityRequest.from_mapping(payload)


@pytest.mark.parametrize("effect_type", list(EFFECT_SPECS))
def test_every_core_effect_measure_is_supported(effect_type: str) -> None:
    response = calculate(_ordinary_request(effect_type))

    spec = EFFECT_SPECS[effect_type]
    assert response["meta"]["effect_spec"]["key"] == effect_type
    assert response["meta"]["effect_spec"]["family"] == spec.family
    assert response["meta"]["effect_spec"]["working_scale"] == spec.working_scale
    assert response["reconstruction"]["null_display"] == spec.default_null
    assert len(response["grid"]["compatibility"]) == 401
    assert all(0.0 <= value <= 1.0 for value in response["grid"]["compatibility"])


def test_provided_estimate_validates_but_ci_midpoint_remains_authoritative() -> None:
    request = CompatibilityRequest.from_mapping(
        {
            "effect_type": "odds_ratio",
            "estimate": 1.8,
            "lower": 1.2,
            "upper": 2.7,
        }
    )
    response = calculate(request)

    assert response["meta"]["estimate_source"] == "provided_validated"
    assert response["reconstruction"]["provided_estimate_display"] == 1.8
    assert response["reconstruction"]["estimate_display"] == 1.8
    with pytest.raises(ValidationError, match="inconsistent"):
        calculate(
            CompatibilityRequest.from_mapping(
                {
                    "effect_type": "odds_ratio",
                    "estimate": 2.0,
                    "lower": 1.2,
                    "upper": 2.7,
                }
            )
        )


@given(
    lower=st.floats(
        allow_nan=False,
        allow_infinity=False,
        min_value=-1e6,
        max_value=1e6 - 1e-3,
    ),
    width=st.floats(
        allow_nan=False,
        allow_infinity=False,
        min_value=1e-3,
        max_value=1e6,
    ),
)
def test_additive_curve_is_finite_bounded_and_peaks_at_one(lower: float, width: float) -> None:
    upper = lower + width
    request = CompatibilityRequest.from_mapping(
        {
            "effect_type": "mean_difference",
            "lower": lower,
            "upper": upper,
            "grid_points": 101,
        }
    )
    response = calculate(request)

    for values in response["grid"].values():
        assert all(math.isfinite(value) for value in values)
    compatibility = response["grid"]["compatibility"]
    assert all(0.0 <= value <= 1.0 for value in compatibility)
    assert compatibility[len(compatibility) // 2] == max(compatibility)
    assert max(compatibility) >= 0.999999


def test_display_range_changes_only_grid_and_adds_marker_warnings() -> None:
    base = calculate(
        CompatibilityRequest.from_mapping(
            {
                "effect_type": "odds_ratio",
                "lower": 1.2,
                "upper": 2.7,
                "null_value": 1.0,
                "thresholds": [1.25],
                "grid_points": 401,
            }
        )
    )
    windowed = calculate(
        CompatibilityRequest.from_mapping(
            {
                "effect_type": "odds_ratio",
                "lower": 1.2,
                "upper": 2.7,
                "null_value": 1.0,
                "thresholds": [1.25],
                "display_range_lower": 0.9,
                "display_range_upper": 1.1,
                "grid_points": 401,
            }
        )
    )

    assert windowed["grid"]["effect_display"][0] == 0.9
    assert windowed["grid"]["effect_display"][-1] == 1.1
    assert windowed["reconstruction"] == base["reconstruction"]
    assert windowed["thresholds"] == base["thresholds"]
    assert [warning["code"] for warning in windowed["warnings"]] == [
        "display_excludes_estimate",
        "display_excludes_lower_ci",
        "display_excludes_upper_ci",
        "display_excludes_threshold",
    ]


def test_ratio_display_range_must_remain_positive() -> None:
    with pytest.raises(ValidationError, match="strictly positive"):
        calculate(
            CompatibilityRequest.from_mapping(
                {
                    "effect_type": "odds_ratio",
                    "lower": 1.2,
                    "upper": 2.7,
                    "display_range_lower": 0.0,
                    "display_range_upper": 3.0,
                }
            )
        )
