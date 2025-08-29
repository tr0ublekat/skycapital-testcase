from pydantic import BaseModel
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
