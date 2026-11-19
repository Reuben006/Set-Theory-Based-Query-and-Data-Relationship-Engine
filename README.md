# Set Theory Based Query and Data Relationship Engine

A small, local web app that turns CSV columns into mathematical sets. It is designed for students and teachers who want to explore set theory using real tabular data rather than abstract examples alone.

Upload CSV files, choose columns, and explore unions, intersections, Cartesian products, relations, equivalence classes, and database joins from one simple browser interface.

## Features

| Area | What you can do |
| --- | --- |
| Datasets | Upload CSV files, preview rows, inspect column types, missing values, and duplicates |
| Sets | Union, intersection, difference, and symmetric difference |
| Cartesian product | Generate ordered pairs with safety limits for large products |
| Relations | Build a relation from rows, a mathematical rule, or manual pairs |
| Relation properties | Check reflexivity, symmetry, transitivity, and equivalence status with witnesses |
| Equivalence classes | Group by a column, grouping rule, or stored equivalence relation |
| Joins | Inner, left, right, outer, and left-anti joins with distinct-key statistics |
| Results | Review generated results and download them as CSV files |

## Tech stack

- Python
- Flask
- pandas
- Plain HTML, CSS, and JavaScript

There is no database, npm setup, frontend framework, or external service. Data stays in memory while the app is running and is cleared when the server stops.

## Run locally

```powershell
git clone https://github.com/v1haan24/Set-Theory-Based-Query-and-Data-Relationship-Engine.git
cd Set-Theory-Based-Query-and-Data-Relationship-Engine
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

If `python` points to the Microsoft Store placeholder on Windows, use the full path to your installed Python executable instead.

## Quick demo

1. Open the **Datasets** tab.
2. Upload `sample_data/students.csv` and `sample_data/clubs.csv`.
3. In **Sets**, compare the `city` column from both files.
4. In **Cartesian**, generate `dept × club`.
5. In **Relations**, build the `equal` rule using `id` against `id`, then check its properties.
6. In **Classes**, group `students.csv` by `city`.
7. In **Joins**, run an inner join on `id`.

## Project structure

```text
app.py                 Flask application and route registration
routes/                Thin HTTP request handlers
services/              Set theory, relation, join, and data logic
static/                Browser interface: HTML, CSS, and JavaScript
sample_data/           Ready-to-use example CSV files
store.py               In-memory datasets and saved results
```

The code follows a small, readable path:

```text
Browser UI → Flask route → service function → pandas / in-memory store
```

## Important behavior

- Set elements are cleaned into strings and retain first-appearance order.
- Empty and blank values are ignored while building sets.
- Multi-column sets join each row's values with ` | `.
- Cartesian products above 10,000 pairs require confirmation; products above 1,000,000 pairs are refused.
- Exports include full results even when the browser preview is limited.

## Sample data

`students.csv` intentionally contains one duplicate row and one missing mark, so it is useful for trying the data-quality panel. `clubs.csv` shares a few IDs and cities with it, making it useful for set operations and joins.

## Learning order

For a quick code walkthrough, start with `app.py`, then read `routes/datasets.py`, `services/dataset_service.py`, `store.py`, and finally `static/js/datasets.js`. The other feature areas follow the same pattern.
