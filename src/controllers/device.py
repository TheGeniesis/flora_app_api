from datetime import datetime

from http import HTTPStatus

from flask import request
from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel, DeviceSchema
from src.models.SensorModel import SensorModel
from src.services.core.db.engine import get_engine
from src.services.core.dispatcher.EventDispatcher import EventDispatcher


def device_create():
    data = request.get_json()

    device_name = data['name']

    session = sessionmaker(bind=get_engine())()
    device = session.query(DeviceModel).filter(device_name == DeviceModel.name).first()

    if type(device) is DeviceModel:
        return {
                   "error": True,
                   "message": "Data already exists"
               }, HTTPStatus.BAD_REQUEST

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device = DeviceModel(name=device_name, createdAt=now)
    session.add(device)
    sensor = SensorModel(device=device, createdAt=now, humility=5, waterAmount=50,
                         waterTime=datetime.now().replace(hour=7, minute=00), waterAutoMode=True, updatedAt=now)
    session.add(sensor)

    session.commit()

    EventDispatcher().get_dispatcher().raise_event("onSensorUpdate", sensor=sensor)

    return DeviceSchema().dump(device), HTTPStatus.CREATED


def device_update(device_id):
    data = request.get_json()

    device_name = data['name']

    session = sessionmaker(bind=get_engine())()
    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()

    if type(device) is not DeviceModel:
        return {
                   "error": True,
                   "message": "Data doesn't exists"
               }, HTTPStatus.NOT_FOUND

    device.name = device_name
    session.add(device)
    session.commit()

    return DeviceSchema().dump(device), HTTPStatus.OK


def device_delete(device_id):
    session = sessionmaker(bind=get_engine())()
    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()

    if type(device) is not DeviceModel:
        return {
                   "error": True,
                   "message": "Data doesn't exists"
               }, HTTPStatus.NOT_FOUND

    session.delete(device)
    session.commit()

    return {}, HTTPStatus.NO_CONTENT


def device_get():
    session = sessionmaker(bind=get_engine())()
    devices = session.query(DeviceModel).all()

    return DeviceSchema(many=True).dump(devices), HTTPStatus.OK
