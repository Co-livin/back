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
    current_user: User = Depends(get_current_user),
):
    if not crud_task.check_user_in_space(
        db, user_id=current_user.id, space_id=space_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Доступ запрещен. Вы не состоите в этом пространстве.",
        )
    return crud_task.create_task(db=db, task=task, space_id=space_id)


@router.get("/spaces/{space_id}/tasks", response_model=List[TaskResponse])
def get_tasks(
    space_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not crud_task.check_user_in_space(
        db, user_id=current_user.id, space_id=space_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Доступ запрещен. Вы не состоите в этом пространстве.",
        )
    return crud_task.get_active_tasks(db=db, space_id=space_id)


@router.post("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = crud_task.get_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if not crud_task.check_user_in_space(
        db, user_id=current_user.id, space_id=task.space_id
    ):
        raise HTTPException(status_code=403, detail="Доступ запрещен, это чужая задача")

    if task.status == "done":
        raise HTTPException(status_code=400, detail="Задача уже выполнена")

    updated_task = crud_task.complete_task(
        db=db, task=task, user_id=current_user.id, username=current_user.name
    )

    return updated_task
