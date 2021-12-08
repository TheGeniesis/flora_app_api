import json
import logging

from sqlalchemy.orm import sessionmaker

from src.models.DeviceModel import DeviceModel
from src.services.core.db.engine import get_engine
from src.services.core.redis.Redis import Redis


def create(data):
    device_id = data['device_id']

    session = sessionmaker(bind=get_engine(), expire_on_commit=False)()

    device = session.query(DeviceModel).filter(device_id == DeviceModel.id).first()


    if type(device) is DeviceModel:
        redis = Redis().get_redis()

        data['device_name'] = device.name
        save_in_redis('temperature', 'Measured temperature', data, redis)
        save_in_redis('humility', 'Measured temperature', data, redis)
        save_in_redis('light', 'Measured temperature', data, redis)
        save_in_redis('water_level', 'Measured temperature', data, redis)

        logger = logging.getLogger('measurement')
        logger.info('Measurement created for object: %s', device_id)

        return True
        # EventDispatcher().get_dispatcher().raise_event("onVideoViewReload")


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
