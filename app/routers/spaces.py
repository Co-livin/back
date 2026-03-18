from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.schemas import SpaceCreate, SpaceResponse, RoleUpdate
from app.models import User, SpaceMember
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


@router.get("/{space_id}/members")
def get_members(
    space_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_member = (
        db.query(SpaceMember)
        .filter_by(user_id=current_user.id, space_id=space_id)
        .first()
    )
    if not is_member:
        raise HTTPException(
            status_code=403, detail="Вы не состоите в этом пространстве"
        )
    members = crud_space.get_space_members(db, space_id)
    return [
        {"user_id": m.user_id, "role": m.role, "joined_at": m.joined_at}
        for m in members
    ]


@router.delete("/{space_id}/members/{target_user_id}")
def kick_member(
    space_id: int,
    target_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    crud_space.remove_member(db, space_id, target_user_id, current_user.id)
    return {"detail": "Участник успешно удален"}


@router.patch("/{space_id}/members/{target_user_id}/role")
def update_role(
    space_id: int,
    target_user_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    crud_space.change_member_role(
        db, space_id, target_user_id, current_user.id, payload.role
    )
    return {"detail": f"Роль успешно изменена на {payload.role}"}
