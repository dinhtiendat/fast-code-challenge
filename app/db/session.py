from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

from app.core.config import settings
from app.utils.aes import aes_decode

SQLALCHEMY_DATABASE_URI = ('postgresql://{username}:%s@{host}:{port}/{database}'.format(
    username=settings.DATABASE_USERNAME,
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    database=settings.DATABASE_NAME)) % quote(aes_decode(settings.DATABASE_PASSWORD))

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_size=20,
    max_overflow=100
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
