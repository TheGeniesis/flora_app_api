from flask_rabmq import RabbitMQ

from src.services.core.App import App
from src.services.core.SingletonMeta import SingletonMeta
from src.services.core.config.Config import Config


class BasicBroker(metaclass=SingletonMeta):
    __broker = None

    def get_broker(self) -> RabbitMQ:
        if isinstance(self.__broker, RabbitMQ):
            return self.__broker

        ramq = RabbitMQ()

        app = App().get_app()
        app.config = (Config()).get_config()["RABBITMQ"]

        ramq.init_app(app=app)

        self.__broker = ramq

        return self.__broker