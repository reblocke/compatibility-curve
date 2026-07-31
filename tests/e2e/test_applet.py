from __future__ import annotations

import struct
from pathlib import Path

from playwright.sync_api import Page, expect


def _ready(page: Page, app_url: str) -> None:
    page.goto(app_url)
    expect(page.locator("#runtime-status")).to_have_attribute(
        "data-state",
        "ready",
        timeout=120_000,
    )


def _png_dimensions(path: Path) -> tuple[int, int]:
    contents = path.read_bytes()
    assert contents.startswith(b"\x89PNG\r\n\x1a\n")
    return struct.unpack(">II", contents[16:24])


def _assert_plot_titles_contained(page: Page) -> None:
    title_bounds = page.locator("#plot").evaluate(
        """
        (plot) => {
          const plotBounds = plot.getBoundingClientRect();
          return Array.from(plot.querySelectorAll(".gtitle")).map((title) => {
            const bounds = title.getBoundingClientRect();
            return {
              left: bounds.left,
              right: bounds.right,
              plotLeft: plotBounds.left,
              plotRight: plotBounds.right,
              viewportWidth: window.innerWidth,
            };
          });
        }
        """
    )
    assert title_bounds
    for bounds in title_bounds:
        assert bounds["left"] >= bounds["plotLeft"] - 1
        assert bounds["right"] <= bounds["plotRight"] + 1
        assert bounds["left"] >= -1
        assert bounds["right"] <= bounds["viewportWidth"] + 1


def test_worker_loads_and_calculates(page: Page, app_url: str) -> None:
    _ready(page, app_url)

    page.locator("#thresholds").fill("1.25")
    page.locator("#calculate").click()

    expect(page.locator("#runtime-status")).to_have_text("Compatibility curve updated.")
    expect(page.locator("#result-summary")).to_contain_text(
        "null value 1 has compatibility 0.00449326"
    )
    expect(page.locator("#threshold-table tbody tr")).to_have_count(1)
    expect(page.locator("#threshold-table tbody tr")).to_contain_text("0.0779619")
    expect(page.locator("#plot .plot-container")).to_be_visible()
    for label in [
        "CI-implied estimate",
        "Null",
        "Reported 95% CI",
        "Reference 1",
        "90% guide",
    ]:
        expect(page.locator("#plot .annotation-text").filter(has_text=label)).to_be_visible()
    expect(page.locator("#reconstruction-summary")).to_contain_text("1.8")
    expect(page.locator("#runtime-versions")).to_contain_text("compatibility-curve 0.1.4")
    expect(page.locator("#runtime-versions")).to_contain_text("wald-inference 0.4.2")
    expect(page.locator("#core-version")).to_have_text("wald-inference core 0.4.2")


def test_additive_case_and_effect_specific_controls(page: Page, app_url: str) -> None:
    _ready(page, app_url)
    page.locator("#effect-type").select_option("mean_difference")
    expect(page.locator("#axis-spacing-group")).to_be_hidden()
    page.locator("#ci-lower").fill("0.11")
    page.locator("#ci-upper").fill("0.73")
    page.locator("#thresholds").fill("0.2")
    page.locator("#calculate").click()

    expect(page.locator("#runtime-status")).to_have_text("Compatibility curve updated.")
    expect(page.locator("#result-summary")).to_contain_text("0.00792062")
    expect(page.locator("#reconstruction-summary")).to_contain_text("0.15816617")
    expect(page.locator("#threshold-table tbody tr")).to_contain_text("0.164243")
    expect(page.locator("#threshold-table tbody tr")).to_contain_text("Yes")


def test_validation_error_and_worker_recovery(page: Page, app_url: str) -> None:
    _ready(page, app_url)
    page.locator("#ci-lower").fill("-1")
    page.locator("#calculate").click()

    expect(page.locator("#error-summary")).to_contain_text("strictly positive")
    expect(page.locator("#runtime-status")).to_have_attribute("data-state", "error")
    expect(page.locator("#error-summary")).not_to_contain_text("Traceback")
    expect(page.locator("#error-summary")).not_to_contain_text("/Users/")

    page.locator("#ci-lower").fill("1.2")
    page.locator("#calculate").click()

    expect(page.locator("#runtime-status")).to_have_text("Compatibility curve updated.")
    expect(page.locator("#result-summary")).to_contain_text("1.8")


def test_input_errors_link_to_controls(page: Page, app_url: str) -> None:
    _ready(page, app_url)
    page.locator("#ci-lower").fill("")
    page.locator("#calculate").click()

    expect(page.locator("#error-summary")).to_be_visible()
    expect(page.locator("#error-summary a")).to_have_attribute("href", "#ci-lower")
    expect(page.locator("#ci-lower")).to_have_attribute("aria-invalid", "true")
    page.locator("#error-summary a").click()
    expect(page.locator("#ci-lower")).to_be_focused()


