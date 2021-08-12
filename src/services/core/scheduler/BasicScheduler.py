from apscheduler.schedulers.background import BackgroundScheduler
from src.services.core.SingletonMeta import SingletonMeta

class BasicScheduler(metaclass=SingletonMeta):
    __scheduler = None

    def get_scheduler(self) -> BackgroundScheduler:
        if isinstance(self.__scheduler, BackgroundScheduler):
            return self.__scheduler

        self.__scheduler = BackgroundScheduler({
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
