from EventNotifier import Notifier

from src.services.core.SingletonMeta import SingletonMeta


class EventDispatcher(metaclass=SingletonMeta):
    __notifier = None

    def get_dispatcher(self):
        if self.__notifier is None:
            self.init([])

        return self.__notifier

    def init(self, event_list: list):
        self.__notifier = Notifier(event_list)
