import datetime
from http import HTTPStatus

from flask import request
from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel, DeviceSchema
from src.services.core.db.engine import get_engine


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

    ins = DeviceModel(name=device_name, createdAt=datetime.date.today())
    session.add(ins)
    session.commit()

    # EventDispatcher().get_dispatcher().raise_event("onHomeViewReload")

    return DeviceSchema().dump(ins), HTTPStatus.CREATED


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
