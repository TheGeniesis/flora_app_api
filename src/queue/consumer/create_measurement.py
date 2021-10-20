import json
import logging

from src.services.core.rabbit.BasicBroker import BasicBroker
from src.services.domain.measurement import create


def create_measurement():
    ramq = (BasicBroker()).get_broker()

    @ramq.queue(exchange_name='flask_rabmq', routing_key='flask_rabmq.measurement')
    def consume(body):
        logger = logging.getLogger('queue')
        logger.warning('Consuming message: %s', 'create_measurement')

        result = create(json.loads(body))

        if result:
            return True

        return False

    ramq.run_consumer()
