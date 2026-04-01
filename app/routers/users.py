from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserResponse
from app.dependencies import get_current_user
from app.crud import user as crud_user

router = APIRouter()


@router.get("/by-login/{login}", response_model=UserResponse)
def get_user_by_login(
    login: str, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    db_user = crud_user.get_user_by_login(db, login=login)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user


@router.get("/by-id/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user
