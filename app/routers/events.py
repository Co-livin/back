from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas import EventResponse
from app.models import User
from app.dependencies import get_current_user

from app.crud import event as crud_event
from app.crud import task as crud_task

router = APIRouter()


@router.get("/spaces/{space_id}/events", response_model=List[EventResponse])
def get_events(
    space_id: int, 
    limit: Optional[int] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not crud_task.check_user_in_space(db, user_id=current_user.id, space_id=space_id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return crud_event.get_space_events(db=db, space_id=space_id, limit=limit)
