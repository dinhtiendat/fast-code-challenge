from app.repository.ou_data import OUDataRepository


class OUDataService:
    def __init__(self, db):
        self.repo = OUDataRepository(db)

    def get_paginate(self, history_id: str, page: int, size: int):
        return self.repo.paginate(history_id, page, size)

