import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Time, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from src.services.core.db.engine import Base, ma


class SensorModel(Base):
    __tablename__ = "sensor"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4
    )

    waterAmount = Column(
        Float(),
        nullable=False
    )

    waterTime = Column(
        Time(),
        nullable=False
    )

    waterAutoMode = Column(
        Boolean(),
        nullable=False
    )

    humility = Column(
        Float(),
        nullable=False
    )

    deviceId = Column(UUID(as_uuid=True), ForeignKey('device.id'))
    device = relationship("DeviceModel", back_populates="sensors")

    createdAt = Column(
        DateTime(),
        nullable=False
    )

    updatedAt = Column(
        DateTime(),
        nullable=True
    )


class SensorSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "waterAmount", "waterTime", "humility", "waterAutoMode", "updatedAt")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("sensor", values=dict(id="<id>")),
            "collection": ma.URLFor("sensors"),
        }
    )
