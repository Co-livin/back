from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.schemas import SpaceCreate, SpaceResponse
from app.models import User
from app.dependencies import get_current_user
from app.crud import space as crud_space

router = APIRouter()


class SpaceJoin(BaseModel):
    invite_code: str


@router.post("/", response_model=SpaceResponse)
def create_space(
    space: SpaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_space.create_space(db=db, space=space, user_id=current_user.id)


@router.get("/my", response_model=List[SpaceResponse])
def get_my_spaces(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return crud_space.get_user_spaces(db=db, user_id=current_user.id)


@router.post("/join", response_model=SpaceResponse)
def join_space(
    payload: SpaceJoin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_space = crud_space.get_space_by_invite_code(db, invite_code=payload.invite_code)
    if not db_space:
        raise HTTPException(
            status_code=404, detail="Пространство с таким кодом не найдено"
        )

    joined = crud_space.join_space(db=db, space_id=db_space.id, user_id=current_user.id)
    if not joined:
        raise HTTPException(
            status_code=400, detail="Вы уже состоите в этом пространстве"
        )

    return db_space
