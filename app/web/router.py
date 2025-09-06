from fastapi import APIRouter
from app.web.routers import match, history


web_router = APIRouter()


web_router.include_router(match.router, prefix="/matches", tags=["matches"])
web_router.include_router(history.router, prefix="/histories", tags=["histories"])
