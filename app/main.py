import time
from pathlib import Path
from fastapi import FastAPI, APIRouter, Request, Depends
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


from app.core.config import settings
from app.web.router import web_router
from app.utils.logs import logger
from app.web.deps import get_current_user
from app.utils.templates import templates
from app.utils.flash import get_flashed_messages
from app.db.session import SessionLocal
from app.services.user import UserService
from starlette.middleware.base import BaseHTTPMiddleware

BASE_PATH = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_PATH / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

root_router = APIRouter()






if settings.DISABLE_OPENAPI == 1:
    app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1, "docExpansion": "none"},
                  openapi_url=None, docs_url=None, redoc_url=None, dependencies=[Depends(get_current_user)])
else:
    app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1, "docExpansion": "none"},
                  openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc", dependencies=[Depends(get_current_user)])


# Bật session (lưu trong cookie, dùng secret_key)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOW_HOSTS
)


app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
# mount static để truy cập file upload
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.middleware("http")
async def log(req: Request, call_next):
    if "clientMessageId" in req.headers:
        client_message_id = req.headers["clientMessageId"]
    else:
        client_message_id = ""
    start_time = time.time()
    response = await call_next(req)

    # # Lưu flash messages vào request.state để template dùng
    # req.state.flash_messages = req.session.pop("flash", []) if "flash" in req.session else []
    # print(req.state.flash_messages)

    process_time = time.time() - start_time
    if not (str(req.url.path) in ["/actuator/health", "/actuator/info", "/actuator/prometheus", "/probe"]):
        message = '"{} {}" {}'.format(req.method, str(req.url.path), response.status_code)
        logger.info(message, extra={"clientMessageId": client_message_id, "status_code": response.status_code,
                                    "duration": str(round(process_time, 1))})
    return response


# @app.middleware("http")
# async def add_flash_messages(request: Request, call_next):
#     # Lấy flash từ session
#     request.state.flash_messages = get_flashed_messages(request, with_categories=True)
#     print(request.state.flash_messages)
#     response = await call_next(request)
#     return response


# @app.middleware("http")
# async def add_current_user(request: Request, call_next):
#     user = None
#     try:
#         user_id = request.session.get("user_id")  # Lấy từ session
#         if user_id:
#             db = SessionLocal()
#             service = UserService(db)
#             user = service.find(user_id)
#             db.close()
#     except Exception as e:
#         logger.error(f"add_current_user error: {e}")
#     request.state.current_user = user
#     response = await call_next(request)
#     return response

@app.exception_handler(HTTPException)
def custom_http_exception(request: Request, ext: HTTPException):
    if ext.status_code == 400:
        return templates.TemplateResponse(name="errors/400.html", context={'request': request})
    elif ext.status_code == 401:
        return templates.TemplateResponse(name="errors/401.html", context={'request': request})
    elif ext.status_code == 403:
        return templates.TemplateResponse(name="errors/403.html", context={'request': request})
    elif ext.status_code == 404:
        return templates.TemplateResponse(name="errors/404.html", context={'request': request})
    else:
        return templates.TemplateResponse(name="errors/500.html", context={'request': request})


@app.get("/", response_class=HTMLResponse, name="homepage")
async def index(request: Request):
    return templates.TemplateResponse(name="homepage.html", context={"request": request})


app.include_router(root_router)
app.include_router(web_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
