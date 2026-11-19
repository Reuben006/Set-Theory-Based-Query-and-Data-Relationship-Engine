# Code Walkthrough

## `app.py`

Imports load Flask, the upload limit, route blueprints, and API error helpers. `create_app()` makes the Flask object. `static_folder="static"` tells Flask where browser files live. The upload size expression converts megabytes to bytes. Each `register_blueprint` line mounts one API family below its URL prefix. The `/` function returns `static/index.html`. Error handlers convert custom errors, oversized uploads, and unexpected exceptions into consistent JSON responses. The final block starts the development server only when the file is run directly.

## `config.py`

Every line is a named constant. Preview and page constants prevent huge browser responses. Cartesian constants prevent accidental memory-heavy pair generation. The class and witness limits keep relation responses readable. `SET_SEPARATOR` is used when multiple columns form one set element.

## `store.py`

The first imports create readable timestamps and use `ApiError`. The four module variables are the in-memory state. `add_dataset` increments a counter, creates an id, and saves the DataFrame record. `get_dataset` validates ids. List and delete functions expose dataset records. Result functions repeat the same pattern for generated output. `clear_all` resets state. `timestamp` creates display timestamps.

## Service pattern

Every service accepts plain dictionaries, lists, or DataFrames and returns plain dictionaries. It never reads HTTP requests or creates HTML. That makes mathematical behavior independent from the browser.

## Browser pattern

`api.js` turns fetch calls into `Api.get`, `Api.post`, and `Api.upload`. `ui.js` renders repeatable visual pieces. A tab object such as `SetsTab` reads its own ids, sends an API request, and displays the returned summary, stats, preview table, and download link.
