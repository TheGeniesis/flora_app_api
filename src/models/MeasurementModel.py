import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.services.core.db.engine import Base


class MeasurementModel(Base):
    __tablename__ = "measurement"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4
    )

    temperature = Column(
        Float(),
        nullable=True
    )

    light = Column(
        Float(),
        nullable=True
    )

    humility = Column(
        Float(),
        nullable=True
    )

    waterLevel = Column(
        Float(),
        nullable=True
    )

    deviceId = Column(Integer(), ForeignKey('device.id'))
    device = relationship("DeviceModel", back_populates="measurements")

    measureDate = Column(
        DateTime(),
        nullable=False
    )

    createdAt = Column(
        DateTime(),
        nullable=False
    )
