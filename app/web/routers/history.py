from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.web import deps
from app.services.history import HistoryService
from app.const import Constant
from app.utils.templates import templates


router = APIRouter()


@router.get("/", response_class=HTMLResponse, name='history.index')
async def index(request: Request, page: int = 1, db=Depends(deps.get_db)):
    service = HistoryService(db)
    histories = service.get_paginate(page, size=Constant.PAGINATION_PAGE_SIZE)
    n_success = service.count_success()

    n_pages = int(histories.total / Constant.PAGINATION_PAGE_SIZE) if histories.total % Constant.PAGINATION_PAGE_SIZE == 0 else int(histories.total / Constant.PAGINATION_PAGE_SIZE) + 1
    if page > 1:
        prev_num = page - 1
    else:
        prev_num = 1

    if page < n_pages:
        next_num = page + 1
    else:
        next_num = n_pages

    return templates.TemplateResponse(name="history/index.html", context={
        'request': request,
        'histories': histories,
        'n_success': n_success,
        'n_pages': n_pages,
        'prev_num': prev_num,
        'next_num': next_num
    })


@router.get("/{history_id}", response_class=HTMLResponse, name='history.detail')
async def detail(request: Request, history_id: str, db=Depends(deps.get_db)):
    service = HistoryService(db)
    history = service.get(history_id)
    ah_data = service.get_ah_data(history_id)
    ou_data = service.get_ou_data(history_id)
    return templates.TemplateResponse(name="history/detail.html", context={'request': request, "history": history, "ah_data": ah_data, "ou_data": ou_data})
