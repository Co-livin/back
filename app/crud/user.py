from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.core.security import get_password_hash


def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        login=user.login,
        name=user.name,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
