# Architecture

```text
Browser
  static/index.html
  static/js/*.js
  static/partials/*.html
       ↓ fetch
Flask route
  routes/*.py
       ↓ plain Python values
Service
  services/*.py
       ↓
pandas + store.py
```

`app.py` creates Flask, registers API blueprints, serves the page, and translates errors into the common JSON envelope.

`routes/` contains small endpoint functions. Routes should only read request data, call a service, and return a response.

`services/` contains the real rules: cleaning values, set operations, products, relations, equivalence classes, and result summaries.

`store.py` is a module-level in-memory database. It assigns `d1`, `d2` to datasets and `r1`, `r2` to results.

`static/` is the browser interface. `app.js` loads partial HTML files and activates tab objects. Each tab JS file calls the matching API.
