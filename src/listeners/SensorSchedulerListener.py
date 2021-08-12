import json

from src.models.SensorModel import SensorModel, SensorSchema
from src.services.core.config.Config import Config
from src.services.core.scheduler.BasicScheduler import BasicScheduler

import pika


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

        if sensor.waterAutoMode:

            scheduler.get_scheduler().add_job(self.water_plant, trigger='interval', seconds=1,
                                              id="water_plant", replace_existing=True,
                                              kwargs={'sensor': sensor})
            pass
        scheduler.get_scheduler().add_job(self.water_plant, 'cron',
                                          hour=sensor.waterTime.hour, minute=sensor.waterTime.minute,
                                          id="water_plant", replace_existing=True,
                                          kwargs={'sensor': sensor})

    def water_plant(self, sensor):
        if sensor.waterAutoMode:
            if sensor.humility > 5:
                pass

        config = Config().get_config()
        credentials = pika.PlainCredentials(config["RABBITMQ"]["USER"], config["RABBITMQ"]["PASSWORD"])

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config["RABBITMQ"]["HOST"], port=config["RABBITMQ"]["PORT"],
                                      credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='watering')
        channel.basic_publish(exchange='',
                              routing_key='watering',
                              body=json.dumps(SensorSchema().dump(sensor)))
        connection.close()
