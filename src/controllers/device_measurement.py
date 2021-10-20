from datetime import datetime
from http import HTTPStatus

from connexion import NoContent
from flask import request, jsonify
from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel
from src.models.MeasurementModel import MeasurementModel, MeasurementSchema
from src.services.core.db.engine import get_engine
from src.services.domain.measurement import create


def measurement_create(device_id):
    data = request.get_json()
    data['device_id'] = device_id

    result = create(data)

    if result:
        return MeasurementSchema().dump(result), HTTPStatus.CREATED

    return NoContent, HTTPStatus.NOT_FOUND


def measurement_get(device_id):
    session = sessionmaker(bind=get_engine())()

    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()

    if type(device) is DeviceModel:
        devices = session.query(MeasurementModel).filter(device == MeasurementModel.device)

        return MeasurementSchema(many=True).dump(devices), HTTPStatus.OK

    return jsonify({"message": "Device not found"}), HTTPStatus.NOT_FOUND
