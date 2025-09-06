import uuid
import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.config import settings


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        {
            "schema": settings.DATABASE_SCHEMA,
            "comment": "user"
        }
    )

    id = Column(String(64), primary_key=True, default=str(uuid.uuid4()), comment="id")
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100),  index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
