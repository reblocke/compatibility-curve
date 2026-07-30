"""Focused browser contract for one-parameter Wald compatibility curves."""

from wald_inference import ValidationError

from .contract import calculate, calculate_json
from .models import CompatibilityRequest, CompatibilityResponse
from .version import __version__

__all__ = [
    "CompatibilityRequest",
    "CompatibilityResponse",
    "ValidationError",
    "__version__",
    "calculate",
    "calculate_json",
]
