import time
from pathlib import Path
from fastapi import FastAPI, APIRouter, Request
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from apscheduler.triggers.cron import CronTrigger


from app.core.config import settings
from app.web.router import web_router
from app.utils.logs import logger
from app.utils.scheduler import scrape
from app.utils.templates import templates
from app.utils.background_scheduler import bg_scheduler


BASE_PATH = Path(__file__).resolve().parent

root_router = APIRouter()

if settings.DISABLE_OPENAPI == 1:
    app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1, "docExpansion": "none"},
                  openapi_url=None, docs_url=None, redoc_url=None)
else:
    app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1, "docExpansion": "none"},
                  openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")

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


# @app.on_event('startup')
# def start_scheduler():
#     bg_scheduler.add_job(scrape, CronTrigger.from_crontab('*/10 * * * *'))
#     bg_scheduler.start()
#
#
# @app.on_event('shutdown')
# def shutdown_scheduler():
#     bg_scheduler.remove_all_jobs()


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


@app.middleware("http")
async def log(req: Request, call_next):
    if "clientMessageId" in req.headers:
        client_message_id = req.headers["clientMessageId"]
    else:
        client_message_id = ""
    start_time = time.time()
    response = await call_next(req)
    process_time = time.time() - start_time
    if not (str(req.url.path) in ["/actuator/health", "/actuator/info", "/actuator/prometheus", "/probe"]):
        message = '"{} {}" {}'.format(req.method, str(req.url.path), response.status_code)
        logger.info(message, extra={"clientMessageId": client_message_id, "status_code": response.status_code,
                                    "duration": str(round(process_time, 1))})
    return response


@app.get("/", response_class=HTMLResponse, name="homepage")
async def index(request: Request):
    return templates.TemplateResponse(name="homepage.html", context={"request": request})


app.include_router(root_router)
app.include_router(web_router)


if __name__ == "main":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
