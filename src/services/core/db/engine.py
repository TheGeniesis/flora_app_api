from __future__ import annotations

from sqlalchemy import create_engine

from src.services.core.config.Config import Config
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow


Base = declarative_base()
ma = Marshmallow()


def get_engine():
    config = Config()
    config = config.get_config()

    return create_engine(config["DATABASE"]["PATH"], echo=True)
