import logging
import os

from flask_cors import CORS

from src.services.core.App import App
from src.services.core.config.Config import Config
from src.services.core.dispatcher.EventDispatcher import EventDispatcher
from src.services.core.loader.consumer import load_consumers
from src.services.core.loader.listener import load_listeners


if __name__ == "__main__":
    app = App().get_app().app
    CORS(app)

    config = Config()
    config.init({
        "path": os.getcwd()
    })

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger('Setup')
    logger.info('main path loaded: %s', os.getcwd())

    load_listeners()

    EventDispatcher().get_dispatcher().raise_event("onKernelStart")

    load_consumers()

    app.run(host='0.0.0.0', port=8001)
