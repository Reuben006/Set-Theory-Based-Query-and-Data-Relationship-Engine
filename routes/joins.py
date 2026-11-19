from flask import Blueprint

from services import join_service
from utils import ok, read_json

bp = Blueprint("joins", __name__)


@bp.route("", methods=["POST"])
def join():
    return ok(join_service.join(read_json(["left", "right", "how"])))
