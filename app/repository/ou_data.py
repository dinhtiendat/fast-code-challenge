from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Params

from app.models.ou_data import OUData
from app.utils.logs import logger


class OUDataRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_all(self, history_id: str):
        return self.db.query(OUData).filter(OUData.history_id == history_id).order_by(OUData.order.asc()).all()

    def paginate(self, history_id: str, page: int, size: int):
        return paginate(self.db.query(OUData)
                        .filter(OUData.history_id == history_id)
                        .order_by(OUData.order.asc())
                        .all(), params=Params(page=page, size=size))

    def create(self, data: OUData):
        try:
            self.db.add(data)
            self.db.commit()
        except Exception as e:
            logger.error("OUDataRepository.create: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def create_many(self, data_list):
        try:
            self.db.add_all(data_list)
            self.db.commit()
        except Exception as e:
            logger.error("OUDataRepository.create_many: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def update(self, _id: str, data_update: Dict[str, Any]):
        try:
            self.db.query(OUData).filter(OUData.id == _id).update(data_update)
            self.db.commit()
        except Exception as e:
            logger.error("OUDataRepository.update: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def delete(self, data: OUData):
        try:
            self.db.delete(data)
            self.db.commit()
        except Exception as e:
            logger.error("OUDataRepository.delete: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def find_by_id(self, _id):
        return self.db.query(OUData).get(_id)
