function formatNumber(value) {
  if (value === null || value === undefined) {
    return "not supplied";
  }
  const magnitude = Math.abs(value);
  if ((magnitude !== 0 && magnitude < 0.0001) || magnitude >= 1_000_000) {
    return Number(value).toExponential(5);
  }
  return Number(value).toLocaleString("en-US", {
    maximumSignificantDigits: 8,
  });
}

function formatCompatibility(value) {
  if (value === 0) {
    return "0 (below floating-point display precision)";
  }
  return Number(value).toLocaleString("en-US", {
    maximumSignificantDigits: 6,
  });
}

function formatRange(values) {
  return `${formatNumber(values[0])} to ${formatNumber(values[1])}`;
}

function locationLabel(value) {
  return value.replaceAll("_", " ");
}

function wrapPlotTitle(text, maxLineLength = 30) {
  const lines = [];
  let currentLine = "";
  for (const word of text.split(/\s+/)) {
    const candidate = currentLine ? `${currentLine} ${word}` : word;
    if (currentLine && candidate.length > maxLineLength) {
      lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine = candidate;
    }
  }
  if (currentLine) {
    lines.push(currentLine);
  }
  return lines.join("<br>");
}

export function buildSummary(response) {
  const reconstruction = response.reconstruction;
  return (
    `The null value ${formatNumber(reconstruction.null_display)} has compatibility ` +
    `${formatCompatibility(reconstruction.compatibility_at_null)} under the reconstructed ` +
    `Wald model. The curve peaks at the CI-implied estimate ` +
    `${formatNumber(reconstruction.estimate_display)}.`
  );
}

export function buildCaption(response, displayOptions) {
  const effect = response.meta.effect_spec;
  const reconstruction = response.reconstruction;
  const thresholds =
    response.thresholds.length === 0
      ? "No user reference thresholds are shown."
      : `User reference thresholds are marked at ${response.thresholds
          .map((row) => formatNumber(row.effect_display))
          .join(", ")}.`;
  const spacing =
    effect.family === "ratio"
      ? `${displayOptions.axisSpacing} natural-scale spacing`
      : "linear identity-scale spacing";
  return (
    `Figure. Wald compatibility curve for ${effect.label.toLowerCase()} reconstructed from ` +
    `the reported 95% confidence interval (${formatRange(
      reconstruction.reported_95_ci_display,
    )}). The CI-implied estimate is ${formatNumber(
      reconstruction.estimate_display,
    )}, and the null is ${formatNumber(reconstruction.null_display)}. ` +
    `Vertical markers identify the estimate, null, reported CI bounds, and supplied reference ` +
    `thresholds. The x-axis uses ${spacing}. ${thresholds} The curve is the two-sided Wald ` +
    `p-value function across candidate effects; it is not an exact profile likelihood or a ` +
    `posterior probability that an effect value is true.`
  );
}

function verticalShape(x, dash, color, width = 2) {
  return {
    type: "line",
    x0: x,
    x1: x,
    xref: "x",
    y0: 0,
    y1: 1,
    yref: "paper",
    line: { color, dash, width },
    layer: "above",
  };
}

function markerAnnotation(x, text, y, color) {
  return {
    x,
    xref: "x",
    y,
    yref: "paper",
    text,
    showarrow: false,
    font: { color, size: 13 },
    bgcolor: "rgba(255,255,255,0.88)",
    borderpad: 2,
  };
}

function plotLayout(response, displayOptions) {
  const reconstruction = response.reconstruction;
  const effect = response.meta.effect_spec;
  const ci = reconstruction.reported_95_ci_display;
  // Plotly log-axis annotations use log10 coordinates; shapes use data values.
  const annotationX = (value) =>
    effect.family === "ratio" && displayOptions.axisSpacing === "log"
      ? Math.log10(value)
      : value;
  const shapes = [
    {
      type: "rect",
      x0: ci[0],
      x1: ci[1],
      xref: "x",
      y0: 0,
      y1: 1,
      yref: "paper",
      fillcolor: "rgba(83,100,107,0.12)",
      line: { width: 0 },
      layer: "below",
    },
    verticalShape(ci[0], "dash", "#68777d", 1.5),
    verticalShape(ci[1], "dash", "#68777d", 1.5),
    verticalShape(reconstruction.estimate_display, "solid", "#006d77", 3),
    verticalShape(reconstruction.null_display, "dot", "#263238", 2.5),
    ...response.thresholds.map((row) =>
      verticalShape(row.effect_display, "dashdot", "#a44a3f", 2),
    ),
  ];
  const annotations = [
    markerAnnotation(
      annotationX(reconstruction.estimate_display),
      "CI-implied estimate",
      0.94,
      "#006d77",
    ),
    markerAnnotation(
      annotationX(reconstruction.null_display),
      "Null",
      0.86,
      "#263238",
    ),
    markerAnnotation(
      annotationX(reconstruction.estimate_display),
      "Reported 95% CI",
      0.08,
      "#59686e",
    ),
    ...response.thresholds.map((row, index) =>
      markerAnnotation(
        annotationX(row.effect_display),
        `Reference ${index + 1}`,
        0.76 - ((index % 4) * 0.09),
        "#8d3f36",
      ),
    ),
  ];

  if (displayOptions.showGuides) {
    for (const guide of response.intervals_or_guides.compatibility_guides) {
      shapes.push({
        type: "line",
        x0: 0,
        x1: 1,
        xref: "paper",
        y0: guide.compatibility,
        y1: guide.compatibility,
        yref: "y",
        line: { color: "#7a6a44", dash: "dot", width: 1.25 },
        layer: "below",
      });
      annotations.push({
        x: 1,
        xref: "paper",
        y: guide.compatibility,
        yref: "y",
        text: `${guide.label} guide`,
        showarrow: false,
        xanchor: "right",
        yanchor: "bottom",
        font: { color: "#625535", size: 12 },
        bgcolor: "rgba(255,255,255,0.82)",
      });
    }
  }

  const xRange = [
    response.grid.effect_display[0],
    response.grid.effect_display.at(-1),
  ];
  const displayedRange =
    xRange[0] === xRange[1]
      ? null
      : effect.family === "ratio" && displayOptions.axisSpacing === "log"
        ? xRange.map((value) => Math.log10(value))
        : xRange;

  return {
    title: {
      text: wrapPlotTitle(
        `Compatibility across candidate ${effect.label.toLowerCase()} values`,
      ),
      font: { size: 18 },
    },
    xaxis: {
      title: { text: effect.label },
      type:
        effect.family === "ratio" && displayOptions.axisSpacing === "log"
          ? "log"
          : "linear",
      ...(displayedRange ? { range: displayedRange } : {}),
      tickformat: "~g",
      automargin: true,
    },
    yaxis: {
      title: { text: "Compatibility / two-sided Wald p-value" },
      range: [0, 1.02],
      automargin: true,
      zeroline: false,
    },
    shapes,
    annotations,
    autosize: true,
    margin: { b: 104, l: 86, r: 34, t: 100 },
    paper_bgcolor: "#ffffff",
    plot_bgcolor: "#ffffff",
    font: { color: "#17202a", size: 14 },
    showlegend: false,
  };
}

