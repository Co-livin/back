from sqlalchemy.orm import Session
from app.models import Task, SpaceMember
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