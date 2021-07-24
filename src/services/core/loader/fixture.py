from sqlalchemy.orm import sessionmaker

from src.services.core.db.engine import get_engine
from src.models.DeviceModel import DeviceModel
from src.services.core.config.Config import Config
from src.services.core.loader.module import load_modules_from_dir
import os
from glob import glob


def load_fixtures():
    Session = sessionmaker(bind=get_engine())
    session = Session()

    device = session.query(DeviceModel).first()
    # if device is None:
    #
    #     # get all paths we use join to fix problem with "/" per os
    #     path = os.path.join(Config().get_config()["path"], "src", "fixtures")
    #
    #     for file in glob(os.path.join(path, "*.py")):
    #         module = load_modules_from_dir(file, "src.fixtures")
    #
    #         module().generate()
