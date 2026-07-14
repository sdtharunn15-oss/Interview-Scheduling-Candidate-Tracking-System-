from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/candidates", response_model=list[schemas.CandidateResponse])
def search_candidates(
    skill: str = "",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    skip = (page - 1) * limit

    candidates = (
        db.query(models.Candidate)
        .filter(models.Candidate.skill_set.ilike(f"%{skill}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return candidates


@router.get("/interviews", response_model=list[schemas.InterviewResponse])
def filter_interviews(
    status: str = None,
    interviewer: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    skip = (page - 1) * limit

    query = db.query(models.Interview)

    if status:
        query = query.filter(models.Interview.status == status)

    if interviewer:
        query = query.filter(models.Interview.interviewer_id == interviewer)

    interviews = query.offset(skip).limit(limit).all()

    return interviews


@router.get("/selected", response_model=list[schemas.CandidateResponse])
def selected_candidates(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    skip = (page - 1) * limit

    return (
        db.query(models.Candidate)
        .filter(models.Candidate.application_status == "Selected")
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/rejected", response_model=list[schemas.CandidateResponse])
def rejected_candidates(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    skip = (page - 1) * limit

    return (
        db.query(models.Candidate)
        .filter(models.Candidate.application_status == "Rejected")
        .offset(skip)
        .limit(limit)
        .all()
    )