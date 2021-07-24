import connexion
from src.services.core.config.Config import Config
from src.services.core.dispatcher.EventDispatcher import EventDispatcher
from src.services.core.loader.listener import load_listeners
import os


if __name__ == "__main__":
    config = Config()
    config.init({
        "path": os.getcwd()
    })

    load_listeners()

    EventDispatcher().get_dispatcher().raise_event("onKernelStart")


# Create the application instance
app = connexion.FlaskApp(__name__, specification_dir="src/swagger/")


# Read the swagger.yml file to configure the endpoints
app.add_api("swagger.yaml")

app.run(port=8002)


# from flask import Flask, redirect, url_for
# from flask_dance.contrib.authentiq import make_authentiq_blueprint
