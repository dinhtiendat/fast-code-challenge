from fastapi import APIRouter
from app.web.routers import match, history, auth, file


web_router = APIRouter()

web_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# web_router.include_router(match.router, prefix="/matches", tags=["matches"])
# web_router.include_router(history.router, prefix="/histories", tags=["histories"])
web_router.include_router(file.router, prefix="/files", tags=["files"])
