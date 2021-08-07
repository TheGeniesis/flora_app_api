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

    def reschedule_job(self, time: str, job_id: str, callback):
        scheduler = self.get_scheduler()
        job = scheduler.get_job(job_id)
        if job:
            job.remove()

        result = time.split(":")
        scheduler.add_job(callback, 'cron', hour=result[0], minutes=result[1], id=job_id)
