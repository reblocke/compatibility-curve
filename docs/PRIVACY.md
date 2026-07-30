# Privacy

## Intended data

The app needs only aggregate, published, or synthetic effect estimates, 95% confidence limits,
null values, and reference thresholds. It is not designed to receive protected health
information, direct identifiers, patient-level records, free-text clinical notes, or uploads.
Do not enter such data.

## Data flow

Input is read by the page, sent through `postMessage` to a same-origin Web Worker, processed by
Python in Pyodide, and returned to the page for display/export. Values exist only in transient
page and worker memory.

The app has:

- no backend, server-side calculation, or database;
- no telemetry, analytics, or crash-reporting service;
- no local storage, session storage, IndexedDB, service-worker cache, or hidden persistence;
- no input values in URL query strings or fragments;
- no cookies, accounts, saved links, or shared-state feature;
- no application logging of inputs or protected health information;
- no upload path.

## Static network requests

The browser fetches the static page, CSS, JavaScript, generated Python files, Plotly, and
Pyodide-provided packages. User-entered values are not placed in request URLs, headers, or
bodies. CDN operators can observe ordinary network metadata such as IP address and requested
asset, but not values entered into the form.

Automated tests inspect requests after a distinctive input value and fail if it appears in any
URL or body.

## Exports and clipboard

CSV and PNG files are generated locally after an explicit button press. The browser's normal
download behavior determines where files are saved; the app does not upload or retain them.
The figure caption is written to the clipboard only after the copy button is selected.

Exported files can reveal the aggregate values a user entered. Users are responsible for where
downloads and copied text are subsequently stored or shared.

## Change boundary

Any proposed backend, storage, analytics, sharing, upload, account, or user-generated URL feature
requires a new documented data-flow and privacy review before implementation. New examples,
fixtures, logs, dependencies, exports, and deployments must remain synthetic or aggregate and
must not introduce PHI.
