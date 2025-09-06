from app.repository.history import HistoryRepository
from app.repository.ah_data import AHDataRepository
from app.repository.ou_data import OUDataRepository


class HistoryService:
    def __init__(self, db):
        self.repo = HistoryRepository(db)
        self.repo_ah = AHDataRepository(db)
        self.repo_ou = OUDataRepository(db)

    def get_paginate(self, page: int, size: int):
        return self.repo.paginate(page, size)

    def get(self, history_id):
        return self.repo.find_by_id(history_id)

    def get_ah_data(self, history_id):
        ah_data = self.repo_ah.get_all(history_id)
        return ah_data

    def get_ou_data(self, history_id):
        ou_data = self.repo_ou.get_all(history_id)
        return ou_data

    def count_success(self):
        return self.repo.count_by_status(True)
