function fieldError(control, message) {
  control.setAttribute("aria-invalid", "true");
  return { controlId: control.id, message };
}

function parseRequiredNumber(form, name, label) {
  const control = form.elements.namedItem(name);
  const value = control.value.trim();
  if (value === "") {
    return { error: fieldError(control, `${label} is required.`) };
  }
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return {
      error: fieldError(control, `${label} must be a finite number.`),
    };
  }
  return { value: parsed };
}

function parseOptionalNumber(form, name, label) {
  const control = form.elements.namedItem(name);
  const value = control.value.trim();
  if (value === "") {
    return { value: null };
  }
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return {
      error: fieldError(control, `${label} must be a finite number or blank.`),
    };
  }
  return { value: parsed };
}

function parseThresholds(form) {
  const control = form.elements.namedItem("thresholds");
  const text = control.value.trim();
  if (text === "") {
    return { value: [] };
  }
  const values = text.split(/[,\s]+/).map(Number);
  if (values.some((value) => !Number.isFinite(value))) {
    return {
      error: fieldError(
        control,
        "Reference thresholds must be finite numbers separated by commas or spaces.",
      ),
    };
  }
  return { value: values };
}

export function readRequest(form) {
  const estimate = parseOptionalNumber(form, "estimate", "Point estimate");
  const lower = parseRequiredNumber(form, "lower", "Lower 95% CI");
  const upper = parseRequiredNumber(form, "upper", "Upper 95% CI");
  const nullValue = parseOptionalNumber(form, "null_value", "Null value");
  const thresholds = parseThresholds(form);
  const rangeLower = parseOptionalNumber(
    form,
    "display_range_lower",
    "Plausible display range lower",
  );
  const rangeUpper = parseOptionalNumber(
    form,
    "display_range_upper",
    "Plausible display range upper",
  );
  const errors = [
    estimate.error,
    lower.error,
    upper.error,
    nullValue.error,
    thresholds.error,
    rangeLower.error,
    rangeUpper.error,
  ].filter(Boolean);

  if (
    errors.length === 0 &&
    (rangeLower.value === null) !== (rangeUpper.value === null)
  ) {
    const control =
      rangeLower.value === null
        ? form.elements.namedItem("display_range_lower")
        : form.elements.namedItem("display_range_upper");
    errors.push(
      fieldError(
        control,
        "Plausible display range lower and upper must be supplied together.",
      ),
    );
  }
  if (errors.length > 0) {
    return { errors, request: null };
  }

  const request = {
    effect_type: form.elements.namedItem("effect_type").value,
    estimate: estimate.value,
    lower: lower.value,
    upper: upper.value,
    null_value: nullValue.value,
    thresholds: thresholds.value,
    grid_points: Number(form.elements.namedItem("grid_points").value),
  };
  if (rangeLower.value !== null && rangeUpper.value !== null) {
    request.display_range_lower = rangeLower.value;
    request.display_range_upper = rangeUpper.value;
  }
  return { errors: [], request };
}

export function readDisplayOptions(form) {
  return {
    axisSpacing: form.elements.namedItem("axis_spacing").value,
    showGuides: form.elements.namedItem("show_guides").checked,
  };
}
