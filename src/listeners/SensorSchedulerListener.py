import json
import logging

import paho.mqtt.client as mqtt

from src.models.SensorModel import SensorModel, SensorSchema
from src.services.core.config.Config import Config
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

        client = mqtt.Client()
        client.username_pw_set(Config().get_config()["RABBITMQ"]["USER"], Config().get_config()["RABBITMQ"]["PASSWORD"])
        client.connect(Config().get_config()["RABBITMQ"]["HOST"], int(Config().get_config()["RABBITMQ"]["PORT"]), 60)
        client.loop_start()
        client.publish("amq_topic.watering", payload=json.dumps(sensor), qos=0, retain=False)
        client.loop_stop()
