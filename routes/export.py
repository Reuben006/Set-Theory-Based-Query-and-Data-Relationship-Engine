from flask import Blueprint, Response

import store

bp = Blueprint("export", __name__)


@bp.route("/<result_id>", methods=["GET"])
def export_result(result_id):
    record = store.get_result(result_id)
    content = record["export_df"].to_csv(index=False)
    return Response("\ufeff" + content, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={record['kind']}_{result_id}.csv"})
