# Feature Flows

## Upload

The browser sends multipart data to `POST /api/datasets`. `routes/datasets.py` calls `dataset_service.read_csv_file`. pandas reads the CSV, `store.add_dataset` saves the DataFrame, and the route returns `d1` style metadata.

## Set operation

The browser sends two set specifications to `/api/sets/operate`. A specification contains a dataset id and selected columns. `common.build_set` removes missing values, converts values to strings, removes duplicates, and preserves first appearance. `set_service.run_operation` produces the requested mathematical result.

## Cartesian product

`cartesian_service.generate` builds pair `[a, b]` values only after checking the pair count. More than 10,000 pairs requires confirmation. More than 1,000,000 is refused.

## Relation

A relation is a subset of A × B. `relation_service` can create pairs from table rows or a rule such as equal or less-or-equal. Properties are checked on A ∪ B. Witnesses explain failures.

## Equivalence classes

`equivalence_service` groups members by a shared key. A key can be a dataset column, a rule, or an equivalence relation. Each class is exported as class id, key, and member.

## Results and export

Each successful operation stores a full DataFrame in `store.py`. The browser sees only a preview. `routes/export.py` writes the full result as UTF-8 CSV.
