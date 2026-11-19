import store


def summarize(kind, stats):
    if kind == "set_operation":
        return f"{stats['operation']} of A ({stats['size_a']} elements) and B ({stats['size_b']} elements) gives {stats['total_after']} elements. {stats['common_count']} elements are common to both."
    if kind == "cartesian":
        return f"A has {stats['size_a']} elements and B has {stats['size_b']} elements, so A x B has {stats['pair_count']} ordered pairs."
    if kind == "relation":
        return f"Relation has {stats['pair_count']} ordered pairs between A ({stats['size_a']} elements) and B ({stats['size_b']} elements)."
    if kind == "equivalence":
        return f"{stats['total_elements']} elements are split into {stats['class_count']} equivalence classes. The largest class has {stats['largest']} members."
    return f"{stats['how'].title()} join gives {stats['result_rows']} rows. {stats['matched_keys']} keys match in both datasets."


def overview():
    kinds = ["set_operation", "cartesian", "relation", "equivalence", "join"]
    records = store.list_results()
    return {"datasets": len(store.list_datasets()), "results": len(records), "by_kind": {kind: sum(record["kind"] == kind for record in records) for kind in kinds}}
