import string
import random
from sqlalchemy.orm import Session
from app.models import Space, SpaceMember
from app.schemas import SpaceCreate


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
