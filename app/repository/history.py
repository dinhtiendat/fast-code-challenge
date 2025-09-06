from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Params

from app.models.history import History
from app.utils.logs import logger


class HistoryRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_all(self):
        return self.db.query(History).order_by(History.start_time.asc()).all()

    def paginate(self, page: int, size: int):
        return paginate(self.db.query(History)
                        .order_by(History.start_time.asc())
                        .all(), params=Params(page=page, size=size))

    def create(self, data: History):
        try:
            self.db.add(data)
            self.db.commit()
        except Exception as e:
            logger.error("HistoryRepository.create: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def update(self, _id: str, data_update: Dict[str, Any]):
        try:
            self.db.query(History).filter(History.id == _id).update(data_update)
            self.db.commit()
        except Exception as e:
            logger.error("HistoryRepository.update: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def delete(self, data: History):
        try:
            self.db.delete(data)
            self.db.commit()
        except Exception as e:
            logger.error("HistoryRepository.delete: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def find_by_id(self, _id):
        return self.db.query(History).get(_id)

    def count_by_status(self, status):
        return self.db.query(History).filter(History.status == status).count()