def test_presentation_range_does_not_change_summary(page: Page, app_url: str) -> None:
    _ready(page, app_url)
    page.locator("#thresholds").fill("1.25")
    page.locator("#calculate").click()
    expect(page.locator("#runtime-status")).to_have_text("Compatibility curve updated.")
    summary = page.locator("#reconstruction-summary").inner_text()

    page.locator("#display-range-lower").fill("0.9")
    page.locator("#display-range-upper").fill("1.1")
    page.locator("#calculate").click()

    expect(page.locator("#runtime-status")).to_have_text("Compatibility curve updated.")
    assert page.locator("#reconstruction-summary").inner_text() == summary
    expect(page.locator("#warnings-list li")).to_have_count(4)
    expect(page.locator("#warnings-list")).to_contain_text("excludes the estimate")
    expect(page.locator("#warnings-list")).to_contain_text("reference thresholds")


def test_csv_png_and_caption_exports(page: Page, app_url: str, tmp_path: Path) -> None:
    page.context.grant_permissions(
        ["clipboard-read", "clipboard-write"], origin=app_url.rstrip("/")
    )
    _ready(page, app_url)
    page.locator("#thresholds").fill("1.25")
    page.locator("#calculate").click()
    expect(page.locator("#runtime-status")).to_have_text("Compatibility curve updated.")

    with page.expect_download() as csv_info:
        page.locator("#export-csv").click()
    csv_download = csv_info.value
    csv_path = tmp_path / csv_download.suggested_filename
    csv_download.save_as(csv_path)
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == ("effect_display,effect_working,standardized_distance,compatibility")
    assert len(lines) == 802
    assert csv_download.suggested_filename == "wald-compatibility-curve.csv"

    for selector, suffix, dimensions in [
        ("#export-manuscript", "-manuscript.png", (2800, 2000)),
        ("#export-dashboard", "-dashboard.png", (1600, 1200)),
    ]:
        with page.expect_download(timeout=60_000) as png_info:
            page.locator(selector).click()
        download = png_info.value
        png_path = tmp_path / download.suggested_filename
        download.save_as(png_path)
        assert download.suggested_filename.endswith(suffix)
        assert _png_dimensions(png_path) == dimensions

    page.locator("#copy-caption").click()
    expect(page.locator("#runtime-status")).to_have_text("Caption copied.")
    clipboard = page.evaluate("navigator.clipboard.readText()")
    assert "reported 95% confidence interval (1.2 to 2.7)" in clipboard
    assert "not an exact profile likelihood" in clipboard
    assert "posterior probability" in clipboard


def test_mobile_keyboard_and_privacy_smoke(page: Page, app_url: str) -> None:
    requests: list[tuple[str, str | None]] = []
    page.context.on("request", lambda request: requests.append((request.url, request.post_data)))
    page.set_viewport_size({"width": 390, "height": 844})
    _ready(page, app_url)
    initial_url = page.url
    page.locator("#ci-lower").fill("1.234567891")
    page.locator("#effect-type").focus()
    page.keyboard.press("Tab")
    expect(page.locator("#estimate")).to_be_focused()
    page.keyboard.press("Tab")
    expect(page.locator("#ci-lower")).to_be_focused()
    page.locator("#calculate").click()
    expect(page.locator("#runtime-status")).to_have_text("Compatibility curve updated.")

    assert page.url == initial_url
    assert page.evaluate("localStorage.length") == 0
    assert page.evaluate("sessionStorage.length") == 0
    assert page.evaluate("document.cookie") == ""
    assert (
        page.evaluate("indexedDB.databases ? indexedDB.databases().then((rows) => rows.length) : 0")
        == 0
    )
    serialized_requests = "\n".join(f"{url}\n{body or ''}" for url, body in requests)
    assert "1.234567891" not in serialized_requests
    expect(page.locator(".controls")).to_be_visible()
    expect(page.locator(".results")).to_be_visible()
    assert page.evaluate(
        "document.documentElement.scrollWidth <= document.documentElement.clientWidth"
    )
    effect_options = page.locator("#effect-type option").evaluate_all(
        """
        (options) => options.map((option) => ({
          label: option.textContent.trim(),
          value: option.value,
        }))
        """
    )
    assert effect_options
    for option in effect_options:
        page.locator("#effect-type").select_option(str(option["value"]))
        page.locator("#calculate").click()
        expect(page.locator("#runtime-status")).to_have_text("Compatibility curve updated.")
        expect(page.locator("#plot .gtitle")).to_contain_text(str(option["label"]).lower())
        _assert_plot_titles_contained(page)
