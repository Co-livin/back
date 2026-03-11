from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from app.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.crud.user import get_user_by_login
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен недействителен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login_name: str = payload.get("sub")
        if login_name is None:
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истек")
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    user = get_user_by_login(db, login_name=login_name)
    if user is None:
        raise credentials_exception
    return user