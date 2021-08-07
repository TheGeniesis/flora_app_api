from datetime import datetime
from http import HTTPStatus

from connexion import NoContent
from flask import request, jsonify
from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel
from src.models.MeasurementModel import MeasurementModel, MeasurementSchema
from src.services.core.db.engine import get_engine
from src.services.core.dispatcher.EventDispatcher import EventDispatcher


def measurement_create(device_id):
    data = request.get_json()

    measure_date = data['date']
    temperature = data['temperature']
    humility = data['humility']
    light = data['light']
    water_level = data['water_level']

    session = sessionmaker(bind=get_engine())()

    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()

    if type(device) is DeviceModel:
        ins = MeasurementModel(temperature=temperature, light=light, humility=humility, waterLevel=water_level,
                               device=device, measureDate=measure_date,
                               createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        session.add(ins)
        session.commit()

        # EventDispatcher().get_dispatcher().raise_event("onVideoViewReload")

        return MeasurementSchema().dump(ins), HTTPStatus.CREATED

    return NoContent, HTTPStatus.NOT_FOUND


def measurement_get(device_id):
    session = sessionmaker(bind=get_engine())()

    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()

    if type(device) is DeviceModel:
        devices = session.query(MeasurementModel).filter(device == MeasurementModel.device)

        return MeasurementSchema(many=True).dump(devices), HTTPStatus.OK

    return jsonify({"message": "Device not found"}), HTTPStatus.NOT_FOUND
