from datetime import datetime

from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel
from src.models.MeasurementModel import MeasurementModel, MeasurementSchema
from src.services.core.db.engine import get_engine
from src.services.core.dispatcher.EventDispatcher import EventDispatcher
import logging

def create(data):
    measure_date = data['date']
    temperature = data['temperature']
    humility = data['humility']
    light = data['light']
    water_level = data['water_level']
    device_id = data['device_id']

    session = sessionmaker(bind=get_engine(), expire_on_commit=False)()

    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()

    if type(device) is DeviceModel:
        ins = MeasurementModel(temperature=temperature, light=light, humility=humility, waterLevel=water_level,
                               device=device, measureDate=measure_date,
                               createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        session.add(ins)
        session.commit()
        logger = logging.getLogger('measurement')
        logger.info('Measurement created for object: %s', device_id, extra=MeasurementSchema().dump(ins))

        # EventDispatcher().get_dispatcher().raise_event("onVideoViewReload")

        return ins
