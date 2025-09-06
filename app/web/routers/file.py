import os
import shutil
from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from app.web import deps
from app.services.user import UserService
from app.const import Constant
from app.utils.templates import templates
from app.core.security import verify_password, get_password_hash, create_access_token
from app.utils.flash import flash

BASE_PATH = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_PATH / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
# Cho phép các đuôi file
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}

# Giới hạn dung lượng file (bytes) → 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024

router = APIRouter()


# Trang upload
@router.get("/upload", name='file.upload')
def upload_form(request: Request):
    return templates.TemplateResponse("file/upload.html", {"request": request})

# Xử lý upload
@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return JSONResponse({"status": "error", "message": "Chỉ cho phép file .pdf, .docx, .doc"})

    # Kiểm tra dung lượng file
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        return JSONResponse({"status": "error", "message": "Dung lượng file vượt quá giới hạn 5 MB"})

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return JSONResponse({"status": "success", "message": "Upload file thành công!"})

# Danh sách file
@router.get("/list", name='file.list')
def list_files(request: Request):
    files = os.listdir(UPLOAD_DIR)
    return templates.TemplateResponse("file/index.html", {"request": request, "files": files})