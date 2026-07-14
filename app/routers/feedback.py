from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


@router.post("/", response_model=schemas.FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    interview = db.query(models.Interview).filter(
        models.Interview.id == feedback.interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    if interview.status != "Completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback can be added only after interview is completed"
        )

    if current_user.role == "Interviewer" and interview.interviewer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can submit feedback only for your assigned interviews"
        )

    existing_feedback = db.query(models.Feedback).filter(
        models.Feedback.interview_id == feedback.interview_id
    ).first()

    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback already submitted"
        )

    new_feedback = models.Feedback(**feedback.model_dump())

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return new_feedback


@router.get("/{interview_id}", response_model=schemas.FeedbackResponse)
def get_feedback(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    feedback = db.query(models.Feedback).filter(
        models.Feedback.interview_id == interview_id
    ).first()

    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )

    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id
    ).first()

    if (
        current_user.role == "Interviewer"
        and interview.interviewer_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return feedback