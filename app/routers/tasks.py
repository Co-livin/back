from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import TaskCreate, TaskResponse
from app.models import User
from app.dependencies import get_current_user
from app.crud import task as crud_task

router = APIRouter()

@router.post("/spaces/{space_id}/tasks", response_model=TaskResponse)
def create_task(
    space_id: int, 
    task: TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not crud_task.check_user_in_space(db, user_id=current_user.id, space_id=space_id):
        raise HTTPException(status_code=403, detail="Доступ запрещен. Вы не состоите в этом пространстве.")
    return crud_task.create_task(db=db, task=task, space_id=space_id)


@router.get("/spaces/{space_id}/tasks", response_model=List[TaskResponse])
def get_tasks(
    space_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not crud_task.check_user_in_space(db, user_id=current_user.id, space_id=space_id):
        raise HTTPException(status_code=403, detail="Доступ запрещен. Вы не состоите в этом пространстве.")
    return crud_task.get_active_tasks(db=db, space_id=space_id)