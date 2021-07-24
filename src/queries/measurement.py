from sqlalchemy import func
from datetime import date
import datetime
from src.models.MeasurementModel import MeasurementModel
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
#from src.services.core.db.engine import BaseModel

def find_by_id(self):
    return self.findTrainingQuantityForDay(date.today())


#
# def findTrainingQuantityForDay(self, start: datetime):
#     base = BaseModel()
#     Session = sessionmaker(bind=base.getEngine())
#     session = Session()
#
#     start_day = start.strftime("%Y-%m-%d 00:00:00")
#     end = start + datetime.timedelta(days=1)
#     end_day = end.strftime("%Y-%m-%d 00:00:00")
#     query = session.query("app.src.models.MeasurementModel")
#     query = query.filter(
#         and_(
#             TrainingModel.grade != None,
#             TrainingModel.createdAt >= start_day,
#             TrainingModel.createdAt < end_day,
#         )
#     )
#     return query.with_entities(func.count()).scalar()
#
# def findWeekTrainingQuantity(self):
#     base = BaseModel()
#
#     Session = sessionmaker(bind=base.getEngine())
#     session = Session()
#
#     start_date = date.today() - datetime.timedelta(days=date.today().isoweekday() % 7)
#     start_day = start_date.strftime("%Y-%m-%d 00:00:00")
#
#     tomorrow = date.today() + datetime.timedelta(days=1)
#     end_day = tomorrow.strftime("%Y-%m-%d 00:00:00")
#     query = session.query("app.src.models.TrainingModel")
#     query = query.filter(
#         and_(
#             TrainingModel.grade != None,
#             TrainingModel.createdAt >= start_day,
#             TrainingModel.createdAt < end_day,
#         )
#     )
#     return query.with_entities(func.count()).scalar()
#
# def findMonthTrainingQuantity(self):
#     base = BaseModel()
#
#     Session = sessionmaker(bind=base.getEngine())
#     session = Session()
#
#     start_date = date.today().replace(day=1)
#     start_day = start_date.strftime("%Y-%m-%d 00:00:00")
#
#     tomorrow = date.today() + datetime.timedelta(days=1)
#     end_day = tomorrow.strftime("%Y-%m-%d 00:00:00")
#     query = session.query("app.src.models.TrainingModel")
#     query = query.filter(
#         and_(
#             TrainingModel.grade != None,
#             TrainingModel.createdAt >= start_day,
#             TrainingModel.createdAt < end_day,
#         )
#     )
#     return query.with_entities(func.count()).scalar()