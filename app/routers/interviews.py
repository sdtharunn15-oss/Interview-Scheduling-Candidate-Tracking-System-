from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)


@router.post("/", response_model=schemas.InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(
    interview: schemas.InterviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin and HR can schedule interviews"
        )

    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == interview.candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    interviewer = db.query(models.User).filter(
        models.User.id == interview.interviewer_id,
        models.User.role == "Interviewer"
    ).first()

    if not interviewer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interviewer not found"
        )

    duplicate = db.query(models.Interview).filter(
        models.Interview.candidate_id == interview.candidate_id,
        models.Interview.interview_date == interview.interview_date,
        models.Interview.interview_time == interview.interview_time
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview already scheduled for this candidate at the same date and time"
        )

    new_interview = models.Interview(**interview.model_dump())

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return new_interview


@router.get("/", response_model=list[schemas.InterviewResponse])
def get_interviews(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role == "Interviewer":
        return db.query(models.Interview).filter(
            models.Interview.interviewer_id == current_user.id
        ).all()

    return db.query(models.Interview).all()


@router.get("/{interview_id}", response_model=schemas.InterviewResponse)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    if (
        current_user.role == "Interviewer"
        and interview.interviewer_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return interview


@router.put("/{interview_id}", response_model=schemas.InterviewResponse)
def update_interview(
    interview_id: int,
    interview_data: schemas.InterviewUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin and HR can update interviews"
        )

    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    duplicate = db.query(models.Interview).filter(
        models.Interview.candidate_id == interview_data.candidate_id,
        models.Interview.interview_date == interview_data.interview_date,
        models.Interview.interview_time == interview_data.interview_time,
        models.Interview.id != interview_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate interview schedule"
        )

    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == interview_data.candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    interviewer = db.query(models.User).filter(
        models.User.id == interview_data.interviewer_id,
        models.User.role == "Interviewer"
    ).first()

    if not interviewer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interviewer not found"
        )

    interview.candidate_id = interview_data.candidate_id
    interview.interviewer_id = interview_data.interviewer_id
    interview.interview_date = interview_data.interview_date
    interview.interview_time = interview_data.interview_time
    interview.interview_mode = interview_data.interview_mode
    interview.status = interview_data.status

    db.commit()
    db.refresh(interview)

    return interview

