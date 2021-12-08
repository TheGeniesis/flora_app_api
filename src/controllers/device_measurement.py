from datetime import datetime
from http import HTTPStatus

from connexion import NoContent
from flask import request

from src.services.domain.measurement import create


def measurement_create(device_id):
    data = request.get_json()
    data['device_id'] = device_id

    result = create(data)

    if result:
        return {}, HTTPStatus.CREATED

    return NoContent, HTTPStatus.NOT_FOUND

