import pandas as pd

import store
from config import CLASS_MEMBERS_LIMIT
from services import analysis_service, relation_service
from services.common import build_set, check_columns, is_missing, to_element
from utils import ApiError


def mod_n(element, param):
    try:
        number = float(element)
    except ValueError:
        raise ApiError(f"'{element}' is not a whole number.")
    if not number.is_integer():
        raise ApiError(f"'{element}' is not a whole number.")
    if not isinstance(param, int) or param < 2:
        raise ApiError("mod_n needs an integer parameter of at least 2.")
    return str(int(number) % param)


KEY_RULES = {"same_value": lambda element, param: element, "same_length": lambda element, param: str(len(element)), "first_letter": lambda element, param: element[0].lower(), "last_char": lambda element, param: element[-1].lower(), "lowercase": lambda element, param: element.lower(), "mod_n": mod_n}


def group_by_key(items, key_function):
    classes = {}
    for item in items:
        classes.setdefault(key_function(item), []).append(item)
    return classes


def classes_from_column(df, group_column, member_column):
    check_columns(df, [group_column])
    if member_column:
        check_columns(df, [member_column])
    classes = {}
    for index, row in df.iterrows():
        key = row[group_column]
        if is_missing(key):
            continue
        member = row[member_column] if member_column else index + 1
        if not is_missing(member):
            classes.setdefault(to_element(key), []).append(to_element(member))
    return classes


def classes_from_rule(elements, rule, param):
    if rule not in KEY_RULES:
        raise ApiError(f"Unknown rule: {rule}.")
    return group_by_key(elements, lambda element: KEY_RULES[rule](element, param))


def classes_from_relation(result_id):
    properties = relation_service.check_properties(result_id)
    for name in ["reflexive", "symmetric", "transitive"]:
        if not properties[name]["holds"]:
            raise ApiError(f"This relation is not an equivalence relation: it is not {name}.")
    record = store.get_result(result_id)
    pairs = record["extra"]["pairs"]
    classes = {}
    for element in record["extra"]["base_set"]:
        members = [b for a, b in pairs if a == element]
        if tuple(members) not in [tuple(values) for values in classes.values()]:
            classes[members[0]] = members
    return classes


def is_partition(classes, total_elements):
    members = [member for values in classes.values() for member in values]
    return len(members) == total_elements and len(members) == len(set(members))


def find_classes(payload):
    mode = payload.get("mode")
    if mode == "column":
        record = store.get_dataset(payload.get("dataset_id", ""))
        classes = classes_from_column(record["df"], payload.get("group_column"), payload.get("member_column"))
        label = f"Classes by column: {record['name']}"
    elif mode == "rule":
        record = store.get_dataset(payload.get("dataset_id", ""))
        check_columns(record["df"], [payload.get("column")])
        elements, _ = build_set(record["df"], [payload["column"]])
        classes = classes_from_rule(elements, payload.get("rule"), payload.get("param"))
        label = f"Classes by rule: {record['name']}"
    elif mode == "relation":
        classes = classes_from_relation(payload.get("result_id", ""))
        label = f"Classes from relation: {payload.get('result_id', '')}"
    else:
        raise ApiError(f"Unknown equivalence mode: {mode}.")
    total = sum(len(members) for members in classes.values())
    sizes = [{"key": key, "size": len(members)} for key, members in classes.items()]
    stats = {"total_elements": total, "class_count": len(classes), "sizes": sizes, "largest": max([item["size"] for item in sizes], default=0), "smallest": min([item["size"] for item in sizes], default=0)}
    summary = analysis_service.summarize("equivalence", stats)
    rows = [[index, key, member] for index, (key, members) in enumerate(classes.items(), 1) for member in members]
    result_id = store.add_result("equivalence", label, pd.DataFrame(rows, columns=["class_id", "class_key", "member"]), stats, summary)
    output = [{"class_id": index, "key": key, "size": len(members), "members": members[:CLASS_MEMBERS_LIMIT], "members_truncated": len(members) > CLASS_MEMBERS_LIMIT} for index, (key, members) in enumerate(classes.items(), 1)]
    return {"result_id": result_id, "kind": "equivalence", "classes": output, "class_count": len(classes), "stats": stats, "is_partition": is_partition(classes, total), "summary": summary}
