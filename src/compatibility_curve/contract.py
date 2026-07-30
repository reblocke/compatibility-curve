"""Strict browser contract delegating all Wald calculations to ``wald-inference``."""

from __future__ import annotations

import json
import math

import numpy as np
from wald_inference import (
    ValidationError,
    build_grid,
    compatibility_curve,
    from_working_scale,
    get_effect_spec,
    max_safe_grid_span,
    reconstruct_wald_from_95_ci,
    standardized_distance,
    to_working_scale,
)
from wald_inference import (
    __version__ as CORE_VERSION,
)

from .models import (
    CompatibilityRequest,
    CompatibilityResponse,
    GuidePayload,
    ThresholdPayload,
    WarningPayload,
)
from .version import __version__

GUIDES: tuple[GuidePayload, ...] = (
    {"label": "90%", "compatibility": 0.10},
    {"label": "95%", "compatibility": 0.05},
    {"label": "99%", "compatibility": 0.01},
)
DEFAULT_GRID_SPAN_IN_STANDARD_ERRORS = 4.5


def _reject_nonstandard_constant(value: str) -> None:
    raise ValidationError(f"Non-finite JSON constant is not allowed: {value}.")


def _float_list(values: object) -> list[float]:
    return [float(value) for value in np.asarray(values, dtype=float).reshape(-1)]


