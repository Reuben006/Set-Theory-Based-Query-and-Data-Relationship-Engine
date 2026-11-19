from flask import Blueprint, request

import store
from services import dataset_service
from utils import ok

bp = Blueprint("datasets", __name__)


@bp.route("", methods=["POST"])
def upload_dataset():
    file_storage = request.files.get("file")
    df = dataset_service.read_csv_file(file_storage)
    dataset_id = store.add_dataset(file_storage.filename, df)
    return ok({"dataset_id": dataset_id, "name": file_storage.filename, "rows": len(df), "columns": list(df.columns)})


@bp.route("", methods=["GET"])
def list_datasets():
    records = store.list_datasets()
    return ok({"datasets": [{"dataset_id": item["id"], "name": item["name"], "rows": len(item["df"]), "column_count": len(item["df"].columns)} for item in records]})


@bp.route("/<dataset_id>", methods=["GET"])
def get_dataset(dataset_id):
    record = store.get_dataset(dataset_id)
    data = dataset_service.page_rows(record["df"], request.args.get("page"), request.args.get("page_size"))
    data.update({"dataset_id": dataset_id, "name": record["name"]})
    return ok(data)


@bp.route("/<dataset_id>/columns", methods=["GET"])
def get_columns(dataset_id):
    return ok({"columns": dataset_service.describe_columns(store.get_dataset(dataset_id)["df"])})


@bp.route("/<dataset_id>/quality", methods=["GET"])
def get_quality(dataset_id):
    return ok(dataset_service.quality_report(store.get_dataset(dataset_id)["df"]))


@bp.route("/<dataset_id>", methods=["DELETE"])
def remove_dataset(dataset_id):
    store.delete_dataset(dataset_id)
    return ok({"deleted": dataset_id})
