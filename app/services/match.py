from fastapi import HTTPException
from app.repository.match import MatchRepository


class MatchService:
    def __init__(self, db):
        self.repo = MatchRepository(db)

    def get_paginate(self, page: int, size: int):
        return self.repo.paginate(page, size)

    # def get(self, match_id):
    #     match = self.repo.find_by_id(match_id)
    #     if not match:
    #         raise HTTPException(status_code=404, detail="Not found")
    #
    #     return match


    # def delete(self, g_dashboard_cf_id):
    #     g_dashboard_cf = self.repo.find_by_id(g_dashboard_cf_id)
    #     if not g_dashboard_cf:
    #         raise HTTPException(status_code=404, detail=Message.DATA_DOES_NOT_EXISTS)
    #
    #     result = self.repo.delete(g_dashboard_cf)
    #
    #     if result:
    #         return JSONResponse(content={"detail": Message.YOU_HAVE_SUCCESSFULLY_DELETED}, status_code=200)
    #     else:
    #         return JSONResponse(content={"detail": Message.YOU_HAVE_FAIL_DELETED}, status_code=400)
    #
    # def find_record(self, key):
    #     return self.repo.find_like(key)
