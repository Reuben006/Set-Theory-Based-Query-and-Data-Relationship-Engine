from flask import Flask, send_from_directory
from werkzeug.exceptions import HTTPException

from config import MAX_UPLOAD_MB
from routes import cartesian, datasets, equivalence, export, joins, relations, results, sets
from utils import ApiError, fail


def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="")
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
    app.register_blueprint(datasets.bp, url_prefix="/api/datasets")
    app.register_blueprint(results.bp, url_prefix="/api/results")
    app.register_blueprint(export.bp, url_prefix="/api/export")
    app.register_blueprint(sets.bp, url_prefix="/api/sets")
    app.register_blueprint(cartesian.bp, url_prefix="/api/cartesian")
    app.register_blueprint(relations.bp, url_prefix="/api/relations")
    app.register_blueprint(equivalence.bp, url_prefix="/api/equivalence")
    app.register_blueprint(joins.bp, url_prefix="/api/joins")

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return fail(error.message, error.status)

    @app.errorhandler(413)
    def handle_large_file(error):
        return fail("File too large. Max 10 MB.", 413)

    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return fail(error.description, error.code)
        return fail("Something went wrong on the server.", 500)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
