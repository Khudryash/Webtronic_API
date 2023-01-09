from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..core.models.utils import verify_password, create_access_token, create_refresh_token
from ..core.models import models
from ..core.models.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users/login",
    tags=["login"]
    # dependencies=[Depends(get_current_user)]
)


@router.post(
    '/',
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_201_CREATED
)
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.Users).filter_by(email=form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }
