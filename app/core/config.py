import pathlib

from pydantic_settings import BaseSettings

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str = 'GuPR4nWYk4QIyCj89VkOLyRC5haRT3zp'
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: str = '5432'
    DATABASE_USERNAME: str = 'postgres'
    DATABASE_PASSWORD: str = 'iO0lNV+XIm++g/Keyf7BnA=='
    DATABASE_NAME: str = 'postgres'
    DATABASE_SCHEMA: str = 'sejourney_analytics'
    KAFKA_BOOTSTRAP_SERVERS: list = '["","",""]'
    KAFKA_TOPIC_LOG: str = 'TOPIC_LOG'
    KAFKA_SECURITY_PROTOCOL: str = 'PLAINTEXT'
    KAFKA_SSL_CAFILE: str = ''
    KAFKA_ARGS_API_VERSION_AUTO_TIMEOUT_MS: int = 1000000
    KAFKA_ARGS_REQUEST_TIMEOUT_MS: int = 1000000
    LOG_TYPE: str = 'stream'
    LOG_LEVEL: str = 'INFO'
    LOG_DIR: str = 'logs'
    APP_LOG_NAME: str = 'app_log.txt'
    WWW_LOG_NAME: str = 'access_log.txt'
    DISABLE_OPENAPI: str = 1
    ALLOW_HOSTS: list = ["*"]

    class Config:
        case_sentitive = True
        env_file = "config.env"


settings = Settings()
