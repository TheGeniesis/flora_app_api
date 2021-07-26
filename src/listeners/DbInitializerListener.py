from src.services.core.loader.fixture import load_fixtures
from src.services.core.db.engine import Base
from src.services.core.db.engine import get_engine


class DbInitializerListener:

    def event_list(self):
        return {
            "onKernelStart": {
                "action": self.on_kernel_start,
                "priority": -200
            }
        }

    def on_kernel_start(self):

        import src.models.DeviceModel
        import src.models.MeasurementModel
        Base.metadata.create_all(get_engine(), checkfirst=True)

        load_fixtures()
