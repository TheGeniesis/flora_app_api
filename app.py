from src.services.core.App import App
from src.services.core.config.Config import Config
from src.services.core.dispatcher.EventDispatcher import EventDispatcher
from src.services.core.loader.consumer import load_consumers
from src.services.core.loader.listener import load_listeners

import os

if __name__ == "__main__":
    config = Config()
    config.init({
        "path": os.getcwd()
    })

    load_listeners()

    EventDispatcher().get_dispatcher().raise_event("onKernelStart")

    load_consumers()

app = App().get_app()
app.run(port=8004)

# from flask import Flask, redirect, url_for
# from flask_dance.contrib.authentiq import make_authentiq_blueprint
