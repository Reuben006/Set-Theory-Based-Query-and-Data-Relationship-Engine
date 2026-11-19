from flask import Blueprint

import store
from services import analysis_service
from utils import ok

bp = Blueprint("results", __name__)


@bp.route("", methods=["GET"])
def list_results():
    records = store.list_results()
    return ok({"results": [{"result_id": item["id"], "kind": item["kind"], "label": item["label"], "summary": item["summary"], "created_at": item["created_at"]} for item in records]})


@bp.route("/overview", methods=["GET"])
def get_overview():
    return ok(analysis_service.overview())


@bp.route("/<result_id>", methods=["GET"])
def get_result(result_id):
    item = store.get_result(result_id)
    return ok({"result_id": item["id"], "kind": item["kind"], "label": item["label"], "summary": item["summary"], "stats": item["stats"], "created_at": item["created_at"]})
