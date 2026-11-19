from flask import Blueprint

from services import equivalence_service
from utils import ok, read_json

bp = Blueprint("equivalence", __name__)


@bp.route("/classes", methods=["POST"])
def classes():
    return ok(equivalence_service.find_classes(read_json(["mode"])))
