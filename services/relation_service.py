import pandas as pd

import store
from config import CARTESIAN_MAX, WITNESS_LIMIT
from services import analysis_service
from services.common import build_set, check_columns, is_missing, limit_preview, load_set, to_element
from utils import ApiError


def as_number(value):
    try:
        return float(value)
    except ValueError:
        return None


def compare(a, b, operator):
    number_a, number_b = as_number(a), as_number(b)
    left, right = (number_a, number_b) if number_a is not None and number_b is not None else (a, b)
    return operator(left, right)


def divides(a, b):
    number_a, number_b = as_number(a), as_number(b)
    return number_a is not None and number_b is not None and number_a.is_integer() and number_b.is_integer() and number_a != 0 and int(number_b) % int(number_a) == 0


RULES = {"equal": lambda a, b: a == b, "not_equal": lambda a, b: a != b, "less_than": lambda a, b: compare(a, b, lambda x, y: x < y), "less_or_equal": lambda a, b: compare(a, b, lambda x, y: x <= y), "greater_than": lambda a, b: compare(a, b, lambda x, y: x > y), "greater_or_equal": lambda a, b: compare(a, b, lambda x, y: x >= y), "divides": divides, "same_length": lambda a, b: len(a) == len(b), "same_first_letter": lambda a, b: bool(a and b) and a[0].lower() == b[0].lower()}


def pairs_from_rule(list_a, list_b, rule):
    if rule not in RULES:
        raise ApiError(f"Unknown rule: {rule}.")
    return [[a, b] for a in list_a for b in list_b if RULES[rule](a, b)]


def pairs_from_rows(df, column_a, column_b):
    check_columns(df, [column_a, column_b])
    rows = [[to_element(a), to_element(b)] for a, b in df[[column_a, column_b]].itertuples(index=False, name=None) if not is_missing(a) and not is_missing(b)]
    pairs = list(map(list, dict.fromkeys(map(tuple, rows))))
    list_a, _ = build_set(df, [column_a])
    list_b, _ = build_set(df, [column_b])
    return list_a, list_b, pairs


def validate_manual_pairs(list_a, list_b, pairs):
    valid = {(a, b) for a in list_a for b in list_b}
    clean = []
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2 or tuple(pair) not in valid:
            raise ApiError(f"Invalid pair: {pair}.")
        if pair not in clean:
            clean.append(pair)
    return clean


def base_set_of(list_a, list_b):
    return list(dict.fromkeys(list_a + list_b))


def is_reflexive(base_set, pair_set):
    witnesses = [[item, item] for item in base_set if (item, item) not in pair_set][:WITNESS_LIMIT]
    return not witnesses, witnesses


def is_symmetric(pair_set):
    witnesses = [[a, b] for a, b in pair_set if (b, a) not in pair_set][:WITNESS_LIMIT]
    return not witnesses, witnesses


def is_transitive(pair_set):
    links = {}
    for a, b in pair_set:
        links.setdefault(a, []).append(b)
    witnesses = []
    for a, b in pair_set:
        for c in links.get(b, []):
            if (a, c) not in pair_set:
                witnesses.append([a, b, c])
                if len(witnesses) == WITNESS_LIMIT:
                    return False, witnesses
    return not witnesses, witnesses


def build(payload):
    mode = payload.get("mode")
    if mode == "from_rows":
        record = store.get_dataset(payload.get("dataset_id", ""))
        list_a, list_b, pairs = pairs_from_rows(record["df"], payload.get("column_a"), payload.get("column_b"))
        label = f"Relation from rows: {record['name']}"
    else:
        list_a, _, name_a = load_set(payload.get("set_a"))
        list_b, _, name_b = load_set(payload.get("set_b"))
        if len(list_a) * len(list_b) > CARTESIAN_MAX:
            raise ApiError("Relation is too large. Maximum is 1,000,000 pairs.")
        pairs = pairs_from_rule(list_a, list_b, payload.get("rule")) if mode == "rule" else validate_manual_pairs(list_a, list_b, payload.get("pairs", [])) if mode == "manual" else None
        if pairs is None:
            raise ApiError(f"Unknown relation mode: {mode}.")
        label = f"{mode.title()} relation: {name_a} + {name_b}"
    base_set = base_set_of(list_a, list_b)
    stats = {"size_a": len(list_a), "size_b": len(list_b), "base_set_size": len(base_set), "pair_count": len(pairs)}
    summary = analysis_service.summarize("relation", stats)
    result_id = store.add_result("relation", label, pd.DataFrame(pairs, columns=["a", "b"]), stats, summary, {"pairs": pairs, "base_set": base_set})
    preview, truncated = limit_preview(pairs)
    return {"result_id": result_id, "kind": "relation", "mode": mode, "pairs": preview, "count": len(pairs), "truncated": truncated, "stats": stats, "summary": summary}


def check_properties(result_id):
    record = store.get_result(result_id)
    if record["kind"] != "relation":
        raise ApiError("Result is not a relation.")
    pairs = {tuple(pair) for pair in record["extra"]["pairs"]}
    base_set = record["extra"]["base_set"]
    reflexive = is_reflexive(base_set, pairs)
    symmetric = is_symmetric(pairs)
    transitive = is_transitive(pairs)
    equivalence = all(item[0] for item in [reflexive, symmetric, transitive])
    record["stats"].update({"reflexive": reflexive[0], "symmetric": symmetric[0], "transitive": transitive[0], "is_equivalence": equivalence})
    words = [name for name, item in [("reflexive", reflexive), ("symmetric", symmetric), ("transitive", transitive)] if item[0]]
    summary = f"The relation is {' and '.join(words) if words else 'not reflexive, symmetric, or transitive'}, so it is {'an' if equivalence else 'not an'} equivalence relation."
    return {"result_id": result_id, "base_set_size": len(base_set), "note": "Properties are checked on the base set A union B.", "reflexive": {"holds": reflexive[0], "witnesses": reflexive[1]}, "symmetric": {"holds": symmetric[0], "witnesses": symmetric[1]}, "transitive": {"holds": transitive[0], "witnesses": transitive[1]}, "is_equivalence": equivalence, "summary": summary}
