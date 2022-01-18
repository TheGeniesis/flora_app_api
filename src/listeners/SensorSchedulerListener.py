import json
import logging

from src.models.SensorModel import SensorModel, SensorSchema
from src.services.core.rabbit.BasicBroker import BasicBroker
from src.services.core.scheduler.BasicScheduler import BasicScheduler


class SensorSchedulerListener:

    def event_list(self):
        return {
            "onSensorUpdate": {
                "action": self.update,
                "priority": 0
            }
        }

    def update(self, sensor: SensorModel):
        scheduler = BasicScheduler()
        logger = logging.getLogger('scheduler')

        logger.info("Scheduler: Data to send %s", SensorSchema().dump(sensor))
        if sensor.waterAutoMode:
            logger.info('Scheduler: Changing scheduler type to: interval')

            scheduler.get_scheduler().add_job(self.water_plant, trigger='interval', seconds=1,
                                              id="water_plant", replace_existing=True,
                                              kwargs={'sensor': SensorSchema().dump(sensor)})
            return

        logger.info('Scheduler: Changing scheduler type to: cron')
        scheduler.get_scheduler().add_job(self.water_plant, 'cron',
                                          hour=sensor.waterTime.hour, minute=sensor.waterTime.minute,
                                          id="water_plant", replace_existing=True,
                                          kwargs={'sensor': SensorSchema().dump(sensor)})

    def water_plant(self, sensor):
        logger = logging.getLogger('scheduler')
        logger.info("Scheduler: Data received %s", SensorSchema().dump(sensor))

        if sensor['waterAutoMode']:
            logger.info('Scheduler: Auto plan mode')
            if sensor['humility'] < sensor['measuredHumility']:
                logger.info('Scheduler: Humility higher than sensor, skipping...')
                return
        else:
            logger.info('Scheduler: Manual plant mode')

        logger.info('Scheduler: Adding message to the queue')

        broker = (BasicBroker()).get_broker()

        broker.send(json.dumps(sensor), routing_key='amq_topic.watering', exchange_name='flask_rabmq')

