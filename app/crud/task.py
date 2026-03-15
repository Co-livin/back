from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.models import Task, SpaceMember, Event  
from app.schemas import TaskCreate

def check_user_in_space(db: Session, user_id: int, space_id: int) -> bool:
    member = db.query(SpaceMember).filter_by(user_id=user_id, space_id=space_id).first()
    return member is not None

def create_task(db: Session, task: TaskCreate, space_id: int):
    db_task = Task(
        space_id=space_id,
        title=task.title,
        is_recurring=task.is_recurring,
        frequency_days=task.frequency_days,
        assignee_id=task.assignee_id,
        status="active"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_active_tasks(db: Session, space_id: int):
    return db.query(Task).filter(Task.space_id == space_id, Task.status == "active").all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def complete_task(db: Session, task: Task, user_id: int, username: str):
    event_payload = {
        "task_title": task.title,
        "user_name": username,
        "action": "completed"
    }
    if task.is_recurring and task.frequency_days:
        task.next_due_date = datetime.now(timezone.utc) + timedelta(days=task.frequency_days)
    else:
        task.status = "done"

    new_event = Event(
        space_id=task.space_id,
        user_id=user_id,
        event_type="TASK_COMPLETED",
        related_task_id=task.id,
        payload=event_payload
    )

    db.add(new_event)
    db.commit()
    db.refresh(task)
    return task
