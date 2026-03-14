from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    xp: int
    rank: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LabResponse(BaseModel):
    id: int
    title: str
    difficulty: str
    status: str
    icon: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class FriendResponse(BaseModel):
    username: str
    status: str

class DownloadResponse(BaseModel):
    id: int
    file_name: str
    progress: int
    time_remaining: str

    model_config = ConfigDict(from_attributes=True)

class PerformanceResponse(BaseModel):
    missions_completed: int
    success_rate: int
    weekly_activity: List[int]

class XPTrendResponse(BaseModel):
    labels: List[str]
    values: List[int]

class LeaderboardEntry(BaseModel):
    id: int
    user_id: int
    username: str
    xp: int
    rank_position: int

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class LabCompletionRequest(BaseModel):
    user_id: int
    lab_id: str

class UserProgressResponse(BaseModel):
    labs_completed: int
    ctf_completed: int
    xp: int
