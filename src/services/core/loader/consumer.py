import os
from glob import glob

from src.services.core.config.Config import Config
from src.services.core.loader.module import load_modules_from_dir


def load_consumers():
    path = os.path.join(Config().get_config()["path"], "src", "queue", "consumer")

    for file in glob(os.path.join(path, "*.py")):
        function = load_modules_from_dir(file, "src.queue.consumer")
        function()
