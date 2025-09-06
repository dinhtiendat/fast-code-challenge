from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

from .config import settings

# Bcrypt để hash mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    subject: thường là user.id dạng string
    """
    if expires_delta is None:
        expires_delta = settings.access_token_expiry_delta()

    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """
    Trả về payload sau khi verify token.
    Gọi trong deps.py -> get_current_user.
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload