from typing import Generator
from fastapi import Request, status, Depends
from starlette.exceptions import HTTPException

from app.db.session import SessionLocal
from app.services.user import UserService


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request):
    if hasattr(request.state, "current_user"):
        return request.state.current_user

    user_id = request.session.get("user_id")
    if not user_id:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        return None

    db = SessionLocal()
    service = UserService(db)
    user = service.get(user_id)
    db.close()

    if not user:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return None

    request.state.current_user = user
    return user


def require_admin(current_user=Depends(get_current_user)):
    if getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return current_user