function renderReconstruction(response, container) {
  const reconstruction = response.reconstruction;
  const rows = [
    ["CI-implied estimate", formatNumber(reconstruction.estimate_display)],
    ["Reported 95% CI", formatRange(reconstruction.reported_95_ci_display)],
    ["Null value", formatNumber(reconstruction.null_display)],
    [
      "Two-sided Wald p-value at null",
      formatCompatibility(reconstruction.compatibility_at_null),
    ],
    ["Working-scale SE", formatNumber(reconstruction.standard_error_working)],
    ["Working scale", response.meta.effect_spec.working_scale],
    [
      "Estimate source",
      response.meta.estimate_source === "provided_validated"
        ? "Provided estimate validated; CI midpoint used"
        : "Inferred from 95% CI midpoint",
    ],
  ];
  container.replaceChildren();
  for (const [label, value] of rows) {
    const wrapper = document.createElement("div");
    const term = document.createElement("dt");
    const description = document.createElement("dd");
    term.textContent = label;
    description.textContent = value;
    wrapper.append(term, description);
    container.append(wrapper);
  }
}

function renderThresholds(response, table, empty) {
  const body = table.querySelector("tbody");
  body.replaceChildren();
  for (const row of response.thresholds) {
    const tableRow = document.createElement("tr");
    const values = [
      formatNumber(row.effect_display),
      formatNumber(row.effect_working),
      formatCompatibility(row.compatibility),
      locationLabel(row.relative_to_estimate),
      locationLabel(row.relative_to_null),
      row.inside_reported_95_ci ? "Yes" : "No",
    ];
    values.forEach((text, index) => {
      const cell = document.createElement(index === 0 ? "th" : "td");
      if (index === 0) {
        cell.scope = "row";
      }
      cell.textContent = text;
      tableRow.append(cell);
    });
    body.append(tableRow);
  }
  table.hidden = response.thresholds.length === 0;
  empty.hidden = response.thresholds.length !== 0;
}

function renderWarnings(response, list, section) {
  list.replaceChildren();
  for (const warning of response.warnings) {
    const item = document.createElement("li");
    item.dataset.warningCode = warning.code;
    item.textContent = warning.message;
    list.append(item);
  }
  section.hidden = response.warnings.length === 0;
}

export async function renderResult(response, elements, displayOptions) {
  const summary = buildSummary(response);
  const caption = buildCaption(response, displayOptions);
  elements.summary.textContent = summary;
  elements.plotDescription.textContent =
    `${summary} Markers identify the estimate, null, reported CI bounds, and ` +
    `${response.thresholds.length} reference threshold(s).`;
  elements.caption.textContent = caption;
  renderReconstruction(response, elements.reconstruction);
  renderThresholds(response, elements.thresholdTable, elements.thresholdEmpty);
  renderWarnings(response, elements.warningList, elements.warningSection);

  if (!globalThis.Plotly) {
    throw new Error("The plotting library did not load.");
  }
  const trace = {
    type: "scatter",
    mode: "lines",
    x: response.grid.effect_display,
    y: response.grid.compatibility,
    customdata: response.grid.effect_working.map((working, index) => [
      working,
      response.grid.standardized_distance[index],
    ]),
    line: { color: "#006d77", width: 3 },
    hovertemplate:
      "Effect: %{x:.6g}<br>Working scale: %{customdata[0]:.6g}" +
      "<br>Standardized distance: %{customdata[1]:.5g}" +
      "<br>Compatibility: %{y:.5g}<extra></extra>",
  };
  await globalThis.Plotly.react(
    elements.plot,
    [trace],
    plotLayout(response, displayOptions),
    {
      displaylogo: false,
      responsive: true,
      scrollZoom: false,
      modeBarButtonsToRemove: ["lasso2d", "select2d"],
    },
  );
  elements.result.hidden = false;
  await new Promise((resolve) => globalThis.requestAnimationFrame(resolve));
  await globalThis.Plotly.Plots.resize(elements.plot);
  return { caption, summary };
}
