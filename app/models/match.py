import uuid
import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.config import settings


class Match(Base):
    __tablename__ = "match"
    __table_args__ = (
        {
            "schema": settings.DATABASE_SCHEMA,
            "comment": "match"
        }
    )

    id = Column(String(64), primary_key=True, default=str(uuid.uuid4()), comment="id")
    match_url = Column(String(500), index=True, nullable=False, comment="match_url")
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment="created_at")

    histories = relationship("History", back_populates="match")
