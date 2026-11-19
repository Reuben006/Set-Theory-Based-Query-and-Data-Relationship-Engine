# File Reference

| File or folder | Purpose |
| --- | --- |
| `app.py` | Flask application factory, routes, error handling, page serving |
| `config.py` | Shared limits and separators |
| `store.py` | In-memory datasets and saved results |
| `utils.py` | API error type, JSON envelope helpers, DataFrame row conversion |
| `routes/` | HTTP endpoint functions grouped by feature |
| `services/common.py` | Value cleaning and set construction |
| `services/dataset_service.py` | CSV loading, paging, quality report |
| `services/set_service.py` | Union, intersection, difference, symmetric difference |
| `services/cartesian_service.py` | Pair count, generation, warning behavior |
| `services/relation_service.py` | Rules, relation pairs, mathematical properties |
| `services/equivalence_service.py` | Classes from columns, rules, relations |
| `services/analysis_service.py` | Plain-English summaries and overview |
| `static/index.html` | Base page, tabs, script order |
| `static/partials/` | One HTML section per tab |
| `static/js/api.js` | Browser fetch helper and error handling |
| `static/js/ui.js` | Shared table, stats, toast, picker UI helpers |
| `static/js/*.js` | Per-feature tab behavior |
| `sample_data/` | Demo CSV files |
