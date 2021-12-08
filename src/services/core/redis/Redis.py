from redis import Redis as R
from src.services.core.SingletonMeta import SingletonMeta
from src.services.core.config.Config import Config


class Redis(metaclass=SingletonMeta):
    __redis = None

    def get_redis(self) -> R:
        if isinstance(self.__redis, R):
            return self.__redis

        config = Config().get_config()

        self.__redis = R(host=config['REDIS']['HOST'], port=config['REDIS']['PORT'], db=config['REDIS']['DB'])

        return self.__redis
