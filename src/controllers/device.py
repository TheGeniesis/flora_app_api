from flask import request
from connexion import NoContent

from sqlalchemy.orm import sessionmaker

from src.services.core.dispatcher.EventDispatcher import EventDispatcher
from src.services.core.db.engine import get_engine
from src.models.DeviceModel import DeviceModel, DeviceSchema
from src.models.MeasurementModel import MeasurementModel
import datetime


def device_create():

    data = request.get_json()

    device_name = data['name']

    session = sessionmaker(bind=get_engine())()
    device = session.query(DeviceModel).filter(device_name == DeviceModel.name).first()

    if type(device) is DeviceModel:
        return {
            "error": True,
            "message": "Data already exists"
       }, 400

    ins = DeviceModel(name=device_name, createdAt=datetime.date.today())
    session.add(ins)
    session.commit()

    # EventDispatcher().get_dispatcher().raise_event("onHomeViewReload")

    return NoContent, 200


def device_get():

    session = sessionmaker(bind=get_engine())()
    devices = session.query(DeviceModel).all()

    return DeviceSchema(many=True).dump(devices), 200


def measurement_create(device_id):

    data = request.get_json()

    measure_date = data['time']
    temperature = data['temperature']
    humility = data['humility']
    light = data['light']
    water_level = data['water_level']

    session = sessionmaker(bind=get_engine())()

    device = session.query(DeviceModel).filter(int(device_id) == DeviceModel.id).first()

    if type(device) is DeviceModel:
        ins = MeasurementModel(temperature=temperature, light=light, humility=humility, waterLevel=water_level, device=device, measureDate=measure_date, createdAt=datetime.date.today())
        session.add(ins)
        session.commit()

        EventDispatcher().get_dispatcher().raise_event("onHomeViewReload")
        EventDispatcher().get_dispatcher().raise_event("onVideoViewReload")

        return NoContent, 201

    return NoContent, 400


def measurement_get(device_id):
    #
    # data = request.get_json()
    #
    # measure_date = data['time']
    # temperature = data['temperature']
    # humility = data['humility']
    # light = data['light']
    # water_level = data['water_level']
    #
    # base = BaseModel()
    # session = sessionmaker(bind=base.getEngine())()
    #
    # device = session.query(DeviceModel).filter(int(device_id) == DeviceModel.id).first()
    #
    # if type(device) is DeviceModel:
    #     ins = MeasurementModel(temperature=temperature, light=light, humility=humility, waterLevel=water_level, device=device, measureDate=measure_date, createdAt=datetime.date.today())
    #     session.add(ins)
    #     session.commit()
    #
    #     EventDispatcher().get_dispatcher().raise_event("onHomeViewReload")
    #     EventDispatcher().get_dispatcher().raise_event("onVideoViewReload")
    #
    #     return NoContent, 201

    return NoContent, 400

