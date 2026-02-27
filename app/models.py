from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    spaces = relationship("SpaceMember", back_populates="user")


class Space(Base):
    __tablename__ = "spaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    invite_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    members = relationship("SpaceMember", back_populates="space", cascade="all, delete")
    tasks = relationship("Task", back_populates="space", cascade="all, delete")
    events = relationship("Event", back_populates="space", cascade="all, delete")


class SpaceMember(Base):
    __tablename__ = "space_members"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), primary_key=True)
    role = Column(String, default="member")  # тут или 'owner', или 'member'
    joined_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="spaces")
    space = relationship("Space", back_populates="members")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"))
    title = Column(String)
    is_recurring = Column(Boolean, default=False)
    frequency_days = Column(Integer, nullable=True)
    next_due_date = Column(DateTime, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="active")
    space = relationship("Space", back_populates="tasks")
    assignee = relationship("User")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String)  # или TASK_COMPLETED, или MEMBER_JOINED
    related_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    space = relationship("Space", back_populates="events")
