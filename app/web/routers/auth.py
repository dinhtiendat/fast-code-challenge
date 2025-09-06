from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from app.web import deps
from app.services.user import UserService
from app.const import Constant
from app.utils.templates import templates
from app.core.security import verify_password, get_password_hash, create_access_token
from app.utils.flash import flash


router = APIRouter()

@router.get("/login", response_class=HTMLResponse, name='auth.login')
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "title": "Login"})


@router.post("/login")
def login_action(request: Request, email: str = Form(...), password: str = Form(...), db=Depends(deps.get_db)):
    service = UserService(db)

    user = service.find_by_email(email)

    if not user or not verify_password(password, user.hashed_password):
        return JSONResponse({"status": "error", "message": "Sai email hoặc mật khẩu!"})

    request.session["user_id"] = user.id
    return JSONResponse({"status": "success", "message": "Đăng nhập thành công!"})


@router.get("/me")
async def me(user=Depends(deps.get_current_user)):
    return {"id": user.id, "name": user.email}


@router.get("/logout", response_class=HTMLResponse, name='auth.logout')
async def logout(request: Request):
    request.session.clear()  # xoá toàn bộ session
    flash(request, "Đăng xuất thành công!", "success")
    return RedirectResponse("/auth/login", status_code=302)