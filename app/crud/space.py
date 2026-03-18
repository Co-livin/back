import string
import random
from sqlalchemy.orm import Session
from app.models import Space, SpaceMember
from app.schemas import SpaceCreate
from fastapi import HTTPException, status


def generate_invite_code(length=6):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


def create_space(db: Session, space: SpaceCreate, user_id: int):
    invite_code = generate_invite_code()
    while db.query(Space).filter(Space.invite_code == invite_code).first():
        invite_code = generate_invite_code()
    db_space = Space(name=space.name, invite_code=invite_code)
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    db_member = SpaceMember(user_id=user_id, space_id=db_space.id, role="owner")
    db.add(db_member)
    db.commit()
    return db_space


def get_space_by_invite_code(db: Session, invite_code: str):
    return db.query(Space).filter(Space.invite_code == invite_code).first()


def join_space(db: Session, space_id: int, user_id: int):
    existing_member = (
        db.query(SpaceMember).filter_by(user_id=user_id, space_id=space_id).first()
    )
    if not existing_member:
        db_member = SpaceMember(user_id=user_id, space_id=space_id, role="member")
        db.add(db_member)
        db.commit()
        return True
    return False


def get_user_spaces(db: Session, user_id: int):
    return (
        db.query(Space).join(SpaceMember).filter(SpaceMember.user_id == user_id).all()
    )


def get_space_members(db: Session, space_id: int):
    return db.query(SpaceMember).filter(SpaceMember.space_id == space_id).all()


def remove_member(
    db: Session, space_id: int, target_user_id: int, current_user_id: int
):
    actor = (
        db.query(SpaceMember)
        .filter_by(user_id=current_user_id, space_id=space_id)
        .first()
    )
    target = (
        db.query(SpaceMember)
        .filter_by(user_id=target_user_id, space_id=space_id)
        .first()
    )

    if not actor or not target:
        raise HTTPException(
            status_code=404, detail="Пользователь не найден в этом пространстве"
        )

    if actor.role == "member":
        raise HTTPException(
            status_code=403, detail="У вас нет прав для удаления участников"
        )

    if target.role == "owner":
        raise HTTPException(status_code=403, detail="Невозможно удалить владельца")

    if actor.role == "admin" and target.role == "admin":
        raise HTTPException(
            status_code=403, detail="Админ не может удалить другого админа"
        )

    if actor.user_id == target.user_id:
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")

    db.delete(target)
    db.commit()
    return True


def change_member_role(
    db: Session, space_id: int, target_user_id: int, current_user_id: int, new_role: str
):
    actor = (
        db.query(SpaceMember)
        .filter_by(user_id=current_user_id, space_id=space_id)
        .first()
    )
    target = (
        db.query(SpaceMember)
        .filter_by(user_id=target_user_id, space_id=space_id)
        .first()
    )

    if not actor or not target:
        raise HTTPException(
            status_code=404, detail="Пользователь не найден в этом пространстве"
        )

    if new_role not in ["admin", "member"]:
        raise HTTPException(status_code=400, detail="Только 'admin' или 'member'")

    if actor.role == "member":
        raise HTTPException(status_code=403, detail="У вас нет прав изменять роли")

    if target.role == "owner":
        raise HTTPException(status_code=403, detail="Насяльника поменять нельзя ежжи")

    if actor.role == "admin" and target.role == "admin":
        raise HTTPException(
            status_code=403, detail="Админ не может менять роль другого админа"
        )

    target.role = new_role
    db.commit()
    db.refresh(target)
    return target
