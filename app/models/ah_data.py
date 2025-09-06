import uuid
import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.config import settings


class AHData(Base):
    __tablename__ = "ah_data"
    __table_args__ = (
        {
            "schema": settings.DATABASE_SCHEMA,
            "comment": "ah_data"
        }
    )

    id = Column(String(64), primary_key=True, default=str(uuid.uuid4()), comment="id")
    history_id = Column(String(64), ForeignKey(settings.DATABASE_SCHEMA + '.history.id'), index=True, nullable=False, comment="history_id")
    order = Column(Integer, nullable=False, comment="order")
    ah_value = Column(String(100), nullable=False, comment="ah_value")
    odds1 = Column(String(50), nullable=False, comment="odds1")
    odds2 = Column(String(50), nullable=False, comment="odds2")
    payout = Column(String(50), nullable=False, comment="payout")
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment="created_at")

    history = relationship("History", back_populates="ah_data")
