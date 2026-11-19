from flask import Blueprint

from services import cartesian_service
from utils import ok, read_json

bp = Blueprint("cartesian", __name__)


@bp.route("/generate", methods=["POST"])
def generate():
    return ok(cartesian_service.generate(read_json(["set_a", "set_b", "confirm"])))
