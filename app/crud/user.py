from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.core.security import get_password_hash

def get_user_by_login(db: Session, login_name: str):
    return db.query(User).filter(User.login_name == login_name).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        login_name=user.login_name, 
        username=user.username, 
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user
