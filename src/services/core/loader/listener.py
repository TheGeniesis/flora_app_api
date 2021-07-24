from src.services.core.config.Config import Config
from src.services.core.dispatcher.EventDispatcher import EventDispatcher
from src.services.core.loader.module import load_modules_from_dir
import os
from glob import glob


def load_listeners():
    # get all paths we use join to fix problem with "/" per os
    path = os.path.join(Config().get_config()["path"], "src", "listeners")

    event_list = list()
    for file in glob(os.path.join(path, "*.py")):
        module = load_modules_from_dir(file, "src.listeners")

        listener_event_list = module().event_list()
        for event in listener_event_list.keys():
            event_list.append(event)

    event_dispatcher = EventDispatcher()
    event_dispatcher.init(list(set(event_list)))
    notifier = event_dispatcher.get_dispatcher()

    index = 0
    priority_list = {}
    for file in glob(os.path.join(path, "*.py")):
        module = load_modules_from_dir(file, "src.listeners")

        listener_event_list = module().event_list()
        for event in listener_event_list.keys():
            if listener_event_list[event]["priority"] not in priority_list:
                priority_list[listener_event_list[event]["priority"]] = {}

            listener_event_list[event]["event"] = event
            priority_list[listener_event_list[event]["priority"]][index] = listener_event_list[event]
            index += 1

    for priority in sorted(priority_list.keys()):
        for elem in priority_list[priority]:
            notifier.subscribe(priority_list[priority][elem]["event"], priority_list[priority][elem]["action"])
