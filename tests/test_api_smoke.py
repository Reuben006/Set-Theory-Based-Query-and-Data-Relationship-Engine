import store
import pandas as pd
from app import create_app
from services import dataset_service


def client():
    store.clear_all()
    return create_app().test_client()


def test_unknown_route_is_json_404():
    response = client().get("/api/nothing")
    assert response.status_code == 404
    assert response.get_json()["ok"] is False


def test_wrong_method_is_json_405():
    response = client().delete("/api/results")
    assert response.status_code == 405
    assert response.get_json()["ok"] is False


def test_unknown_dataset_message():
    response = client().get("/api/datasets/d99")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Dataset d99 not found."


def test_unexpected_error_is_json_500(monkeypatch):
    store.add_dataset("data.csv", pd.DataFrame({"value": [1]}))
    monkeypatch.setattr(dataset_service, "describe_columns", lambda df: (_ for _ in ()).throw(Exception()))
    response = create_app().test_client().get("/api/datasets/d1/columns")
    assert response.status_code == 500
    assert response.get_json()["error"] == "Something went wrong on the server."
