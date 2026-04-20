from sqlalchemy.orm import Session
from app.models import Event
from typing import Optional


def get_space_events(db: Session, space_id: int, limit: Optional[int] = None):
    return (
        db.query(Event)
        .filter(Event.space_id == space_id)
        .order_by(Event.created_at.desc())
        .limit(limit)
        .all()
    )
