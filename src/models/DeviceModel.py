from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.services.core.db.engine import Base, ma

import uuid


class DeviceModel(Base):
    __tablename__ = "device"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4
    )

    name = Column(
        String(),
        nullable=True
    )

    measurements = relationship("MeasurementModel", back_populates="device")

    createdAt = Column(
        DateTime(),
        nullable=False
    )


class DeviceSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("device", values=dict(id="<id>")),
            "collection": ma.URLFor("devices"),
        }
    )
