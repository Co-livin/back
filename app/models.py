from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    spaces: Mapped[List["SpaceMember"]] = relationship(
        "SpaceMember", back_populates="user"
    )


class Space(Base):
    __tablename__ = "spaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    invite_code: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    members: Mapped[List["SpaceMember"]] = relationship(
        "SpaceMember", back_populates="space", cascade="all, delete"
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task", back_populates="space", cascade="all, delete"
    )
    events: Mapped[List["Event"]] = relationship(
        "Event", back_populates="space", cascade="all, delete"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    space_id: Mapped[int] = mapped_column(Integer, ForeignKey("spaces.id"), index=True)
    title: Mapped[str] = mapped_column(String)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    frequency_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    next_due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    assignee_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(String, default="active")

    space: Mapped["Space"] = relationship("Space", back_populates="tasks")


class SpaceMember(Base):
    __tablename__ = "space_members"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    space_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("spaces.id"), primary_key=True
    )
    role: Mapped[str] = mapped_column(String, default="member")
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="spaces")
    space: Mapped["Space"] = relationship("Space", back_populates="members")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    space_id: Mapped[int] = mapped_column(Integer, ForeignKey("spaces.id"), index=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    event_type: Mapped[str] = mapped_column(String)
    related_task_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    space: Mapped["Space"] = relationship("Space", back_populates="events")
