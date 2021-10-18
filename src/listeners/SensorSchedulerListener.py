import json

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

        if sensor.waterAutoMode:
            scheduler.get_scheduler().add_job(self.water_plant, trigger='interval', seconds=1,
                                              id="water_plant", replace_existing=True,
                                              kwargs={'sensor': SensorSchema().dump(sensor)})
            pass
        scheduler.get_scheduler().add_job(self.water_plant, 'cron',
                                          hour=sensor.waterTime.hour, minute=sensor.waterTime.minute,
                                          id="water_plant", replace_existing=True,
                                          kwargs={'sensor': SensorSchema().dump(sensor)})

    def water_plant(self, sensor):
        if sensor.waterAutoMode:
            if sensor.humility > 5:
                pass
        broker = (BasicBroker()).get_broker()

        broker.send(json.dumps(sensor), routing_key='flask_rabmq.watering', exchange_name='flask_rabmq')

