from flask import Blueprint

from services import relation_service
from utils import ok, read_json

bp = Blueprint("relations", __name__)


@bp.route("/build", methods=["POST"])
def build():
    return ok(relation_service.build(read_json(["mode"])))


@bp.route("/<result_id>/properties", methods=["POST"])
def properties(result_id):
    return ok(relation_service.check_properties(result_id))
