import pandas as pd

import store
from services import analysis_service
from services.common import limit_preview, load_set
from utils import ApiError


def run_operation(operation, list_a, list_b):
    values_a = set(list_a)
    values_b = set(list_b)
    if operation == "union":
        return list_a + [item for item in list_b if item not in values_a]
    if operation == "intersection":
        return [item for item in list_a if item in values_b]
    if operation == "difference":
        return [item for item in list_a if item not in values_b]
    if operation == "symmetric_difference":
        return [item for item in list_a if item not in values_b] + [item for item in list_b if item not in values_a]
    raise ApiError(f"Unknown operation: {operation}.")


def compute_stats(list_a, list_b, result, info_a, info_b):
    values_b = set(list_b)
    values_a = set(list_a)
    common_count = sum(item in values_b for item in list_a)
    return {"rows_a": info_a["rows"], "rows_b": info_b["rows"], "size_a": len(list_a), "size_b": len(list_b), "total_before": len(list_a) + len(list_b), "total_after": len(result), "common_count": common_count, "only_a_count": len(list_a) - common_count, "only_b_count": len(list_b) - common_count}


def preview_set(payload):
    elements, info, _ = load_set(payload)
    preview, truncated = limit_preview(elements)
    return {"elements": preview, "count": len(elements), "truncated": truncated, "info": info}


def operate(payload):
    list_a, info_a, name_a = load_set(payload["set_a"])
    list_b, info_b, name_b = load_set(payload["set_b"])
    if len(payload["set_a"]["columns"]) != len(payload["set_b"]["columns"]):
        raise ApiError("Set A and set B must use the same number of columns.")
    result = run_operation(payload["operation"], list_a, list_b)
    stats = compute_stats(list_a, list_b, result, info_a, info_b)
    stats["operation"] = {"union": "Union", "intersection": "Intersection", "difference": "Difference (A - B)", "symmetric_difference": "Symmetric difference"}.get(payload["operation"], payload["operation"])
    summary = analysis_service.summarize("set_operation", stats)
    result_id = store.add_result("set_operation", f"{stats['operation']}: {name_a} + {name_b}", pd.DataFrame({"element": result}), stats, summary)
    preview, truncated = limit_preview(result)
    return {"result_id": result_id, "kind": "set_operation", "operation": payload["operation"], "elements": preview, "count": len(result), "truncated": truncated, "stats": stats, "summary": summary}
