import connexion
from connexion import FlaskApp

from src.services.core.SingletonMeta import SingletonMeta


class App(metaclass=SingletonMeta):
    __app = None

    def get_app(self) -> FlaskApp:
        if isinstance(self.__app, FlaskApp):
            return self.__app

        self.__app = connexion.FlaskApp(__name__, specification_dir="../../swagger/")

        # Read the swagger.yml file to configure the endpoints
        self.__app.add_api("swagger.yaml")

        return self.__app
