from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Params

from app.models.ah_data import AHData
from app.utils.logs import logger


class AHDataRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_all(self, history_id: str):
        return self.db.query(AHData).filter(AHData.history_id == history_id).order_by(AHData.order.asc()).all()

    def paginate(self, history_id: str, page: int, size: int):
        return paginate(self.db.query(AHData)
                        .filter(AHData.history_id == history_id)
                        .order_by(AHData.order.asc())
                        .all(), params=Params(page=page, size=size))

    def create(self, data: AHData):
        try:
            self.db.add(data)
            self.db.commit()
        except Exception as e:
            logger.error("AHDataRepository.create: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def create_many(self, data_list):
        try:
            self.db.add_all(data_list)
            self.db.commit()
        except Exception as e:
            logger.error("AHDataRepository.create_many: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def update(self, _id: str, data_update: Dict[str, Any]):
        try:
            self.db.query(AHData).filter(AHData.id == _id).update(data_update)
            self.db.commit()
        except Exception as e:
            logger.error("AHDataRepository.update: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def delete(self, data: AHData):
        try:
            self.db.delete(data)
            self.db.commit()
        except Exception as e:
            logger.error("AHDataRepository.delete: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def find_by_id(self, _id):
        return self.db.query(AHData).get(_id)
