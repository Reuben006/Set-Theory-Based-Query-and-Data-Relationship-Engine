# Study Plan

## First 20 minutes

Run `python app.py`, upload both files in `sample_data/`, and try every visible tab. Start with the Datasets tab because every operation uses an uploaded dataset.

## Next 30 minutes

Read `app.py`, `config.py`, `store.py`, and `utils.py`. These four files explain server startup, shared limits, in-memory data, JSON responses, and errors.

## Next 40 minutes

Read `services/common.py`, then `dataset_service.py`, `set_service.py`, and `cartesian_service.py`. These are the easiest feature implementations.

## Final 30 minutes

Read `relation_service.py`, `equivalence_service.py`, `analysis_service.py`, then one route file and its matching JavaScript file. You will understand the complete request path.

## Demo order

Upload `students.csv` and `clubs.csv`. Show dataset quality. Run city union. Run department × club. Build an equal relation on ids. Check properties. Group students by city. Open Results and download one CSV.
