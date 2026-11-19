import pandas as pd

import store
from services import analysis_service
from services.common import check_columns, is_missing, limit_preview, to_element
from utils import ApiError, df_to_rows


def prepare_keys(df, columns):
    result = df.copy()
    for column in columns:
        result[column] = result[column].map(lambda value: None if is_missing(value) else to_element(value))
    return result


def run_join(left_df, right_df, left_on, right_on, how):
    left = prepare_keys(left_df, left_on)
    right = prepare_keys(right_df, right_on).dropna(subset=right_on)
    if how == "left_anti":
        right_keys = key_set(right, right_on)
        keep = [key not in right_keys for key in left[left_on].itertuples(index=False, name=None)]
        return left[keep]
    return pd.merge(left, right, left_on=left_on, right_on=right_on, how=how, suffixes=("_left", "_right"))


def key_set(df, columns):
    return {tuple(row) for row in df[columns].itertuples(index=False, name=None) if not any(is_missing(value) for value in row)}


def join_stats(left_df, right_df, left_on, right_on, result_df):
    left_keys = key_set(prepare_keys(left_df, left_on), left_on)
    right_keys = key_set(prepare_keys(right_df, right_on), right_on)
    return {"left_rows": len(left_df), "right_rows": len(right_df), "result_rows": len(result_df), "matched_keys": len(left_keys & right_keys), "left_only_keys": len(left_keys - right_keys), "right_only_keys": len(right_keys - left_keys)}


def join(payload):
    left_spec, right_spec = payload["left"], payload["right"]
    left_record = store.get_dataset(left_spec.get("dataset_id", ""))
    right_record = store.get_dataset(right_spec.get("dataset_id", ""))
    left_on, right_on, how = left_spec.get("on", []), right_spec.get("on", []), payload.get("how")
    check_columns(left_record["df"], left_on)
    check_columns(right_record["df"], right_on)
    if len(left_on) != len(right_on):
        raise ApiError("Left and right key lists must have the same length.")
    if how not in ["inner", "left", "right", "outer", "left_anti"]:
        raise ApiError(f"Unknown join type: {how}.")
    result = run_join(left_record["df"], right_record["df"], left_on, right_on, how)
    stats = join_stats(left_record["df"], right_record["df"], left_on, right_on, result)
    stats["how"] = how
    summary = analysis_service.summarize("join", stats)
    result_id = store.add_result("join", f"{how.title()} join: {left_record['name']} + {right_record['name']}", result, stats, summary)
    rows = df_to_rows(result)
    preview, truncated = limit_preview(rows)
    return {"result_id": result_id, "kind": "join", "how": how, "columns": list(result.columns), "rows": preview, "count": len(rows), "truncated": truncated, "stats": stats, "summary": summary}
