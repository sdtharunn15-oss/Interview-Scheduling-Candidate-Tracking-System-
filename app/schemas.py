from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================
# Authentication
# ==========================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# ==========================
# Candidate
# ==========================

class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=10)
    experience: float
    skill_set: str
    application_status: str = "Applied"


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(CandidateBase):
    pass


class CandidateResponse(CandidateBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Interview
# ==========================

class InterviewBase(BaseModel):
    candidate_id: int
    interviewer_id: int
    interview_date: date
    interview_time: time
    interview_mode: str
    status: str = "Scheduled"


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(InterviewBase):
    pass


class InterviewResponse(InterviewBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Feedback
# ==========================

class FeedbackBase(BaseModel):
    interview_id: int
    technical_rating: int = Field(..., ge=1, le=10)
    communication_rating: int = Field(..., ge=1, le=10)
    remarks: str


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackResponse(FeedbackBase):
    id: int

    model_config = ConfigDict(from_attributes=True)