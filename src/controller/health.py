from flask import jsonify


def index():
    resp = jsonify(success=True)

    return resp
