import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating init data")
    try:
        init()
        logger.info("Init data created")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
