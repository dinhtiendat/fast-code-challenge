import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.config import settings


class History(Base):
    __tablename__ = "history"
    __table_args__ = (
        {
            "schema": settings.DATABASE_SCHEMA,
            "comment": "history"
        }
    )

    id = Column(String(64), primary_key=True, default=str(uuid.uuid4()), comment="id")
    match_id = Column(String(64), ForeignKey(settings.DATABASE_SCHEMA + '.match.id'), index=True, nullable=False, comment="match_id")
    start_time = Column(DateTime, nullable=False, comment="start_time")
    end_time = Column(DateTime, nullable=False, comment="end_time")
    duration = Column(Float, nullable=False, comment="duration")
    status = Column(Boolean, nullable=False, comment="status")
    error_cookies = Column(Text, nullable=False, comment="error_cookies")
    error_decimal_odds = Column(Text, nullable=False, comment="error_decimal_odds")
    error_ah = Column(Text, nullable=False, comment="error_ah")
    error_ou = Column(Text, nullable=False, comment="error_ou")
    source_page_cookies = Column(Text, nullable=False, comment="source_page_cookies")
    source_page_decimal_odds = Column(Text, nullable=False, comment="source_page_decimal_odds")
    source_page_ah = Column(Text, nullable=False, comment="source_page_ah")
    source_page_ou = Column(Text, nullable=False, comment="source_page_ou")
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment="created_at")

    match = relationship("Match", back_populates="histories")
    ah_data = relationship("AHData", back_populates="history")
    ou_data = relationship("OUData", back_populates="history")
