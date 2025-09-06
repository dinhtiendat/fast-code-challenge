from app.repository.user import UserRepository


class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    def get_paginate(self, page: int, size: int):
        return self.repo.paginate(page, size)

    def get(self, id):
        return self.repo.find_by_id(id)

    def find_by_email(self, email):
        return self.repo.find_by_email(email)