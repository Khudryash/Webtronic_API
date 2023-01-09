from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from authlib.jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))
JWT_REFRESH_SECRET_KEY = str(os.getenv('JWT_REFRESH_SECRET_KEY'))

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    print(password_context.hash(password))
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta += datetime.utcnow()
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode({"alg": ALGORITHM}, to_encode, JWT_SECRET_KEY)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta += datetime.utcnow()
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode({"alg": ALGORITHM}, to_encode, JWT_REFRESH_SECRET_KEY)
    return encoded_jwt
