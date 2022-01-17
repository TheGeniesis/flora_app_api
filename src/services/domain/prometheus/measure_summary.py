import json
import logging
from prometheus_client import Summary

from src.services.core.redis.Redis import Redis
from prometheus_client import CollectorRegistry, generate_latest


def set_measure_summary():
    graphs = {}

    redis = Redis().get_redis()
    labels = ['device_id', 'device_name', 'env', 'app', 'date']
    cr = CollectorRegistry()

    for key in redis.scan_iter('prometheus_summar*'):
        data = json.loads(redis.get(key))
        if not graphs.get(data['name']):
            graphs[data['name']] = Summary(data['name'], data['description'], labels, registry=cr)

        graphs.get(data['name']).labels(data['labels']['device_id'], data['labels']['device_name'],
                                        data['labels']['env'], data['labels']['app_name'],
                                        data['labels']['date']).observe(data['value'])

        logger = logging.getLogger('measurement')
        logger.info('Cleaning measurement from redis: %s', key)
        redis.delete(key)

    return graphs
