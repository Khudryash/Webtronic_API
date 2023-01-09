from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..core.models.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from ..core.schemas.schemas import User
from ..core.models import models
from ..core.models.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", summary="Get list of users")
def get_users(limit: int, offset: int, db: Session = Depends(get_db)):
    users = db.query(models.Users).offset(offset=offset).limit(limit=limit).all()
    return users


@router.delete("/{id}", summary="delete user by id")
def del_user(key: int, db: Session = Depends(get_db)):
    inst = db.get(models.Users, key)
    db.delete(inst)
    db.commit()
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@router.post("/", summary="Create new user")
def create_user(data: User, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter_by(email=data.email).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    user_model = models.Users()
    user_model.username = data.username
    user_model.email = data.email
    user_model.password = get_hashed_password(data.password)

    db.add(user_model)
    db.commit()

    return JSONResponse(
        content={},
        headers={"Location": "/users/"+str(user_model.id)},
        status_code=status.HTTP_201_CREATED
    )
