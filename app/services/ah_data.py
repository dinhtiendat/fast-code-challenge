from app.repository.ah_data import AHDataRepository


class AHDataService:
    def __init__(self, db):
        self.repo = AHDataRepository(db)

    def get_paginate(self, history_id: str, page: int, size: int):
        return self.repo.paginate(history_id, page, size)

