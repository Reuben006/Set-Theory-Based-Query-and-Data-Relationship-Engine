import pandas as pd

import store
from config import CARTESIAN_MAX, CARTESIAN_WARN
from services import analysis_service
from services.common import limit_preview, load_set
from utils import ApiError


def count_pairs(list_a, list_b):
    return len(list_a) * len(list_b)


def make_pairs(list_a, list_b):
    return [[item_a, item_b] for item_a in list_a for item_b in list_b]


def generate(payload):
    confirm = bool(payload.get("confirm", False))
    list_a, _, name_a = load_set(payload["set_a"])
    list_b, _, name_b = load_set(payload["set_b"])
    if not list_a:
        raise ApiError("Set A is empty.")
    if not list_b:
        raise ApiError("Set B is empty.")
    total_pairs = count_pairs(list_a, list_b)
    if total_pairs > CARTESIAN_MAX:
        raise ApiError("Cartesian product is too large. Maximum is 1,000,000 pairs.")
    if total_pairs > CARTESIAN_WARN and not confirm:
        return {"warning": True, "total_pairs": total_pairs, "message": f"This will create {total_pairs:,} pairs. Send confirm=true to continue."}
    pairs = make_pairs(list_a, list_b)
    stats = {"size_a": len(list_a), "size_b": len(list_b), "pair_count": total_pairs}
    summary = analysis_service.summarize("cartesian", stats)
    result_id = store.add_result("cartesian", f"Cartesian product: {name_a} x {name_b}", pd.DataFrame(pairs, columns=["a", "b"]), stats, summary)
    preview, truncated = limit_preview(pairs)
    return {"warning": False, "result_id": result_id, "kind": "cartesian", "pairs": preview, "count": total_pairs, "truncated": truncated, "stats": stats, "summary": summary}
