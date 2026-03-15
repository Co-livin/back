from sqlalchemy.orm import Session
from app.models import Event


def get_space_events(db: Session, space_id: int, limit: int = 50):
    return (
        db.query(Event)
        .filter(Event.space_id == space_id)
        .order_by(Event.created_at.desc())
        .limit(limit)
        .all()
    )
