from src.models.SensorModel import SensorModel
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
            scheduler.get_scheduler().add_job(self.water_plant, 'interval', minutes=0,
                                              hours=1, id="water_plant", replace_existing=True,
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

        # connect with external device
        # send request to do action
        pass
        # send request