from src.services.core.SingletonMeta import SingletonMeta
import configparser


class Config(metaclass=SingletonMeta):
    __config = None

    def get_config(self):
        return self.__config

    def init(self, vars):
        if self.__config is None:
            self.__config = vars

            config = configparser.ConfigParser()
            config.read(self.__config["path"] + '/' + '.env.ini')

            self.__config = {**self.__config, **config}
