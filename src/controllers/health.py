from http import HTTPStatus

from flask import jsonify


def index():
    return jsonify(success=True), HTTPStatus.OK
