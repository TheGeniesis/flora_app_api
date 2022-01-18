from datetime import datetime

import json
import logging

from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel
from src.models.SensorModel import SensorModel
from src.services.core.db.engine import get_engine
from src.services.core.redis.Redis import Redis


def create(data):
    device_id = data['device_id']

    session = sessionmaker(bind=get_engine(), expire_on_commit=False)()

    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()

    if (not isinstance(data['light'], float) and not isinstance(data['light'], int)) or data['light'] <= 0:
        data['light'] = 0
    if (not isinstance(data['humility'], float) and not isinstance(data['humility'], int)) or data['humility'] <= 0:
        data['humility'] = 0
    if (not isinstance(data['water_level'], float) and not isinstance(data['water_level'], int)) or data['water_level'] <= 0:
        data['water_level'] = 0
    if (not isinstance(data['temperature'], float) and not isinstance(data['temperature'], int)) or data['temperature'] <= 0:
        data['temperature'] = 0

    if type(device) is DeviceModel:
        redis = Redis().get_redis()

        data['device_name'] = device.name
        save_in_redis('temperature', 'Measured temperature', data, redis)
        save_in_redis('humility', 'Measured temperature', data, redis)
        save_in_redis('light', 'Measured temperature', data, redis)
        save_in_redis('water_level', 'Measured temperature', data, redis)

        logger = logging.getLogger('measurement')
        logger.info('Measurement created for object: %s', device_id)

        save_water_amount(device_id, data['humility'])

        return True

def save_in_redis(name: str, description: str, data: dict, redis):
    prom_data = prepare_data(name, description, data[name], data)
    index_name = 'prometheus_summary_%s_%s' % (prom_data['name'], prom_data['trace_id'])
    redis.set(index_name, json.dumps(prom_data))


def prepare_data(name: str, description: str, value: int, data: dict) -> dict:
    return {
        'name': name,
        'description': description,
        'value': value,
        'trace_id': data['message_id'],
        'labels': {
            'device_id': data['device_id'],
            'device_name': data['device_name'],
            'env': 'dev',
            'app_name': 'flora',
            'date': data['date']
        }
    }

def save_water_amount(device_id: str, humility: float):
    session = sessionmaker(bind=get_engine())()

    sensor = session.query(SensorModel).filter(device_id == DeviceModel.id).first()

    if type(sensor) is SensorModel:
        sensor.measuredHumility = humility
        sensor.updatedAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        session.add(sensor)
        session.commit()
