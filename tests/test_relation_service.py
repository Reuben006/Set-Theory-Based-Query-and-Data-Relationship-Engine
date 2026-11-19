import pandas as pd

import store
from services import relation_service


def test_property_witnesses_follow_input_order():
    pairs = [("1", "2"), ("2", "3")]
    pair_set = set(pairs)
    assert relation_service.is_reflexive(["1", "2", "3"], pair_set)[1] == [["1", "1"], ["2", "2"], ["3", "3"]]
    assert relation_service.is_symmetric(pair_set, pairs)[1] == [["1", "2"], ["2", "3"]]
    assert relation_service.is_transitive(pair_set, pairs)[1] == [["1", "2", "3"]]


def test_properties_are_repeatable():
    store.clear_all()
    result_id = store.add_result("relation", "R", pd.DataFrame([["1", "2"], ["2", "3"]], columns=["a", "b"]), {}, "", {"pairs": [["1", "2"], ["2", "3"]], "base_set": ["1", "2", "3"]})
    assert relation_service.check_properties(result_id) == relation_service.check_properties(result_id)


def test_less_or_equal_has_first_symmetric_witness():
    store.clear_all()
    store.add_dataset("numbers.csv", pd.DataFrame({"id": range(1, 7)}))
    result = relation_service.build({"mode": "rule", "set_a": {"dataset_id": "d1", "columns": ["id"]}, "set_b": {"dataset_id": "d1", "columns": ["id"]}, "rule": "less_or_equal"})
    assert relation_service.check_properties(result["result_id"])["symmetric"]["witnesses"][0] == ["1", "2"]
