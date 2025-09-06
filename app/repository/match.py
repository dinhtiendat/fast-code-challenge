from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Params

from app.models.match import Match
from app.utils.logs import logger


class MatchRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_all(self):
        return self.db.query(Match).order_by(Match.created_at.desc()).all()

    def paginate(self, page: int, size: int):
        return paginate(self.db.query(Match).order_by(Match.created_at.desc()).all(), params=Params(page=page, size=size))

    def create(self, data: Match):
        try:
            self.db.add(data)
            self.db.commit()
        except Exception as e:
            logger.error("MatchRepository.create: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def update(self, _id: str, data_update: Dict[str, Any]):
        try:
            self.db.query(Match).filter(Match.id == _id).update(data_update)
            self.db.commit()
        except Exception as e:
            logger.error("MatchRepository.update: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def delete(self, data: Match):
        try:
            self.db.delete(data)
            self.db.commit()
        except Exception as e:
            logger.error("MatchRepository.delete: " + str(e), extra={"status_code": 500})
            self.db.rollback()
            return False
        return True

    def find_by_id(self, _id):
        return self.db.query(Match).get(_id)
