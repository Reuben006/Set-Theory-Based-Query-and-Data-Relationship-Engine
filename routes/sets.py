from flask import Blueprint

from services import set_service
from utils import ok, read_json

bp = Blueprint("sets", __name__)


@bp.route("/preview", methods=["POST"])
def preview_set():
    return ok(set_service.preview_set(read_json(["dataset_id", "columns"])))


@bp.route("/operate", methods=["POST"])
def operate():
    return ok(set_service.operate(read_json(["operation", "set_a", "set_b"])))
