from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.web import deps
from app.services.match import MatchService
from app.const import Constant


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, name='match.index')
async def index(request: Request, page: int = 1, db=Depends(deps.get_db)):
    service = MatchService(db)
    matches = service.get_paginate(page, size=Constant.PAGINATION_PAGE_SIZE)

    n_pages = int(matches.total / Constant.PAGINATION_PAGE_SIZE) if matches.total % Constant.PAGINATION_PAGE_SIZE == 0 else int(matches.total / Constant.PAGINATION_PAGE_SIZE) + 1
    if page > 1:
        prev_num = page - 1
    else:
        prev_num = 1

    if page < n_pages:
        next_num = page + 1
    else:
        next_num = n_pages

    return templates.TemplateResponse(name="match/index.html", context={
        'request': request,
        'matches': matches,
        'n_pages': n_pages,
        'prev_num': prev_num,
        'next_num': next_num
    })


@router.get("/{id}", response_class=HTMLResponse)
async def get(request: Request, id: str, db=Depends(deps.get_db)):
    service = MatchService(db)
    match = service.get(id)
    return templates.TemplateResponse(name="match/index.html", context={'request': request, "id": match.id})
