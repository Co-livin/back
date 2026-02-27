from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class UserBase(BaseModel):
    login_name: str
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    is_recurring: bool = False
    frequency_days: Optional[int] = None
    assignee_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    space_id: int
    status: str
    next_due_date: Optional[datetime]

    class Config:
        from_attributes = True


class SpaceCreate(BaseModel):
    name: str


class SpaceResponse(BaseModel):
    id: int
    name: str
    invite_code: str
    created_at: datetime

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    id: int
    event_type: str
    user_id: Optional[int]
    payload: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
