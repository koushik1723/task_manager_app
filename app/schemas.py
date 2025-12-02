from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .models import RoleEnum, TaskStatusEnum

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    owner_id: int
    status: Optional[TaskStatusEnum] = TaskStatusEnum.pending

class TaskUpdateStatus(BaseModel):
    status: TaskStatusEnum

class TaskOut(TaskBase):
    id: int
    status: TaskStatusEnum
    owner_id: int
    created_at: datetime
    class Config:
        from_attributes = True
