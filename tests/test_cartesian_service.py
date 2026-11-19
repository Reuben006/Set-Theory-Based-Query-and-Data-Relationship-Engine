import pandas as pd

import store
from services import cartesian_service


def add_sample_datasets():
    store.add_dataset("students.csv", pd.read_csv("sample_data/students.csv"))
    store.add_dataset("clubs.csv", pd.read_csv("sample_data/clubs.csv"))


def test_generate_without_confirm_returns_pairs():
    store.clear_all()
    add_sample_datasets()
    result = cartesian_service.generate({"set_a": {"dataset_id": "d1", "columns": ["dept"]}, "set_b": {"dataset_id": "d2", "columns": ["club"]}})
    assert result["count"] == 9
    assert result["warning"] is False


def test_large_product_without_confirm_returns_warning():
    store.clear_all()
    store.add_dataset("a.csv", pd.DataFrame({"value": range(101)}))
    store.add_dataset("b.csv", pd.DataFrame({"value": range(101)}))
    result = cartesian_service.generate({"set_a": {"dataset_id": "d1", "columns": ["value"]}, "set_b": {"dataset_id": "d2", "columns": ["value"]}})
    assert result["warning"] is True
    assert store.list_results() == []


def test_large_product_with_confirm_returns_pairs():
    store.clear_all()
    store.add_dataset("a.csv", pd.DataFrame({"value": range(101)}))
    store.add_dataset("b.csv", pd.DataFrame({"value": range(101)}))
    result = cartesian_service.generate({"set_a": {"dataset_id": "d1", "columns": ["value"]}, "set_b": {"dataset_id": "d2", "columns": ["value"]}, "confirm": True})
    assert result["count"] == 10201
