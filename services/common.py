import math

from config import PREVIEW_LIMIT, SET_SEPARATOR
from store import get_dataset
from utils import ApiError


def is_missing(value):
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    try:
        return bool(math.isnan(value))
    except (TypeError, ValueError):
        return False


def to_element(value):
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def check_columns(df, columns):
    if not columns:
        raise ApiError("Choose at least one column.")
    for column in columns:
        if column not in df.columns:
            raise ApiError(f"Column '{column}' not found in dataset.")


def build_set(df, columns):
    check_columns(df, columns)
    values = []
    missing_dropped = 0
    for row in df[columns].itertuples(index=False, name=None):
        if any(is_missing(value) for value in row):
            missing_dropped += 1
            continue
        values.append(SET_SEPARATOR.join(to_element(value) for value in row))
    elements = list(dict.fromkeys(values))
    return elements, {"rows": len(df), "missing_dropped": missing_dropped, "duplicates_removed": len(values) - len(elements)}


def load_set(spec):
    if not isinstance(spec, dict) or "dataset_id" not in spec or "columns" not in spec:
        raise ApiError("Set needs dataset_id and columns.")
    record = get_dataset(spec["dataset_id"])
    elements, info = build_set(record["df"], spec["columns"])
    return elements, info, record["name"]


def limit_preview(items):
    return items[:PREVIEW_LIMIT], len(items) > PREVIEW_LIMIT
