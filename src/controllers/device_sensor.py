from datetime import datetime
from http import HTTPStatus

from flask import request, jsonify
from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel
from src.models.SensorModel import SensorModel, SensorSchema
from src.services.core.db.engine import get_engine
from src.services.core.dispatcher.EventDispatcher import EventDispatcher


def sensor_update(device_id: str, sensor_id: str):
    data = request.get_json()

    session = sessionmaker(bind=get_engine())()

    sensor = session.query(SensorModel).filter(device_id == DeviceModel.id, sensor_id == SensorModel.id).first()

    if type(sensor) is SensorModel:
        sensor.waterAmount = data['water_amount']
        sensor.waterTime = data['water_time']
        sensor.waterAutoMode = bool(data['water_auto_mode'])
        sensor.humility = data['humility']
        sensor.updatedAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        session.add(sensor)
        session.commit()

        EventDispatcher().get_dispatcher().raise_event("onSensorUpdate", sensor=sensor)

        return SensorSchema().dump(sensor), HTTPStatus.OK

    return {"message": "Can't find sensor for device"}, HTTPStatus.NOT_FOUND


def sensor_get_all(device_id: str):
    session = sessionmaker(bind=get_engine())()

    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()

    if type(device) is DeviceModel:
        sensors = session.query(SensorModel).filter(device_id == DeviceModel.id)
        return SensorSchema(many=True).dump(sensors), HTTPStatus.OK

    return jsonify({"message": "Device not found"}), HTTPStatus.NOT_FOUND


def sensor_get(device_id: str, sensor_id: str):
    session = sessionmaker(bind=get_engine())()

    sensor = session.query(SensorModel).filter(device_id == DeviceModel.id, sensor_id == SensorModel.id).first()

    if type(sensor) is SensorModel:
        return SensorSchema().dump(sensor), HTTPStatus.OK

    return jsonify({"message": "Can't find sensor for device"}), HTTPStatus.NOT_FOUND
