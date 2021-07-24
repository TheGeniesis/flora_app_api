from apscheduler.schedulers.qt import QtScheduler
from src.services.core.SingletonMeta import SingletonMeta


class BasicScheduler(metaclass=SingletonMeta):
    __scheduler = None

    def get_scheduler(self) -> QtScheduler:
        if isinstance(self.__scheduler, QtScheduler):
            return self.__scheduler

        self.__scheduler = QtScheduler({
            'apscheduler.jobstores.default': {
                'type': 'sqlalchemy',
                'url': 'sqlite:///jobs.sqlite'
            },
            'apscheduler.executors.default': {
                'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                'max_workers': '20'
            },
            'apscheduler.executors.processpool': {
                'type': 'processpool',
                'max_workers': '5'
            },
            'apscheduler.job_defaults.coalesce': 'false',
            'apscheduler.job_defaults.max_instances': '3',
            'apscheduler.timezone': 'UTC',
        })

        self.__scheduler.start()

        return self.__scheduler

    def reschedule_job(self, time: float, id: str, callback):
        scheduler = self.get_scheduler()
        job = scheduler.get_job(id)
        if job:
            job.remove()

        scheduler.add_job(callback, 'interval', minutes=time, id=id)
