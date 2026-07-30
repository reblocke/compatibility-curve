"""Typed request and response models for the focused compatibility applet."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal, TypedDict

from wald_inference import DEFAULT_EFFECT_TYPE, ValidationError

DEFAULT_GRID_POINTS = 801
MIN_GRID_POINTS = 101
MAX_GRID_POINTS = 1601


def _finite_number(value: object, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValidationError(f"{field} must be a number.")
    number = float(value)
    if not math.isfinite(number):
        raise ValidationError(f"{field} must be finite.")
    return number


def _optional_number(payload: dict[str, object], key: str, *, field: str) -> float | None:
    value = payload.get(key)
    return None if value is None else _finite_number(value, field=field)


def _thresholds(value: object) -> tuple[float, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValidationError("Reference thresholds must be supplied as a JSON array.")
    return tuple(
        _finite_number(item, field=f"Reference threshold {index}")
        for index, item in enumerate(value, start=1)
    )


def _grid_points(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError("Grid points must be an integer.")
    if value < MIN_GRID_POINTS or value > MAX_GRID_POINTS:
        raise ValidationError(
            f"Grid points must be between {MIN_GRID_POINTS} and {MAX_GRID_POINTS}."
        )
    if value % 2 == 0:
        raise ValidationError("Grid points must be odd so the estimate is a grid point.")
    return value


@dataclass(frozen=True)
class CompatibilityRequest:
    """Validated app inputs before scientific reconstruction."""

    effect_type: str
    estimate: float | None
    lower: float
    upper: float
    null_value: float | None
    thresholds: tuple[float, ...]
    display_range: tuple[float, float] | None
    grid_points: int

    @classmethod
    def from_mapping(cls, payload: object) -> CompatibilityRequest:
        if not isinstance(payload, dict) or not all(isinstance(key, str) for key in payload):
            raise ValidationError("Request must be a JSON object.")

        allowed = {
            "display_range_lower",
            "display_range_upper",
            "effect_type",
            "estimate",
            "grid_points",
            "lower",
            "null_value",
            "thresholds",
            "upper",
        }
        unexpected = sorted(set(payload) - allowed)
        if unexpected:
            raise ValidationError(f"Unexpected field: {unexpected[0]}.")
        for required in ("lower", "upper"):
            if required not in payload:
                raise ValidationError(f"Missing required field: {required}.")

        effect_type = payload.get("effect_type", DEFAULT_EFFECT_TYPE)
        if not isinstance(effect_type, str) or not effect_type:
            raise ValidationError("Effect measure must be a non-empty string.")

        range_lower = _optional_number(
            payload,
            "display_range_lower",
            field="Plausible display range lower",
        )
        range_upper = _optional_number(
            payload,
            "display_range_upper",
            field="Plausible display range upper",
        )
        if (range_lower is None) != (range_upper is None):
            raise ValidationError(
                "Plausible display range lower and upper must be supplied together."
            )
        display_range = (
            None if range_lower is None or range_upper is None else (range_lower, range_upper)
        )

        return cls(
            effect_type=effect_type,
            estimate=_optional_number(payload, "estimate", field="Point estimate"),
            lower=_finite_number(payload["lower"], field="Lower 95% confidence limit"),
            upper=_finite_number(payload["upper"], field="Upper 95% confidence limit"),
            null_value=_optional_number(payload, "null_value", field="Null value"),
            thresholds=_thresholds(payload.get("thresholds")),
            display_range=display_range,
            grid_points=_grid_points(payload.get("grid_points", DEFAULT_GRID_POINTS)),
        )


class EffectSpecPayload(TypedDict):
    key: str
    label: str
    family: Literal["additive", "ratio"]
    working_scale: Literal["identity", "log"]
    default_null: float
    positive_only: bool


class MetaPayload(TypedDict):
    schema_version: int
    app_version: str
    core_version: str
    effect_spec: EffectSpecPayload
    estimate_source: Literal["inferred_from_ci", "provided_validated"]
    default_null_applied: bool
    grid_points: int
    display_axis_scale: Literal["identity", "natural"]
    display_range_active: bool
    display_range_display: list[float] | None
    display_range_working: list[float] | None


class ReconstructionPayload(TypedDict):
    estimate_display: float
    estimate_working: float
    provided_estimate_display: float | None
    provided_estimate_working: float | None
    reported_95_ci_display: list[float]
    reported_95_ci_working: list[float]
    null_display: float
    null_working: float
    standard_error_working: float
    standard_error_method: Literal["ci_width", "mean_side_se"]
    standard_error_lower_side: float
    standard_error_upper_side: float
    standard_error_from_width: float
    relative_asymmetry: float
    standardized_distance_at_null: float
    compatibility_at_null: float


class GridPayload(TypedDict):
    effect_display: list[float]
    effect_working: list[float]
    standardized_distance: list[float]
    compatibility: list[float]


class ThresholdPayload(TypedDict):
    effect_display: float
    effect_working: float
    standardized_distance: float
    compatibility: float
    relative_to_estimate: Literal["below_estimate", "at_estimate", "above_estimate"]
    relative_to_null: Literal["below_null", "at_null", "above_null"]
    inside_reported_95_ci: bool


class GuidePayload(TypedDict):
    label: Literal["90%", "95%", "99%"]
    compatibility: float


class IntervalsOrGuidesPayload(TypedDict):
    reported_95_ci_display: list[float]
    reported_95_ci_working: list[float]
    compatibility_guides: list[GuidePayload]


class WarningPayload(TypedDict):
    code: str
    message: str


class CompatibilityResponse(TypedDict):
    meta: MetaPayload
    reconstruction: ReconstructionPayload
    grid: GridPayload
    thresholds: list[ThresholdPayload]
    intervals_or_guides: IntervalsOrGuidesPayload
    warnings: list[WarningPayload]
