import math

from flask import jsonify, request


class ApiError(Exception):
    def __init__(self, message, status=400):
        self.message = message
        self.status = status


def ok(data):
    return jsonify({"ok": True, "data": data})


def fail(message, status=400):
    return jsonify({"ok": False, "error": message}), status


def read_json(required=[]):
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        raise ApiError("Request body must be JSON.")
    for field in required:
        if field not in body:
            raise ApiError(f"Missing field: {field}.")
    return body


def df_to_rows(df):
    rows = df.astype(object).where(df.notna(), None).values.tolist()
    return [[plain_value(value) for value in row] for row in rows]


def plain_value(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return value.item() if hasattr(value, "item") else value