def _strict_finite_tree(value: object, *, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            _strict_finite_tree(nested, path=f"{path}.{key}")
        return
    if isinstance(value, list | tuple):
        for index, nested in enumerate(value):
            _strict_finite_tree(nested, path=f"{path}[{index}]")
        return
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError(
            f"Computed response value at {path} exceeds the finite floating-point range."
        )


def _direction(
    value: float,
    reference: float,
    reference_name: str,
) -> str:
    if math.isclose(value, reference, rel_tol=1e-12, abs_tol=1e-12):
        return f"at_{reference_name}"
    return f"below_{reference_name}" if value < reference else f"above_{reference_name}"


def _display_values(effect_type: str, working_values: np.ndarray) -> tuple[np.ndarray, bool]:
    spec = get_effect_spec(effect_type)
    if spec.family == "additive":
        return np.asarray(from_working_scale(effect_type, working_values), dtype=float), False

    smallest_positive = float(np.nextafter(0.0, 1.0))
    lower_working = float(to_working_scale(effect_type, smallest_positive))
    upper_working = float(to_working_scale(effect_type, float(np.finfo(float).max)))
    safe_values = np.clip(working_values, lower_working, upper_working)
    clipped = bool(np.any(safe_values != working_values))
    return np.asarray(from_working_scale(effect_type, safe_values), dtype=float), clipped


def _warning(code: str, message: str) -> WarningPayload:
    return {"code": code, "message": message}


def _display_range_warnings(
    display_range_working: tuple[float, float] | None,
    *,
    estimate_working: float,
    lower_working: float,
    upper_working: float,
    null_working: float,
    thresholds_working: np.ndarray,
) -> list[WarningPayload]:
    if display_range_working is None:
        return []
    range_lower, range_upper = display_range_working

    def outside(value: float) -> bool:
        return value < range_lower or value > range_upper

    warnings: list[WarningPayload] = []
    if outside(estimate_working):
        warnings.append(
            _warning("display_excludes_estimate", "The chosen display range excludes the estimate.")
        )
    if outside(lower_working):
        warnings.append(
            _warning(
                "display_excludes_lower_ci",
                "The chosen display range excludes the lower 95% CI bound.",
            )
        )
    if outside(upper_working):
        warnings.append(
            _warning(
                "display_excludes_upper_ci",
                "The chosen display range excludes the upper 95% CI bound.",
            )
        )
    if outside(null_working):
        warnings.append(
            _warning("display_excludes_null", "The chosen display range excludes the null value.")
        )
    if any(outside(float(value)) for value in thresholds_working):
        warnings.append(
            _warning(
                "display_excludes_threshold",
                "The chosen display range excludes one or more reference thresholds / MCIDs.",
            )
        )
    return warnings


def calculate(request: CompatibilityRequest) -> CompatibilityResponse:
    """Construct one focused compatibility-curve response."""

    spec = get_effect_spec(request.effect_type)
    reconstruction = reconstruct_wald_from_95_ci(
        effect_type=request.effect_type,
        estimate=request.estimate,
        lower=request.lower,
        upper=request.upper,
        null_value=request.null_value,
    )

    thresholds_display = np.asarray(request.thresholds, dtype=float)
    thresholds_working = np.asarray(
        to_working_scale(request.effect_type, thresholds_display),
        dtype=float,
    )

    display_range_working: tuple[float, float] | None = None
    safe_span: float | None = None
    if request.display_range is None:
        natural_axis_upper_bound = (
            float(to_working_scale(request.effect_type, float(np.finfo(float).max)))
            if spec.family == "ratio"
            else None
        )
        safe_span = max_safe_grid_span(
            reconstruction.estimate_working,
            reconstruction.standard_error,
            natural_axis_upper_bound=natural_axis_upper_bound,
        )
        included = np.asarray(
            [reconstruction.null_working, *thresholds_working],
            dtype=float,
        )
        grid_working = build_grid(
            reconstruction.estimate_working,
            reconstruction.standard_error,
            n=request.grid_points,
            include_values=included,
            max_span=safe_span,
        )
    else:
        range_lower, range_upper = request.display_range
        if range_lower >= range_upper:
            raise ValidationError(
                "Plausible display range lower must be less than plausible display range upper."
            )
        transformed = np.asarray(
            to_working_scale(request.effect_type, request.display_range),
            dtype=float,
        )
        display_range_working = (float(transformed[0]), float(transformed[1]))
        grid_working = np.linspace(
            display_range_working[0],
            display_range_working[1],
            num=request.grid_points,
            dtype=float,
        )

    z_values = np.asarray(
        standardized_distance(
            grid_working,
            reconstruction.estimate_working,
            reconstruction.standard_error,
        ),
        dtype=float,
    )
    compatibility_values = np.asarray(
        compatibility_curve(
            grid_working,
            reconstruction.estimate_working,
            reconstruction.standard_error,
        ),
        dtype=float,
    )

    candidate_working = np.asarray(
        [reconstruction.null_working, *thresholds_working],
        dtype=float,
    )
    candidate_z = np.asarray(
        standardized_distance(
            candidate_working,
            reconstruction.estimate_working,
            reconstruction.standard_error,
        ),
        dtype=float,
    )
    candidate_compatibility = np.asarray(
        compatibility_curve(
            candidate_working,
            reconstruction.estimate_working,
            reconstruction.standard_error,
        ),
        dtype=float,
    )

    grid_display, display_clipped = _display_values(request.effect_type, grid_working)
    if request.display_range is not None:
        grid_display[0], grid_display[-1] = request.display_range

    warnings = [_warning("wald_reconstruction", message) for message in reconstruction.warnings]
    grid_was_truncated = safe_span is not None and (
        safe_span / reconstruction.standard_error < DEFAULT_GRID_SPAN_IN_STANDARD_ERRORS
        or any(
            value < float(grid_working[0]) or value > float(grid_working[-1])
            for value in candidate_working
        )
    )
    if grid_was_truncated:
        warnings.append(
            _warning(
                "grid_truncated",
                "Grid expansion was truncated to keep the plotted payload finite. "
                "An extreme null or reference threshold may fall outside the x-axis.",
            )
        )
    if safe_span == 0.0:
        warnings.append(
            _warning(
                "grid_collapsed",
                "The estimate is at the finite working-scale boundary, so the x-grid "
                "collapses to the estimate.",
            )
        )
    warnings.extend(
        _display_range_warnings(
            display_range_working,
            estimate_working=reconstruction.estimate_working,
            lower_working=reconstruction.lower_working,
            upper_working=reconstruction.upper_working,
            null_working=reconstruction.null_working,
            thresholds_working=thresholds_working,
        )
    )
    if display_clipped:
        warnings.append(
            _warning(
                "natural_axis_clipped",
                "Natural-axis x-values were clipped to finite positive values. "
                "Working-scale calculations are unchanged.",
            )
        )

    threshold_rows: list[ThresholdPayload] = []
    for index, (display, working) in enumerate(
        zip(thresholds_display, thresholds_working, strict=True),
        start=1,
    ):
        threshold_rows.append(
            {
                "effect_display": float(display),
                "effect_working": float(working),
                "standardized_distance": float(candidate_z[index]),
                "compatibility": float(candidate_compatibility[index]),
                "relative_to_estimate": _direction(
                    float(working),
                    reconstruction.estimate_working,
                    "estimate",
                ),
                "relative_to_null": _direction(
                    float(working),
                    reconstruction.null_working,
                    "null",
                ),
                "inside_reported_95_ci": (
                    reconstruction.lower_working <= float(working) <= reconstruction.upper_working
                ),
            }
        )

    response: CompatibilityResponse = {
        "meta": {
            "schema_version": 1,
            "app_version": __version__,
            "core_version": CORE_VERSION,
            "effect_spec": {
                "key": spec.key,
                "label": spec.label,
                "family": spec.family,
                "working_scale": spec.working_scale,
                "default_null": spec.default_null,
                "positive_only": spec.positive_only,
            },
            "estimate_source": reconstruction.estimate_source,
            "default_null_applied": reconstruction.default_null_applied,
            "grid_points": len(grid_working),
            "display_axis_scale": "natural" if spec.family == "ratio" else "identity",
            "display_range_active": request.display_range is not None,
            "display_range_display": (
                None
                if request.display_range is None
                else [float(value) for value in request.display_range]
            ),
            "display_range_working": (
                None
                if display_range_working is None
                else [float(value) for value in display_range_working]
            ),
        },
        "reconstruction": {
            "estimate_display": reconstruction.estimate_display,
            "estimate_working": reconstruction.estimate_working,
            "provided_estimate_display": reconstruction.provided_estimate_display,
            "provided_estimate_working": reconstruction.provided_estimate_working,
            "reported_95_ci_display": [
                reconstruction.lower_display,
                reconstruction.upper_display,
            ],
            "reported_95_ci_working": [
                reconstruction.lower_working,
                reconstruction.upper_working,
            ],
            "null_display": reconstruction.null_display,
            "null_working": reconstruction.null_working,
            "standard_error_working": reconstruction.standard_error,
            "standard_error_method": reconstruction.se_method,
            "standard_error_lower_side": reconstruction.se_lower,
            "standard_error_upper_side": reconstruction.se_upper,
            "standard_error_from_width": reconstruction.se_width,
            "relative_asymmetry": reconstruction.relative_asymmetry,
            "standardized_distance_at_null": float(candidate_z[0]),
            "compatibility_at_null": float(candidate_compatibility[0]),
        },
        "grid": {
            "effect_display": _float_list(grid_display),
            "effect_working": _float_list(grid_working),
            "standardized_distance": _float_list(z_values),
            "compatibility": _float_list(compatibility_values),
        },
        "thresholds": threshold_rows,
        "intervals_or_guides": {
            "reported_95_ci_display": [
                reconstruction.lower_display,
                reconstruction.upper_display,
            ],
            "reported_95_ci_working": [
                reconstruction.lower_working,
                reconstruction.upper_working,
            ],
            "compatibility_guides": [dict(guide) for guide in GUIDES],
        },
        "warnings": warnings,
    }
    _strict_finite_tree(response)
    return response


def calculate_json(request_json: str) -> str:
    """Validate strict JSON and return strict JSON for the worker boundary."""

    try:
        payload = json.loads(request_json, parse_constant=_reject_nonstandard_constant)
    except json.JSONDecodeError as exc:
        raise ValidationError("Request must be valid JSON.") from exc
    response = calculate(CompatibilityRequest.from_mapping(payload))
    return json.dumps(
        response,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
    )
