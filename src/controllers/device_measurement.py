import datetime
from http import HTTPStatus

from connexion import NoContent
from flask import request
from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel
from src.models.MeasurementModel import MeasurementModel
from src.services.core.db.engine import get_engine
from src.services.core.dispatcher.EventDispatcher import EventDispatcher


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
        ins = MeasurementModel(temperature=temperature, light=light, humility=humility, waterLevel=water_level,
                               device=device, measureDate=measure_date, createdAt=datetime.date.today())
        session.add(ins)
        session.commit()

        EventDispatcher().get_dispatcher().raise_event("onHomeViewReload")
        EventDispatcher().get_dispatcher().raise_event("onVideoViewReload")

        return NoContent, HTTPStatus.NO_CONTENT

    return NoContent, HTTPStatus.BAD_REQUEST


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

    return NoContent, HTTPStatus.BAD_REQUEST
