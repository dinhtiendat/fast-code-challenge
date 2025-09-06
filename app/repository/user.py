from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Params

from app.models.user import User
from app.utils.logs import logger


class UserRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_all(self):
        return self.db.query(User).order_by(User.start_time.asc()).all()

    def paginate(self, page: int, size: int):
        return paginate(self.db.query(User)
                        .order_by(User.start_time.asc())
                        .all(), params=Params(page=page, size=size))

    def create(self, data: User):
        try:
            self.db.add(data)
            self.db.commit()
        except Exception as e:
            logger.error("UserRepository.create: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def update(self, _id: str, data_update: Dict[str, Any]):
        try:
            self.db.query(User).filter(User.id == _id).update(data_update)
            self.db.commit()
        except Exception as e:
            logger.error("UserRepository.update: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def delete(self, data: User):
        try:
            self.db.delete(data)
            self.db.commit()
        except Exception as e:
            logger.error("UserRepository.delete: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def find_by_id(self, _id):
        return self.db.query(User).get(_id)

    def find_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

    def count_by_status(self, status):
        return self.db.query(User).filter(User.status == status).count()
